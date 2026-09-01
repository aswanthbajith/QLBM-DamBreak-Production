import pytest
from quantum.carleman_collision import build_carleman_basis
from quantum.two_phase_carleman import build_two_phase_carleman_basis


class TestCarlemanBasis:
    """
    Rigorously tests Carleman Basis Configurations & Dimension Properties.
    """

    def test_01_single_phase_basis_hierarchy(self):
        b1 = build_carleman_basis(dim_base=9, order=1)
        assert b1["total_dim"] == 9
        assert b1["layer_dims"] == [9]
        
        b2 = build_carleman_basis(dim_base=9, order=2)
        assert b2["total_dim"] == 90
        assert b2["layer_dims"] == [9, 81]
        
        b3 = build_carleman_basis(dim_base=9, order=3)
        assert b3["total_dim"] == 819
        assert b3["layer_dims"] == [9, 81, 729]

    def test_02_two_phase_basis_hierarchy(self):
        b1 = build_two_phase_carleman_basis(order=1)
        assert b1["total_dim"] == 18
        assert b1["layer_dims"] == [18]
        
        b2 = build_two_phase_carleman_basis(order=2)
        assert b2["total_dim"] == 342
        assert b2["layer_dims"] == [18, 324]
