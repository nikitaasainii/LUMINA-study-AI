import streamlit as st
import io
from agent import run_agent

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Lumina Study AI",
    page_icon="✨",
    layout="wide"
)

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Reset & Base ── */
* { box-sizing: border-box; }
.stApp { 
    background-color: #0f050a; 
}
.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* Hide anchor links */
h1 a, h2 a, h3 a, h4 a { display: none !important; }

/* ── Hero Section ── */
.hero {
    background: linear-gradient(135deg, #1a0a12 0%, #2d1320 60%, #4a1f35 100%);
    padding: 80px 80px 60px 80px;
    position: relative;
    overflow: hidden;
    border-bottom: 1px solid #4a1f35;
}

.hero::before {
    content: '';
    position: absolute;
    top: -100px;
    right: -100px;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(255,105,180,0.1) 0%, transparent 70%);
    border-radius: 50%;
}

.hero::after {
    content: '';
    position: absolute;
    bottom: -80px;
    left: 30%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(255,20,147,0.05) 0%, transparent 70%);
    border-radius: 50%;
}

.hero-badge {
    display: inline-block;
    background: rgba(255,20,147,0.15);
    color: #ff69b4;
    border: 1px solid rgba(255,20,147,0.3);
    padding: 6px 16px;
    border-radius: 20px;
    font-family: 'DM Sans', sans-serif;
    font-size: 13px;
    font-weight: 500;
    letter-spacing: 0.5px;
    margin-bottom: 24px;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 62px;
    font-weight: 900;
    color: #ffffff;
    line-height: 1.1;
    margin: 0 0 20px 0;
    position: relative;
    z-index: 1;
}

.hero-title span {
    color: #ff1493;
}

.hero-subtitle {
    font-family: 'DM Sans', sans-serif;
    font-size: 18px;
    color: #c4a0b0;
    font-weight: 300;
    line-height: 1.6;
    max-width: 520px;
    margin: 0 0 40px 0;
}

/* ── Stats Row ── */
.stats-row {
    display: flex;
    gap: 40px;
    margin-top: 10px;
}

.stat-item {
    font-family: 'DM Sans', sans-serif;
}

.stat-number {
    font-size: 28px;
    font-weight: 700;
    color: #ff1493;
    display: block;
}

.stat-label {
    font-size: 12px;
    color: #9b6b82;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* ── Main Content ── */
.content-area {
    padding: 50px 80px;
    max-width: 1100px;
}

/* ── Input Card ── */
.input-section-title {
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    color: #ffffff;
    margin-bottom: 8px;
}

.input-section-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 15px;
    color: #9b6b82;
    margin-bottom: 32px;
}

/* Override Streamlit inputs */
.stTextInput > div > div > input {
    background: #1a0a12 !important;
    border: 1.5px solid #4a1f35 !important;
    border-radius: 12px !important;
    padding: 14px 18px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    color: #ffffff !important;
    caret-color: #ff1493 !important;
    transition: border-color 0.2s !important;
}

.stTextInput > div > div > input:focus {
    border-color: #ff1493 !important;
    box-shadow: 0 0 0 3px rgba(255,20,147,0.15) !important;
}

.stTextInput > div > div > input::placeholder {
    color: #6b3a52 !important;
}

.stSelectbox > div > div {
    background: #1a0a12 !important;
    border: 1.5px solid #4a1f35 !important;
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    color: #ffffff !important;
}

.stNumberInput > div > div {
    background: #1a0a12 !important;
    border: 1.5px solid #4a1f35 !important;
    border-radius: 12px !important;
    color: #ffffff !important;
}

/* Labels */
label, .stSelectbox label, .stNumberInput label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    color: #c4a0b0 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    margin-bottom: 6px !important;
}

