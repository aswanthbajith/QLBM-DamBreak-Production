#!/usr/bin/env bash
# ==============================================================================
# PHASE 9 QUANTUM HARDWARE READINESS & INTEGRITY VALIDATION PIPELINE
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$SCRIPT_DIR"

echo "========================================================================"
echo "STARTING PHASE 9 QUANTUM HARDWARE VALIDATION PIPELINE"
echo "Repository: $REPO_ROOT"
echo "Date: $(date -u)"
echo "========================================================================"

cd "$REPO_ROOT"

VENV_PYTHON="$REPO_ROOT/.venv/bin/python3"
VENV_PYTEST="$REPO_ROOT/.venv/bin/pytest"

echo "--- [1/6] Running Phase 5-8 Automated Test Suite (52 tests) ---"
$VENV_PYTEST -v

echo "--- [2/6] Executing Phase 9 Batch 1 Discovery ---"
$VENV_PYTHON scripts/run_phase9_batch1.py

echo "--- [3/6] Executing Phase 9 Batch 2 Transpilation Benchmarks ---"
$VENV_PYTHON scripts/run_phase9_batch2.py

echo "--- [4/6] Executing Phase 9 Batch 3 Hardware Demonstration Suite ---"
$VENV_PYTHON scripts/run_phase9_batch3.py

echo "--- [5/6] Running and Validating All quantum_hardware Demonstration Scripts ---"
$VENV_PYTHON quantum_hardware/01_block_encoding_demo.py
$VENV_PYTHON quantum_hardware/02_qsvt_demo.py
$VENV_PYTHON quantum_hardware/03_measurement_demo.py
$VENV_PYTHON quantum_hardware/04_small_qlbm_state.py
$VENV_PYTHON quantum_hardware/05_qae_scalar_demo.py
$VENV_PYTHON quantum_hardware/transpile_hardware.py
$VENV_PYTHON quantum_hardware/run_hardware.py
$VENV_PYTHON quantum_hardware/validate_results.py

echo "--- [6/6] Verifying Phase 9 Artifact Integrity ---"
if [ ! -f "PHASE9_FINAL_SCIENTIFIC_REPORT.md" ] || [ ! -f "PHASE9_FINAL_VERDICT.md" ]; then
    echo "ERROR: Final Phase 9 reports missing!" >&2
    exit 1
fi

echo "========================================================================"
echo "PHASE 9 VALIDATION PIPELINE COMPLETED SUCCESSFULLY (STATUS: PASS)"
echo "========================================================================"
