import pytest
from scripts.hardware_preflight import run_preflight

class TestHardwareVerification:
    def test_01_preflight_dry_run_interlock(self):
        allowed = run_preflight()
        assert not allowed # default dry-run prevents submission
