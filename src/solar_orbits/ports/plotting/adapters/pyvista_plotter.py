from __future__ import annotations

from pathlib import Path

from solar_orbits.model.models import PlotResult, SolarSystemOrbit
from solar_orbits.ports.plotting.adapters.animation import (
    orbit_position_at_progress,
    sampled_frame_indexes,
)
from solar_orbits.ports.plotting.orbit_plotter import OrbitPlotterPort


class PyVistaOrbitPlotter(OrbitPlotterPort):
    engine_name = "pyvista"

    def plot(
        self,
        solar_system: SolarSystemOrbit,
        output_path: str | None = None,
        show: bool = False,
    ) -> PlotResult:
        try:
            import numpy as np
            import pyvista as pv
        except ImportError as exc:
            raise ImportError(
                "PyVista is optional. Install it with: python -m pip install -e '.[pyvista]'"
            ) from exc

        if not output_path:
            raise ValueError("PyVista 2D plotter requires an output path ending in .gif.")

        path = Path(output_path)
        if path.suffix.lower() != ".gif":
            raise ValueError("PyVista 2D plotter only exports .gif animations.")

        path.parent.mkdir(parents=True, exist_ok=True)
        frame_indexes = sampled_frame_indexes(solar_system)
        max_frame_index = max(frame_indexes)
        colors = _colors()

        plotter = pv.Plotter(off_screen=not show, window_size=(1100, 850))
        plotter.set_background("#0B1020")
        plotter.add_mesh(pv.Sphere(radius=0.08, center=(0, 0, 0)), color="gold")

        for index, orbit in enumerate(solar_system.orbits):
            points = np.array([(p.x, p.y, 0.0) for p in orbit.positions])
            plotter.add_lines(points, color=colors[index % len(colors)], width=2)

        plotter.add_legend(
            [[solar_system.center, "gold"]]
            + [
                [orbit.body.name, colors[index % len(colors)]]
                for index, orbit in enumerate(solar_system.orbits)
            ]
        )
        plotter.show_grid(xlabel="X (AU)", ylabel="Y (AU)", zlabel="")
        plotter.view_xy()
        plotter.open_gif(str(path), fps=15)

        actor_names: list[str] = []
        for frame_index in frame_indexes:
            for actor_name in actor_names:
                plotter.remove_actor(actor_name)
            actor_names = []

            for index, orbit in enumerate(solar_system.orbits):
                position = orbit_position_at_progress(orbit, frame_index, max_frame_index)
                actor_name = f"{orbit.body.name}-{frame_index}"
                plotter.add_mesh(
                    pv.Sphere(radius=0.05, center=(position.x, position.y, 0.0)),
                    color=colors[index % len(colors)],
                    name=actor_name,
                )
                actor_names.append(actor_name)
            plotter.write_frame()

        plotter.close()
        return PlotResult(engine=self.engine_name, output_path=output_path, rendered=True)


def _colors() -> list[str]:
    return [
        "#4E79A7",
        "#F28E2B",
        "#59A14F",
        "#E15759",
        "#B07AA1",
        "#9C755F",
        "#76B7B2",
        "#EDC948",
        "#FF9DA7",
    ]
