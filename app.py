import time

import streamlit as st

from agents import build_reader_agent, build_search_agent, critic_chain, writer_chain


st.set_page_config(
    page_title="InsightAI | Research Studio",
    page_icon="I",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&family=Newsreader:opsz,wght@6..72,500;6..72,600&display=swap');

    :root { --ink:#edf4fb; --muted:#93a5b8; --line:#263a50; --paper:#09121f; --navy:#142b43; --sky:#65c5f1; --aqua:#142f42; --mint:#65d7b1; }
    html, body, [class*="css"] { font-family:'Manrope', sans-serif; color:var(--ink); }
    .stApp { background:var(--paper); background-image:radial-gradient(ellipse 70% 55% at 85% -15%, rgba(35,126,173,.22), transparent 60%), linear-gradient(90deg, rgba(132,177,210,.045) 1px, transparent 1px), linear-gradient(rgba(132,177,210,.045) 1px, transparent 1px); background-size:auto,42px 42px,42px 42px; }
    #MainMenu, footer, header { visibility:hidden; }
    .block-container { max-width:1240px; padding:1.4rem 3rem 3rem; }

    .masthead { display:flex; align-items:center; justify-content:space-between; padding:0.5rem 0 2.3rem; }
    .brand { display:flex; align-items:center; gap:.75rem; font-weight:800; font-size:1.05rem; letter-spacing:-.03em; }
    .brand-mark { display:grid; place-items:center; width:33px; height:33px; border-radius:10px; background:var(--sky); color:#07111d; font-family:'Newsreader', serif; font-size:1.2rem; }
    .tag { font:500 .68rem 'DM Mono', monospace; letter-spacing:.1em; color:var(--muted); text-transform:uppercase; }
    .hero { max-width:800px; padding:1.5rem 0 3.4rem; }
    .eyebrow { color:var(--sky); font:500 .72rem 'DM Mono', monospace; letter-spacing:.14em; text-transform:uppercase; margin-bottom:1rem; }
    .hero h1 { color:var(--navy); font:600 clamp(3rem,6vw,5.7rem)/.94 'Newsreader', serif; letter-spacing:-.055em; margin:0; }
    .hero h1 em { color:var(--sky); font-style:italic; }
    .hero p { color:var(--muted); font-size:1rem; line-height:1.75; max-width:600px; margin:1.35rem 0 0; }

    .panel-kicker { color:var(--sky); font:500 .67rem 'DM Mono', monospace; letter-spacing:.13em; text-transform:uppercase; margin-bottom:.5rem; }
    .panel-title { color:var(--navy); font-size:1.05rem; font-weight:800; margin-bottom:1.25rem; }
    .stTextInput > div > div > input { border:1px solid #39526c !important; background:#0c1b2a !important; border-radius:12px !important; color:var(--ink) !important; font-size:1.12rem !important; padding:1.15rem 1.1rem !important; min-height:3.8rem !important; }
    .stTextInput > div > div > input:focus { border-color:var(--sky) !important; box-shadow:0 0 0 3px rgba(22,119,184,.12) !important; }
    .stTextInput label { font-size:.78rem !important; font-weight:700 !important; color:var(--navy) !important; }
    .stButton > button { width:100%; border:0 !important; border-radius:10px !important; background:var(--sky) !important; color:#07111d !important; font:700 .88rem 'Manrope', sans-serif !important; padding:.78rem 1rem !important; transition:background .2s, transform .2s !important; }
    .stButton > button:hover { background:#a8e4fb !important; transform:translateY(-1px); }
    .hint { color:var(--muted); font-size:.75rem; line-height:1.5; margin:1rem 0 0; }

    .stage { border-left:2px solid #cdd9e3; padding:0 0 1.2rem 1.15rem; margin-left:.45rem; position:relative; }
    .stage:last-child { padding-bottom:0; }
    .stage:before { content:''; position:absolute; left:-.38rem; top:.05rem; width:.6rem; height:.6rem; background:#0c1b2a; border:2px solid #587087; border-radius:100%; }
    .stage.active { border-color:#8bc4de; }.stage.active:before { background:var(--sky); border-color:var(--sky); }.stage.complete:before { background:var(--mint); border-color:var(--mint); }
    .stage-top { display:flex; align-items:baseline; gap:.7rem; }.stage-no { color:var(--muted); font:500 .65rem 'DM Mono',monospace; }.stage-name { color:var(--navy); font-weight:800; font-size:.88rem; }.stage-state { margin-left:auto; color:var(--muted); font:500 .62rem 'DM Mono',monospace; letter-spacing:.06em; }.active .stage-state{color:var(--sky)}.complete .stage-state{color:var(--mint)}
    .stage-note { color:var(--muted); font-size:.75rem; margin-top:.25rem; }
    .section-rule { border:0; border-top:1px solid var(--line); margin:2.6rem 0 1.5rem; }
    .result-heading { color:var(--navy); font:600 2rem 'Newsreader',serif; letter-spacing:-.03em; margin-bottom:1rem; }
    .output-card { background:rgba(16,35,54,.88); border:1px solid var(--line); border-radius:14px; padding:1.5rem 1.8rem; margin:1rem 0; }
    .output-label { color:var(--sky); font:500 .67rem 'DM Mono',monospace; letter-spacing:.12em; text-transform:uppercase; border-bottom:1px solid var(--line); padding-bottom:.8rem; margin-bottom:1rem; }
    .review-card { border-top:3px solid var(--mint); }
    details summary { color:var(--navy) !important; font-size:.82rem !important; font-weight:700 !important; }
    .footnote { color:var(--muted); font:500 .67rem 'DM Mono',monospace; letter-spacing:.06em; text-align:center; padding:3rem 0 .5rem; }
    @media (max-width: 700px) { .block-container{padding:1rem 1.1rem 2rem}.masthead{padding-bottom:1.5rem}.hero{padding-bottom:2rem}.tag{display:none;} }
    </style>
    """,
    unsafe_allow_html=True,
)


def stage(number: str, name: str, state: str, note: str) -> None:
    labels = {"waiting": "QUEUED", "running": "IN PROGRESS", "done": "COMPLETE"}
    css_class = {"waiting": "", "running": "active", "done": "complete"}[state]
    st.markdown(
        f'<div class="stage {css_class}"><div class="stage-top"><span class="stage-no">{number}</span>'
        f'<span class="stage-name">{name}</span><span class="stage-state">{labels[state]}</span></div>'
        f'<div class="stage-note">{note}</div></div>',
        unsafe_allow_html=True,
    )


for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False

st.markdown(
    """
    <div class="masthead"><div class="brand"><span class="brand-mark">I</span>InsightAI</div>
    <div class="tag">Evidence-led research studio</div></div>
    <section class="hero"><div class="eyebrow">A four-part research workflow</div>
    <h1>Let intelligent agents<br><em>research, reason, and deliver clarity.</em></h1>
    <p>Turn a broad question into a clear, sourced brief. InsightAI coordinates discovery, reading, synthesis, and quality review in one focused workspace.</p></section>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([1.15, 0.85], gap="large")
with left:
    topic = st.text_input("Research question", placeholder="e.g. How is green hydrogen scaling in India?", key="topic_input")
    run_btn = st.button("Create research brief")
    st.markdown('''<p class="hint">Try one of these research questions:</p><ul class="hint"><li>How will AI agents change customer support in 2026?</li><li>What is the outlook for green hydrogen in India?</li><li>How is CRISPR advancing treatments for rare diseases?</li><li>What are the key risks and opportunities of quantum computing?</li><li>How are cities adapting to extreme heat and climate change?</li></ul>''', unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel-kicker">Brief progress</div><div class="panel-title">Research desk</div>', unsafe_allow_html=True)
    results = st.session_state.results
    steps = ["search", "reader", "writer", "critic"]

    def status(step_name: str) -> str:
        if step_name in results:
            return "done"
        if st.session_state.running and step_name == next((item for item in steps if item not in results), None):
            return "running"
        return "waiting"

    stage("01", "Scout sources", status("search"), "Locate timely, credible starting points")
    stage("02", "Read deeply", status("reader"), "Extract detail from the strongest source")
    stage("03", "Shape the brief", status("writer"), "Turn evidence into a structured report")
    stage("04", "Editorial review", status("critic"), "Assess clarity, coverage, and gaps")

if run_btn:
    if not topic.strip():
        st.warning("Enter a research question to begin.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = {}
    topic_value = st.session_state.topic_input

    with st.spinner("InsightAI is scouting sources..."):
        search_agent = build_search_agent()
        response = search_agent.invoke({"messages": [("user", f"Find recent, reliable and detailed information about: {topic_value}")]})
        results["search"] = response["messages"][-1].content
        st.session_state.results = dict(results)

    with st.spinner("InsightAI is reading the most relevant source..."):
        reader_agent = build_reader_agent()
        response = reader_agent.invoke({"messages": [("user", f"Based on the following search results about '{topic_value}', pick the most relevant URL and scrape it for deeper content.\n\nSearch Results:\n{results['search'][:800]}")]})
        results["reader"] = response["messages"][-1].content
        st.session_state.results = dict(results)

    with st.spinner("InsightAI is shaping your research brief..."):
        research = f"SEARCH RESULTS:\n{results['search']}\n\nDETAILED SCRAPED CONTENT:\n{results['reader']}"
        results["writer"] = writer_chain.invoke({"topic": topic_value, "research": research})
        st.session_state.results = dict(results)

    with st.spinner("InsightAI is performing an editorial review..."):
        results["critic"] = critic_chain.invoke({"report": results["writer"]})
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()

results = st.session_state.results
if results:
    st.markdown('<hr class="section-rule"><div class="result-heading">Your research brief</div>', unsafe_allow_html=True)
    if "search" in results:
        with st.expander("View source discovery notes"):
            st.code(results["search"], language=None)
    if "reader" in results:
        with st.expander("View source reading notes"):
            st.code(results["reader"], language=None)
    if "writer" in results:
        st.markdown('<div class="output-card"><div class="output-label">InsightAI research brief</div>', unsafe_allow_html=True)
        st.markdown(results["writer"])
        st.markdown('</div>', unsafe_allow_html=True)
        st.download_button("Download brief (.md)", results["writer"], f"insightai_brief_{int(time.time())}.md", "text/markdown")
    if "critic" in results:
        st.markdown('<div class="output-card review-card"><div class="output-label">Editorial review</div>', unsafe_allow_html=True)
        st.markdown(results["critic"])
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="footnote">INSIGHTAI · MULTI-AGENT RESEARCH WORKFLOW</div>', unsafe_allow_html=True)
