# IBM QUANTUM CLOUD ACCESS & SECURE AUTHENTICATION GUIDE
## Step-by-Step Configuration for Real-QPU Job Execution (Qiskit Runtime 0.49.0)

**Document**: IBM Access Guide  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Date**: September 2026  

---

## 1. Prerequisites & Account Type

To execute quantum circuits on physical IBM Quantum processors:
1. An active account at [IBM Quantum Platform](https://quantum.ibm.com/).
2. An API token retrieved from your IBM Quantum dashboard.
3. Installed runtime stack: `qiskit >= 2.0.0` and `qiskit-ibm-runtime >= 0.49.0` (already installed in `.venv`).

---

## 2. Secure Local Credential Configuration

Never commit API tokens to Git. Use either of the following two secure methods:

### Method A: Permanent Saved Account (Recommended)
Run the following python one-liner in your terminal (replace `<YOUR_API_TOKEN>` with your actual token):

```bash
./.venv/bin/python -c "
from qiskit_ibm_runtime import QiskitRuntimeService
QiskitRuntimeService.save_account(
    channel='ibm_quantum',
    token='<YOUR_API_TOKEN>',
    overwrite=True
)
print('IBM Quantum account securely saved to ~/.qiskit/qiskit-ibm.json')
"
```

### Method B: Environment Variable (Session-Only)
Export the token in your active terminal session:

```bash
export QISKIT_IBM_TOKEN="<YOUR_API_TOKEN>"
```

---

## 3. Verifying Authentication & Discovering Real Backends

Verify that your credentials are authenticated and discover real physical backends without displaying your secret:

```bash
./.venv/bin/python scripts/run_phase_f37_discovery.py
```

Expected output upon successful authentication:
```text
Authentication Status: AUTHENTICATED
Provider Accessible: True
--- Discovered Hardware Topologies ---
Backend: ibm_sherbrooke | Qubits: 127 | Status: ONLINE | Type: REAL HARDWARE
Backend: ibm_brisbane   | Qubits: 127 | Status: ONLINE | Type: REAL HARDWARE
```

---

## 4. Executing the Real-QPU Dam-Break Experiment

Once authenticated, dispatch the complete $2\times 2, T=1$ quantum two-phase dam-break experiment using the double opt-in safety flags:

```bash
QLBM_ENABLE_REAL_QPU=1 QLBM_CONFIRM_REAL_QPU=YES ./.venv/bin/python scripts/run_phase_f37_qpu.py
```

Results and raw counts will automatically be serialized to `results/f37/`.
