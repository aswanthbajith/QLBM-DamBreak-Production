#!/usr/bin/env bash
# ==============================================================================
# PHASE 11 COMPLETE REPRODUCIBILITY & STRUCTURED ORACLE VALIDATION PIPELINE
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$SCRIPT_DIR"

echo "========================================================================"
echo "STARTING PHASE 11 STRUCTURED QUANTUM ORACLE VALIDATION PIPELINE"
echo "Repository: $REPO_ROOT"
echo "Date: $(date -u)"
echo "Safety Interlock: DRY_RUN=True (Zero unauthorized credits consumed)"
echo "========================================================================"

cd "$REPO_ROOT"

VENV_PYTHON="$REPO_ROOT/.venv/bin/python3"
VENV_PYTEST="$REPO_ROOT/.venv/bin/pytest"

echo "--- [1/6] Running Full Test Suite (52 Base + 4 Phase 11 Tests = 56 Tests) ---"
$VENV_PYTEST -v

echo "--- [2/6] Executing Phase 11 Batch 1 Inventory & Mapping ---"
$VENV_PYTHON scripts/run_phase11_batch1.py

echo "--- [3/6] Executing Phase 11 Batch 2 Structured Oracles ---"
$VENV_PYTHON scripts/run_phase11_batch2.py

echo "--- [4/6] Executing Phase 11 Batch 3 Simulations & Scaling ---"
$VENV_PYTHON scripts/run_phase11_batch3.py

echo "--- [5/6] Executing Phase 11 Batch 4 Figures, Tables & Reports ---"
$VENV_PYTHON scripts/run_phase11_batch4.py

echo "--- [6/6] Verifying Artifact Integrity ---"
if [ ! -f "phase11_final_status.json" ] || [ ! -f "PHASE11_FINAL_SCIENTIFIC_REPORT.md" ]; then
    echo "ERROR: Final Phase 11 reports missing!" >&2
    exit 1
fi

echo "========================================================================"
echo "PHASE 11 VALIDATION PIPELINE COMPLETED SUCCESSFULLY (STATUS: PASS)"
echo "========================================================================"
