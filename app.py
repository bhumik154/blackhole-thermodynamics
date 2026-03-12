"""
app.py — Black Hole Thermodynamics Interactive Visualizer
Author: Bhumik Khatwani
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import streamlit as st
from physics import get_all_properties, scaling_curves

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Black Hole Thermodynamics",
    page_icon="⚫",
    layout="wide",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Syne:wght@400;700;800&display=swap');

html, body, [class*="css"] {
    background-color: #050508;
    color: #e8e4d8;
    font-family: 'Space Mono', monospace;
}

h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    letter-spacing: -0.02em;
}

.stSlider > div { padding-top: 0.5rem; }

/* Metric cards */
.metric-card {
    background: linear-gradient(135deg, #0e0e18 0%, #12121f 100%);
    border: 1px solid #2a2a45;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.75rem;
    transition: border-color 0.2s;
}
.metric-card:hover { border-color: #5a4fcf; }
.metric-label {
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #6b6b8a;
    margin-bottom: 0.3rem;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.35rem;
    font-weight: 700;
    color: #c8c3ff;
}
.metric-unit {
    font-size: 0.75rem;
    color: #6b6b8a;
    margin-top: 0.1rem;
}

/* Section header */
.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #5a4fcf;
    margin: 2rem 0 1rem;
    border-bottom: 1px solid #1e1e30;
    padding-bottom: 0.4rem;
}

/* Insight box */
.insight-box {
    background: #0a0a14;
    border-left: 3px solid #5a4fcf;
    border-radius: 0 8px 8px 0;
    padding: 1rem 1.2rem;
    font-size: 0.82rem;
    color: #9e9ec0;
    line-height: 1.7;
    margin-top: 1.5rem;
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Matplotlib dark theme ──────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor":  "#050508",
    "axes.facecolor":    "#0e0e18",
    "axes.edgecolor":    "#2a2a45",
    "axes.labelcolor":   "#9e9ec0",
    "xtick.color":       "#4a4a6a",
    "ytick.color":       "#4a4a6a",
    "text.color":        "#e8e4d8",
    "grid.color":        "#1a1a2e",
    "grid.linestyle":    "--",
    "grid.alpha":        0.6,
    "font.family":       "monospace",
})

ACCENT  = "#7b6fe8"
ACCENT2 = "#e87b6f"
ACCENT3 = "#6fe8b4"
ACCENT4 = "#e8d06f"


# ── Helper: format large/small numbers ────────────────────────────────────────
def fmt(val, unit=""):
    for prefix, exp in [("", 0), ("k", 3), ("M", 6), ("B", 9),
                        ("T", 12), ("quadrillion", 15), ("10^18", 18),
                        ("10^21", 21), ("10^24", 24), ("10^27", 27),
                        ("10^30", 30), ("10^33", 33), ("10^36", 36),
                        ("10^39", 39), ("10^42", 42), ("10^45", 45),
                        ("10^48", 48), ("10^51", 51), ("10^54", 54),
                        ("10^57", 57), ("10^60", 60), ("10^63", 63),
                        ("10^66", 66), ("10^80", 80)]:
        pass

    if abs(val) == 0:
        return f"0 {unit}"
    exp = int(np.floor(np.log10(abs(val))))
    if exp >= 9:
        return f"{val:.3e} {unit}"
    elif exp >= 6:
        return f"{val/1e6:.3f} M{unit}"
    elif exp >= 3:
        return f"{val/1e3:.3f} k{unit}"
    elif exp >= 0:
        return f"{val:.4f} {unit}"
    else:
        return f"{val:.3e} {unit}"


def fmt_time(yr):
    if yr < 1:
        return f"{yr * 365.25:.2f} days"
    elif yr < 1e3:
        return f"{yr:.2f} years"
    elif yr < 1e6:
        return f"{yr/1e3:.2f} thousand years"
    elif yr < 1e9:
        return f"{yr/1e6:.2f} million years"
    elif yr < 1e12:
        return f"{yr/1e9:.2f} billion years"
    else:
        return f"{yr:.2e} years"


def metric_card(label, value_str, unit_str=""):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value_str}</div>
        <div class="metric-unit">{unit_str}</div>
    </div>""", unsafe_allow_html=True)


# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<h1 style='font-size:2.8rem; margin-bottom:0; color:#e8e4d8;'>
    ⚫ Black Hole Thermodynamics
