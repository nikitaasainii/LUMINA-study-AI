# 🌟 Lumina Study AI
### An Agentic Learning Assistant for Personalized Curriculum Synthesis

---

## What this does
You type a topic → the AI agent searches the web → reads the results → generates a personalised study plan. It uses a ReAct agentic loop (Plan → Act → Observe → Generate).

---

## Setup (takes ~5 minutes)

### Step 1 — Get your free Groq API key
1. Go to https://console.groq.com
2. Sign in with Google
3. Click "Get API Key" → "Create API Key"
4. Copy the key

### Step 2 — Add your key
Open the `.env` file and replace `paste_your_key_here` with your actual key:
```
GROQ_API_KEY=AIzaSy...your_key_here
```

### Step 3 — Install dependencies
Open Terminal, navigate to this folder, and run:
```bash
cd lumina-study-ai
pip install -r requirements.txt
```

### Step 4 — Run the app
```bash
streamlit run app.py
```

Your browser will open automatically at http://localhost:8501 🎉

---

## Project Structure
```
lumina-study-ai/
├── app.py           # Frontend — Streamlit UI
├── agent.py         # Backend — Agentic logic (search + AI)
├── requirements.txt # Dependencies
├── .env             # Your API key (never share this)
└── README.md        # This file
```

---

## Tech Stack
| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| AI Brain | GROQ API (free) |
| Web Search | DuckDuckGo Search API (free) |
| Encyclopedia | Wikipedia API (free) |
| Deployment | Streamlit Community Cloud (free) |

---

## Deploying to the internet (free)
1. Push this folder to GitHub
2. Go to https://share.streamlit.io
3. Connect your GitHub repo
4. Add your GROQ_API_KEY in the "Secrets" section
5. Click Deploy → you get a live public URL ✅

---

## Methodology
This project implements an **Agentic AI Workflow** using the **ReAct (Reasoning + Acting)** framework:
1. **Plan** — Agent decides what to search for based on the topic
2. **Act** — Agent uses DuckDuckGo and Wikipedia as tools
3. **Observe** — Agent reads and compiles the search results
4. **Generate** — Agent calls Gemini LLM to synthesise a study plan

This is Phase 1 (Rapid Prototyping). Phase 2 will migrate to React + FastAPI for production architecture.
