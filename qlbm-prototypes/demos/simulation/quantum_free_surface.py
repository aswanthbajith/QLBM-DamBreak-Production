"""Evolve a 3D wet-bed release with a quantum linear free-surface model."""

import argparse
import json
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, transpile
from qiskit.circuit.library import UnitaryGate
from qiskit_aer import AerSimulator
from scipy.integrate import solve_ivp

if __package__:
    from .quantum_free_surface_model import FreeSurfaceModel
else:
    from quantum_free_surface_model import FreeSurfaceModel

GRID_SIZE = 8
VERTICAL_CELLS = 4
SPACING_M = 0.25
HEAD_DIFFERENCE_M = 0.16
GRAVITY_M_S2 = 9.81
WATER_DENSITY_KG_M3 = 1000.0
TIME_STEP_S = 0.04
STEPS = 30


def narrow_gate(open_breach=True):
    """Set up a tank initially at rest with a higher water level upstream."""
    wall = GRID_SIZE // 2
    wet = np.ones((GRID_SIZE, GRID_SIZE), dtype=bool)
    wet[:, wall] = False
    if open_breach:
        wet[wall - 1 : wall + 1, wall] = True
    model = FreeSurfaceModel(wet, VERTICAL_CELLS, SPACING_M)
    x = np.where(wet)[1]
    eta = np.where(x < wall, HEAD_DIFFERENCE_M / 2, -HEAD_DIFFERENCE_M / 2)
    return model, eta - eta.mean()


def evolve_surface(model, initial_elevation, time_step, steps, gravity=GRAVITY_M_S2):
    """Decode elevation and velocity-potential snapshots from one circuit."""
    if steps < 1 or not np.isfinite(time_step) or time_step <= 0:
        raise ValueError("A positive timestep and at least one step are required.")
    if not np.isfinite(gravity) or gravity <= 0:
        raise ValueError("Gravity must be positive and finite.")
    operator = model.surface_operator
    size = len(operator)
    elevation = np.asarray(initial_elevation, dtype=float)
    if elevation.shape != (size,) or not np.isfinite(elevation).all():
        raise ValueError("Initial elevation must be finite at every open surface cell.")

    # For eta_t = G phi and phi_t = -g eta, use energy coordinates
    # a = sqrt(g) eta and b = sqrt(G) phi. The resulting generator is
    # skew-symmetric, so the propagator is unitary in the encoded basis.
    eigenvalues, modes = np.linalg.eigh(operator)
    tolerance = np.finfo(float).eps * size * max(1.0, np.max(np.abs(eigenvalues)))
    if np.min(eigenvalues) < -tolerance:
        raise ValueError("The discrete surface operator must be positive semidefinite.")
    positive = eigenvalues > tolerance
    roots = np.sqrt(np.where(positive, eigenvalues, 0))
    inverse_roots = np.divide(1, roots, out=np.zeros_like(roots), where=positive)
    inverse_root = (modes * inverse_roots) @ modes.T

    angle = np.sqrt(gravity) * time_step * roots
    coordinate_bits = (size - 1).bit_length()
    padded_size = 1 << coordinate_bits
    cosine = np.eye(padded_size)
    sine = np.zeros_like(cosine)
    cosine[:size, :size] = (modes * np.cos(angle)) @ modes.T
    sine[:size, :size] = (modes * np.sin(angle)) @ modes.T
    propagator = np.block([[cosine, sine], [-sine, cosine]])

    initial = np.zeros(2 * padded_size)
    initial[:size] = np.sqrt(gravity) * elevation
    scale = np.linalg.norm(initial)
    reg = QuantumRegister(coordinate_bits, "surface_cell")
    component = QuantumRegister(1, "surface_component")
    circuit = QuantumCircuit(reg, component)
    # A zero release remains at rest. The encoded state can be arbitrary in
    # that case because the physical scale used at readout is exactly zero.
    if scale:
        circuit.prepare_state(initial / scale, circuit.qubits)
    circuit.save_statevector(label="step_0")
    gate = UnitaryGate(propagator, label="gravity and free surface")
    for step in range(1, steps + 1):
        circuit.append(gate, circuit.qubits)
        circuit.save_statevector(label=f"step_{step}")

    backend = AerSimulator(method="statevector", max_parallel_threads=2)
    compiled = transpile(circuit, backend, optimization_level=0)
    result = backend.run(compiled, shots=1).result()
    if not result.success:
        raise RuntimeError(f"Aer failed to run the surface circuit: {result.status}")
    readout = result.data(0)
    states = scale * np.stack(
        [np.asarray(readout[f"step_{step}"]) for step in range(steps + 1)]
    ).reshape(-1, 2, padded_size)
    if np.max(np.abs(states.imag)) > 1e-10:
        raise RuntimeError("The circuit produced an unexpected imaginary component.")
    if np.any(np.abs(states[..., size:]) > 1e-10):
        raise RuntimeError("The circuit leaked into padded surface coordinates.")
    states = states.real[:, :, :size]
    eta = states[:, 0] / np.sqrt(gravity)
    phi = states[:, 1] @ inverse_root.T
    return eta, phi, circuit.num_qubits


