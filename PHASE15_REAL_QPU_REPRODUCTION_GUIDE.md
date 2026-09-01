# PHASE 15 REAL QPU REPRODUCTION GUIDE & EXECUTION PROTOCOL

**Status**: Verified Execution Protocol  
**Date**: 2026-08-19  

---

## 1. Single Action Required from Researcher for Real Hardware Execution
To submit real jobs to IBM Quantum:
1. Save your IBM Quantum API token:
   ```bash
   python3 -c "from qiskit_ibm_runtime import QiskitRuntimeService; QiskitRuntimeService.save_account(channel='ibm_quantum_platform', token='<YOUR_TOKEN>', overwrite=True)"
   ```
2. Run validation with explicit hardware flags:
   ```bash
   QLBM_ENABLE_REAL_QPU=1 QLBM_CONFIRM_REAL_QPU=YES ./run_phase15_validation.sh
   ```
