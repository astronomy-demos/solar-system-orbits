from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class CartesianPosition:
    """Celestial body position in astronomical units."""

    x: float
    y: float
    z: float
    epoch: str


@dataclass(frozen=True)
class CelestialBody:
    name: str
    jpl_id: str
    body_type: str = "planet"


@dataclass(frozen=True)
class BodyOrbit:
    body: CelestialBody
    positions: tuple[CartesianPosition, ...]

    @classmethod
    def from_positions(
        cls, body: CelestialBody, positions: Iterable[CartesianPosition]
    ) -> "BodyOrbit":
        return cls(body=body, positions=tuple(positions))

    def require_positions(self) -> None:
        if not self.positions:
            raise ValueError(f"No positions were found for {self.body.name}.")


@dataclass(frozen=True)
class SolarSystemOrbit:
    orbits: tuple[BodyOrbit, ...]
    center: str = "Sun"

    @classmethod
    def from_orbits(cls, orbits: Iterable[BodyOrbit]) -> "SolarSystemOrbit":
        orbit_tuple = tuple(orbits)
        if not orbit_tuple:
            raise ValueError("At least one body orbit is required.")
        for orbit in orbit_tuple:
            orbit.require_positions()
        return cls(orbits=orbit_tuple)


@dataclass(frozen=True)
class PlotResult:
    engine: str
    output_path: str | None
    rendered: bool


@dataclass(frozen=True)
class AnimationResult:
    engine: str
    output_path: str | None
    rendered: bool
    dimensions: str = "3d"
