from solar_orbits.domain.orbit_animation_3d_service import OrbitAnimation3DService
from solar_orbits.domain.orbit_data_service import OrbitDataService
from solar_orbits.domain.orbit_plot_service import OrbitPlotService
from solar_orbits.model.models import AnimationResult, PlotResult, SolarSystemOrbit
from solar_orbits.ports.animation.orbit_animation_3d import OrbitAnimation3DPort
from solar_orbits.config.factories import build_3d_animator, build_plotter
from solar_orbits.ports.ephemeris.adapters.synthetic_provider import (
    SyntheticEphemerisProvider,
)
from solar_orbits.ports.plotting.orbit_plotter import OrbitPlotterPort


class SpyPlotter(OrbitPlotterPort):
    engine_name = "spy"

    def __init__(self) -> None:
        self.received: SolarSystemOrbit | None = None

    def plot(
        self,
        solar_system: SolarSystemOrbit,
        output_path: str | None = None,
        show: bool = False,
    ) -> PlotResult:
        self.received = solar_system
        return PlotResult(engine=self.engine_name, output_path=output_path, rendered=True)


class Spy3DAnimator(OrbitAnimation3DPort):
    engine_name = "spy-3d"

    def __init__(self) -> None:
        self.received: SolarSystemOrbit | None = None

    def animate(
        self,
        solar_system: SolarSystemOrbit,
        output_path: str | None = None,
        show: bool = False,
    ) -> AnimationResult:
        self.received = solar_system
        return AnimationResult(
            engine=self.engine_name,
            output_path=output_path,
            rendered=True,
        )


def test_data_service_builds_orbits_independently_from_plotting() -> None:
    data_service = OrbitDataService(SyntheticEphemerisProvider())

    solar_system = data_service.get_orbits(
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
    assert all(orbit.positions for orbit in solar_system.orbits)


def test_data_service_rejects_invalid_date_range() -> None:
    data_service = OrbitDataService(SyntheticEphemerisProvider())

    try:
        data_service.get_orbits(
            start="2026-12-31",
            stop="2026-01-01",
            step="30d",
            bodies=["Earth"],
        )
    except ValueError as exc:
        assert "stop must be greater than or equal to start" in str(exc)
    else:
        raise AssertionError("Expected invalid date range to raise ValueError")


def test_plot_service_delegates_existing_orbits_to_selected_plotter() -> None:
    plotter = SpyPlotter()
    data_service = OrbitDataService(SyntheticEphemerisProvider())
    plot_service = OrbitPlotService(plotter)
    solar_system = data_service.get_orbits(
        start="2026-01-01",
        stop="2026-12-31",
        step="30d",
        bodies=["Earth", "Mars", "Halley"],
    )

    result = plot_service.plot_orbits(solar_system, output_path="out.gif")

    assert result.engine == "spy"
    assert plotter.received is solar_system


def test_3d_animation_service_delegates_existing_orbits_to_selected_animator() -> None:
    animator = Spy3DAnimator()
    data_service = OrbitDataService(SyntheticEphemerisProvider())
    animation_service = OrbitAnimation3DService(animator)
    solar_system = data_service.get_orbits(
        start="2026-01-01",
        stop="2026-12-31",
        step="30d",
        bodies=["Earth", "Mars", "Halley"],
    )

    result = animation_service.animate_orbits(
        solar_system,
        output_path="orbitas_3d.gif",
    )

    assert result.engine == "spy-3d"
    assert result.dimensions == "3d"
    assert animator.received is solar_system


def test_factories_build_supported_visual_engines_without_loading_optional_deps() -> None:
    assert build_plotter("matplotlib").engine_name == "matplotlib"
    assert build_plotter("pillow").engine_name == "pillow"
    assert build_plotter("pyvista").engine_name == "pyvista"
    assert build_plotter("vedo").engine_name == "vedo"
    assert build_3d_animator("matplotlib").engine_name == "matplotlib-3d"
    assert build_3d_animator("pillow").engine_name == "pillow-3d"
    assert build_3d_animator("pyvista").engine_name == "pyvista-3d"
    assert build_3d_animator("vedo").engine_name == "vedo-3d"
