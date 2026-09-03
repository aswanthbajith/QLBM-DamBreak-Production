"""
Phase F34: Test Suite for Result Parsing and Disk Archiving.
"""

import pytest
import os
import shutil
from quantum.f34_result_parser import F34ResultParser


def test_result_parser_and_disk_io():
    """Verify result parser converts counts and saves/loads JSON files."""
    test_dir = "results/f34_test_io"

    counts = {"0010110000101100": 800, "0010001000100010": 200}
    probs = F34ResultParser.parse_counts_to_probabilities(counts)

    assert probs["0010110000101100"] == 0.8
    assert probs["0010001000100010"] == 0.2

    # Save to test dir
    F34ResultParser.save_results_to_disk(
        test_dir,
        job_metadata={"job_id": "test_123"},
        raw_counts=counts,
        measurement_summary={"mass": 10.0},
        validation_summary={"valid": True},
    )

    loaded = F34ResultParser.load_saved_results(test_dir)
    assert loaded["job_metadata"]["job_id"] == "test_123"
    assert loaded["raw_counts"]["0010110000101100"] == 800

    # Cleanup
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
