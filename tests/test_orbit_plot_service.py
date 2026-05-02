from __future__ import annotations

from solar_orbits.domain.orbit_plot_service import OrbitPlotService
from solar_orbits.model.models import PlotResult, SolarSystemOrbit
from solar_orbits.ports.plotting.orbit_plotter import OrbitPlotterPort

from tests.conftest import make_solar_system


class SpyPlotter(OrbitPlotterPort):
    engine_name = "spy"

    def __init__(self) -> None:
        self.received_solar_system: SolarSystemOrbit | None = None
        self.received_output_path: str | None = None
        self.received_show: bool | None = None

    def plot(
        self,
        solar_system: SolarSystemOrbit,
        output_path: str | None = None,
        show: bool = False,
    ) -> PlotResult:
        self.received_solar_system = solar_system
        self.received_output_path = output_path
        self.received_show = show
        return PlotResult(engine=self.engine_name, output_path=output_path, rendered=True)


def test_plot_orbits_delegates_existing_orbits_to_selected_plotter() -> None:
    plotter = SpyPlotter()
    service = OrbitPlotService(plotter)
    solar_system = make_solar_system()

    result = service.plot_orbits(
        solar_system,
        output_path="outputs/test.gif",
        show=True,
    )

    assert result == PlotResult(
        engine="spy",
        output_path="outputs/test.gif",
        rendered=True,
    )
    assert plotter.received_solar_system is solar_system
    assert plotter.received_output_path == "outputs/test.gif"
    assert plotter.received_show is True
