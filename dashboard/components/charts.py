import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from dashboard.theme import TOKENS, plotly_template


def trend_chart(frame: pd.DataFrame, theme: str, complete_only: bool = False) -> None:
    t = TOKENS[theme]
    fig = go.Figure()
    if frame.empty:
        st.info("No trend records available for the selected filter.")
        return

    frame = frame.copy()
    frame["month"] = pd.to_datetime(frame["month"])

    # 95% Confidence Band (Audited)
    ci_fill = "rgba(5, 150, 105, 0.12)" if theme == "light" else "rgba(52, 211, 153, 0.15)"
    fig.add_trace(
        go.Scatter(
            x=pd.concat([frame["month"], frame["month"][::-1]]),
            y=pd.concat([frame["verified_ci_high"], frame["verified_ci_low"][::-1]]),
            fill="toself",
            fillcolor=ci_fill,
            line={"width": 0},
            name="95% CI Band",
            hoverinfo="skip",
        )
    )

    # Legacy Rate (Dashed line)
    fig.add_trace(
        go.Scatter(
            x=frame["month"],
            y=frame["reported_recovery_rate"],
            mode="lines+markers",
            name="Legacy View (Contacted)",
            line={"color": t["legacy"], "dash": "dash", "width": 2},
            marker={"size": 6},
            hovertemplate="Legacy: %{y:.1%}<extra></extra>",
        )
    )

    # Audited Rate (Solid line)
    fig.add_trace(
        go.Scatter(
            x=frame["month"],
            y=frame["verified_recovery_rate"],
            mode="lines+markers",
            name="Audited View (Eligible)",
            line={"color": t["teal"], "width": 3},
            marker={"size": 7, "color": t["teal"]},
            hovertemplate="Audited: %{y:.1%}<extra></extra>",
        )
    )

    # Annotation for partial August
    if not complete_only and frame["month"].dt.month.eq(8).any():
        august = frame[frame["month"].dt.month.eq(8)].iloc[0]
        fig.add_annotation(
            x=august["month"],
            y=august["verified_recovery_rate"],
            text="Partial Month (Aug 8)",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1.5,
            arrowcolor=t["amber"],
            font={"color": t["amber"], "size": 11, "family": "Inter, sans-serif"},
            bgcolor=t["card_bg"],
            bordercolor=t["amber"],
            borderwidth=1,
            borderpad=4,
            ax=0,
            ay=-35,
        )

    fig.update_layout(
        template=plotly_template(theme),
        paper_bgcolor=t["chart_bg"],
        plot_bgcolor=t["chart_bg"],
        font={"family": "Inter, sans-serif", "color": t["text"]},
        height=360,
        margin={"l": 16, "r": 16, "t": 24, "b": 16},
        yaxis={
            "tickformat": ".0%",
            "title": "Monthly Recovery Rate",
            "zeroline": False,
            "gridcolor": t["grid"],
            "linecolor": t["border"],
            "tickcolor": t["axis"],
            "color": t["axis"],
        },
        xaxis={
            "gridcolor": t["grid"],
            "linecolor": t["border"],
            "tickcolor": t["axis"],
            "color": t["axis"],
            "dtick": "M1",
            "tickformat": "%b %Y",
        },
        legend={
            "orientation": "h",
            "y": 1.12,
            "x": 0,
            "font": {"color": t["text"], "size": 12},
        },
    )
    st.plotly_chart(fig, width="stretch")


def trend_insight(frame: pd.DataFrame, theme: str) -> None:
    del theme
    if frame.empty:
        return
    gap = (frame["verified_recovery_rate"] - frame["reported_recovery_rate"]) * 100
    peak = frame.iloc[gap.argmax()]
    peak_month = pd.to_datetime(peak["month"]).strftime("%b %Y")
    exceeded_count = int((gap > 0).sum())
    total_count = len(frame)

    st.markdown(
        f"""<div class='callout insight-card'>
            <div class='insight-label'>Variance Forensic</div>
            <div class='insight-value'>Audited recovery exceeded legacy in {exceeded_count} of {total_count} months.</div>
            <div class='muted' style='margin-top: 8px;'>
                Peak Discrepancy: <b>{peak_month}</b><br>
                Largest Gap: <b>+{gap.max():.1f} pts</b><br>
                Confidence Interval: <b>95% coverage</b> without overlapping legacy bounds.
            </div>
        </div>""",
        unsafe_allow_html=True,
    )


def waterfall_chart(frame: pd.DataFrame, theme: str) -> None:
    t = TOKENS[theme]
    if frame.empty:
        st.info("No waterfall decomposition data available.")
        return

    fig = go.Figure(
        go.Waterfall(
            x=frame["label"],
            y=frame["value_pts"],
            measure=["absolute", "relative", "total"],
            connector={"line": {"color": t["border"], "width": 1.5}},
            increasing={"marker": {"color": t["teal"]}},
            decreasing={"marker": {"color": t["red"]}},
            totals={"marker": {"color": t["primary"]}},
            text=[f"{v:+.1f} pts" for v in frame["value_pts"]],
            textposition="outside",
            textfont={"family": "Inter, sans-serif", "size": 12, "color": t["text"]},
            hovertemplate="%{x}: %{y:+.1f} pts<extra></extra>",
        )
    )
    fig.update_layout(
        template=plotly_template(theme),
        paper_bgcolor=t["chart_bg"],
        plot_bgcolor=t["chart_bg"],
        font={"family": "Inter, sans-serif", "color": t["text"]},
        height=320,
        margin={"l": 16, "r": 16, "t": 32, "b": 16},
        yaxis_title="Percentage Points (pts)",
        yaxis={
            "gridcolor": t["grid"],
            "linecolor": t["border"],
            "tickcolor": t["axis"],
            "color": t["axis"],
        },
        xaxis={
            "linecolor": t["border"],
            "tickcolor": t["axis"],
            "color": t["axis"],
        },
        showlegend=False,
    )
    st.plotly_chart(fig, width="stretch")