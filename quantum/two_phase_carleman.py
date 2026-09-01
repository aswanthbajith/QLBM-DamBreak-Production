"""
Local second-order Carleman representation for two-phase D2Q9 BGK.

Important:
This module implements the truncated polynomial collision map

    Psi' = M1 Psi + M2 (Psi ⊗ Psi)

and does NOT claim that the quadratic layer itself evolves exactly
under M1 ⊗ M1.

The quadratic layer is reconstructed at every timestep from the
current physical state. This makes the algorithm a hybrid
quantum-classical/re-encoding algorithm rather than a closed U^t
quantum evolution.
"""

import numpy as np

from classical.d2q9 import C_X, C_Y, W


NPOP = 9
NPHASE = 9
NVAR = 18
NQUAD = NVAR * NVAR


def build_two_phase_linear_collision_matrix_18x18(
    tau_f: float = 0.8,
    tau_g: float = 0.7,
) -> np.ndarray:
    """
    Linear part of the weakly-compressible two-phase collision model.
    """

    omega_f = 1.0 / tau_f
    omega_g = 1.0 / tau_g

    M1 = np.zeros((NVAR, NVAR), dtype=np.float64)

    # Hydrodynamic f block
    for i in range(NPOP):
        for j in range(NPOP):

            ci_dot_cj = (
                C_X[i] * C_X[j]
                + C_Y[i] * C_Y[j]
            )

            equilibrium_linear = (
                W[i] *
                (
                    1.0
                    + 3.0 * ci_dot_cj
                )
            )

            M1[i, j] = (
                (1.0 - omega_f) * (1.0 if i == j else 0.0)
                + omega_f * equilibrium_linear
            )

    # Phase-field g block
    #
    # Linear equilibrium:
    #     g_i^eq = w_i phi
    #
    for i in range(NPOP):
        for j in range(NPOP):
            M1[NPOP + i, NPOP + j] = (
                (1.0 - omega_g) * (1.0 if i == j else 0.0)
                + omega_g * W[i]
            )

    return M1


def build_two_phase_quadratic_collision_tensor_18x324(
    tau_f: float = 0.8,
    tau_g: float = 0.7,
    rho0: float = 1.0,
) -> np.ndarray:
    """
    Quadratic contribution to the local collision map.

    Output:
        M2 shape = (18, 324)

    such that

        Psi' = M1 @ Psi + M2 @ kron(Psi, Psi)

    within the chosen weakly-compressible second-order model.
    """

    if rho0 <= 0.0:
        raise ValueError("rho0 must be positive.")

    omega_f = 1.0 / tau_f
    omega_g = 1.0 / tau_g

    M2 = np.zeros((NVAR, NQUAD), dtype=np.float64)

    cs2 = 1.0 / 3.0
    cs4 = cs2 * cs2

    # ------------------------------------------------------------
    # f quadratic convective term
    # ------------------------------------------------------------
    for i in range(NPOP):

        wi = W[i]

        for q1 in range(NPOP):
            for q2 in range(NPOP):

                ci_q1 = (
                    C_X[i] * C_X[q1]
                    + C_Y[i] * C_Y[q1]
                )

                ci_q2 = (
                    C_X[i] * C_X[q2]
                    + C_Y[i] * C_Y[q2]
                )

                q1_q2 = (
                    C_X[q1] * C_X[q2]
                    + C_Y[q1] * C_Y[q2]
                )

                coefficient = (
                    omega_f
                    * wi
                    / rho0
                    * (
                        (ci_q1 * ci_q2) / (2.0 * cs4)
                        - q1_q2 / (2.0 * cs2)
                    )
                )

                col = q1 * NVAR + q2

                M2[i, col] = coefficient

    # ------------------------------------------------------------
    # g phase-advection term
    #
    # g_i^eq ~ w_i phi [1 + 3 c_i.u]
    #
    # phi = sum g_q1
    # j   = sum c_q2 f_q2
    # ------------------------------------------------------------
    for i in range(NPOP):

        wi = W[i]

        for q1 in range(NPOP):
            for q2 in range(NPOP):

                ci_dot_cq2 = (
                    C_X[i] * C_X[q2]
                    + C_Y[i] * C_Y[q2]
                )

                coefficient = (
                    omega_g
                    * wi
                    * 3.0
                    * ci_dot_cq2
                    / rho0
                )

                # g index first, f index second
                col = (NPOP + q1) * NVAR + q2

                M2[NPOP + i, col] = coefficient

    return M2


def lift_two_phase_state(
    f: np.ndarray,
    g: np.ndarray,
    order: int = 2,
) -> np.ndarray:
    """
    Build the physical + quadratic Carleman vector.

    Y = [Psi, Psi⊗Psi]
    """

    f = np.asarray(f, dtype=np.float64).reshape(9)
    g = np.asarray(g, dtype=np.float64).reshape(9)

    psi = np.concatenate([f, g])

    if order == 1:
        return psi

    quadratic = np.kron(psi, psi)

    return np.concatenate([psi, quadratic])


def project_two_phase_state(
    Y: np.ndarray,
    order: int = 2,
):
    """
    Extract physical populations only.
    """

    Y = np.asarray(Y, dtype=np.float64)

    if Y.size < NVAR:
        raise ValueError("Invalid Carleman state.")

    psi = Y[:NVAR]

    f = psi[:NPOP].copy()
    g = psi[NPOP:].copy()

    return f, g


def build_second_order_evaluation_operator(
    tau_f: float = 0.8,
    tau_g: float = 0.7,
    rho0: float = 1.0,
) -> np.ndarray:
    """
    Construct the operator actually required for stepwise
    second-order Carleman evaluation.

    A_eval has shape:

        18 x 342

    and satisfies

        Psi_next =
            A_eval [Psi ; Psi⊗Psi]

    for the retained second-order polynomial model.

    Unlike the old 342x342 matrix, this function does not
    pretend that the quadratic layer evolves independently.
    """

    M1 = build_two_phase_linear_collision_matrix_18x18(
        tau_f=tau_f,
        tau_g=tau_g,
    )

    M2 = build_two_phase_quadratic_collision_tensor_18x324(
        tau_f=tau_f,
        tau_g=tau_g,
        rho0=rho0,
    )

    A_eval = np.concatenate(
        [M1, M2],
        axis=1,
    )

    assert A_eval.shape == (18, 342)

    return A_eval


def apply_second_order_carleman(
    f: np.ndarray,
    g: np.ndarray,
    tau_f: float = 0.8,
    tau_g: float = 0.7,
    rho0: float = 1.0,
):
    """
    Apply one physical collision step.

    The quadratic state is rebuilt from the current physical
    populations at every timestep.

    This is the mathematically consistent interpretation of
    second-order local Carleman truncation for the present
    hybrid implementation.
    """

    Y = lift_two_phase_state(f, g)

    A_eval = build_second_order_evaluation_operator(
        tau_f=tau_f,
        tau_g=tau_g,
        rho0=rho0,
    )

    psi_next = A_eval @ Y

    f_next = psi_next[:9]
    g_next = psi_next[9:18]

    return f_next, g_next
