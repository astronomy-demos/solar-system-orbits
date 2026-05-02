from __future__ import annotations

from solar_orbits.model.models import PlotResult, SolarSystemOrbit
from solar_orbits.ports.plotting.orbit_plotter import OrbitPlotterPort


class OrbitPlotService:
    def __init__(self, plotter: OrbitPlotterPort) -> None:
        self._plotter = plotter

    def plot_orbits(
        self,
        solar_system: SolarSystemOrbit,
        output_path: str | None = None,
        show: bool = False,
    ) -> PlotResult:
        return self._plotter.plot(
            solar_system,
            output_path=output_path,
            show=show,
        )
