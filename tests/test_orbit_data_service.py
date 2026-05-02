from __future__ import annotations

import pytest

from solar_orbits.domain.orbit_data_service import OrbitDataService
from solar_orbits.model.models import BodyOrbit, CelestialBody
from solar_orbits.ports.ephemeris.ephemeris_provider import EphemerisProviderPort

from tests.conftest import make_orbit


class SpyEphemerisProvider(EphemerisProviderPort):
    def __init__(self) -> None:
        self.calls: list[tuple[str, str, str, str]] = []

    def get_orbit(
        self,
        body: CelestialBody,
        start: str,
        stop: str,
        step: str,
    ) -> BodyOrbit:
        self.calls.append((body.name, start, stop, step))
        return make_orbit(body.name)


def test_get_orbits_requests_each_selected_body_from_provider() -> None:
    provider = SpyEphemerisProvider()
    service = OrbitDataService(provider)

    solar_system = service.get_orbits(
        start="2026-01-01",
        stop="2026-12-31",
        step="30d",
        bodies=["Earth", "Mars", "Halley"],
    )

    assert [orbit.body.name for orbit in solar_system.orbits] == [
        "Earth",
        "Mars",
        "Halley",
    ]
    assert provider.calls == [
        ("Earth", "2026-01-01", "2026-12-31", "30d"),
        ("Mars", "2026-01-01", "2026-12-31", "30d"),
        ("Halley", "2026-01-01", "2026-12-31", "30d"),
    ]


def test_get_orbits_rejects_invalid_date_range_before_calling_provider() -> None:
    provider = SpyEphemerisProvider()
    service = OrbitDataService(provider)

    with pytest.raises(ValueError, match="stop must be greater than or equal to start"):
        service.get_orbits(
            start="2026-12-31",
            stop="2026-01-01",
            step="30d",
            bodies=["Earth"],
        )

    assert provider.calls == []


def test_get_orbits_rejects_unknown_body() -> None:
    service = OrbitDataService(SpyEphemerisProvider())

    with pytest.raises(ValueError, match="Unknown celestial body names: pluto"):
        service.get_orbits(
            start="2026-01-01",
            stop="2026-12-31",
            step="30d",
            bodies=["Pluto"],
        )


def test_calculate_complete_orbit_stop_uses_longest_selected_orbit_plus_margin() -> None:
    assert (
        OrbitDataService.calculate_complete_orbit_stop(
            start="2026-01-01",
            bodies=["Earth", "Mars"],
        )
        == "2027-12-19"
    )


def test_get_complete_orbits_uses_calculated_stop_date() -> None:
    provider = SpyEphemerisProvider()
    service = OrbitDataService(provider)

    service.get_complete_orbits(
        start="2026-01-01",
        step="30d",
        bodies=["Earth", "Mars"],
    )

    assert provider.calls == [
        ("Earth", "2026-01-01", "2027-12-19", "30d"),
        ("Mars", "2026-01-01", "2027-12-19", "30d"),
    ]
