# Solar System Orbits

Proyecto en Python para obtener posiciones cartesianas `x`, `y`, `z` de cuerpos del Sistema Solar y visualizar orbitas completas en 2D y 3D desde notebooks.

## Incluye

- Todos los planetas: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus y Neptune.
- Cometa Halley.
- Proveedor sintetico local para demos sin internet.
- Adaptador NASA JPL Horizons.
- Graficadores 2D: Matplotlib, Pillow, PyVista y Vedo.
- Animadores 3D: Matplotlib, Pillow, PyVista y Vedo.
- Notebook para comparar cada libreria en dos columnas: 2D a la izquierda y 3D a la derecha.

## Estructura

```text
src/solar_orbits
├── notebook_utils.py
├── model
├── domain
├── ports
│   ├── animation
│   ├── ephemeris
│   └── plotting
└── config
```

## Instalacion

Todas las dependencias necesarias estan en `requirements.txt`.

```bash
bash scripts/install.sh
```

## Notebook

```text
notebooks/casos_graficadores.ipynb
```

El notebook obtiene las orbitas una sola vez y luego renderiza cada motor con la misma informacion:

- Matplotlib: 2D y 3D.
- Pillow: 2D y 3D.
- PyVista: 2D y 3D.
- Vedo: 2D y 3D.

Los GIFs generados se guardan en `outputs/`.

## Pruebas

```bash
python -m pytest tests
```

## Diagrama

El diagrama general de arquitectura tambien esta disponible en `docs/architecture.mmd`.

```mermaid
flowchart LR
    Notebook["Notebook"]

    subgraph Model["Model"]
        Body["CelestialBody"]
        Position["CartesianPosition"]
        BodyOrbit["BodyOrbit"]
        SolarSystem["SolarSystemOrbit"]
        PlotResult["PlotResult"]
        AnimationResult["AnimationResult"]
    end

    subgraph Domain["Domain services"]
        DataService["OrbitDataService"]
        PlotService["OrbitPlotService"]
        AnimationService["OrbitAnimation3DService"]
    end

    subgraph EphemerisPort["Port: ephemeris"]
        EphemerisContract["EphemerisProviderPort"]
        Synthetic["SyntheticEphemerisProvider"]
        JPL["JplHorizonsEphemerisProvider"]
    end

    subgraph PlottingPort["Port: plotting"]
        PlotterContract["OrbitPlotterPort"]
        Matplotlib["MatplotlibOrbitPlotter 2D"]
        Pillow["PillowOrbitPlotter 2D"]
        PyVista["PyVistaOrbitPlotter 2D"]
        Vedo["VedoOrbitPlotter 2D"]
    end

    subgraph AnimationPort["Port: animation 3D"]
        AnimationContract["OrbitAnimation3DPort"]
        Matplotlib3D["Matplotlib3DOrbitAnimator"]
        Pillow3D["Pillow3DOrbitAnimator"]
        PyVista3D["PyVista3DOrbitAnimator"]
        Vedo3D["Vedo3DOrbitAnimator"]
    end

    Notebook --> DataService
    DataService --> EphemerisContract
    EphemerisContract -. implementa .-> Synthetic
    EphemerisContract -. implementa .-> JPL
    DataService --> SolarSystem
    SolarSystem --> BodyOrbit
    BodyOrbit --> Body
    BodyOrbit --> Position

    Notebook --> PlotService
    Notebook --> SolarSystem
    PlotService --> PlotterContract
    PlotterContract -. implementa .-> Matplotlib
    PlotterContract -. implementa .-> Pillow
    PlotterContract -. implementa .-> PyVista
    PlotterContract -. implementa .-> Vedo
    PlotService --> PlotResult

    Notebook --> AnimationService
    AnimationService --> AnimationContract
    AnimationContract -. implementa .-> Matplotlib3D
    AnimationContract -. implementa .-> Pillow3D
    AnimationContract -. implementa .-> PyVista3D
    AnimationContract -. implementa .-> Vedo3D
    AnimationService --> AnimationResult
```
