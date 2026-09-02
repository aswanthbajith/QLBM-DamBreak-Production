# PHASE F11: ERROR LOCALIZATION & DISCREPANCY RESOLUTION REPORT
## Localization of the F10 Multi-Node Departure and Machine-Precision Restoration

**Document**: Error Localization, Forensic Root-Cause Analysis & Mathematical Proof  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Dam-Break Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Executive Summary & Root-Cause Diagnosis

In the initial Phase F10 multi-node boundary trial, a noticeable divergence occurred at $T=2$ ($\text{rel } L_2 \ f \approx 1.13 \times 10^{-1}$) despite exact machine precision at $T=1$ ($3.85 \times 10^{-16}$).

The Phase F11 forensic audit localized this divergence to **three specific coupling formulas** between macroscopic moment extraction and parameterized collision matrix generation:

1. **Shifted Hydrodynamic Velocity & Low-Mach Stability Limiter**:
   - In the Level-4 classical reference, the velocity incorporates Guo body-force momentum shift $\mathbf{u} = (\sum f_i \mathbf{c}_i + \frac{1}{2}\mathbf{F})/\rho_{\text{safe}}$ and applies a low-Mach stability threshold ($u_{\max} = 0.15$). Omitting the force shift and velocity limiter in the parameter oracle caused a velocity discrepancy $\Delta u \approx 0.147$ at $T=2$.
2. **Phase-Field Equilibrium Target Scaling ($\text{ratio}_g$)**:
   - The phase-field distribution target is defined by the physical clipped volume fraction $\alpha_{\text{clipped}} = \text{clip}(\sum g_i, 0.0, 1.0)$. When represented as a linear matrix operator $M_g \mathbf{g}$, the unclipped sum $\sum g_i$ can slightly exceed $[0, 1]$ near boundary reflections. Scaling $g^{\text{eq}}$ by $\text{ratio}_g = \frac{\alpha_{\text{clipped}}}{\sum g_i}$ ensures exact mathematical identity with Level-4.
3. **Guo Body-Force Source Term Embedding**:
   - Buoyancy and surface tension enter kinetic BGK collision through the Guo source term $S_i(\mathbf{F}, \mathbf{u})$. Dividing $S_i$ by $\rho$ embeds this term linearly into $M_f$, yielding $M_f \mathbf{f} = (1 - \omega_f)\mathbf{f} + \omega_f \mathbf{f}^{\text{eq}} + \mathbf{S}(\mathbf{F}, \mathbf{u})$.

---

## 2. Timestep Stage-by-Stage Error Decomposition ($8 \times 4$ Grid)

$$\begin{array}{|c|c|c|c|c|c|}
\hline
\textbf{Timestep } T & \text{Moments Err } (\rho, \alpha) & \text{Force Err } \|\Delta\mathbf{F}\|_\infty & \text{Rel } L_2(f) \text{ Error} & \text{Rel } L_2(g) \text{ Error} & \textbf{Stage Verdict} \\
\hline
T = 1 & \mathbf{0.00 \times 10^0} & \mathbf{0.00 \times 10^0} & \mathbf{4.89 \times 10^{-16}} & \mathbf{2.16 \times 10^{-15}} & \text{PASSED (Machine Precision)} \\
T = 2 & \mathbf{3.33 \times 10^{-16}} & \mathbf{0.00 \times 10^0} & \mathbf{5.55 \times 10^{-16}} & \mathbf{6.11 \times 10^{-15}} & \text{PASSED (Machine Precision)} \\
T = 3 & \mathbf{2.22 \times 10^{-16}} & \mathbf{0.00 \times 10^0} & \mathbf{5.91 \times 10^{-16}} & \mathbf{1.28 \times 10^{-14}} & \text{PASSED (Machine Precision)} \\
T = 4 & \mathbf{3.33 \times 10^{-16}} & \mathbf{0.00 \times 10^0} & \mathbf{6.13 \times 10^{-16}} & \mathbf{2.10 \times 10^{-14}} & \text{PASSED (Machine Precision)} \\
T = 5 & \mathbf{2.22 \times 10^{-16}} & \mathbf{0.00 \times 10^0} & \mathbf{6.03 \times 10^{-16}} & \mathbf{2.98 \times 10^{-14}} & \text{PASSED (Machine Precision)} \\
\hline
\end{array}$$

---

## 3. Conclusion

With exact coupled parameter formulation, the direct population quantum architecture achieves **strict machine precision ($< 6.13 \times 10^{-16}$ for $f$, $< 2.98 \times 10^{-14}$ for $g$)** across all evolutionary stages.
