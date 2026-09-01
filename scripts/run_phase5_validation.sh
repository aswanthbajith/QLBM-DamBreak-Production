#!/usr/bin/env bash
# ==============================================================================
# PHASE 5 CLEAN-ROOM REPRODUCIBILITY & VALIDATION PIPELINE
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "========================================================================"
echo "STARTING PHASE 5 SCIENTIFIC VALIDATION PIPELINE"
echo "Repository: $REPO_ROOT"
echo "Date: $(date -u)"
echo "========================================================================"

cd "$REPO_ROOT"

# 1. Environment & Python check
VENV_PYTHON="$REPO_ROOT/.venv/bin/python3"
VENV_PYTEST="$REPO_ROOT/.venv/bin/pytest"

if [ ! -f "$VENV_PYTHON" ]; then
    echo "ERROR: Virtual environment not found at $REPO_ROOT/.venv" >&2
    exit 1
fi

echo "--- [1/6] Running Full Test Suite (pytest) ---"
$VENV_PYTEST -v

echo "--- [2/6] Running Classical Two-Phase LBM Ground Truth Regression ---"
$VENV_PYTHON classical/verify_matrix_equivalence.py

echo "--- [3/6] Running Carleman Quadratic Dimension & Stability Verification ---"
$VENV_PYTHON quantum/carleman_lbm.py

echo "--- [4/6] Running Unitary Block Encoding Verification ---"
$VENV_PYTHON quantum/verify_block_encoding.py

echo "--- [5/6] Running Multi-Step QSVT End-to-End Dam-Break Simulation ---"
$VENV_PYTHON quantum/run_end_to_end_validation.py

echo "--- [6/6] Executing Adversarial Audit Suite & Generating Final JSON ---"
$VENV_PYTHON /home/aswa/.gemini/antigravity-cli/brain/8d80f195-5a44-4008-90af-7791a75a68d6/scratch/run_stage7_adversarial_audit.py

echo "========================================================================"
echo "PHASE 5 VALIDATION PIPELINE COMPLETED SUCCESSFULLY (STATUS: PASS)"
echo "========================================================================"
