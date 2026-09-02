"""
Phase F25: Multi-Scale Scaling Analysis, Bottleneck Ranking, and Literature Comparison.

Compares:
1. Precision Scaling (Q4.8 vs Q4.12 vs Q4.16 vs Q4.20)
2. Spatial Lattice Scaling (2x2 up to 128x64)
3. Quantitative Bottleneck Hierarchy
4. Architectural Comparison with Existing Literature.
"""

from typing import Dict, Any, List
from quantum.f25_gate_resource_model import F25GateResourceModel


class F25ScalingAnalysis:
    """
    Rigorously analyzes precision convergence, spatial scaling, and computational bottlenecks.
    """

    @staticmethod
    def get_precision_scaling_table() -> List[Dict[str, Any]]:
        """
        Calculates resource progression across precision formats.
        """
        table = []
        for name, bits in [("Q4.8", 12), ("Q4.12", 16), ("Q4.16", 20), ("Q4.20", 24)]:
            res = F25GateResourceModel.calculate_node_gate_resources(bit_width=bits)
            table.append({
                "format": name,
                "total_bits": bits,
                "qubits_per_node": res["logical_qubits_node"],
                "toffolis_per_node": res["toffoli_count_node"],
                "t_gates_per_node": res["t_gate_count_node"],
                "t_depth_per_node": res["t_depth_node"],
            })
        return table

    @staticmethod
    def get_spatial_scaling_table(bit_width: int = 16, timesteps: int = 32) -> List[Dict[str, Any]]:
        """
        Calculates lattice scaling across standard grid domains.
        """
        domains = [(2, 2), (4, 4), (8, 8), (16, 16), (32, 32), (64, 64), (128, 64)]
        table = []
        for nx, ny in domains:
            lat = F25GateResourceModel.calculate_lattice_resources(
                nx=nx, ny=ny, bit_width=bit_width, timesteps=timesteps
            )
            table.append(lat)
        return table

    @staticmethod
    def rank_computational_bottlenecks() -> List[Dict[str, Any]]:
        """
        Ranks the physical and gate-level implementation bottlenecks from highest to lowest.
        """
        return [
            {
                "rank": 1,
                "component": "D2Q9 Maxwell-Boltzmann Polynomial Multiplications",
                "impact": "Requires 28 fixed-point multipliers per node (~7,168 Toffolis/node/step)",
                "bottleneck_type": "Arithmetic Volume",
            },
            {
                "rank": 2,
                "component": "Reversible CSF Curvature & Normal Division Stencils",
                "impact": "Requires 2 non-restoring dividers + 1 square root (~4,736 Toffolis/node/step)",
                "bottleneck_type": "Nonlinear Arithmetic",
            },
            {
                "rank": 3,
                "component": "Fluid Velocity Division (u = j / rho)",
                "impact": "Requires Newton-Raphson reciprocal iterations (~3,584 Toffolis/node/step)",
                "bottleneck_type": "Reciprocal Latency",
            },
            {
                "rank": 4,
                "component": "Logical Qubit Footprint (624 qubits/node)",
                "impact": "For 128x64 lattice (8,192 nodes), requires 5.11 million logical qubits",
                "bottleneck_type": "Hardware Memory Scale",
            },
        ]
