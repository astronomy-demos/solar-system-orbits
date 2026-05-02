from __future__ import annotations

from solar_orbits.model.models import BodyOrbit, CartesianPosition, CelestialBody
from solar_orbits.ports.ephemeris.ephemeris_provider import EphemerisProviderPort


class JplHorizonsEphemerisProvider(EphemerisProviderPort):
    """Fetch cartesian vectors from NASA JPL Horizons through astroquery."""

    def __init__(self, center: str = "500@10") -> None:
        self._center = center

    def get_orbit(
        self,
        body: CelestialBody,
        start: str,
        stop: str,
        step: str,
    ) -> BodyOrbit:
        try:
            from astroquery.jplhorizons import Horizons
        except ImportError as exc:
            raise RuntimeError(
                "JPL provider requires astroquery. Install with: "
                'pip install -e ".[jpl]"'
            ) from exc

        horizons_kwargs = {
            "id": body.jpl_id,
            "location": self._center,
            "epochs": {"start": start, "stop": stop, "step": step},
        }
        if body.body_type == "comet":
            horizons_kwargs["id_type"] = "smallbody"

        obj = Horizons(
            **horizons_kwargs,
        )
        vectors = obj.vectors()
        positions = [
            CartesianPosition(
                x=float(row["x"]),
                y=float(row["y"]),
                z=float(row["z"]),
                epoch=str(row["datetime_str"]),
            )
            for row in vectors
        ]
        return BodyOrbit.from_positions(body, positions)
