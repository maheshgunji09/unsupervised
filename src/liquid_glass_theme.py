"""
Apple Liquid Glass Design System - macOS Tahoe Dark Tint
Refined design tokens and monochrome iconography matching Apple WWDC25 Liquid Glass specifications.
"""

import urllib.parse

# -----------------------------------------------------------------------------
# 1. LUCIDE MONOCHROME ICON SYSTEM (SVG STRINGS)
# -----------------------------------------------------------------------------
LUCIDE_ICONS = {
    'layout-dashboard': (
        '<rect width="7" height="9" x="3" y="3" rx="1"/>'
        '<rect width="7" height="5" x="14" y="3" rx="1"/>'
        '<rect width="7" height="9" x="14" y="12" rx="1"/>'
        '<rect width="7" height="5" x="3" y="16" rx="1"/>'
    ),
    'chart-no-axes-combined': (
        '<path d="M12 16v5"/><path d="M16 14v7"/><path d="M20 10v11"/>'
        '<path d="m22 3-8.646 8.646a.5.5 0 0 1-.708 0L9.354 8.354a.5.5 0 0 0-.707 0L2 15"/>'
        '<path d="M4 18v3"/><path d="M8 14v7"/>'
    ),
    'workflow': (
        '<rect width="8" height="8" x="3" y="3" rx="2"/>'
        '<path d="M7 11v4a2 2 0 0 0 2 2h4"/>'
        '<rect width="8" height="8" x="13" y="13" rx="2"/>'
    ),
    'map': (
        '<path d="M14.106 5.553a2 2 0 0 0 1.788 0l3.659-1.83A1 1 0 0 1 21 4.619v12.764a1 1 0 0 1-.553.894l-4.553 2.277a2 2 0 0 1-1.788 0l-4.212-2.106a2 2 0 0 0-1.788 0l-3.659 1.83A1 1 0 0 1 3 19.381V6.618a1 1 0 0 1 .553-.894l4.553-2.277a2 2 0 0 1 1.788 0z"/>'
        '<path d="M15 5.764v15"/><path d="M9 3.236v15"/>'
    ),
    'orbit': (
        '<circle cx="12" cy="12" r="3"/>'
        '<path d="M20.17 17.6a9 9 0 0 0-16.34 0"/>'
        '<path d="M3.83 6.4a9 9 0 0 0 16.34 0"/>'
    ),
    'chart-bar': (
        '<path d="M3 3v16a2 2 0 0 0 2 2h16"/>'
        '<path d="M7 16h3"/><path d="M7 11h7"/><path d="M7 6h11"/>'
    ),
    'users': (
        '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>'
        '<circle cx="9" cy="7" r="4"/>'
        '<path d="M22 21v-2a4 4 0 0 0-3-3.87"/>'
        '<path d="M16 3.13a4 4 0 0 1 0 7.75"/>'
    ),
    'compass': (
        '<circle cx="12" cy="12" r="10"/>'
        '<polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>'
    ),
    'database': (
        '<ellipse cx="12" cy="5" rx="9" ry="3"/>'
        '<path d="M3 5V19A9 3 0 0 0 21 19V5"/>'
        '<path d="M3 12A9 3 0 0 0 21 12"/>'
    ),
    'star': (
        '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>'
    ),
    'map-pin': (
        '<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/>'
        '<circle cx="12" cy="10" r="3"/>'
    ),
    'message-square': (
        '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>'
    ),
    'thumbs-up': (
        '<path d="M7 10v12"/><path d="M15 5.88 14 10h5.83a2 2 0 0 1 1.92 2.56l-2.33 8A2 2 0 0 1 17.5 22H4a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2h2.76a2 2 0 0 0 1.79-1.11L12 2a3.13 3.13 0 0 1 3 3.88Z"/>'
    ),
    'trending-up': (
        '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/>'
        '<polyline points="16 7 22 7 22 13"/>'
    ),
    'ticket': (
        '<path d="M2 9a3 3 0 0 1 0 6v2a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-2a3 3 0 0 1 0-6V7a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"/>'
        '<path d="M13 5v2"/><path d="M13 17v2"/><path d="M13 11v2"/>'
    ),
    'clock': (
        '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>'
    ),
    'download': (
        '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>'
        '<polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/>'
    ),
    'layers': (
        '<polygon points="12 2 2 7 12 12 22 7 12 2"/>'
        '<polyline points="2 17 12 22 22 17"/>'
        '<polyline points="2 12 12 17 22 12"/>'
    ),
    'sliders': (
        '<line x1="4" x2="4" y1="21" y2="14"/><line x1="4" x2="4" y1="10" y2="3"/>'
        '<line x1="12" x2="12" y1="21" y2="12"/><line x1="12" x2="12" y1="8" y2="3"/>'
        '<line x1="20" x2="20" y1="21" y2="16"/><line x1="20" x2="20" y1="12" y2="3"/>'
        '<line x1="1" x2="7" y1="14" y2="14"/><line x1="9" x2="15" y1="8" y2="8"/>'
        '<line x1="17" x2="23" y1="16" y2="16"/>'
    ),
    'alert-circle': (
        '<circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/>'
        '<line x1="12" x2="12.01" y1="16" y2="16"/>'
    ),
    'landmark': (
        '<line x1="3" x2="21" y1="22" y2="22"/><line x1="6" x2="6" y1="18" y2="11"/>'
        '<line x1="10" x2="10" y1="18" y2="11"/><line x1="14" x2="14" y1="18" y2="11"/>'
        '<line x1="18" x2="18" y1="18" y2="11"/><polygon points="12 2 20 7 4 7"/>'
    ),
    'trees': (
        '<path d="M10 10v.2A3 3 0 0 1 8.9 16H5a3 3 0 0 1-1-5.8V10a3 3 0 0 1 6 0Z"/>'
        '<path d="M7 16v6"/><path d="M13 19v3"/>'
        '<path d="M12 19h8.3a1 1 0 0 0 .7-1.7L18 14h.3a1 1 0 0 0 .7-1.7L16 9h.2a1 1 0 0 0 .8-1.7L13 3l-1.4 1.5"/>'
    )
}

