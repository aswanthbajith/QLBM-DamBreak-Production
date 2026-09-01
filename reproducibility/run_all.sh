#!/usr/bin/env bash
# ==============================================================================
# Master Execution & Benchmark Validation Suite
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${ROOT_DIR}"

PYTHON_BIN="${ROOT_DIR}/.venv/bin/python"
PYTEST_BIN="${ROOT_DIR}/.venv/bin/pytest"

echo "============================================================"
echo "RUNNING FULL QLBM-DAMBREAK REPRODUCIBILITY SUITE"
echo "============================================================"

echo "[1/4] Running Complete Unit Test Suite..."
"${PYTEST_BIN}" -v

echo "[2/4] Running Operator Ablation & Forensic Evaluation..."
"${PYTHON_BIN}" scripts/run_operator_ablation.py

echo "[3/4] Running Shot Noise & Error Decomposition..."
"${PYTHON_BIN}" scripts/run_shot_noise_analysis.py

echo "[4/4] Running Physical Dam-Break Tracking..."
"${PYTHON_BIN}" scripts/run_dam_break_physics_analysis.py

echo "============================================================"
echo "FULL REPRODUCIBILITY PIPELINE COMPLETED SUCCESSFULLY"
echo "============================================================"
