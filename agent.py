"""
agent.py — The agentic brain of Lumina Study AI

Flow (ReAct loop):
  1. PLAN   → decide what to search for
  2. ACT    → search DuckDuckGo + Wikipedia
  3. OBSERVE → read and filter results
  4. GENERATE → call Groq/LLM to produce structured timetable study plan
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


# ── Call Groq ─────────────────────────────────────────────────────────────────
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

    # Calculate session breakdown
    if hours <= 3:
        session_label = "hours"
        sessions = hours
        session_duration = "1 hour"
    elif hours <= 24:
        sessions = min(hours, 8)
        session_label = "sessions"
        session_duration = f"{round(hours/sessions, 1)} hours"
    else:
        sessions = min(round(hours / 8), 14)
        session_label = "days"
        session_duration = f"{round(hours/sessions)} hours/day"

    prompt = f"""
You are Lumina Study AI, an expert academic learning assistant.

A student wants to learn about: **{topic}**
Depth level: {depth} ({depth_instruction})
Total available study time: {hours} hours

You have gathered the following real-time information from the web:
---
{full_context}
---

Generate a STRUCTURED TIMETABLE STUDY PLAN in clean Markdown. Follow this EXACT format:

---

## Overview
Write 3-4 sentences about what {topic} is and why it matters. Keep it motivating.

---

## Key Concepts
List exactly 5-7 key concepts as bullet points. One line each. Be specific.

---

## Study Timetable

Create a timetable with exactly {sessions} sessions totalling {hours} hours.
For EACH session use this exact format:

### Session N — [Session Title]
**Time Block:** [e.g. Hour 1-2 / Day 1 / Week 1]
**Duration:** [e.g. 2 hours]
**Focus:** [One line describing the main goal of this session]

**What to study:**
- [Specific topic or subtopic]
- [Specific topic or subtopic]
- [Specific topic or subtopic]

**Resource:** [One specific free resource from search results — name and URL]

**Outcome:** By the end of this session you will be able to [specific skill or knowledge]

---

Repeat for all {sessions} sessions. Make each session build on the previous one logically.

---

## Quick Reference
5 bullet points — the most important facts to memorise about {topic}.

---

## Knowledge Check
3 questions the student should answer after completing the full plan. Number them 1, 2, 3.

---

RULES:
- Use ONLY the format above. No extra sections.
- Keep language clear and direct — no filler phrases.
- Each session must have a distinct, meaningful focus.
- Resources must be real URLs from the search results where possible.
- Do not use emojis.
"""

    try:
        return call_groq(prompt)
    except Exception as e:
        return "Something went wrong. Please try again in a moment."