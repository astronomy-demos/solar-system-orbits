from __future__ import annotations

from abc import ABC, abstractmethod

from solar_orbits.model.models import CelestialBody, BodyOrbit


class EphemerisProviderPort(ABC):
    @abstractmethod
    def get_orbit(
            self,
            body: CelestialBody,
            start: str,
            stop: str,
            step: str,
    ) -> BodyOrbit:
        """Return cartesian positions for a body in the requested time range."""
