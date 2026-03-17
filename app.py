import streamlit as st
from agent import run_agent

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Lumina Study AI",
    page_icon="✨",
    layout="centered"
)

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Hide anchor link icons */
    .stMarkdown h1 a, .stMarkdown h2 a, .stMarkdown h3 a, .stMarkdown h4 a { display: none; }

    /* White background */
    .stApp { background-color: #fff0f6; }
    .main { background-color: #fff0f6; }

    /* Left align everything */
    .block-container {
        padding-left: 3rem;
        padding-right: 3rem;
        max-width: 860px;
        margin-left: 0 !important;
    }

    /* Headings */
    h1 { color: #ff1493 !important; font-size: 2.4rem !important; }
    h2 { color: #ff1493 !important; }
    h3 { color: #ff69b4 !important; }
    h4 { color: #ffb6c1 !important; }

    /* Body text */
    p, label, .stMarkdown { color: #1a1a1a !important; }

    /* Input box */
    .stTextInput > div > div > input {
        background-color: #fff0f6;
        color: #1a1a1a;
        border: 2px solid #ff69b4;
        border-radius: 10px;
        padding: 12px;
        font-size: 15px;
        caret-color: #ff1493;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        background-color: #fff0f6 !important;
        border: 2px solid #ff69b4 !important;
        color: #1a1a1a !important;
        border-radius: 10px;
    }

    /* Number input */
    .stNumberInput > div > div {
        background-color: #fff0f6 !important;
        border: 2px solid #ff69b4 !important;
        color: #1a1a1a !important;
        border-radius: 10px;
    }

    /* Button */
    .stButton > button {
        background: linear-gradient(135deg, #ff69b4, #ff1493);
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
        background-color: #ffffff;
        border: 1px solid #ff69b4;
        border-radius: 12px;
        padding: 24px;
        margin-top: 20px;
        color: #1a1a1a;
        line-height: 1.8;
    }

    /* Divider */
    hr { border-color: #ffb6c1; }

    /* Expander */
    .streamlit-expanderHeader {
        background-color: #fff0f6 !important;
        color: #ff1493 !important;
        border: 1px solid #ff69b4 !important;
        border-radius: 8px !important;
    }


    /* Footer */
    .footer {
        color: #ffb6c1;
        font-size: 13px;
        margin-top: 40px;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("# Lumina Study AI")
st.markdown("#### Your Agentic Learning Assistant")
st.markdown("---")

# ── Session state ─────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

# ── Input ─────────────────────────────────────────────────────────────────────
st.markdown("### What do you want to study?")
topic = st.text_input(
    label="topic",
    placeholder="e.g. Quantum Computing, French Revolution, Machine Learning...",
    label_visibility="collapsed"
)

col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    depth = st.selectbox(
        "Depth",
        ["Beginner Overview", "Intermediate Deep Dive", "Advanced Research"],
        label_visibility="visible"
    )
with col2:
    time_amount = st.number_input("Time available", min_value=1, max_value=52, value=3)
with col3:
    time_unit = st.selectbox("Unit", ["Hours", "Days", "Weeks"], label_visibility="visible")

hours = time_amount * (1 if time_unit == "Hours" else 8 if time_unit == "Days" else 40)

generate = st.button("Generate My Study Plan")

# ── Agent run ─────────────────────────────────────────────────────────────────
if generate:
    if not topic.strip():
        st.warning("Please enter a topic first!")
    else:
        with st.spinner("Working on your study plan..."):
            status = st.empty()

            status.markdown("**Step 1:** Searching for resources on *" + topic + "*...")
            import time; time.sleep(1)

            status.markdown("**Step 2:** Analysing and filtering results...")
            time.sleep(1)

            status.markdown("**Step 3:** Generating your personalised study plan...")

            result = run_agent(topic, depth, hours)
            status.empty()

        # ── Display result ────────────────────────────────────────────────────
        st.markdown("---")
        st.markdown("### Your Personalised Study Plan")
        st.markdown(result)
        st.session_state.history.append({"topic": topic, "plan": result})
        

# ── History ───────────────────────────────────────────────────────────────────
if st.session_state.history:
    st.markdown("---")
    st.markdown("### Previous Study Plans")
    for item in reversed(st.session_state.history[-5:]):
        with st.expander(f"{item['topic']}"):
            st.markdown(item["plan"], unsafe_allow_html=True)
# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<p class="footer">Lumina Study AI — Powered by GROQ</p>',
    unsafe_allow_html=True
)
