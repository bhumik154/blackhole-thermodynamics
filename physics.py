"""
physics.py — Black Hole Thermodynamics Engine
All calculations based on General Relativity and Quantum Field Theory in curved spacetime.
Author: Bhumik Khatwani
"""

import numpy as np

# ── Physical Constants (SI units) ──────────────────────────────────────────────
G  = 6.674e-11       # Gravitational constant      [m³ kg⁻¹ s⁻²]
c  = 2.998e8         # Speed of light              [m/s]
hbar = 1.055e-34     # Reduced Planck constant     [J·s]
k_B  = 1.381e-23     # Boltzmann constant          [J/K]
sigma = 5.670e-8     # Stefan-Boltzmann constant   [W m⁻² K⁻⁴]

# ── Solar mass reference ───────────────────────────────────────────────────────
M_sun = 1.989e30     # kg


def schwarzschild_radius(M_kg: float) -> float:
    """
    Event horizon radius: r_s = 2GM/c²
    Returns radius in metres.
    """
    return (2 * G * M_kg) / c**2


def hawking_temperature(M_kg: float) -> float:
    """
    Hawking temperature: T = ℏc³ / (8πGMk_B)
    Returns temperature in Kelvin.
    """
    return (hbar * c**3) / (8 * np.pi * G * M_kg * k_B)


def bekenstein_hawking_entropy(M_kg: float) -> float:
    """
    Bekenstein–Hawking entropy: S = k_B·A / (4·l_P²)
    Simplified: S = 4πGM²k_B / (ℏc)
    Returns entropy in J/K.
    """
    return (4 * np.pi * G * M_kg**2 * k_B) / (hbar * c)


def hawking_luminosity(M_kg: float) -> float:
    """
    Power radiated by a black hole via Hawking radiation.
    L = ℏc⁶ / (15360π G²M²)
    Returns luminosity in Watts.
    """
    return (hbar * c**6) / (15360 * np.pi * G**2 * M_kg**2)


def evaporation_time(M_kg: float) -> float:
    """
    Time for complete evaporation: t = 5120π G²M³ / (ℏc⁴)
    Returns time in seconds.
    """
    return (5120 * np.pi * G**2 * M_kg**3) / (hbar * c**4)


def surface_gravity(M_kg: float) -> float:
    """
    Surface gravity at the event horizon: κ = c⁴ / (4GM)
    Returns surface gravity in m/s².
    """
    return c**4 / (4 * G * M_kg)


def get_all_properties(M_solar: float) -> dict:
    """
    Given mass in solar masses, return all thermodynamic properties.
    """
    M_kg = M_solar * M_sun

    t_evap_s = evaporation_time(M_kg)
    t_evap_yr = t_evap_s / (3.154e7)            # seconds → years

    rs_m = schwarzschild_radius(M_kg)
    rs_km = rs_m / 1e3

    T_K = hawking_temperature(M_kg)

    S = bekenstein_hawking_entropy(M_kg)

    L_W = hawking_luminosity(M_kg)

    kappa = surface_gravity(M_kg)

    return {
        "mass_solar":       M_solar,
        "mass_kg":          M_kg,
        "schwarzschild_m":  rs_m,
        "schwarzschild_km": rs_km,
        "hawking_temp_K":   T_K,
        "entropy_JK":       S,
        "luminosity_W":     L_W,
        "surface_gravity":  kappa,
        "evap_time_s":      t_evap_s,
        "evap_time_yr":     t_evap_yr,
    }


def scaling_curves(mass_range_solar: np.ndarray) -> dict:
    """
    Returns arrays of all properties across a range of masses.
    Used for plotting scaling relations.
    """
    masses_kg = mass_range_solar * M_sun
    return {
        "masses_solar":     mass_range_solar,
        "schwarzschild_km": np.array([schwarzschild_radius(m) / 1e3 for m in masses_kg]),
        "hawking_temp_K":   np.array([hawking_temperature(m) for m in masses_kg]),
        "entropy_JK":       np.array([bekenstein_hawking_entropy(m) for m in masses_kg]),
        "luminosity_W":     np.array([hawking_luminosity(m) for m in masses_kg]),
        "evap_time_yr":     np.array([evaporation_time(m) / 3.154e7 for m in masses_kg]),
    }
