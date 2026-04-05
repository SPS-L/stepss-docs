---
title: Overview
description: An overview of the STEPSS simulation suite
---

**STEPSS** (*Static and Transient Electric Power Systems Simulation*) is a power system simulation tool for dynamic studies of electrical grids. It performs power flow computations and simulates the dynamic response of power systems to disturbances under the phasor approximation.

STEPSS has been developed by [Dr. Petros Aristidou](https://sps-lab.org) (Cyprus University of Technology) and Dr. Thierry Van Cutsem (University of Liège).

For more information, visit the [STEPSS project page](https://sps-lab.org/project/stepss/) and [Thierry Van Cutsem's software page](https://thierryvancutsem.github.io/home/software.html).

## The Three Modules

STEPSS includes three tightly integrated modules:

| Module | Full Name | Description |
|--------|-----------|-------------|
| **PFC** | Power Flow Computation | Determines the initial operating point using the Newton-Raphson method in polar coordinates. Computes bus voltage magnitudes and phase angles, with optional transformer ratio adjustment. |
| **RAMSES** | RApid Multiprocessor Simulation of Electric power Systems | Simulates the dynamic evolution of the power system in response to disturbances. Supports Backward Euler, Trapezoidal, and BDF2 integration methods. Exploits OpenMP parallelism. |
| **CODEGEN** | CODE GENerator | Translates user-defined models from text descriptions into Fortran 2003 code for compilation and linking with RAMSES. Supports excitation controllers, torque controllers, injectors, and two-port components. |

Each module can be used independently:

- **PFC alone**: Run power flow computations to inspect system state or save solutions for RAMSES
- **RAMSES alone**: With a pre-computed power flow solution, run multiple dynamic simulations from the same initial state
- **CODEGEN alone**: Build and save models for future incorporation into a user-defined version of RAMSES

## PFC Module

The power flow computation uses the Newton-Raphson method in polar coordinates. Input data consists of:

- Network data (buses, lines, transformers, etc.)
- Power flow data specified at PV, PQ, and slack buses
- PFC control parameters (tolerances, reactive power limits, etc.) — optional, defaults are used if not provided

PFC can optionally adjust transformer ratios to:
- Bring voltage magnitudes inside specified deadbands (in-phase transformers)
- Bring active power flows inside specified deadbands (phase-shifting transformers)

## RAMSES Module

RAMSES simulates the dynamic response of power system models under the phasor (RMS) approximation. It takes as input:

- Network data (shared with PFC)
- Dynamic component data
- Solver control parameters (tolerances, time steps, reference speed, etc.)
- Sequence of disturbances and actions

### Integration Methods

Three algebraization methods are available:

- **Backward Euler**: $x_{k+1} = x_k + h \dot{x}_{k+1}$
- **Trapezoidal**: $x_{k+1} = x_k + \frac{h}{2}(\dot{x}_{k+1} + \dot{x}_k)$
- **BDF2**: $x_{k+1} = \frac{4}{3}x_k - \frac{1}{3}x_{k-1} + \frac{2h}{3}\dot{x}_{k+1}$

All three methods are implicit, ensuring numerical robustness. BDF2 is an $L_1$-stable scheme allowing larger time steps when fast transients are not of interest.

### Solver Acceleration

The solver achieves high computational efficiency through two techniques:

**Parallel Processing**: The power system model is decomposed into the network, injectors, and two-ports. A Schur-complement approach for network equations ensures the exact same solution as a non-decomposed scheme. Tasks are distributed among threads using OpenMP shared-memory parallelism.

**Localization**: After a disturbance, components exhibit different levels of dynamic activity. This is exploited at each time step to:
- Skip Newton iterations on converged injectors/two-ports
- Replace latent (inactive) injectors with sensitivity-based models

### Key References

- D. Fabozzi, A. Chieh, B. Haut, and T. Van Cutsem, "Accelerated and localized Newton schemes for faster dynamic simulation of large power systems," *IEEE Trans. on Power Systems*, Vol. 28, No. 4, pp. 4936-4947, Dec. 2013. doi: [10.1109/TPWRS.2013.2251915](https://doi.org/10.1109/TPWRS.2013.2251915)
- P. Aristidou, D. Fabozzi, and T. Van Cutsem, "Dynamic simulation of large-scale power systems using a parallel Schur-complement-based decomposition method," *IEEE Trans. on Parallel and Distributed Systems*, Vol. 25, No. 10, pp. 2561-2570, Sept. 2014. doi: [10.1109/TPDS.2013.252](https://doi.org/10.1109/TPDS.2013.252)

## CODEGEN Module

CODEGEN allows incorporating user-defined models in RAMSES. The user describes a model in a text file, and CODEGEN translates it into Fortran 2003 code for compilation and linking.

Four types of user-defined models are supported:

- **Excitation controllers** (EXC): excitation system and automatic voltage regulator
- **Torque controllers** (TOR): turbine and speed governor
- **Injectors** (INJ): components connected to a single AC bus
- **Two-ports** (TWOP): components connecting two buses

The user model is **compiled, not interpreted** — resulting in efficient number-crunching code. While the solver code is proprietary, the models are designed to be freely shared, making STEPSS an **open-source simulation software** for the modeling part.

### CODEGEN Studio

[CODEGEN Studio](/developer/cg-studio/) is a browser-based visual editor for building CODEGEN models. Instead of writing DSL files by hand, you drag blocks onto a canvas, connect them, and export a valid model file. It can also import existing DSL files for visual inspection and editing.

## Simulation Interfaces

STEPSS modules can be run through three interfaces:

| Interface | RAMSES (Dynamic) | PFC (Static) | CODEGEN |
|-----------|:----------------:|:------------:|:-------:|
| **Command Line** | `ramses -t cmd.txt` | `pfc -t cmd.txt` | `codegen model.txt` |
| **GUI (Java)** | Full support | Full support | Full support |
| **Python (PyRAMSES)** | Full support | — | — |

See the [Quick Start](/getting-started/quickstart/) for details on each interface.

## Platform Support

| Feature | Details |
|---------|---------|
| **STEPSS GUI** | Windows and Linux, Java 20 |
| **PyRAMSES** | Windows and Linux, Python 3.x |
| **Command-line executables** | Windows and Linux (ramses, pfc) |
| **CODEGEN compilation** | Visual Studio 2022 + Intel oneAPI Fortran |
| **Free version limits** | 1000 buses max, 2 OpenMP cores |

## Next Steps

- [Installation](/getting-started/installation/) — Set up STEPSS on your system
- [Quick Start](/getting-started/quickstart/) — Run your first simulation
