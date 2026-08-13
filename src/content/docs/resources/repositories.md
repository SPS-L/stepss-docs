---
title: Repositories
description: All STEPSS-related GitHub repositories
---

All STEPSS repositories are hosted under the [SPS-L GitHub organization](https://github.com/SPS-L).

## Repository Index

| Repository | Role | Language | Visibility |
|------------|------|----------|------------|
| [stepss-java-ui](https://github.com/SPS-L/stepss-java-ui) | Java-based GUI front-end, bundling the whole toolchain | Java | Public |
| [stepss-python-ui](https://github.com/SPS-L/stepss-python-ui) | Python API/wrapper for RAMSES and the Helios power-flow engine | Python | Public |
| [stepss-userguide](https://github.com/SPS-L/stepss-userguide) | LaTeX user documentation and models reference | LaTeX | Public |
| [stepss-uramses](https://github.com/SPS-L/stepss-uramses) | User-defined device models framework | Fortran | Public |
| [stepss-eigenanalysis](https://github.com/SPS-L/stepss-eigenanalysis) | Reference data and validation suite for small-signal analysis | Python | Public |
| [stepss-cg-studio](https://github.com/SPS-L/stepss-cg-studio) | Visual block diagram editor for CODEGEN models | Python/JS | Public |
| stepss-ramses | Core RAMSES simulation engine | Fortran | Private |
| stepss-test-systems | Curated collection of test cases and network models | RAMSES data | Private |
| stepss-helios | AC power-flow engine (Newton-Raphson), with a C API shared library wrapped by stepss (`stepss.helios`); releases ship CLI and C API binaries for Linux/macOS/Windows | C++ | Private |
| stepss-dyngraph | Dynamic graph / topology module | Fortran | Private |
| stepss-Codegen | DSL-to-Fortran model code generator | Fortran | Private |
| [stepss-RamsesNN](https://github.com/SPS-L/stepss-RamsesNN) | Physics-informed neural network experiments on RAMSES models | Python | Public |
| stepss-docs | This documentation website | Astro/Starlight | Public |

## Public Repositories

### STEPSS (GUI)

The main graphical user interface for STEPSS, built with Java (Swing/AWT) and the Ant build system.

- **Repository**: [github.com/SPS-L/stepss-java-ui](https://github.com/SPS-L/stepss-java-ui)
- **License**: Apache License 2.0
- **Requirements**: 64-bit Java 11 or later (JRE to run, JDK plus Apache Ant to build)
- **Build**: `ant jar`
- **Run**: `java -jar dist/stepss.jar`

### stepss-python-ui

Python interface to the RAMSES simulator providing scripting access to simulations, plus the `stepss.helios` module for AC power flows with the bundled Helios engine (Windows, Linux, and macOS).

- **Repository**: [github.com/SPS-L/stepss-python-ui](https://github.com/SPS-L/stepss-python-ui)
- **Install**: `pip install stepss`
- **Documentation**: [Python API section](/python/overview/) on this site
- **Includes**: five runnable power-flow examples under `examples/helios/`

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

Reference spectra and the validation suite for RAMSES's built-in small-signal
analysis. The analysis itself runs in the engine, documented under
[Eigenanalysis](/user-guide/eigenanalysis/); this repository holds the
independently captured reference data the engine is checked against, so its
tests need neither a RAMSES licence nor the engine itself.

- **Repository**: [github.com/SPS-L/stepss-eigenanalysis](https://github.com/SPS-L/stepss-eigenanalysis)
- **Requirements**: Python with numpy and pytest

### stepss-cg-studio (CODEGEN Studio)

Browser-based visual editor for building CODEGEN user-defined models with drag-and-drop blocks.

- **Repository**: [github.com/SPS-L/stepss-cg-studio](https://github.com/SPS-L/stepss-cg-studio)
- **Requirements**: Python 3.10 or later
- **Install**: `pip install stepss-cg-studio`
- **Run**: `cg-studio` → open `http://localhost:8765`
- **Documentation**: [CODEGEN Studio guide](/developer/cg-studio/) on this site

:::note
Test-system data repositories (Nordic, 5-bus, Kundur, GB Network, and others) are not listed here; see the [Test Systems](/test-systems/) section of this site.
:::

## Contributing

Contributions to public repositories are welcome. For each repository:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

For issues or feature requests, use the GitHub Issues tab on the relevant repository.
