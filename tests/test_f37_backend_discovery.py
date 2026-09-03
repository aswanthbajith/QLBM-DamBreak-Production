"""
Phase F37: Test Suite for Backend Discovery & Credential Auditing.
"""

import pytest
from quantum.f37_backend_discovery import F37BackendDiscovery


def test_credential_audit():
    """Verify credential audit accurately detects missing credentials without error."""
    audit = F37BackendDiscovery.audit_credentials()
    assert "authenticated" in audit
    assert "provider_accessible" in audit
    assert "status" in audit


def test_backend_discovery():
    """Verify backend discovery enumerates candidate hardware topologies."""
    backends = F37BackendDiscovery.discover_backends()
    assert len(backends) > 0
    assert any("sherbrooke" in b["name"].lower() for b in backends)
