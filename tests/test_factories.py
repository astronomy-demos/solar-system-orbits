from __future__ import annotations

import pytest

from solar_orbits.config.factories import (
    build_3d_animator,
    build_ephemeris_provider,
    build_plotter,
)


def test_build_ephemeris_provider_supports_known_providers() -> None:
    assert build_ephemeris_provider("synthetic").__class__.__name__ == (
        "SyntheticEphemerisProvider"
    )


def test_build_plotter_supports_known_2d_engines() -> None:
    assert build_plotter("matplotlib").engine_name == "matplotlib"
    assert build_plotter("pillow").engine_name == "pillow"
    assert build_plotter("pyvista").engine_name == "pyvista"
    assert build_plotter("vedo").engine_name == "vedo"


def test_build_3d_animator_supports_known_3d_engines() -> None:
    assert build_3d_animator("matplotlib").engine_name == "matplotlib-3d"
    assert build_3d_animator("pillow").engine_name == "pillow-3d"
    assert build_3d_animator("pyvista").engine_name == "pyvista-3d"
    assert build_3d_animator("vedo").engine_name == "vedo-3d"


def test_factories_reject_unknown_engines() -> None:
    with pytest.raises(ValueError, match="Unknown ephemeris provider"):
        build_ephemeris_provider("missing")

    with pytest.raises(ValueError, match="Unknown plotter engine"):
        build_plotter("missing")

    with pytest.raises(ValueError, match="Unknown 3D animator engine"):
        build_3d_animator("missing")
