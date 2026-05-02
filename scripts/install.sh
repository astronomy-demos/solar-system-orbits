#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

VENV_DIR="${VENV_DIR:-"$PROJECT_ROOT/.venv"}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
KERNEL_NAME="${KERNEL_NAME:-solar-system-orbits}"
KERNEL_DISPLAY_NAME="${KERNEL_DISPLAY_NAME:-Solar System Orbits}"

if [ ! -d "$VENV_DIR" ]; then
  "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

VENV_PYTHON="$VENV_DIR/bin/python"

"$VENV_PYTHON" -m pip install --upgrade pip
"$VENV_PYTHON" -m pip install -r requirements.txt
"$VENV_PYTHON" -m pip install -e .
"$VENV_PYTHON" -m ipykernel install \
  --user \
  --name "$KERNEL_NAME" \
  --display-name "$KERNEL_DISPLAY_NAME"

"$VENV_PYTHON" - <<'PY'
import importlib

packages = [
    "numpy",
    "matplotlib",
    "PIL",
    "astroquery",
    "imageio",
    "pytest",
    "ipykernel",
    "solar_orbits",
]

for package in packages:
    importlib.import_module(package)

print("Instalacion validada: dependencias y paquete importan correctamente.")
PY

echo "Entorno listo en: $VENV_DIR"
echo "Kernel registrado: $KERNEL_DISPLAY_NAME"
