import streamlit as st
from agent import run_agent

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Lumina Study AI",
    page_icon="🌟",
    layout="centered"
)

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .stTextInput > div > div > input {
        background-color: #1e2130;
        color: white;
        border: 1px solid #3a3f5c;
        border-radius: 10px;
        padding: 12px;
    }
    .stButton > button {
        background: linear-gradient(135deg, #6e57e0, #a78bfa);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 30px;
        font-size: 16px;
        font-weight: 600;
        width: 100%;
        transition: opacity 0.2s;
    }
    .stButton > button:hover { opacity: 0.85; }
    .result-box {
        background-color: #1e2130;
        border: 1px solid #3a3f5c;
        border-radius: 12px;
        padding: 24px;
        margin-top: 20px;
        color: #e2e8f0;
        line-height: 1.8;
    }
    .step-badge {
        background: #6e57e0;
        color: white;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-right: 8px;
    }
    h1 { color: #a78bfa !important; }
    h3 { color: #cbd5e1 !important; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("# 🌟 Lumina Study AI")
st.markdown("#### Your Agentic Learning Assistant")
st.markdown("---")

# ── Session state ─────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

# ── Input ─────────────────────────────────────────────────────────────────────
st.markdown("### 📚 What do you want to study?")
topic = st.text_input(
    label="topic",
    placeholder="e.g. Quantum Computing, French Revolution, Machine Learning...",
    label_visibility="collapsed"
)

col1, col2 = st.columns([3, 1])
with col1:
    depth = st.selectbox(
        "Depth",
        ["Beginner Overview", "Intermediate Deep Dive", "Advanced Research"],
        label_visibility="visible"
    )
with col2:
    hours = st.number_input("Study hours available", min_value=1, max_value=20, value=3)

generate = st.button("✨ Generate My Study Plan")

# ── Agent run ─────────────────────────────────────────────────────────────────
if generate:
    if not topic.strip():
        st.warning("Please enter a topic first!")
    else:
        with st.spinner("🤖 Agent is working... searching, thinking, planning..."):

            # Show agentic steps live
            status = st.empty()

            status.markdown("**🔍 Step 1:** Searching for resources on *" + topic + "*...")
            import time; time.sleep(1)

            status.markdown("**🧠 Step 2:** Analysing and filtering results...")
            time.sleep(1)

            status.markdown("**📝 Step 3:** Generating your personalised study plan...")

            result = run_agent(topic, depth, hours)
            status.empty()

        # ── Display result ────────────────────────────────────────────────────
        st.markdown("---")
        st.markdown("### 🎯 Your Personalised Study Plan")
        st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)

        # Save to history
        st.session_state.history.append({"topic": topic, "plan": result})

        # Download button
        st.download_button(
            label="📥 Download Study Plan",
            data=result,
            file_name=f"{topic.replace(' ', '_')}_study_plan.txt",
            mime="text/plain"
        )

# ── History sidebar ───────────────────────────────────────────────────────────
if st.session_state.history:
    st.markdown("---")
    st.markdown("### 🕘 Previous Study Plans")
    for i, item in enumerate(reversed(st.session_state.history[-5:])):
        with st.expander(f"📖 {item['topic']}"):
            st.markdown(item["plan"], unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<center><small>Lumina Study AI · Powered by Gemini + Agentic Workflow</small></center>",
    unsafe_allow_html=True
)
