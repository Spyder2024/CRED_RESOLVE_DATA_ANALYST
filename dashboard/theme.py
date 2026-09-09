import streamlit as st


TOKENS = {
    "light": {
        "page_bg": "#F8FAFC",
        "card_bg": "#FFFFFF",
        "nav_hover_bg": "rgba(15, 23, 42, 0.04)",
        "nav_active_bg": "rgba(15, 23, 42, 0.08)",
        "border": "#E2E8F0",
        "border_strong": "#CBD5E1",
        "text": "#0F172A",
        "secondary": "#64748B",
        "muted": "#94A3B8",
        "primary": "#0F172A",
        "legacy": "#64748B",
        "teal": "#059669",
        "red": "#DC2626",
        "amber": "#D97706",
        "blue": "#2563EB",
        "grid": "#E8EEF5",
        "chart_bg": "#FFFFFF",
        "axis": "#475569",
        "shadow": "rgba(15, 23, 42, 0.06)",
        "shadow_hover": "rgba(15, 23, 42, 0.12)",
    },
    "dark": {
        "page_bg": "#0B1220",
        "card_bg": "#131D31",
        "nav_hover_bg": "rgba(248, 250, 252, 0.05)",
        "nav_active_bg": "rgba(248, 250, 252, 0.10)",
        "border": "#22314E",
        "border_strong": "#334568",
        "text": "#F8FAFC",
        "secondary": "#94A3B8",
        "muted": "#64748B",
        "primary": "#F8FAFC",
        "legacy": "#94A3B8",
        "teal": "#34D399",
        "red": "#F87171",
        "amber": "#FBBF24",
        "blue": "#60A5FA",
        "grid": "#1A263D",
        "chart_bg": "#131D31",
        "axis": "#CBD5E1",
        "shadow": "rgba(0, 0, 0, 0.35)",
        "shadow_hover": "rgba(0, 0, 0, 0.50)",
    },
}


