"""
Apple Liquid Glass Design System
A design system inspired by Apple visionOS & macOS Liquid Glass materials.
Features:
- SVG displacement & chromatic aberration filters
- Multi-tier glass materials (Primary, Floating, Subtle, Highlight)
- Dual-bevel specular rim lighting & multi-layer ambient occlusion shadows
- SF Pro typography hierarchy & Apple system color tokens
"""

def get_liquid_glass_svg_filters() -> str:
    """
    Renders SVG filters for true optical liquid glass refraction,
    specular highlight simulation, and subtle chromatic dispersion.
    """
    return """
    <svg style="position: absolute; width: 0; height: 0; pointer-events: none;" aria-hidden="true">
      <defs>
        <!-- Liquid Glass Refraction & Bevel Filter -->
        <filter id="apple-liquid-glass" x="-20%" y="-20%" width="140%" height="140%" color-interpolation-filters="sRGB">
          <feTurbulence type="fractalNoise" baseFrequency="0.012 0.012" numOctaves="2" result="noise" />
          <feDisplacementMap in="SourceGraphic" in2="noise" scale="5" xChannelSelector="R" yChannelSelector="G" result="displaced" />
          <feGaussianBlur in="displaced" stdDeviation="0.4" result="smoothRefraction" />
          <feBlend mode="normal" in="SourceGraphic" in2="smoothRefraction" />
        </filter>
        
        <!-- Specular Edge Illumination Filter -->
        <filter id="apple-specular-edge" x="-10%" y="-10%" width="120%" height="120%" color-interpolation-filters="sRGB">
          <feGaussianBlur in="SourceAlpha" stdDeviation="1.5" result="blur" />
          <feSpecularLighting in="blur" surfaceScale="2" specularConstant="1.2" specularExponent="24" lighting-color="#ffffff" result="specOut">
            <fePointLight x="-100" y="-100" z="200" />
          </feSpecularLighting>
          <feComposite in="specOut" in2="SourceAlpha" operator="in" result="specularEdge" />
          <feComposite in="SourceGraphic" in2="specularEdge" operator="over" />
        </filter>
      </defs>
    </svg>
    """

