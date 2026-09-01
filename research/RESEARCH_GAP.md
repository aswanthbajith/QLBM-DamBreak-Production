# SCIENTIFIC RESEARCH GAP & NOVELTY ANALYSIS

**Date**: 2026-08-20  
**Author**: Lead Quantum-CFD Implementation Researcher  

---

## 1. Comprehensive State of the Art vs. Research Gap

| Capability / Feature | State of the Art in Literature (2024–2026) | Demonstrated on Real IBM QPU? | Research Gap in QLBM-DamBreak |
| :--- | :--- | :--- | :--- |
| **D2Q9 Classical Fluid CFD** | Mature, highly verified (OpenLB, Palabos) | N/A (Classical) | Fully verified reference baseline in `classical/` |
| **Linear QLBM (Acoustics/Diffusion)** | Demonstrated on 1D/2D meshes (DLR, Bastida-Zamora) | **YES (2Q–4Q Toy Problems)** | Fully understood; baseline reference |
| **Nonlinear BGK Collision** | Variational SQC (TU Delft) / Carleman Linearization | **NO (Circuit Simulation Only)**| Need verified small-scale circuit on real hardware |
| **Local Carleman Linearization** | PRE 113, 035307 (Zamora et al., March 2026) | **NO (Circuit Simulation Only)**| Benchmark local Carleman vs OSSLBM vs Standard Carleman |
| **Two-Phase Fluid / Interface Tracking**| Only classical LBM (Allen-Cahn, Shan-Chen, VOF) | **NO (Completely Absent)** | **Primary Theoretical & Numerical Contribution** |
| **Dam-Break Wavefront Extraction** | Classical experiments only (Martin & Moyce 1952) | **NO (Completely Absent)** | **Small Quantum Proof-of-Concept Pipeline** |
| **End-to-End Real QPU Dam-Break** | **Completely Unsolved on NISQ Hardware** | **NO** | Honest NISQ boundary identification & FTQC roadmap |

---

## 2. Smallest Defensible Research Contribution
1. Build a clean, mathematically rigorous modular pipeline:
   $$\text{D2Q9 LBM} \to \text{BGK} \to \text{Carleman} \to \text{Quantum Oracles} \to \text{Aer / Fake / Real IBM} \to \text{Classical Reconstruction}$$
2. Benchmark the **Three Primary Approaches**:
   * **Approach A**: Conventional D2Q9 + Global Carleman
   * **Approach B**: Local Carleman Linearization (PRE 113, 035307)
   * **Approach C**: One-Step Simplified LBM (OSSLBM)
3. Execute the validated small primitives (Level 1 Collision, Level 2 Streaming, Level 4 $2\times 2$ QLBM step) through an automated, dual-locked hardware pipeline targeting real IBM Quantum QPUs.
