#!/usr/bin/env bash
# ==============================================================================
# Validation Pipeline
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${ROOT_DIR}"

PYTHON_BIN="${ROOT_DIR}/.venv/bin/python"

echo "============================================================"
echo "RUNNING QLBM VALIDATION BENCHMARKS"
echo "============================================================"

echo "[1/3] Running Collision Operator Validation..."
"${PYTHON_BIN}" scripts/validate_collision_operator.py

echo "[2/3] Running Operator Ablation..."
"${PYTHON_BIN}" scripts/run_operator_ablation.py

echo "[3/3] Running Shot Noise Decomposition..."
"${PYTHON_BIN}" scripts/run_shot_noise_analysis.py

echo "============================================================"
echo "ALL VALIDATIONS GENERATED IN results/validation/"
echo "============================================================"
