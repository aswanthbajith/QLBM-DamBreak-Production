"""Finite-volume spatial operators for linear, three-dimensional gravity waves."""

import operator

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.sparse import csc_matrix, diags, eye, kron
from scipy.sparse.linalg import splu


def _graph_laplacian(size: int, left: NDArray, right: NDArray) -> csc_matrix:
    """Assemble the positive graph Laplacian across open cell faces."""
    adjacency = csc_matrix(
        (np.ones(2 * left.size), (np.r_[left, right], np.r_[right, left])),
        shape=(size, size),
    )
    degree = np.asarray(adjacency.sum(axis=1)).ravel()
    return diags(degree, format="csc") - adjacency


class FreeSurfaceModel:
    """Discretize a tank with a flat bed and rigid vertical walls.

    The fixed, cell-centred fluid grid is ordered (z, y, x). A true entry in
    ``wet[y, x]`` selects a fluid column. The surface potential uses the wet
    columns in row-major order. ``surface_operator`` maps it to the upper face
    velocity. In the linearized model this velocity is the surface elevation
    rate. At the bottom, exterior sides, and faces touching walls, the normal
    velocity is exactly zero.
    """

    def __init__(self, wet: ArrayLike, nz: int, spacing: float) -> None:
        """Build the fixed spatial operators with uniform spacing in metres."""
        self.wet = np.array(wet, dtype=bool, copy=True)
        self.wet.setflags(write=False)
        self.nz = operator.index(nz)
        self.spacing = float(spacing)
        if self.wet.ndim != 2 or not self.wet.any():
            raise ValueError("The wet mask must be two-dimensional with a fluid cell.")
        if self.nz < 1 or not np.isfinite(self.spacing) or self.spacing <= 0:
            raise ValueError("Use at least one vertical layer and positive spacing.")
        self.depth = self.nz * self.spacing
        self._wet_count = int(self.wet.sum())

        indices = np.full(self.wet.shape, -1, dtype=int)
        indices[self.wet] = np.arange(self._wet_count)
        open_x = self.wet[:, :-1] & self.wet[:, 1:]
        open_y = self.wet[:-1, :] & self.wet[1:, :]
        horizontal = _graph_laplacian(
            self._wet_count,
            np.r_[indices[:, :-1][open_x], indices[:-1, :][open_y]],
            np.r_[indices[:, 1:][open_x], indices[1:, :][open_y]],
        )
        vertical = _graph_laplacian(
            self.nz, np.arange(self.nz - 1), np.arange(1, self.nz)
        )

        # Each interior face is one cell-spacing away. The prescribed surface
        # potential is half a spacing from the top cell centres, so its stencil
        # coefficient is twice that of an interior face.
        size = self.nz * self._wet_count
        top = slice(size - self._wet_count, size)
        surface_weight = np.zeros(size)
        surface_weight[top] = 2
        stiffness = (
            kron(eye(self.nz), horizontal, format="csc")
            + kron(vertical, eye(self._wet_count), format="csc")
            + diags(surface_weight, format="csc")
        )
        source = np.zeros((size, self._wet_count))
        identity = np.eye(self._wet_count)
        source[top] = 2 * identity
        self._harmonic_extension = splu(stiffness).solve(source)

        # The symmetric Dirichlet-to-Neumann map is the surface Schur complement
        # of the same discrete Laplacian, divided by the cell spacing.
        normal = (identity - self._harmonic_extension[top]) * (2 / self.spacing)
        self.surface_operator = (normal + normal.T) * 0.5

    def extend(self, surface_potential: ArrayLike) -> NDArray:
        """Lift surface potentials harmonically through the 3D fluid grid."""
        potentials = np.asarray(surface_potential)
        if potentials.shape[-1:] != (self._wet_count,):
            raise ValueError("Supply one surface potential value per wet column.")
        compact = potentials @ self._harmonic_extension.T
        batch = potentials.shape[:-1]
        result = np.zeros((*batch, self.nz, *self.wet.shape), dtype=compact.dtype)
        result[..., self.wet] = compact.reshape(*batch, self.nz, self._wet_count)
        return result

    def face_velocity(
        self, surface_potential: ArrayLike
    ) -> tuple[NDArray, NDArray, NDArray]:
        """Return the x-, y-, and z-normal velocities on their staggered faces."""
        potential = self.extend(surface_potential)
        ny, nx = self.wet.shape
        batch = potential.shape[:-3]
        u = np.zeros((*batch, self.nz, ny, nx + 1), dtype=potential.dtype)
        v = np.zeros((*batch, self.nz, ny + 1, nx), dtype=potential.dtype)
        w = np.zeros((*batch, self.nz + 1, ny, nx), dtype=potential.dtype)
        open_x = self.wet[:, :-1] & self.wet[:, 1:]
        open_y = self.wet[:-1, :] & self.wet[1:, :]
        u[..., 1:-1] = np.diff(potential, axis=-1) * open_x / self.spacing
        v[..., 1:-1, :] = np.diff(potential, axis=-2) * open_y / self.spacing
        w[..., 1:-1, :, :] = np.diff(potential, axis=-3) / self.spacing
        w[..., -1, self.wet] = (
            np.asarray(surface_potential) - potential[..., -1, self.wet]
        ) * (2 / self.spacing)
        return u, v, w

    def flow_velocity(self, surface_potential: ArrayLike) -> NDArray:
        """Average face velocities to cell centres with components (x, y, z)."""
        u, v, w = self.face_velocity(surface_potential)
        return 0.5 * np.stack(
            (
                u[..., :-1] + u[..., 1:],
                v[..., :-1, :] + v[..., 1:, :],
                w[..., :-1, :, :] + w[..., 1:, :, :],
            ),
            axis=-1,
        )
