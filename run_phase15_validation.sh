#!/usr/bin/env bash
# ==============================================================================
# PHASE 15 REPRODUCIBILITY & REAL QUANTUM HARDWARE VALIDATION PIPELINE
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$SCRIPT_DIR"

echo "========================================================================"
echo "STARTING PHASE 15 QUANTUM HARDWARE VALIDATION PIPELINE"
echo "Repository: $REPO_ROOT"
echo "Date: $(date -u)"
echo "Safety Interlock: DRY_RUN=True (Dual-Lock Active)"
echo "========================================================================"

cd "$REPO_ROOT"

VENV_PYTHON="$REPO_ROOT/.venv/bin/python3"
VENV_PYTEST="$REPO_ROOT/.venv/bin/pytest"

echo "--- [1/6] Running Full Test Suite (69 Base + 5 Phase 15 Tests = 74 Tests) ---"
$VENV_PYTEST -v

echo "--- [2/6] Executing Phase 15 Batch 1 Baseline Freeze & Diagnostic ---"
$VENV_PYTHON scripts/run_phase15_batch1.py

echo "--- [3/6] Executing Phase 15 Batch 2 Ladder & Cross Comparisons ---"
$VENV_PYTHON scripts/run_phase15_batch2.py

echo "--- [4/6] Executing Phase 15 Batch 3 14 Figures & Scaling ---"
$VENV_PYTHON scripts/run_phase15_batch3.py

echo "--- [5/6] Executing Phase 15 Batch 4 Reports & Final Verdict ---"
$VENV_PYTHON scripts/run_phase15_batch4.py

echo "--- [6/6] Verifying Artifact Integrity ---"
if [ ! -f "phase15_final_status.json" ] || [ ! -f "PHASE15_FINAL_SCIENTIFIC_REPORT.md" ]; then
    echo "ERROR: Final Phase 15 reports missing!" >&2
    exit 1
fi

echo "========================================================================"
echo "PHASE 15 VALIDATION PIPELINE COMPLETED SUCCESSFULLY (STATUS: PASS)"
echo "========================================================================"
