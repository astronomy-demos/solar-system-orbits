from __future__ import annotations

import base64
from pathlib import Path

from solar_orbits.domain.orbit_animation_3d_service import OrbitAnimation3DService
from solar_orbits.domain.orbit_animation_2d_service import OrbitAnimation2DService
from solar_orbits.model.models import SolarSystemOrbit
from solar_orbits.ports.animation_3d.orbit_animation_3d import OrbitAnimation3DPort
from solar_orbits.ports.animation_2d.orbit_animation_2d import OrbitAnimation2DPort


def show_gif(path: Path, width: int = 900) -> None:
    from IPython.display import HTML, display

    display(
        HTML(
            f'<img src="{_gif_data_uri(path)}" width="{width}" '
            'style="max-width:100%; height:auto;" />'
        )
    )


def show_gif_pair(
    left_path: Path,
    right_path: Path,
    left_title: str,
    right_title: str,
) -> None:
    from IPython.display import HTML, display

    html = f"""
    <div style="display:grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap:16px; align-items:start;">
      <div>
        <h4 style="margin:0 0 8px 0; font-family:sans-serif;">{left_title}</h4>
        <img src="{_gif_data_uri(left_path)}" style="width:100%; max-width:100%; height:auto;" />
      </div>
      <div>
        <h4 style="margin:0 0 8px 0; font-family:sans-serif;">{right_title}</h4>
        <img src="{_gif_data_uri(right_path)}" style="width:100%; max-width:100%; height:auto;" />
      </div>
    </div>
    """
    display(HTML(html))


def render_engine_pair(
    engine_name: str,
    animator_2d: OrbitAnimation2DPort,
    animator_3d: OrbitAnimation3DPort,
    solar_system_orbits: SolarSystemOrbit,
    outputs_dir: Path,
    prefix: str,
) -> None:
    gif_2d = outputs_dir / f"{prefix}_2d.gif"
    gif_3d = outputs_dir / f"{prefix}_3d.gif"
    gif_2d.unlink(missing_ok=True)
    gif_3d.unlink(missing_ok=True)

    try:
        OrbitAnimation2DService(animator_2d).animate_orbits(
            solar_system_orbits,
            output_path=str(gif_2d),
            show=False,
        )
        OrbitAnimation3DService(animator_3d).animate_orbits(
            solar_system_orbits,
            output_path=str(gif_3d),
            show=False,
        )
    except Exception as error:
        show_engine_error(engine_name, error)
        return

    show_gif_pair(
        gif_2d,
        gif_3d,
        f"{engine_name} 2D",
        f"{engine_name} 3D",
    )


def show_engine_error(engine: str, error: Exception) -> None:
    from IPython.display import HTML, display

    html = f"""
    <div style="border:1px solid #ddd; padding:12px; border-radius:6px; font-family:sans-serif;">
      <strong>{engine}</strong><br />
      No se pudo ejecutar este motor.<br />
      <code>{type(error).__name__}: {error}</code>
    </div>
    """
    display(HTML(html))


def _gif_data_uri(path: Path) -> str:
    data = path.read_bytes()
    if not data.startswith((b"GIF87a", b"GIF89a")):
        raise ValueError(f"El archivo no es un GIF valido: {path}")
    encoded = base64.b64encode(data).decode("ascii")
    return f"data:image/gif;base64,{encoded}"
