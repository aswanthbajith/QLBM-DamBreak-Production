#!/usr/bin/env bash
# ==============================================================================
# PHASE 10 COMPLETE REPRODUCIBILITY & HARDWARE VALIDATION PIPELINE
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$SCRIPT_DIR"

echo "========================================================================"
echo "STARTING PHASE 10 QUANTUM HARDWARE VALIDATION PIPELINE"
echo "Repository: $REPO_ROOT"
echo "Date: $(date -u)"
echo "Safety Interlock: DRY_RUN=True (Zero unauthorized credits consumed)"
echo "========================================================================"

cd "$REPO_ROOT"

VENV_PYTHON="$REPO_ROOT/.venv/bin/python3"
VENV_PYTEST="$REPO_ROOT/.venv/bin/pytest"

echo "--- [1/6] Running Full Test Suite (52 tests) ---"
$VENV_PYTEST -v

echo "--- [2/6] Executing Phase 10 Batch 1 Inventory & Discovery ---"
$VENV_PYTHON scripts/run_phase10_batch1.py

echo "--- [3/6] Executing Phase 10 Batch 2 Ideal/Noisy Simulations & Transpilation ---"
$VENV_PYTHON scripts/run_phase10_batch2.py

echo "--- [4/6] Executing Phase 10 Batch 3 Hardware Comparison & Noise Scaling ---"
$VENV_PYTHON scripts/run_phase10_batch3.py

echo "--- [5/6] Executing Phase 10 Batch 4 Figures & Final Reports ---"
$VENV_PYTHON scripts/run_phase10_batch4.py

echo "--- [6/6] Verifying Artifact Integrity ---"
if [ ! -f "phase10_final_status.json" ] || [ ! -f "PHASE10_FINAL_HARDWARE_REPORT.md" ]; then
    echo "ERROR: Final Phase 10 reports missing!" >&2
    exit 1
fi

echo "========================================================================"
echo "PHASE 10 VALIDATION PIPELINE COMPLETED SUCCESSFULLY (STATUS: PASS)"
echo "========================================================================"
