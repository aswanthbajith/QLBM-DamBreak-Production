"""
IBM Quantum Qiskit Runtime Service & SamplerV2 Interface with Dual-Lock Safety Gate.
"""
import os

class IBMRuntimeServiceWrapper:
    def __init__(self):
        self.enabled = os.environ.get("QLBM_ENABLE_REAL_QPU", "0") == "1"
        self.confirmed = os.environ.get("QLBM_CONFIRM_REAL_QPU", "NO") == "YES"
        self.dry_run = not (self.enabled and self.confirmed)
        
    def is_real_execution_allowed(self):
        return not self.dry_run
