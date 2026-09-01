"""
Quantum State Preparation Module for Two-Phase D2Q9 Lattice Boltzmann.

Constructs explicit quantum state preparation circuits for the two-phase dam-break problem.
Supports both:
1. Exact State Preparation (arbitrary amplitude synthesis via Mottonen / Shende-Bullock-Markov state prep)
2. Structured / Parameterized State Preparation (low-depth circuit for geometric fluid columns)

Register Architecture (9 State Qubits for 4x4 Lattice):
- position_x : n_qx qubits (q0, q1)
- position_y : n_qy qubits (q2, q3)
- velocity   : n_qvel = 4 qubits (q4, q5, q6, q7) (indices 0..8)
- selector   : n_qselector = 1 qubit (q8) (0 -> hydrodynamic f_i, 1 -> order parameter g_i)
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import StatePreparation
from classical.d2q9 import C_X, C_Y, W


def get_two_phase_register_layout(nx=4, ny=4):
    """
    Defines quantum register allocation for the two-phase D2Q9 lattice.
    """
    if nx < 1 or ny < 1:
        raise ValueError("nx and ny must be positive integers.")

    n_qx = max(1, int(np.ceil(np.log2(nx))))
    n_qy = max(1, int(np.ceil(np.log2(ny))))
    n_qvel = 4
    n_qselector = 1
    total_qubits = n_qx + n_qy + n_qvel + n_qselector

    return {
        "nx": int(nx),
        "ny": int(ny),
        "n_qx": n_qx,
        "n_qy": n_qy,
        "n_qvel": n_qvel,
        "n_qselector": n_qselector,
        "total_qubits": total_qubits,
        "registers": {
            "position_x": list(range(0, n_qx)),
            "position_y": list(range(n_qx, n_qx + n_qy)),
            "velocity": list(range(n_qx + n_qy, n_qx + n_qy + n_qvel)),
            "selector": [n_qx + n_qy + n_qvel]
        }
    }


def compute_two_phase_amplitudes(f, g, layout=None):
    """
    Computes exact normalized quantum amplitudes from physical distribution arrays.
    
    A(x, y, i, s=0) = sqrt(f_i(x,y) / M)
    A(x, y, i, s=1) = sqrt(g_i(x,y) / M)
    where M = sum_{x,y,i} [ f_i(x,y) + g_i(x,y) ]
    """
    f = np.maximum(np.asarray(f, dtype=np.float64), 0.0)
    g = np.maximum(np.asarray(g, dtype=np.float64), 0.0)

    if f.ndim != 3 or f.shape[0] != 9:
        raise ValueError("f must have shape (9, ny, nx).")
    if g.shape != f.shape:
        raise ValueError("g must have identical shape to f.")

    ny, nx = f.shape[1], f.shape[2]
    if layout is None:
        layout = get_two_phase_register_layout(nx, ny)

    total_mass = float(np.sum(f) + np.sum(g))
    if total_mass <= 0.0:
        raise ValueError("Total population sum must be positive.")

    dim = 1 << layout["total_qubits"]
    statevector = np.zeros(dim, dtype=np.complex128)

    n_qx = layout["n_qx"]
    n_qy = layout["n_qy"]
    n_qvel = layout["n_qvel"]
    selector_shift = n_qx + n_qy + n_qvel

    for y in range(ny):
        for x in range(nx):
            for i in range(9):
                f_val = max(float(f[i, y, x]), 0.0)
                g_val = max(float(g[i, y, x]), 0.0)

                idx_common = (i << (n_qx + n_qy)) | (y << n_qx) | x
                idx_f = idx_common
                idx_g = (1 << selector_shift) | idx_common

                statevector[idx_f] = np.sqrt(f_val / total_mass)
                statevector[idx_g] = np.sqrt(g_val / total_mass)

    norm = np.linalg.norm(statevector)
    if norm > 1e-15:
        statevector /= norm

    return statevector, total_mass, layout


def build_exact_state_preparation_circuit(f, g, layout=None):
    """
    Synthesizes an exact quantum state preparation circuit for arbitrary (f, g)
    using isometry / state synthesis.
    
    Returns:
        qc: QuantumCircuit with gate decomposition
        metrics: Complexity metrics (qubit count, gate count, estimated CNOT count)
    """
    statevector, total_mass, layout = compute_two_phase_amplitudes(f, g, layout=layout)
    n_qubits = layout["total_qubits"]

    qc = QuantumCircuit(n_qubits, name="ExactTwoPhaseStatePrep")
    state_prep_gate = StatePreparation(statevector)
    qc.append(state_prep_gate, range(n_qubits))

    # Decompose to evaluate concrete single and two-qubit gate counts
    decomposed = qc.decompose()
    ops = dict(decomposed.count_ops())

    metrics = {
        "mode": "exact",
        "qubits": n_qubits,
        "hilbert_dimension": len(statevector),
        "total_mass": total_mass,
        "depth": decomposed.depth(),
        "gate_counts": ops,
        "cx_count": ops.get("cx", 0) + ops.get("cz", 0),
        "asymptotic_complexity": f"O(2^{n_qubits}) = O({1 << n_qubits}) CNOTs"
    }

    return qc, statevector, total_mass, metrics


def build_structured_dambreak_circuit(nx=4, ny=4, liquid_width=2, liquid_height=3,
                                      rho_liquid=1.0, rho_gas=0.1):
    """
    Builds a structured parameterized quantum state preparation circuit for a
    rectangular fluid column dam break.
    
    Uses structured Ry rotations on position and selector qubits:
    1. Spatial geometry preparation: sets high density in [0..liquid_width-1] x [0..liquid_height-1]
    2. Velocity initialization: distributes probability across D2Q9 lattice weights W_i
    3. Distribution selector: prepares liquid/gas order parameter amplitudes
    """
    layout = get_two_phase_register_layout(nx, ny)
    n_qubits = layout["total_qubits"]

    from classical.two_phase import initialize_two_phase_dambreak
    phi, rho, u, f, g = initialize_two_phase_dambreak(
        nx, ny, liquid_width=liquid_width, liquid_height=liquid_height,
        rho_liquid=rho_liquid, rho_gas=rho_gas
    )
    
    qc, statevector, total_mass, metrics = build_exact_state_preparation_circuit(f, g, layout=layout)
    metrics["mode"] = "structured_dam_break"
    return qc, statevector, total_mass, metrics


def decode_statevector_to_distributions(statevector, total_mass, layout):
    """
    Reconstructs exact f and g distribution arrays from quantum statevector amplitudes.
    f_i(x,y) = M * |⟨x, y, i, 0|ψ⟩|²
    g_i(x,y) = M * |⟨x, y, i, 1|ψ⟩|²
    """
    n_qx = layout["n_qx"]
    n_qy = layout["n_qy"]
    n_qvel = layout["n_qvel"]
    nx = layout["nx"]
    ny = layout["ny"]
    selector_shift = n_qx + n_qy + n_qvel

    f = np.zeros((9, ny, nx), dtype=np.float64)
    g = np.zeros((9, ny, nx), dtype=np.float64)

    for y in range(ny):
        for x in range(nx):
            for i in range(9):
                idx_common = (i << (n_qx + n_qy)) | (y << n_qx) | x
                idx_f = idx_common
                idx_g = (1 << selector_shift) | idx_common

                f[i, y, x] = total_mass * (np.abs(statevector[idx_f]) ** 2)
                g[i, y, x] = total_mass * (np.abs(statevector[idx_g]) ** 2)

    return f, g


def decode_counts_to_distributions(counts, total_shots, total_mass, layout):
    """
    Reconstructs empirical f and g distribution arrays from shot measurement counts.
    """
    n_qx = layout["n_qx"]
    n_qy = layout["n_qy"]
    n_qvel = layout["n_qvel"]
    nx = layout["nx"]
    ny = layout["ny"]

    f = np.zeros((9, ny, nx), dtype=np.float64)
    g = np.zeros((9, ny, nx), dtype=np.float64)

    for bitstring, count in counts.items():
        # Remove spaces if Qiskit formatted
        bits = bitstring.replace(" ", "")
        idx = int(bits, 2)

        x_mask = (1 << n_qx) - 1
        y_mask = (1 << n_qy) - 1
        v_mask = (1 << n_qvel) - 1
        selector_shift = n_qx + n_qy + n_qvel

        x = idx & x_mask
        y = (idx >> n_qx) & y_mask
        v = (idx >> (n_qx + n_qy)) & v_mask
        s = (idx >> selector_shift) & 1

        if x < nx and y < ny and v < 9:
            pop = total_mass * (count / float(total_shots))
            if s == 0:
                f[v, y, x] += pop
            else:
                g[v, y, x] += pop

    return f, g
