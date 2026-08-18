# Discrete Two-Phase Lattice Boltzmann System: Exact Algebraic Evolution Map

**Author**: Lead Numerical Fluid-Dynamics Researcher  
**Target Map**: $\mathbf{\Psi}(t+1) = \mathcal{F}(\mathbf{\Psi}(t))$  
**Lattice Architecture**: Coupled D2Q9-D2Q9 Velocity-Based Interface System  

---

## 1. Global State Vector Definition
Let the spatial lattice contain $N = N_x \times N_y$ nodes. The coupled state vector is:
$$
\mathbf{\Psi}(t) = \begin{bmatrix} \mathbf{g}(t) \\ \mathbf{h}(t) \end{bmatrix} \in \mathbb{R}^{18 N}
$$
where:
- $\mathbf{g}(t) = [g_0(\mathbf{x}_1), \dots, g_0(\mathbf{x}_N), \dots, g_8(\mathbf{x}_N)]^T \in \mathbb{R}^{9 N}$ (Hydrodynamic populations)
- $\mathbf{h}(t) = [h_0(\mathbf{x}_1), \dots, h_0(\mathbf{x}_N), \dots, h_8(\mathbf{x}_N)]^T \in \mathbb{R}^{9 N}$ (Phase-field populations)

---

## 2. Step-by-Step Mathematical Operator Decomposition

The discrete time evolution $\mathbf{\Psi}(t+1) = \mathcal{F}(\mathbf{\Psi}(t))$ decomposes into 5 consecutive stages:

```
               Ψ(t) = [g(t); h(t)]
                       │
       ┌───────────────┴───────────────┐
       ▼                               ▼
 [1. Moments & Properties]     [2. Force Evaluation]
   φ = Σ h_i                     F_g = (ρ(φ) - ρ_G) g_grav
   ρ(φ) = ρ_G + φ Δρ             F_s = σ κ_I ∇φ
   τ_v(φ) = 3 ν(φ) + 0.5         F = F_g + F_s
       │                               │
       └───────────────┬───────────────┘
                       ▼
       [3. Velocity & Equilibrium State]
         u = Σ g_i c_i + (Δt / 2ρ(φ)) F
         h_i^eq = w_i φ (1 + c_i·u / c_s²)
         g_i^eq = w_i ( Σ g_k + c_i·u / c_s² + (c_i·u)² / (2 c_s⁴) - |u|² / (2 c_s²) )
                       │
                       ▼
         [4. Local Collision Operator]
         h_i^post = h_i - (1/τ_φ)(h_i - h_i^eq) + S_i(φ, u)
         g_i^post = g_i - (1/τ_v(φ))(g_i - g_i^eq) + F_i(u, F, ρ, τ_v)
                       │
                       ▼
         [5. Global Permutation Streaming & BCs]
           Ψ(t+1) = S · Ψ^post(t)
```

---

## 3. Explicit Node-Level Algebraic Formulas

### Stage 1: Moment Projections
$$ \phi(\mathbf{x}) = \sum_{q=0}^8 h_q(\mathbf{x}) $$
$$ \rho(\mathbf{x}) = \rho_G + \phi(\mathbf{x}) (\rho_L - \rho_G) $$
$$ \tau_v(\mathbf{x}) = 3 \left( \frac{\mu_G + \phi(\mathbf{x})(\mu_L - \mu_G)}{\rho(\mathbf{x})} \right) + 0.5 $$

### Stage 2: Total Body Force
$$ \mathbf{F}_g(\mathbf{x}) = \phi(\mathbf{x}) (\rho_L - \rho_G) \mathbf{g}_{grav} $$
$$ \mathbf{F}_s(\mathbf{x}) = \sigma \left[ -\nabla \cdot \left(\frac{\nabla \phi}{|\nabla \phi| + \epsilon}\right) \right] \nabla \phi $$
$$ \mathbf{F}(\mathbf{x}) = \mathbf{F}_g(\mathbf{x}) + \mathbf{F}_s(\mathbf{x}) $$

### Stage 3: Macroscopic Velocity & Normal Sharpening Flux
$$ \mathbf{u}(\mathbf{x}) = \sum_{q=0}^8 g_q(\mathbf{x}) \mathbf{c}_q + \frac{\Delta t}{2 \rho(\mathbf{x})} \mathbf{F}(\mathbf{x}) $$
$$ \mathbf{F}_\phi(\mathbf{x}) = M \left( \nabla \phi(\mathbf{x}) - \frac{1 - 4(\phi(\mathbf{x}) - 0.5)^2}{W} \frac{\nabla \phi(\mathbf{x})}{|\nabla \phi(\mathbf{x})| + \epsilon} \right) $$

### Stage 4: Collision Operators
1. **Phase Field**:
   $$ h_q^{post} = h_q - \frac{1}{\tau_\phi} \left( h_q - w_q \phi \left(1 + \frac{\mathbf{c}_q \cdot \mathbf{u}}{c_s^2}\right) \right) + \left(1 - \frac{1}{2\tau_\phi}\right) w_q \frac{\mathbf{c}_q \cdot \mathbf{F}_\phi}{c_s^2} $$
2. **Hydrodynamics**:
   $$ g_q^{post} = g_q - \frac{1}{\tau_v(\mathbf{x})} \left( g_q - w_q \left[ \sum_{k=0}^8 g_k + \frac{\mathbf{c}_q \cdot \mathbf{u}}{c_s^2} + \frac{(\mathbf{c}_q \cdot \mathbf{u})^2}{2 c_s^4} - \frac{|\mathbf{u}|^2}{2 c_s^2} \right] \right) + F_q $$
   where Guo force term is:
   $$ F_q = \left( 1 - \frac{1}{2\tau_v(\mathbf{x})} \right) w_q \left[ \frac{(\mathbf{c}_q - \mathbf{u})\cdot \mathbf{F}}{\rho(\mathbf{x}) c_s^2} + \frac{(\mathbf{c}_q \cdot \mathbf{u})(\mathbf{c}_q \cdot \mathbf{F})}{\rho(\mathbf{x}) c_s^4} \right] $$

### Stage 5: Streaming & Boundary Matrix $\mathbf{S}$
$$
\mathbf{\Psi}(t+1) = \mathbf{S} \mathbf{\Psi}^{post}(t)
$$
where $\mathbf{S} \in \{0, 1\}^{18N \times 18N}$ is the exact linear permutation and reflection matrix with $\mathbf{S}^T \mathbf{S} = \mathbf{I}$.
