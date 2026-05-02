from __future__ import annotations

from math import cos, radians, sin
from pathlib import Path

from PIL import Image, ImageDraw

from solar_orbits.model.models import AnimationResult, CartesianPosition, SolarSystemOrbit
from solar_orbits.ports.animation.orbit_animation_3d import OrbitAnimation3DPort
from solar_orbits.ports.plotting.adapters.animation import (
    orbit_position_at_progress,
    sampled_frame_indexes,
)


class Pillow3DOrbitAnimator(OrbitAnimation3DPort):
    engine_name = "pillow-3d"

    def plot(
        self,
        solar_system: SolarSystemOrbit,
        output_path: str | None = None,
        show: bool = False,
    ) -> AnimationResult:
        return self.animate(solar_system, output_path=output_path, show=show)

    def animate(
        self,
        solar_system: SolarSystemOrbit,
        output_path: str | None = None,
        show: bool = False,
    ) -> AnimationResult:
        if not output_path:
            raise ValueError("Pillow 3D animator requires an output path ending in .gif.")

        path = Path(output_path)
        if path.suffix.lower() != ".gif":
            raise ValueError("Pillow 3D animator only exports .gif animations.")

        path.parent.mkdir(parents=True, exist_ok=True)
        _write_pillow_3d_gif(solar_system, path)

        return AnimationResult(
            engine=self.engine_name,
            output_path=output_path,
            rendered=True,
        )


def _write_pillow_3d_gif(solar_system: SolarSystemOrbit, path: Path) -> None:
    width = 1250
    height = 850
    padding = 70
    legend_width = 210
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

    projector = _IsometricProjector(solar_system, plot_width, height, padding)
    orbit_paths = [
        [projector.project(position)[:2] for position in orbit.positions]
        for orbit in solar_system.orbits
    ]
    grid = _build_reference_grid(solar_system)

    frames: list[Image.Image] = []
    for frame_index in frame_indexes:
        image = Image.new("RGB", (width, height), "#0B1020")
        draw = ImageDraw.Draw(image)
        draw.text((24, 20), "Solar System Orbits - 3D", fill="#E8EEF8")
        _draw_3d_grid(draw, projector, grid)

        sun_x, sun_y, _ = projector.project(CartesianPosition(0, 0, 0, "center"))
        draw.ellipse((sun_x - 9, sun_y - 9, sun_x + 9, sun_y + 9), fill="#FFD23F")
        draw.text((sun_x + 14, sun_y - 8), solar_system.center, fill="#FFD23F")

        for index, path_points in enumerate(orbit_paths):
            color = colors[index % len(colors)]
            if len(path_points) > 1:
                draw.line(path_points, fill=color, width=2)

        current_positions = []
        for index, orbit in enumerate(solar_system.orbits):
            position = orbit_position_at_progress(orbit, frame_index, max_frame_index)
            px, py, depth = projector.project(position)
            current_positions.append((depth, index, orbit.body.name, px, py))

        for _, index, name, px, py in sorted(current_positions):
            color = colors[index % len(colors)]
            draw.ellipse((px - 5, py - 5, px + 5, py + 5), fill=color)
            draw.text((px + 7, py - 7), name, fill=color)

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


def _build_reference_grid(
    solar_system: SolarSystemOrbit,
) -> tuple[list[float], list[float], float, float, float, float, float, float]:
    xs = [position.x for orbit in solar_system.orbits for position in orbit.positions]
    ys = [position.y for orbit in solar_system.orbits for position in orbit.positions]
    zs = [position.z for orbit in solar_system.orbits for position in orbit.positions]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    min_z, max_z = min(zs), max(zs)
    return (
        _ticks(min_x, max_x),
        _ticks(min_y, max_y),
        min_x,
        max_x,
        min_y,
        max_y,
        min_z,
        max_z,
    )


