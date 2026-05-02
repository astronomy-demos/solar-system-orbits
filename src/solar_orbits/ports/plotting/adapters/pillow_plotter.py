from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

from solar_orbits.ports.plotting.adapters.animation import (
    orbit_position_at_progress,
    sampled_frame_indexes,
)
from solar_orbits.model.models import PlotResult, SolarSystemOrbit
from solar_orbits.ports.plotting.orbit_plotter import OrbitPlotterPort


class PillowOrbitPlotter(OrbitPlotterPort):
    engine_name = "pillow"

    def plot(
        self,
        solar_system: SolarSystemOrbit,
        output_path: str | None = None,
        show: bool = False,
    ) -> PlotResult:
        if not output_path:
            raise ValueError("Pillow plotter requires an output path ending in .gif.")

        path = Path(output_path)
        if path.suffix.lower() != ".gif":
            raise ValueError("Pillow plotter only exports .gif animations.")

        path.parent.mkdir(parents=True, exist_ok=True)
        _write_pillow_gif(solar_system, path)

        return PlotResult(
            engine=self.engine_name,
            output_path=output_path,
            rendered=True,
        )


def _write_pillow_gif(solar_system: SolarSystemOrbit, path: Path) -> None:
    width = 1150
    height = 800
    padding = 60
    legend_width = 190
    plot_width = width - legend_width
    frame_indexes = sampled_frame_indexes(solar_system)
    max_frame_index = max(frame_indexes)
    colors = [
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

    xs = [position.x for orbit in solar_system.orbits for position in orbit.positions]
    ys = [position.y for orbit in solar_system.orbits for position in orbit.positions]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    span = max(max_x - min_x, max_y - min_y) or 1
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2

    def project(x: float, y: float) -> tuple[int, int]:
        scale = (min(plot_width, height) - padding * 2) / span
        px = plot_width / 2 + (x - center_x) * scale
        py = height / 2 - (y - center_y) * scale
        return round(px), round(py)

    orbit_paths = [
        [project(position.x, position.y) for position in orbit.positions]
        for orbit in solar_system.orbits
    ]

    frames: list[Image.Image] = []
    for frame_index in frame_indexes:
        image = Image.new("RGB", (width, height), "#0B1020")
        draw = ImageDraw.Draw(image)
        draw.text((24, 20), "Solar System Orbits - 2D", fill="#E8EEF8")
        _draw_2d_grid(draw, project, min_x, max_x, min_y, max_y)
        draw.ellipse(
            (
                plot_width / 2 - 8,
                height / 2 - 8,
                plot_width / 2 + 8,
                height / 2 + 8,
            ),
            fill="#FFD23F",
        )
        draw.text(
            (plot_width / 2 + 12, height / 2 - 8),
            solar_system.center,
            fill="#FFD23F",
        )

        for index, (orbit, path_points) in enumerate(
            zip(solar_system.orbits, orbit_paths)
        ):
            color = colors[index % len(colors)]
            if len(path_points) > 1:
                draw.line(path_points, fill=color, width=2)

            position = orbit_position_at_progress(orbit, frame_index, max_frame_index)
            px, py = project(position.x, position.y)
            draw.ellipse((px - 5, py - 5, px + 5, py + 5), fill=color)
            draw.text((px + 7, py - 7), orbit.body.name, fill=color)

        _draw_legend(draw, solar_system, colors, x=plot_width + 18, y=48)
        frames.append(image.convert("P", palette=Image.ADAPTIVE))

    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=70,
        loop=0,
        optimize=True,
    )


def _draw_2d_grid(
    draw: ImageDraw.ImageDraw,
    project,
    min_x: float,
    max_x: float,
    min_y: float,
    max_y: float,
) -> None:
    grid_color = "#223047"
    axis_color = "#6C7A92"
    for tick in _ticks(min_x, max_x):
        x1, y1 = project(tick, min_y)
        x2, y2 = project(tick, max_y)
        draw.line((x1, y1, x2, y2), fill=grid_color, width=1)
    for tick in _ticks(min_y, max_y):
        x1, y1 = project(min_x, tick)
        x2, y2 = project(max_x, tick)
        draw.line((x1, y1, x2, y2), fill=grid_color, width=1)

    zero_x1, zero_y1 = project(0, min_y)
    zero_x2, zero_y2 = project(0, max_y)
    zero_x3, zero_y3 = project(min_x, 0)
    zero_x4, zero_y4 = project(max_x, 0)
    draw.line((zero_x1, zero_y1, zero_x2, zero_y2), fill=axis_color, width=2)
    draw.line((zero_x3, zero_y3, zero_x4, zero_y4), fill=axis_color, width=2)
    draw.text((zero_x2 + 5, zero_y2), "Y", fill=axis_color)
    draw.text((zero_x4 + 5, zero_y4), "X", fill=axis_color)


def _draw_legend(
    draw: ImageDraw.ImageDraw,
    solar_system: SolarSystemOrbit,
    colors: list[str],
    x: int,
    y: int,
) -> None:
    draw.text((x, y), "Legend", fill="#E8EEF8")
    draw.ellipse((x, y + 30, x + 12, y + 42), fill="#FFD23F")
    draw.text((x + 20, y + 28), solar_system.center, fill="#E8EEF8")
    for index, orbit in enumerate(solar_system.orbits):
        item_y = y + 58 + index * 24
        color = colors[index % len(colors)]
        draw.rectangle((x, item_y + 3, x + 14, item_y + 17), fill=color)
        draw.text((x + 22, item_y), orbit.body.name, fill="#E8EEF8")


def _ticks(min_value: float, max_value: float, count: int = 8) -> list[float]:
    if count <= 1 or min_value == max_value:
        return [min_value]
    step = (max_value - min_value) / (count - 1)
    return [min_value + step * index for index in range(count)]
