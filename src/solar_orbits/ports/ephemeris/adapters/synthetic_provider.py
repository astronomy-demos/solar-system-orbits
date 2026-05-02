from __future__ import annotations

from datetime import date, timedelta
from math import cos, pi, sin, sqrt

from solar_orbits.model.models import BodyOrbit, CartesianPosition, CelestialBody
from solar_orbits.model.orbital_periods import ORBITAL_PERIOD_DAYS
from solar_orbits.ports.ephemeris.ephemeris_provider import EphemerisProviderPort


_ORBITAL_RADII_AU = {
    "Mercury": 0.387,
    "Venus": 0.723,
    "Earth": 1.0,
    "Mars": 1.524,
    "Jupiter": 5.203,
    "Saturn": 9.537,
    "Uranus": 19.191,
    "Neptune": 30.07,
    "Halley": 17.8,
}

_ORBITAL_ECCENTRICITY = {
    "Mercury": 0.206,
    "Venus": 0.007,
    "Earth": 0.017,
    "Mars": 0.093,
    "Jupiter": 0.049,
    "Saturn": 0.057,
    "Uranus": 0.046,
    "Neptune": 0.011,
    "Halley": 0.967,
}

_INCLINATIONS_DEG = {
    "Mercury": 7.0,
    "Venus": 3.4,
    "Earth": 0.0,
    "Mars": 1.8,
    "Jupiter": 1.3,
    "Saturn": 2.5,
    "Uranus": 0.8,
    "Neptune": 1.8,
    "Halley": 162.3,
}


class SyntheticEphemerisProvider(EphemerisProviderPort):
    """Deterministic local provider for demos and tests without network access."""

    def get_orbit(
        self,
        body: CelestialBody,
        start: str,
        stop: str,
        step: str,
    ) -> BodyOrbit:
        start_date = date.fromisoformat(start)
        stop_date = date.fromisoformat(stop)
        step_days = _parse_day_step(step)
        semi_major_axis = _ORBITAL_RADII_AU[body.name]
        period = ORBITAL_PERIOD_DAYS[body.name]
        eccentricity = _ORBITAL_ECCENTRICITY[body.name]
        inclination = _INCLINATIONS_DEG[body.name] * pi / 180

        positions: list[CartesianPosition] = []
        current = start_date
        day_index = 0
        while current <= stop_date:
            anomaly = 2 * pi * (day_index / period)
            orbital_x = semi_major_axis * (cos(anomaly) - eccentricity)
            orbital_y = (
                semi_major_axis * sqrt(1 - eccentricity**2) * sin(anomaly)
            )
            positions.append(
                CartesianPosition(
                    x=orbital_x,
                    y=orbital_y * cos(inclination),
                    z=orbital_y * sin(inclination),
                    epoch=current.isoformat(),
                )
            )
            current += timedelta(days=step_days)
            day_index += step_days

        return BodyOrbit.from_positions(body, positions)


def _parse_day_step(step: str) -> int:
    normalized = step.strip().lower()
    if normalized.endswith("d"):
        normalized = normalized[:-1]
    days = int(normalized)
    if days <= 0:
        raise ValueError("Step must be a positive number of days, for example 15d.")
    return days
