from __future__ import annotations

from solar_orbits.domain.orbit_animation_3d_service import OrbitAnimation3DService
from solar_orbits.model.models import AnimationResult, SolarSystemOrbit
from solar_orbits.ports.animation.orbit_animation_3d import OrbitAnimation3DPort

from tests.conftest import make_solar_system


class Spy3DAnimator(OrbitAnimation3DPort):
    engine_name = "spy-3d"

    def __init__(self) -> None:
        self.received_solar_system: SolarSystemOrbit | None = None
        self.received_output_path: str | None = None
        self.received_show: bool | None = None

    def animate(
        self,
        solar_system: SolarSystemOrbit,
        output_path: str | None = None,
        show: bool = False,
    ) -> AnimationResult:
        self.received_solar_system = solar_system
        self.received_output_path = output_path
        self.received_show = show
        return AnimationResult(
            engine=self.engine_name,
            output_path=output_path,
            rendered=True,
        )


def test_animate_orbits_delegates_existing_orbits_to_selected_animator() -> None:
    animator = Spy3DAnimator()
    service = OrbitAnimation3DService(animator)
    solar_system = make_solar_system()

    result = service.animate_orbits(
        solar_system,
        output_path="outputs/test_3d.gif",
        show=True,
    )

    assert result == AnimationResult(
        engine="spy-3d",
        output_path="outputs/test_3d.gif",
        rendered=True,
        dimensions="3d",
    )
    assert animator.received_solar_system is solar_system
    assert animator.received_output_path == "outputs/test_3d.gif"
    assert animator.received_show is True