def _draw_3d_grid(
    draw: ImageDraw.ImageDraw,
    projector: "_IsometricProjector",
    grid: tuple[list[float], list[float], float, float, float, float, float, float],
) -> None:
    x_ticks, y_ticks, min_x, max_x, min_y, max_y, min_z, max_z = grid
    grid_color = "#223047"
    axis_color = "#7D8CA6"
    x_color = "#E15759"
    y_color = "#59A14F"
    z_color = "#4E79A7"

    for tick in x_ticks:
        start = projector.project(CartesianPosition(tick, min_y, 0, "grid"))[:2]
        end = projector.project(CartesianPosition(tick, max_y, 0, "grid"))[:2]
        draw.line((*start, *end), fill=grid_color, width=1)
    for tick in y_ticks:
        start = projector.project(CartesianPosition(min_x, tick, 0, "grid"))[:2]
        end = projector.project(CartesianPosition(max_x, tick, 0, "grid"))[:2]
        draw.line((*start, *end), fill=grid_color, width=1)

    x_start = projector.project(CartesianPosition(min_x, 0, 0, "axis"))[:2]
    x_end = projector.project(CartesianPosition(max_x, 0, 0, "axis"))[:2]
    y_start = projector.project(CartesianPosition(0, min_y, 0, "axis"))[:2]
    y_end = projector.project(CartesianPosition(0, max_y, 0, "axis"))[:2]
    z_start = projector.project(CartesianPosition(0, 0, min_z, "axis"))[:2]
    z_end = projector.project(CartesianPosition(0, 0, max_z, "axis"))[:2]

    draw.line((*x_start, *x_end), fill=x_color, width=3)
    draw.line((*y_start, *y_end), fill=y_color, width=3)
    draw.line((*z_start, *z_end), fill=z_color, width=3)
    draw.text((x_end[0] + 6, x_end[1]), "X", fill=x_color)
    draw.text((y_end[0] + 6, y_end[1]), "Y", fill=y_color)
    draw.text((z_end[0] + 6, z_end[1]), "Z", fill=z_color)

    base_a = projector.project(CartesianPosition(min_x, min_y, 0, "plane"))[:2]
    base_b = projector.project(CartesianPosition(max_x, min_y, 0, "plane"))[:2]
    base_c = projector.project(CartesianPosition(max_x, max_y, 0, "plane"))[:2]
    base_d = projector.project(CartesianPosition(min_x, max_y, 0, "plane"))[:2]
    draw.line((*base_a, *base_b), fill=axis_color, width=1)
    draw.line((*base_b, *base_c), fill=axis_color, width=1)
    draw.line((*base_c, *base_d), fill=axis_color, width=1)
    draw.line((*base_d, *base_a), fill=axis_color, width=1)


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


class _IsometricProjector:
    def __init__(
        self,
        solar_system: SolarSystemOrbit,
        width: int,
        height: int,
        padding: int,
    ) -> None:
        self._width = width
        self._height = height
        self._padding = padding
        self._yaw = radians(42)
        self._pitch = radians(34)
        self._z_scale = 1.35

        projected = [
            self._rotate(position)
            for orbit in solar_system.orbits
            for position in orbit.positions
        ]
        projected.append(self._rotate(CartesianPosition(0, 0, 0, "center")))

        xs = [point[0] for point in projected]
        ys = [point[1] for point in projected]
        span = max(max(xs) - min(xs), max(ys) - min(ys)) or 1
        self._center_x = (min(xs) + max(xs)) / 2
        self._center_y = (min(ys) + max(ys)) / 2
        self._scale = (min(width, height) - padding * 2) / span

    def project(self, position: CartesianPosition) -> tuple[int, int, float]:
        rotated_x, rotated_y, depth = self._rotate(position)
        px = self._width / 2 + (rotated_x - self._center_x) * self._scale
        py = self._height / 2 - (rotated_y - self._center_y) * self._scale
        return round(px), round(py), depth

    def _rotate(self, position: CartesianPosition) -> tuple[float, float, float]:
        z = position.z * self._z_scale
        yaw_x = position.x * cos(self._yaw) - position.y * sin(self._yaw)
        yaw_y = position.x * sin(self._yaw) + position.y * cos(self._yaw)
        pitch_y = yaw_y * cos(self._pitch) - z * sin(self._pitch)
        depth = yaw_y * sin(self._pitch) + z * cos(self._pitch)
        return yaw_x, pitch_y, depth