def validate(model, eta, phi, initial_elevation, times):
    """Check the circuit against an independent integration in physical variables."""
    size = len(initial_elevation)
    operator = model.surface_operator

    def derivative(_time, state):
        return np.concatenate((operator @ state[size:], -GRAVITY_M_S2 * state[:size]))

    initial = np.concatenate((initial_elevation, np.zeros_like(initial_elevation)))
    reference = solve_ivp(
        derivative, (0, times[-1]), initial, t_eval=times,
        rtol=1e-11, atol=1e-13, method="DOP853",
    )
    if not reference.success:
        raise RuntimeError(reference.message)
    eta_error = np.max(np.abs(eta - reference.y[:size].T))
    # A spatially constant offset in the potential is a gauge for the velocity.
    surface_speed_error = np.max(np.abs((phi - reference.y[size:].T) @ operator))
    volumes = model.spacing**2 * (model.depth + eta).sum(axis=1)
    energies = (
        0.5 * WATER_DENSITY_KG_M3 * model.spacing**2
        * (GRAVITY_M_S2 * np.sum(eta**2, axis=1) + np.sum(phi * (phi @ operator), axis=1))
    )
    volume_error = np.max(np.abs(volumes - volumes[0]))
    energy_error = np.max(np.abs(energies - energies[0]))
    if max(eta_error, surface_speed_error, volume_error, energy_error) > 1e-8:
        raise RuntimeError("Surface evolution failed its numerical checks.")

    return {
        "initial_water_volume_m3": float(volumes[0]),
        "maximum_volume_drift_m3": float(volume_error),
        "initial_wave_energy_j": float(energies[0]),
        "maximum_wave_energy_drift_j": float(energy_error),
        "maximum_elevation_error_vs_reference_m": float(eta_error),
        "maximum_surface_velocity_error_vs_reference_m_s": float(surface_speed_error),
    }


def run_demo(output, steps, time_step):
    model, initial_elevation = narrow_gate()
    eta, phi, qubits = evolve_surface(model, initial_elevation, time_step, steps)
    times = np.arange(steps + 1) * time_step
    report = validate(model, eta, phi, initial_elevation, times)

    heights = np.zeros((len(times), *model.wet.shape))
    heights[:, model.wet] = eta + model.depth
    velocities = model.flow_velocity(phi)
    u, v, w = model.face_velocity(phi)
    wall_column = GRID_SIZE // 2
    gate_flux = u[..., wall_column].sum(axis=(1, 2)) * model.spacing**2
    downstream = np.where(model.wet)[1] >= wall_column
    surface_rate = phi @ model.surface_operator
    downstream_rate = surface_rate[:, downstream].sum(axis=1) * model.spacing**2
    discharge_error = np.max(np.abs(downstream_rate - gate_flux))
    continuity_error = np.max(np.abs(
        np.diff(u, axis=-1) + np.diff(v, axis=-2) + np.diff(w, axis=-3)
    )) / model.spacing
    if max(discharge_error, continuity_error) > 1e-8:
        raise RuntimeError("The decoded velocity failed the volume flux checks.")
    if np.min(heights[:, model.wet]) <= 0:
        raise RuntimeError("The linear wet-bed model would leave its valid regime.")
    report.update(
        model="3D linearized inviscid water waves with a moving free surface",
        atmosphere="Constant pressure",
        backend="Qiskit Aer statevector simulator",
        qubits=qubits,
        grid_shape_zyx=[model.nz, *model.wet.shape],
        cell_size_m=model.spacing,
        mean_depth_m=model.depth,
        gravity_m_s2=GRAVITY_M_S2,
        initial_head_difference_m=HEAD_DIFFERENCE_M,
        water_density_kg_m3=WATER_DENSITY_KG_M3,
        maximum_vertical_speed_m_s=float(np.max(np.abs(velocities[..., 2]))),
        peak_forward_breach_discharge_m3_s=float(np.max(gate_flux)),
        maximum_breach_discharge_balance_error_m3_s=float(discharge_error),
        maximum_discrete_divergence_s_inverse=float(continuity_error),
        maximum_elevation_change_m=float(np.max(np.abs(eta - eta[0]))),
        times_s=times.tolist(),
    )

    if __package__:
        from .quantum_free_surface_output import write_outputs
    else:
        from quantum_free_surface_output import write_outputs

    output.mkdir(parents=True, exist_ok=True)
    write_outputs(output, heights, velocities, model.wet, model.spacing, times)
    (output / "simulation.json").write_text(json.dumps(report, indent=2) + "\n")
    print(
        f"{qubits} qubits, {steps} steps, "
        f"maximum elevation error {report['maximum_elevation_error_vs_reference_m']:.3g} m"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--steps", type=int, default=STEPS)
    parser.add_argument("--time-step", type=float, default=TIME_STEP_S)
    parser.add_argument(
        "--output", type=Path,
        default=Path(__file__).resolve().parents[1] / "qlbm-output" / "quantum-free-surface-3d",
    )
    args = parser.parse_args()
    run_demo(args.output, args.steps, args.time_step)


if __name__ == "__main__":
    main()
