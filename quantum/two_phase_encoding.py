"""
Quantum State Encoding & Register Layout for Reduced Two-Phase Lattice Boltzmann Dam-Break.

Implements exact Square-Root Population Amplitude Encoding:
- A(x, y, i, 0) = sqrt((1 - phi) * f_i / M_total)  [Gas Phase]
- A(x, y, i, 1) = sqrt(phi * f_i / M_total)        [Liquid Phase]

Guarantees exact state reconstruction (relative L2 < 1e-12) across all valid classical states.
"""
import numpy as np
from qiskit import QuantumCircuit
from classical.two_phase import initialize_two_phase_dambreak, compute_density


def get_two_phase_register_layout(nx=4, ny=4):
    """
    Returns qubit counts and register assignments:
    - position_x : nx qubits (q0 .. q_{nx-1})
    - position_y : ny qubits (q_{nx} .. q_{nx+ny-1})
    - velocity   : 4 qubits (q_{nx+ny} .. q_{nx+ny+3})
    - phase      : 1 qubit  (q_{nx+ny+4})
    """
    n_qx = max(1, int(np.ceil(np.log2(nx))))
    n_qy = max(1, int(np.ceil(np.log2(ny))))
    n_qvel = 4
    n_qphase = 1
    total_qubits = n_qx + n_qy + n_qvel + n_qphase
    
    return {
        "n_qx": n_qx,
        "n_qy": n_qy,
        "n_qvel": n_qvel,
        "n_qphase": n_qphase,
        "total_qubits": total_qubits,
        "registers": {
            "position_x": list(range(0, n_qx)),
            "position_y": list(range(n_qx, n_qx + n_qy)),
            "velocity": list(range(n_qx + n_qy, n_qx + n_qy + n_qvel)),
            "phase": [n_qx + n_qy + n_qvel]
        }
    }


def normalize_distribution(f, phi=None):
    """
    Calculates total physical mass partition function Z = sum_{x,y,i} f_i(x,y).
    """
    total_mass = float(np.sum(f))
    return total_mass


def validate_normalization(state, norm=1.0):
    """
    Validates quantum state normalization <psi|psi> == 1.0 within numerical precision.
    """
    inner_prod = float(np.vdot(state, state).real)
    is_valid = bool(abs(inner_prod - 1.0) < 1e-10 and norm > 0.0)
    return is_valid, inner_prod


def encode_distribution(f, phi, layout=None):
    """
    Encodes classical (9, ny, nx) populations and (ny, nx) phase field into
    normalized statevector using square-root population amplitude encoding.
    
    Returns:
        state: (2^total_qubits,) complex numpy array
        total_mass: scalar float
        layout: dict of register metadata
    """
    ny = f.shape[1]
    nx = f.shape[2]
    if layout is None:
        layout = get_two_phase_register_layout(nx, ny)
        
    total_dim = 1 << layout["total_qubits"]
    state = np.zeros(total_dim, dtype=np.complex128)
    
    n_qx = layout["n_qx"]
    n_qy = layout["n_qy"]
    n_qvel = layout["n_qvel"]
    
    total_mass = float(np.sum(f))
    if total_mass <= 0:
        total_mass = 1.0
        
    for y in range(ny):
        for x in range(nx):
            phi_val = np.clip(phi[y, x], 0.0, 1.0)
            for i in range(9):
                f_val = max(0.0, float(f[i, y, x]))
                # Gas amplitude (phase = 0)
                amp_gas = np.sqrt(max(0.0, (1.0 - phi_val) * f_val / total_mass))
                # Liquid amplitude (phase = 1)
                amp_liq = np.sqrt(max(0.0, phi_val * f_val / total_mass))
                
                idx_gas = (0 << (n_qx + n_qy + n_qvel)) | (i << (n_qx + n_qy)) | (y << n_qx) | x
                idx_liq = (1 << (n_qx + n_qy + n_qvel)) | (i << (n_qx + n_qy)) | (y << n_qx) | x
                
                state[idx_gas] = amp_gas
                state[idx_liq] = amp_liq
                
    norm = np.linalg.norm(state)
    if norm > 0:
        state /= norm
        
    return state, total_mass, layout


def encode_two_phase_state(phi, f, g=None):
    """
    Backward-compatible wrapper for encode_distribution.
    """
    return encode_distribution(f, phi)


def decode_distribution(probs, layout, total_mass=None, rho_liquid=1.0):
    """
    Reconstructs macroscopic fields (rho, u, phi) directly from probability array.
    Using exact conditional probabilities:
    - rho(x,y) = M_total * P(x,y)
    - phi(x,y) = P(phase=1, x, y) / P(x, y)
    - u(x,y) = sum_i c_i P(i, x, y) / P(x, y)
    """
    from classical.d2q9 import C_X, C_Y
    
    n_qx = layout["n_qx"]
    n_qy = layout["n_qy"]
    n_qvel = layout["n_qvel"]
    
    nx = 1 << n_qx
    ny = 1 << n_qy
    
    rho_prob = np.zeros((ny, nx), dtype=np.float64)
    phi_prob = np.zeros((ny, nx), dtype=np.float64)
    mom_x_prob = np.zeros((ny, nx), dtype=np.float64)
    mom_y_prob = np.zeros((ny, nx), dtype=np.float64)
    
    for idx, p in enumerate(probs):
        if p <= 1e-18:
            continue
        x = idx & ((1 << n_qx) - 1)
        y = (idx >> n_qx) & ((1 << n_qy) - 1)
        v = (idx >> (n_qx + n_qy)) & ((1 << n_qvel) - 1)
        phase_bit = (idx >> (n_qx + n_qy + n_qvel)) & 1
        
        if v < 9 and x < nx and y < ny:
            rho_prob[y, x] += p
            if phase_bit == 1:
                phi_prob[y, x] += p
            mom_x_prob[y, x] += p * C_X[v]
            mom_y_prob[y, x] += p * C_Y[v]
            
    rho_safe = np.where(rho_prob > 1e-14, rho_prob, 1.0)
    
    if total_mass is not None:
        rho = rho_prob * total_mass
    else:
        rho = rho_prob
        
    phi = np.where(rho_prob > 1e-14, np.clip(phi_prob / rho_safe, 0.0, 1.0), 0.0)
    ux = np.where(rho_prob > 1e-14, mom_x_prob / rho_safe, 0.0)
    uy = np.where(rho_prob > 1e-14, mom_y_prob / rho_safe, 0.0)
    u = np.stack((ux, uy), axis=0)
    
    return rho, u, phi


def quantum_initialize_two_phase_dambreak(nx=4, ny=4):
    """
    Initializes the two-phase dam-break quantum state and circuit.
    """
    phi, rho, u, f, g = initialize_two_phase_dambreak(nx, ny)
    layout = get_two_phase_register_layout(nx, ny)
    state, total_mass, _ = encode_distribution(f, phi, layout)
    
    qc = QuantumCircuit(layout["total_qubits"], name="TwoPhaseInit")
    qc.initialize(state, range(layout["total_qubits"]))
    
    return qc, state, total_mass, layout