def inject_css(theme: str) -> None:
    t = TOKENS[theme]
    variables = "; ".join(f"--{key.replace('_', '-')}: {value}" for key, value in t.items())
    st.markdown(
        f"""<style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        :root {{
            {variables};
            color-scheme: {theme};
        }}

        /* Reset & Global Typography */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {{
            background-color: var(--page-bg) !important;
            color: var(--text);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            -webkit-font-smoothing: antialiased;
        }}
        
        .stApp, .stApp * {{
            font-family: 'Inter', sans-serif;
        }}

        .stApp [data-testid="stIconMaterial"] {{
            font-family: "Material Symbols Rounded", "Material Symbols Outlined", sans-serif !important;
            font-variation-settings: "FILL" 0, "wght" 500, "GRAD" 0, "opsz" 20;
        }}

        [data-testid="stAppViewContainer"] > .main {{
            background: var(--page-bg);
        }}

        .block-container {{
            max-width: 1280px;
            padding: 1.5rem 2rem 3rem !important;
        }}

        /* Strict 280px Enterprise Sidebar */
        section[data-testid="stSidebar"] {{
            width: 280px !important;
            min-width: 280px !important;
            max-width: 280px !important;
            background: var(--card-bg) !important;
            border-right: 1px solid var(--border) !important;
            box-shadow: 1px 0 12px var(--shadow);
        }}

        section[data-testid="stSidebar"] > div:first-child {{
            background: var(--card-bg) !important;
            padding: 1.25rem 1rem 2rem;
        }}

        /* Professional Sidebar Navigation */
        nav[data-testid="stSidebarNav"] {{
            width: 100%;
            margin-bottom: 1.25rem;
        }}

        nav[data-testid="stSidebarNav"] span[data-testid="stSidebarNavSectionHeader"],
        nav[data-testid="stSidebarNav"] div[data-testid="stSidebarNavItems"] > div > span {{
            font-size: 11px !important;
            font-weight: 700 !important;
            letter-spacing: 0.08em !important;
            text-transform: uppercase !important;
            color: var(--secondary) !important;
            padding: 0.75rem 0.75rem 0.35rem !important;
            display: block;
        }}

        nav[data-testid="stSidebarNav"] a {{
            display: flex !important;
            align-items: center !important;
            gap: 10px !important;
            padding: 8px 12px !important;
            border-radius: 8px !important;
            color: var(--secondary) !important;
            font-size: 13px !important;
            font-weight: 500 !important;
            text-decoration: none !important;
            transition: background 0.15s ease, color 0.15s ease, border-color 0.15s ease !important;
            border: 1px solid transparent !important;
            margin-bottom: 3px;
        }}

        nav[data-testid="stSidebarNav"] a:hover {{
            background: var(--nav-hover-bg) !important;
            color: var(--text) !important;
            border-color: var(--border) !important;
        }}

        nav[data-testid="stSidebarNav"] a[aria-current="page"] {{
            background: var(--nav-active-bg) !important;
            color: var(--text) !important;
            font-weight: 600 !important;
            border-color: color-mix(in srgb, var(--primary) 20%, var(--border)) !important;
        }}

        nav[data-testid="stSidebarNav"] svg {{
            fill: currentColor !important;
            color: inherit !important;
        }}

        /* Header overrides */
        div[data-testid="stHeader"], header {{
            background: var(--page-bg) !important;
        }}
        div[data-testid="stHeader"] button, header button {{
            color: var(--text) !important;
        }}

        /* General element colors */
        h1, h2, h3, h4, h5, h6, p, span, label, small {{
            color: var(--text);
        }}
        .stCaption, [data-testid="stCaptionContainer"] {{
            color: var(--secondary) !important;
        }}

        /* Inputs & Interactive Controls */
        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div,
        div[data-baseweb="textarea"] > div {{
            background: var(--card-bg) !important;
            color: var(--text) !important;
            border-color: var(--border) !important;
            border-radius: 8px !important;
        }}
        div[data-baseweb="select"] *, div[data-baseweb="input"] *, div[data-baseweb="textarea"] * {{
            color: var(--text) !important;
        }}
        div[data-baseweb="select"] svg, div[data-baseweb="input"] svg {{
            fill: var(--secondary) !important;
            color: var(--secondary) !important;
        }}
        div[data-baseweb="popover"] > div, ul[role="listbox"] {{
            background: var(--card-bg) !important;
            border: 1px solid var(--border) !important;
            border-radius: 8px !important;
            box-shadow: 0 8px 24px var(--shadow) !important;
        }}
        ul[role="listbox"] li, ul[role="listbox"] li * {{
            color: var(--text) !important;
            background: var(--card-bg) !important;
        }}
        button[kind="secondary"], button[kind="tertiary"] {{
            color: var(--text) !important;
            background: var(--card-bg) !important;
            border-color: var(--border) !important;
            border-radius: 8px !important;
            transition: all 0.15s ease !important;
        }}
        button[kind="secondary"]:hover, button[kind="tertiary"]:hover {{
            color: var(--primary) !important;
            border-color: var(--border-strong) !important;
            background: var(--nav-hover-bg) !important;
        }}
        button[kind="primary"] {{
            background: var(--primary) !important;
            color: var(--page-bg) !important;
            border: none !important;
            border-radius: 8px !important;
        }}

        [data-testid="stToggle"] [data-baseweb="checkbox"] > div {{
            background: var(--border);
            border-color: var(--border);
        }}
        [data-testid="stToggle"] [data-baseweb="checkbox"] input:checked + div {{
            background: var(--teal);
            border-color: var(--teal);
        }}
        [data-testid="stToggle"] label, [data-testid="stCheckbox"] label {{
            color: var(--text);
            font-size: 13px;
        }}

        /* DataTables & DataFrames */
        div[data-testid="stDataFrame"], div[data-testid="stTable"] {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 10px;
        }}
        div[data-testid="stDataFrame"] iframe {{
            background: var(--card-bg);
        }}

        /* Alerts */
        [data-testid="stAlert"] {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            color: var(--text);
            border-radius: 10px;
        }}

        #MainMenu, footer {{
            visibility: hidden;
        }}

        /* Enterprise Top Nav Bar */
        .top-nav {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            padding: 10px 0 16px;
            border-bottom: 1px solid var(--border);
            margin-bottom: 22px;
            font-size: 12px;
        }}
        .top-nav-brand {{
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 700;
            letter-spacing: -0.01em;
            color: var(--text);
        }}
        .top-nav-breadcrumbs {{
            display: flex;
            align-items: center;
            gap: 8px;
            color: var(--secondary);
        }}
        .top-nav-breadcrumbs .crumb-active {{
            color: var(--text);
            font-weight: 600;
        }}
        .top-nav-meta {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        /* Enterprise Page Header */
        .page-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 24px;
            flex-wrap: wrap;
            margin-bottom: 24px;
        }}
        .page-header-main {{
            flex: 1 1 500px;
            min-width: 0;
        }}
        .page-eyebrow {{
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--secondary);
            margin-bottom: 6px;
        }}
        .page-title {{
            font-size: 28px;
            font-weight: 700;
            letter-spacing: -0.02em;
            line-height: 1.25;
            color: var(--text);
            margin: 0 0 8px 0;
        }}
        .page-desc {{
            font-size: 14px;
            line-height: 1.55;
            color: var(--secondary);
            margin: 0;
        }}
        .page-header-aside {{
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            gap: 10px;
            flex-shrink: 0;
        }}
        .badge-group {{
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }}

        /* Section Headings */
        .section-head {{
            margin: 32px 0 16px;
        }}
        .section-head h2 {{
            margin: 0;
            font-size: 20px;
            font-weight: 700;
            letter-spacing: -0.02em;
            color: var(--text);
        }}
        .section-head p {{
            margin: 4px 0 0;
            color: var(--secondary);
            font-size: 13px;
            line-height: 1.5;
        }}

        /* Enterprise Executive Summary / Verdict Banner (Flexbox, No Absolute Positioning) */
        .verdict-banner {{
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 24px;
            background: linear-gradient(135deg, color-mix(in srgb, var(--red) 8%, var(--card-bg)), var(--card-bg));
            border: 1px solid color-mix(in srgb, var(--red) 32%, var(--border));
            border-left: 5px solid var(--red);
            border-radius: 14px;
            padding: 24px;
            margin: 8px 0 24px;
            box-shadow: 0 4px 20px var(--shadow);
        }}
        .verdict-banner-body {{
            flex: 1 1 auto;
            min-width: 0;
        }}
        .verdict-banner-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 10px;
            border-radius: 999px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: var(--red);
            background: color-mix(in srgb, var(--red) 12%, transparent);
            margin-bottom: 12px;
        }}
        .verdict-banner-title {{
            font-size: 22px;
            font-weight: 700;
            letter-spacing: -0.02em;
            line-height: 1.3;
            color: var(--text);
            margin: 0 0 8px 0;
        }}
        .verdict-banner-text {{
            font-size: 14px;
            line-height: 1.6;
            color: var(--secondary);
            margin: 0;
            max-width: 820px;
        }}
        .verdict-banner-icon {{
            flex-shrink: 0;
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background: color-mix(in srgb, var(--red) 14%, transparent);
            color: var(--red);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            font-weight: 800;
        }}
        .verdict-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-top: 20px;
            padding-top: 18px;
            border-top: 1px solid color-mix(in srgb, var(--red) 20%, var(--border));
        }}
        .verdict-grid-item {{
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}
        .verdict-grid-label {{
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--secondary);
        }}
        .verdict-grid-value {{
            font-size: 22px;
            font-weight: 700;
            letter-spacing: -0.02em;
            color: var(--text);
        }}

        /* Content-Driven Production Cards */
        .card {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 18px 20px;
            box-shadow: 0 2px 10px var(--shadow);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            gap: 10px;
            min-height: min-content;
            box-sizing: border-box;
            transition: border-color 0.15s ease, box-shadow 0.15s ease, transform 0.15s ease;
        }}
        .card:hover {{
            border-color: color-mix(in srgb, var(--blue) 40%, var(--border));
            box-shadow: 0 6px 20px var(--shadow_hover);
            transform: translateY(-1px);
        }}
        .card-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
        }}
        .card-label {{
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: var(--secondary);
        }}
        .card-icon {{
            width: 28px;
            height: 28px;
            border-radius: 8px;
            background: color-mix(in srgb, var(--blue) 12%, transparent);
            color: var(--blue);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            font-weight: 700;
        }}
        .kpi-value {{
            font-size: 28px;
            font-weight: 700;
            letter-spacing: -0.03em;
            line-height: 1.25;
            color: var(--text);
            margin: 4px 0;
        }}
        .card-meta {{
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }}
        .metric-trend {{
            font-size: 12px;
            font-weight: 700;
            color: var(--teal);
        }}
        .metric-trend.negative {{
            color: var(--red);
        }}
        .muted {{
            color: var(--secondary);
            font-size: 12px;
            line-height: 1.5;
        }}

        /* Status Pills & Badges */
        .status-pill {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 5px 12px;
            border-radius: 999px;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.04em;
            white-space: nowrap;
            flex-shrink: 0;
            box-sizing: border-box;
        }}
        .status-pill::before {{
            content: "";
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: currentColor;
        }}
        .status-good {{
            color: var(--teal);
            background: color-mix(in srgb, var(--teal) 12%, transparent);
            border: 1px solid color-mix(in srgb, var(--teal) 25%, transparent);
        }}
        .status-warn {{
            color: var(--amber);
            background: color-mix(in srgb, var(--amber) 12%, transparent);
            border: 1px solid color-mix(in srgb, var(--amber) 25%, transparent);
        }}
        .status-bad {{
            color: var(--red);
            background: color-mix(in srgb, var(--red) 12%, transparent);
            border: 1px solid color-mix(in srgb, var(--red) 25%, transparent);
        }}
        .status-neutral {{
            color: var(--secondary);
            background: color-mix(in srgb, var(--secondary) 10%, transparent);
            border: 1px solid var(--border);
        }}

        .badge-red, .badge-amber, .badge-teal {{
            display: inline-block;
            border-radius: 999px;
            padding: 4px 10px;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.03em;
        }}
        .badge-red {{
            color: var(--red);
            background: color-mix(in srgb, var(--red) 13%, transparent);
        }}
        .badge-amber {{
            color: var(--amber);
            background: color-mix(in srgb, var(--amber) 13%, transparent);
        }}
        .badge-teal {{
            color: var(--teal);
            background: color-mix(in srgb, var(--teal) 13%, transparent);
        }}

        /* Callouts & Insights */
        .callout {{
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 18px 20px;
            background: var(--card-bg);
            box-shadow: 0 2px 10px var(--shadow);
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        .insight-card {{
            border-left: 4px solid var(--blue);
        }}
        .insight-label {{
            color: var(--blue);
            font-size: 11px;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            font-weight: 800;
        }}
        .insight-value {{
            font-size: 16px;
            font-weight: 700;
            line-height: 1.4;
            color: var(--text);
            margin: 4px 0;
        }}

        .confidence-meter {{
            height: 6px;
            background: color-mix(in srgb, var(--teal) 15%, var(--border));
            border-radius: 999px;
            overflow: hidden;
            margin-top: 8px;
        }}
        .confidence-meter span {{
            display: block;
            width: 95%;
            height: 100%;
            background: var(--teal);
            border-radius: inherit;
        }}

        /* Audit Timeline (Flexbox, No Coordinate Math) */
        .audit-timeline {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            padding: 16px 12px;
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            margin: 12px 0;
            flex-wrap: wrap;
        }}
        .timeline-step {{
            display: flex;
            align-items: center;
            gap: 8px;
            color: var(--secondary);
            font-size: 12px;
            font-weight: 500;
        }}
        .timeline-step.active {{
            color: var(--text);
            font-weight: 600;
        }}
        .timeline-dot {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: var(--teal);
            box-shadow: 0 0 0 3px color-mix(in srgb, var(--teal) 20%, transparent);
            flex-shrink: 0;
        }}
        .timeline-arrow {{
            color: var(--muted);
            font-size: 14px;
        }}

        /* Lineage Flow */
        .flow {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            flex-wrap: wrap;
            margin: 14px 0;
        }}
        .flow-step {{
            flex: 1 1 140px;
            text-align: center;
            padding: 14px;
            border: 1px solid var(--border);
            border-radius: 10px;
            background: var(--card-bg);
            box-shadow: 0 2px 8px var(--shadow);
        }}
        .flow-step b {{
            font-size: 13px;
            color: var(--text);
            display: block;
            margin-bottom: 4px;
        }}

        /* Enterprise Footer */
        .platform-footer {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 16px;
            padding: 24px 0 12px;
            margin-top: 40px;
            border-top: 1px solid var(--border);
            font-size: 12px;
            color: var(--secondary);
        }}
        .footer-left {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .footer-right {{
            display: flex;
            align-items: center;
            gap: 16px;
        }}

        /* Responsive Breakpoints */
        @media (max-width: 900px) {{
            .verdict-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
            .block-container {{
                padding: 1rem 1rem 2rem !important;
            }}
        }}
        @media (max-width: 760px) {{
            .page-header {{
                flex-direction: column;
            }}
            .page-header-aside {{
                align-items: flex-start;
            }}
            .page-title {{
                font-size: 24px;
            }}
            .verdict-banner {{
                flex-direction: column;
            }}
            .verdict-grid {{
                grid-template-columns: 1fr;
            }}
        }}
        </style>""",
        unsafe_allow_html=True,
    )


def plotly_template(theme: str) -> str:
    t = TOKENS[theme]
    import plotly.io as pio
    name = f"fc_{theme}"
    pio.templates[name] = {
        "layout": {
            "font": {"family": "Inter, sans-serif", "color": t["text"]},
            "paper_bgcolor": t["chart_bg"],
            "plot_bgcolor": t["chart_bg"],
            "colorway": [t["primary"], t["teal"], t["legacy"], t["amber"], t["blue"]],
            "xaxis": {
                "gridcolor": t["grid"],
                "linecolor": t["border"],
                "tickcolor": t["axis"],
                "color": t["axis"],
                "zerolinecolor": t["grid"],
            },
            "yaxis": {
                "gridcolor": t["grid"],
                "linecolor": t["border"],
                "tickcolor": t["axis"],
                "color": t["axis"],
                "zerolinecolor": t["grid"],
            },
            "hoverlabel": {
                "bgcolor": t["card_bg"],
                "bordercolor": t["border"],
                "font": {"family": "Inter, sans-serif", "color": t["text"]},
            },
        }
    }
    return name