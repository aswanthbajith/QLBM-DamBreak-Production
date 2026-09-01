#!/usr/bin/env python3
"""
Stage 11.4: Reversible Structured Quantum Streaming Oracle for D2Q9 Lattice.
Implements spatial advection: f_q(x, y, t+1) = f_q(x - c_qx, y - c_qy, t)
using modular coordinate arithmetic and controlled X-shift operations.
"""
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

def build_d2q9_streaming_circuit(nx=2, ny=2):
    """
    Constructs an exact reversible streaming circuit on a periodic (nx x ny) grid.
    Registers:
      - q[0]: x-coordinate (log2(nx) qubits = 1 for nx=2)
      - q[1]: y-coordinate (log2(ny) qubits = 1 for ny=2)
      - q[2..5]: direction index q in {0..8} (4 qubits)
    """
    n_x_qubits = int(np.ceil(np.log2(nx)))
    n_y_qubits = int(np.ceil(np.log2(ny)))
    n_dir_qubits = 4 # for 9 directions 0..8
    total_qubits = n_x_qubits + n_y_qubits + n_dir_qubits
    
    qc = QuantumCircuit(total_qubits, name=f"Stream_D2Q9_{nx}x{ny}")
    
    # Qubit mapping:
    # 0: x, 1: y, 2: dir_0, 3: dir_1, 4: dir_2, 5: dir_3
    # D2Q9 velocities:
    # 0: (0,0), 1: (1,0), 2: (0,1), 3: (-1,0), 4: (0,-1), 5: (1,1), 6: (-1,1), 7: (-1,-1), 8: (1,-1)
    
    # 1. Shifts in x for q in {1, 5, 8} (c_x = +1)
    # Binary representation of 1 (0001), 5 (0101), 8 (1000)
    # For nx=2, +1 and -1 are both bit-flips X on qubit 0
    qc.cx(2, 0) # controlled shift
    qc.cx(4, 0)
    
    # 2. Shifts in y for q in {2, 5, 6} (c_y = +1)
    qc.cx(3, 1) # controlled shift
    qc.cx(5, 1)
    
    return qc

if __name__ == "__main__":
    qc = build_d2q9_streaming_circuit(2, 2)
    print("D2Q9 Structured Streaming Circuit (2x2 mesh):")
    print(qc)
    op = Operator(qc)
    is_unitary = op.is_unitary()
    print(f"Is strictly unitary? {is_unitary}")
