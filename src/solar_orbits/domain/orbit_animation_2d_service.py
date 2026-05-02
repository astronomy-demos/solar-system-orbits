from __future__ import annotations

from solar_orbits.model.models import Animation2DResult, SolarSystemOrbit
from solar_orbits.ports.animation_2d.orbit_animation_2d import OrbitAnimation2DPort


class OrbitAnimation2DService:
    def __init__(self, animator: OrbitAnimation2DPort) -> None:
        self._animator = animator

    def animate_orbits(
        self,
        solar_system: SolarSystemOrbit,
        output_path: str | None = None,
        show: bool = False,
    ) -> Animation2DResult:
        return self._animator.animate(
            solar_system,
            output_path=output_path,
            show=show,
        )
