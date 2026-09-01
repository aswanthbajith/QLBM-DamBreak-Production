"""
Automated Operational IBM Quantum Backend Selection.
"""
from backends.fake_ibm_backend import get_fake_ibm_backend

def select_real_backend(prefer_name="ibm_brisbane"):
    """
    Discovers and selects candidate operational IBM Quantum backend.
    In dry-run mode, returns the 127Q Heavy-Hex fake backend.
    """
    try:
        from qiskit_ibm_runtime import QiskitRuntimeService
        service = QiskitRuntimeService()
        backends = service.backends(simulator=False, operational=True)
        for b in backends:
            if b.name == prefer_name:
                return b
        return backends[0] if len(backends) > 0 else get_fake_ibm_backend()
    except Exception:
        return get_fake_ibm_backend()
