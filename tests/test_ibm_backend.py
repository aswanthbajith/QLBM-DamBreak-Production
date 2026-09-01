import pytest
from backends.fake_ibm_backend import get_fake_ibm_backend
from backends.select_backend import select_real_backend
from backends.ibm_backend import IBMRuntimeServiceWrapper

class TestIBMBackend:
    def test_01_fake_backend_properties(self):
        backend = get_fake_ibm_backend()
        assert backend.num_qubits == 127
        assert "cx" in backend.operation_names

    def test_02_safety_interlock_default(self):
        wrapper = IBMRuntimeServiceWrapper()
        assert not wrapper.is_real_execution_allowed()
