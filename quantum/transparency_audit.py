"""
Phase F9: Quantum-Path Transparency & Runtime Instrumentation Module.

Provides:
1. TransparencyEvent: Enumeration of execution events across quantum, hybrid, and classical domains.
2. TransparencyLogger: Runtime event recorder (active when QLBM_TRANSPARENCY_AUDIT=1).
3. DependencyAuditor: Static and runtime audit tool mapping all operations to their classification.
"""

import os
from enum import Enum
from typing import List, Dict, Any, Optional
import numpy as np


class TransparencyEvent(str, Enum):
    STATE_PREPARATION = "STATE_PREPARATION"
    CLASSICAL_PARAMETER_GENERATION = "CLASSICAL_PARAMETER_GENERATION"
    COHERENT_MOMENT_EMULATION = "COHERENT_MOMENT_EMULATION"
    QUANTUM_DILATION_SYNTHESIS = "QUANTUM_DILATION_SYNTHESIS"
    QUANTUM_COLLISION_EXECUTION = "QUANTUM_COLLISION_EXECUTION"
    OAA_AMPLIFICATION = "OAA_AMPLIFICATION"
    PROJECTIVE_RESET = "PROJECTIVE_RESET"
    QUANTUM_STREAMING_EXECUTION = "QUANTUM_STREAMING_EXECUTION"
    QUANTUM_BOUNDARY_EXECUTION = "QUANTUM_BOUNDARY_EXECUTION"
    CLASSICAL_DECODE = "CLASSICAL_DECODE"
    CLASSICAL_REENCODE = "CLASSICAL_REENCODE"
    DIAGNOSTIC_EVALUATION = "DIAGNOSTIC_EVALUATION"


class TransparencyLogger:
    """Logs runtime execution events to guarantee complete audit transparency."""

    def __init__(self, enabled: Optional[bool] = None):
        if enabled is None:
            self.enabled = os.environ.get("QLBM_TRANSPARENCY_AUDIT", "0") == "1"
        else:
            self.enabled = enabled
        self.events: List[Dict[str, Any]] = []

    def log(self, event: TransparencyEvent, metadata: Optional[Dict[str, Any]] = None):
        if self.enabled:
            entry = {
                "event": event.value,
                "metadata": metadata or {},
            }
            self.events.append(entry)

    def clear(self):
        self.events.clear()

    def get_event_counts(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for ev in self.events:
            name = ev["event"]
            counts[name] = counts.get(name, 0) + 1
        return counts


# Global singleton instance
_GLOBAL_LOGGER = TransparencyLogger()


def get_transparency_logger() -> TransparencyLogger:
    return _GLOBAL_LOGGER


def get_operation_classification_table() -> List[Dict[str, str]]:
    """Returns the comprehensive classification of all operations in the QLBM solver."""
    return [
        {
            "operation": "State Preparation (|Psi> = 1/N sum f|i,0> + g|i,1>)",
            "mode1_classification": "Classical Statevector Loading / Quantum Basis State",
            "mode2_classification": "Classical Statevector Loading / Quantum Basis State",
            "domain": "Hybrid Setup / Quantum State",
            "autonomous": "No",
        },
        {
            "operation": "Moment Extraction (rho, alpha)",
            "mode1_classification": "Classical Reference Feed / Feedback",
            "mode2_classification": "Coherent Fixed-Point Arithmetic Emulator (Q4.12)",
            "domain": "Mode 1: Classical | Mode 2: Arithmetic Emulator",
            "autonomous": "Mode 1: No | Mode 2: Emulated",
        },
        {
            "operation": "Kinematic Velocity Extraction (u = j / rho)",
            "mode1_classification": "Classical Reference Feed / Feedback",
            "mode2_classification": "Coherent Fixed-Point Division Emulator (Q4.12)",
            "domain": "Mode 1: Classical | Mode 2: Arithmetic Emulator",
            "autonomous": "Mode 1: No | Mode 2: Emulated",
        },
        {
            "operation": "Parameterized Matrix Synthesis C(alpha, u)",
            "mode1_classification": "Classical Matrix Builder (Continuous Angles)",
            "mode2_classification": "Classical Matrix Builder (Continuous Angles)",
            "domain": "Classical Preprocessing",
            "autonomous": "No",
        },
        {
            "operation": "Sz.-Nagy Unitary Dilation U_C in U(64)",
            "mode1_classification": "6-Qubit Unitary Operator (Exact Matrix / Dilation)",
            "mode2_classification": "6-Qubit Unitary Operator (Exact Matrix / Dilation)",
            "domain": "Quantum Unitary Core",
            "autonomous": "Yes (Unitary Block-Encoding)",
        },
        {
            "operation": "Local Collision Execution (U_C @ z_pad)",
            "mode1_classification": "6-Qubit Quantum Collision Dilation Execution",
            "mode2_classification": "6-Qubit Quantum Collision Dilation Execution",
            "domain": "Quantum Unitary Core",
            "autonomous": "Yes (Unitary Core)",
        },
        {
            "operation": "Oblivious Amplitude Amplification (OAA)",
            "mode1_classification": "Quantum Reflection & Grover Operator (m=1)",
            "mode2_classification": "Quantum Reflection & Grover Operator (m=1)",
            "domain": "Quantum Amplification Subroutine",
            "autonomous": "Yes",
        },
        {
            "operation": "Reversible Arithmetic Streaming (S_arith)",
            "mode1_classification": "7-Qubit Quantum Ripple-Carry Modular Permutation",
            "mode2_classification": "7-Qubit Quantum Ripple-Carry Modular Permutation",
            "domain": "Quantum Unitary Core",
            "autonomous": "Yes (Gate-Level Reversible)",
        },
        {
            "operation": "Bounce-Back Boundary Involution (B)",
            "mode1_classification": "7-Qubit Quantum Unitary Involution (B^2 = I)",
            "mode2_classification": "7-Qubit Quantum Unitary Involution (B^2 = I)",
            "domain": "Quantum Unitary Core",
            "autonomous": "Yes (Gate-Level Reversible)",
        },
        {
            "operation": "Ancilla Reset / Intermediate Projection",
            "mode1_classification": "Projective Measurement / Defect Reset",
            "mode2_classification": "Projective Measurement / Defect Reset",
            "domain": "Quantum Projective Subspace",
            "autonomous": "Yes (Projective Reset)",
        },
        {
            "operation": "Continuous Population Decoding",
            "mode1_classification": "Classical Amplitude Extraction / Diagnostic",
            "mode2_classification": "Classical Amplitude Extraction / Diagnostic",
            "domain": "Classical Diagnostic / Readout",
            "autonomous": "No",
        },
    ]
