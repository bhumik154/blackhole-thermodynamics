# ⚫ Black Hole Thermodynamics

A calculator for things that shouldn't exist.

Plug in a mass. Get back the temperature, entropy, radius, luminosity, surface gravity, and evaporation timescale of a black hole. Watch how the numbers change across 30 orders of magnitude. Compare two black holes side by side. Or just throw Earth into one and see what happens.

Built with Streamlit + Plotly. The physics is real. The fun facts are too.

---

## What's in here

**Single mode** — Pick a mass (or choose a preset like Cygnus X-1, Sagittarius A*, or M87*). Get all six thermodynamic properties, a size comparison chart, scaling relations, and a handful of facts that'll make you stare at the ceiling for a bit.

**Compare mode** — Put two black holes next to each other. A 10 solar mass stellar remnant vs the 6.5 billion solar mass monster at the center of M87. The numbers are... not close.

**Feed mode** — Start with a 10 solar mass black hole. Throw things into it. You. A car. The Moon. Earth. Jupiter. The Sun. Sagittarius A*. Each one gets a quip, the mass updates live, and the properties shift in real time. It's a cosmic garbage disposal with math.

**Export** — Download everything as a clean HTML one-pager.

---

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

That's it. Opens in your browser.

---

## Files

```
app.py              the whole UI
physics.py          the math (Bekenstein-Hawking thermodynamics, all SI units)
requirements.txt    streamlit, plotly, numpy
README.md           you're reading it
```

---

## The physics

Everything here comes from three results:

- **Schwarzschild (1916)** solved Einstein's field equations for a non-rotating black hole
- **Bekenstein (1973)** showed that black holes have entropy proportional to their horizon area
- **Hawking (1974)** proved they radiate thermally and will eventually evaporate

Constants from NIST CODATA 2018.

The formulas are in `physics.py`. They're short, clean, and annotated. If you're studying this stuff, read that file first.

---

## Some things you'll learn

- A 10 solar mass black hole is colder than empty space
- Sagittarius A* is less dense than water
- A primordial micro black hole evaporates faster than you can blink, and it's hotter than anything that has ever existed
- If you threw the Sun into a stellar black hole, the black hole wouldn't even change regime

---

**Bhumik Khatwani** · Astrophysics · University of Illinois Urbana-Champaign  
[bhumikkhatwani.com](https://bhumikkhatwani.com) · [LinkedIn](https://www.linkedin.com/in/bhumik-khatwani)
