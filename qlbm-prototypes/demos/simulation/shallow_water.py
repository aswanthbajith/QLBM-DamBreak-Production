"""Conservative, flat-bed shallow-water solver for the dam-break demos."""

from collections.abc import Iterable, Iterator

import numpy as np
from numpy.typing import ArrayLike, NDArray

DRY_DEPTH = 1e-9  # m, below which momentum is set to zero
CFL = 0.4


def velocity(state: NDArray) -> NDArray:
    """Return the depth-averaged x and y velocities in m/s."""
    depth = state[0]
    return np.divide(
        state[1:], depth, out=np.zeros_like(state[1:]), where=depth > DRY_DEPTH
    )


def _physical_flux(state: NDArray, normal: int, gravity: float) -> tuple[NDArray, NDArray]:
    """Return the shallow-water flux and wave speed normal to a cell face."""
    depth = state[0]
    speed = velocity(state)[normal - 1]
    flux = state * speed
    flux[0] = state[normal]
    flux[normal] += 0.5 * gravity * depth**2
    return flux, np.abs(speed) + np.sqrt(gravity * depth)


def _face_flux(
    state: NDArray, solid: NDArray, axis: int, normal: int, gravity: float
) -> tuple[NDArray, float]:
    # Arrange either direction along the last array axis and add exterior walls.
    padded = np.pad(np.swapaxes(state, axis, -1), ((0, 0), (0, 0), (1, 1)))
    walls = np.pad(
        np.swapaxes(solid, axis, -1), ((0, 0), (1, 1)), constant_values=True
    )
    left = padded[..., :-1].copy()
    right = padded[..., 1:].copy()
    left_wall = walls[:, :-1] & ~walls[:, 1:]
    right_wall = walls[:, 1:] & ~walls[:, :-1]

    # Mirror depth and tangential momentum while reversing normal momentum.
    # This gives zero mass flux through walls and preserves their pressure force.
    left[:, left_wall] = right[:, left_wall]
    left[normal, left_wall] *= -1
    right[:, right_wall] = left[:, right_wall]
    right[normal, right_wall] *= -1

    left_flux, left_speed = _physical_flux(left, normal, gravity)
    right_flux, right_speed = _physical_flux(right, normal, gravity)
    speed = np.maximum(left_speed, right_speed)
    flux = 0.5 * (left_flux + right_flux - speed * (right - left))
    return np.swapaxes(flux, axis, -1), float(speed.max())


def simulate(
    depth: ArrayLike,
    solid: ArrayLike,
    cell_size: float,
    times: Iterable[float],
    gravity: float = 9.81,
) -> Iterator[NDArray]:
    """Yield independent (depth, x momentum, y momentum) snapshots.

    Depth starts at rest on a flat bed. `solid[y, x]` takes True for cells inside
    walls. Both those walls and the exterior boundaries reflect normal flow.
    The grid spacing is in metres and output times are in seconds. The first-order
    finite-volume update uses local Lax-Friedrichs (Rusanov) face fluxes and
    advances exactly to each requested time using an adaptive CFL time step.
    """
    depth = np.asarray(depth, dtype=float)
    solid = np.asarray(solid, dtype=bool)
    times = np.asarray(tuple(times), dtype=float)
    if depth.ndim != 2 or not depth.size or depth.shape != solid.shape:
        raise ValueError("Depth and solid must have the same nonempty 2D shape.")
    if not np.isfinite(depth).all() or (depth < 0).any():
        raise ValueError("Initial depth must be finite and nonnegative.")
    if depth[solid].any():
        raise ValueError("Initial depth must be zero inside solid cells.")
    if not np.isfinite(cell_size) or cell_size <= 0:
        raise ValueError("Cell size must be finite and positive.")
    if not np.isfinite(gravity) or gravity <= 0:
        raise ValueError("Gravity must be finite and positive.")
    if (
        times.ndim != 1
        or not times.size
        or not np.isfinite(times).all()
        or times[0] < 0
        or (np.diff(times) <= 0).any()
    ):
        raise ValueError("Output times must be finite, nonnegative, and increasing.")

    state = np.zeros((3, *depth.shape), dtype=float)
    state[0] = depth
    initial_volume = depth.sum() * cell_size**2
    time = 0.0
    for target in times:
        while time < target:
            x_flux, x_speed = _face_flux(state, solid, -1, 1, gravity)
            y_flux, y_speed = _face_flux(state, solid, -2, 2, gravity)
            max_speed = x_speed + y_speed
            remaining = target - time
            dt = min(remaining, CFL * cell_size / max_speed) if max_speed else remaining
            if time + dt <= time:
                raise RuntimeError("The shallow-water time step became too small.")
            divergence = np.diff(x_flux, axis=-1) + np.diff(y_flux, axis=-2)
            state -= (dt / cell_size) * divergence
            state[:, solid] = 0
            if not np.isfinite(state).all() or state[0].min() < -1e-12:
                raise RuntimeError("The shallow-water update produced an invalid state.")
            np.maximum(state[0], 0, out=state[0])
            state[1:, state[0] <= DRY_DEPTH] = 0
            time = target if dt == remaining else time + dt

        volume = state[0].sum() * cell_size**2
        if not np.isclose(volume, initial_volume, rtol=1e-10, atol=1e-12):
            raise RuntimeError("The shallow-water update did not conserve volume.")
        yield state.copy()
