# Dam-Break Benchmark Geometries and Validation Parameters

## 1. Physical Domain & Geometry
Standard 2D rectangular tank with length $L$ and height $H$.
Initial water column of width $a$ and height $b$ situated at the left wall ($x \in [0, a], y \in [0, b]$).

Typical classic setups:
- **Martin & Moyce (1952) Benchmark**: $a = 0.05715\text{ m}, b = 0.05715\text{ m}$ (or $a = 0.114\text{ m}, b = 0.05715\text{ m}$).
- **Zhou et al. / Watanabe & Hu (2026) Setup**:
  - Tank: $L = 4a$, $H = 3a$ (or with obstacle of dimension $w_{obs} \times h_{obs}$ placed downstream at $x = x_{obs}$).
  - Sensors:
    - Impact pressure sensor P1 on right/obstacle wall: $(x_{p1}, y_{p1})$.
    - Wavefront tracking: $x_{front}(t)$.
    - Remaining column height: $h(t)$.

## 2. Dimensionless Numbers & Scaling
- **Froude Number**:
$$ Fr = \frac{U}{\sqrt{g b}} \sim 1 $$
- **Reynolds Number**:
$$ Re = \frac{\rho_l \sqrt{g b} b}{\mu_l} $$
- **Weber Number**:
$$ We = \frac{\rho_l g b^2}{\sigma} $$
- **Density Ratio**:
$$ r_\rho = \frac{\rho_l}{\rho_g} \approx 800 - 1000 $$
- **Viscosity Ratio**:
$$ r_\mu = \frac{\mu_l}{\mu_g} \approx 50 - 100 $$

## 3. Dimensionless Time & Distance
$$
t^* = t \sqrt{\frac{g}{b}}, \quad x^* = \frac{x}{b}, \quad y^* = \frac{y}{b}, \quad p^* = \frac{p}{\rho_l g b}
$$

## 4. Primary Validation Targets
1. Dimensionless surge front position $x^*(t^*)$ vs. experimental data ($x^* \approx 2 t^*$ initially).
2. Residual column height $h^*(t^*)$ vs. experimental decay curve.
3. First impact pressure peak magnitude $p_{max}^*$ and arrival time $t_{impact}^*$ on downstream obstacle/wall.
4. Second impact/splash-up pressure peak and cavity entrapment dynamics.
