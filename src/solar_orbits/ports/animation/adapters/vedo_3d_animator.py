from __future__ import annotations

from pathlib import Path

from solar_orbits.model.models import AnimationResult, SolarSystemOrbit
from solar_orbits.ports.animation.orbit_animation_3d import OrbitAnimation3DPort
from solar_orbits.ports.plotting.adapters.animation import (
    orbit_position_at_progress,
    sampled_frame_indexes,
)
from solar_orbits.ports.plotting.adapters.vedo_plotter import _colors


class Vedo3DOrbitAnimator(OrbitAnimation3DPort):
    engine_name = "vedo-3d"

    def animate(
        self,
        solar_system: SolarSystemOrbit,
        output_path: str | None = None,
        show: bool = False,
    ) -> AnimationResult:
        try:
            from vedo import Line, Plotter, Point, Video
        except ImportError as exc:
            raise ImportError(
                "Vedo is optional. Install it with: python -m pip install -e '.[vedo]'"
            ) from exc

        if not output_path:
            raise ValueError("Vedo 3D animator requires an output path ending in .gif.")

        path = Path(output_path)
        if path.suffix.lower() != ".gif":
            raise ValueError("Vedo 3D animator only exports .gif animations.")

        path.parent.mkdir(parents=True, exist_ok=True)
        frame_indexes = sampled_frame_indexes(solar_system)
        max_frame_index = max(frame_indexes)
        colors = _colors()

        plotter = Plotter(offscreen=not show, size=(1100, 850), bg="#0B1020")
        static_actors = [Point((0, 0, 0), r=16, c="gold")]
        for index, orbit in enumerate(solar_system.orbits):
            points = [(p.x, p.y, p.z) for p in orbit.positions]
            static_actors.append(Line(points, c=colors[index % len(colors)], lw=2))

        video = Video(str(path), fps=15)
        for frame_index in frame_indexes:
            moving_actors = []
            for index, orbit in enumerate(solar_system.orbits):
                position = orbit_position_at_progress(orbit, frame_index, max_frame_index)
                moving_actors.append(
                    Point(
                        (position.x, position.y, position.z),
                        r=10,
                        c=colors[index % len(colors)],
                    )
                )
            plotter.clear()
            plotter.show(*static_actors, *moving_actors, axes=1, interactive=False)
            video.add_frame()

        video.close()
        plotter.close()
        return AnimationResult(
            engine=self.engine_name,
            output_path=output_path,
            rendered=True,
        )
