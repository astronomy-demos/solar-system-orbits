from __future__ import annotations

from solar_orbits.ports.ephemeris.ephemeris_provider import EphemerisProviderPort
from solar_orbits.ports.animation.orbit_animation_3d import OrbitAnimation3DPort
from solar_orbits.ports.plotting.orbit_plotter import OrbitPlotterPort


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


def build_plotter(name: str) -> OrbitPlotterPort:
    plotter_name = name.lower()
    if plotter_name == "matplotlib":
        from solar_orbits.ports.plotting.adapters.matplotlib_plotter import (
            MatplotlibOrbitPlotter,
        )

        return MatplotlibOrbitPlotter()
    if plotter_name == "pillow":
        from solar_orbits.ports.plotting.adapters.pillow_plotter import PillowOrbitPlotter

        return PillowOrbitPlotter()
    if plotter_name == "pyvista":
        from solar_orbits.ports.plotting.adapters.pyvista_plotter import (
            PyVistaOrbitPlotter,
        )

        return PyVistaOrbitPlotter()
    if plotter_name == "vedo":
        from solar_orbits.ports.plotting.adapters.vedo_plotter import VedoOrbitPlotter

        return VedoOrbitPlotter()
    raise ValueError(f"Unknown plotter engine: {name}")


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