def get_lucide_icon(name: str, size: int = 18, color: str = "currentColor", stroke_width: float = 1.8) -> str:
    """Returns an inline monochrome SVG element for a Lucide icon."""
    path = LUCIDE_ICONS.get(name, LUCIDE_ICONS['compass'])
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" '
        f'stroke-linecap="round" stroke-linejoin="round" style="vertical-align: -2px; display: inline-block;">'
        f'{path}</svg>'
    )

def _build_svg_data_uri(icon_name: str, stroke_hex: str = "%23F5F5F7") -> str:
    """Builds a URL-encoded SVG data URI for CSS background injection."""
    path = LUCIDE_ICONS.get(icon_name, LUCIDE_ICONS['compass'])
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" '
        f'fill="none" stroke="{stroke_hex}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
        f'{path}</svg>'
    )
    return "data:image/svg+xml;utf8," + svg

# Pre-generate CSS data URIs for all 9 sidebar items
NAV_ICON_NAMES = [
    'layout-dashboard',
    'chart-no-axes-combined',
    'workflow',
    'map',
    'orbit',
    'chart-bar',
    'users',
    'compass',
    'database'
]

# -----------------------------------------------------------------------------
# 2. CENTRAL CSS DESIGN-TOKEN SYSTEM (MACOS TAHOE DARK TINT)
# -----------------------------------------------------------------------------
def get_liquid_glass_css() -> str:
    """
    Returns central CSS design tokens adhering to Apple macOS Tahoe Dark Tint Liquid Glass.
    Completely eliminates cyberpunk neons, saturated glows, and decorative emojis.
    """
    # Build sidebar icon pseudo-element rules
    sidebar_icon_rules = []
    for i, icon in enumerate(NAV_ICON_NAMES, start=1):
        uri_normal = _build_svg_data_uri(icon, stroke_hex="%23A1A1AA")
        uri_active = _build_svg_data_uri(icon, stroke_hex="%23F5F5F7")
        sidebar_icon_rules.append(f"""
        [data-testid="stRadio"] label:nth-of-type({i})::before {{
            content: '';
            display: inline-block;
            width: 17px;
            height: 17px;
            margin-right: 11px;
            background-image: url('{uri_normal}');
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
            vertical-align: -2.5px;
            opacity: 0.75;
            transition: opacity 180ms ease, filter 180ms ease;
        }}
        [data-testid="stRadio"] label:nth-of-type({i}):hover::before,
        [data-testid="stRadio"] label:nth-of-type({i})[data-checked="true"]::before,
        [data-testid="stRadio"] [aria-checked="true"]:nth-of-type({i})::before {{
            opacity: 1;
            background-image: url('{uri_active}');
        }}
        """)
    sidebar_icons_css = "\n".join(sidebar_icon_rules)

    return f"""
<style>
/* -------------------------------------------------------------------------
   APPLE MACOS TAHOE LIQUID GLASS DESIGN TOKENS
   ------------------------------------------------------------------------- */
:root {{
  /* Background system */
  --app-background: #141418;
  --app-background-deep: #101014;
  --app-background-elevated: #1C1B20;

  --ambient-warm: rgba(205, 171, 143, 0.08);
  --ambient-cool: rgba(164, 151, 190, 0.06);

  /* Liquid Glass materials */
  --glass-primary: rgba(250, 250, 252, 0.075);
  --glass-floating: rgba(35, 35, 40, 0.72);
  --glass-secondary: rgba(250, 250, 252, 0.045);
  --glass-hover: rgba(250, 250, 252, 0.085);

  --glass-border: rgba(255, 255, 255, 0.14);
  --glass-specular: rgba(255, 255, 255, 0.30);
  --glass-highlight: rgba(255, 255, 255, 0.42);
  --glass-shadow: rgba(0, 0, 0, 0.38);

  /* Typography */
  --text-primary: #F5F5F7;
  --text-secondary: rgba(235, 235, 245, 0.72);
  --text-tertiary: rgba(235, 235, 245, 0.46);
  --text-muted: rgba(235, 235, 245, 0.28);

  /* Apple-inspired functional accents */
  --system-blue: #0A84FF;
  --system-green: #30D158;
  --system-orange: #FF9F0A;
  --system-yellow: #FFD60A;
  --system-purple: #BF5AF2;
  --system-cyan: #64D2FF;
  --system-pink: #FF375F;

  /* Animation timing */
  --apple-ease: cubic-bezier(0.16, 1, 0.3, 1);
  --apple-duration: 240ms;
}}

/* -------------------------------------------------------------------------
   GLOBAL ATMOSPHERE (RESTRAINED GRAPHITE DESKTOP)
   ------------------------------------------------------------------------- */
html, body, [data-testid="stAppViewContainer"] {{
    background-color: var(--app-background) !important;
    background-image: 
        radial-gradient(circle at 18% 12%, var(--ambient-warm) 0%, transparent 45%),
        radial-gradient(circle at 82% 28%, var(--ambient-cool) 0%, transparent 48%),
        linear-gradient(180deg, var(--app-background-elevated) 0%, var(--app-background-deep) 100%) !important;
    background-attachment: fixed !important;
    color: var(--text-primary) !important;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Helvetica Neue", sans-serif !important;
    -webkit-font-smoothing: antialiased !important;
    -moz-osx-font-smoothing: grayscale !important;
}}

/* Hide Streamlit Header Chrome */
header[data-testid="stHeader"] {{
    background: transparent !important;
}}
#MainMenu, footer {{
    visibility: hidden;
}}

.block-container {{
    padding-top: 2rem !important;
    padding-bottom: 3.5rem !important;
    max-width: 1360px !important;
}}

/* -------------------------------------------------------------------------
   MATERIAL 1: PRIMARY GLASS PANELS
   ------------------------------------------------------------------------- */
.glass-panel {{
    background: var(--glass-primary);
    backdrop-filter: blur(20px) saturate(150%);
    -webkit-backdrop-filter: blur(20px) saturate(150%);
    border-radius: 24px;
    border: 1px solid var(--glass-border);
    border-top: 1px solid var(--glass-specular);
    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.20),
        inset 0 -1px 0 rgba(255, 255, 255, 0.045),
        0 14px 40px var(--glass-shadow);
    padding: 32px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
    transition: all var(--apple-duration) var(--apple-ease);
}}

.glass-panel:hover {{
    border-top-color: var(--glass-highlight);
    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.28),
        inset 0 -1px 0 rgba(255, 255, 255, 0.05),
        0 18px 48px rgba(0, 0, 0, 0.44);
}}

/* -------------------------------------------------------------------------
   MATERIAL 2: FLOATING GLASS (SIDEBAR & ELEVATED CONTROLS)
   ------------------------------------------------------------------------- */
section[data-testid="stSidebar"] {{
    background: var(--glass-floating) !important;
    backdrop-filter: blur(28px) saturate(150%) !important;
    -webkit-backdrop-filter: blur(28px) saturate(150%) !important;
    border-right: 1px solid var(--glass-border) !important;
    box-shadow: 0 20px 48px var(--glass-shadow) !important;
}}

section[data-testid="stSidebar"] > div:first-child {{
    padding-top: 1.5rem !important;
    padding-left: 1.25rem !important;
    padding-right: 1.25rem !important;
}}

/* -------------------------------------------------------------------------
   MATERIAL 3: NESTED SECONDARY CARDS & KPI METRICS
   ------------------------------------------------------------------------- */
.glass-card, .apple-metric-card {{
    background: var(--glass-secondary);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-radius: 18px;
    border: 1px solid var(--glass-border);
    border-top: 1px solid rgba(255, 255, 255, 0.24);
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.15), 0 8px 24px rgba(0, 0, 0, 0.20);
    padding: 22px 20px;
    transition: all var(--apple-duration) var(--apple-ease);
    position: relative;
}}

.glass-card:hover, .apple-metric-card:hover {{
    background: var(--glass-hover);
    border-top-color: var(--glass-highlight);
    transform: translateY(-2px);
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.25), 0 12px 30px rgba(0, 0, 0, 0.30);
}}

/* Clean KPI Typography (No neon accents) */
.metric-title {{
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: var(--text-tertiary);
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 7px;
}}

.metric-value {{
    font-size: 2.1rem;
    font-weight: 700;
    letter-spacing: -0.6px;
    color: var(--text-primary);
    line-height: 1.15;
    margin-bottom: 6px;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif;
}}

.metric-subtitle {{
    font-size: 0.8rem;
    color: var(--text-secondary);
    display: flex;
    align-items: center;
    gap: 6px;
}}

/* -------------------------------------------------------------------------
   MATERIAL 4: PILLS & BADGES
   ------------------------------------------------------------------------- */
.glass-pill {{
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(14px);
    border-radius: 9999px;
    padding: 5px 13px;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-top: 1px solid rgba(255, 255, 255, 0.25);
    font-size: 0.78rem;
    font-weight: 500;
    color: var(--text-secondary);
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.15);
}}

/* -------------------------------------------------------------------------
   MACOS HEADER & MONOCHROME SIDEBAR NAVIGATION
   ------------------------------------------------------------------------- */
.macos-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 14px;
    margin-bottom: 18px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}}

.macos-traffic-lights {{
    display: flex;
    align-items: center;
    gap: 8px;
}}

.traffic-light {{
    width: 12px;
    height: 12px;
    border-radius: 50%;
    display: inline-block;
    box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.4), 0 1px 2px rgba(0, 0, 0, 0.35);
}}

.light-red {{ background: #ff5f56; }}
.light-yellow {{ background: #ffbd2e; }}
.light-green {{ background: #27c93f; }}

/* Streamlit Radio Nav Styling */
[data-testid="stRadio"] > div {{
    gap: 5px !important;
}}

[data-testid="stRadio"] label {{
    background: transparent !important;
    border: 1px solid transparent !important;
    border-radius: 12px !important;
    padding: 9px 12px !important;
    color: var(--text-secondary) !important;
    font-size: 0.90rem !important;
    font-weight: 500 !important;
    transition: all var(--apple-duration) var(--apple-ease) !important;
    cursor: pointer !important;
}}

[data-testid="stRadio"] label:hover {{
    background: rgba(255, 255, 255, 0.05) !important;
    color: var(--text-primary) !important;
    border-color: rgba(255, 255, 255, 0.08) !important;
}}

/* Active Navigation Selection: Restrained Apple Tahoe Highlight */
[data-testid="stRadio"] label[data-checked="true"],
[data-testid="stRadio"] [aria-checked="true"] {{
    background: rgba(255, 255, 255, 0.09) !important;
    backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(255, 255, 255, 0.16) !important;
    border-top: 1px solid rgba(255, 255, 255, 0.32) !important;
    color: #ffffff !important;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.20), 0 4px 14px rgba(0, 0, 0, 0.25) !important;
    font-weight: 600 !important;
}}

/* Inject Lucide SVG icons next to each navigation label */
{sidebar_icons_css}

/* -------------------------------------------------------------------------
   STREAMLIT FORM CONTROLS & WIDGETS ELEVATION
   ------------------------------------------------------------------------- */
/* Tabs */
.stTabs [data-baseweb="tab-list"] {{
    background: rgba(255, 255, 255, 0.035) !important;
    backdrop-filter: blur(20px) !important;
    padding: 5px !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255, 255, 255, 0.09) !important;
    border-top: 1px solid rgba(255, 255, 255, 0.20) !important;
    gap: 4px !important;
}}

.stTabs [data-baseweb="tab"] {{
    border-radius: 10px !important;
    padding: 7px 16px !important;
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    font-size: 0.86rem !important;
    border: none !important;
    background: transparent !important;
    transition: all var(--apple-duration) var(--apple-ease) !important;
}}

.stTabs [data-baseweb="tab"]:hover {{
    color: var(--text-primary) !important;
    background: rgba(255, 255, 255, 0.05) !important;
}}

.stTabs [aria-selected="true"] {{
    background: rgba(255, 255, 255, 0.12) !important;
    backdrop-filter: blur(14px) !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    border: 1px solid rgba(255, 255, 255, 0.18) !important;
    border-top: 1px solid rgba(255, 255, 255, 0.38) !important;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.25), 0 4px 10px rgba(0, 0, 0, 0.18) !important;
}}

/* Inputs & Selectboxes */
[data-baseweb="select"] > div {{
    background: rgba(255, 255, 255, 0.04) !important;
    backdrop-filter: blur(16px) !important;
    border: 1px solid var(--glass-border) !important;
    border-top: 1px solid rgba(255, 255, 255, 0.22) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
}}

[data-baseweb="select"] > div:hover {{
    border-color: rgba(255, 255, 255, 0.25) !important;
}}

/* Sliders */
[data-testid="stSlider"] [role="slider"] {{
    background-color: #ffffff !important;
    border: 2px solid var(--system-blue) !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.35) !important;
}}

/* Buttons */
.stButton > button, 
[data-testid="stDownloadButton"] > button {{
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.12) 0%, rgba(255, 255, 255, 0.04) 100%) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border: 1px solid var(--glass-border) !important;
    border-top: 1px solid rgba(255, 255, 255, 0.38) !important;
    border-radius: 9999px !important;
    color: var(--text-primary) !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    padding: 9px 22px !important;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.30), 0 6px 16px rgba(0, 0, 0, 0.22) !important;
    transition: all var(--apple-duration) var(--apple-ease) !important;
}}

.stButton > button:hover, 
[data-testid="stDownloadButton"] > button:hover {{
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.18) 0%, rgba(255, 255, 255, 0.07) 100%) !important;
    border-top-color: rgba(255, 255, 255, 0.60) !important;
    transform: translateY(-1px) !important;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.45), 0 8px 22px rgba(0, 0, 0, 0.28) !important;
}}

/* DataFrames */
[data-testid="stDataFrame"] {{
    background: var(--glass-secondary) !important;
    border: 1px solid var(--glass-border) !important;
    border-top: 1px solid rgba(255, 255, 255, 0.20) !important;
    border-radius: 16px !important;
    overflow: hidden !important;
}}

/* Reduced Motion Accessibility */
@media (prefers-reduced-motion: reduce) {{
    * {{
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }}
}}
</style>
"""

