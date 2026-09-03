"""
Phase F34: Quantum Hardware Result Parser.

Parses raw bitstring counts, job metadata, and shot distributions into structured
data for macroscopic observable extraction.
"""

from typing import Dict, Any, List, Tuple
import json
import os
import numpy as np


class F34ResultParser:
    """
    Parses and archives raw QPU execution dictionaries and job metadata.
    """

    @staticmethod
    def parse_counts_to_probabilities(counts: Dict[str, int]) -> Dict[str, float]:
        """Converts raw counts dictionary to normalized probabilities."""
        total_shots = sum(counts.values())
        if total_shots == 0:
            return {}
        return {k.replace(" ", ""): v / total_shots for k, v in counts.items()}

    @staticmethod
    def save_results_to_disk(
        results_dir: str,
        job_metadata: Dict[str, Any],
        raw_counts: Dict[str, int],
        measurement_summary: Dict[str, Any],
        validation_summary: Dict[str, Any],
    ) -> None:
        """Saves machine-readable execution artifacts to results/f34/."""
        os.makedirs(results_dir, exist_ok=True)

        with open(os.path.join(results_dir, "job_metadata.json"), "w") as f:
            json.dump(job_metadata, f, indent=2)

        with open(os.path.join(results_dir, "raw_counts.json"), "w") as f:
            json.dump(raw_counts, f, indent=2)

        with open(os.path.join(results_dir, "measurement_summary.json"), "w") as f:
            json.dump(measurement_summary, f, indent=2)

        with open(os.path.join(results_dir, "validation_summary.json"), "w") as f:
            json.dump(validation_summary, f, indent=2)

    @staticmethod
    def load_saved_results(results_dir: str) -> Dict[str, Any]:
        """Loads machine-readable artifacts from results/f34/."""
        data = {}
        files = ["job_metadata.json", "raw_counts.json", "measurement_summary.json", "validation_summary.json"]
        for fname in files:
            fpath = os.path.join(results_dir, fname)
            if os.path.exists(fpath):
                with open(fpath, "r") as f:
                    data[fname.replace(".json", "")] = json.load(f)
        return data
