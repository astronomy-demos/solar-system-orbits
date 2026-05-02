from __future__ import annotations

from abc import ABC, abstractmethod

from solar_orbits.model.models import PlotResult, SolarSystemOrbit


class OrbitPlotterPort(ABC):
    engine_name: str

    @abstractmethod
    def plot(
        self,
        solar_system: SolarSystemOrbit,
        output_path: str | None = None,
        show: bool = False,
    ) -> PlotResult:
        """Render the given solar system orbit."""
