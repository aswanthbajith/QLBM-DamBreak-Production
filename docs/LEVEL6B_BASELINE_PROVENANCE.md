# LEVEL-6B BASELINE PROVENANCE & CHECKSUM VERIFICATION
## Forensic Proof of Frozen Reference Integrity

**Target File**: `quantum/level6b_hybrid_solver.py`  
**Expected SHA-256 Checksum**: `2a306f5a413945adc1acd10f3f63340c3d3617e4ef1c94981a92e8ebad8742c8`  
**Current Calculated SHA-256**: `2a306f5a413945adc1acd10f3f63340c3d3617e4ef1c94981a92e8ebad8742c8`  
**Verification Verdict**: **EXACT MATCH (100% Intact and Unmodified)**  

---

## 1. Provenance and History

1. **Origin**: Created in Commit `064e67a` on branch `feature/level6b-hybrid-k1` to solve the Carleman truncation instability discovered in Level-6A.
2. **Architecture**: Implements the Hybrid $K=1$ Local-Carleman Two-Phase QLBM solver combining exact local Carleman collision blocks with exact classical spatial streaming and Guo forcing.
3. **Freeze Mandate**: Frozen in Commit `e5d258e` as the permanent independent physical and numerical baseline for all subsequent quantum-circuit phases.
4. **Conservation & Physics**: Validated to conserve total fluid mass to machine precision ($<10^{-15}$) and capture the physical dam-break surge front across $T=1 \dots 100$ timesteps.
