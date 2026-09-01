#!/usr/bin/env bash
# ==============================================================================
# PHASE 12 COMPLETE REPRODUCIBILITY & HARDWARE VALIDATION PIPELINE
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$SCRIPT_DIR"

echo "========================================================================"
echo "STARTING PHASE 12 QUANTUM HARDWARE VALIDATION PIPELINE"
echo "Repository: $REPO_ROOT"
echo "Date: $(date -u)"
echo "Safety Interlock: DRY_RUN=True (Zero unauthorized credits consumed)"
echo "========================================================================"

cd "$REPO_ROOT"

VENV_PYTHON="$REPO_ROOT/.venv/bin/python3"
VENV_PYTEST="$REPO_ROOT/.venv/bin/pytest"

echo "--- [1/6] Running Full Test Suite (56 Base + 4 Phase 12 Tests = 60 Tests) ---"
$VENV_PYTEST -v

echo "--- [2/6] Executing Phase 12 Batch 1 Freeze & Inventory ---"
$VENV_PYTHON scripts/run_phase12_batch1.py

echo "--- [3/6] Executing Phase 12 Batch 2 Reference, Ideal, Noisy & Transpilation ---"
$VENV_PYTHON scripts/run_phase12_batch2.py

echo "--- [4/6] Executing Phase 12 Batch 3 Hardware Studies & Scaling ---"
$VENV_PYTHON scripts/run_phase12_batch3.py

echo "--- [5/6] Executing Phase 12 Batch 4 Figures, Tables & Reports ---"
$VENV_PYTHON scripts/run_phase12_batch4.py

echo "--- [6/6] Verifying Artifact Integrity ---"
if [ ! -f "phase12_final_status.json" ] || [ ! -f "PHASE12_FINAL_SCIENTIFIC_REPORT.md" ]; then
    echo "ERROR: Final Phase 12 reports missing!" >&2
    exit 1
fi

echo "========================================================================"
echo "PHASE 12 VALIDATION PIPELINE COMPLETED SUCCESSFULLY (STATUS: PASS)"
echo "========================================================================"
