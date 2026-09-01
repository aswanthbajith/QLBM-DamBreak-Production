"""
Quantum State Encoding for Two-Phase D2Q9 Carleman LBM.

AUTHORITATIVE LOCAL STATE:

    Psi = [f_0,...,f_8,g_0,...,g_8]^T

The final qubit is NOT a physical phase-field qubit.

It is a distribution-selector qubit:

    selector = 0 -> hydrodynamic distribution f_i
    selector = 1 -> phase/order-parameter distribution g_i

Amplitude encoding:

    A(x,y,i,0) = sqrt(f_i(x,y) / M)
    A(x,y,i,1) = sqrt(g_i(x,y) / M)

where

    M = sum_{x,y,i} [f_i(x,y) + g_i(x,y)]

Thus measurement probabilities reconstruct f and g independently:

    f_i(x,y) = M P(x,y,i,0)
    g_i(x,y) = M P(x,y,i,1)

The physical phase field is subsequently reconstructed from g:

    phi(x,y) = sum_i g_i(x,y)

This encoding is consistent with the 18-component Carleman state used
by quantum/two_phase_carleman.py.
"""

import numpy as np
from qiskit import QuantumCircuit

from classical.d2q9 import C_X, C_Y


# ---------------------------------------------------------------------------
# Register layout
# ---------------------------------------------------------------------------

def get_two_phase_register_layout(nx=4, ny=4):
    """
    Construct the quantum register layout.

    Registers:

        position_x : ceil(log2(nx)) qubits
        position_y : ceil(log2(ny)) qubits
        velocity   : 4 qubits
        selector   : 1 qubit

    The selector qubit distinguishes f and g.

        selector=0 -> f
        selector=1 -> g

    For nx=ny=4:

        2 x-qubits
        2 y-qubits
        4 velocity qubits
        1 selector qubit

        total = 9 qubits
    """

    if nx < 1 or ny < 1:
        raise ValueError("nx and ny must be positive.")

    n_qx = max(1, int(np.ceil(np.log2(nx))))
    n_qy = max(1, int(np.ceil(np.log2(ny))))

    # D2Q9 requires 4 bits to represent velocity index 0..8.
    n_qvel = 4

    # One qubit selects f or g.
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
            "velocity": list(
                range(
                    n_qx + n_qy,
                    n_qx + n_qy + n_qvel
                )
            ),
            "selector": [
                n_qx + n_qy + n_qvel
            ],
        },
    }


# ---------------------------------------------------------------------------
# Classical normalization
# ---------------------------------------------------------------------------

def normalize_distribution(f, g):
    """
    Compute the normalization constant

        M = sum(f) + sum(g)

    for the joint f/g amplitude encoding.
    """

    f = np.asarray(f, dtype=np.float64)
    g = np.asarray(g, dtype=np.float64)

    if f.ndim != 3 or f.shape[0] != 9:
        raise ValueError(
            "f must have shape (9, ny, nx)."
        )

    if g.shape != f.shape:
        raise ValueError(
            "g must have the same shape as f."
        )

    if np.any(f < 0.0):
        raise ValueError("f contains negative populations.")

    if np.any(g < 0.0):
        raise ValueError("g contains negative populations.")

    total_mass = float(np.sum(f) + np.sum(g))

    if total_mass <= 0.0:
        raise ValueError(
            "Total f+g population must be positive."
        )

    return total_mass


# ---------------------------------------------------------------------------
# Encoding
# ---------------------------------------------------------------------------

def encode_two_phase_state(f, g, layout=None):
    """
    Encode independent f and g populations.

    Basis state:

        |x>|y>|i>|s>

    where

        s=0 -> f_i
        s=1 -> g_i

    Returns:

        state
        normalization M
        layout
    """

    f = np.asarray(f, dtype=np.float64)
    g = np.asarray(g, dtype=np.float64)

    if f.ndim != 3 or f.shape[0] != 9:
        raise ValueError(
            "f must have shape (9, ny, nx)."
        )

    if g.shape != f.shape:
        raise ValueError(
            "g must have the same shape as f."
        )

    ny, nx = f.shape[1], f.shape[2]

    if layout is None:
        layout = get_two_phase_register_layout(nx, ny)

    if nx > (1 << layout["n_qx"]):
        raise ValueError("x register is too small.")

    if ny > (1 << layout["n_qy"]):
        raise ValueError("y register is too small.")

    M = normalize_distribution(f, g)

    dim = 1 << layout["total_qubits"]

    state = np.zeros(dim, dtype=np.complex128)

    n_qx = layout["n_qx"]
    n_qy = layout["n_qy"]
    n_qvel = layout["n_qvel"]

    selector_shift = n_qx + n_qy + n_qvel

    for y in range(ny):
        for x in range(nx):

            for i in range(9):

                f_val = max(float(f[i, y, x]), 0.0)
                g_val = max(float(g[i, y, x]), 0.0)

                idx_common = (
                    (i << (n_qx + n_qy))
                    | (y << n_qx)
                    | x
                )

                # selector = 0 -> f
                idx_f = idx_common

                # selector = 1 -> g
                idx_g = (
                    (1 << selector_shift)
                    | idx_common
                )

                state[idx_f] = np.sqrt(f_val / M)
                state[idx_g] = np.sqrt(g_val / M)

    # Numerical normalization check.
    norm = np.linalg.norm(state)

    if norm <= 1e-15:
        raise ValueError(
            "Encoded state has zero norm."
        )

    state /= norm

    return state, M, layout


