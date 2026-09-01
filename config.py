"""
Configuration Module for QLBM Two-Phase Dam-Break Solver.
"""
from dataclasses import dataclass, field


@dataclass
class SimulationConfig:
    """
    Simulation parameters for Two-Phase D2Q9 Carleman Dam-Break Solver.
    """
    nx: int = 4
    ny: int = 4
    timesteps: int = 10
    tau_f: float = 0.80
    tau_g: float = 0.70
    g_acc: float = -0.001
    rho_liquid: float = 1.0
    rho_gas: float = 0.10
    carleman_order: int = 2
    backend: str = "statevector" # options: "statevector", "aer", "noisy", "fake_ibm", "real_ibm"
    shots: int = 4096
    output_dir: str = "results"
    save_plots: bool = True
