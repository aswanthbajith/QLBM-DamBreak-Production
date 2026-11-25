"""D3Q19 lattice and independent checks for the linearized shear-wave benchmark."""

from itertools import product

import numpy as np

VELOCITIES = np.array(
    [(0, 0, 0)]
    + [
        (cx, cy, cz)
        for cx, cy, cz in product((-1, 0, 1), repeat=3)
        if 1 <= abs(cx) + abs(cy) + abs(cz) <= 2
    ]
)
_SPEED_SQUARED = (VELOCITIES**2).sum(axis=1)
WEIGHTS = np.array([1 / 3, 1 / 18, 1 / 36])[_SPEED_SQUARED]
NUM_VELOCITY_STATES = 32
SOUND_SPEED_SQUARED = 1 / 3


def equilibrium_projector():
    """Project scaled populations δf_i / sqrt(w_i) onto density and momentum."""
    modes = np.zeros((NUM_VELOCITY_STATES, 4))
    root_weights = np.sqrt(WEIGHTS)
    active_modes = modes[: len(VELOCITIES)]
    active_modes[:, 0] = root_weights
    active_modes[:, 1:] = (
        root_weights[:, None] * VELOCITIES / np.sqrt(SOUND_SPEED_SQUARED)
    )
    return modes @ modes.T


def _shear_velocity(size, amplitude):
    z, y, x = np.indices((size, size, size))
    phase = 2 * np.pi / size
    return amplitude * np.sin(phase * np.stack((z, x, y), axis=-1))


def initial_state(size, amplitude):
    """Return the scaled equilibrium perturbation on a unit-density lattice."""
    populations = np.zeros((NUM_VELOCITY_STATES, size, size, size))
    velocity = _shear_velocity(size, amplitude)
    populations[: len(VELOCITIES)] = (
        np.sqrt(WEIGHTS)[:, None, None, None]
        * np.einsum("ia,zyxa->izyx", VELOCITIES, velocity)
        / SOUND_SPEED_SQUARED
    )
    return populations


def moments(populations):
    """Recover linearized velocity and relative density from one or more states."""
    active = populations[..., : len(VELOCITIES), :, :, :]
    physical = active * np.sqrt(WEIGHTS)[:, None, None, None]
    velocity = np.einsum("...izyx,ia->...zyxa", physical, VELOCITIES)
    relative_density = 1 + physical.sum(axis=-4)
    return velocity, relative_density


def reference(initial, steps):
    """Classically advance the linearized full-relaxation LBM for validation."""
    snapshots = np.zeros((steps + 1, *initial.shape), dtype=float)
    snapshots[0] = initial
    projector = equilibrium_projector()
    for time in range(1, steps + 1):
        equilibrium = np.einsum(
            "ij,jzyx->izyx", projector, snapshots[time - 1], optimize=True
        )
        for index, direction in enumerate(VELOCITIES):
            snapshots[time, index] = np.roll(
                equilibrium[index], shift=tuple(direction[::-1]), axis=(0, 1, 2)
            )
    return snapshots


def analytic_velocity(size, amplitude, steps):
    """Return the exact discrete shear decay for relaxation time τ = 1.

    One third of the transverse momentum streams along the wave axis, split
    equally in its two directions. The other two thirds stay on that plane.
    A sinusoid with wave number k therefore decays by (2 + cos(k)) / 3
    each step, with continuum viscosity 1/6 in lattice units as k approaches 0.
    """
    wave_number = 2 * np.pi / size
    decay = (2 + np.cos(wave_number)) / 3
    factors = decay ** np.arange(steps + 1)
    return factors[:, None, None, None, None] * _shear_velocity(size, amplitude)
