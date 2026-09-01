import pytest
from scripts.hardware_preflight import run_preflight


class TestHardwarePreflight:
    """
    Rigorously tests Part T: Hardware Preflight & Safety Dual-Lock Interlock.
    """

    def test_01_preflight_dry_run_interlock(self):
        allowed = run_preflight()
        assert not allowed, "Default dry-run mode must safely prevent real hardware submission"

    def test_02_preflight_metadata_details(self):
        status = run_preflight(nx=4, ny=4, timesteps=1, return_dict=True)
        assert status["required_qubits"] == 9
        assert status["available_qubits"] >= 9
        assert not status["dual_lock_active"]
        assert not status["submission_permitted"]
