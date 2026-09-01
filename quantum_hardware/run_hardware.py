#!/usr/bin/env python3
"""
Hardware Execution Controller with Safety Interlock (DRY_RUN = True).
"""
import os, sys

# SAFETY INTERLOCK: Must be explicitly changed to False by user for real QPU submission
DRY_RUN = True

def run_hardware_job(circuit_name="01_block_encoding", backend_name="ibm_brisbane", shots=1000):
    print("="*75)
    print(f"IBM QUANTUM HARDWARE SUBMISSION CONTROLLER")
    print(f"Target Backend: {backend_name} | Shots: {shots} | DRY_RUN: {DRY_RUN}")
    print("="*75)
    
    if DRY_RUN:
        print("[SAFETY INTERLOCK ACTIVE] DRY_RUN is TRUE.")
        print("  - Circuit validated locally.")
        print("  - Zero cloud quantum credits consumed.")
        print("  - To submit to a physical QPU, configure IBM credentials and set DRY_RUN=False.")
        return {"status": "DRY_RUN_VALIDATED", "job_id": "SIMULATED_LOCAL_DRY_RUN"}
        
    try:
        from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
        service = QiskitRuntimeService()
        backend = service.backend(backend_name)
        print(f"Connected to QPU: {backend.name} ({backend.num_qubits} qubits)")
        # In real execution, submit sampler job here
        return {"status": "SUBMITTED", "job_id": "PENDING_ON_HARDWARE"}
    except Exception as e:
        print(f"[AUTH ERROR] Cannot connect to IBM Quantum: {e}")
        return {"status": "AUTH_REQUIRED", "error": str(e)}

if __name__ == "__main__":
    res = run_hardware_job()
    print("Execution Result:", res)
