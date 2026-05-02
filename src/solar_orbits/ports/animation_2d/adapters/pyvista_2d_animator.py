from __future__ import annotations

from pathlib import Path

from solar_orbits.model.models import Animation2DResult, SolarSystemOrbit
from solar_orbits.ports.animation_2d.adapters.animation import (
    orbit_position_at_progress,
    sampled_frame_indexes,
)
from solar_orbits.ports.animation_2d.orbit_animation_2d import OrbitAnimation2DPort


class PyVista2DOrbitAnimator(OrbitAnimation2DPort):
    engine_name = "pyvista"

    def animate(
        self,
        solar_system: SolarSystemOrbit,
        output_path: str | None = None,
        show: bool = False,
    ) -> Animation2DResult:
        try:
            import numpy as np
            import pyvista as pv
        except ImportError as exc:
            raise ImportError(
                "PyVista is required for this engine. Run: bash scripts/install.sh"
            ) from exc

        if not output_path:
            raise ValueError("PyVista 2D animator requires an output path ending in .gif.")

        path = Path(output_path)
        if path.suffix.lower() != ".gif":
            raise ValueError("PyVista 2D animator only exports .gif animations.")

        path.parent.mkdir(parents=True, exist_ok=True)
        frame_indexes = sampled_frame_indexes(solar_system)
        max_frame_index = max(frame_indexes)
        colors = _colors()

        animator = pv.Plotter(off_screen=not show, window_size=(1100, 850))
        animator.set_background("#0B1020")
        animator.add_mesh(pv.Sphere(radius=0.08, center=(0, 0, 0)), color="gold")

        for index, orbit in enumerate(solar_system.orbits):
            points = np.array([(p.x, p.y, 0.0) for p in orbit.positions])
            animator.add_lines(points, color=colors[index % len(colors)], width=2)

        animator.add_legend(
            [[solar_system.center, "gold"]]
            + [
                [orbit.body.name, colors[index % len(colors)]]
                for index, orbit in enumerate(solar_system.orbits)
            ]
        )
        animator.show_grid(xlabel="X (AU)", ylabel="Y (AU)", zlabel="")
        animator.view_xy()
        animator.open_gif(str(path), fps=15)

        actor_names: list[str] = []
        for frame_index in frame_indexes:
            for actor_name in actor_names:
                animator.remove_actor(actor_name)
            actor_names = []

            for index, orbit in enumerate(solar_system.orbits):
                position = orbit_position_at_progress(orbit, frame_index, max_frame_index)
                actor_name = f"{orbit.body.name}-{frame_index}"
                animator.add_mesh(
                    pv.Sphere(radius=0.05, center=(position.x, position.y, 0.0)),
                    color=colors[index % len(colors)],
                    name=actor_name,
                )
                actor_names.append(actor_name)
            animator.write_frame()

        animator.close()
        return Animation2DResult(engine=self.engine_name, output_path=output_path, rendered=True)


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
