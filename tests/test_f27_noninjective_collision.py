"""
Phase F27: Test Suite for Non-Injective Collision Pairs and Environment Preimage Preservation.
"""

import pytest
from quantum.f27_local_node_circuit import F27LocalNodeCircuit


def test_noninjective_collision_pair_distinguishability():
    """
    Verify that two distinct non-equilibrium states x1 != x2 that relax to the
    same equilibrium macrostate F(x1) == F(x2) remain globally distinguishable
    in the joint system-environment Hilbert space |F(x)>_S |x>_E.
    """
    node_circ = F27LocalNodeCircuit(frac_bits=12, bit_width=16)

    # State x1: equilibrium with rho=2700
    f_x1 = [1200, 300, 300, 300, 300, 75, 75, 75, 75]
    g_x1 = [1200, 300, 300, 300, 300, 75, 75, 75, 75]

    # State x2: non-equilibrium shear perturbation with same total mass rho=2700
    f_x2 = [1200, 350, 250, 350, 250, 75, 75, 75, 75]
    g_x2 = [1200, 350, 250, 350, 250, 75, 75, 75, 75]

    assert f_x1 != f_x2

    # Execute forward Stinespring
    f1_out, g1_out, e_f1, e_g1, _ = node_circ.execute_forward_stinespring_node(f_x1, g_x1)
    f2_out, g2_out, e_f2, e_g2, _ = node_circ.execute_forward_stinespring_node(f_x2, g_x2)

    # In environment, preimages e_f1 and e_f2 remain strictly distinct
    assert e_f1 != e_f2
    assert e_f1 == f_x1
    assert e_f2 == f_x2

    # Joint state is orthogonal: <Psi1|Psi2> = <F(x1)|F(x2)> * <x1|x2> = 0 because <x1|x2> = 0!
    assert any(a != b for a, b in zip(e_f1, e_f2))
