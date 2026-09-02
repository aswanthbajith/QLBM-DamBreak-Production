"""
Phase F21: Quantum Channel Verification for CSF Force Injection.

Verifies complete positivity, trace preservation, and CPTP channel properties
for the reversible CSF operator.
"""

from typing import Dict, Any, Tuple
import numpy as np
import scipy.linalg as la

from quantum.f20_kraus import F20KrausRepresentation
from quantum.f20_choi import F20ChoiVerification


class F21CSFChannelVerification:
    """
    Audits CPTP channel properties for CSF force injection.
    """

    def __init__(self, dim: int, mapping_dict: Dict[int, int]):
        self.dim = dim
        self.kraus_rep = F20KrausRepresentation(dim, mapping_dict)
        self.choi_verifier = F20ChoiVerification(self.kraus_rep)

    def verify_csf_channel_cptp(self) -> Dict[str, Any]:
        """
        Verifies trace preservation and complete positivity of the CSF channel.
        """
        res_tp, is_tp = self.kraus_rep.verify_trace_preservation()
        choi_res = self.choi_verifier.audit_choi_properties()

        return {
            "trace_preservation_residual": res_tp,
            "is_trace_preserving": is_tp,
            "min_choi_eigenvalue": choi_res["min_eigenvalue"],
            "is_completely_positive": choi_res["is_completely_positive"],
            "is_cptp": choi_res["is_cptp"],
        }
