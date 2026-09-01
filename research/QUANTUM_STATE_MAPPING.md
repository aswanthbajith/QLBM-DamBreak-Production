# QUANTUM STATE ENCODING & AMPLITUDE NORMALIZATION MAPPING

**Date**: 2026-08-25  
**Author**: Lead Quantum-CFD Implementation Specialist  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  

---

## 1. Formal Hilbert Space Definition

For a 2D lattice of dimensions $N_x \times N_y$ with 9 discrete D2Q9 velocities and a binary phase indicator (liquid/gas), the physical state is embedded into an $n$-qubit Hilbert space $\mathcal{H} = (\mathbb{C}^2)^{\otimes n}$:

$$|\psi\rangle = \sum_{x=0}^{N_x-1} \sum_{y=0}^{N_y-1} \sum_{i=0}^8 \sum_{p \in \{0, 1\}} A(x, y, i, p) |p\rangle |i\rangle |y\rangle |x\rangle$$

### Register Allocation:
* **Spatial $X$ Register**: $n_x = \lceil \log_2 N_x \rceil$ qubits ($|x\rangle$)
* **Spatial $Y$ Register**: $n_y = \lceil \log_2 N_y \rceil$ qubits ($|y\rangle$)
* **Velocity Register**: $n_{\text{vel}} = 4$ qubits ($|i\rangle$, encoding directions $i=0 \dots 8$)
* **Phase Register**: $n_{\text{phase}} = 1$ qubit ($|p\rangle$, where $|0\rangle = \text{gas}, |1\rangle = \text{liquid}$)

For an $N_x=4, N_y=4$ lattice:
$$n_{\text{total}} = 2 + 2 + 4 + 1 = 9 \text{ qubits}, \quad \dim(\mathcal{H}) = 2^9 = 512$$

---

## 2. Mathematical Definition of Quantum Amplitudes $A(x, y, i, p)$

To ensure that quantum projective measurement probabilities directly yield physical observables, we define **Square-Root Population Amplitude Encoding**:

$$A(x, y, i, 0) = \sqrt{\frac{(1 - \phi(x, y)) f_i(x, y)}{Z}}$$
$$A(x, y, i, 1) = \sqrt{\frac{\phi(x, y) f_i(x, y)}{Z}}$$

where the global normalization partition function $Z$ is:
$$Z = \sum_{x,y} \sum_{i=0}^8 \left[ (1 - \phi(x, y)) f_i(x, y) + \phi(x, y) f_i(x, y) \right] = \sum_{x,y} \sum_{i=0}^8 f_i(x, y) = \sum_{x,y} \rho(x, y) = M_{\text{total}}$$

### Unitarity & Quantum State Normalization:
$$\langle \psi | \psi \rangle = \sum_{x,y,i,p} |A(x, y, i, p)|^2 = \frac{1}{Z} \sum_{x,y} \left( (1-\phi) \sum_i f_i + \phi \sum_i f_i \right) = \frac{M_{\text{total}}}{M_{\text{total}}} = 1$$

---

## 3. Forward Encoding Pipeline: Classical $\to$ Quantum
Given classical fields $\{\phi(x, y), f_i(x, y)\}$:
1. `validate_normalization(f, phi)`: Check $f_i \ge 0, 0 \le \phi \le 1$.
2. `normalize_distribution(f, phi)`: Compute total mass $Z = M_{\text{total}} = \sum_{x,y,i} f_i(x, y)$.
3. `encode_distribution(f, phi, layout)`:
   * Construct 512-element complex vector $v$.
   * For each $(x, y, i)$:
     * Bitstring index for gas: $\text{idx}_0 = (0 \ll 8) | (i \ll 4) | (y \ll 2) | x$
     * Bitstring index for liquid: $\text{idx}_1 = (1 \ll 8) | (i \ll 4) | (y \ll 2) | x$
     * $v[\text{idx}_0] = \sqrt{(1 - \phi(x, y)) f_i(x, y) / Z}$
     * $v[\text{idx}_1] = \sqrt{\phi(x, y) f_i(x, y) / Z}$
   * Return statevector $|\psi\rangle = v$.

---

## 4. Reverse Decoding Pipeline: Quantum Measurement $\to$ Classical Observables
When the quantum circuit is measured with $N_{\text{shots}}$ projective measurements, each bitstring $b = |p\, i\, y\, x\rangle$ yields count $C(b)$ and probability $P(b) = C(b) / N_{\text{shots}} \approx |A(x, y, i, p)|^2$.

Macroscopic fluid observables are reconstructed as:

1. **Macroscopic Density $\rho(x, y)$**:
   $$\rho(x, y) = M_{\text{total}} \sum_{i=0}^8 \left( P(0, i, y, x) + P(1, i, y, x) \right)$$

2. **Phase Indicator Field $\phi(x, y)$**:
   $$\phi(x, y) = \frac{\sum_{i=0}^8 P(1, i, y, x)}{\sum_{i=0}^8 \left( P(0, i, y, x) + P(1, i, y, x) \right)}$$

3. **Macroscopic Velocity $u(x, y) = (u_x, u_y)$**:
   $$u_x(x, y) = \frac{\sum_{i=0}^8 c_{ix} \left( P(0, i, y, x) + P(1, i, y, x) \right)}{\sum_{i=0}^8 \left( P(0, i, y, x) + P(1, i, y, x) \right)}$$
   $$u_y(x, y) = \frac{\sum_{i=0}^8 c_{iy} \left( P(0, i, y, x) + P(1, i, y, x) \right)}{\sum_{i=0}^8 \left( P(0, i, y, x) + P(1, i, y, x) \right)}$$

---

## 5. Mathematical Proof of Zero Encoding Error

Under ideal statevector sampling (infinite shots, $P(b) = |A(b)|^2$):
$$\rho_{\text{reconstructed}}(x, y) = M_{\text{total}} \sum_{i=0}^8 \left( \frac{(1-\phi) f_i}{M_{\text{total}}} + \frac{\phi f_i}{M_{\text{total}}} \right) = \sum_{i=0}^8 f_i(x, y) = \rho_{\text{classical}}(x, y)$$

$$\phi_{\text{reconstructed}}(x, y) = \frac{\sum_i \phi f_i / M_{\text{total}}}{\sum_i f_i / M_{\text{total}}} = \frac{\phi \rho}{\rho} = \phi_{\text{classical}}(x, y)$$

$$\text{Initial Encoding Relative } L_2 = \frac{\|\rho_{\text{reconstructed}} - \rho_{\text{classical}}\|_2}{\|\rho_{\text{classical}}\|_2} \equiv 0.000000000000 \quad (< 10^{-14})$$

This rigorously resolves the previous 43–57% encoding discrepancy.
