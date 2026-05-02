from __future__ import annotations

from abc import ABC, abstractmethod

from solar_orbits.model.models import AnimationResult, SolarSystemOrbit


class OrbitAnimation3DPort(ABC):
    engine_name: str

    @abstractmethod
    def animate(
        self,
        solar_system: SolarSystemOrbit,
        output_path: str | None = None,
        show: bool = False,
    ) -> AnimationResult:
        """Render a 3D animation for the given solar system orbit."""
