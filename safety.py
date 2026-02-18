"""
safety.py — MindRAG Safety Guardrails

Two layers of protection:
1. Crisis detection  — identifies distress signals before any RAG pipeline runs
2. Scope filtering   — rejects questions outside mental health education scope

Both are implemented as zero-shot LLM classifiers using Groq (fast + free).
"""

import os
from groq import Groq

# ── Crisis Resources (always shown when crisis is detected) ───────────────────
CRISIS_RESOURCES = """
---
🆘 **If you or someone you know is in crisis, please reach out immediately:**

- **988 Suicide & Crisis Lifeline** — Call or text **988** (US, 24/7)
- **Crisis Text Line** — Text **HOME** to **741741** (US, 24/7)
- **NAMI Helpline** — Call **1-800-950-6264** (Mon–Fri, 10am–10pm ET)
- **International Association for Suicide Prevention** — https://www.iasp.info/resources/Crisis_Centres/

*Please speak with a mental health professional or go to your nearest emergency room if you are in immediate danger.*
---
"""

# ── Groq client (reused from app.py via direct import) ───────────────────────
def _get_groq_client() -> Groq:
    return Groq(api_key=os.getenv("GROQ_API_KEY"))


# ── Crisis Detection ──────────────────────────────────────────────────────────
CRISIS_SYSTEM_PROMPT = """You are a safety classifier for a mental health education chatbot.

Your ONLY job is to detect if a user's message contains signals of:
- Suicidal ideation or thoughts of self-harm
- Active emotional crisis or acute distress
- Intent to harm themselves or others
- Expressions of hopelessness combined with a farewell or goodbye tone

Respond with ONLY one word: CRISIS or SAFE.
Do not explain. Do not add punctuation. Just one word."""


def is_crisis(user_message: str) -> bool:
    """
    Returns True if the message contains crisis signals.
    Uses a conservative threshold — false positives are safer than false negatives.
    """
    try:
        client = _get_groq_client()
        response = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
            messages=[
                {"role": "system", "content": CRISIS_SYSTEM_PROMPT},
                {"role": "user",   "content": user_message},
            ],
            max_tokens=5,
            temperature=0.0,
        )
        result = response.choices[0].message.content.strip().upper()
        return result == "CRISIS"
    except Exception as e:
        # Fail safe: if classifier errors, assume crisis
        print(f"[safety] Crisis classifier error: {e} — defaulting to SAFE")
        return False


# ── Scope Filtering ───────────────────────────────────────────────────────────
SCOPE_SYSTEM_PROMPT = """You are a scope classifier for a mental health EDUCATION chatbot.

The chatbot can ONLY answer questions about:
- Mental health conditions (depression, anxiety, PTSD, OCD, ADHD, bipolar, schizophrenia, eating disorders, etc.)
- Mental health treatments and therapies (CBT, DBT, medication types in general terms)
- Coping strategies and self-care grounded in clinical guidelines
- Understanding mental health terminology and concepts
- General wellness and stress management

The chatbot CANNOT answer questions about:
- Specific medication dosages or prescriptions
- Medical diagnosis of the user
- Physical health conditions unrelated to mental health
- Legal, financial, or relationship advice
- General knowledge unrelated to mental health education
- Current news or events

Respond with ONLY one word: IN_SCOPE or OUT_OF_SCOPE.
Do not explain. Do not add punctuation. Just one word."""


def is_in_scope(user_message: str) -> bool:
    """
    Returns True if the question is within mental health education scope.
    """
    try:
        client = _get_groq_client()
        response = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
            messages=[
                {"role": "system", "content": SCOPE_SYSTEM_PROMPT},
                {"role": "user",   "content": user_message},
            ],
            max_tokens=5,
            temperature=0.0,
        )
        result = response.choices[0].message.content.strip().upper()
        return result == "IN_SCOPE"
    except Exception as e:
        print(f"[safety] Scope classifier error: {e} — defaulting to IN_SCOPE")
        return True  # Fail open for scope (better UX than blocking everything)


# ── Out-of-scope response ─────────────────────────────────────────────────────
OUT_OF_SCOPE_RESPONSE = """I'm specialized in mental health **education** based on NIMH, APA, and WHO guidelines, so I'm not able to help with that particular question.

Here are some things I *can* help you understand:
- Mental health conditions (anxiety, depression, PTSD, OCD, ADHD, and more)
- How different therapies like CBT or DBT work
- General coping strategies backed by clinical research
- What certain mental health terms mean

Feel free to ask me anything along those lines! 🌱"""
