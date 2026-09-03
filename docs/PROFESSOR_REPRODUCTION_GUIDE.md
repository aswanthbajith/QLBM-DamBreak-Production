# PROFESSOR REPRODUCTION GUIDE
## Quick-Start Commands to Reproduce Key Quantum Dam-Break Findings

This guide provides exact terminal commands to verify the classical physical baseline, the frozen reference, the scalable quantum circuit, and the hardware execution gateway.

---

## 1. Environment Setup

```bash
git clone git@github.com:aswanthbajith/QLBM-DamBreak-Production.git
cd QLBM-DamBreak-Production

# Activate Python 3.10+ virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 2. Verify Frozen Baseline Integrity (SHA-256)

```bash
sha256sum quantum/level6b_hybrid_solver.py
# Expected output:
# 2a306f5a413945adc1acd10f3f63340c3d3617e4ef1c94981a92e8ebad8742c8  quantum/level6b_hybrid_solver.py
```

---

## 3. Run the Automated Regression Suite (336 Tests)

```bash
./.venv/bin/pytest -q tests/
# Output: 336 passed in ~450s
```

---

## 4. Run the Primary Executable Demonstrator

### Mode A: Ideal Quantum Simulation
```bash
./.venv/bin/python scripts/run_phase_f38_ideal.py
```

### Mode B: Noisy Hardware Emulation on 127-Qubit Model (FakeSherbrooke)
```bash
./.venv/bin/python scripts/run_phase_f38_noisy.py
```

### Mode C: Hardware Transpilation & Dry Run
```bash
./.venv/bin/python scripts/run_phase_f38_dryrun.py
```

### Mode D: Master Multi-Tier Validation Report
```bash
./.venv/bin/python scripts/run_phase_f38_validation.py
```

---

## 5. Verify Scalable Reversible Circuits (Phases F29–F31)

To run the scalable gate-level circuit and Three-Layer physical validation on $4\times 4, 8\times 8, 16\times 16$ meshes:

```bash
./.venv/bin/python scripts/run_phase_f29_validation.py
./.venv/bin/python scripts/run_phase_f31_validation.py
```
