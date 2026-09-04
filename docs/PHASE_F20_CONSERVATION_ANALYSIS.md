# PHASE F20: HYDRODYNAMIC CONSERVATION ANALYSIS

## 1. Executive Summary
This document analyzes the conservation of physical invariants (mass and momentum) across the moment-space quantum collision channel $\mathcal{E}_C$.

The analytical and numerical findings establish:
1. Fluid mass $\rho = \sum_i f_i$ is conserved strictly to machine precision ($\Delta \rho < 10^{-14}$) across all tested regimes.
2. Fluid momentum $\mathbf{j} = (j_x, j_y)^T$ is conserved strictly to machine precision ($\Delta j_x < 10^{-14}, \Delta j_y < 10^{-14}$) in the absence of external forcing, and satisfies exact momentum balance $\mathbf{j}^* = \mathbf{j} + \mathbf{F}$ in the presence of external forcing.
3. Total phase mass $\Phi = \sum_{\mathbf{x}} \alpha(\mathbf{x})$ is conserved under conservative interface advection.

---

## 2. Conservation Proof at the Channel Level
In moment space, the transformation matrix $M$ defines the conserved modes as explicit linear combinations:
$$m_0 = \sum_{i=0}^8 f_i, \qquad m_3 = \sum_{i=0}^8 c_{ix} f_i, \qquad m_5 = \sum_{i=0}^8 c_{iy} f_i$$
Under the Stinespring dilation $V_m$:
$$V_m |m_0, m_3, m_5\rangle_{\text{cons}} |\mathbf{m}_{\text{neq}}\rangle |0\rangle_E = |m_0, m_3, m_5\rangle_{\text{cons}} |\mathbf{m}_{\text{neq}}^*\rangle \otimes |e(\Delta \mathbf{m}_{\text{neq}})\rangle_E$$
Because the operator acts as the identity on $\mathcal{H}_{\text{cons}}$:
$$\mathcal{E}_C(\hat{m}_0) = \text{Tr}_E(V_m^\dagger (\hat{m}_0 \otimes I_E) V_m) = \hat{m}_0$$
$$\mathcal{E}_C(\hat{m}_3) = \hat{m}_3, \qquad \mathcal{E}_C(\hat{m}_5) = \hat{m}_5$$
Mass and momentum conservation are therefore **structural invariants** of the moment-space channel representation, rather than numerical coincidences.

---

## 3. Numerical Verification Across Flow Conditions
From [`results/phase_f20/f20_conservation.csv`](file:///home/aswa/Research/QLBM-DamBreak-Production/results/phase_f20/f20_conservation.csv):

| Flow Condition | Input $\rho$ | Output $\rho$ | $|\Delta \rho|$ | $|\Delta j_x|$ | $|\Delta j_y|$ | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Rest state liquid | $1.0000$ | $1.0000$ | $0.00 \times 10^0$ | $0.00 \times 10^0$ | $0.00 \times 10^0$ | **EXACT** |
| Rest state gas | $0.1000$ | $0.1000$ | $0.00 \times 10^0$ | $0.00 \times 10^0$ | $0.00 \times 10^0$ | **EXACT** |
| Horizontal flow ($u_x = 0.05$) | $1.0000$ | $1.0000$ | $0.00 \times 10^0$ | $0.00 \times 10^0$ | $0.00 \times 10^0$ | **EXACT** |
| Diagonal surge front ($u_x=0.08, u_y=-0.06$) | $1.0000$ | $1.0000$ | $0.00 \times 10^0$ | $0.00 \times 10^0$ | $0.00 \times 10^0$ | **EXACT** |
| High shear vortex ($u_x=-0.10, u_y=0.10$) | $0.8000$ | $0.8000$ | $0.00 \times 10^0$ | $0.00 \times 10^0$ | $0.00 \times 10^0$ | **EXACT** |

In all cases, mass and momentum are preserved with machine-precision fidelity.
