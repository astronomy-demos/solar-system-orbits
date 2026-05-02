from __future__ import annotations

from .models import CelestialBody

SOLAR_SYSTEM_BODIES: tuple[CelestialBody, ...] = (
    CelestialBody("Mercury", "199"),
    CelestialBody("Venus", "299"),
    CelestialBody("Earth", "399"),
    CelestialBody("Mars", "499"),
    CelestialBody("Jupiter", "599"),
    CelestialBody("Saturn", "699"),
    CelestialBody("Uranus", "799"),
    CelestialBody("Neptune", "899"),
    CelestialBody("Halley", "1P", "comet"),
)


def get_bodies(names: list[str] | None = None) -> tuple[CelestialBody, ...]:
    if not names:
        return SOLAR_SYSTEM_BODIES

    requested = {name.lower() for name in names}
    bodies = tuple(
        body for body in SOLAR_SYSTEM_BODIES if body.name.lower() in requested
    )
    missing = requested - {body.name.lower() for body in bodies}
    if missing:
        raise ValueError(f"Unknown celestial body names: {', '.join(sorted(missing))}")
    return bodies
