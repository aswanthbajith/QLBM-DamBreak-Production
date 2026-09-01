# PHASE 10 IBM QUANTUM HARDWARE SETUP & AUTHENTICATION GUIDE (STAGE 10.6)

**Auditor Role**: Quantum Hardware Engineer  
**Date**: 2026-08-19  
**Status**: Authentication Safety Interlock Active (`DRY_RUN = True`)  

---

## 1. Zero-Exposure Authentication Instructions
To execute the validated demonstration circuits on physical IBM Quantum QPUs without hardcoding API keys or committing tokens to version control:

### Step 1: Install IBM Quantum Runtime
```bash
pip install qiskit-ibm-runtime
```

### Step 2: Save Credentials Securely to OS Keyring
Run in your private terminal:
```bash
python3 -c "from qiskit_ibm_runtime import QiskitRuntimeService; QiskitRuntimeService.save_account(channel='ibm_quantum', token='YOUR_IBM_API_TOKEN_HERE', overwrite=True)"
```

### Step 3: Verify Connection
```bash
python3 -c "from qiskit_ibm_runtime import QiskitRuntimeService; service = QiskitRuntimeService(); print('Connected. Available Backends:', [b.name for b in service.backends()])"
```

### Step 4: Submit Hardware Jobs Safely
Execute the controller with `DRY_RUN=False`:
```bash
python3 -c "from quantum_hardware.run_hardware import run_hardware_job; run_hardware_job(backend_name='ibm_brisbane', shots=1000)"
```

---

## 2. Safety Interlock Policy
* **`DRY_RUN = True`** is hardcoded by default in `quantum_hardware/run_hardware.py` and `run_phase10_validation.sh`.
* Zero unauthorized quantum compute credits will be consumed during automated validation passes.
