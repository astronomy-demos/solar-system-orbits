from __future__ import annotations

from solar_orbits.model.models import BodyOrbit, SolarSystemOrbit


def sampled_frame_indexes(
    solar_system: SolarSystemOrbit,
    max_frames: int = 240,
) -> list[int]:
    longest = max(len(orbit.positions) for orbit in solar_system.orbits)
    if longest <= 1:
        return [0]
    if longest <= max_frames:
        return list(range(longest))

    step = (longest - 1) / (max_frames - 1)
    return sorted({round(index * step) for index in range(max_frames)})


def orbit_position_at_progress(orbit: BodyOrbit, frame_index: int, max_index: int):
    if max_index <= 0:
        return orbit.positions[0]
    orbit_index = round(frame_index * (len(orbit.positions) - 1) / max_index)
    return orbit.positions[orbit_index]
