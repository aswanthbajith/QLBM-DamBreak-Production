"""
Phase F19: Environment / Stinespring Embedding (Architecture B).

Implements the unitary transformation:
U_E |x> |0>_E = |F(x)> |e(x)>_E

where e(x) = x stores the dissipated non-equilibrium modes into an environmental ancilla register.
Tracing out register E yields the exact dissipative physical BGK state:
rho_out = Tr_E [ U_E (rho_in (x) |0><0|) U_E^dag ]
"""

from typing import Tuple, Dict, Any, List
import numpy as np

from quantum.f19_compute_output import ComputeOutputEmbedding


class EnvironmentStinespringEmbedding:
    """
    Architecture B: Environment / Stinespring Unitary Dilation.
    Embeds dissipative BGK into a joint unitary with environmental dissipation.
    """

    def __init__(
        self,
        omega_f: float = 1.0,
        omega_g: float = 1.42857,
        g_acc: float = -0.0005,
    ):
        self.engine = ComputeOutputEmbedding(omega_f=omega_f, omega_g=omega_g, g_acc=g_acc)

    def execute_environment_dilation(
        self,
        f_in: List[int],
        g_in: List[int],
    ) -> Tuple[List[int], List[int], List[int], List[int], Dict[str, Any]]:
        """
        Executes unitary dilation:
        |x> |0>_E -> |F(x)> |x>_E
        """
        f_out, g_out, meta = self.engine.evaluate_physical_bgk(f_in, g_in)
        # Environmental state e(x) stores input state x
        e_f = list(f_in)
        e_g = list(g_in)

        meta["is_unitary"] = True
        meta["environment_retained"] = True
        return f_out, g_out, e_f, e_g, meta