/* ── Generate Button ── */
.stButton > button {
    background: linear-gradient(135deg, #ff69b4, #ff1493) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 32px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    width: 100% !important;
    letter-spacing: 0.3px !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 20px rgba(255,20,147,0.25) !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 28px rgba(255,20,147,0.35) !important;
}

/* ── Result Section ── */
.result-header {
    font-family: 'Playfair Display', serif;
    font-size: 32px;
    color: #ffffff;
    margin: 48px 0 6px 0;
}

.result-topic-tag {
    display: inline-block;
    background: linear-gradient(135deg, #ff69b4, #ff1493);
    color: white;
    padding: 4px 14px;
    border-radius: 20px;
    font-family: 'DM Sans', sans-serif;
    font-size: 13px;
    font-weight: 500;
    margin-bottom: 24px;
}

/* ── Timetable Cards ── */
.timetable-grid {
    display: grid;
    gap: 16px;
    margin-top: 16px;
}

.time-card {
    background: #1a0a12;
    border: 1px solid #4a1f35;
    border-left: 4px solid #ff1493;
    border-radius: 12px;
    padding: 20px 24px;
    font-family: 'DM Sans', sans-serif;
}

.time-card-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 10px;
}

.time-badge {
    background: linear-gradient(135deg, #ff69b4, #ff1493);
    color: white;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    white-space: nowrap;
}

.time-card-title {
    font-size: 16px;
    font-weight: 600;
    color: #ffffff;
}

.time-card-body {
    font-size: 14px;
    color: #c4a0b0;
    line-height: 1.7;
}

/* ── Divider ── */
hr { border-color: #4a1f35 !important; margin: 32px 0 !important; }

/* ── Expander ── */
.streamlit-expanderHeader {
    background: #1a0a12 !important;
    border: 1px solid #4a1f35 !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    color: #ff69b4 !important;
    font-weight: 600 !important;
}

/* ── Download Button ── */
.stDownloadButton > button {
    background: transparent !important;
    color: #ff1493 !important;
    border: 1.5px solid #ff1493 !important;
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    padding: 10px 24px !important;
    transition: all 0.2s !important;
}

.stDownloadButton > button:hover {
    background: #ff1493 !important;
    color: white !important;
}

/* ── Footer ── */
.footer {
    font-family: 'DM Sans', sans-serif;
    font-size: 13px;
    color: #6b3a52;
    text-align: center;
    padding: 32px 0;
    margin-top: 40px;
    border-top: 1px solid #4a1f35;
}

/* ── Steps indicator ── */
.steps-row {
    display: flex;
    gap: 8px;
    margin-bottom: 32px;
    flex-wrap: wrap;
}

.step-pill {
    background: #1a0a12;
    border: 1px solid #4a1f35;
    color: #9b6b82;
    padding: 6px 14px;
    border-radius: 20px;
    font-family: 'DM Sans', sans-serif;
    font-size: 12px;
    font-weight: 500;
}

.step-pill.active {
    background: linear-gradient(135deg, #ff69b4, #ff1493);
    border-color: #ff1493;
    color: white;
}

/* General text */
p, li, .stMarkdown p { 
    font-family: 'DM Sans', sans-serif !important;
    color: #e0d0d8 !important;
}

h1, h2, h3, h4 {
    font-family: 'Playfair Display', serif !important;
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# ── Hero Section ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">AI Agent · Real-time Web Search · Personalised Plans</div>
    <h1 class="hero-title">Study smarter,<br>not <span>harder.</span></h1>
    <p class="hero-subtitle">
        Lumina is an AI agent that searches the web in real time and builds 
        you a complete, personalised study plan, in seconds.
    </p>
    <div class="stats-row">
        <div class="stat-item">
            <span class="stat-number">3</span>
            <span class="stat-label">Live Data Sources</span>
        </div>
        <div class="stat-item">
            <span class="stat-number">∞</span>
            <span class="stat-label">Topics Supported</span>
        </div>
        <div class="stat-item">
            <span class="stat-number">0₹</span>
            <span class="stat-label">Cost to Use</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

# ── Input Section ─────────────────────────────────────────────────────────────
st.markdown('<div class="content-area">', unsafe_allow_html=True)

st.markdown("""
<p class="input-section-title">Build your study plan</p>
<p class="input-section-sub">Tell Lumina what you want to learn,it handles the rest.</p>
""", unsafe_allow_html=True)

topic = st.text_input(
    label="TOPIC",
    placeholder="e.g. Quantum Computing, DSA, French Revolution, Machine Learning...",
    label_visibility="visible"
)

col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    depth = st.selectbox(
        "DEPTH LEVEL",
        ["Beginner Overview", "Intermediate Deep Dive", "Advanced Research"],
        label_visibility="visible"
    )
with col2:
    time_amount = st.number_input("TIME AVAILABLE", min_value=1, max_value=52, value=3)
with col3:
    time_unit = st.selectbox("UNIT", ["Hours", "Days", "Weeks"], label_visibility="visible")

hours = time_amount * (1 if time_unit == "Hours" else 8 if time_unit == "Days" else 40)

generate = st.button("Generate My Study Plan")

# ── Agent Run ─────────────────────────────────────────────────────────────────
if generate:
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        # Show live steps
        st.markdown("""
        <div class="steps-row">
            <div class="step-pill active">Searching the web</div>
            <div class="step-pill">Analysing results</div>
            <div class="step-pill">Building your plan</div>
        </div>
        """, unsafe_allow_html=True)

        with st.spinner(""):
            import time
            status = st.empty()
            status.markdown("**Searching** for resources on *" + topic + "*...")
            time.sleep(1)
            status.markdown("**Analysing** and filtering results...")
            time.sleep(1)
            status.markdown("**Generating** your personalised study plan...")
            result = run_agent(topic, depth, hours)
            status.empty()

        # ── Result Display ────────────────────────────────────────────────────
        st.markdown(f"""
        <div class="result-header">Your Study Plan</div>
        <div class="result-topic-tag">{topic} · {depth} · {time_amount} {time_unit}</div>
        """, unsafe_allow_html=True)

        # Render result as proper markdown
        st.markdown(result)

        # Save to history
        st.session_state.history.append({
            "topic": topic,
            "depth": depth,
            "time": f"{time_amount} {time_unit}",
            "plan": result
        })

        # ── PDF Download ──────────────────────────────────────────────────────
        st.markdown("---")

        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import cm
            from reportlab.lib import colors
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
            from reportlab.lib.enums import TA_LEFT, TA_CENTER
            import re

            def generate_pdf(topic, depth, time_str, content):
                buffer = io.BytesIO()
                doc = SimpleDocTemplate(
                    buffer,
                    pagesize=A4,
                    rightMargin=2*cm,
                    leftMargin=2*cm,
                    topMargin=2*cm,
                    bottomMargin=2*cm
                )

                pink = colors.HexColor('#ff1493')
                light_pink = colors.HexColor('#fff0f6')
                dark = colors.HexColor('#1a0a12')
                muted = colors.HexColor('#6b3a52')

                styles = getSampleStyleSheet()

                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Title'],
                    fontSize=28,
                    textColor=dark,
                    spaceAfter=6,
                    fontName='Helvetica-Bold'
                )

                meta_style = ParagraphStyle(
                    'Meta',
                    parent=styles['Normal'],
                    fontSize=11,
                    textColor=muted,
                    spaceAfter=20,
                    fontName='Helvetica'
                )

                h1_style = ParagraphStyle(
                    'H1',
                    parent=styles['Heading1'],
                    fontSize=16,
                    textColor=pink,
                    spaceBefore=16,
                    spaceAfter=8,
                    fontName='Helvetica-Bold'
                )

                h2_style = ParagraphStyle(
                    'H2',
                    parent=styles['Heading2'],
                    fontSize=13,
                    textColor=dark,
                    spaceBefore=12,
                    spaceAfter=6,
                    fontName='Helvetica-Bold'
                )

                body_style = ParagraphStyle(
                    'Body',
                    parent=styles['Normal'],
                    fontSize=11,
                    textColor=dark,
                    spaceAfter=6,
                    leading=16,
                    fontName='Helvetica'
                )

                bullet_style = ParagraphStyle(
                    'Bullet',
                    parent=styles['Normal'],
                    fontSize=11,
                    textColor=dark,
                    spaceAfter=4,
                    leading=16,
                    leftIndent=16,
                    fontName='Helvetica'
                )

                story = []

                # Title
                story.append(Paragraph("Lumina Study AI", title_style))
                story.append(Paragraph(f"{topic} · {depth} · {time_str}", meta_style))
                story.append(HRFlowable(width="100%", thickness=1, color=pink))
                story.append(Spacer(1, 16))

                # Parse markdown content
                lines = content.split('\n')
                for line in lines:
                    line = line.strip()
                    if not line:
                        story.append(Spacer(1, 6))
                    elif line.startswith('## '):
                        story.append(Paragraph(line[3:], h1_style))
                    elif line.startswith('### '):
                        story.append(Paragraph(line[4:], h2_style))
                    elif line.startswith('# '):
                        story.append(Paragraph(line[2:], h1_style))
                    elif line.startswith('- ') or line.startswith('* '):
                        text = line[2:]
                        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
                        story.append(Paragraph(f"• {text}", bullet_style))
                    elif line.startswith('**') and line.endswith('**'):
                        story.append(Paragraph(line.replace('**', ''), h2_style))
                    else:
                        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
                        story.append(Paragraph(text, body_style))

                story.append(Spacer(1, 20))
                story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#ffc8dc')))
                story.append(Paragraph("Generated by Lumina Study AI", meta_style))

                doc.build(story)
                buffer.seek(0)
                return buffer

            pdf_buffer = generate_pdf(topic, depth, f"{time_amount} {time_unit}", result)

            st.download_button(
                label="Download as PDF",
                data=pdf_buffer,
                file_name=f"{topic.replace(' ', '_')}_study_plan.pdf",
                mime="application/pdf"
            )

        except ImportError:
            st.info("Install reportlab to enable PDF downloads: `pip install reportlab`")

# ── History ───────────────────────────────────────────────────────────────────
if st.session_state.history:
    st.markdown("---")
    st.markdown("### Previous Study Plans")
    for item in reversed(st.session_state.history[-5:]):
        with st.expander(f"{item['topic']} · {item['depth']} · {item['time']}"):
            st.markdown(item["plan"])

st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Lumina Study AI — Powered by Agentic Workflow · Built with Streamlit
</div>
""", unsafe_allow_html=True)