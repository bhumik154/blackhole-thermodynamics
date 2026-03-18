"""
app.py — Black Hole Thermodynamics Interactive Visualizer (Streamlit)
Author: Bhumik Khatwani
"""

import math
import datetime
import numpy as np
import plotly.graph_objects as go
import streamlit as st
from physics import get_all_properties, scaling_curves, M_sun

# ── Page config ──
st.set_page_config(page_title="Black Hole Thermodynamics", page_icon="⚫", layout="wide")

# ── Theme / CSS ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap');
html, body, [class*="css"], .stApp { background-color: #0c0c14 !important; color: #e2e8f0; font-family: 'DM Sans', -apple-system, sans-serif; }
h1, h2, h3 { font-family: 'DM Sans', sans-serif !important; color: #e2e8f0 !important; }
.stTabs [data-baseweb="tab-list"] { gap: 4px; background: rgba(255,255,255,0.03); border-radius: 8px; padding: 4px; border: 1px solid rgba(255,255,255,0.06); }
.stTabs [data-baseweb="tab"] { background: transparent; border-radius: 6px; color: rgba(255,255,255,0.4); font-family: 'DM Sans', sans-serif; font-size: 0.85rem; }
.stTabs [aria-selected="true"] { background: rgba(129,140,248,0.15) !important; color: #a5b4fc !important; }
.stSelectbox > div > div { background: rgba(255,255,255,0.06) !important; border: 1px solid rgba(255,255,255,0.1) !important; color: #e2e8f0 !important; }
.stNumberInput > div > div > input { background: rgba(255,255,255,0.06) !important; border: 1px solid rgba(255,255,255,0.1) !important; color: #e2e8f0 !important; font-family: 'JetBrains Mono', monospace !important; }
div[data-testid="stMetric"] { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 14px 16px; }
div[data-testid="stMetric"] label { font-size: 0.65rem !important; letter-spacing: 0.1em; text-transform: uppercase; color: rgba(255,255,255,0.35) !important; }
div[data-testid="stMetric"] [data-testid="stMetricValue"] { font-family: 'DM Sans', sans-serif !important; font-size: 1.2rem !important; font-weight: 700 !important; }
.metric-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 14px 16px; margin-bottom: 8px; transition: border-color 0.2s; }
.metric-card:hover { border-color: rgba(129,140,248,0.4); }
.metric-label { font-size: 0.65rem; letter-spacing: 0.1em; text-transform: uppercase; color: rgba(255,255,255,0.35); margin-bottom: 6px; }
.metric-value { font-family: 'DM Sans', sans-serif; font-size: 1.2rem; font-weight: 700; line-height: 1.1; }
.metric-unit { font-size: 0.7rem; color: rgba(255,255,255,0.3); margin-top: 4px; }
.section-label { font-size: 0.65rem; letter-spacing: 0.1em; text-transform: uppercase; color: rgba(255,255,255,0.35); margin: 1.5rem 0 0.75rem; }
.regime-badge { display: inline-flex; align-items: center; gap: 8px; border-radius: 8px; padding: 6px 14px; margin-bottom: 14px; }
.fact-row { display: flex; gap: 10px; align-items: flex-start; margin-bottom: 10px; }
.fact-icon { font-size: 16px; flex-shrink: 0; margin-top: 2px; }
.fact-text { font-size: 0.78rem; color: rgba(255,255,255,0.55); line-height: 1.65; }
.compare-table { width: 100%; border-collapse: collapse; }
.compare-table td { padding: 9px 12px; border-bottom: 1px solid rgba(255,255,255,0.04); }
.compare-left { text-align: right; font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; }
.compare-center { text-align: center; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.06em; color: rgba(255,255,255,0.35); }
.compare-right { text-align: left; font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; }
.compare-winner { font-weight: 600; }
.feed-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(145px, 1fr)); gap: 8px; }
.feed-btn { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 8px; padding: 10px 12px; cursor: pointer; text-align: left; transition: all 0.15s; }
.feed-btn:hover { border-color: #818cf8; background: rgba(129,140,248,0.06); }
.feed-icon { font-size: 18px; margin-bottom: 4px; }
.feed-name { font-size: 0.78rem; color: #e2e8f0; font-weight: 500; }
.feed-mass { font-size: 0.65rem; color: rgba(255,255,255,0.25); font-family: 'JetBrains Mono', monospace; margin-top: 2px; }
.quip-box { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 8px; padding: 12px 16px; margin-top: 12px; }
.quip-text { font-size: 0.78rem; color: rgba(255,255,255,0.45); font-style: italic; line-height: 1.5; }
.log-item { display: flex; gap: 10px; align-items: flex-start; padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.04); }
.log-name { font-size: 0.78rem; color: #e2e8f0; font-weight: 500; }
.log-kg { font-size: 0.65rem; color: rgba(255,255,255,0.2); font-family: 'JetBrains Mono', monospace; }
.log-quip { font-size: 0.72rem; color: rgba(255,255,255,0.35); margin-top: 3px; line-height: 1.5; }
.growth-label { font-size: 0.65rem; color: rgba(255,255,255,0.3); text-transform: uppercase; letter-spacing: 0.06em; }
.growth-val { font-size: 0.82rem; font-family: 'JetBrains Mono', monospace; font-weight: 600; }
#MainMenu, footer, header { visibility: hidden; }
div[data-testid="stToolbar"] { display: none; }
.stButton > button { font-family: 'DM Sans', sans-serif !important; }
</style>
""", unsafe_allow_html=True)

# ── Plotly theme ──
PLOTLY_LAYOUT = dict(
    paper_bgcolor="#0c0c14",
    plot_bgcolor="#0e0e18",
    font=dict(family="DM Sans, sans-serif", color="rgba(255,255,255,0.4)", size=11),
    margin=dict(l=50, r=20, t=36, b=40),
    xaxis=dict(gridcolor="rgba(255,255,255,0.04)", zerolinecolor="rgba(255,255,255,0.06)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.04)", zerolinecolor="rgba(255,255,255,0.06)"),
)

# ── Constants ──
PRESETS = {
    "Custom": None,
    "Primordial Micro (1e-18 M☉)": 1e-18,
    "Stellar (10 M☉)": 10,
    "Cygnus X-1 (21 M☉)": 21,
    "GW150914 (62 M☉)": 62,
    "Sagittarius A* (4M M☉)": 4e6,
    "M87* (6.5B M☉)": 6.5e9,
}

THROWABLES = [
    {"name": "You", "icon": "🧍", "kg": 70, "quip": "Gone. Didn't even make a ripple."},
    {"name": "A car", "icon": "🚗", "kg": 1500, "quip": "Not even a rounding error."},
    {"name": "Blue whale", "icon": "🐋", "kg": 150000, "quip": "The largest animal that ever lived. The black hole didn't notice."},
    {"name": "Titanic", "icon": "🚢", "kg": 5.23e7, "quip": "Sank once in the Atlantic. Sank again into a singularity. At least this time was quick."},
    {"name": "Great Pyramid", "icon": "🔺", "kg": 6e9, "quip": "4,500 years of human labor. Consumed in less time than a thought."},
    {"name": "Mt. Everest", "icon": "🏔️", "kg": 8.1e14, "quip": "The tallest thing on Earth. In here, it's nothing."},
    {"name": "The Moon", "icon": "🌙", "kg": 7.342e22, "quip": "No more tides. No more eclipses. Just gone."},
    {"name": "Earth", "icon": "🌍", "kg": 5.972e24, "quip": "8 billion people. Every song, every memory, every sunrise. Swallowed whole."},
    {"name": "Jupiter", "icon": "🪐", "kg": 1.898e27, "quip": "1,300 Earths could fit inside Jupiter. And Jupiter just fit inside this."},
    {"name": "The Sun", "icon": "☀️", "kg": 1.989e30, "quip": "The thing everything in our solar system orbits. Fed to something that doesn't care."},
    {"name": "Another 10 M☉ BH", "icon": "🕳️", "kg": 1.989e31, "quip": "Two black holes walk into each other. One walks out. That's the whole joke."},
    {"name": "Sagittarius A*", "icon": "⚫", "kg": 7.956e36, "quip": "You just fed the center of our galaxy to this thing. What are you doing."},
]

SIZE_REFS = [
    ("Proton", 1.7e-18), ("Virus", 1e-7), ("Everest", 8.849e-3),
    ("Moon", 1737), ("Earth", 6371), ("Jupiter", 71492),
    ("Sun", 696000), ("Solar Sys.", 4.5e9),
]


# ── Formatters ──
def fmt_time(yr):
    if yr < 1/365.25:   return f"{yr*365.25*24:.2f} hrs"
    elif yr < 1:         return f"{yr*365.25:.2f} days"
    elif yr < 1e3:       return f"{yr:.2f} yr"
    elif yr < 1e6:       return f"{yr/1e3:.2f} kyr"
    elif yr < 1e9:       return f"{yr/1e6:.2f} Myr"
    elif yr < 1e12:      return f"{yr/1e9:.2f} Gyr"
    else:                return f"{yr:.2e} yr"

def fmt_sci(v, d=3):
    if v == 0: return "0"
    if 0.01 <= abs(v) < 1e6:
        return f"{v:.{d-1}g}"
    return f"{v:.{d-1}e}"

def fmt_big(v):
    a = abs(v)
    if a == 0: return "0"
    if a < 1e-3: return f"{v:.1e}"
    if a < 1:    return f"{v:.2f}"
    if a < 1e3:  return f"{v:.1f}"
    names = [
        (1e6, "thousand"), (1e9, "million"), (1e12, "billion"),
        (1e15, "trillion"), (1e18, "quadrillion"), (1e21, "quintillion"),
        (1e24, "sextillion"), (1e27, "septillion"), (1e30, "octillion"),
        (1e33, "nonillion"), (1e36, "decillion"),
    ]
    for threshold, name in names:
        if a < threshold:
            val = v / (threshold / 1e3)
            s = f"{val:.2f}".rstrip('0').rstrip('.')
            return f"{s} {name}"
    if a < 1e100:
        exp = int(math.floor(math.log10(a)))
        coeff = v / 10**exp
        return f"{coeff:.1f} × 10^{exp}"
    return f"{v:.1e}"


# ── Regime ──
def get_regime(m):
    if m < 1e-10: return ("Primordial / Micro", "#f472b6", "micro")
    if m < 3:     return ("Sub-Stellar / Exotic", "#fb923c", "sub")
    if m < 100:   return ("Stellar-Mass", "#38bdf8", "stellar")
    if m < 1e7:   return ("Intermediate (IMBH)", "#a78bfa", "imbh")
    return ("Supermassive (SMBH)", "#facc15", "smbh")

def get_size_context(km):
    if km < 1737:     return "smaller than the Moon"
    if km < 6371:     return "between the Moon and Earth"
    if km < 696000:   return "between Earth and the Sun"
    if km < 4.5e9:    return "larger than the Sun"
    return "larger than the Solar System"


# ── Fun Facts ──
def get_fun_facts(p, m_solar):
    facts = []
    rs_km, temp_K, evap_yr = p["rs_km"], p["temp_K"], p["evap_yr"]
    lum_W, mass_kg, surf_grav, rs_m = p["lum_W"], p["mass_kg"], p["surf_grav"], p["rs_m"]
    _, _, tag = get_regime(m_solar)

    earths_inside = (rs_km ** 3) / (6371 ** 3)
    if earths_inside >= 1:
        facts.append(("🌍", f"You could park {fmt_big(earths_inside)} Earths inside this thing. Just... gone. Swallowed whole."))
    elif rs_km < 6371:
        pct = rs_km / 6371 * 100
        if pct < 0.001:
            facts.append(("🔬", f"This event horizon is {pct:.1e}% of Earth's radius. You couldn't see it if you were standing next to it."))
        else:
            facts.append(("🔬", f"The event horizon is {pct:.2f}% of Earth's radius. Tiny. But it'll still ruin your day."))

    CMB = 2.725
    if temp_K < CMB:
        facts.append(("🧊", "Colder than empty space itself. The cosmic background radiation is 2.725 K and this thing can't even match that. It just sits there, soaking up photons, giving nothing back."))
    elif temp_K > 5778:
        facts.append(("🔥", f"{fmt_big(temp_K / 5778)}× hotter than the surface of the Sun. This black hole is screaming energy into the void and nobody's around to measure it."))
    elif temp_K > CMB and temp_K < 300:
        facts.append(("❄️", f"Hawking temperature of {fmt_big(temp_K)} Kelvin. Warmer than deep space, colder than your freezer. A weird in-between that nobody will ever feel."))

    universe_age = 1.38e10
    age_ratio = evap_yr / universe_age
    if age_ratio > 1e50:
        facts.append(("♾️", f"This takes {fmt_big(age_ratio)}× the age of the universe to evaporate. The stars will burn out. The galaxies will scatter. And this thing will still be here, barely getting started."))
    elif age_ratio > 1:
        facts.append(("⏳", f"{fmt_big(age_ratio)}× the age of the universe to evaporate. Everything you've ever known will be long gone and this black hole won't even notice."))
    elif evap_yr < 1:
        facts.append(("💥", f"Gone in {fmt_time(evap_yr)}. No slow fade. Just a flash of radiation and then nothing. Like it was never there."))

    g_ratio = surf_grav / 9.81
    facts.append(("⚡", f"Surface gravity: {fmt_big(g_ratio)}× what you feel standing on Earth right now. At this pull, your atoms wouldn't hold together. You'd be stretched into a string of particles before you got close."))

    sun_lum = 3.828e26
    if lum_W > sun_lum:
        facts.append(("☀️", f"Radiating {fmt_big(lum_W / sun_lum)}× more energy than the Sun. A black hole outshining a star. Let that sit for a second."))
    elif lum_W < 1e-30:
        facts.append(("🕳️", "The glow from this thing is so faint that every instrument humanity has ever built would miss it. Hawking radiation is real. We just can't prove it yet. Not at this scale."))

    regime_facts = {
        "micro": ("🌌", "These might have blinked into existence in the first second after the Big Bang. Tiny knots of density in a universe that was still figuring itself out. Most of them are probably gone by now."),
        "smbh": ("🌀", "This is the kind that sits at the center of a galaxy and runs the show. The brightest things in the universe, quasars, are just matter falling into one of these. The light we see is the scream on the way down."),
        "stellar": ("💫", "A massive star burned through its fuel, its core gave up, and what was left collapsed into this. The outer layers blew off as a supernova. The core just... kept falling."),
        "imbh": ("🔭", "Too heavy to come from a single star. Too light to be the monster at a galaxy's center. These are the ones we can barely find. The universe's middle children."),
    }
    if tag in regime_facts:
        facts.append(regime_facts[tag])

    vol = (4 / 3) * math.pi * rs_m**3
    density = mass_kg / vol if vol > 0 else float('inf')
    if density < 1000:
        facts.append(("🌊", f"Average density inside the horizon: {fmt_big(density)} kg/m³. That's less dense than water. You could technically float in it. You wouldn't survive, but you could float."))
    elif density > 1e17:
        facts.append(("⚛️", f"Density of {fmt_big(density)} kg/m³. That's nuclear territory. Imagine crushing a mountain down to the size of a sugar cube. Now do that to everything."))

    return facts[:5]


# ── HTML helpers ──
def metric_card(label, value, unit="", accent="#818cf8"):
    unit_html = f'<div class="metric-unit">{unit}</div>' if unit else ''
    st.markdown(f'<div class="metric-card" style="border-color:rgba(255,255,255,0.06);"><div class="metric-label">{label}</div><div class="metric-value" style="color:{accent};">{value}</div>{unit_html}</div>', unsafe_allow_html=True)

def regime_badge(m_solar):
    name, color, _ = get_regime(m_solar)
    st.markdown(f"""<div class="regime-badge" style="background:{color}12;border:1px solid {color}30;">
        <div style="width:7px;height:7px;border-radius:50%;background:{color};"></div>
        <span style="font-size:0.78rem;color:{color};font-weight:500;">{name}</span>
        <span style="font-size:0.72rem;color:rgba(255,255,255,0.3);">· {fmt_sci(m_solar)} M☉</span>
    </div>""", unsafe_allow_html=True)

def show_facts(facts, limit=5):
    html = ""
    for icon, text in facts[:limit]:
        html += f'<div class="fact-row"><span class="fact-icon">{icon}</span><span class="fact-text">{text}</span></div>'
    st.markdown(html, unsafe_allow_html=True)


# ── Charts ──
def make_scaling_chart(m_solar, field, label, unit, color):
    curves = scaling_curves(m_solar)
    p = get_all_properties(m_solar)
    x = curves["masses_solar"]
    y = curves[field]
    current_y = p[field] if field != "evap_yr" else p["evap_yr"]
    if field == "rs_km": current_y = p["rs_km"]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(color=color, width=2.5),
                             hovertemplate=f"Mass: %{{x:.2e}} M☉<br>{label}: %{{y:.2e}} {unit}<extra></extra>"))
    fig.add_trace(go.Scatter(x=[m_solar], y=[current_y], mode="markers",
                             marker=dict(color=color, size=9, line=dict(color="white", width=1.5)),
                             hovertemplate=f"{fmt_sci(m_solar)} M☉<br>{fmt_sci(current_y)} {unit}<extra></extra>"))
    fig.update_xaxes(type="log", title=dict(text="Mass (M☉)", font=dict(size=10)))
    fig.update_yaxes(type="log", title=dict(text=f"{label} ({unit})", font=dict(size=10)))
    fig.update_layout(**PLOTLY_LAYOUT, title=dict(text=label, font=dict(size=12, color="rgba(255,255,255,0.5)")),
                      showlegend=False, height=260)
    return fig

def make_size_chart(m_solar, rs_km):
    names = [n for n, _ in SIZE_REFS] + [f"BH ({fmt_sci(m_solar, 2)} M☉)"]
    vals = [v for _, v in SIZE_REFS] + [rs_km]
    colors = ["rgba(255,255,255,0.08)"] * len(SIZE_REFS) + ["#818cf8"]

    fig = go.Figure()
    fig.add_trace(go.Bar(y=names, x=vals, orientation="h", marker=dict(color=colors, line=dict(width=0)),
                         text=[f"{v:.1e} km" if (v < 0.01 or v >= 1e6) else f"{v:,.0f} km" for v in vals],
                         textposition="outside", textfont=dict(size=9, color="rgba(255,255,255,0.35)", family="JetBrains Mono, monospace"),
                         hovertemplate="%{y}: %{x:.2e} km<extra></extra>"))
    fig.update_xaxes(type="log", range=[-20, 11])
    layout_copy = {**PLOTLY_LAYOUT}
    layout_copy["yaxis"] = dict(gridcolor="rgba(0,0,0,0)", zerolinecolor="rgba(255,255,255,0.06)")
    fig.update_layout(**layout_copy, height=max(250, len(names) * 32), showlegend=False,
                      title=dict(text=f"Size Comparison · {get_size_context(rs_km)}", font=dict(size=11, color="rgba(255,255,255,0.4)")))
    return fig


# ── Compare row HTML ──
def compare_row(label, val_a, val_b, unit=""):
    str_a = val_a if isinstance(val_a, str) else fmt_sci(val_a)
    str_b = val_b if isinstance(val_b, str) else fmt_sci(val_b)
    winner = ""
    ratio_html = ""
    if isinstance(val_a, (int, float)) and isinstance(val_b, (int, float)):
        if val_a > val_b:
            winner = "A"
        elif val_b > val_a:
            winner = "B"
        r = max(val_a, val_b) / min(val_a, val_b) if min(val_a, val_b) > 0 else 0
        if r > 1.01:
            ratio_html = f'<div style="font-size:0.6rem;color:rgba(255,255,255,0.18);margin-top:1px;">{fmt_sci(r,2)}×</div>'

    col_a = "#818cf8" if winner == "A" else "rgba(255,255,255,0.5)"
    col_b = "#fb923c" if winner == "B" else "rgba(255,255,255,0.5)"
    fw_a = "600" if winner == "A" else "400"
    fw_b = "600" if winner == "B" else "400"
    unit_html = f'<div style="font-size:0.55rem;color:rgba(255,255,255,0.18);">{unit}</div>' if unit else ""

    return f"""<tr>
        <td class="compare-left" style="color:{col_a};font-weight:{fw_a};">{str_a}</td>
        <td class="compare-center">{label}{unit_html}{ratio_html}</td>
        <td class="compare-right" style="color:{col_b};font-weight:{fw_b};">{str_b}</td>
    </tr>"""


# ── Export HTML ──
def build_export_html(mode, props=None, regime=None, m_solar=None, facts=None, props_a=None, props_b=None, m_a=None, m_b=None):
    def row(label, val, unit):
        return f'<tr><td style="padding:6px 12px;color:#888;font-size:11px;text-transform:uppercase;letter-spacing:0.08em">{label}</td><td style="padding:6px 12px;font-family:Courier New,monospace;font-size:14px;font-weight:600;color:#e2e8f0">{val}</td><td style="padding:6px 12px;color:#666;font-size:11px">{unit}</td></tr>'

    body = ""
    if mode == "single" and props:
        name, color, _ = regime
        body = f"""
        <div style="display:inline-block;background:{color}18;border:1px solid {color}40;border-radius:6px;padding:4px 12px;margin-bottom:16px">
            <span style="color:{color};font-size:12px;font-weight:600">{name}</span>
            <span style="color:#666;font-size:11px;margin-left:6px">{fmt_sci(m_solar)} M☉</span>
        </div>
        <table style="width:100%;border-collapse:collapse;margin-bottom:20px">
            {row("Mass", fmt_sci(props["mass_kg"]), "kg")}
            {row("Schwarzschild Radius", fmt_sci(props["rs_km"]), "km")}
            {row("Hawking Temperature", fmt_sci(props["temp_K"]), "K")}
            {row("B-H Entropy", fmt_sci(props["entropy_JK"]), "J/K")}
            {row("Luminosity", fmt_sci(props["lum_W"]), "W")}
            {row("Surface Gravity", fmt_sci(props["surf_grav"]), "m/s²")}
            {row("Evaporation Time", fmt_time(props["evap_yr"]), "")}
            {row("Event Horizon", fmt_sci(props["rs_m"]), "m")}
        </table>"""
        if facts:
            body += '<div style="margin-top:16px;padding:14px 16px;background:#111;border-radius:8px"><div style="font-size:10px;text-transform:uppercase;letter-spacing:0.1em;color:#555;margin-bottom:10px">Did you know?</div>'
            for icon, text in facts:
                body += f'<p style="margin:0 0 8px;font-size:12px;color:#aaa;line-height:1.6">{icon} {text}</p>'
            body += '</div>'

    title_extra = f" - {fmt_sci(m_solar)} M☉" if mode == "single" else " - Comparison"
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><title>Black Hole Thermodynamics{title_extra}</title>
<style>*{{margin:0;padding:0;box-sizing:border-box}}body{{background:#0c0c14;color:#e2e8f0;font-family:-apple-system,'Segoe UI',sans-serif;padding:40px;max-width:700px;margin:0 auto}}
tr:nth-child(even){{background:rgba(255,255,255,0.02)}}tr:hover{{background:rgba(255,255,255,0.04)}}table{{border-radius:8px;overflow:hidden}}</style></head>
<body>
<h1 style="font-size:22px;font-weight:700;margin-bottom:4px">Black Hole Thermodynamics</h1>
<p style="font-size:11px;color:#555;letter-spacing:0.06em;margin-bottom:24px">BHUMIK KHATWANI · ASTROPHYSICS, UIUC · {datetime.date.today().isoformat()}</p>
{body}
<p style="text-align:center;font-size:9px;color:#333;margin-top:32px;letter-spacing:0.08em">BEKENSTEIN-HAWKING THERMODYNAMICS · NIST CODATA 2018</p>
</body></html>"""


# ══════════════════════════════════════════════════
# PAGE
# ══════════════════════════════════════════════════

# ── Header ──
col_title, col_export = st.columns([5, 1])
with col_title:
    st.markdown("<div style='font-size:1.6rem;font-weight:700;letter-spacing:-0.02em;'>Black Hole Thermodynamics</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.7rem;color:rgba(255,255,255,0.25);letter-spacing:0.06em;margin-top:-8px;margin-bottom:16px;'>BHUMIK KHATWANI · ASTROPHYSICS, UIUC</div>", unsafe_allow_html=True)

# ── Session state init ──
if "feed_mass" not in st.session_state:
    st.session_state.feed_mass = 10.0
if "feed_log" not in st.session_state:
    st.session_state.feed_log = []

# ── Tabs ──
tab_single, tab_compare, tab_feed = st.tabs(["Single", "Compare", "Feed"])

# ══════════════════════════════════════════════════
# SINGLE MODE
# ══════════════════════════════════════════════════
with tab_single:
    c1, c2 = st.columns([2, 3])
    with c1:
        M_solar = st.number_input("Mass (solar masses M☉)", min_value=1e-20, max_value=1e12, value=10.0, format="%.4g", key="single_mass")
    with c2:
        preset = st.selectbox("Or load a preset", list(PRESETS.keys()), key="single_preset")
        if preset != "Custom":
            M_solar = PRESETS[preset]

    props = get_all_properties(M_solar)
    regime_badge(M_solar)

    # Metrics
    r1c1, r1c2, r1c3, r1c4 = st.columns(4)
    with r1c1: metric_card("Schwarzschild Radius", fmt_sci(props["rs_km"]), "km", "#818cf8")
    with r1c2: metric_card("Hawking Temperature", fmt_sci(props["temp_K"]), "Kelvin", "#fb923c")
    with r1c3: metric_card("B-H Entropy", fmt_sci(props["entropy_JK"]), "J/K", "#34d399")
    with r1c4: metric_card("Luminosity", fmt_sci(props["lum_W"]), "Watts", "#f472b6")

    r2c1, r2c2, r2c3, r2c4 = st.columns(4)
    with r2c1: metric_card("Surface Gravity", fmt_sci(props["surf_grav"]), "m/s²", "#a78bfa")
    with r2c2: metric_card("Evaporation Time", fmt_time(props["evap_yr"]), accent="#facc15")
    with r2c3: metric_card("Mass", fmt_sci(props["mass_kg"]), "kg", "#94a3b8")
    with r2c4: metric_card("Event Horizon", fmt_sci(props["rs_m"]), "metres", "#94a3b8")

    # Fun facts
    facts = get_fun_facts(props, M_solar)
    if facts:
        st.markdown('<div class="section-label">Did you know?</div>', unsafe_allow_html=True)
        show_facts(facts)

    # Size comparison
    st.markdown('<div class="section-label">Size Comparison</div>', unsafe_allow_html=True)
    st.plotly_chart(make_size_chart(M_solar, props["rs_km"]), use_container_width=True, config={"displayModeBar": False})

    # Scaling
    st.markdown('<div class="section-label">Scaling Relations</div>', unsafe_allow_html=True)
    chart_choice = st.radio("Property", ["Schwarzschild Radius", "Hawking Temperature", "B-H Entropy", "Evaporation Time"],
                            horizontal=True, key="scaling_radio", label_visibility="collapsed")
    chart_map = {
        "Schwarzschild Radius": ("rs_km", "Schwarzschild Radius", "km", "#818cf8"),
        "Hawking Temperature": ("temp_K", "Hawking Temperature", "K", "#fb923c"),
        "B-H Entropy": ("entropy_JK", "B-H Entropy", "J/K", "#34d399"),
        "Evaporation Time": ("evap_yr", "Evaporation Time", "yr", "#facc15"),
    }
    f, l, u, clr = chart_map[chart_choice]
    st.plotly_chart(make_scaling_chart(M_solar, f, l, u, clr), use_container_width=True, config={"displayModeBar": False})

    # Export
    regime_info = get_regime(M_solar)
    export_html = build_export_html("single", props=props, regime=regime_info, m_solar=M_solar, facts=facts)
    with col_export:
        st.download_button("⬇ Export", data=export_html, file_name=f"blackhole-{fmt_sci(M_solar, 2)}.html", mime="text/html")


# ══════════════════════════════════════════════════
# COMPARE MODE
# ══════════════════════════════════════════════════
with tab_compare:
    ca, cb = st.columns(2)
    with ca:
        st.markdown('<div class="section-label" style="color:#818cf8;">Black Hole A</div>', unsafe_allow_html=True)
        mass_a = st.number_input("Mass A (M☉)", min_value=1e-20, max_value=1e12, value=10.0, format="%.4g", key="cmp_a")
        preset_a = st.selectbox("Preset A", list(PRESETS.keys()), key="cmp_preset_a")
        if preset_a != "Custom": mass_a = PRESETS[preset_a]
        regime_badge(mass_a)
    with cb:
        st.markdown('<div class="section-label" style="color:#fb923c;">Black Hole B</div>', unsafe_allow_html=True)
        mass_b = st.number_input("Mass B (M☉)", min_value=1e-20, max_value=1e12, value=4e6, format="%.4g", key="cmp_b")
        preset_b = st.selectbox("Preset B", list(PRESETS.keys()), key="cmp_preset_b")
        if preset_b != "Custom": mass_b = PRESETS[preset_b]
        regime_badge(mass_b)

    pa = get_all_properties(mass_a)
    pb = get_all_properties(mass_b)

    # Comparison table
    name_a = next((k for k, v in PRESETS.items() if v == mass_a), f"{fmt_sci(mass_a)} M☉")
    name_b = next((k for k, v in PRESETS.items() if v == mass_b), f"{fmt_sci(mass_b)} M☉")

    table_html = f"""<table class="compare-table">
        <tr><td class="compare-left" style="font-weight:700;font-size:0.88rem;color:#818cf8;">{name_a}</td>
            <td class="compare-center" style="font-size:0.6rem;">vs</td>
            <td class="compare-right" style="font-weight:700;font-size:0.88rem;color:#fb923c;">{name_b}</td></tr>
        {compare_row("Mass", pa["mass_kg"], pb["mass_kg"], "kg")}
        {compare_row("Radius", pa["rs_km"], pb["rs_km"], "km")}
        {compare_row("Temperature", pa["temp_K"], pb["temp_K"], "K")}
        {compare_row("Entropy", pa["entropy_JK"], pb["entropy_JK"], "J/K")}
        {compare_row("Luminosity", pa["lum_W"], pb["lum_W"], "W")}
        {compare_row("Surf. Gravity", pa["surf_grav"], pb["surf_grav"], "m/s²")}
        {compare_row("Evaporation", fmt_time(pa["evap_yr"]), fmt_time(pb["evap_yr"]))}
    </table>"""
    st.markdown(table_html, unsafe_allow_html=True)

    # Side-by-side facts
    fa, fb = get_fun_facts(pa, mass_a), get_fun_facts(pb, mass_b)
    fc1, fc2 = st.columns(2)
    with fc1:
        st.markdown('<div class="section-label" style="color:#818cf8;">Facts — A</div>', unsafe_allow_html=True)
        show_facts(fa, 3)
    with fc2:
        st.markdown('<div class="section-label" style="color:#fb923c;">Facts — B</div>', unsafe_allow_html=True)
        show_facts(fb, 3)


# ══════════════════════════════════════════════════
# FEED MODE
# ══════════════════════════════════════════════════
with tab_feed:
    st.markdown("""<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
        <div>
            <div style="font-size:1rem;font-weight:600;color:#e2e8f0;">Feed the Black Hole</div>
            <div style="font-size:0.72rem;color:rgba(255,255,255,0.3);margin-top:3px;">Starting mass: 10 M☉. Throw things in. See what happens.</div>
        </div>
    </div>""", unsafe_allow_html=True)

    # Reset button
    if st.button("🔄 Reset", key="feed_reset"):
        st.session_state.feed_mass = 10.0
        st.session_state.feed_log = []
        st.rerun()

    fm = st.session_state.feed_mass
    fp = get_all_properties(fm)
    fr_name, fr_color, _ = get_regime(fm)

    # Status badges
    st.markdown(f"""<div style="display:flex;gap:10px;margin-bottom:16px;flex-wrap:wrap;">
        <div class="regime-badge" style="background:{fr_color}12;border:1px solid {fr_color}30;">
            <div style="width:7px;height:7px;border-radius:50%;background:{fr_color};"></div>
            <span style="font-size:0.78rem;color:{fr_color};font-weight:500;">{fr_name}</span>
        </div>
        <div class="metric-card" style="padding:6px 14px;display:inline-flex;align-items:center;gap:6px;margin-bottom:0;">
            <span style="font-size:0.65rem;color:rgba(255,255,255,0.35);text-transform:uppercase;letter-spacing:0.08em;">Mass</span>
            <span style="font-size:0.88rem;font-weight:700;color:#818cf8;font-family:'JetBrains Mono',monospace;">{fmt_sci(fm)} M☉</span>
        </div>
        <div class="metric-card" style="padding:6px 14px;display:inline-flex;align-items:center;gap:6px;margin-bottom:0;">
            <span style="font-size:0.65rem;color:rgba(255,255,255,0.35);text-transform:uppercase;letter-spacing:0.08em;">Consumed</span>
            <span style="font-size:0.88rem;font-weight:700;color:#fb923c;font-family:'JetBrains Mono',monospace;">{len(st.session_state.feed_log)}</span>
        </div>
    </div>""", unsafe_allow_html=True)

    # Throwable buttons
    st.markdown('<div class="section-label">Throw something in</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    for i, item in enumerate(THROWABLES):
        with cols[i % 4]:
            kg_str = f"{item['kg']:.2e}" if item["kg"] >= 1e6 else f"{item['kg']:,.0f}"
            if st.button(f"{item['icon']} {item['name']}\n{kg_str} kg", key=f"feed_{item['name']}", use_container_width=True):
                added_solar = item["kg"] / M_sun
                st.session_state.feed_mass += added_solar
                st.session_state.feed_log.append(item)
                st.rerun()

    # Metrics
    st.markdown('<div class="section-label">Current Properties</div>', unsafe_allow_html=True)
    mc1, mc2, mc3, mc4 = st.columns(4)
    with mc1: metric_card("Schwarzschild Radius", fmt_sci(fp["rs_km"]), "km", "#818cf8")
    with mc2: metric_card("Hawking Temperature", fmt_sci(fp["temp_K"]), "Kelvin", "#fb923c")
    with mc3: metric_card("B-H Entropy", fmt_sci(fp["entropy_JK"]), "J/K", "#34d399")
    with mc4: metric_card("Evaporation Time", fmt_time(fp["evap_yr"]), accent="#facc15")

    # Growth tracker
    if st.session_state.feed_log:
        start_p = get_all_properties(10.0)
        st.markdown('<div class="section-label" style="color:#818cf8;">Growth since you started</div>', unsafe_allow_html=True)
        gc1, gc2, gc3, gc4 = st.columns(4)
        for col, (label, key) in zip([gc1, gc2, gc3, gc4], [("Mass", "mass_kg"), ("Radius", "rs_km"), ("Temperature", "temp_K"), ("Entropy", "entropy_JK")]):
            ratio = fp[key] / start_p[key] if start_p[key] != 0 else 0
            grew = ratio > 1
            color = "#34d399" if grew else "#fb923c"
            prefix = "×" if ratio >= 1 else "÷"
            display_ratio = ratio if ratio >= 1 else (1 / ratio if ratio > 0 else 0)
            with col:
                st.markdown(f"""<div class="growth-label">{label}</div>
                    <div class="growth-val" style="color:{color};">{prefix}{fmt_sci(display_ratio)}</div>""", unsafe_allow_html=True)

        # Fun facts for current state
        feed_facts = get_fun_facts(fp, fm)
        if feed_facts:
            st.markdown('<div class="section-label">What you\'ve created</div>', unsafe_allow_html=True)
            show_facts(feed_facts, 3)

        # Last quip
        last = st.session_state.feed_log[-1]
        st.markdown(f"""<div class="quip-box">
            <div class="quip-text">{last["icon"]} {last["quip"]}</div>
        </div>""", unsafe_allow_html=True)

        # Feed log
        st.markdown(f'<div class="section-label">Consumed ({len(st.session_state.feed_log)} items)</div>', unsafe_allow_html=True)
        log_html = ""
        for item in reversed(st.session_state.feed_log):
            kg_str = f"{item['kg']:.2e}" if item["kg"] >= 1e6 else f"{item['kg']:,.0f}"
            log_html += f"""<div class="log-item">
                <span style="font-size:16px;flex-shrink:0;">{item["icon"]}</span>
                <div style="flex:1;min-width:0;">
                    <div style="display:flex;justify-content:space-between;align-items:baseline;gap:8px;">
                        <span class="log-name">{item["name"]}</span>
                        <span class="log-kg">+{kg_str} kg</span>
                    </div>
                    <div class="log-quip">{item["quip"]}</div>
                </div>
            </div>"""
        st.markdown(f'<div style="max-height:280px;overflow-y:auto;">{log_html}</div>', unsafe_allow_html=True)


# ── Footer ──
st.markdown("<div style='text-align:center;font-size:0.6rem;color:rgba(255,255,255,0.12);margin-top:2rem;letter-spacing:0.08em;'>BEKENSTEIN–HAWKING THERMODYNAMICS · NIST CODATA 2018</div>", unsafe_allow_html=True)
