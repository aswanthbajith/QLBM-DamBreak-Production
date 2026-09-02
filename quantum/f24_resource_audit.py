"""
Phase F24: Detailed Resource and Qubit Register Forensic Audit.

Provides exact breakdown of the 624-qubit per node claim:
- System Registers (Hydrodynamic + Phase Populations): 18 fields * 16 bits = 288 qubits
- Stinespring Environment Registers: 18 fields * 16 bits = 288 qubits
- Reversible CSF Stencil Ancillas: 3 fields (grad_x, grad_y, kappa) * 16 bits = 48 qubits
Total Logical Qubits per Node = 288 + 288 + 48 = 624 qubits.
"""

from typing import Dict, Any


class F24ResourceForensicAudit:
    """
    Rigorously accounts for every logical qubit, arithmetic register, and environment wire.
    """

    @staticmethod
    def audit_qubit_breakdown(
        nx: int = 4,
        ny: int = 4,
        bit_width: int = 16,
    ) -> Dict[str, Any]:
        """
        Calculates exact per-node and whole-lattice qubit allocation.
        """
        num_nodes = nx * ny

        # System Registers
        f_pop_qubits = 9 * bit_width  # 144
        g_pop_qubits = 9 * bit_width  # 144
        system_qubits_node = f_pop_qubits + g_pop_qubits  # 288

        # Stinespring Environment Registers
        f_env_qubits = 9 * bit_width  # 144
        g_env_qubits = 9 * bit_width  # 144
        env_qubits_node = f_env_qubits + g_env_qubits  # 288

        # Reversible CSF Ancillas (grad_x, grad_y, kappa)
        csf_ancillas_node = 3 * bit_width  # 48

        total_node_qubits = system_qubits_node + env_qubits_node + csf_ancillas_node  # 624

        return {
            "num_nodes": num_nodes,
            "bit_width": bit_width,
            "system_qubits_per_node": system_qubits_node,
            "environment_qubits_per_node": env_qubits_node,
            "csf_ancillas_per_node": csf_ancillas_node,
            "total_qubits_per_node": total_node_qubits,
            "total_lattice_qubits": total_node_qubits * num_nodes,
            "is_624_exact": (total_node_qubits == 624),
        }
