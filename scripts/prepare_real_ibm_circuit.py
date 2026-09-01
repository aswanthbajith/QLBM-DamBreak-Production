#!/usr/bin/env python3
"""
IBM Quantum ISA Circuit Preparation & Transpilation Analysis.

Transpiles the reduced two-phase dam-break quantum circuit to IBM Quantum ISA
using generate_preset_pass_manager and reports comprehensive architectural metrics.
"""
import argparse
import os
import sys
import time
import json
from qiskit import transpile
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

# Add root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from quantum.two_phase_encoding import get_two_phase_register_layout, quantum_initialize_two_phase_dambreak
from quantum.two_phase_collision import build_two_phase_collision_circuit
from quantum.streaming import build_two_phase_streaming_circuit
from quantum.two_phase_boundary import build_two_phase_boundary_circuit
from backends.fake_ibm_backend import get_fake_ibm_backend


def parse_args():
    parser = argparse.ArgumentParser(description="Prepare Real IBM ISA Quantum Circuit")
    parser.add_argument("--nx", type=int, default=4, help="Grid nodes in X (default: 4)")
    parser.add_argument("--ny", type=int, default=4, help="Grid nodes in Y (default: 4)")
    parser.add_argument("--timesteps", type=int, default=1, help="Number of timesteps (default: 1)")
    parser.add_argument("--opt_level", type=int, default=1, help="Transpiler optimization level (default: 1)")
    return parser.parse_args()


def main():
    args = parse_args()
    print("============================================================")
    print("PREPARING IBM QUANTUM ISA CIRCUIT FOR TWO-PHASE DAM-BREAK")
    print(f"Mesh: {args.nx} x {args.ny}")
    print(f"Timesteps: {args.timesteps}")
    print(f"Transpiler Optimization Level: {args.opt_level}")
    print("============================================================")

    # 1. Build uncompiled quantum circuit
    layout = get_two_phase_register_layout(args.nx, args.ny)
    qc, state, total_mass, _ = quantum_initialize_two_phase_dambreak(args.nx, args.ny)
    
    coll = build_two_phase_collision_circuit(layout)
    stream = build_two_phase_streaming_circuit(layout)
    bnd = build_two_phase_boundary_circuit(layout)
    
    for t in range(args.timesteps):
        qc.append(coll, range(layout["total_qubits"]))
        qc.append(stream, range(layout["total_qubits"]))
        qc.append(bnd, range(layout["total_qubits"]))
        
    qc.measure_all()
    
    orig_qubits = qc.num_qubits
    orig_depth = qc.depth()
    orig_gate_counts = dict(qc.count_ops())
    
    print(f"Original Logical Circuit:")
    print(f"  Logical Qubits:      {orig_qubits}")
    print(f"  Original Depth:      {orig_depth}")
    print(f"  Gate Count Breakdown: {orig_gate_counts}")

    # 2. Get Target Hardware Backend (Fake IBM Eagle 127Q Heavy-Hex)
    backend = get_fake_ibm_backend()
    backend_name = backend.name if hasattr(backend, "name") else "ibm_eagle_generic_127q"
    num_physical_qubits = backend.num_qubits if hasattr(backend, "num_qubits") else 127
    
    # 3. Transpile to IBM ISA
    print(f"\n--- Transpiling to IBM ISA Target ({backend_name}) ---")
    start_time = time.time()
    try:
        pm = generate_preset_pass_manager(backend=backend, optimization_level=args.opt_level)
        isa_qc = pm.run(qc)
    except Exception:
        isa_qc = transpile(qc, backend=backend, optimization_level=args.opt_level)
    transpile_duration = time.time() - start_time
    
    isa_depth = isa_qc.depth()
    isa_gate_counts = dict(isa_qc.count_ops())
    two_qubit_count = sum(count for gate, count in isa_gate_counts.items() if gate in ["cx", "cz", "ecr"])
    measure_count = isa_gate_counts.get("measure", 0)

    print(f"ISA Compiled Circuit:")
    print(f"  Backend Target:      {backend_name} ({num_physical_qubits} physical qubits)")
    print(f"  ISA Circuit Depth:   {isa_depth}")
    print(f"  Two-Qubit Gates:     {two_qubit_count}")
    print(f"  Measurement Ops:     {measure_count}")
    print(f"  ISA Gate Breakdown:  {isa_gate_counts}")
    print(f"  Transpilation Time:  {transpile_duration:.3f} s")

    # 4. Save Report
    out_dir = os.path.join(os.path.dirname(__file__), "..", "results/two_phase")
    os.makedirs(out_dir, exist_ok=True)
    
    report = {
        "mesh": f"{args.nx}x{args.ny}",
        "timesteps": args.timesteps,
        "backend": backend_name,
        "logical_qubits": orig_qubits,
        "physical_qubits": num_physical_qubits,
        "original_depth": orig_depth,
        "isa_depth": isa_depth,
        "two_qubit_gates": two_qubit_count,
        "measurement_operations": measure_count,
        "transpilation_time_seconds": transpile_duration,
        "isa_gate_breakdown": isa_gate_counts
    }
    
    with open(os.path.join(out_dir, "ibm_isa_circuit_report.json"), "w") as f:
        json.dump(report, f, indent=2)

    print("============================================================")
    print(f"ISA preparation complete. Report saved in: {out_dir}/ibm_isa_circuit_report.json")
    print("============================================================")


if __name__ == "__main__":
    main()
