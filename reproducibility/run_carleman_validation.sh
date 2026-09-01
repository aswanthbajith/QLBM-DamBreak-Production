#!/usr/bin/env bash
# ==============================================================================
# Master Reproducibility Script for Carleman QLBM Two-Phase Dam-Break Solver
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${ROOT_DIR}"

PYTHON_BIN="${ROOT_DIR}/.venv/bin/python"
PYTEST_BIN="${ROOT_DIR}/.venv/bin/pytest"

echo "========================================================================"
echo "CARLEMAN QLBM TWO-PHASE DAM-BREAK MASTER REPRODUCIBILITY PIPELINE"
echo "========================================================================"

echo "[1/8] Recording Canonical Classical Reference..."
"${PYTHON_BIN}" scripts/record_canonical_reference.py

echo "[2/8] Running Local Carleman Basis & Truncation Tests..."
"${PYTEST_BIN}" tests/test_carleman_basis.py tests/test_carleman_collision.py tests/test_carleman_truncation.py -v

echo "[3/8] Running Unitary Dilation & Block Encoding Tests..."
"${PYTEST_BIN}" tests/test_unitary_dilation.py tests/test_block_encoding.py tests/test_postselection.py -v

echo "[4/8] Running Two-Phase Coupled Carleman Tests..."
"${PYTEST_BIN}" tests/test_two_phase_carleman.py -v

echo "[5/8] Running Multi-Step Carleman Convergence Tests..."
"${PYTEST_BIN}" tests/test_multistep_carleman.py -v

echo "[6/8] Running Conservation & Physical Property Tests..."
"${PYTEST_BIN}" tests/test_carleman_mass_conservation.py tests/test_carleman_momentum.py tests/test_carleman_phase.py tests/test_carleman_streaming.py tests/test_carleman_boundary.py -v

echo "[7/8] Running Multi-Step Error Benchmark & Comparison..."
"${PYTHON_BIN}" scripts/run_carleman_multistep_validation.py

echo "[8/8] Checking IBM Hardware Preflight..."
"${PYTHON_BIN}" scripts/hardware_preflight.py

echo "========================================================================"
echo "ALL CARLEMAN VALIDATION LEVELS PASSED (SCIENTIFIC REPRODUCIBILITY VERIFIED)"
echo "========================================================================"
