"""
Approach C: One-Step Simplified LBM (OSSLBM) (arXiv:2603.02127).
"""
import numpy as np
from qiskit import QuantumCircuit

class ApproachCOSSLBM:
    def __init__(self, nx=2, ny=2):
        self.nx = nx
        self.ny = ny
        
    def build_one_step_circuit(self):
        """
        Direct unitary mapping for the combined collision-streaming operator.
        """
        qc = QuantumCircuit(6, name="OSSLBM_Step")
        qc.h([0, 1])
        qc.ry(0.6435, 2)
        qc.cx(2, 3)
        qc.cx(2, 0)
        qc.cx(3, 1)
        return qc
