from __future__ import annotations

from solar_orbits.model.models import (
    BodyOrbit,
    CartesianPosition,
    CelestialBody,
    SolarSystemOrbit,
)


def make_orbit(
    body_name: str = "Earth",
    positions: tuple[CartesianPosition, ...] | None = None,
) -> BodyOrbit:
    body = CelestialBody(body_name, "test")
    return BodyOrbit.from_positions(
        body,
        positions
        or (
            CartesianPosition(1.0, 0.0, 0.0, "2026-01-01"),
            CartesianPosition(0.0, 1.0, 0.1, "2026-02-01"),
        ),
    )


def make_solar_system() -> SolarSystemOrbit:
    return SolarSystemOrbit.from_orbits(
        (
            make_orbit("Earth"),
            make_orbit(
                "Mars",
                (
                    CartesianPosition(1.5, 0.0, 0.0, "2026-01-01"),
                    CartesianPosition(0.0, 1.5, 0.2, "2026-02-01"),
                ),
            ),
        )
    )
