# FINAL REPRODUCIBILITY GUIDE
## Step-by-Step Instructions to Reproduce All Results in a Fresh Environment

---

## 1. System Requirements & Environment

- **Operating System**: Linux (Ubuntu 22.04+ / Debian 12+) or macOS
- **Python Version**: Python 3.10, 3.11, 3.12, or 3.14
- **Core Library Versions**:
  - `qiskit >= 2.5.2`
  - `qiskit-aer >= 0.17.2`
  - `qiskit-ibm-runtime >= 0.45.1`
  - `numpy >= 2.2.6`
  - `scipy >= 1.15.3`
  - `pytest >= 9.1.1`

---

## 2. Setup Procedure

```bash
# 1. Clone repository
git clone git@github.com:aswanthbajith/QLBM-DamBreak-Production.git
cd QLBM-DamBreak-Production

# 2. Switch to final integration branch
git checkout consolidation/final-working-prototype

# 3. Create virtual environment & install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 3. Verification & Execution Commands

### Step 1: Verify Frozen Baseline SHA-256 Checksum
```bash
sha256sum quantum/level6b_hybrid_solver.py
# Expected Output:
# 2a306f5a413945adc1acd10f3f63340c3d3617e4ef1c94981a92e8ebad8742c8  quantum/level6b_hybrid_solver.py
```

### Step 2: Run Automated Regression Test Suite (348 Tests)
```bash
./.venv/bin/pytest -q tests/
# Expected Output: 348 passed in ~450s
```

### Step 3: Run Primary Integrated Prototype Suite
```bash
# Mode A: Ideal Simulator
./.venv/bin/python scripts/run_phase_f38_ideal.py

# Mode B: Noisy Hardware Emulation (127-Qubit Heavy-Hex FakeSherbrooke)
./.venv/bin/python scripts/run_phase_f38_noisy.py

# Mode C: Master Multi-Tier Validation
./.venv/bin/python scripts/run_phase_f38_validation.py
```

### Step 4: Run Scalable Fault-Tolerant Reversible Architecture
```bash
./.venv/bin/python scripts/run_phase_f29_validation.py
./.venv/bin/python scripts/run_phase_f31_reduction.py
```
