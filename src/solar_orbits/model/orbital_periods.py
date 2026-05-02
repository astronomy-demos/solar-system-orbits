from __future__ import annotations

ORBITAL_PERIOD_DAYS = {
    "Mercury": 88.0,
    "Venus": 224.7,
    "Earth": 365.2,
    "Mars": 687.0,
    "Jupiter": 4331.0,
    "Saturn": 10747.0,
    "Uranus": 30589.0,
    "Neptune": 59800.0,
    "Halley": 27510.0,
}


def longest_orbital_period_days(body_names: list[str] | None = None) -> int:
    if not body_names:
        return int(max(ORBITAL_PERIOD_DAYS.values()))

    selected: list[float] = []
    for name in body_names:
        normalized = name.title()
        try:
            selected.append(ORBITAL_PERIOD_DAYS[normalized])
        except KeyError as exc:
            raise ValueError(f"Unknown celestial body name: {name}") from exc
    return int(max(selected))
