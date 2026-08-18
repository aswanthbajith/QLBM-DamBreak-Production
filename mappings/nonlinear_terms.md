# Nonlinear Term Taxonomy and Algebraic Decomposition (Level 4)

## 1. Complete Classification of Discrete Nonlinearities

The discrete two-phase evolution equation is strictly quadratic ($p=2$):
$$
\mathbf{\Psi}(t+1) = \mathbf{S} \left[ \mathbf{M}_1 \mathbf{\Psi}(t) + \mathbf{M}_2 (\mathbf{\Psi}(t) \otimes \mathbf{\Psi}(t)) + \mathbf{b}_{force}(\mathbf{\Psi}(t)) \right]
$$

### A. Hydrodynamic Convective Momentum Flux ($\mathbf{g} \otimes \mathbf{g}$)
- **Continuous form**: $\frac{(\mathbf{c}_{q^*} \cdot \mathbf{u})^2}{2 c_s^4} - \frac{|\mathbf{u}|^2}{2 c_s^2}$
- **Tensor kernel**:
  $$ (\mathbf{K}_{hydro})_{q^*, q, q'} = \frac{w_{q^*}}{\tau_v \rho_0} \left[ \frac{(\mathbf{c}_q \cdot \mathbf{c}_{q^*})(\mathbf{c}_{q'} \cdot \mathbf{c}_{q^*})}{2 c_s^4} - \frac{\mathbf{c}_q \cdot \mathbf{c}_{q'}}{2 c_s^2} \right] $$
- **Order**: Strictly quadratic polynomial ($p=2$).

### B. Phase-Field Advection ($\mathbf{h} \otimes \mathbf{g}$)
- **Continuous form**: $\frac{w_{q^*}}{\tau_\phi} \phi \frac{\mathbf{c}_{q^*} \cdot \mathbf{u}}{c_s^2}$
- **Tensor kernel**:
  $$ (\mathbf{K}_{phase})_{q^*, q, q'} = \frac{w_{q^*}}{\tau_\phi c_s^2 \rho_0} (\mathbf{c}_{q^*} \cdot \mathbf{c}_{q'}) $$
  where index $q$ contracts with phase distribution $\mathbf{h}$ and index $q'$ contracts with hydrodynamic distribution $\mathbf{g}$.
- **Order**: Strictly bilinear cross-product ($p=2$).

### C. Guo Body Force Convective Coupling ($\mathbf{g} \otimes \mathbf{h}$)
- **Continuous form**: $\left(1 - \frac{1}{2\tau_v}\right) w_i \left[ \frac{(\mathbf{c}_i \cdot \mathbf{u})(\mathbf{c}_i \cdot \mathbf{F})}{c_s^4} - \frac{\mathbf{u} \cdot \mathbf{F}}{c_s^2} \right]$
- **Order**: Strictly bilinear cross-product ($p=2$) in $\mathbf{g}$ and $\mathbf{h}$.

---

## 2. Locality and Sparsity Properties of $\mathbf{M}_2$
1. **Spatial Decoupling**:
   - $\mathbf{M}_2$ contains **zero spatial cross-derivatives**.
   - For all distinct nodes $n \neq m$:
     $$ (\mathbf{M}_2)_{(q^* n), (q_1 n_1), (q_2 n_2)} = 0 \quad \text{unless } n = n_1 = n_2 $$
2. **Kronecker Structure**:
   $$\mathbf{M}_2 = \bigoplus_{n=1}^N \mathbf{K}_{local}$$
   where $\mathbf{K}_{local} \in \mathbb{R}^{18 \times 324}$ is the compact local 18-population quadratic collision tensor.
3. **Implications for Carleman Lifting (Level 5)**:
   - The absence of non-local spatial terms in $\mathbf{M}_2$ ensures that the Carleman matrix $\mathcal{M}_K$ retains the same block sparsity pattern as standard single-phase LBM!
