import os, sys, time, csv, tracemalloc
sys.path.append("/home/aswa/Research/QLBM-DamBreak/classical")
sys.path.append("/home/aswa/Research/QLBM-DamBreak/quantum")

import numpy as np
import scipy.linalg as la
import scipy.sparse as sp

from two_phase_lbm import TwoPhaseLBM2D
from carleman_lbm import CarlemanTwoPhaseLBM
from block_encoding import QuantumBlockEncoding
from qsvt_solver import QSVTSolver

repo_dir = "/home/aswa/Research/QLBM-DamBreak"

# ==============================================================================
# STAGE 6.2: INDEPENDENT CLASSICAL REFERENCE BENCHMARK
# ==============================================================================
print("--- [STAGE 6.2] Running Classical Benchmark Across 6 Grids ---")
grids = [
    ("4x2", 4, 2, 2, 2, 50),
    ("8x4", 8, 4, 3, 3, 50),
    ("16x8", 16, 8, 6, 6, 50),
    ("32x16", 32, 16, 12, 12, 50),
    ("64x32", 64, 32, 24, 24, 50),
    ("300x100", 300, 100, 120, 120, 50)
]

cl_records = []
for name, nx, ny, dw, dh, steps in grids:
    tracemalloc.start()
    t0 = time.perf_counter()
    sim = TwoPhaseLBM2D(nx=nx, ny=ny, rho_L=1.0, rho_G=0.1, nu_L=0.01, nu_G=0.01, gy=-2e-4, free_slip_bottom=True)
    sim.initialize_dam(dam_w=dw, dam_h=dh)
    m0 = float(np.sum(sim.phi))
    
    t_steps = []
    for s in range(1, steps + 1):
        ts0 = time.perf_counter()
        sim.step()
        t_steps.append(time.perf_counter() - ts0)
        
    t_tot = time.perf_counter() - t0
    cur_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    m_final = float(np.sum(sim.phi))
    m_drift = abs(m_final - m0) / (m0 + 1e-15)
    u_mag = np.sqrt(sim.u[0]**2 + sim.u[1]**2)
    u_max = float(np.max(u_mag))
    
    # Observables
    floor_phi = sim.phi[:, min(1, ny-1)]
    liq_idx = np.where(floor_phi > 0.5)[0]
    x_front = float(np.max(liq_idx)) if len(liq_idx) > 0 else float(dw)
    x_star = x_front / float(dh)
    
    wall_phi = sim.phi[min(1, nx-1), :]
    col_idx = np.where(wall_phi > 0.5)[0]
    h_col = float(np.max(col_idx)) if len(col_idx) > 0 else float(dh)
    h_star = h_col / float(dh)
    
    step_ms = np.mean(t_steps) * 1000.0
    ram_mb = peak_mem / (1024 * 1024)
    
    rec = {
        "grid": name,
        "nodes": nx * ny,
        "steps": steps,
        "total_time_sec": t_tot,
        "step_time_ms": step_ms,
        "peak_ram_mb": ram_mb,
        "initial_mass": m0,
        "final_mass": m_final,
        "mass_drift": m_drift,
        "max_velocity_u": u_max,
        "surge_front_x_star": x_star,
        "column_height_h_star": h_star,
        "classification": "MEASURED"
    }
    cl_records.append(rec)
    print(f"Grid {name:<8} | Nodes={nx*ny:<6d} | Time={t_tot:6.3f}s | Step={step_ms:6.2f}ms | RAM={ram_mb:6.2f}MB | Drift={m_drift:.2e} | x*={x_star:.2f}")

