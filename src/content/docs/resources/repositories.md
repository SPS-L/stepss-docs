---
title: Repositories
description: All STEPSS-related GitHub repositories
---

All STEPSS repositories are hosted under the [SPS-L GitHub organization](https://github.com/SPS-L).

## Repository Index

| Repository | Role | Language | Visibility |
|------------|------|----------|------------|
| [stepss-java-ui](https://github.com/SPS-L/stepss-java-ui) | Java-based GUI front-end (v3.40) | Java | Public |
| [stepss-pyramses](https://github.com/SPS-L/stepss-pyramses) | Python API/wrapper for RAMSES and the Helios power-flow engine | Python | Public |
| [stepss-userguide](https://github.com/SPS-L/stepss-userguide) | LaTeX user documentation and models reference | LaTeX | Public |
| [stepss-uramses](https://github.com/SPS-L/stepss-uramses) | User-defined device models framework | Fortran | Public |
| [stepss-eigenanalysis](https://github.com/SPS-L/stepss-eigenanalysis) | Small-signal / eigenvalue analysis tools | MATLAB | Public |
| [stepss-cg-studio](https://github.com/SPS-L/stepss-cg-studio) | Visual block diagram editor for CODEGEN models | Python/JS | Public |
| stepss-ramses | Core RAMSES simulation engine | Fortran | Private |
| stepss-test-systems | Curated collection of test cases and network models | RAMSES data | Private |
| stepss-PFC | Power-flow calculator (Newton-Raphson) | Fortran | Private |
| stepss-helios | Modern C++ reimplementation of the PFC power-flow calculator, with a C API shared library wrapped by PyRAMSES (`pyramses.helios`); releases ship CLI and C API binaries for Linux/macOS/Windows | C++ | Private |
| stepss-dyngraph | Dynamic graph / topology module | Fortran | Private |
| stepss-Codegen | DSL-to-Fortran model code generator | Fortran | Private |
| stepss-docs | This documentation website | Astro/Starlight | Public |

## Public Repositories

### STEPSS (GUI)

The main graphical user interface for STEPSS, built with Java (Swing/AWT) and the Ant build system.

- **Repository**: [github.com/SPS-L/stepss-java-ui](https://github.com/SPS-L/stepss-java-ui)
- **License**: Apache License 2.0
- **Requirements**: Java 20 (64-bit)
- **Build**: `ant build`
- **Run**: `java -jar dist/stepss.jar`

### stepss-pyramses

Python interface to the RAMSES simulator providing scripting access to simulations, plus the `pyramses.helios` module for AC power flows with the bundled Helios engine (Windows, Linux, and macOS).

- **Repository**: [github.com/SPS-L/stepss-pyramses](https://github.com/SPS-L/stepss-pyramses)
- **Install**: `pip install pyramses`
- **Documentation**: [PyRAMSES section](/pyramses/overview/) on this site
- **Includes**: Nordic test system example; runnable power-flow examples under `examples/helios/`

### stepss-userguide

The original LaTeX source for the STEPSS documentation (models reference and user guide).

- **Repository**: [github.com/SPS-L/stepss-userguide](https://github.com/SPS-L/stepss-userguide)
- **Build**: `pdflatex stepss_doc.tex` (run twice)
- **Main file**: `stepss_doc.tex`

### stepss-uramses

Framework for compiling and linking custom Fortran models with RAMSES.

- **Repository**: [github.com/SPS-L/stepss-uramses](https://github.com/SPS-L/stepss-uramses)
- **Platforms**: Linux (gfortran), macOS (gfortran, Apple Silicon), Windows (MinGW gfortran or Intel Fortran)
- **Build (Linux)**: `make -f build/Makefile.linux all`
- **Build (macOS)**: `make -f build/Makefile.macos all`
- **Build (Windows/MinGW)**: `make -f build/Makefile.windows all`
- **Build (Windows/Intel)**: Visual Studio with `build/msvs/URAMSES.sln`

### stepss-eigenanalysis

MATLAB-based tool for small-signal stability analysis using eigenvalues extracted from RAMSES.

- **Repository**: [github.com/SPS-L/stepss-eigenanalysis](https://github.com/SPS-L/stepss-eigenanalysis)
- **Requirements**: MATLAB R2016a+, PyRAMSES
- **Methods**: QZ, ARPACK, JDQR

### stepss-cg-studio (CODEGEN Studio)

Browser-based visual editor for building CODEGEN user-defined models with drag-and-drop blocks.

- **Repository**: [github.com/SPS-L/stepss-cg-studio](https://github.com/SPS-L/stepss-cg-studio)
- **Requirements**: Python 3.10 or later
- **Install**: `pip install stepss-cg-studio`
- **Run**: `cg-studio` → open `http://localhost:8765`
- **Documentation**: [CODEGEN Studio guide](/developer/cg-studio/) on this site

:::note
Test-system data repositories (Nordic, 5-bus, Kundur, GB Network, and others) are not listed here — see the [Test Systems](/test-systems/nordic/) section of this site.
:::

## Contributing

Contributions to public repositories are welcome. For each repository:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

For issues or feature requests, use the GitHub Issues tab on the relevant repository.