</h1>
<p style='color:#4a4a6a; font-size:0.82rem; margin-top:0.3rem; letter-spacing:0.08em;'>
    INTERACTIVE VISUALIZER · BHUMIK KHATWANI
</p>
""", unsafe_allow_html=True)

st.divider()

# ── Sidebar controls ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div class='section-header'>Configuration</div>", unsafe_allow_html=True)

    mass_mode = st.radio(
        "Mass input mode",
        ["Slider (solar masses)", "Direct entry"],
        index=0,
    )

    if mass_mode == "Slider (solar masses)":
        M_solar = st.slider(
            "Black hole mass (M☉)",
            min_value=0.1,
            max_value=1e9,
            value=10.0,
            step=0.1,
            format="%.1f",
        )
    else:
        M_solar = st.number_input(
            "Black hole mass (M☉)",
            min_value=0.0001,
            max_value=1e12,
            value=10.0,
            format="%.4f",
        )

    st.markdown("<div class='section-header'>Presets</div>", unsafe_allow_html=True)
    preset = st.selectbox("Load a known black hole", [
        "Custom",
        "Stellar BH (10 M☉)",
        "Cygnus X-1 (21 M☉)",
        "GW150914 merger remnant (62 M☉)",
        "Sagittarius A* (4M M☉)",
        "M87* (6.5B M☉)",
        "Primordial micro BH (1e-18 M☉)",
    ])

    preset_map = {
        "Stellar BH (10 M☉)": 10,
        "Cygnus X-1 (21 M☉)": 21,
        "GW150914 merger remnant (62 M☉)": 62,
        "Sagittarius A* (4M M☉)": 4e6,
        "M87* (6.5B M☉)": 6.5e9,
        "Primordial micro BH (1e-18 M☉)": 1e-18,
    }
    if preset != "Custom":
        M_solar = preset_map[preset]

    st.markdown("<div class='section-header'>About</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.75rem; color:#4a4a6a; line-height:1.7;'>
    Built on Bekenstein–Hawking thermodynamics.<br><br>
    Formulae: Schwarzschild (1916), Bekenstein (1973), Hawking (1974–75).<br><br>
    Constants sourced from NIST CODATA 2018.
    </div>
    """, unsafe_allow_html=True)

# ── Compute ────────────────────────────────────────────────────────────────────
props = get_all_properties(M_solar)

# ── Metrics grid ───────────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>Thermodynamic Properties</div>",
            unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    metric_card("Mass", f"{M_solar:.4g}", "solar masses (M☉)")
    metric_card("Mass (SI)", f"{props['mass_kg']:.3e}", "kg")
with c2:
    metric_card("Schwarzschild Radius", f"{props['schwarzschild_km']:.4g}", "km")
    metric_card("Surface Gravity κ", f"{props['surface_gravity']:.3e}", "m/s²")
with c3:
    metric_card("Hawking Temperature", f"{props['hawking_temp_K']:.3e}", "Kelvin")
    metric_card("Luminosity", f"{props['luminosity_W']:.3e}", "Watts")
with c4:
    metric_card("B–H Entropy", f"{props['entropy_JK']:.3e}", "J/K")
    metric_card("Evaporation Time", fmt_time(props['evap_time_yr']), "")

# ── Plots ──────────────────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>Scaling Relations</div>",
            unsafe_allow_html=True)

# Build log-spaced mass range around the selected mass
log_center = np.log10(max(M_solar, 1e-20))
m_range = np.logspace(
    max(log_center - 4, -20),
    min(log_center + 4, 12),
    400,
)
curves = scaling_curves(m_range)

def make_fig(x, y, xlabel, ylabel, title, color, current_x, current_y, current_label):
    fig, ax = plt.subplots(figsize=(4.5, 3.2))
    ax.plot(x, y, color=color, linewidth=1.8, alpha=0.9)
    ax.axvline(current_x, color="#ffffff", linewidth=0.7, linestyle=":", alpha=0.5)
    ax.axhline(current_y, color="#ffffff", linewidth=0.7, linestyle=":", alpha=0.5)
    ax.scatter([current_x], [current_y], color=color, s=60, zorder=5,
               edgecolors="#ffffff", linewidths=0.8)
    ax.annotate(current_label, (current_x, current_y),
                textcoords="offset points", xytext=(8, 6),
                fontsize=7, color="#e8e4d8", alpha=0.9)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(xlabel, fontsize=8)
    ax.set_ylabel(ylabel, fontsize=8)
    ax.set_title(title, fontsize=9, color="#c8c3ff", pad=8)
    ax.grid(True)
    ax.tick_params(labelsize=7)
    fig.tight_layout()
    return fig

