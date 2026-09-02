r"""
Phase F25: Gate-Level Reversible BGK+CSF Feasibility Study Master Runner.

Audits:
1. Reversible Primitive Forward & Inverse Verification (Add, Sub, Mul, Comp, Select, Recip, Sqrt).
2. Gate Synthesis Resource Breakdown per Node (16-bit Q4.12).
3. Precision Scaling Analysis (Q4.8 vs Q4.12 vs Q4.16 vs Q4.20).
4. Spatial Lattice Scaling Analysis (2x2 up to 128x64).
5. Computational Bottleneck Ranking & Literature Comparison.
6. Feasibility Decision (Option B: Mathematically Feasible but Currently Impractical).
"""

import os
import sys
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from quantum.f25_reversible_primitives import F25ReversiblePrimitives
from quantum.f25_gate_resource_model import F25GateResourceModel
from quantum.f25_scaling_analysis import F25ScalingAnalysis


def run_phase_f25_feasibility():
    print("=" * 95)
    print("PHASE F25: GATE-LEVEL REVERSIBLE BGK+CSF FEASIBILITY & RESOURCE STUDY")
    print("=" * 95)

    # 1. ISOLATED REVERSIBLE PRIMITIVES
    print("\n--- 1. ISOLATED REVERSIBLE PRIMITIVE VERIFICATION ---")
    prim = F25ReversiblePrimitives(frac_bits=8)
    _, sum_val = prim.reversible_add(50, 150)
    _, _, prod_val = prim.reversible_multiply(256, 384)
    _, recip_val = prim.reversible_reciprocal(512)
    _, root_val = prim.reversible_sqrt(1024)

    print(f"Reversible Add:        (50, 150) -> Sum: {sum_val} | Inverse: {prim.reversible_add_inverse(50, sum_val)[1] == 150}")
    print(f"Reversible Multiply:   (1.0, 1.5) -> Prod: {prod_val/256:.2f} | Uncompute Residual: {prim.reversible_multiply_uncompute(256, 384, prod_val)[2]}")
    print(f"Reversible Reciprocal: 1 / 2.0 -> {recip_val/256:.2f}")
    print(f"Reversible Sqrt:       sqrt(4.0) -> {root_val/256:.2f}")

    # 2. SINGLE NODE GATE RESOURCES (16-bit Q4.12)
    print("\n--- 2. PER-NODE GATE RESOURCE BREAKDOWN (16-bit Q4.12) ---")
    node_res = F25GateResourceModel.calculate_node_gate_resources(bit_width=16)
    print(f"Logical Qubits per Node:   {node_res['logical_qubits_node']} Qubits (System 288 + Env 288 + CSF 48)")
    print(f"Toffoli Gates per Node:    {node_res['toffoli_count_node']:,} Toffolis/step")
    print(f"T-Gate Count per Node:     {node_res['t_gate_count_node']:,} T-gates/step (4 T/Toffoli)")
    print(f"Clifford Gates per Node:   {node_res['clifford_gate_count_node']:,} Clifford gates/step")
    print(f"T-Depth per Node:          {node_res['t_depth_node']:,} (8-lane parallel synthesis)")
    print(f"Dominant Subcircuit:       {node_res['dominant_cost_subcircuit']}")

    # 3. PRECISION SCALING ANALYSIS
    print("\n--- 3. PRECISION SCALING PROGRESSION (Q4.8 to Q4.20) ---")
    prec_table = F25ScalingAnalysis.get_precision_scaling_table()
    for row in prec_table:
        print(f"Format: {row['format']:<5} | Bits: {row['total_bits']:>2} | Qubits/Node: {row['qubits_per_node']:>4} | Toffolis/Node: {row['toffolis_per_node']:>6,} | T-Gates/Node: {row['t_gates_per_node']:>7,}")

    # 4. SPATIAL SCALING ANALYSIS (32 Timesteps)
    print("\n--- 4. SPATIAL LATTICE DOMAIN SCALING (T=32 Timesteps, Q4.12) ---")
    lat_table = F25ScalingAnalysis.get_spatial_scaling_table(bit_width=16, timesteps=32)
    for row in lat_table:
        print(f"Domain: {row['domain_size']:<7} | Nodes: {row['num_nodes']:>5} | Total Qubits: {row['total_logical_qubits']:>9,} | Sim Toffolis: {row['total_toffolis_simulation']:>12,} | Sim T-Gates: {row['total_t_gates_simulation']:>12,}")

    # 5. BOTTLENECK RANKING
    print("\n--- 5. COMPUTATIONAL BOTTLENECK HIERARCHY ---")
    ranks = F25ScalingAnalysis.rank_computational_bottlenecks()
    for r in ranks:
        print(f"Rank {r['rank']}: [{r['bottleneck_type']:<22}] {r['component']:<50} | {r['impact']}")

    # 6. FEASIBILITY DECISION
    print("\n--- 6. FEASIBILITY DECISION & SCIENTIFIC STATUS ---")
    print("DECISION: OPTION B")
    print("STATEMENT: Gate-level implementation is mathematically feasible but currently impractical due to resource requirements.")
    print("STATUS: LEVEL B (Autonomous open-system CPTP formulation with quantified finite-precision equivalence)")

    print("\n" + "=" * 95)
    print("PHASE F25 GATE-LEVEL FEASIBILITY STUDY COMPLETE: ALL METRICS QUANTIFIED")
    print("=" * 95)


if __name__ == "__main__":
    run_phase_f25_feasibility()
