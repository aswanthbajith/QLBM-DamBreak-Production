# QLBM Research Reproducibility Guide

This guide enables an independent researcher or professor to reproduce all scientific results from a clean Linux environment.

---

## 1. System Requirements

- **Operating System**: Linux (Ubuntu 20.04+, 22.04+, 24.04+, Debian 11+, or compatible Linux distribution)
- **Python Version**: Python 3.10 to Python 3.14 (Python 3.14.4 tested)
- **Hardware**: Standard x86_64 workstation (16 GB RAM recommended for multi-qubit statevector simulations)
- **Quantum Hardware**: Not required (all benchmarks run via exact statevector / Qiskit Aer simulation)

---

## 2. Environment Setup

```bash
# 1. Clone the repository
git clone https://github.com/aswanthbajith/QLBM-DamBreak-Production.git
cd QLBM-DamBreak-Production

# 2. Checkout the professor-shareable branch
git checkout professor/final-research-code

# 3. Create and activate a clean virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 4. Install exact validated dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 3. Running the Automated Test Suite

Run the full 212-test suite to verify all mathematical proofs, CPTP channels, and physics benchmarks:

```bash
pytest -q
```
*Expected Output*: `212 passed in ~350s (100% passing)`.

---

## 4. Minimal Reproducible CLI Examples

### Example A: Canonical Classical Two-Phase Reference Run
```bash
python run.py --mode classical --nx 4 --ny 4 --timesteps 2 --no-plots
```

### Example B: Direct Quantum Emulator Multi-Step Run
```bash
python run.py --mode quantum --nx 4 --ny 4 --timesteps 2 --no-plots
```

### Example C: Phase F20 CPTP BGK Channel Equivalence Master Audit
```bash
python scripts/run_phase_f20_channel_equivalence.py
```

---

## 5. Hardware Safety Interlocks

To ensure no accidental remote IBM QPU calls or cloud charges occur, execution on physical QPUs is disabled by default. If desired, hardware preflight can be verified locally:
```bash
export QLBM_ENABLE_REAL_QPU=0
export QLBM_CONFIRM_REAL_QPU=NO
python -c "from hardware.preflight import run_preflight; print(run_preflight())"
```
