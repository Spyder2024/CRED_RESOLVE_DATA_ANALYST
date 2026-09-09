from pathlib import Path
import sys

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dashboard.data import load_data
from dashboard.state import get_theme
from dashboard.views import data_quality, decision, methodology, metrics, recovery, verdict


st.set_page_config(
    page_title="CRED RESOLVE · Forensics Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


def page(view, section_name: str, page_title: str):
    def render_page():
        theme = get_theme()
        data = load_data(theme, str(st.session_state.get("complete_only", True)))
        view.render(data)
    return render_page


pages = {
    "Overview": [
        st.Page(
            page(verdict, "Overview", "Executive Overview"),
            title="Executive Overview",
            url_path="overview",
            icon=":material/dashboard:",
            default=True,
        ),
        st.Page(
            page(recovery, "Overview", "Recovery Analytics"),
            title="Recovery Analytics",
            url_path="recovery",
            icon=":material/trending_up:",
        ),
        st.Page(
            page(data_quality, "Overview", "Data Quality & Lineage"),
            title="Data Quality & Lineage",
            url_path="data-quality",
            icon=":material/verified_user:",
        ),
    ],
    "Verdict": [
        st.Page(
            page(decision, "Verdict", "₹10 Cr Capital Allocation"),
            title="₹10 Cr Decision",
            url_path="decision",
            icon=":material/account_balance:",
        ),
        st.Page(
            page(metrics, "Verdict", "Metrics Truth Table"),
            title="Metrics & Confidence",
            url_path="metrics",
            icon=":material/fact_check:",
        ),
        st.Page(
            page(methodology, "Verdict", "Methodology & Reproduction"),
            title="Methodology & Lineage",
            url_path="methodology",
            icon=":material/account_tree:",
        ),
    ],
}

st.navigation(pages).run()
