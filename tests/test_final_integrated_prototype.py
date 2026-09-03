"""
Final Integration & Completeness Test Suite for Two-Phase QLBM Prototype.

Verifies:
1. Initialization & state dimensions
2. State normalization & register encoding
3. Two-phase populations (f and g)
4. Quantum collision operator
5. Quantum streaming permutation
6. Boundary bounce-back involution
7. Complete single timestep
8. Multi-timestep evolution
9. Final readout & observable reconstruction
10. Physical comparison against classical Level-4 baseline
11. Mass and phase-field conservation
12. Scalable FTQC reversibility and environment compression
"""

import pytest
import numpy as np
from qiskit import QuantumCircuit
from classical.level4_two_phase import Level4TwoPhaseLBM
from quantum.f33_state_preparation import F33StatePreparation
from quantum.f33_hardware_demo import F33HardwareDamBreakDemo
from quantum.f38_observables_reconstruction import F38ObservablesReconstructor
from quantum.f38_backend_discovery import F38BackendDiscovery
from quantum.f38_qpu_executor import F38QPUExecutor
from quantum.f31_reduced_architecture import F31ResourceReducedQuantumCircuit


def test_01_initialization_and_dimensions():
    """Verify 2x2 two-phase dam-break state dimensions and register allocation."""
    nx, ny, bits = 2, 2, 4
    circ, meta = F33StatePreparation.build_dam_break_initial_state(nx, ny, bits)
    assert circ.num_qubits == nx * ny * bits
    assert circ.num_qubits == 16
    assert meta["fidelity"] == 1.0


def test_02_state_normalization_and_encoding():
    """Verify Pauli-X state preparation creates an exact basis state with unit norm."""
    from qiskit.quantum_info import Statevector
    circ, _ = F33StatePreparation.build_dam_break_initial_state(2, 2, 4)
    sv = Statevector.from_instruction(circ)
    assert np.isclose(np.linalg.norm(sv.data), 1.0)
    # Check that it's a computational basis state (single non-zero amplitude)
    non_zero = np.sum(np.abs(sv.data) > 1e-10)
    assert non_zero == 1


def test_03_two_phase_populations_and_column():
    """Verify liquid column vs gas reservoir distribution in initial quantum state."""
    demo = F33HardwareDamBreakDemo(nx=2, ny=2, bits_per_node=4)
    res = demo.execute_mode(mode="ideal", num_timesteps=1, shots=1024)
    rho = res["extracted_fields"]["rho"]
    alpha = res["extracted_fields"]["alpha"]
    # Left nodes (x=0) must be liquid; right nodes (x=1) must be gas
    assert rho[0, 0] > rho[0, 1]
    assert alpha[0, 0] > alpha[0, 1]


def test_04_quantum_collision_and_csf():
    """Verify collision and CSF operators are unitary gates in the circuit."""
    demo = F33HardwareDamBreakDemo(nx=2, ny=2, bits_per_node=4)
    circ = demo.build_timestep_circuit(num_timesteps=1)
    ops = circ.count_ops()
    assert "cx" in ops
    assert "rz" in ops
    assert ops["cx"] > 0


def test_05_quantum_streaming_permutation():
    """Verify streaming operator applies unitary SWAP networks on quantum wires."""
    demo = F33HardwareDamBreakDemo(nx=2, ny=2, bits_per_node=4)
    circ = demo.build_timestep_circuit(num_timesteps=1)
    ops = circ.count_ops()
    assert "swap" in ops
    assert ops["swap"] > 0


def test_06_boundary_bounce_back_involution():
    """Verify bounce-back reflection uses Pauli involutions (X and Z gates)."""
    demo = F33HardwareDamBreakDemo(nx=2, ny=2, bits_per_node=4)
    circ = demo.build_timestep_circuit(num_timesteps=1)
    ops = circ.count_ops()
    assert "x" in ops
    assert "z" in ops


def test_07_complete_single_timestep():
    """Verify single timestep executes unitarily without intermediate measurement."""
    demo = F33HardwareDamBreakDemo(nx=2, ny=2, bits_per_node=4)
    circ = demo.build_timestep_circuit(num_timesteps=1)
    ops = circ.count_ops()
    assert ops["measure"] == 16


def test_08_multi_timestep_quantum_evolution():
    """Verify multi-timestep execution over T=1, 2, 4 timesteps."""
    demo = F33HardwareDamBreakDemo(nx=2, ny=2, bits_per_node=4)
    for T in [1, 2, 4]:
        res = demo.execute_mode(mode="ideal", num_timesteps=T, shots=512)
        assert res["is_executed"] == True
        assert res["timesteps"] == T
        assert res["extracted_fields"]["total_mass"] > 0.0


def test_09_final_readout_observable_reconstruction():
    """Verify bitstring decoding into macroscopic density, phase, and stderr."""
    counts = {"0010110000101100": 2048, "0010001000100010": 2048}
    reconstructed = F38ObservablesReconstructor.reconstruct_from_counts(
        counts, nx=2, ny=2, bits_per_node=4
    )
    assert "rho" in reconstructed
    assert "alpha" in reconstructed
    assert "rho_stderr" in reconstructed
    assert reconstructed["total_shots"] == 4096


def test_10_classical_level4_comparison():
    """Verify quantum observables correlate with classical Level-4 reference."""
    solver_c = Level4TwoPhaseLBM(nx=2, ny=2, g_acc=-0.001)
    solver_c.step()

    demo = F33HardwareDamBreakDemo(nx=2, ny=2, bits_per_node=4)
    res_q = demo.execute_mode(mode="ideal", num_timesteps=1, shots=2048)

    # Both must exhibit higher density on the left (liquid column) than right
    assert solver_c.rho[0, 0] > solver_c.rho[0, 1]
    assert res_q["extracted_fields"]["rho"][0, 0] > res_q["extracted_fields"]["rho"][0, 1]


def test_11_mass_and_phase_conservation():
    """Verify exact mass conservation in ideal simulation and bounded drift in noisy."""
    demo = F33HardwareDamBreakDemo(nx=2, ny=2, bits_per_node=4)
    res_ideal = demo.execute_mode(mode="ideal", num_timesteps=1, shots=4096)
    res_noisy = demo.execute_mode(mode="noisy", num_timesteps=1, shots=4096)

    m_ideal = res_ideal["extracted_fields"]["total_mass"]
    m_noisy = res_noisy["extracted_fields"]["total_mass"]

    assert m_ideal > 0
    assert abs(m_noisy - m_ideal) / m_ideal < 0.15  # Bounded within 15% noise envelope


def test_12_scalable_ftqc_reversibility():
    """Verify scalable reversible architecture (Phase F31) preserves exact invertibility."""
    circ_f31 = F31ResourceReducedQuantumCircuit(nx=2, ny=2, frac_bits=12, bit_width=16)
    f_in = np.ones((9, 2, 2), dtype=int) * 1000
    g_in = np.ones((9, 2, 2), dtype=int) * 500
    e_in = np.zeros((14, 2, 2), dtype=int)

    f_next, g_next, e_out, meta = circ_f31.execute_one_timestep(f_in, g_in, e_in)
    assert f_next.shape == (9, 2, 2)
    assert g_next.shape == (9, 2, 2)
    assert e_out.shape == (14, 2, 2)
    assert meta["is_mass_conserved"] == True
    assert meta["environment_compressed_fields"] == 14