# -----------------------------------------------------------------------------
# 3. REFINED PLOTLY LAYOUT (MACOS TAHOE GRAPHITE PALETTE)
# -----------------------------------------------------------------------------
def get_apple_plotly_layout() -> dict:
    """
    Returns an Apple dark-tint Plotly chart layout specification.
    Neutral transparent background, refined subtle gridlines, restrained typography.
    """
    return dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family='-apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", sans-serif',
            color='rgba(235, 235, 245, 0.85)',
            size=12
        ),
        margin=dict(l=35, r=35, t=45, b=35),
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.05)',
            zerolinecolor='rgba(255, 255, 255, 0.10)',
            showline=False,
            tickfont=dict(color='rgba(235, 235, 245, 0.55)')
        ),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.05)',
            zerolinecolor='rgba(255, 255, 255, 0.10)',
            showline=False,
            tickfont=dict(color='rgba(235, 235, 245, 0.55)')
        ),
        legend=dict(
            bgcolor='rgba(28, 27, 32, 0.65)',
            bordercolor='rgba(255, 255, 255, 0.10)',
            borderwidth=1,
            font=dict(color='rgba(235, 235, 245, 0.80)')
        ),
        hoverlabel=dict(
            bgcolor='rgba(28, 27, 32, 0.94)',
            bordercolor='rgba(255, 255, 255, 0.18)',
            font=dict(
                family='-apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif',
                size=12,
                color='#F5F5F7'
            )
        )
    )
