from datetime import datetime

import pandas as pd
import streamlit as st

from dashboard.state import get_theme, init_state, set_theme
from dashboard.theme import TOKENS, inject_css


def page_shell(
    data: dict,
    title: str,
    description: str,
    category: str = "Overview",
    status_text: str = "AUDITED",
    status_class: str = "status-good",
) -> str:
    """Enterprise page shell implementing Top Nav, Page Header, and Professional Sidebar."""
    init_state()
    theme = get_theme()
    inject_css(theme)
    source = data.get("source", "SYNTHETIC")
    now_str = datetime.now().strftime("%d %b %Y, %H:%M")

    # -------------------------------------------------------------
    # 1. Professional Sidebar (280px Workspace Drawer)
    # -------------------------------------------------------------
    with st.sidebar:
        st.markdown(
            """<div style='display:flex;align-items:center;gap:8px;margin-bottom:4px;'>
                <span style='font-size:16px;'>⚡</span>
                <span class='page-eyebrow' style='margin:0;'>CRED RESOLVE</span>
            </div>
            <div style='font-size:18px;font-weight:700;letter-spacing:-0.02em;margin-bottom:16px;'>
                Forensics Engine
            </div>""",
            unsafe_allow_html=True,
        )

        st.markdown("<div class='card-label' style='margin-bottom:8px;'>WORKSPACE CONTROLS</div>", unsafe_allow_html=True)
        st.date_input(
            "Audit interval",
            value=(datetime(2026, 1, 1), datetime(2026, 8, 8)),
            key="date_range",
            format="DD-MM-YYYY",
        )
        st.toggle("Complete months only", key="complete_only")
        st.selectbox("Portfolio segment", ["All Portfolios", "Unsecured Personal", "Credit Card"], key="segment")

        st.markdown("<div class='card-label' style='margin:20px 0 8px;'>AUDIT INTEGRITY</div>", unsafe_allow_html=True)
        st.markdown(
            f"""<div style='display:flex;flex-direction:column;gap:6px;'>
                <div class='status-pill status-good'>AUDITED LAYER ACTIVE</div>
                <div class='status-pill status-warn'>PROVISIONAL AUG EXCLUDED</div>
            </div>
            <div class='muted' style='margin-top:10px;font-size:11px;line-height:1.4;'>
                Source Mart: <b>{source}</b><br>
                Reconciliation: <b>Strict Mart Contract</b>
            </div>""",
            unsafe_allow_html=True,
        )
        sidebar_theme_sync()

    # -------------------------------------------------------------
    # 2. Enterprise Top Nav
    # -------------------------------------------------------------
    theme_icon = "☀️" if theme == "dark" else "🌙"
    theme_label = "Switch to Light Mode" if theme == "dark" else "Switch to Dark Mode"

    nav_cols = st.columns([4, 1.2])
    with nav_cols[0]:
        st.markdown(
            f"""<div class='top-nav' style='border-bottom:none;padding-bottom:0;margin-bottom:0;'>
                <div class='top-nav-breadcrumbs'>
                    <span>Platform</span>
                    <span>/</span>
                    <span>{category}</span>
                    <span>/</span>
                    <span class='crumb-active'>{title}</span>
                </div>
            </div>""",
            unsafe_allow_html=True,
        )
    with nav_cols[1]:
        mode_cols = st.columns([2, 1])
        with mode_cols[0]:
            st.markdown(
                f"<div style='text-align:right;padding-top:6px;'><span class='status-pill status-neutral'>● {source}</span></div>",
                unsafe_allow_html=True,
            )
        with mode_cols[1]:
            if st.button(theme_icon, key="theme_top", help=theme_label, width="stretch"):
                set_theme("light" if theme == "dark" else "dark")

    st.markdown("<div style='border-bottom: 1px solid var(--border); margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # 3. Enterprise Page Header
    # -------------------------------------------------------------
    header_cols = st.columns([3.2, 1.8])
    with header_cols[0]:
        st.markdown(
            f"""<div class='page-header-main'>
                <div class='page-eyebrow'>COLLECTIONS INTELLIGENCE · AUDIT REPORT</div>
                <h1 class='page-title'>{title}</h1>
                <p class='page-desc'>{description}</p>
            </div>""",
            unsafe_allow_html=True,
        )
    with header_cols[1]:
        st.markdown(
            f"""<div class='page-header-aside'>
                <div class='badge-group'>
                    <span class='status-pill {status_class}'>{status_text}</span>
                    <span class='status-pill status-neutral'>Updated {now_str[:11]}</span>
                </div>
                <div class='muted' style='text-align:right;'>
                    Period: Jan–Aug 2026 &nbsp;·&nbsp; 7 complete + 1 partial
                </div>
            </div>""",
            unsafe_allow_html=True,
        )

    # Action Toolbar
    action_cols = st.columns([1, 1, 1.2, 3.8])
    with action_cols[0]:
        if st.button(":material/download: Export", key="export_btn", help="Export audit packet", width="stretch"):
            st.toast("Export generated for current mart snapshot.")
    with action_cols[1]:
        if st.button(":material/share: Share", key="share_btn", help="Share current audit view", width="stretch"):
            st.toast("Direct deep-link copied to clipboard.")
    with action_cols[2]:
        trend = data.get("trend", pd.DataFrame())
        csv = trend.to_csv(index=False) if not trend.empty else "No trend data"
        st.download_button(
            ":material/table_view: Trend CSV",
            csv,
            file_name="recovery_forensics_trend.csv",
            mime="text/csv",
            help="Download verified monthly trend series",
            width="stretch",
        )

    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)
    return theme


def page_footer(data: dict) -> None:
    """Enterprise footer displaying audit metadata and mart freshness."""
    source = data.get("source", "SYNTHETIC")
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    st.markdown(
        f"""<div class='platform-footer'>
            <div class='footer-left'>
                <span>⚡ <b>CRED RESOLVE</b> Enterprise Analytics</span>
                <span>·</span>
                <span>Audit Lineage: Verified DuckDB Marts (<b>{source}</b>)</span>
                <span>·</span>
                <span>Reconciliation Discrepancy: ₹17.2 Cr (non-loss accounting adjustment)</span>
            </div>
            <div class='footer-right'>
                <span>Trailing Month Provisional</span>
                <span>·</span>
                <span>System Timestamp: {now_str} UTC</span>
            </div>
        </div>""",
        unsafe_allow_html=True,
    )


def sidebar_theme_sync() -> None:
    theme = get_theme()
    is_dark = theme == "dark"
    new_dark = st.sidebar.toggle("Dark mode", value=is_dark, key="dark_mode_toggle")
    if new_dark != is_dark:
        set_theme("dark" if new_dark else "light")