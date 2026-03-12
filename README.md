# ⚫ Black Hole Thermodynamics — Interactive Visualizer

An interactive web app that computes and visualizes the thermodynamic properties of a black hole given its mass — built on Bekenstein–Hawking thermodynamics and Hawking radiation theory.

**Live demo:** *(deploy to Streamlit Cloud and paste link here)*

---

## What It Computes

| Property | Formula |
|---|---|
| Schwarzschild Radius | r_s = 2GM/c² |
| Hawking Temperature | T = ℏc³ / (8πGMk_B) |
| Bekenstein–Hawking Entropy | S = 4πGM²k_B / (ℏc) |
| Hawking Luminosity | L = ℏc⁶ / (15360πG²M²) |
| Evaporation Timescale | t = 5120πG²M³ / (ℏc⁴) |
| Surface Gravity | κ = c⁴ / (4GM) |

All constants sourced from **NIST CODATA 2018**.

---

## Features

- 🎚 **Slider or direct entry** for black hole mass
- 🌌 **Presets** for real black holes: Cygnus X-1, Sagittarius A*, M87*, GW150914
- 📊 **4 scaling relation plots** (log–log) with your selected mass highlighted
- 🧠 **Contextual physical insight** that adapts to the mass regime (micro, stellar, IMBH, SMBH)
- 🎨 Dark space-themed UI

---

## Installation

```bash
git clone https://github.com/yourusername/blackhole-thermodynamics.git
cd blackhole-thermodynamics
pip install -r requirements.txt
streamlit run app.py
```

---

## Requirements

```
streamlit
matplotlib
numpy
```

Or install directly:
```bash
pip install streamlit matplotlib numpy
```

---

## Project Structure

```
.
├── app.py         # Streamlit UI and visualizations
├── physics.py     # Physics engine — all thermodynamic calculations
├── requirements.txt
└── README.md
```

---

## Physics Background

This project is grounded in **semi-classical gravity** — the intersection of general relativity and quantum field theory. Key results used:

- **Schwarzschild (1916)**: exact solution to Einstein's field equations for a non-rotating, uncharged black hole
- **Bekenstein (1973)**: black hole entropy is proportional to event horizon area
- **Hawking (1974–75)**: black holes emit thermal radiation with temperature inversely proportional to mass

> *"Black holes are not the eternal prisons they were once thought. Things can get out of a black hole, both to the outside, and possibly, to another universe."* — Stephen Hawking

---

## Author

**Bhumik Khatwani** — Astrophysics undergraduate, University of Illinois Urbana-Champaign  
[bhumikkhatwani.com](https://bhumikkhatwani.com) · [LinkedIn](https://www.linkedin.com/in/bhumik-khatwani)
