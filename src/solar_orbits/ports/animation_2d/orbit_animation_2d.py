from __future__ import annotations

from abc import ABC, abstractmethod

from solar_orbits.model.models import Animation2DResult, SolarSystemOrbit


class OrbitAnimation2DPort(ABC):
    engine_name: str

    @abstractmethod
    def animate(
        self,
        solar_system: SolarSystemOrbit,
        output_path: str | None = None,
        show: bool = False,
    ) -> Animation2DResult:
        """Render a 2D animation for the given solar system orbit."""
