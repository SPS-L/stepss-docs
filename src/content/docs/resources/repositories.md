---
title: Repositories
description: All STEPSS-related GitHub repositories
---

All STEPSS repositories are hosted under the [SPS-L GitHub organization](https://github.com/SPS-L).

## Repository Index

| Repository | Role | Language | Visibility |
|------------|------|----------|------------|
| [STEPSS](https://github.com/SPS-L/STEPSS) | Java-based GUI front-end (v3.40) | Java | Public |
| [stepss-PyRAMSES](https://github.com/SPS-L/stepss-PyRAMSES) | Python API/wrapper for RAMSES | Python | Public |
| [STEPSS-Userguide](https://github.com/SPS-L/STEPSS-Userguide) | LaTeX user documentation and models reference | LaTeX | Public |
| [stepss-URAMSES](https://github.com/SPS-L/stepss-URAMSES) | User-defined device models framework | Fortran | Public |
| [RAMSES-Eigenanalysis](https://github.com/SPS-L/RAMSES-Eigenanalysis) | Small-signal / eigenvalue analysis tools | MATLAB | Public |
| stepss-ramses | Core RAMSES simulation engine | Fortran | Private |
| stepss-PFC | Power-flow calculator (Newton-Raphson) | Fortran | Private |
| stepss-dyngraph | Dynamic graph / topology module | Fortran | Private |
| stepss-Codegen | DSL-to-Fortran model code generator | Fortran | Private |
| stepss-docs | This documentation website | Astro/Starlight | Public |

## Public Repositories

### STEPSS (GUI)

The main graphical user interface for STEPSS, built with Java (Swing/AWT) and the Ant build system.

- **Repository**: [github.com/SPS-L/STEPSS](https://github.com/SPS-L/STEPSS)
- **License**: Apache License 2.0
- **Requirements**: Java 20 (64-bit)
- **Build**: `ant build`
- **Run**: `java -jar dist/stepss.jar`

### stepss-PyRAMSES

Python interface to the RAMSES simulator providing scripting access to simulations.

- **Repository**: [github.com/SPS-L/stepss-PyRAMSES](https://github.com/SPS-L/stepss-PyRAMSES)
- **Install**: `pip install pyramses`
- **Documentation**: [pyramses.sps-lab.org](https://pyramses.sps-lab.org/)
- **Includes**: Nordic test system example

### STEPSS-Userguide

The original LaTeX source for the STEPSS documentation (models reference and user guide).

- **Repository**: [github.com/SPS-L/STEPSS-Userguide](https://github.com/SPS-L/STEPSS-Userguide)
- **Build**: `pdflatex stepss_doc.tex` (run twice)
- **Main file**: `stepss_doc.tex`

### stepss-URAMSES

Framework for compiling and linking custom Fortran models with RAMSES.

- **Repository**: [github.com/SPS-L/stepss-URAMSES](https://github.com/SPS-L/stepss-URAMSES)
- **Platforms**: Windows (Intel Fortran) and Linux (gfortran)
- **Build (Linux)**: `make -f Makefile.gfortran all`

### RAMSES-Eigenanalysis

MATLAB-based tool for small-signal stability analysis using eigenvalues extracted from RAMSES.

- **Repository**: [github.com/SPS-L/RAMSES-Eigenanalysis](https://github.com/SPS-L/RAMSES-Eigenanalysis)
- **Requirements**: MATLAB R2016a+, PyRAMSES
- **Methods**: QZ, ARPACK, JDQR

## Contributing

Contributions to public repositories are welcome. For each repository:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

For issues or feature requests, use the GitHub Issues tab on the relevant repository.
