# 🧠 MindRAG — Mental Health Psychoeducation RAG Agent

A RAG-powered chatbot for mental health education, grounded **strictly** in
NIMH and APA guidelines. Built as a learning project with a path to deployment.

---

## 🗂️ Project Structure

```
mindrag/
├── app.py              # Chainlit chat app (main entry point)
├── ingest.py           # One-time ingestion pipeline
├── safety.py           # Crisis detection + scope filtering
├── corpus_sources.py   # Approved NIMH/APA source URLs
├── chainlit.toml       # Chainlit UI config
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
└── vectorstore/        # Auto-created by ingest.py (Chroma DB)
```

---

## ⚡ Setup in 5 Steps

### 1. Clone & create virtual environment

```bash
git clone <your-repo>
cd mindrag
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Get your free API keys

| Service    | Where to get it              | Free tier                      |
| ---------- | ---------------------------- | ------------------------------ |
| **Groq**   | https://console.groq.com     | Very generous — no credit card |
| **Cohere** | https://dashboard.cohere.com | 1000 calls/min free            |

### 4. Set up environment variables

```bash
cp .env.example .env
# Edit .env and fill in your GROQ_API_KEY and COHERE_API_KEY
```

### 5. Run ingestion (once)

```bash
python ingest.py
```

This scrapes ~15 NIMH/APA pages, chunks them, embeds with Cohere,
and saves a local Chroma vector DB. Takes ~1–2 minutes.

### 6. Launch the app

```bash
chainlit run app.py
```

Open http://localhost:8000 in your browser. 🎉

---

## 🏗️ Architecture

```
User Query
    │
    ▼
┌─────────────────────┐
│  Safety Pre-filter  │  ← Crisis detection + scope check (Groq, zero-shot)
└─────────────────────┘
    │ (safe + in-scope)
    ▼
┌─────────────────────┐
│  Chroma Retriever   │  ← Similarity search over NIMH/APA chunks (Cohere embeddings)
└─────────────────────┘
    │ top-5 chunks
    ▼
┌─────────────────────┐
│  RAG Prompt         │  ← Strict grounding rules + mandatory citation
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  Groq LLM           │  ← llama-3.1-8b-instant (fast + free)
└─────────────────────┘
    │
    ▼
  Streamed response with source citations
```

---

## 🛡️ Safety Guardrails

| Guardrail                | What it does                                                             |
| ------------------------ | ------------------------------------------------------------------------ |
| **Crisis Detection**     | Classifies distress signals → shows local crisis resources and helplines |
| **Scope Filter**         | Rejects out-of-scope questions (diagnosis, medication, etc.)             |
| **Hard Rules in Prompt** | No diagnosis, no prescriptions, always cite sources                      |
| **Strict Grounding**     | LLM only uses retrieved context — no hallucination from training data    |

---

## ⚠️ Important Disclaimer

This tool is for **educational purposes only**. It does not provide medical advice,
diagnosis, or treatment. Always consult a licensed mental health professional.
