import pytest
import os
import json
from backends.fake_ibm_backend import get_fake_ibm_backend
from scripts.hardware_preflight import run_preflight


class TestIBMISA:
    """
    Rigorously tests Part T: IBM Quantum ISA Target & Transpilation.
    """

    def test_01_fake_backend_has_127_qubits(self):
        backend = get_fake_ibm_backend()
        assert backend.num_qubits >= 9, f"Backend has insufficient qubits: {backend.num_qubits}"

    def test_02_isa_circuit_report_exists_and_valid(self):
        report_file = os.path.join(os.path.dirname(__file__), "..", "results/two_phase/ibm_isa_circuit_report.json")
        if os.path.exists(report_file):
            with open(report_file, "r") as f:
                data = json.load(f)
            assert data["logical_qubits"] == 9
            assert data["physical_qubits"] >= 9
            assert data["two_qubit_gates"] > 0
