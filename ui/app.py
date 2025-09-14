import os
import sys
import time
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# Ensure project root is on sys.path so we can import workflow from repo root
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from workflow import MultiAgentWorkflow


def ensure_output_dir():
    out = Path(os.getenv("OUTPUT_DIR", "./outputs"))
    out.mkdir(parents=True, exist_ok=True)
    return out


def main():
    load_dotenv()
    st.set_page_config(page_title="Multi-Agent Research & Analysis", page_icon="🤖", layout="wide")

    st.title("🤖 Multi-Agent Research & Analysis")
    st.caption("Researcher → Analyst → Reporter | LangGraph + Gemini")

    # Sidebar config
    with st.sidebar:
        st.header("⚙️ Configuration")
        google_ok = bool(os.getenv("GOOGLE_API_KEY"))
        serper_ok = bool(os.getenv("SERPER_API_KEY"))
        out_dir = ensure_output_dir()
        st.write(f"Output dir: `{out_dir}`")
        st.write(f"Gemini key: {'✅' if google_ok else '❌'}")
        st.write(f"Serper key: {'✅' if serper_ok else '❌'} (optional)")

    # Query input
    query = st.text_area(
        "Enter your research question",
        placeholder="e.g., Analyze Apple's 2024 Q4 performance",
        height=120,
        max_chars=1000,
    )
    run = st.button("🚀 Run Analysis", type="primary", disabled=not bool(query))

    # Progress widgets
    overall = st.progress(0, text="Waiting to start…")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("🔍 Researcher")
        r_stat = st.empty()
        r_prog = st.progress(0)
    with c2:
        st.subheader("📊 Analyst")
        a_stat = st.empty()
        a_prog = st.progress(0)
    with c3:
        st.subheader("📝 Reporter")
        p_stat = st.empty()
        p_prog = st.progress(0)

    if run:
        if not os.getenv("GOOGLE_API_KEY"):
            st.error("GOOGLE_API_KEY not set. Please configure it in .env.")
            return

        overall.progress(5, text="Initializing workflow…")
        r_stat.info("Preparing search…")
        a_stat.info("Waiting…")
        p_stat.info("Waiting…")

        wf = MultiAgentWorkflow()

        # Simulate staged progress around the blocking run
        r_prog.progress(25)
        overall.progress(25, text="Researcher running…")
        time.sleep(0.2)

        a_prog.progress(15)
        overall.progress(40, text="Analyst preparing…")
        time.sleep(0.2)

        p_prog.progress(10)
        overall.progress(50, text="Reporter preparing…")
        time.sleep(0.2)

        with st.spinner("Running multi-agent workflow…"):
            state = wf.run(query)

        # Fill progress after completion
        r_prog.progress(100)
        a_prog.progress(100)
        p_prog.progress(100)
        overall.progress(100, text="Completed")
        r_stat.success("Search complete")
        a_stat.success("Analysis complete")
        p_stat.success("Report generated")

        # Display results
        st.subheader("📊 Results")
        tab1, tab2, tab3, tab4 = st.tabs(["Executive Summary", "Research", "Analysis", "Final Report"])

        with tab1:
            st.markdown("#### Summary")
            st.write(state.get("analysis_insights") or state.get("research_summary") or "N/A")

        with tab2:
            st.markdown("#### Research Findings")
            st.write(state.get("research_findings", "N/A"))

        with tab3:
            st.markdown("#### Analysis Insights")
            st.write(state.get("analysis_insights", "N/A"))
            st.markdown("#### Calculation Results")
            st.code(state.get("calculation_results", "N/A"))

        with tab4:
            st.markdown("#### Final Report")
            st.write(state.get("final_report", "N/A"))
            st.info(state.get("save_result", ""))


if __name__ == "__main__":
    main()
