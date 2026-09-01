"""
Unit tests verifying architecture comparison metrics and scorecard consistency.
"""

import os
import csv
import pytest
import numpy as np


class TestLevel6ARArchitectures:
    """Test suite verifying architecture scores, data consistency, and decision gate."""

    def test_01_architecture_scores_csv_consistency(self):
        """Verify Architecture D attains highest score in 16-criteria scorecard."""
        csv_path = "results/level6a_r_architecture_scores.csv"
        assert os.path.exists(csv_path)

        with open(csv_path, "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        total_row = rows[-1]
        score_A = int(total_row["Arch_A_NaiveLift"])
        score_B = int(total_row["Arch_B_GlobalTensor"])
        score_C = int(total_row["Arch_C_MidCircuitReset"])
        score_D = int(total_row["Arch_D_HybridK1"])
        score_E = int(total_row["Arch_E_GlobalQSVT"])

        assert score_D > score_A
        assert score_D > score_B
        assert score_D > score_C
        assert score_D > score_E
        assert score_D >= 70

    def test_02_resource_comparison_qubits_consistency(self):
        """Verify qubit scaling numbers across resolutions."""
        csv_path = "results/level6a_r_resource_comparison.csv"
        assert os.path.exists(csv_path)

        with open(csv_path, "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        assert len(rows) == 6
        # Check 128x64 grid
        row_128x64 = rows[-1]
        assert row_128x64["mesh_name"] == "128x64"
        assert int(row_128x64["qubits_Arch_D_Hybrid"]) == 19
        assert int(row_128x64["qubits_Arch_B_GlobalTensor"]) == 36
