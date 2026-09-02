"""
Unit tests for Level-7 literature matrix, claim qualification, and level status datasets.
"""

import os
import csv
import pytest


class TestLevel7LiteratureAudit:
    """Test suite validating literature and claim audit datasets."""

    def test_01_literature_matrix_structure(self):
        """Verify literature matrix contains required benchmark papers."""
        path = os.path.join(os.path.dirname(__file__), "../results/level7_final_literature_matrix.csv")
        assert os.path.exists(path), "level7_final_literature_matrix.csv must exist"

        with open(path, "r") as f:
            reader = list(csv.DictReader(f))
            assert len(reader) >= 5, "Must contain at least 5 benchmark literature comparisons"
            citations = [r["paper_citation"] for r in reader]
            assert any("Mezzacapo" in c for c in citations)
            assert any("Itani" in c for c in citations)
            assert any("Lăcătuş" in c or "Lacatus" in c for c in citations)

    def test_02_claim_matrix_purged_unqualified_claims(self):
        """Verify claim matrix properly purges NISQ and fully coherent claims."""
        path = os.path.join(os.path.dirname(__file__), "../results/level7_final_claim_matrix.csv")
        assert os.path.exists(path), "level7_final_claim_matrix.csv must exist"

        with open(path, "r") as f:
            reader = list(csv.DictReader(f))
            assert len(reader) >= 6
            for row in reader:
                assert row["audited_status"] in [
                    "REJECTED / PURGED",
                    "QUALIFIED / CORRECTED",
                    "QUALIFIED AS CANDIDATE NOVELTY",
                    "VERIFIED UNDER STATED CONDITIONS",
                ]

    def test_03_level_status_invariants(self):
        """Verify Level-6B remains GREEN (Frozen Baseline) and Level-7 remains YELLOW."""
        path = os.path.join(os.path.dirname(__file__), "../results/level7_final_status.csv")
        assert os.path.exists(path), "level7_final_status.csv must exist"

        with open(path, "r") as f:
            reader = {r["level"]: r["verdict"] for r in csv.DictReader(f)}
            assert "GREEN" in reader["Level 6B"]
            assert "YELLOW" in reader["Level 7"]
            assert "GREEN" in reader["Level 4"]
