# LEVEL-5 AUDIT: INDEPENDENT MATHEMATICAL RE-DERIVATION OF LEVEL-4 SOLVER

**Target File**: [`classical/level4_two_phase.py`](file:///home/aswa/Research/QLBM-DamBreak-Production/classical/level4_two_phase.py)  
**Audit Purpose**: Direct algebraic extraction of every mathematical term in the authoritative classical two-phase solver to determine exact polynomial vs rational/piecewise structure.

---

## 1. Step-by-Step Algorithmic & Algebraic Breakdown

### Step 1: Macroscopic Moments
$$\rho(\mathbf{x}, t) = \sum_{i=0}^8 f_i(\mathbf{x}, t)$$
$$\alpha(\mathbf{x}, t) = \text{clip}\left(\sum_{i=0}^8 g_i(\mathbf{x}, t), 0.0, 1.0\right) \quad \text{\textbf{[NON-POLYNOMIAL CLIPPING]}}$$

### Step 2: Body & Surface Forces ($\mathbf{F} = \mathbf{F}_g + \mathbf{F}_s$)
1. **Gravitational Buoyancy**:
   $$\mathbf{F}_g(\mathbf{x}, t) = \begin{bmatrix} 0 \\ (\rho(\mathbf{x}, t) - \rho_G) g_{\text{acc}} \end{bmatrix} \quad \text{\textbf{[EXACTLY LINEAR IN $f$]}}$$
2. **Continuum Surface Force (CSF)**:
   $$\nabla \alpha = \left[ \frac{\alpha(x+1, y) - \alpha(x-1, y)}{2}, \frac{\alpha(x, y+1) - \alpha(x, y-1)}{2} \right]^T$$
   $$\mathbf{n} = \frac{\nabla \alpha}{\sqrt{|\nabla \alpha|^2} + 10^{-12}} \quad \text{\textbf{[NON-POLYNOMIAL SQUARE ROOT & DIVISION]}}$$
   $$\kappa = \text{clip}\left(-\nabla \cdot \mathbf{n}, -2.0, 2.0\right) \quad \text{\textbf{[NON-POLYNOMIAL CLIPPING]}}$$
   $$\mathbf{F}_s = \sigma \kappa \nabla \alpha \cdot \mathbb{I}(|\nabla \alpha| > 10^{-3}) \quad \text{\textbf{[NONLOCAL PIECEWISE MASKING]}}$$

### Step 3: Barycentric Velocity Shift & Clamping
$$\mathbf{j}(\mathbf{x}, t) = \sum_{i=0}^8 \mathbf{c}_i f_i(\mathbf{x}, t)$$
$$\mathbf{u}^* = \frac{\mathbf{j} + 0.5 \mathbf{F}}{\max(\rho, 10^{-6})} \quad \text{\textbf{[RATIONAL DIVISION BY DENSITY $\rho$]}}$$
$$\mathbf{u} = \mathbf{u}^* \cdot \min\left(1.0, \frac{0.15}{|\mathbf{u}^*| + 10^{-12}}\right) \quad \text{\textbf{[NON-POLYNOMIAL MAGNITUDE CLAMPING]}}$$

### Step 4: Phase-Dependent Viscosity & Relaxation
$$\nu_{\text{mix}}(\alpha) = \alpha \nu_L + (1-\alpha) \nu_G$$
$$\tau_f(\alpha) = 3 \nu_{\text{mix}}(\alpha) + 0.5$$
$$\omega_f(\alpha) = \frac{1}{3(\alpha \nu_L + (1-\alpha)\nu_G) + 0.5} \quad \text{\textbf{[RATIONAL DIVISION BY $\alpha$]}}$$
$$\omega_g = \frac{1}{\tau_\phi}$$

### Step 5: Equilibrium Distributions
1. **Hydrodynamic Equilibrium ($f_i^{\text{eq}}$)**:
   $$f_i^{\text{eq}}(\rho, \mathbf{u}) = w_i \rho \left[ 1 + 3(\mathbf{c}_i \cdot \mathbf{u}) + \frac{9}{2}(\mathbf{c}_i \cdot \mathbf{u})^2 - \frac{3}{2}|\mathbf{u}|^2 \right]$$
   Substituting $\mathbf{u} \approx \mathbf{j}/\rho$:
   $$f_i^{\text{eq}} = w_i \rho + 3 w_i (\mathbf{c}_i \cdot \mathbf{j}) + \frac{w_i}{\rho} \left[ \frac{9}{2}(\mathbf{c}_i \cdot \mathbf{j})^2 - \frac{3}{2}|\mathbf{j}|^2 \right] \quad \text{\textbf{[RATIONAL $j^2/\rho$]}}$$
2. **Phase Equilibrium ($g_i^{\text{eq}}$)**:
   $$g_i^{\text{eq}}(\alpha, \mathbf{u}) = w_i \alpha \left[ 1 + 3(\mathbf{c}_i \cdot \mathbf{u}) \right] = w_i \alpha + 3 w_i \frac{\alpha (\mathbf{c}_i \cdot \mathbf{j})}{\rho} \quad \text{\textbf{[RATIONAL $\alpha j / \rho$]}}$$

### Step 6: Guo Forcing Term
$$S_i = \left(1 - \frac{\omega_f}{2}\right) w_i \left[ 3(\mathbf{c}_i \cdot \mathbf{F}) + 9(\mathbf{c}_i \cdot \mathbf{u})(\mathbf{c}_i \cdot \mathbf{F}) - 3(\mathbf{u} \cdot \mathbf{F}) \right]$$

### Step 7: Streaming & Boundary Involution
$$f_i^*(\mathbf{x}, t) = f_i - \omega_f(f_i - f_i^{\text{eq}}) + S_i, \quad g_i^*(\mathbf{x}, t) = g_i - \omega_g(g_i - g_i^{\text{eq}})$$
$$f_i(\mathbf{x} + \mathbf{c}_i, t+1) = f_i^*(\mathbf{x}, t), \quad g_i(\mathbf{x} + \mathbf{c}_i, t+1) = g_i^*(\mathbf{x}, t)$$
$$\text{Solid Boundary: } f_{\text{opp}(i)}(\mathbf{x}_{\text{wall}}) = f_i^*(\mathbf{x}_{\text{wall}}), \quad g_{\text{opp}(i)}(\mathbf{x}_{\text{wall}}) = g_i^*(\mathbf{x}_{\text{wall}})$$

---

## 2. Definitive Classification of Terms

| Term / Operation | Exact Mathematical Nature | Level-5 Carleman Treatment | Nature of Carleman Approximation |
| :--- | :---: | :---: | :--- |
| $\sum f_i$ (Mass) | Linear | **Exact** | Exact in $M_1$ ($E = 0$) |
| $\mathbf{c}_i \cdot \mathbf{j}$ (Linear Momentum) | Linear | **Exact** | Exact in $M_1$ ($E = 0$) |
| $\rho - \rho_G$ (Buoyancy) | Linear | **Exact** | Exact in $M_1$ ($E = 0$) |
| $j_a j_b / \rho$ (Convective Momentum) | **Rational** | **Approximated** | Expanded around $\rho_0$: $j_a j_b / \rho_0 + \mathcal{O}(\text{Ma}^2 \delta\rho)$ in $M_2$ |
| $\alpha j_a / \rho$ (Phase Advection) | **Rational** | **Approximated** | Expanded around $\rho_0$: $\alpha j_a / \rho_0$ bilinear in $M_2$ |
| $1/\tau_f(\alpha)$ (Viscosity Relaxation) | **Rational** | **Approximated** | Fixed mean reference $\tau_0 = 3\nu_{\text{mean}} + 0.5$ in $M_1, M_2$ |
| $\text{clip}(\alpha, 0, 1)$ (Volume Fraction) | **Piecewise** | **Omitted in Linear Operator** | Enforced during quantum measurement/decoding |
| $|\mathbf{u}| \le 0.15$ (Velocity Clamping) | **Non-polynomial** | **Omitted in Linear Operator** | Assumed low-Mach $\text{Ma} < 0.1$ |
| $\mathbf{F}_s = \sigma \kappa \nabla \alpha$ (Surface Tension) | **Nonlocal / Non-polynomial** | **Hybrid Preprocessing** | Omitted from $U_C$; computed via classical stencil |

---

## 3. Audit Verdict on "Exact Quadratic Polynomialization"

> [!WARNING]
> **AUDIT FINDING**: The claim of an "exact quadratic polynomial formulation" is **scientifically invalid**.
> 
> The physical Level-4 D2Q9 solver contains **rational functions of density** ($\frac{j_a j_b}{\rho}$, $\frac{\alpha j_a}{\rho}$), **rational functions of phase fraction** ($\frac{1}{\tau_f(\alpha)}$), **non-polynomial geometric stencils** ($\kappa = -\nabla \cdot \frac{\nabla\alpha}{|\nabla\alpha|}$), and **piecewise clipping operations** ($\text{clip}(\alpha, 0, 1)$, $|\mathbf{u}| \le 0.15$).
> 
> The Level-5 Carleman system is a **second-order low-Mach weakly-compressible Taylor approximation** around $\rho_0 = 1.0$ with fixed mean relaxation $\tau_0$.
