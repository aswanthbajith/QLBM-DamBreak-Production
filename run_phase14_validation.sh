#!/usr/bin/env bash
# ==============================================================================
# PHASE 14 REPRODUCIBILITY & HARDWARE VALIDATION PIPELINE
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$SCRIPT_DIR"

echo "========================================================================"
echo "STARTING PHASE 14 QUANTUM HARDWARE VALIDATION PIPELINE"
echo "Repository: $REPO_ROOT"
echo "Date: $(date -u)"
echo "Safety Interlock: DRY_RUN=True (Dual-Lock Active)"
echo "========================================================================"

cd "$REPO_ROOT"

VENV_PYTHON="$REPO_ROOT/.venv/bin/python3"
VENV_PYTEST="$REPO_ROOT/.venv/bin/pytest"

echo "--- [1/6] Running Full Test Suite (64 Base + 5 Phase 14 Tests = 69 Tests) ---"
$VENV_PYTEST -v

echo "--- [2/6] Executing Phase 14 Batch 1 Baseline Freeze & Diagnostic ---"
$VENV_PYTHON scripts/run_phase14_batch1.py

echo "--- [3/6] Executing Phase 14 Batch 2 Levels 1-5 & Master Comparisons ---"
$VENV_PYTHON scripts/run_phase14_batch2.py

echo "--- [4/6] Executing Phase 14 Batch 3 12 Figures & Scaling Reports ---"
$VENV_PYTHON scripts/run_phase14_batch3.py

echo "--- [5/6] Executing Phase 14 Batch 4 Reports & Final Verdict ---"
$VENV_PYTHON scripts/run_phase14_batch4.py

echo "--- [6/6] Verifying Artifact Integrity ---"
if [ ! -f "phase14_final_status.json" ] || [ ! -f "PHASE14_FINAL_HARDWARE_REPORT.md" ]; then
    echo "ERROR: Final Phase 14 reports missing!" >&2
    exit 1
fi

echo "========================================================================"
echo "PHASE 14 VALIDATION PIPELINE COMPLETED SUCCESSFULLY (STATUS: PASS)"
echo "========================================================================"
