from __future__ import annotations

import pytest

from solar_orbits.config.factories import (
    build_3d_animator,
    build_ephemeris_provider,
    build_2d_animator,
)


def test_build_ephemeris_provider_supports_known_providers() -> None:
    assert build_ephemeris_provider("synthetic").__class__.__name__ == (
        "SyntheticEphemerisProvider"
    )


def test_build_2d_animator_supports_known_2d_engines() -> None:
    assert build_2d_animator("matplotlib").engine_name == "matplotlib"
    assert build_2d_animator("pillow").engine_name == "pillow"


def test_build_3d_animator_supports_known_3d_engines() -> None:
    assert build_3d_animator("matplotlib").engine_name == "matplotlib-3d"
    assert build_3d_animator("pillow").engine_name == "pillow-3d"


def test_factories_reject_unknown_engines() -> None:
    with pytest.raises(ValueError, match="Unknown ephemeris provider"):
        build_ephemeris_provider("missing")

    with pytest.raises(ValueError, match="Unknown 2D animator engine"):
        build_2d_animator("missing")

    with pytest.raises(ValueError, match="Unknown 3D animator engine"):
        build_3d_animator("missing")
