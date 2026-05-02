from __future__ import annotations

from solar_orbits.domain.orbit_animation_2d_service import OrbitAnimation2DService
from solar_orbits.model.models import Animation2DResult, SolarSystemOrbit
from solar_orbits.ports.animation_2d.orbit_animation_2d import OrbitAnimation2DPort

from tests.conftest import make_solar_system


class Spy2DAnimator(OrbitAnimation2DPort):
    engine_name = "spy"

    def __init__(self) -> None:
        self.received_solar_system: SolarSystemOrbit | None = None
        self.received_output_path: str | None = None
        self.received_show: bool | None = None

    def animate(
        self,
        solar_system: SolarSystemOrbit,
        output_path: str | None = None,
        show: bool = False,
    ) -> Animation2DResult:
        self.received_solar_system = solar_system
        self.received_output_path = output_path
        self.received_show = show
        return Animation2DResult(engine=self.engine_name, output_path=output_path, rendered=True)


def test_animate_orbits_delegates_existing_orbits_to_selected_animator() -> None:
    animator = Spy2DAnimator()
    service = OrbitAnimation2DService(animator)
    solar_system = make_solar_system()

    result = service.animate_orbits(
        solar_system,
        output_path="outputs/test.gif",
        show=True,
    )

    assert result == Animation2DResult(
        engine="spy",
        output_path="outputs/test.gif",
        rendered=True,
    )
    assert animator.received_solar_system is solar_system
    assert animator.received_output_path == "outputs/test.gif"
    assert animator.received_show is True