# ---------------------------------------------------------------------------
# Backward-compatible alias
# ---------------------------------------------------------------------------

def encode_distribution(f, g=None, layout=None, phi=None):
    """
    Explicit f/g encoding.

    This alias is retained for compatibility with older code.
    """
    if g is None and phi is not None:
        # If g is not given, derive standard initial g from phi
        from classical.d2q9 import W
        ny, nx = f.shape[1], f.shape[2]
        g = np.zeros_like(f)
        for i in range(9):
            g[i] = W[i] * phi

    if g is None:
        g = np.zeros_like(f)

    return encode_two_phase_state(
        f=f,
        g=g,
        layout=layout
    )


# ---------------------------------------------------------------------------
# State normalization validation
# ---------------------------------------------------------------------------

def validate_normalization(state, tolerance=1e-10):
    """
    Verify <psi|psi> = 1.
    """

    state = np.asarray(state, dtype=np.complex128)

    norm_squared = float(
        np.vdot(state, state).real
    )

    error = abs(norm_squared - 1.0)

    return (
        error < tolerance,
        norm_squared,
    )


# ---------------------------------------------------------------------------
# Probability decoding
# ---------------------------------------------------------------------------

def decode_distributions(
    probs,
    layout,
    total_mass,
):
    """
    Decode f and g populations from measurement probabilities.

    Because

        P(x,y,i,0) = f_i / M
        P(x,y,i,1) = g_i / M

    we recover

        f_i = M P(x,y,i,0)
        g_i = M P(x,y,i,1)
    """

    probs = np.asarray(probs, dtype=np.float64)

    expected_dim = 1 << layout["total_qubits"]

    if probs.size != expected_dim:
        raise ValueError(
            f"Expected probability vector of length "
            f"{expected_dim}, got {probs.size}."
        )

    n_qx = layout["n_qx"]
    n_qy = layout["n_qy"]
    n_qvel = layout["n_qvel"]

    nx = layout["nx"]
    ny = layout["ny"]

    selector_shift = n_qx + n_qy + n_qvel

    f = np.zeros((9, ny, nx), dtype=np.float64)
    g = np.zeros((9, ny, nx), dtype=np.float64)

    x_mask = (1 << n_qx) - 1
    y_mask = (1 << n_qy) - 1
    v_mask = (1 << n_qvel) - 1

    for idx, probability in enumerate(probs):

        if probability <= 0.0:
            continue

        x = idx & x_mask

        y = (
            idx >> n_qx
        ) & y_mask

        v = (
            idx >> (n_qx + n_qy)
        ) & v_mask

        selector = (
            idx >> selector_shift
        ) & 1

        # Padding velocity states 9..15 are ignored.
        if x >= nx or y >= ny or v >= 9:
            continue

        population = total_mass * probability

        if selector == 0:
            f[v, y, x] += population
        else:
            g[v, y, x] += population

    return f, g


# ---------------------------------------------------------------------------
# Macroscopic observables
# ---------------------------------------------------------------------------

def decode_macroscopic(
    probs,
    layout,
    total_mass,
):
    """
    Decode:

        rho(x,y)
        u(x,y)
        phi(x,y)

    from the independently encoded f and g distributions.
    """

    f, g = decode_distributions(
        probs=probs,
        layout=layout,
        total_mass=total_mass,
    )

    rho = np.sum(f, axis=0)

    phi = np.sum(g, axis=0)

    rho_safe = np.where(
        rho > 1e-14,
        rho,
        1.0
    )

    ux = np.zeros_like(rho)
    uy = np.zeros_like(rho)

    for i in range(9):
        ux += C_X[i] * f[i]
        uy += C_Y[i] * f[i]

    ux /= rho_safe
    uy /= rho_safe

    ux = np.where(rho > 1e-14, ux, 0.0)
    uy = np.where(rho > 1e-14, uy, 0.0)

    u = np.stack(
        [ux, uy],
        axis=0
    )

    return f, g, rho, u, phi


# ---------------------------------------------------------------------------
# Convenience initialization
# ---------------------------------------------------------------------------

def quantum_initialize_two_phase_dambreak(nx=4, ny=4):
    """
    Initialize the classical dam-break state and encode the independent
    f and g distributions into a quantum state.
    """

    from classical.two_phase import initialize_two_phase_dambreak

    phi, rho, u, f, g = (
        initialize_two_phase_dambreak(nx, ny)
    )

    layout = get_two_phase_register_layout(
        nx,
        ny
    )

    state, total_mass, layout = (
        encode_two_phase_state(
            f,
            g,
            layout
        )
    )

    qc = QuantumCircuit(
        layout["total_qubits"],
        name="TwoPhaseFGEncoding"
    )

    qc.initialize(
        state,
        range(layout["total_qubits"])
    )

    return (
        qc,
        state,
        total_mass,
        layout,
    )
