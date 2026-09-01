#!/usr/bin/env bash
# ==============================================================================
# Hardware Preflight & Compilation Verification
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${ROOT_DIR}"

PYTHON_BIN="${ROOT_DIR}/.venv/bin/python"

echo "============================================================"
echo "RUNNING IBM QUANTUM HARDWARE PREFLIGHT PIPELINE"
echo "============================================================"

echo "[1/2] Checking 9-Point Hardware Preflight Interlocks..."
"${PYTHON_BIN}" scripts/hardware_preflight.py

echo "[2/2] Transpiling to IBM Quantum ISA Target..."
"${PYTHON_BIN}" scripts/prepare_real_ibm_circuit.py --nx 4 --ny 4 --timesteps 1

echo "============================================================"
echo "HARDWARE PREFLIGHT COMPLETED"
echo "============================================================"
