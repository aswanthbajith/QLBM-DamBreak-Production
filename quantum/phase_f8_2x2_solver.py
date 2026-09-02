"""
Phase F8: End-to-End 2x2 Quantum Two-Phase Dam-Break Lattice Boltzmann Solver.

Mathematical Architecture:
1. State Representation:
   Hilbert space H = H_x (x) H_y (x) H_vel (x) H_phase (7 data qubits, dim = 128)
   Qubit Layout:
   - Phase qubit: index 0 (0=f species, 1=g species)
   - Velocity qubits: indices 1, 2, 3, 4 (v0..v3, velocities 0..8, 9..15 idle)
   - Y-spatial qubit: index 5 (y in {0, 1})
   - X-spatial qubit: index 6 (x in {0, 1})
   State Index: (x << 6) | (y << 5) | (i << 1) | p

2. Quantum Collision Core (Phase F5):
   Parameterized 6-qubit Sz.-Nagy unitary dilation U_C(alpha, u) in U(64) on each node (x, y).

3. Exact Reversible Arithmetic Streaming (Phase F6):
   S_arith |x, y, i, p> = |(x + c_ix) mod 2, (y + c_iy) mod 2, i, p> via modular quantum gates.

4. Physical Bounce-Back Boundary Involution (Phase F7):
   B |x, y, i, p> = |x, y, opp(i), p> (B^2 = I, B†B = I).

5. Two Execution Modes:
   - Mode 1: Parameter-Fed Quantum Collision (exact parameters fed to quantum dilation)
   - Mode 2: State-Derived Parameter Mode (coherent fixed-point moment arithmetic emulator)
"""

from typing import Tuple, Dict, Any, Optional, List
import numpy as np
import scipy.linalg as la
from qiskit.quantum_info import Operator

from classical.d2q9 import C_X, C_Y, W, OPPOSITE
from classical.equilibrium import compute_equilibrium
from classical.level4_two_phase import Level4TwoPhaseLBM
from quantum.reference_collision import reference_one_node_level4_collision
from quantum.parameterized_collision_oracle import (
    build_parameterized_collision_matrix,
    CoherentFixedPointMomentOracle,
    ParameterizedQuantumCollisionOracle,
)
from quantum.arithmetic_streaming import (
    build_direct_streaming_circuit,
    build_direct_boundary_circuit,
)
from quantum.transparency_audit import (
    TransparencyEvent,
    get_transparency_logger,
)


