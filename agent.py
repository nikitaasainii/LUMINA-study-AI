

"""
agent.py — The agentic brain of Lumina Study AI

Flow (ReAct loop):
  1. PLAN   → decide what to search for
  2. ACT    → search DuckDuckGo + Wikipedia
  3. OBSERVE → read and filter results
  4. GENERATE → call Gemini to produce study plan
"""

import os
import urllib.request
import urllib.parse
import json
import requests
from dotenv import load_dotenv
from duckduckgo_search import DDGS

load_dotenv()


# ── Tool 1: Web Search (DuckDuckGo) ──────────────────────────────────────────
def search_web(query: str, max_results: int = 5) -> list:
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        return results
    except Exception as e:
        return [{"title": "Search failed", "body": str(e), "href": ""}]


# ── Tool 2: Wikipedia Summary ─────────────────────────────────────────────────
def search_wikipedia(topic: str) -> str:
    try:
        encoded = urllib.parse.quote(topic.replace(" ", "_"))
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded}"
        req = urllib.request.Request(url, headers={"User-Agent": "LuminaStudyAI/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            return data.get("extract", "No Wikipedia summary found.")
    except Exception:
        return "Wikipedia lookup failed."


# ── Tool 3: Format search results ────────────────────────────────────────────
def format_search_context(results: list) -> str:
    lines = []
    for r in results:
        title = r.get("title", "")
        body  = r.get("body", r.get("snippet", ""))
        href  = r.get("href", r.get("link", ""))
        lines.append(f"• {title}\n  {body}\n  Source: {href}")
    return "\n\n".join(lines)


# ── Call Gemini via REST API directly (bypasses library DNS issue) ────────────
def call_groq(prompt: str) -> str:
    from groq import Groq
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found.")
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


# ── Main Agent ────────────────────────────────────────────────────────────────
def run_agent(topic: str, depth: str, hours: int) -> str:

    # ── STEP 1: PLAN ─────────────────────────────────────────────────────────
    search_queries = [
        f"{topic} introduction overview",
        f"{topic} key concepts explained",
        f"how to learn {topic} resources"
    ]

    # ── STEP 2: ACT ───────────────────────────────────────────────────────────
    all_results = []
    for query in search_queries:
        results = search_web(query, max_results=3)
        all_results.extend(results)

    wiki_summary = search_wikipedia(topic)

    # ── STEP 3: OBSERVE ───────────────────────────────────────────────────────
    web_context  = format_search_context(all_results)
    full_context = f"Wikipedia Summary:\n{wiki_summary}\n\nWeb Results:\n{web_context}"

    # ── STEP 4: GENERATE ──────────────────────────────────────────────────────
    depth_map = {
        "Beginner Overview":      "beginner-friendly, avoid jargon, focus on fundamentals",
        "Intermediate Deep Dive": "intermediate level, include technical concepts and practical applications",
        "Advanced Research":      "advanced level, include research papers, cutting-edge developments, and deep technical detail"
    }
    depth_instruction = depth_map.get(depth, "beginner-friendly")

    prompt = f"""
You are Lumina Study AI, an expert academic learning assistant.

A student wants to learn about: **{topic}**
Depth level: {depth} ({depth_instruction})
Available study time: {hours} hours

You have gathered the following real-time information from the web:

---
{full_context}
---

Using this information, generate a comprehensive, personalised study plan in Markdown format with:

1. **Topic Overview** — What is {topic} and why does it matter? (3-4 sentences)
2. **Key Concepts to Master** — List the 5-7 most important concepts to understand
3. **Recommended Learning Path** — Step-by-step sequence broken into the {hours} hours available
4. **Best Free Resources** — Specific websites, YouTube channels, or tools (use the search results)
5. **Quick Reference** — 3-5 bullet points the student should memorise
6. **Knowledge Check** — 3 questions the student should be able to answer after studying

Make it motivating, clear, and actionable. Use emojis sparingly to make it readable.
Format everything neatly in Markdown.
"""

    try:
        return call_groq(prompt)
    except Exception as e:
          return f"⚠️ Error calling Groq API: {str(e)}"
