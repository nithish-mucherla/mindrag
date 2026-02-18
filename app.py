"""
app.py — MindRAG Chainlit Application

A psychoeducation RAG agent grounded strictly in NIMH and APA guidelines.

Start with:
    chainlit run app.py
"""

import os
from pathlib import Path

import chainlit as cl
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain_cohere import CohereEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_groq import ChatGroq
from qdrant_client import QdrantClient

from safety import is_crisis, is_in_scope, CRISIS_RESOURCES, OUT_OF_SCOPE_RESPONSE

load_dotenv()

# ── Config ────────────────────────────────────────────────────────────────────
QDRANT_URL      = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY  = os.getenv("QDRANT_API_KEY", "")
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "mindrag_psychoeducation")
EMBED_MODEL     = os.getenv("COHERE_EMBED_MODEL", "embed-english-light-v3.0")
GROQ_MODEL      = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
TOP_K           = int(os.getenv("TOP_K", "5"))

# ── System Prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are MindRAG, a mental health psychoeducation assistant.

Your role is to help people UNDERSTAND mental health — not to diagnose, treat, or prescribe.

STRICT RULES you must ALWAYS follow:
1. Answer ONLY using the provided context below. Do not use outside knowledge.
2. If the context does not contain enough information to answer, say:
   "I don't have reliable information on that in my current knowledge base. Please consult a mental health professional or visit nimh.nih.gov."
3. NEVER diagnose the user or suggest they have any condition.
4. NEVER recommend specific medications, dosages, or treatment plans.
5. ALWAYS end your response with a source citation in this exact format:
   📚 Source: [Authority] — [URL]
6. ALWAYS include this disclaimer at the very end:
   ⚕️ *This information is for educational purposes only and does not replace professional medical advice. Please consult a licensed mental health professional for personal guidance.*

Your tone should be:
- Warm, clear, and accessible — explain clinical terms in plain language
- Non-judgmental and supportive
- Factual and grounded — never speculative

CONTEXT FROM APPROVED SOURCES:
{context}
"""

USER_PROMPT = """Question: {question}

