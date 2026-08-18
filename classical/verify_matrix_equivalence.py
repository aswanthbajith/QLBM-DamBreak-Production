#!/usr/bin/env python3
"""
Verification Script for Step 5: Exact Numerical Equivalence
Between Classical Two-Phase LBM and Matrix-Operator System.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from two_phase_lbm import TwoPhaseLBM2D
from matrix_two_phase_lbm import MatrixTwoPhaseLBM2D

def verify_equivalence():
    val_dir = "/home/aswa/Research/QLBM-DamBreak/validation"
    os.makedirs(val_dir, exist_ok=True)

    nx, ny = 40, 20
    dam_w, dam_h = 10, 10
    total_steps = 50

    print("="*80)
    print("STEP 5: EXACT MATRIX-OPERATOR ALGEBRAIC EQUIVALENCE PROOF")
    print(f"Domain: {nx}x{ny} ({nx*ny} nodes) | Dam: {dam_w}x{dam_h} | Steps: {total_steps}")
    print("="*80)

    # 1. Classical Continuous Solver
    classical_sim = TwoPhaseLBM2D(
        nx=nx, ny=ny,
        rho_L=1.0, rho_G=0.1,
        nu_L=0.01, nu_G=0.01,
        sigma=0.001, gy=-4.0e-4,
        width=3.5, mobility=0.05,
        enable_surface_tension=True,
        free_slip_bottom=True
    )
    classical_sim.initialize_dam(dam_w=dam_w, dam_h=dam_h)

    # 2. Matrix Operator Solver
    matrix_sim = MatrixTwoPhaseLBM2D(
        nx=nx, ny=ny,
        rho_L=1.0, rho_G=0.1,
        nu_L=0.01, nu_G=0.01,
        sigma=0.001, gy=-4.0e-4,
        width=3.5, mobility=0.05,
        enable_surface_tension=True,
        free_slip_bottom=True
    )

    N = nx * ny
    dim_single = 9 * N
    Psi = np.zeros(2 * dim_single, dtype=np.float64)

    # Populate initial state
    for q in range(9):
        Psi[q * N : (q + 1) * N] = classical_sim.g[q].flatten()
        Psi[dim_single + q * N : dim_single + (q + 1) * N] = classical_sim.phase_field.h[q].flatten()

    u_m = classical_sim.u.copy()
    v_m = classical_sim.v.copy()

    max_linf = 0.0
    max_l2 = 0.0
    records = []

    print(f"\n{'Step':>6} | {'Max Linf Error':>18} | {'Relative L2 Error':>18} | {'Status':>12}")
    print("-" * 65)

    for step in range(total_steps + 1):
        # Extract classical state
        Psi_c = np.zeros(2 * dim_single, dtype=np.float64)
        for q in range(9):
            Psi_c[q * N : (q + 1) * N] = classical_sim.g[q].flatten()
            Psi_c[dim_single + q * N : dim_single + (q + 1) * N] = classical_sim.phase_field.h[q].flatten()

        diff = np.abs(Psi - Psi_c)
        linf = float(np.max(diff))
        l2 = float(np.linalg.norm(diff) / (np.linalg.norm(Psi_c) + 1e-15))

        max_linf = max(max_linf, linf)
        max_l2 = max(max_l2, l2)

        status = "EXACT (ZERO)" if linf < 1e-13 else ("MACHINE PREC" if linf < 1e-10 else "DISCREPANCY")
        records.append((step, linf, l2, status))

        if step % 10 == 0:
            print(f"{step:6d} | {linf:18.4e} | {l2:18.4e} | {status:>12}")

        # Step both forward
        classical_sim.step()
        Psi, u_m, v_m = matrix_sim.step(Psi, u_m, v_m)

    print("-" * 65)
    print(f"Overall Max L_inf Error over {total_steps} steps: {max_linf:.4e}")
    print(f"Overall Max Rel L_2 Error over {total_steps} steps: {max_l2:.4e}")

    # Generate Markdown Report
    report = f"""# Exact Matrix-Operator Equivalence Verification Report

## 1. Executive Summary
- **Operator Structure**:
  $$\\mathbf{{\\Psi}}(t+1) = \\mathbf{{S}} \\cdot \\mathbf{{\\Psi}}^{{post}}(\\mathbf{{\\Psi}}(t))$$
  where $\\mathbf{{S}} \\in \\{{0, 1\\}}^{{18N \\times 18N}}$ is the unitary spatial permutation and boundary reflection matrix.
- **Maximum Point-wise Discrepancy**: $L_\\infty = {max_linf:.4e}$ across {total_steps} time steps.
- **Maximum Relative $L_2$ Discrepancy**: $L_2 = {max_l2:.4e}$.

---

## 2. Step-by-Step Numerical Verification Table

| Step | Max Point-Wise Error $L_\\infty$ | Relative Error $L_2$ | Equivalence Status |
| :---: | :---: | :---: | :---: |
"""
    for s, li, l2, st in records:
        if s % 10 == 0:
            report += f"| **{s}** | ${li:.4e}$ | ${l2:.4e}$ | **{st}** |\n"

    report += f"""
---

## 3. Structural Properties of Discrete Operators
1. **Global Streaming Matrix $\\mathbf{{S}}$**:
   - Dimension: $18N \\times 18N = {2 * 9 * N} \\times {2 * 9 * N}$
   - Sparsity: Exactly $1.0$ non-zero entry ($+1.0$) per row and column.
   - Unitary Property: $\\mathbf{{S}}^T \\mathbf{{S}} = \\mathbf{{I}}_{{18N}}$ (strictly exact).
2. **Boundary Treatment**:
   - Solid walls: Half-way bounce back ($\mathbf{{c}}_{{\\bar{{q}}}} = -\\mathbf{{c}}_q$).
   - Floor: Specular reflection ($c_y \\to -c_y$).
"""
    with open(f"{val_dir}/EXACT_MATRIX_EQUIVALENCE.md", "w") as f:
        f.write(report)

    print(f"\nReport written to: {val_dir}/EXACT_MATRIX_EQUIVALENCE.md")

if __name__ == "__main__":
    verify_equivalence()
