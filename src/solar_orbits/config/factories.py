from __future__ import annotations

from solar_orbits.ports.ephemeris.ephemeris_provider import EphemerisProviderPort
from solar_orbits.ports.animation.orbit_animation_3d import OrbitAnimation3DPort
from solar_orbits.ports.animation_2d.orbit_animation_2d import OrbitAnimation2DPort


def build_ephemeris_provider(name: str) -> EphemerisProviderPort:
    provider_name = name.lower()
    if provider_name == "jpl":
        from solar_orbits.ports.ephemeris.adapters.jpl_horizons_provider import (
            JplHorizonsEphemerisProvider,
        )

        return JplHorizonsEphemerisProvider()
    if provider_name == "synthetic":
        from solar_orbits.ports.ephemeris.adapters.synthetic_provider import (
            SyntheticEphemerisProvider,
        )

        return SyntheticEphemerisProvider()
    raise ValueError(f"Unknown ephemeris provider: {name}")


def build_2d_animator(name: str) -> OrbitAnimation2DPort:
    animator_name = name.lower()
    if animator_name == "matplotlib":
        from solar_orbits.ports.animation_2d.adapters.matplotlib_2d_animator import (
            Matplotlib2DOrbitAnimator,
        )

        return Matplotlib2DOrbitAnimator()
    if animator_name == "pillow":
        from solar_orbits.ports.animation_2d.adapters.pillow_2d_animator import Pillow2DOrbitAnimator

        return Pillow2DOrbitAnimator()
    if animator_name == "pyvista":
        from solar_orbits.ports.animation_2d.adapters.pyvista_2d_animator import (
            PyVista2DOrbitAnimator,
        )

        return PyVista2DOrbitAnimator()
    if animator_name == "vedo":
        from solar_orbits.ports.animation_2d.adapters.vedo_2d_animator import Vedo2DOrbitAnimator

        return Vedo2DOrbitAnimator()
    raise ValueError(f"Unknown 2D animator engine: {name}")


def build_3d_animator(name: str) -> OrbitAnimation3DPort:
    animator_name = name.lower()
    if animator_name == "matplotlib":
        from solar_orbits.ports.animation.adapters.matplotlib_3d_animator import (
            Matplotlib3DOrbitAnimator,
        )

        return Matplotlib3DOrbitAnimator()
    if animator_name == "pillow":
        from solar_orbits.ports.animation.adapters.pillow_3d_animator import (
            Pillow3DOrbitAnimator,
        )

        return Pillow3DOrbitAnimator()
    if animator_name == "pyvista":
        from solar_orbits.ports.animation.adapters.pyvista_3d_animator import (
            PyVista3DOrbitAnimator,
        )

        return PyVista3DOrbitAnimator()
    if animator_name == "vedo":
        from solar_orbits.ports.animation.adapters.vedo_3d_animator import (
            Vedo3DOrbitAnimator,
        )

        return Vedo3DOrbitAnimator()
    raise ValueError(f"Unknown 3D animator engine: {name}")
