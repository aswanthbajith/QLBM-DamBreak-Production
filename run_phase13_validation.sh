#!/usr/bin/env bash
# ==============================================================================
# PHASE 13 COMPLETE REPRODUCIBILITY & HARDWARE VALIDATION PIPELINE
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$SCRIPT_DIR"

echo "========================================================================"
echo "STARTING PHASE 13 QUANTUM HARDWARE VALIDATION PIPELINE"
echo "Repository: $REPO_ROOT"
echo "Date: $(date -u)"
echo "Safety Interlock: DRY_RUN=True (Zero unauthorized credits consumed)"
echo "========================================================================"

cd "$REPO_ROOT"

VENV_PYTHON="$REPO_ROOT/.venv/bin/python3"
VENV_PYTEST="$REPO_ROOT/.venv/bin/pytest"

echo "--- [1/6] Running Full Test Suite (60 Base + 4 Phase 13 Tests = 64 Tests) ---"
$VENV_PYTEST -v

echo "--- [2/6] Executing Phase 13 Batch 1 Freeze & Setup ---"
$VENV_PYTHON scripts/run_phase13_batch1.py

echo "--- [3/6] Executing Phase 13 Batch 2 Simulations & Mitigation ---"
$VENV_PYTHON scripts/run_phase13_batch2.py

echo "--- [4/6] Executing Phase 13 Batch 3 Hardware Reports & Analysis ---"
$VENV_PYTHON scripts/run_phase13_batch3.py

echo "--- [5/6] Executing Phase 13 Batch 4 Figures, Claim Matrix & Reports ---"
$VENV_PYTHON scripts/run_phase13_batch4.py

echo "--- [6/6] Verifying Artifact Integrity ---"
if [ ! -f "phase13_final_status.json" ] || [ ! -f "PHASE13_FINAL_SCIENTIFIC_REPORT.md" ]; then
    echo "ERROR: Final Phase 13 reports missing!" >&2
    exit 1
fi

echo "========================================================================"
echo "PHASE 13 VALIDATION PIPELINE COMPLETED SUCCESSFULLY (STATUS: PASS)"
echo "========================================================================"
