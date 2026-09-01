import pytest
import numpy as np
import scipy.linalg as la
from classical.d2q9 import C_X, C_Y, W
from classical.equilibrium import compute_equilibrium
from quantum.carleman_collision import (
    build_carleman_basis,
    build_local_carleman_operator,
    lift_state,
    project_state,
    apply_carleman_operator
)


def classical_bgk_single_node(f, omega=1.25):
    """Exact classical single-node D2Q9 BGK collision."""
    rho = float(np.sum(f))
    ux = float(np.sum(f * C_X) / rho)
    uy = float(np.sum(f * C_Y) / rho)
    f_eq = np.zeros(9)
    for i in range(9):
        c_dot_u = C_X[i] * ux + C_Y[i] * uy
        u_sq = ux**2 + uy**2
        f_eq[i] = W[i] * rho * (1.0 + 3.0 * c_dot_u + 4.5 * c_dot_u**2 - 1.5 * u_sq)
    return (1.0 - omega) * f + omega * f_eq


class TestCarlemanCollision:
    """
    Rigorously tests Step 4: Local Carleman Linearization vs Exact Classical BGK Collision.
    """

    def test_01_carleman_basis_dimensions(self):
        b1 = build_carleman_basis(dim_base=9, order=1)
        assert b1["total_dim"] == 9
        
        b2 = build_carleman_basis(dim_base=9, order=2)
        assert b2["total_dim"] == 90
        assert b2["layer_dims"] == [9, 81]
        
        b3 = build_carleman_basis(dim_base=9, order=3)
        assert b3["total_dim"] == 819
        assert b3["layer_dims"] == [9, 81, 729]

    def test_02_carleman_on_equilibrium_state(self):
        rho = 1.0
        u = np.array([0.05, -0.02])
        f_eq = np.zeros(9)
        for i in range(9):
            c_dot_u = C_X[i] * u[0] + C_Y[i] * u[1]
            u_sq = u[0]**2 + u[1]**2
            f_eq[i] = W[i] * rho * (1.0 + 3.0 * c_dot_u + 4.5 * c_dot_u**2 - 1.5 * u_sq)
            
        omega = 1.25
        f_c = classical_bgk_single_node(f_eq, omega=omega)
        
        C2 = build_local_carleman_operator(omega=omega, rho0=rho, order=2)
        f_q2 = apply_carleman_operator(f_eq, C2, order=2)
        
        err_rel = la.norm(f_q2 - f_c) / la.norm(f_c)
        assert err_rel < 1e-3, f"Carleman Order 2 equilibrium error {err_rel:.2e} >= 1e-3"

    def test_03_carleman_order_convergence_on_100_random_states(self):
        np.random.seed(42)
        omega = 1.25
        rho0 = 1.0
        
        C1 = build_local_carleman_operator(omega=omega, rho0=rho0, order=1)
        C2 = build_local_carleman_operator(omega=omega, rho0=rho0, order=2)
        C3 = build_local_carleman_operator(omega=omega, rho0=rho0, order=3)
        
        errs_o1 = []
        errs_o2 = []
        errs_o3 = []
        
        for _ in range(100):
            rho = np.random.uniform(0.8, 1.2)
            u_mag = np.random.uniform(0.01, 0.08)
            ang = np.random.uniform(0, 2*np.pi)
            ux, uy = u_mag * np.cos(ang), u_mag * np.sin(ang)
            
            f_base = np.zeros(9)
            for i in range(9):
                c_dot_u = C_X[i] * ux + C_Y[i] * uy
                u_sq = ux**2 + uy**2
                f_base[i] = W[i] * rho * (1.0 + 3.0 * c_dot_u + 4.5 * c_dot_u**2 - 1.5 * u_sq)
                
            # Perturb
            pert = np.random.uniform(-0.01, 0.01, 9)
            pert -= np.sum(pert) * W
            f_in = np.maximum(f_base + pert, 1e-4)
            f_in = f_in * (rho / np.sum(f_in))
            
            f_c = classical_bgk_single_node(f_in, omega=omega)
            
            f_o1 = apply_carleman_operator(f_in, C1, order=1)
            f_o2 = apply_carleman_operator(f_in, C2, order=2)
            f_o3 = apply_carleman_operator(f_in, C3, order=3)
            
            errs_o1.append(la.norm(f_o1 - f_c) / la.norm(f_c))
            errs_o2.append(la.norm(f_o2 - f_c) / la.norm(f_c))
            errs_o3.append(la.norm(f_o3 - f_c) / la.norm(f_c))
            
        mean_o1 = np.mean(errs_o1)
        mean_o2 = np.mean(errs_o2)
        mean_o3 = np.mean(errs_o3)
        
        print(f"\n100-State Ensemble Carleman Convergence:")
        print(f"  Order 1 Mean Relative Error: {mean_o1*100:.3f}%")
        print(f"  Order 2 Mean Relative Error: {mean_o2*100:.3f}%")
        print(f"  Order 3 Mean Relative Error: {mean_o3*100:.3f}%")
        
        # Rigorous hierarchy check: Order 2 must be significantly more accurate than Order 1
        assert mean_o2 < mean_o1
        assert mean_o2 < 0.05, f"Order 2 mean error {mean_o2*100:.2f}% >= 5%"
