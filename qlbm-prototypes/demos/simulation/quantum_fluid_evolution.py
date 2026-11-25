"""Run a periodic 3D linearized fluid model as a postselected quantum circuit."""

import argparse
import json
from pathlib import Path

import numpy as np
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister, transpile
from qiskit.circuit.library import MCXGate, UnitaryGate
from qiskit_aer import AerSimulator

if __package__:
    from .quantum_flow_reference import (
        NUM_VELOCITY_STATES,
        VELOCITIES,
        analytic_velocity,
        equilibrium_projector,
        initial_state,
        moments,
        reference,
    )
else:
    from quantum_flow_reference import (
        NUM_VELOCITY_STATES,
        VELOCITIES,
        analytic_velocity,
        equilibrium_projector,
        initial_state,
        moments,
        reference,
    )

GRID_SIZE = 8
TIMESTEPS = 12
VELOCITY_AMPLITUDE = 0.01
SHOTS = 128
SEED = 42


def quantum_step(size):
    """Build a unitary dilation of the collision and a periodic streaming step."""
    bits = size.bit_length() - 1
    x = QuantumRegister(bits, "x")
    y = QuantumRegister(bits, "y")
    z = QuantumRegister(bits, "z")
    channel = QuantumRegister(NUM_VELOCITY_STATES.bit_length() - 1, "channel")
    flag = QuantumRegister(1, "collision_flag")
    circuit = QuantumCircuit(x, y, z, channel, flag, name="collide_and_stream")

    # The linearized BGK collision at tau=1 projects onto density and momentum
    # modes in the weighted population basis. Embed that projection in a unitary.
    conserved = equilibrium_projector()
    discarded = np.eye(NUM_VELOCITY_STATES) - conserved
    dilation = np.block([[conserved, discarded], [discarded, -conserved]])
    circuit.append(UnitaryGate(dilation, label="D3Q19 collision"), [*channel, flag[0]])

    # Apply each velocity's shift modulo the lattice length. Update high bits
    # first so carries/borrows are controlled by the original low coordinate bits.
    for index, direction in enumerate(VELOCITIES):
        for axis, increment in zip((x, y, z), direction, strict=True):
            if increment == 0:
                continue
            for bit in reversed(range(bits)):
                low_bits = axis[:bit]
                required = (1 << bit) - 1 if increment > 0 else 0
                control_state = index | (required << len(channel))
                gate = MCXGate(len(channel) + bit, ctrl_state=control_state)
                circuit.append(gate, [*channel, *low_bits, axis[bit]])
    return circuit


