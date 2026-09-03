"""
Phase F33: Quantum State Preparation Engine.

Constructs explicit Qiskit quantum circuits to initialize the two-phase dam-break state:
- Liquid column on left (x=0) with alpha=1.0, rho=1.0
- Gas phase on right (x=1) with alpha=0.0, rho=0.1
- Zero initial velocity u = (0, 0)
"""

from typing import Dict, Any, List, Tuple
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister


class F33StatePreparation:
    """
    Synthesizes explicit gate-level state preparation circuits.
    """

    @staticmethod
    def build_dam_break_initial_state(
        nx: int = 2,
        ny: int = 2,
        bits_per_field: int = 4,
    ) -> Tuple[QuantumCircuit, Dict[str, Any]]:
        """
        Creates a gate-level quantum circuit initializing 2x2 dam-break populations.
        """
        # For 2x2 grid: 4 nodes
        # Each node has liquid state (x=0) or gas state (x=1)
        q_sys = QuantumRegister(nx * ny * bits_per_field, name="q_sys")
        circ = QuantumCircuit(q_sys, name="DamBreakStatePrep")

        # Set bit patterns via Pauli-X gates for computational basis encoding
        # Liquid nodes at x=0: high density pattern (e.g. 1100 in 4 bits)
        # Gas nodes at x=1: low density pattern (e.g. 0010 in 4 bits)
        gate_1q_count = 0
        gate_2q_count = 0

        for y in range(ny):
            for x in range(nx):
                node_idx = y * nx + x
                base_qubit = node_idx * bits_per_field

                if x == 0:
                    # Liquid: binary 12 (1100)
                    circ.x(q_sys[base_qubit + 2])
                    circ.x(q_sys[base_qubit + 3])
                    gate_1q_count += 2
                else:
                    # Gas: binary 2 (0010)
                    circ.x(q_sys[base_qubit + 1])
                    gate_1q_count += 1

        meta = {
            "num_qubits": circ.num_qubits,
            "depth": circ.depth(),
            "1q_gates": gate_1q_count,
            "2q_gates": gate_2q_count,
            "total_gates": gate_1q_count + gate_2q_count,
            "fidelity": 1.0,
        }
        return circ, meta
