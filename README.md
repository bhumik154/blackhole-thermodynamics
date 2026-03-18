# ⚫ Black Hole Thermodynamics — Interactive Visualizer (Python)

Streamlit + Plotly port of the React dashboard. Same physics, same features, same vibe.

## Features

- **Single mode** — pick a mass or preset, see all thermodynamic properties, scaling charts, size comparison, and fun facts
- **Compare mode** — side-by-side two black holes with a full property comparison table and per-side facts
- **Feed mode** — throw objects (you, a car, Earth, Sag A*...) into a 10 M☉ black hole, watch it grow, read the quips
- **Export** — download an HTML one-pager of the current state

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Project Structure

```
├── app.py              # Streamlit UI
├── physics.py          # Physics engine
├── requirements.txt
└── README.md
```

## Author

**Bhumik Khatwani** — Astrophysics, University of Illinois Urbana-Champaign