def evolve(initial, steps, shots, seed):
    """Evolve successive accepted states without classical fluid feedback."""
    if initial.ndim != 4 or initial.shape[0] != NUM_VELOCITY_STATES:
        raise ValueError("Expected populations with shape (32, z, y, x).")
    size = initial.shape[-1]
    if size < 2 or size & (size - 1) or initial.shape[1:] != (size,) * 3:
        raise ValueError("The cubic lattice size must be a power of two of at least 2.")
    if steps < 1 or shots < 1:
        raise ValueError("The number of steps and shots must be positive.")
    norm = np.linalg.norm(initial)
    if not np.isfinite(norm) or norm <= 0:
        raise ValueError("Initial perturbations must be finite and nonzero.")

    step_circuit = quantum_step(size)
    circuit = QuantumCircuit(*step_circuit.qregs)
    history = ClassicalRegister(steps, "collision_history")
    circuit.add_register(history)
    circuit.prepare_state(initial.ravel() / norm, circuit.qubits[:-1])
    circuit.save_statevector(label="initial")
    for timestep in range(1, steps + 1):
        # Postselection keeps flag=0, which applies the BGK projection to the
        # fluid register. Failed trajectories exit without feeding back a field.
        with circuit.if_test((history, 0)):
            circuit.compose(step_circuit, inplace=True)
            circuit.save_statevector(label=f"step_{timestep}", conditional=True)
            circuit.measure(circuit.qubits[-1], history[timestep - 1])

    backend = AerSimulator(
        method="statevector", max_parallel_threads=2, shot_branching_enable=True
    )
    compiled = transpile(circuit, backend, optimization_level=0)
    result = backend.run(compiled, shots=shots, seed_simulator=seed).result()
    if not result.success:
        raise RuntimeError(f"Aer failed to run the fluid circuit: {result.status}")

    saved = result.data(0)
    prepared = np.asarray(saved["initial"]).reshape(2, *initial.shape)[0]
    states = [prepared * norm]
    success_probability = [1.0]
    for timestep in range(1, steps + 1):
        accepted_branch = saved.get(f"step_{timestep}", {}).get("0x0")
        if accepted_branch is None:
            raise RuntimeError(f"No shots reached timestep {timestep}. Increase --shots.")
        accepted = np.asarray(accepted_branch).reshape(2, *initial.shape)[0]
        step_probability = float(np.vdot(accepted, accepted).real)
        success_probability.append(success_probability[-1] * step_probability)
        # Aer returns the normalized surviving state before the current
        # measurement. Restore its physical scale for diagnostic readout only.
        states.append(accepted * norm * np.sqrt(success_probability[-2]))

    populations = np.stack(states)
    if not np.allclose(populations.imag, 0, atol=1e-10, rtol=0):
        raise RuntimeError("Expected a real fluid population in the accepted state.")
    accepted_shots = result.get_counts(0).get("0" * steps, 0)
    if accepted_shots == 0:
        raise RuntimeError("No shots survived every collision. Increase --shots.")
    statistics = {
        "qubits": circuit.num_qubits,
        "steps": steps,
        "shots": shots,
        "accepted_shots": accepted_shots,
        "cumulative_success_probability": success_probability,
        "logical_gates_per_step": step_circuit.size(),
    }
    return populations.real, statistics


def run_benchmark(output, steps, shots):
    initial = initial_state(GRID_SIZE, VELOCITY_AMPLITUDE)
    states, statistics = evolve(initial, steps, shots, SEED)
    velocities, relative_density = moments(states)
    expected = analytic_velocity(GRID_SIZE, VELOCITY_AMPLITUDE, steps)
    classical_states = reference(initial, steps)

    projection_error = float(np.max(np.abs(classical_states - states)))
    velocity_error = float(np.max(np.abs(expected - velocities)))
    density_error = float(np.max(np.abs(relative_density - 1)))
    if max(projection_error, velocity_error, density_error) > 1e-10:
        raise RuntimeError("Circuit output diverged from the independent flow reference.")

    if __package__:
        from .quantum_flow_output import write_outputs
    else:
        from quantum_flow_output import write_outputs

    output.mkdir(parents=True, exist_ok=True)
    write_outputs(output, velocities, relative_density, expected)
    statistics.update(
        model="3D linearized D3Q19 BGK fluid with periodic boundaries",
        backend="Qiskit Aer statevector simulator",
        grid_shape=list(initial.shape[1:]),
        viscosity_lattice_units=1 / 6,
        initial_component_velocity_amplitude=VELOCITY_AMPLITUDE,
        max_error_vs_classical_populations=projection_error,
        max_error_vs_exact_lattice_velocity=velocity_error,
        max_relative_density_error=density_error,
    )
    (output / "simulation.json").write_text(json.dumps(statistics, indent=2) + "\n")
    print(
        f"{statistics['qubits']} qubits, "
        f"{statistics['accepted_shots']}/{shots} accepted shots, "
        f"maximum velocity error {velocity_error:.3g}"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--steps", default=TIMESTEPS, type=int)
    parser.add_argument("--shots", default=SHOTS, type=int)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "qlbm-output" / "quantum-fluid-3d",
    )
    args = parser.parse_args()
    run_benchmark(args.output, args.steps, args.shots)


if __name__ == "__main__":
    main()