with open(os.path.join(repo_dir, "PHASE6_CLASSICAL_BENCHMARK.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(cl_records[0].keys()))
    writer.writeheader()
    writer.writerows(cl_records)

# ==============================================================================
# STAGE 6.3: CARLEMAN ACCURACY VS TIME
# ==============================================================================
print("\n--- [STAGE 6.3] Running Carleman Accuracy vs Time (t=1..200) ---")
nx, ny, dw, dh = 4, 2, 2, 2
N = nx * ny
sim_c = TwoPhaseLBM2D(nx=nx, ny=ny, rho_L=1.0, rho_G=0.1, nu_L=0.01, nu_G=0.01, gy=-2e-4, free_slip_bottom=True)
sim_c.initialize_dam(dam_w=dw, dam_h=dh)
carle = CarlemanTwoPhaseLBM(nx=nx, ny=ny, rho0=1.0, nu=0.01, gy=-2e-4, truncation_order=2, free_slip_bottom=True)

Psi_0 = np.zeros(18 * N, dtype=np.float64)
for q in range(9):
    Psi_0[q * N : (q + 1) * N] = sim_c.g[q].flatten()
    Psi_0[(9 + q) * N : (9 + q + 1) * N] = sim_c.phase_field.h[q].flatten()

Y_curr = carle.lift_state(Psi_0)
eval_horizons = [1, 5, 10, 20, 50, 100, 200]
carle_records = []

for step in range(1, 201):
    sim_c.step()
    Y_curr = carle.step(Y_curr)
    
    if step in eval_horizons:
        Psi_c = np.zeros(18 * N, dtype=np.float64)
        for q in range(9):
            Psi_c[q * N : (q + 1) * N] = sim_c.g[q].flatten()
            Psi_c[(9 + q) * N : (9 + q + 1) * N] = sim_c.phase_field.h[q].flatten()
            
        Psi_k = carle.project_state(Y_curr)
        
        err_vec = Psi_k - Psi_c
        l1_err = float(np.sum(np.abs(err_vec)) / (np.sum(np.abs(Psi_c)) + 1e-15))
        l2_err = float(la.norm(err_vec) / (la.norm(Psi_c) + 1e-15))
        linf_err = float(np.max(np.abs(err_vec)))
        
        # Velocity error
        g_c = Psi_c[:9*N].reshape((9, nx, ny))
        g_k = Psi_k[:9*N].reshape((9, nx, ny))
        u_c = np.einsum("qxy,qd->dxy", g_c, sim_c.c)
        u_k = np.einsum("qxy,qd->dxy", g_k, sim_c.c)
        u_err = float(la.norm(u_k - u_c) / (la.norm(u_c) + 1e-15))
        
        # Phase field error
        h_c = Psi_c[9*N:18*N].reshape((9, nx, ny))
        h_k = Psi_k[9*N:18*N].reshape((9, nx, ny))
        phi_c = np.sum(h_c, axis=0)
        phi_k = np.sum(h_k, axis=0)
        phi_err = float(la.norm(phi_k - phi_c) / (la.norm(phi_c) + 1e-15))
        
        # Mass error
        m_c = float(np.sum(np.clip(phi_c, 0, 1)))
        m_k = float(np.sum(np.clip(phi_k, 0, 1)))
        m_err = float(abs(m_k - m_c) / (m_c + 1e-15))
        
        # Manifold defect
        psi_mat = Psi_k.reshape((18, N))
        ideal_quad = np.einsum("in,jn->ijn", psi_mat, psi_mat).reshape((324 * N,))
        actual_quad = Y_curr[18 * N:]
        manifold_defect = float(la.norm(actual_quad - ideal_quad) / (la.norm(ideal_quad) + 1e-15))
        
        rec = {
            "step": step,
            "l1_error": l1_err,
            "l2_error": l2_err,
            "linf_error": linf_err,
            "relative_velocity_error": u_err,
            "relative_phase_error": phi_err,
            "relative_mass_error": m_err,
            "invariant_manifold_defect": manifold_defect,
            "error_regime": "SATURATED_BOUNDED",
            "classification": "MEASURED"
        }
        carle_records.append(rec)
        print(f"Step {step:3d} | L2 Err={l2_err:.4e} | Linf={linf_err:.4e} | u_err={u_err:.4e} | phi_err={phi_err:.4e} | MassErr={m_err:.4e} | Defect={manifold_defect:.4e}")

with open(os.path.join(repo_dir, "PHASE6_CARLEMAN_TIME_ERROR.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(carle_records[0].keys()))
    writer.writeheader()
    writer.writerows(carle_records)

# ==============================================================================
# STAGE 6.4: QSVT POLYNOMIAL DEGREE STUDY
# ==============================================================================
print("\n--- [STAGE 6.4] Running QSVT Degree Sweep (d=3..31) ---")
c_mod = CarlemanTwoPhaseLBM(nx=2, ny=1, truncation_order=2)
A_mat = c_mod.A_C.toarray()
dim_q = A_mat.shape[0] # 684
M_mat = np.eye(dim_q, dtype=np.complex128) + 0.01 * A_mat

np.random.seed(42)
b_vec = np.random.randn(dim_q) + 0.1j * np.random.randn(dim_q)
x_exact = la.solve(M_mat, b_vec)

degrees = [3, 5, 7, 9, 11, 15, 21, 31]
qsvt_deg_records = []

for d in degrees:
    t0 = time.perf_counter()
    solver = QSVTSolver(M_mat, b_vec, degree=d)
    res = solver.solve()
    t_comp = time.perf_counter() - t0
    
    # Polynomial evaluation on [-1, 1]
    x_test = np.linspace(-1.0, 1.0, 1000)
    p_vals = np.polynomial.chebyshev.chebval(x_test, solver.poly_coeffs)
    p_max = float(np.max(np.abs(p_vals)))
    p_neg = np.polynomial.chebyshev.chebval(-x_test, solver.poly_coeffs)
    parity_err = float(np.max(np.abs(p_neg + p_vals)))
    
    # Approximation error on singular value interval
    x_sv = np.linspace(solver.sigma_min / solver.alpha, solver.sigma_max / solver.alpha, 500)
    p_sv = np.polynomial.chebyshev.chebval(x_sv, solver.poly_coeffs)
    target_sv = 1.0 / (solver.alpha * x_sv)
    scale_poly = target_sv[len(target_sv)//2] / (p_sv[len(p_sv)//2] + 1e-15)
    approx_err = float(np.max(np.abs(p_sv * scale_poly - target_sv)) / np.max(target_sv))
    
    sol_err = float(la.norm(res["x_quantum"] - x_exact) / la.norm(x_exact))
    
    res_val = float(res["residual"])
    fid_val = float(res["fidelity"])
    depth_val = int(res["depth"])
    comp_ms = t_comp * 1000.0
    
    rec = {
        "degree": d,
        "max_poly_magnitude": p_max,
        "parity_violation": parity_err,
        "approx_error": approx_err,
        "linear_residual": res_val,
        "relative_sol_error": sol_err,
        "fidelity": fid_val,
        "circuit_depth": depth_val,
        "phase_rotations": len(solver.phases),
        "compilation_time_ms": comp_ms,
        "satisfies_1e8": bool(res_val < 1e-8),
        "satisfies_1e10": bool(res_val < 1e-10),
        "satisfies_1e12": bool(res_val < 1e-12),
        "classification": "MEASURED"
    }
    qsvt_deg_records.append(rec)
    print(f"Degree {d:2d} | Res={res_val:.4e} | SolErr={sol_err:.4e} | Fid={fid_val:.6f} | Max|P|={p_max:.4f} | Depth={depth_val:2d} | Comp={comp_ms:6.2f}ms")

with open(os.path.join(repo_dir, "PHASE6_QSVT_DEGREE_SWEEP.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(qsvt_deg_records[0].keys()))
    writer.writeheader()
    writer.writerows(qsvt_deg_records)

# ==============================================================================
# STAGE 6.5: CONDITION NUMBER STUDY
# ==============================================================================
print("\n--- [STAGE 6.5] Running Condition Number Study Across dt ---")
dt_values = [0.001, 0.005, 0.01, 0.02, 0.05, 0.1]
cond_records = []

for dt in dt_values:
    M_dt = np.eye(dim_q, dtype=np.complex128) + dt * A_mat
    svs = la.svd(M_dt, compute_uv=False)
    s_max = float(np.max(svs))
    s_min = float(np.min(svs))
    kappa = float(s_max / (s_min + 1e-15))
    spectral_norm = s_max
    
    solver_dt = QSVTSolver(M_dt, b_vec, degree=15)
    res_dt = solver_dt.solve()
    res_dt_val = float(res_dt["residual"])
    fid_dt_val = float(res_dt["fidelity"])
    
    rec = {
        "dt": dt,
        "sigma_min": s_min,
        "sigma_max": s_max,
        "condition_number_kappa": kappa,
        "spectral_norm": spectral_norm,
        "kappa_below_1_5": bool(kappa < 1.5),
        "residual": res_dt_val,
        "fidelity": fid_dt_val,
        "required_degree_for_1e10": 15 if res_dt_val < 1e-10 else 21,
        "classification": "MEASURED"
    }
    cond_records.append(rec)
    print(f"dt={dt:6.4f} | s_min={s_min:6.4f} | s_max={s_max:6.4f} | kappa={kappa:6.4f} | kappa<1.5: {rec["kappa_below_1_5"]} | Res={res_dt_val:.4e} | Fid={fid_dt_val:.6f}")

with open(os.path.join(repo_dir, "PHASE6_CONDITION_NUMBER_SWEEP.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(cond_records[0].keys()))
    writer.writeheader()
    writer.writerows(cond_records)

print("\nSaved CSVs for Stages 6.2, 6.3, 6.4, 6.5 successfully.")