class PhaseF8TwoPhaseQLBM2x2:
    """
    End-to-End 2x2 Quantum Two-Phase Lattice Boltzmann Solver.
    """

    def __init__(
        self,
        rho_L: float = 1.0,
        rho_G: float = 0.1,
        nu_L: float = 0.05,
        nu_G: float = 0.05,
        tau_g: float = 0.70,
        sigma: float = 0.0,
        g_acc: float = 0.0,
        dam_width_ratio: float = 0.5,
        dam_height_ratio: float = 0.5,
    ):
        self.nx = 2
        self.ny = 2
        self.rho_L = rho_L
        self.rho_G = rho_G
        self.nu_L = nu_L
        self.nu_G = nu_G
        self.tau_g = tau_g
        self.sigma = sigma
        self.g_acc = g_acc

        self.num_data_qubits = 7  # 1_x + 1_y + 4_vel + 1_phase
        self.hilbert_dim = 128

        # Precompute unitary streaming and boundary operators on 7-qubit data register
        qc_stream = build_direct_streaming_circuit(nx=2, ny=2)
        self.U_stream = Operator(qc_stream).data  # (128, 128)

        qc_bnd = build_direct_boundary_circuit(nx=2, ny=2)
        self.U_bnd = Operator(qc_bnd).data  # (128, 128)

        # Quantum collision oracle
        self.collision_oracle = ParameterizedQuantumCollisionOracle(
            nu_L=self.nu_L,
            nu_G=self.nu_G,
            tau_g=self.tau_g,
        )

        # Initialize physical fields matching Level-4 dam break setup
        self._init_physical_distributions(dam_width_ratio, dam_height_ratio)
        self.norm_N = float(np.sqrt(np.sum(self.f**2) + np.sum(self.g**2)))
        self.psi = self.encode_state()

    def _state_index(self, x: int, y: int, i: int, p: int) -> int:
        """Qubit layout: (x << 6) | (y << 5) | (i << 1) | p."""
        return (x << 6) | (y << 5) | (i << 1) | p

    def _init_physical_distributions(self, dam_w: float, dam_h: float):
        """Initializes f and g matching Level-4 2x2 dam-break setup."""
        self.f = np.zeros((9, self.ny, self.nx), dtype=np.float64)
        self.g = np.zeros((9, self.ny, self.nx), dtype=np.float64)

        x_grid, y_grid = np.meshgrid(np.arange(self.nx), np.arange(self.ny))
        dam_mask = (x_grid < dam_w * self.nx) & (y_grid < dam_h * self.ny)

        rho = np.where(dam_mask, self.rho_L, self.rho_G)
        alpha = np.where(dam_mask, 1.0, 0.0)
        u_init = np.zeros((2, self.ny, self.nx), dtype=np.float64)

        f_eq = compute_equilibrium(rho, u_init)
        self.f = f_eq.copy()

        for i in range(9):
            self.g[i] = W[i] * alpha

    def encode_state(self) -> np.ndarray:
        """Encodes physical f, g into normalized 128-dimensional quantum statevector."""
        logger = get_transparency_logger()
        logger.log(TransparencyEvent.STATE_PREPARATION)
        self.norm_N = float(np.sqrt(np.sum(self.f**2) + np.sum(self.g**2)))
        psi = np.zeros(self.hilbert_dim, dtype=np.complex128)

        for x in range(self.nx):
            for y in range(self.ny):
                for i in range(9):
                    idx_f = self._state_index(x, y, i, 0)
                    idx_g = self._state_index(x, y, i, 1)
                    psi[idx_f] = self.f[i, y, x] / self.norm_N
                    psi[idx_g] = self.g[i, y, x] / self.norm_N

        return psi

    def decode_state(self, psi_vec: Optional[np.ndarray] = None) -> Tuple[np.ndarray, np.ndarray]:
        """Decodes 128-dimensional statevector back to continuous physical fields f and g."""
        logger = get_transparency_logger()
        logger.log(TransparencyEvent.CLASSICAL_DECODE)
        psi = self.psi if psi_vec is None else psi_vec
        f = np.zeros((9, self.ny, self.nx), dtype=np.float64)
        g = np.zeros((9, self.ny, self.nx), dtype=np.float64)

        for x in range(self.nx):
            for y in range(self.ny):
                for i in range(9):
                    idx_f = self._state_index(x, y, i, 0)
                    idx_g = self._state_index(x, y, i, 1)
                    f[i, y, x] = float(np.real(psi[idx_f])) * self.norm_N
                    g[i, y, x] = float(np.real(psi[idx_g])) * self.norm_N

        return f, g

    def compute_diagnostics(self) -> Dict[str, Any]:
        """Evaluates macroscopic fields and conservation metrics."""
        logger = get_transparency_logger()
        logger.log(TransparencyEvent.DIAGNOSTIC_EVALUATION)
        rho = np.sum(self.f, axis=0)
        alpha = np.sum(self.g, axis=0)
        jx = np.sum(self.f * C_X[:, None, None], axis=0)
        jy = np.sum(self.f * C_Y[:, None, None], axis=0)
        ux = jx / (rho + 1e-15)
        uy = jy / (rho + 1e-15)

        total_mass = float(np.sum(rho))
        phase_mass = float(np.sum(alpha))
        norm_psi = float(la.norm(self.psi))

        return {
            "rho": rho,
            "alpha": alpha,
            "jx": jx,
            "jy": jy,
            "ux": ux,
            "uy": uy,
            "total_mass": total_mass,
            "phase_mass": phase_mass,
            "norm_psi": norm_psi,
        }

    def step_mode1_parameter_fed(
        self,
        alpha_feed: Optional[np.ndarray] = None,
        u_feed: Optional[np.ndarray] = None,
        apply_oaa: bool = False,
    ) -> Dict[str, Any]:
        """
        Mode 1: Parameter-Fed Quantum Collision + Arithmetic Streaming + Boundary Involution.
        """
        logger = get_transparency_logger()
        f_coll = np.zeros_like(self.f)
        g_coll = np.zeros_like(self.g)
        diag_step = []

        # 1. Apply Parameterized Quantum Collision on each spatial node
        for x in range(self.nx):
            for y in range(self.ny):
                z_node = np.concatenate([self.f[:, y, x], self.g[:, y, x]])
                if alpha_feed is not None:
                    alpha_val = alpha_feed[y, x]
                    logger.log(TransparencyEvent.CLASSICAL_PARAMETER_GENERATION, {"source": "external_feed"})
                else:
                    alpha_val = float(np.sum(self.g[:, y, x]))
                    logger.log(TransparencyEvent.CLASSICAL_PARAMETER_GENERATION, {"source": "classical_moment_sum"})

                if u_feed is not None:
                    u_val = u_feed[:, y, x]
                else:
                    rho_n = float(np.sum(self.f[:, y, x]))
                    ux_n = float(np.sum(self.f[:, y, x] * C_X)) / (rho_n + 1e-15)
                    uy_n = float(np.sum(self.f[:, y, x] * C_Y)) / (rho_n + 1e-15)
                    u_val = np.array([ux_n, uy_n], dtype=np.float64)

                logger.log(TransparencyEvent.QUANTUM_COLLISION_EXECUTION, {"node": (x, y), "alpha": alpha_val})
                z_post, metrics = self.collision_oracle.execute_collision(
                    z=z_node,
                    alpha=alpha_val,
                    u_vec=u_val,
                    apply_oaa=apply_oaa,
                )
                f_coll[:, y, x] = z_post[:9]
                g_coll[:, y, x] = z_post[9:]
                diag_step.append(metrics)

        # 2. Encode post-collision populations into statevector
        self.f = f_coll
        self.g = g_coll
        logger.log(TransparencyEvent.CLASSICAL_REENCODE)
        self.psi = self.encode_state()

        # 3. Apply Reversible Quantum Arithmetic Streaming (S_arith)
        logger.log(TransparencyEvent.QUANTUM_STREAMING_EXECUTION)
        self.psi = self.U_stream @ self.psi

        # 4. Apply Physical Bounce-Back Boundary Involution (B)
        logger.log(TransparencyEvent.QUANTUM_BOUNDARY_EXECUTION)
        self.psi = self.U_bnd @ self.psi

        # 5. Decode updated populations
        self.f, self.g = self.decode_state()

        return {
            "mode": "Mode 1 (Parameter-Fed Quantum Collision)",
            "node_metrics": diag_step,
            "diagnostics": self.compute_diagnostics(),
        }

    def step_mode2_state_derived(
        self,
        word_length: int = 16,
        frac_bits: int = 12,
        apply_oaa: bool = False,
    ) -> Dict[str, Any]:
        """
        Mode 2: State-Derived Parameter Quantum Collision (Coherent-Arithmetic Emulator).
        """
        logger = get_transparency_logger()
        moment_oracle = CoherentFixedPointMomentOracle(total_bits=word_length, frac_bits=frac_bits)
        f_coll = np.zeros_like(self.f)
        g_coll = np.zeros_like(self.g)
        diag_step = []

        for x in range(self.nx):
            for y in range(self.ny):
                z_node = np.concatenate([self.f[:, y, x], self.g[:, y, x]])
                # Derive moments coherently via fixed-point arithmetic
                logger.log(TransparencyEvent.COHERENT_MOMENT_EMULATION, {"word_length": word_length, "node": (x, y)})
                m = moment_oracle.evaluate_moments(z_node)
                u_derived = np.array([m["u_x"], m["u_y"]], dtype=np.float64)
                alpha_derived = m["alpha"]

                logger.log(TransparencyEvent.QUANTUM_COLLISION_EXECUTION, {"node": (x, y), "alpha": alpha_derived})
                z_post, metrics = self.collision_oracle.execute_collision(
                    z=z_node,
                    alpha=alpha_derived,
                    u_vec=u_derived,
                    apply_oaa=apply_oaa,
                )
                f_coll[:, y, x] = z_post[:9]
                g_coll[:, y, x] = z_post[9:]
                diag_step.append(metrics)

        self.f = f_coll
        self.g = g_coll
        logger.log(TransparencyEvent.CLASSICAL_REENCODE)
        self.psi = self.encode_state()
        logger.log(TransparencyEvent.QUANTUM_STREAMING_EXECUTION)
        self.psi = self.U_stream @ self.psi
        logger.log(TransparencyEvent.QUANTUM_BOUNDARY_EXECUTION)
        self.psi = self.U_bnd @ self.psi
        self.f, self.g = self.decode_state()

        return {
            "mode": "Mode 2 (State-Derived Parameter Mode / Coherent-Arithmetic Emulator)",
            "word_length": word_length,
            "node_metrics": diag_step,
            "diagnostics": self.compute_diagnostics(),
        }

    def audit_dilation_leakage(self, K_powers: List[int] = [1, 2, 4, 8]) -> List[Dict[str, Any]]:
        """
        Mandatory mathematical audit: tests unprojected dilation powers (alpha_C * U_C)^K
        vs exact projected powers to quantify defect leakage into the ancilla.
        """
        leakage_results = []
        # Sample center node
        z_node = np.concatenate([self.f[:, 0, 0], self.g[:, 0, 0]])
        rho_n = float(np.sum(self.f[:, 0, 0]))
        alpha_n = float(np.sum(self.g[:, 0, 0]))
        u_n = np.array([float(np.sum(self.f[:, 0, 0] * C_X)) / rho_n, float(np.sum(self.f[:, 0, 0] * C_Y)) / rho_n])

        C_mat, alpha_C, U_C, diag = build_parameterized_collision_matrix(alpha_n, u_n)
        P = np.zeros((18, 64), dtype=np.float64)
        P[:18, :18] = np.eye(18)

        for K in K_powers:
            C_K = np.linalg.matrix_power(C_mat, K)
            unproj_K = P @ np.linalg.matrix_power(alpha_C * U_C, K) @ P.T
            proj_K = np.linalg.matrix_power(P @ (alpha_C * U_C) @ P.T, K)

            err_unproj = float(la.norm(unproj_K - C_K, 2) / (la.norm(C_K, 2) + 1e-15))
            err_proj = float(la.norm(proj_K - C_K, 2) / (la.norm(C_K, 2) + 1e-15))

            leakage_results.append({
                "K_powers": K,
                "unprojected_leakage_error": err_unproj,
                "unprojected_percentage": f"{err_unproj * 100:.2f}%",
                "projected_reset_error": err_proj,
                "alpha_C": alpha_C,
                "base_p0": diag["p0"],
                "oaa_best_m": diag["optimal_m"],
                "oaa_p_m": diag["best_p_m"],
            })

        return leakage_results
