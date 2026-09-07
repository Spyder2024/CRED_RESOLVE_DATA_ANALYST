"""Shared visual tokens and the Plotly template for the executive fact-check dashboard."""

import plotly.graph_objects as go

TOKENS = {
    "page_bg": "#FAFAFA",
    "card_bg": "#FFFFFF",
    "card_border": "#E2E8F0",
    "primary_navy": "#1A365D",
    "legacy_grey": "#6B7280",
    "legacy_light": "#9CA3AF",
    "genuine_teal": "#0F766E",
    "misleading_red": "#B91C1C",
    "inconclusive_amber": "#B45309",
    "text": "#1F2937",
    "secondary_text": "#64748B",
    "grid": "#F1F5F9",
    "soft_bg": "#F8FAFC",
}


def build_plotly_template() -> go.layout.Template:
    """Return the one approved chart theme used by every Plotly figure."""
    return go.layout.Template(
        layout=go.Layout(
            font={"family": "Inter, system-ui, sans-serif", "size": 13, "color": TOKENS["text"]},
            colorway=[TOKENS["primary_navy"], TOKENS["legacy_grey"]],
            plot_bgcolor=TOKENS["card_bg"],
            paper_bgcolor=TOKENS["card_bg"],
            hoverlabel={"bgcolor": TOKENS["card_bg"], "bordercolor": TOKENS["primary_navy"], "font": {"color": TOKENS["text"]}},
            xaxis={"showgrid": False, "zeroline": False},
            yaxis={"showgrid": True, "gridcolor": TOKENS["grid"], "zeroline": False},
            legend={"orientation": "h", "y": 1.12, "x": 0, "bgcolor": TOKENS["card_bg"]},
            margin={"l": 42, "r": 18, "t": 42, "b": 38},
        )
    )


PLOTLY_TEMPLATE = build_plotly_template()
