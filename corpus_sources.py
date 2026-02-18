"""
corpus_sources.py — MindRAG Enriched Corpus

Curated sub-pages from NIMH and APA only.
Expanded from index/landing pages to the actual detailed content pages:
  - /health/publications/ — in-depth NIMH booklets and fact sheets
  - /health/statistics/   — prevalence and epidemiology data
  - /patients-families/   — APA condition pages, FAQs, expert Q&As

Do NOT add sources outside NIMH and APA for the MVP.
"""

CORPUS_SOURCES = [

    # ══════════════════════════════════════════════════════════════════════
    # NIMH — DEPRESSION
    # ══════════════════════════════════════════════════════════════════════
    {"url": "https://www.nimh.nih.gov/health/topics/depression",                         "topic": "depression",       "authority": "NIMH", "content_type": "overview"},
    {"url": "https://www.nimh.nih.gov/health/publications/depression",                   "topic": "depression",       "authority": "NIMH", "content_type": "publication"},
    {"url": "https://www.nimh.nih.gov/health/publications/postpartum-depression-facts",  "topic": "depression",       "authority": "NIMH", "content_type": "publication"},
    {"url": "https://www.nimh.nih.gov/health/publications/seasonal-affective-disorder",  "topic": "depression",       "authority": "NIMH", "content_type": "publication"},
    {"url": "https://www.nimh.nih.gov/health/statistics/major-depression",               "topic": "depression",       "authority": "NIMH", "content_type": "statistics"},

    # ══════════════════════════════════════════════════════════════════════
    # NIMH — ANXIETY
    # ══════════════════════════════════════════════════════════════════════
    {"url": "https://www.nimh.nih.gov/health/topics/anxiety-disorders",                  "topic": "anxiety",          "authority": "NIMH", "content_type": "overview"},
    {"url": "https://www.nimh.nih.gov/health/publications/anxiety-disorders",            "topic": "anxiety",          "authority": "NIMH", "content_type": "publication"},
    {"url": "https://www.nimh.nih.gov/health/topics/panic-disorder",                     "topic": "anxiety",          "authority": "NIMH", "content_type": "overview"},
    {"url": "https://www.nimh.nih.gov/health/topics/social-anxiety-disorder-social-phobia", "topic": "anxiety",       "authority": "NIMH", "content_type": "overview"},
    {"url": "https://www.nimh.nih.gov/health/statistics/any-anxiety-disorder",           "topic": "anxiety",          "authority": "NIMH", "content_type": "statistics"},

    # ══════════════════════════════════════════════════════════════════════
    # NIMH — PTSD
    # ══════════════════════════════════════════════════════════════════════
    {"url": "https://www.nimh.nih.gov/health/topics/post-traumatic-stress-disorder-ptsd","topic": "ptsd",             "authority": "NIMH", "content_type": "overview"},
    {"url": "https://www.nimh.nih.gov/health/publications/post-traumatic-stress-disorder-ptsd", "topic": "ptsd",      "authority": "NIMH", "content_type": "publication"},
    {"url": "https://www.nimh.nih.gov/health/statistics/post-traumatic-stress-disorder-ptsd",   "topic": "ptsd",      "authority": "NIMH", "content_type": "statistics"},

    # ══════════════════════════════════════════════════════════════════════
    # NIMH — BIPOLAR DISORDER
    # ══════════════════════════════════════════════════════════════════════
    {"url": "https://www.nimh.nih.gov/health/topics/bipolar-disorder",                   "topic": "bipolar disorder", "authority": "NIMH", "content_type": "overview"},
    {"url": "https://www.nimh.nih.gov/health/publications/bipolar-disorder",             "topic": "bipolar disorder", "authority": "NIMH", "content_type": "publication"},
    {"url": "https://www.nimh.nih.gov/health/statistics/bipolar-disorder",               "topic": "bipolar disorder", "authority": "NIMH", "content_type": "statistics"},

    # ══════════════════════════════════════════════════════════════════════
    # NIMH — SCHIZOPHRENIA
    # ══════════════════════════════════════════════════════════════════════
    {"url": "https://www.nimh.nih.gov/health/topics/schizophrenia",                      "topic": "schizophrenia",    "authority": "NIMH", "content_type": "overview"},
    {"url": "https://www.nimh.nih.gov/health/publications/schizophrenia",                "topic": "schizophrenia",    "authority": "NIMH", "content_type": "publication"},
    {"url": "https://www.nimh.nih.gov/health/statistics/schizophrenia",                  "topic": "schizophrenia",    "authority": "NIMH", "content_type": "statistics"},

    # ══════════════════════════════════════════════════════════════════════
    # NIMH — OCD
    # ══════════════════════════════════════════════════════════════════════
    {"url": "https://www.nimh.nih.gov/health/topics/obsessive-compulsive-disorder-ocd",  "topic": "ocd",              "authority": "NIMH", "content_type": "overview"},
    {"url": "https://www.nimh.nih.gov/health/publications/obsessive-compulsive-disorder-when-unwanted-thoughts-or-repetitive-behaviors-take-over", "topic": "ocd", "authority": "NIMH", "content_type": "publication"},
    {"url": "https://www.nimh.nih.gov/health/statistics/obsessive-compulsive-disorder-ocd", "topic": "ocd",           "authority": "NIMH", "content_type": "statistics"},

    # ══════════════════════════════════════════════════════════════════════
    # NIMH — EATING DISORDERS
    # ══════════════════════════════════════════════════════════════════════
    {"url": "https://www.nimh.nih.gov/health/topics/eating-disorders",                   "topic": "eating disorders", "authority": "NIMH", "content_type": "overview"},
    {"url": "https://www.nimh.nih.gov/health/publications/eating-disorders",             "topic": "eating disorders", "authority": "NIMH", "content_type": "publication"},
    {"url": "https://www.nimh.nih.gov/health/statistics/eating-disorders",               "topic": "eating disorders", "authority": "NIMH", "content_type": "statistics"},

    # ══════════════════════════════════════════════════════════════════════
    # NIMH — ADHD
    # ══════════════════════════════════════════════════════════════════════
    {"url": "https://www.nimh.nih.gov/health/topics/attention-deficit-hyperactivity-disorder-adhd", "topic": "adhd",  "authority": "NIMH", "content_type": "overview"},
    {"url": "https://www.nimh.nih.gov/health/publications/attention-deficit-hyperactivity-disorder-adhd-what-you-need-to-know", "topic": "adhd", "authority": "NIMH", "content_type": "publication"},
    {"url": "https://www.nimh.nih.gov/health/statistics/attention-deficit-hyperactivity-disorder-adhd", "topic": "adhd", "authority": "NIMH", "content_type": "statistics"},

    # ══════════════════════════════════════════════════════════════════════
    # NIMH — SUICIDE PREVENTION
    # ══════════════════════════════════════════════════════════════════════
    {"url": "https://www.nimh.nih.gov/health/topics/suicide-prevention",                 "topic": "suicide prevention", "authority": "NIMH", "content_type": "overview"},
    {"url": "https://www.nimh.nih.gov/health/publications/suicide-faq",                  "topic": "suicide prevention", "authority": "NIMH", "content_type": "publication"},
    {"url": "https://www.nimh.nih.gov/health/statistics/suicide",                        "topic": "suicide prevention", "authority": "NIMH", "content_type": "statistics"},

    # ══════════════════════════════════════════════════════════════════════
    # NIMH — THERAPY & TREATMENT
    # ══════════════════════════════════════════════════════════════════════
    {"url": "https://www.nimh.nih.gov/health/topics/psychotherapies",                    "topic": "therapy",          "authority": "NIMH", "content_type": "overview"},
    {"url": "https://www.nimh.nih.gov/health/publications/psychotherapies",              "topic": "therapy",          "authority": "NIMH", "content_type": "publication"},
    {"url": "https://www.nimh.nih.gov/health/topics/mental-health-medications",          "topic": "therapy",          "authority": "NIMH", "content_type": "overview"},
    {"url": "https://www.nimh.nih.gov/health/publications/brain-stimulation-therapies",  "topic": "therapy",          "authority": "NIMH", "content_type": "publication"},
    {"url": "https://www.nimh.nih.gov/health/topics/caring-for-your-mental-health",      "topic": "self care",        "authority": "NIMH", "content_type": "overview"},

    # ══════════════════════════════════════════════════════════════════════
    # NIMH — OTHER CONDITIONS
    # ══════════════════════════════════════════════════════════════════════
    {"url": "https://www.nimh.nih.gov/health/topics/autism-spectrum-disorder-asd",       "topic": "autism",           "authority": "NIMH", "content_type": "overview"},
    {"url": "https://www.nimh.nih.gov/health/topics/borderline-personality-disorder",    "topic": "personality disorders", "authority": "NIMH", "content_type": "overview"},
    {"url": "https://www.nimh.nih.gov/health/topics/men-and-mental-health",              "topic": "men mental health","authority": "NIMH", "content_type": "overview"},
    {"url": "https://www.nimh.nih.gov/health/topics/women-and-mental-health",            "topic": "women mental health", "authority": "NIMH", "content_type": "overview"},
    {"url": "https://www.nimh.nih.gov/health/topics/child-and-adolescent-mental-health", "topic": "child adolescent", "authority": "NIMH", "content_type": "overview"},

    # ══════════════════════════════════════════════════════════════════════
    # APA — DEPRESSION
    # ══════════════════════════════════════════════════════════════════════
    {"url": "https://www.psychiatry.org/patients-families/depression/what-is-depression",      "topic": "depression", "authority": "APA", "content_type": "overview"},
    {"url": "https://www.psychiatry.org/patients-families/depression/depression-faq",          "topic": "depression", "authority": "APA", "content_type": "faq"},

    # ══════════════════════════════════════════════════════════════════════
    # APA — ANXIETY
    # ══════════════════════════════════════════════════════════════════════
    {"url": "https://www.psychiatry.org/patients-families/anxiety-disorders/what-are-anxiety-disorders", "topic": "anxiety", "authority": "APA", "content_type": "overview"},
    {"url": "https://www.psychiatry.org/patients-families/anxiety-disorders/anxiety-faq",                "topic": "anxiety", "authority": "APA", "content_type": "faq"},
    {"url": "https://www.psychiatry.org/patients-families/anxiety-disorders/expert-q-and-a",             "topic": "anxiety", "authority": "APA", "content_type": "expert_qa"},

    # ══════════════════════════════════════════════════════════════════════
    # APA — PTSD
    # ══════════════════════════════════════════════════════════════════════
    {"url": "https://www.psychiatry.org/patients-families/ptsd/what-is-ptsd",            "topic": "ptsd", "authority": "APA", "content_type": "overview"},
    {"url": "https://www.psychiatry.org/patients-families/ptsd/ptsd-faq",                "topic": "ptsd", "authority": "APA", "content_type": "faq"},
    {"url": "https://www.psychiatry.org/patients-families/ptsd/expert-q-and-a",          "topic": "ptsd", "authority": "APA", "content_type": "expert_qa"},

    # ══════════════════════════════════════════════════════════════════════
    # APA — BIPOLAR
    # ══════════════════════════════════════════════════════════════════════
    {"url": "https://www.psychiatry.org/patients-families/bipolar-disorders/what-are-bipolar-disorders", "topic": "bipolar disorder", "authority": "APA", "content_type": "overview"},
    {"url": "https://www.psychiatry.org/patients-families/bipolar-disorders/bipolar-disorder-faq",       "topic": "bipolar disorder", "authority": "APA", "content_type": "faq"},
    {"url": "https://www.psychiatry.org/patients-families/bipolar-disorders/expert-q-and-a",             "topic": "bipolar disorder", "authority": "APA", "content_type": "expert_qa"},

    # ══════════════════════════════════════════════════════════════════════
    # APA — OCD
    # ══════════════════════════════════════════════════════════════════════
    {"url": "https://www.psychiatry.org/patients-families/ocd/what-is-obsessive-compulsive-disorder", "topic": "ocd", "authority": "APA", "content_type": "overview"},
    {"url": "https://www.psychiatry.org/patients-families/ocd/ocd-faq",                               "topic": "ocd", "authority": "APA", "content_type": "faq"},
    {"url": "https://www.psychiatry.org/patients-families/ocd/expert-q-and-a",                        "topic": "ocd", "authority": "APA", "content_type": "expert_qa"},

    # ══════════════════════════════════════════════════════════════════════
    # APA — OTHER CONDITIONS
    # ══════════════════════════════════════════════════════════════════════
    {"url": "https://www.psychiatry.org/patients-families/schizophrenia/what-is-schizophrenia",                      "topic": "schizophrenia",    "authority": "APA", "content_type": "overview"},
    {"url": "https://www.psychiatry.org/patients-families/schizophrenia/schizophrenia-faq",                          "topic": "schizophrenia",    "authority": "APA", "content_type": "faq"},
    {"url": "https://www.psychiatry.org/patients-families/adhd/what-is-adhd",                                        "topic": "adhd",             "authority": "APA", "content_type": "overview"},
    {"url": "https://www.psychiatry.org/patients-families/adhd/adhd-faq",                                            "topic": "adhd",             "authority": "APA", "content_type": "faq"},
    {"url": "https://www.psychiatry.org/patients-families/eating-disorders/what-are-eating-disorders",               "topic": "eating disorders", "authority": "APA", "content_type": "overview"},
    {"url": "https://www.psychiatry.org/patients-families/eating-disorders/eating-disorders-faq",                    "topic": "eating disorders", "authority": "APA", "content_type": "faq"},
    {"url": "https://www.psychiatry.org/patients-families/autism/what-is-autism-spectrum-disorder",                  "topic": "autism",           "authority": "APA", "content_type": "overview"},
    {"url": "https://www.psychiatry.org/patients-families/borderline-personality-disorder/what-is-borderline-personality-disorder", "topic": "personality disorders", "authority": "APA", "content_type": "overview"},
    {"url": "https://www.psychiatry.org/patients-families/sleep-disorders/what-are-sleep-disorders",                 "topic": "sleep disorders",  "authority": "APA", "content_type": "overview"},
    {"url": "https://www.psychiatry.org/patients-families/addiction-substance-use-disorders/what-is-a-substance-use-disorder", "topic": "substance use", "authority": "APA", "content_type": "overview"},
    {"url": "https://www.psychiatry.org/patients-families/suicide/what-is-suicide",                                  "topic": "suicide prevention", "authority": "APA", "content_type": "overview"},
    {"url": "https://www.psychiatry.org/patients-families/suicide/suicide-faq",                                      "topic": "suicide prevention", "authority": "APA", "content_type": "faq"},

    # ══════════════════════════════════════════════════════════════════════
    # APA — THERAPY
    # ══════════════════════════════════════════════════════════════════════
    {"url": "https://www.psychiatry.org/patients-families/psychotherapy",                                            "topic": "therapy",          "authority": "APA", "content_type": "overview"},
    {"url": "https://www.psychiatry.org/patients-families/what-is-psychiatry-and-mental-illness",                   "topic": "mental health general", "authority": "APA", "content_type": "overview"},
]


# ── Summary (run directly to inspect corpus) ──────────────────────────────────
if __name__ == "__main__":
    from collections import Counter
    authorities = Counter(s["authority"]    for s in CORPUS_SOURCES)
    topics      = Counter(s["topic"]        for s in CORPUS_SOURCES)
    ctypes      = Counter(s["content_type"] for s in CORPUS_SOURCES)

    print(f"\n📚 Enriched Corpus Summary")
    print(f"   Total sources  : {len(CORPUS_SOURCES)}")
    print(f"   By authority   : {dict(authorities)}")
    print(f"\n   By content type: {dict(ctypes)}")
    print(f"\n   By topic:")
    for topic, count in sorted(topics.items()):
        print(f"     {topic:<40} {count} source(s)")
    print()
