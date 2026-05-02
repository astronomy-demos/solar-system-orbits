from __future__ import annotations

from pathlib import Path

from solar_orbits.model.models import PlotResult, SolarSystemOrbit
from solar_orbits.ports.plotting.orbit_plotter import OrbitPlotterPort
from solar_orbits.ports.plotting.adapters.animation import (
    orbit_position_at_progress,
    sampled_frame_indexes,
)


class MatplotlibOrbitPlotter(OrbitPlotterPort):
    engine_name = "matplotlib"

    def plot(
        self,
        solar_system: SolarSystemOrbit,
        output_path: str | None = None,
        show: bool = False,
    ) -> PlotResult:
        import matplotlib.pyplot as plt
        from matplotlib.animation import FuncAnimation, PillowWriter

        frame_indexes = sampled_frame_indexes(solar_system)
        max_frame_index = max(frame_indexes)
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111)
        ax.scatter([0], [0], color="gold", s=160, label=solar_system.center)

        all_xs: list[float] = []
        all_ys: list[float] = []
        moving_points = []

        for orbit in solar_system.orbits:
            xs = [position.x for position in orbit.positions]
            ys = [position.y for position in orbit.positions]
            all_xs.extend(xs)
            all_ys.extend(ys)
            ax.plot(xs, ys, label=f"{orbit.body.name} orbit", linewidth=1.2)
            moving_points.append(ax.scatter([xs[0]], [ys[0]], s=32, label=orbit.body.name))

        ax.set_title("Animacion 2D de orbitas del Sistema Solar")
        ax.set_xlabel("X (AU)")
        ax.set_ylabel("Y (AU)")
        ax.grid(True, color="#D0D0D0", linestyle="--", linewidth=0.5, alpha=0.65)
        ax.legend(loc="upper left")
        ax.set_aspect("equal", adjustable="box")
        _set_equal_limits(ax, all_xs, all_ys)
        fig.tight_layout()

        def update(frame_index: int):
            for moving_point, orbit in zip(moving_points, solar_system.orbits):
                position = orbit_position_at_progress(orbit, frame_index, max_frame_index)
                moving_point.set_offsets([[position.x, position.y]])
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
                raise ValueError("Matplotlib animations must be saved as .gif or .html.")

        if show:
            plt.show()

        plt.close(fig)
        return PlotResult(
            engine=self.engine_name,
            output_path=output_path,
            rendered=bool(output_path or show),
        )


def _set_equal_limits(ax, xs: list[float], ys: list[float]) -> None:
    max_range = max(
        max(xs) - min(xs),
        max(ys) - min(ys),
    )
    half_range = max_range / 2
    center_x = (max(xs) + min(xs)) / 2
    center_y = (max(ys) + min(ys)) / 2
    ax.set_xlim(center_x - half_range, center_x + half_range)
    ax.set_ylim(center_y - half_range, center_y + half_range)
