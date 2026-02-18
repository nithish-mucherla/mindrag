"""
ingest.py — MindRAG Ingestion Pipeline

Scrapes approved NIMH/APA sources, chunks them, embeds with Cohere,
and stores in Qdrant Cloud vector database.

Run once before starting the app:
    python ingest.py
"""

import os
import time
import hashlib
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_cohere import CohereEmbeddings
from langchain_qdrant import QdrantVectorStore

from corpus_sources import CORPUS_SOURCES

load_dotenv()

# ── Config ────────────────────────────────────────────────────────────────────
QDRANT_URL      = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY  = os.getenv("QDRANT_API_KEY", "")
CHUNK_SIZE      = 512
CHUNK_OVERLAP   = 64
EMBED_MODEL     = os.getenv("COHERE_EMBED_MODEL", "embed-english-light-v3.0")
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "mindrag_psychoeducation")

# Tags to strip from HTML (nav, footer, etc. — not content)
STRIP_TAGS = ["nav", "header", "footer", "script", "style", "aside", "form"]


# ── HTML Scraper ──────────────────────────────────────────────────────────────
def scrape_page(url: str) -> str:
    """Fetch a URL and return clean body text, stripping boilerplate HTML."""
    headers = {"User-Agent": "MindRAG-Educational-Bot/1.0 (Research project)"}
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"  ⚠️  Failed to fetch {url}: {e}")
        return ""

    soup = BeautifulSoup(resp.text, "html.parser")

    # Remove boilerplate elements
    for tag in STRIP_TAGS:
        for el in soup.find_all(tag):
            el.decompose()

    # Try main content area first, fall back to body
    main = soup.find("main") or soup.find("article") or soup.find("body")
    if not main:
        return ""

    # Clean up whitespace
    text = main.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines()]
    text = "\n".join(line for line in lines if line)
    return text


# ── Document Builder ──────────────────────────────────────────────────────────
def build_documents() -> list[Document]:
    """Scrape all corpus sources and return LangChain Documents with metadata."""
    documents = []
    print(f"\n📥 Scraping {len(CORPUS_SOURCES)} approved sources...\n")

    for source in CORPUS_SOURCES:
        url       = source["url"]
        topic     = source["topic"]
        authority = source["authority"]

        print(f"  → [{authority}] {topic} — {url}")
        text = scrape_page(url)

        if not text or len(text) < 200:
            print(f"     ⚠️  Skipped (too short or empty)")
            continue

        doc = Document(
            page_content=text,
            metadata={
                "source_url": url,
                "topic":      topic,
                "authority":  authority,
                "source_id":  hashlib.md5(url.encode()).hexdigest()[:8],
            },
        )
        documents.append(doc)
        time.sleep(0.5)  # Be polite to servers

    print(f"\n✅ Scraped {len(documents)} documents successfully.\n")
    return documents


# ── Chunker ───────────────────────────────────────────────────────────────────
def chunk_documents(documents: list[Document]) -> list[Document]:
    """Split documents into chunks, preserving metadata on each chunk."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(documents)

    # Add chunk index to metadata for traceability
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_index"] = i

    print(f"📄 Created {len(chunks)} chunks from {len(documents)} documents.")
    return chunks


# ── Embedder + Vector Store ───────────────────────────────────────────────────
def build_vectorstore(chunks: list[Document]) -> QdrantVectorStore:
    """Embed chunks with Cohere and persist to Qdrant Cloud."""
    print(f"\n🔢 Embedding {len(chunks)} chunks with Cohere ({EMBED_MODEL})...")
    print("   This may take a minute on first run...\n")

    embeddings = CohereEmbeddings(
        model=EMBED_MODEL,
        cohere_api_key=os.getenv("COHERE_API_KEY"),
    )

    # Create vectorstore and upload to Qdrant Cloud
    # Pass connection params directly instead of pre-instantiated client
    vectorstore = QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
    )

    print(f"✅ Vector store created and published to Qdrant Cloud")
    print(f"   URL: {QDRANT_URL}/collections/{COLLECTION_NAME}")
    print(f"   Collection: {COLLECTION_NAME}")
    print(f"   Total vectors: {len(chunks)}\n")
    return vectorstore


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    # Validate Qdrant Cloud credentials
    if not QDRANT_API_KEY:
        print("❌ QDRANT_API_KEY not set in .env")
        print("   Please configure Qdrant Cloud credentials and try again.")
        return

    documents = build_documents()
    if not documents:
        print("❌ No documents scraped. Check your internet connection.")
        return

    chunks = chunk_documents(documents)
    build_vectorstore(chunks)

    print("🎉 Ingestion complete! You can now run: chainlit run app.py")


if __name__ == "__main__":
    main()
