"""
Phase F20: Unit Test Suite for Environment Memory Scaling and Recycling.
"""

import pytest
from quantum.f20_environment import F20EnvironmentAudit


def test_environment_memory_scaling():
    """Verify constant memory footprint with environment recycling."""
    audit = F20EnvironmentAudit()
    res = audit.calculate_memory_scaling(num_nodes=16, timesteps=16, bits_per_node=288)

    assert res["is_constant_with_recycling"] == True
    assert res["recycled_env_bits"] == 16 * 288 * 2
    assert res["history_chain_bits"] == 16 * 288 * 17
