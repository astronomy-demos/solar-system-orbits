from __future__ import annotations

from pathlib import Path

from solar_orbits.model.models import AnimationResult, SolarSystemOrbit
from solar_orbits.ports.animation.orbit_animation_3d import OrbitAnimation3DPort
from solar_orbits.ports.animation_2d.adapters.animation import (
    orbit_position_at_progress,
    sampled_frame_indexes,
)


class Matplotlib3DOrbitAnimator(OrbitAnimation3DPort):
    engine_name = "matplotlib-3d"

    def animate(
        self,
        solar_system: SolarSystemOrbit,
        output_path: str | None = None,
        show: bool = False,
    ) -> AnimationResult:
        import matplotlib.pyplot as plt
        from matplotlib.animation import FuncAnimation, PillowWriter

        frame_indexes = sampled_frame_indexes(solar_system)
        max_frame_index = max(frame_indexes)
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection="3d")
        ax.scatter([0], [0], [0], color="gold", s=160, label=solar_system.center)

        all_xs: list[float] = []
        all_ys: list[float] = []
        all_zs: list[float] = []
        moving_points = []

        for orbit in solar_system.orbits:
            xs = [position.x for position in orbit.positions]
            ys = [position.y for position in orbit.positions]
            zs = [position.z for position in orbit.positions]
            all_xs.extend(xs)
            all_ys.extend(ys)
            all_zs.extend(zs)
            ax.animate(xs, ys, zs, label=f"{orbit.body.name} orbit", linewidth=1.2)
            moving_points.append(
                ax.scatter([xs[0]], [ys[0]], [zs[0]], s=32, label=orbit.body.name)
            )

        ax.set_title("Animacion 3D de orbitas del Sistema Solar")
        ax.set_xlabel("X (AU)")
        ax.set_ylabel("Y (AU)")
        ax.set_zlabel("Z (AU)")
        ax.legend(loc="upper left")
        ax.set_box_aspect((1, 1, 0.35))
        _set_equal_limits_3d(ax, all_xs, all_ys, all_zs)
        fig.tight_layout()

        def update(frame_index: int):
            for moving_point, orbit in zip(moving_points, solar_system.orbits):
                position = orbit_position_at_progress(orbit, frame_index, max_frame_index)
                moving_point._offsets3d = ([position.x], [position.y], [position.z])
            return moving_points

        animation = FuncAnimation(
            fig,
            update,
            frames=frame_indexes,
            interval=70,
            blit=False,
        )

        if output_path:
            path = Path(output_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.suffix.lower() == ".html":
                path.write_text(animation.to_jshtml(), encoding="utf-8")
            elif path.suffix.lower() == ".gif":
                animation.save(path, writer=PillowWriter(fps=15))
            else:
                raise ValueError("Matplotlib 3D animations must be saved as .gif or .html.")

        if show:
            plt.show()

        plt.close(fig)
        return AnimationResult(
            engine=self.engine_name,
            output_path=output_path,
            rendered=bool(output_path or show),
        )


def _set_equal_limits_3d(
    ax,
    xs: list[float],
    ys: list[float],
    zs: list[float],
) -> None:
    max_range = max(
        max(xs) - min(xs),
        max(ys) - min(ys),
        max(zs) - min(zs),
    )
    half_range = max_range / 2
    center_x = (max(xs) + min(xs)) / 2
    center_y = (max(ys) + min(ys)) / 2
    center_z = (max(zs) + min(zs)) / 2
    ax.set_xlim(center_x - half_range, center_x + half_range)
    ax.set_ylim(center_y - half_range, center_y + half_range)
    ax.set_zlim(center_z - half_range, center_z + half_range)