Please answer based strictly on the context provided above."""


# ── Helpers ───────────────────────────────────────────────────────────────────
def format_context(docs) -> str:
    """Format retrieved documents into a clean context string with source labels."""
    sections = []
    seen_urls = set()
    for doc in docs:
        url       = doc.metadata.get("source_url", "Unknown")
        authority = doc.metadata.get("authority", "Unknown")
        topic     = doc.metadata.get("topic", "general")
        if url not in seen_urls:
            seen_urls.add(url)
        sections.append(
            f"[Source: {authority} | Topic: {topic} | URL: {url}]\n{doc.page_content}"
        )
    return "\n\n---\n\n".join(sections)


def format_sources(docs) -> str:
    """Return a deduplicated, formatted list of sources used."""
    seen = set()
    lines = []
    for doc in docs:
        url       = doc.metadata.get("source_url", "")
        authority = doc.metadata.get("authority", "")
        topic     = doc.metadata.get("topic", "")
        key = url
        if key and key not in seen:
            seen.add(key)
            lines.append(f"- **{authority}** ({topic}): {url}")
    return "\n".join(lines) if lines else "- Source information unavailable"


# ── App Startup ───────────────────────────────────────────────────────────────
@cl.on_chat_start
async def on_chat_start():
    """Initialize the RAG chain and store in user session."""

    # Validate Qdrant Cloud credentials
    if not QDRANT_API_KEY:
        await cl.Message(
            content=(
                "⚠️ **Qdrant Cloud not configured.**\n\n"
                "Please set QDRANT_URL and QDRANT_API_KEY in your .env file.\n\n"
                "Steps:\n"
                "1. Create a Qdrant Cloud account at https://cloud.qdrant.io\n"
                "2. Create a cluster\n"
                "3. Copy the API URL and API key to your .env\n"
                "4. Run `python ingest.py` to populate the vector database\n"
                "5. Restart this app."
            )
        ).send()
        return

    # Load embeddings
    embeddings = CohereEmbeddings(
        model=EMBED_MODEL,
        cohere_api_key=os.getenv("COHERE_API_KEY"),
    )

    # Create Qdrant Cloud client
    qdrant_client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
    )

    # Connect to Qdrant Cloud
    vectorstore = QdrantVectorStore(
        client=qdrant_client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings,
    )
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": TOP_K},
    )

    # Build LLM
    llm = ChatGroq(
        model=GROQ_MODEL,
        temperature=0.2,
        groq_api_key=os.getenv("GROQ_API_KEY"),
    )

    # Build RAG chain
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human",  USER_PROMPT),
    ])

    rag_chain = (
        {"context": retriever | format_context, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # Store in session
    cl.user_session.set("rag_chain", rag_chain)
    cl.user_session.set("retriever", retriever)

    # Welcome message
    await cl.Message(
        content=(
            "## 👋 Welcome to MindRAG\n\n"
            "I'm a mental health **psychoeducation** assistant grounded in "
            "**NIMH** and **APA** guidelines.\n\n"
            "I can help you **understand** mental health conditions, therapies, "
            "and coping strategies — but I'm not a substitute for professional care.\n\n"
            "**Try asking me:**\n"
            "- *What is generalized anxiety disorder?*\n"
            "- *How does CBT work for depression?*\n"
            "- *What are the symptoms of PTSD?*\n"
            "- *What's the difference between bipolar I and II?*\n\n"
            "---\n"
            "⚠️ *In crisis? Contact emergency services or a local crisis helpline in your country.*"
        )
    ).send()


# ── Message Handler ───────────────────────────────────────────────────────────
@cl.on_message
async def on_message(message: cl.Message):
    """Handle each user message through the safety + RAG pipeline."""
    user_query = message.content.strip()

    if not user_query:
        return

    rag_chain = cl.user_session.get("rag_chain")
    retriever = cl.user_session.get("retriever")

    if not rag_chain:
        await cl.Message(
            content="⚠️ Session not initialized. Please refresh the page."
        ).send()
        return

    # ── Layer 1: Crisis Detection ─────────────────────────────────────────────
    thinking_msg = cl.Message(content="Identifying potential crisis...")
    await thinking_msg.send()
    
    if is_crisis(user_query):
        thinking_msg.content = (
                "I want to make sure you're okay. "
                "It sounds like you might be going through something really difficult right now.\n\n"
                + CRISIS_RESOURCES
                + "\n\nIf you'd like to continue learning about mental health topics, "
                "I'm here for that too. 💙"
            )
        await thinking_msg.update()
        return

    thinking_msg.content = "Checking if your question is within my scope..."
    await thinking_msg.update()
    # ── Layer 2: Scope Check ──────────────────────────────────────────────────
    if not is_in_scope(user_query):
        thinking_msg.content = OUT_OF_SCOPE_RESPONSE
        await thinking_msg.update()
        return


    thinking_msg.content = "Retrieving relevant information and formulating a response..."
    await thinking_msg.update()
    # ── Layer 3: RAG Pipeline ─────────────────────────────────────────────────
    # Retrieve docs for source display
    try:
        docs = retriever.invoke(user_query)
        sources_text = format_sources(docs)
    except Exception:
        docs = []
        sources_text = ""

    thinking_msg.content = ""
    await thinking_msg.update()
    # Stream response
    response_text = ""
    try:
        async for chunk in rag_chain.astream(user_query):
            response_text += chunk
            await thinking_msg.stream_token(chunk)
    except Exception as e:
        thinking_msg.content = f"⚠️ Something went wrong: {str(e)}\n\nPlease try again."
        await thinking_msg.update()
        return

    await thinking_msg.update()

    # Show retrieved sources as a collapsible element
    if sources_text:
        sources_element = cl.Text(
            name="📚 Retrieved Sources",
            content=f"**Sources consulted for this answer:**\n\n{sources_text}",
            display="side",
        )
        await cl.Message(
            content="",
            elements=[sources_element],
        ).send()
