"""
Phase F27: Test Suite for Stinespring Local Node Transformation and Adjoint Inversion.
"""

import pytest
from quantum.f27_local_node_circuit import F27LocalNodeCircuit


def test_local_node_stinespring_and_inverse():
    """Verify forward transformation, environment storage, and inverse exactness."""
    node_circ = F27LocalNodeCircuit(frac_bits=12, bit_width=16)

    f_in = [1800, 450, 450, 450, 450, 110, 110, 110, 110]
    g_in = [1800, 450, 450, 450, 450, 110, 110, 110, 110]
    f_ext = (12, -6)

    f_out, g_out, e_f, e_g, meta_fwd = node_circ.execute_forward_stinespring_node(f_in, g_in, F_ext=f_ext)

    assert meta_fwd["is_mass_conserved"] == True
    assert meta_fwd["is_workspace_clean"] == True
    assert meta_fwd["environment_preserved"] == True

    f_restored, g_restored, e_f_rst, e_g_rst, meta_inv = node_circ.execute_inverse_stinespring_node(
        f_out, g_out, e_f, e_g, F_ext=f_ext
    )

    assert f_restored == f_in
    assert g_restored == g_in
    assert meta_inv["environment_reset_to_zero"] == True