p1, p2 = st.columns(2)
p3, p4 = st.columns(2)

with p1:
    fig = make_fig(
        curves["masses_solar"], curves["schwarzschild_km"],
        "Mass (M☉)", "r_s (km)",
        "Schwarzschild Radius vs Mass",
        ACCENT,
        M_solar, props["schwarzschild_km"],
        f"{props['schwarzschild_km']:.2g} km",
    )
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

with p2:
    fig = make_fig(
        curves["masses_solar"], curves["hawking_temp_K"],
        "Mass (M☉)", "T (K)",
        "Hawking Temperature vs Mass",
        ACCENT2,
        M_solar, props["hawking_temp_K"],
        f"{props['hawking_temp_K']:.2e} K",
    )
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

with p3:
    fig = make_fig(
        curves["masses_solar"], curves["entropy_JK"],
        "Mass (M☉)", "S (J/K)",
        "Bekenstein–Hawking Entropy vs Mass",
        ACCENT3,
        M_solar, props["entropy_JK"],
        f"{props['entropy_JK']:.2e} J/K",
    )
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

with p4:
    fig = make_fig(
        curves["masses_solar"], curves["evap_time_yr"],
        "Mass (M☉)", "t_evap (yr)",
        "Evaporation Timescale vs Mass",
        ACCENT4,
        M_solar, props["evap_time_yr"],
        fmt_time(props["evap_time_yr"]),
    )
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

# ── Contextual insight ─────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>Physical Insight</div>",
            unsafe_allow_html=True)

T = props["hawking_temp_K"]
rs = props["schwarzschild_km"]
t_yr = props["evap_time_yr"]

if M_solar < 1e-10:
    regime = "primordial / micro black hole"
    note = (f"At {M_solar:.2e} M☉, this is a hypothetical primordial black hole. "
            f"Its Hawking temperature of {T:.2e} K is so extreme it would evaporate "
            f"almost instantaneously on cosmological timescales — in {fmt_time(t_yr)}.")
elif M_solar < 3:
    regime = "sub-stellar / exotic compact object"
    note = (f"Below ~3 M☉, general relativity predicts neutron star collapse rather than "
            f"a black hole. This is a theoretical Schwarzschild black hole at {M_solar:.2g} M☉ "
            f"with r_s = {rs:.3g} km and T_H = {T:.2e} K — "
            f"imperceptibly cold by any detector standard.")
elif M_solar < 100:
    regime = "stellar-mass black hole"
    note = (f"A classic stellar remnant at {M_solar:.2g} M☉. "
            f"Its event horizon sits at r_s ≈ {rs:.2f} km. "
            f"The Hawking temperature of {T:.2e} K is unmeasurably small — "
            f"the CMB at 2.7 K vastly overwhelms any Hawking signal. "
            f"Evaporation would take {fmt_time(t_yr)}.")
elif M_solar < 1e7:
    regime = "intermediate-mass black hole (IMBH)"
    note = (f"At {M_solar:.3g} M☉, this sits in the poorly understood IMBH regime. "
            f"Its event horizon radius is {rs:.2f} km and Hawking temperature "
            f"{T:.2e} K — effectively undetectable. "
            f"Evaporation time: {fmt_time(t_yr)}.")
else:
    regime = "supermassive black hole (SMBH)"
    note = (f"A supermassive giant at {M_solar:.3g} M☉ — comparable to galactic-centre SMBHs. "
            f"r_s ≈ {rs:.3g} km, T_H ≈ {T:.2e} K (essentially absolute zero). "
            f"This black hole would outlive the current age of the universe many times over: "
            f"evaporation time ≈ {fmt_time(t_yr)}.")

st.markdown(f"""
<div class='insight-box'>
<strong style='color:#c8c3ff;'>Regime: {regime}</strong><br><br>
{note}
</div>
""", unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; color:#2a2a45; font-size:0.7rem;
            margin-top:3rem; letter-spacing:0.1em;'>
    BHUMIK KHATWANI · ASTROPHYSICS, UIUC · BUILT WITH PYTHON + STREAMLIT
</div>
""", unsafe_allow_html=True)
