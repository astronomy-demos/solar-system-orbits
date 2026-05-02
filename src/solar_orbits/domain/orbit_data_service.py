from __future__ import annotations

from datetime import date, timedelta

from solar_orbits.model.bodies import get_bodies
from solar_orbits.model.models import SolarSystemOrbit
from solar_orbits.model.orbital_periods import longest_orbital_period_days
from solar_orbits.ports.ephemeris.ephemeris_provider import EphemerisProviderPort


class OrbitDataService:
    def __init__(self, ephemeris_provider: EphemerisProviderPort) -> None:
        self._ephemeris_provider = ephemeris_provider

    def get_orbits(
        self,
        start: str,
        stop: str,
        step: str,
        bodies: list[str] | None = None,
    ) -> SolarSystemOrbit:
        self._validate_date_range(start, stop)
        body_models = get_bodies(bodies)
        orbits = [
            self._ephemeris_provider.get_orbit(body, start, stop, step)
            for body in body_models
        ]
        return SolarSystemOrbit.from_orbits(orbits)

    def get_complete_orbits(
        self,
        start: str,
        step: str,
        bodies: list[str] | None = None,
    ) -> SolarSystemOrbit:
        stop = self.calculate_complete_orbit_stop(start, bodies)
        return self.get_orbits(start=start, stop=stop, step=step, bodies=bodies)

    @staticmethod
    def calculate_complete_orbit_stop(
        start: str, bodies: list[str] | None = None
    ) -> str:
        start_date = date.fromisoformat(start)
        margin_days = 30
        body_names = [body.name for body in get_bodies(bodies)]
        total_days = longest_orbital_period_days(body_names) + margin_days
        return (start_date + timedelta(days=total_days)).isoformat()

    @staticmethod
    def _validate_date_range(start: str, stop: str) -> None:
        start_date = date.fromisoformat(start)
        stop_date = date.fromisoformat(stop)
        if stop_date < start_date:
            raise ValueError("stop must be greater than or equal to start")