def get_liquid_glass_css() -> str:
    """
    Returns production CSS implementing Apple's multi-layered Liquid Glass material hierarchy.
    """
    return """
<style>
/* -------------------------------------------------------------------------
   1. APPLE LIQUID GLASS DESIGN TOKENS
   ------------------------------------------------------------------------- */
:root {
    /* Color Palette: Deep Midnight & Apple Accents */
    --apple-bg: #030712;
    --apple-midnight: #070d1a;
    --apple-slate: #0f172a;
    
    /* Accents (Muted, Sophisticated Apple Tone) */
    --apple-blue: #0a84ff;
    --apple-cyan: #64d2ff;
    --apple-indigo: #5e5ce6;
    --apple-purple: #bf5af2;
    --apple-pink: #ff375f;
    --apple-green: #30d158;
    --apple-orange: #ff9f0a;
    --apple-yellow: #ffd60a;
    
    /* Text Hierarchy */
    --text-primary: #ffffff;
    --text-secondary: rgba(255, 255, 255, 0.72);
    --text-tertiary: rgba(255, 255, 255, 0.48);
    --text-quaternary: rgba(255, 255, 255, 0.28);
    
    /* Material Tier 1: Primary Glass (Content Panels) */
    --primary-glass-bg: rgba(255, 255, 255, 0.045);
    --primary-glass-border-top: rgba(255, 255, 255, 0.38);
    --primary-glass-border-left: rgba(255, 255, 255, 0.22);
    --primary-glass-border-bottom: rgba(255, 255, 255, 0.08);
    --primary-glass-border-right: rgba(255, 255, 255, 0.12);
    --primary-glass-blur: blur(36px) saturate(190%);
    
    /* Material Tier 2: Floating Glass (Sidebar, Floating Modals, Docks) */
    --floating-glass-bg: rgba(18, 24, 38, 0.72);
    --floating-glass-border: rgba(255, 255, 255, 0.16);
    --floating-glass-border-top: rgba(255, 255, 255, 0.45);
    --floating-glass-blur: blur(45px) saturate(200%);
    --floating-glass-shadow: 0 28px 60px -12px rgba(0, 0, 0, 0.65), 0 12px 24px -8px rgba(0, 0, 0, 0.45);
    
    /* Material Tier 3: Subtle Glass (Inner Cards & Secondary Elements) */
    --subtle-glass-bg: rgba(255, 255, 255, 0.03);
    --subtle-glass-border: rgba(255, 255, 255, 0.09);
    --subtle-glass-border-top: rgba(255, 255, 255, 0.22);
    --subtle-glass-blur: blur(20px);
    
    /* Material Tier 4: Highlight Glass (Active Controls, Key Indicators) */
    --highlight-glass-bg: linear-gradient(135deg, rgba(10, 132, 255, 0.22) 0%, rgba(94, 92, 230, 0.12) 100%);
    --highlight-glass-border: rgba(100, 210, 255, 0.45);
    
    /* Bevel Inset Specular Lighting */
    --bevel-shadow: inset 0 1px 1px 0 rgba(255, 255, 255, 0.45), 
                    inset 0 -1px 1px 0 rgba(0, 0, 0, 0.35);
                    
    /* Smooth Apple Animation Curves */
    --apple-ease: cubic-bezier(0.16, 1, 0.3, 1);
    --apple-duration: 280ms;
}

/* -------------------------------------------------------------------------
   2. GLOBAL ATMOSPHERE & BACKGROUND
   ------------------------------------------------------------------------- */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--apple-bg) !important;
    background-image: 
        radial-gradient(circle at 15% 15%, rgba(10, 132, 255, 0.08) 0%, transparent 42%),
        radial-gradient(circle at 85% 25%, rgba(191, 90, 242, 0.06) 0%, transparent 48%),
        radial-gradient(circle at 50% 85%, rgba(48, 209, 88, 0.05) 0%, transparent 52%),
        linear-gradient(180deg, #040814 0%, #02040a 100%) !important;
    background-attachment: fixed !important;
    color: var(--text-primary) !important;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Helvetica Neue", sans-serif !important;
    -webkit-font-smoothing: antialiased !important;
    -moz-osx-font-smoothing: grayscale !important;
}

/* Hide default streamlit header clutter */
header[data-testid="stHeader"] {
    background: transparent !important;
}
#MainMenu, footer {
    visibility: hidden;
}

/* Container constraints for clean desktop presentation */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 3.5rem !important;
    max-width: 1360px !important;
}

/* -------------------------------------------------------------------------
   3. APPLE LIQUID GLASS MATERIAL TIERS
   ------------------------------------------------------------------------- */

/* TIER 1: PRIMARY GLASS PANELS */
.glass-panel {
    background: var(--primary-glass-bg);
    backdrop-filter: var(--primary-glass-blur);
    -webkit-backdrop-filter: var(--primary-glass-blur);
    border-radius: 28px;
    border: 1px solid var(--primary-glass-border-bottom);
    border-top: 1.5px solid var(--primary-glass-border-top);
    border-left: 1.5px solid var(--primary-glass-border-left);
    box-shadow: 
        var(--bevel-shadow),
        0 20px 48px -12px rgba(0, 0, 0, 0.55),
        0 8px 16px -6px rgba(0, 0, 0, 0.35);
    padding: 32px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
    transition: transform var(--apple-duration) var(--apple-ease), 
                box-shadow var(--apple-duration) var(--apple-ease),
                border-color var(--apple-duration) var(--apple-ease);
}

.glass-panel:hover {
    box-shadow: 
        var(--bevel-shadow),
        0 28px 64px -14px rgba(0, 0, 0, 0.65),
        0 12px 28px -6px rgba(10, 132, 255, 0.12);
    border-top-color: rgba(255, 255, 255, 0.6);
}

/* Subtle Specular Sheen across the top edge */
.glass-panel::before {
    content: '';
    position: absolute;
    top: 0;
    left: 20px;
    right: 20px;
    height: 1px;
    background: linear-gradient(90deg, 
        transparent 0%, 
        rgba(255, 255, 255, 0.65) 25%, 
        rgba(255, 255, 255, 0.8) 50%, 
        rgba(255, 255, 255, 0.65) 75%, 
        transparent 100%
    );
    pointer-events: none;
}

/* TIER 2: FLOATING GLASS (SIDEBAR & FLOATING DOCKS) */
section[data-testid="stSidebar"] {
    background: var(--floating-glass-bg) !important;
    backdrop-filter: var(--floating-glass-blur) !important;
    -webkit-backdrop-filter: var(--floating-glass-blur) !important;
    border-right: 1px solid var(--floating-glass-border) !important;
    box-shadow: var(--floating-glass-shadow) !important;
}

section[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem !important;
    padding-left: 1.25rem !important;
    padding-right: 1.25rem !important;
}

/* TIER 3: SUBTLE GLASS (INNER CARDS & WIDGETS) */
.glass-card {
    background: var(--subtle-glass-bg);
    backdrop-filter: var(--subtle-glass-blur);
    -webkit-backdrop-filter: var(--subtle-glass-blur);
    border-radius: 20px;
    border: 1px solid var(--subtle-glass-border);
    border-top: 1.2px solid var(--subtle-glass-border-top);
    box-shadow: inset 0 1px 1px 0 rgba(255, 255, 255, 0.25), 0 8px 20px rgba(0, 0, 0, 0.25);
    padding: 22px 24px;
    transition: all var(--apple-duration) var(--apple-ease);
}

.glass-card:hover {
    background: rgba(255, 255, 255, 0.05);
    border-top-color: rgba(255, 255, 255, 0.4);
    transform: translateY(-2px);
    box-shadow: inset 0 1px 1px 0 rgba(255, 255, 255, 0.35), 0 14px 28px rgba(0, 0, 0, 0.35);
}

/* TIER 4: HIGHLIGHT GLASS PILLS */
.glass-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(16px);
    border-radius: 9999px;
    padding: 6px 14px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-top: 1px solid rgba(255, 255, 255, 0.45);
    font-size: 0.8rem;
    font-weight: 500;
    color: var(--text-primary);
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.3), 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* -------------------------------------------------------------------------
   4. MACOS WINDOW CONTROLS & APPLE NAVIGATION
   ------------------------------------------------------------------------- */
.macos-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 16px;
    margin-bottom: 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.macos-traffic-lights {
    display: flex;
    align-items: center;
    gap: 8px;
}

.traffic-light {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    display: inline-block;
    box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.5), 0 1px 2px rgba(0, 0, 0, 0.3);
}

.light-red { background: #ff5f56; }
.light-yellow { background: #ffbd2e; }
.light-green { background: #27c93f; }

/* Apple-style Radio Nav Buttons in Sidebar */
[data-testid="stRadio"] > div {
    gap: 6px !important;
}

[data-testid="stRadio"] label {
    background: transparent !important;
    border: 1px solid transparent !important;
    border-radius: 14px !important;
    padding: 10px 14px !important;
    color: var(--text-secondary) !important;
    font-size: 0.92rem !important;
    font-weight: 500 !important;
    transition: all var(--apple-duration) var(--apple-ease) !important;
    cursor: pointer !important;
}

[data-testid="stRadio"] label:hover {
    background: rgba(255, 255, 255, 0.05) !important;
    color: var(--text-primary) !important;
    border-color: rgba(255, 255, 255, 0.1) !important;
}

/* Active Nav State */
[data-testid="stRadio"] label[data-checked="true"],
[data-testid="stRadio"] [aria-checked="true"] {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.12) 0%, rgba(255, 255, 255, 0.05) 100%) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255, 255, 255, 0.22) !important;
    border-top: 1px solid rgba(255, 255, 255, 0.5) !important;
    color: #ffffff !important;
    box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.35), 0 8px 16px rgba(0, 0, 0, 0.25) !important;
    font-weight: 600 !important;
}

/* -------------------------------------------------------------------------
   5. KPI METRIC CARDS (APPLE LIQUID GLASS STYLE)
   ------------------------------------------------------------------------- */
.apple-metric-card {
    background: var(--subtle-glass-bg);
    backdrop-filter: var(--subtle-glass-blur);
    -webkit-backdrop-filter: var(--subtle-glass-blur);
    border-radius: 22px;
    border: 1px solid var(--subtle-glass-border);
    border-top: 1.5px solid var(--subtle-glass-border-top);
    padding: 22px 20px;
    box-shadow: var(--bevel-shadow), 0 10px 24px rgba(0, 0, 0, 0.3);
    position: relative;
    overflow: hidden;
    transition: all var(--apple-duration) var(--apple-ease);
}

.apple-metric-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--bevel-shadow), 0 16px 36px rgba(0, 0, 0, 0.45);
    border-top-color: rgba(255, 255, 255, 0.55);
}

.metric-accent-line {
    position: absolute;
    top: 0;
    left: 20px;
    right: 20px;
    height: 2px;
    border-radius: 2px;
}

.metric-title {
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: var(--text-tertiary);
    margin-bottom: 6px;
}

.metric-value {
    font-size: 2.1rem;
    font-weight: 700;
    letter-spacing: -0.5px;
    color: #ffffff;
    line-height: 1.1;
    margin-bottom: 6px;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif;
}

.metric-subtitle {
    font-size: 0.8rem;
    color: var(--text-secondary);
    display: flex;
    align-items: center;
    gap: 6px;
}

/* -------------------------------------------------------------------------
   6. STREAMLIT WIDGETS ELEVATION (APPLE GLASS THEMING)
   ------------------------------------------------------------------------- */

/* Apple-style Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255, 255, 255, 0.04) !important;
    backdrop-filter: blur(24px) !important;
    padding: 6px !important;
    border-radius: 16px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-top: 1px solid rgba(255, 255, 255, 0.25) !important;
    gap: 6px !important;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 12px !important;
    padding: 8px 18px !important;
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    border: none !important;
    background: transparent !important;
    transition: all var(--apple-duration) var(--apple-ease) !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: #ffffff !important;
    background: rgba(255, 255, 255, 0.06) !important;
}

.stTabs [aria-selected="true"] {
    background: rgba(255, 255, 255, 0.14) !important;
    backdrop-filter: blur(16px) !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    border: 1px solid rgba(255, 255, 255, 0.22) !important;
    border-top: 1px solid rgba(255, 255, 255, 0.5) !important;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.35), 0 4px 12px rgba(0, 0, 0, 0.2) !important;
}

/* Sliders */
[data-testid="stSlider"] {
    padding-top: 8px !important;
}

[data-testid="stSlider"] [role="slider"] {
    background-color: #ffffff !important;
    border: 2px solid var(--apple-blue) !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4) !important;
}

/* Selectbox & Inputs */
[data-baseweb="select"] > div {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-top: 1px solid rgba(255, 255, 255, 0.25) !important;
    border-radius: 14px !important;
    color: #ffffff !important;
}

[data-baseweb="select"] > div:hover {
    border-color: rgba(255, 255, 255, 0.3) !important;
}

/* Buttons (Apple Glass Capsules) */
.stButton > button, 
[data-testid="stDownloadButton"] > button {
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.14) 0%, rgba(255, 255, 255, 0.05) 100%) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255, 255, 255, 0.16) !important;
    border-top: 1.5px solid rgba(255, 255, 255, 0.5) !important;
    border-radius: 9999px !important;
    color: #ffffff !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    padding: 10px 24px !important;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.4), 0 8px 20px rgba(0, 0, 0, 0.25) !important;
    transition: all var(--apple-duration) var(--apple-ease) !important;
}

.stButton > button:hover, 
[data-testid="stDownloadButton"] > button:hover {
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.22) 0%, rgba(255, 255, 255, 0.08) 100%) !important;
    border-top-color: rgba(255, 255, 255, 0.75) !important;
    transform: translateY(-2px) !important;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.6), 0 12px 28px rgba(10, 132, 255, 0.25) !important;
}

/* Dataframe Styling */
[data-testid="stDataFrame"] {
    background: rgba(255, 255, 255, 0.02) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-top: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 20px !important;
    overflow: hidden !important;
}

/* Reduced Motion Support */
@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
</style>
"""

def get_apple_plotly_layout() -> dict:
    """
    Returns an Apple-inspired Plotly chart layout specification.
    Clean, transparent, minimal gridlines, elegant typography.
    """
    return dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family='-apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif',
            color='rgba(255, 255, 255, 0.85)',
            size=12
        ),
        margin=dict(l=35, r=35, t=50, b=35),
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.06)',
            zerolinecolor='rgba(255, 255, 255, 0.12)',
            showline=False,
            tickfont=dict(color='rgba(255, 255, 255, 0.6)')
        ),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.06)',
            zerolinecolor='rgba(255, 255, 255, 0.12)',
            showline=False,
            tickfont=dict(color='rgba(255, 255, 255, 0.6)')
        ),
        legend=dict(
            bgcolor='rgba(15, 23, 42, 0.6)',
            bordercolor='rgba(255, 255, 255, 0.12)',
            borderwidth=1,
            font=dict(color='rgba(255, 255, 255, 0.8)')
        ),
        hoverlabel=dict(
            bgcolor='rgba(18, 24, 38, 0.92)',
            bordercolor='rgba(255, 255, 255, 0.25)',
            font=dict(
                family='-apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif',
                size=12,
                color='#ffffff'
            )
        )
    )
