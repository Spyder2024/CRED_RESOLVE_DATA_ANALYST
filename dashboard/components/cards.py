import streamlit as st


def kpi_card(
    label: str,
    value: str,
    detail: str = "",
    badge: str = "",
    badge_class: str = "badge-teal",
    icon: str = "↗",
    trend: str = "",
) -> None:
    badge_html = f"<span class='{badge_class}'>{badge}</span>" if badge else ""
    trend_html = f"<span class='metric-trend'>{trend}</span>" if trend else ""
    meta_html = f"<div class='card-meta'>{badge_html} {trend_html}</div>" if (badge or trend) else ""
    detail_html = f"<div class='muted'>{detail}</div>" if detail else ""
    
    st.markdown(
        f"""<div class='card'>
            <div class='card-header'>
                <span class='card-label'>{label}</span>
                <span class='card-icon'>{icon}</span>
            </div>
            <div class='kpi-value'>{value}</div>
            {meta_html}
            {detail_html}
        </div>""",
        unsafe_allow_html=True,
    )


def section(title: str, description: str = "") -> None:
    desc_html = f"<p>{description}</p>" if description else ""
    st.markdown(
        f"""<div class='section-head'>
            <h2>{title}</h2>
            {desc_html}
        </div>""",
        unsafe_allow_html=True,
    )


def executive_summary_banner(
    badge_text: str,
    title: str,
    body_text: str,
    metrics: list[tuple[str, str]],
    icon: str = "!",
) -> None:
    grid_items = "".join(
        f"""<div class='verdict-grid-item'>
            <div class='verdict-grid-label'>{label}</div>
            <div class='verdict-grid-value'>{val}</div>
        </div>"""
        for label, val in metrics
    )
    
    st.markdown(
        f"""<div class='verdict-banner'>
            <div class='verdict-banner-body'>
                <div class='verdict-banner-badge'>
                    <span>●</span> {badge_text}
                </div>
                <h3 class='verdict-banner-title'>{title}</h3>
                <p class='verdict-banner-text'>{body_text}</p>
                <div class='verdict-grid'>
                    {grid_items}
                </div>
            </div>
            <div class='verdict-banner-icon'>{icon}</div>
        </div>""",
        unsafe_allow_html=True,
    )


def insight_card(label: str, value: str, detail: str) -> None:
    st.markdown(
        f"""<div class='callout insight-card'>
            <div class='insight-label'>{label}</div>
            <div class='insight-value'>{value}</div>
            <div class='muted'>{detail}</div>
        </div>""",
        unsafe_allow_html=True,
    )


def evidence_card(
    label: str,
    value: str,
    badge_text: str,
    badge_class: str,
    detail: str,
) -> None:
    st.markdown(
        f"""<div class='card'>
            <div class='card-header'>
                <span class='card-label'>{label}</span>
                <span class='{badge_class}'>{badge_text}</span>
            </div>
            <div class='kpi-value' style='font-size: 20px;'>{value}</div>
            <div class='muted'>{detail}</div>
        </div>""",
        unsafe_allow_html=True,
    )


def audit_timeline(steps: list[tuple[str, bool]]) -> None:
    step_html = []
    for i, (step_label, is_active) in enumerate(steps):
        active_cls = "active" if is_active else ""
        arrow = "<span class='timeline-arrow'>→</span>" if i < len(steps) - 1 else ""
        step_html.append(
            f"""<div class='timeline-step {active_cls}'>
                <span class='timeline-dot'></span>
                <span>{step_label}</span>
            </div>
            {arrow}"""
        )
    
    st.markdown(
        f"""<div class='audit-timeline'>
            {''.join(step_html)}
        </div>""",
        unsafe_allow_html=True,
    )


def empty_state(title: str, reason: str, unlock: str) -> None:
    st.markdown(
        f"""<div class='callout'>
            <div style='font-weight: 700; font-size: 14px;'>{title}</div>
            <div class='muted'>{reason}</div>
            <div style='margin-top: 8px;'>
                <span class='badge-amber'>Unlock Path</span>
                <span style='font-size: 12px; margin-left: 6px;'>{unlock}</span>
            </div>
        </div>""",
        unsafe_allow_html=True,
    )