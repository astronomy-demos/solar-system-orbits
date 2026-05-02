from __future__ import annotations

from solar_orbits.model.models import AnimationResult, SolarSystemOrbit
from solar_orbits.ports.animation_3d.orbit_animation_3d import OrbitAnimation3DPort


class OrbitAnimation3DService:
    def __init__(self, animator: OrbitAnimation3DPort) -> None:
        self._animator = animator

    def animate_orbits(
        self,
        solar_system: SolarSystemOrbit,
        output_path: str | None = None,
        show: bool = False,
    ) -> AnimationResult:
        return self._animator.animate(
            solar_system,
            output_path=output_path,
            show=show,
        )
