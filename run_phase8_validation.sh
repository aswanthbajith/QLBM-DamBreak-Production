#!/usr/bin/env bash
# ==============================================================================
# PHASE 8 COMPLETE REPRODUCIBILITY & VALIDATION PIPELINE
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$SCRIPT_DIR"

echo "========================================================================"
echo "STARTING PHASE 8 SCIENTIFIC REPRODUCIBILITY PIPELINE"
echo "Repository: $REPO_ROOT"
echo "Date: $(date -u)"
echo "========================================================================"

cd "$REPO_ROOT"

VENV_PYTHON="$REPO_ROOT/.venv/bin/python3"
VENV_PYTEST="$REPO_ROOT/.venv/bin/pytest"

if [ ! -f "$VENV_PYTHON" ]; then
    echo "ERROR: Virtual environment not found at $REPO_ROOT/.venv" >&2
    exit 1
fi

echo "--- [1/6] Running Full Automated Test Suite (pytest) ---"
$VENV_PYTEST -v

echo "--- [2/6] Executing Phase 8 Batch 2 Benchmarks (Classical, Carleman, Block, QSVT, Condition) ---"
$VENV_PYTHON scripts/run_phase8_batch2.py

echo "--- [3/6] Executing Phase 8 Batch 3 Benchmarks (Resources, Advantage, QAE, FT, Error Budget) ---"
$VENV_PYTHON scripts/run_phase8_batch3.py

echo "--- [4/6] Executing Phase 8 Batch 4 Audits (Figures, Tables) ---"
$VENV_PYTHON scripts/run_phase8_batch4.py

echo "--- [5/6] Executing Phase 8 Batch 5 Package Generation ---"
$VENV_PYTHON scripts/run_phase8_batch5.py

echo "--- [6/6] Verifying Artifact Integrity ---"
if [ ! -f "PHASE8_FINAL_SCIENTIFIC_VERDICT.md" ] || [ ! -f "phase8_final_status.json" ]; then
    echo "ERROR: Final Phase 8 reports missing!" >&2
    exit 1
fi

echo "========================================================================"
echo "PHASE 8 VALIDATION PIPELINE COMPLETED SUCCESSFULLY (STATUS: PASS)"
echo "========================================================================"
