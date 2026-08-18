#!/usr/bin/env python3
"""
Automated paper ingestion and structured extraction utility for QLBM DamBreak Research Base.
"""

import sys
import os
import subprocess
from pathlib import Path

KNOWLEDGE_TEMPLATE = """# Knowledge Base Dossier: {paper_title}

## 1. Citation & Metadata
- **Title**: {paper_title}
- **Authors**: 
- **Year**: 
- **Journal / Archive**: 
- **DOI / URL**: 

## 2. Research Objective & Core Contribution
- 

## 3. Physical Model & Governing PDEs
- 

## 4. Lattice Model & Discrete Velocity Set ($D_d Q_q$)
- 

## 5. Equilibrium Distribution Function ($f_i^{eq} / g_i^{eq}$)
- 

## 6. Collision Operator & Relaxation Mechanics
- 

## 7. Streaming & Spatial Transport
- 

## 8. Multiphase / Interface Capturing Scheme
- 

## 9. Forcing & Body Force Coupling
- 

## 10. Boundary Conditions
- 

## 11. Dam-Break Benchmark Setup & Geometry
- 

## 12. Validation Metrics & Targets
- 

## 13. Numerical Parameters & Stability Bounds
- 

## 14. Linear vs. Nonlinear Term Catalog
- 

## 15. Carleman Linearization Suitability & Tensor Mapping
- 

## 16. Quantum Encoding / QSVT Algorithmic Relevance
- 
"""

def extract_text_from_pdf(pdf_path):
    cmd = ["pdftotext", str(pdf_path), "-"]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0:
        return res.stdout
    return ""

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 ingest_paper.py <path_to_pdf>")
        sys.exit(1)
    
    pdf_path = Path(sys.argv[1])
    if not pdf_path.exists():
        print(f"File not found: {pdf_path}")
        sys.exit(1)
        
    print(f"Extracting text from: {pdf_path.name}")
    raw_text = extract_text_from_pdf(pdf_path)
    print(f"Extracted {len(raw_text)} characters.")
    
    out_dir = Path("/home/aswa/Research/QLBM-DamBreak/knowledge")
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = pdf_path.stem.replace(" ", "_").lower()
    out_file = out_dir / f"{stem}.md"
    
    if not out_file.exists():
        content = KNOWLEDGE_TEMPLATE.format(paper_title=pdf_path.stem)
        out_file.write_text(content)
        print(f"Created template: {out_file}")
    else:
        print(f"Knowledge file already exists: {out_file}")

if __name__ == "__main__":
    main()
