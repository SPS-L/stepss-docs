---
title: Overview
description: An overview of the STEPSS simulation suite
---

**STEPSS** (*Static and Transient Electric Power Systems Simulation*) is a power system simulation tool for dynamic studies of electrical grids. It performs power flow computations and simulates the dynamic response of power systems to disturbances under the phasor approximation.

## The People Behind STEPSS

STEPSS is the work of two people, and each of its engines belongs to one of them.

[**Dr. Petros Aristidou**](https://sps-lab.org/author/petros-aristidou/)
contributed the parallel algorithms that let STEPSS simulate large systems in
usable time. His doctorate, at the University of Liège in 2015, was on domain
decomposition methods for real-time dynamic security assessment, and the
Schur-complement decomposition that RAMSES solves with came directly out of that
work, later extended to a two-level form. Before Liège he took his diploma at the
National Technical University of Athens; afterwards he was a postdoctoral
researcher at the Power Systems Laboratory of ETH Zurich, then a Lecturer at the
University of Leeds leading its Smart Grids Lab. Since January 2020 he has been
Assistant Professor in Sustainable Power Systems at the Cyprus University of
Technology. **Helios** is his.

[**Dr. Thierry Van Cutsem**](https://thierryvancutsem.github.io/home/)
contributed the simulation core: the accelerated and localized Newton schemes the
solver runs on, and the treatment of angle references that makes long-term runs
well posed. He has spent 42 years on the dynamics of large power systems, their
modelling, stability, security and control, much of it in collaboration with
transmission and distribution system operators. He was Research Director at
Belgium's Fund for Scientific Research (FNRS) and Adjunct Professor at the
Montefiore Institute of the University of Liège, and now consults for
transmission system operators and advises on research projects. **CODEGEN** is
his.

The work behind those contributions is published, and
[Publications](/resources/references/) lists the papers, each with a DOI, so the
attribution above can be checked rather than taken on trust. RAMSES itself is the
property of the University of Liège; see [License](/getting-started/license/) for
who owns what.

## The Three Modules

STEPSS includes three tightly integrated modules:

<img src="/images/over-general.svg" alt="The three modules of STEPSS" style="width:60%" />

In the figure above, files shown in blue are provided by the user; those in black are produced internally.

| Module | Full Name | Description |
|--------|-----------|-------------|
| **Helios** | AC Power Flow | Determines the initial operating point using the Newton-Raphson method in polar coordinates. Computes bus voltage magnitudes and phase angles, with optional transformer ratio adjustment. |
| **RAMSES** | RApid Multithreaded Simulation of Electric power Systems | Simulates the dynamic evolution of the power system in response to disturbances. Supports Backward Euler, Trapezoidal, and BDF2 integration methods. Exploits OpenMP parallelism. |
| **CODEGEN** | CODE GENerator | Translates user-defined models from text descriptions into Fortran 2003 code for compilation and linking with RAMSES. Supports excitation controllers, torque controllers, injectors, and two-port components. |

Each module can be used independently:

- **Helios alone**: Run one power flow computation, or a sequence of them until the desired system state is obtained, to inspect that state and/or save the solution for RAMSES
- **RAMSES alone**: With a pre-computed power flow solution, run multiple dynamic simulations from the same initial state
- **CODEGEN alone**: Build and save models for future incorporation into a user-defined version of RAMSES

## Two Editions

STEPSS is the name of the platform, not of any one program. It reaches users in
two editions, which drive the same engines and read the same data files:

| Edition | Distributed as | Use it for |
|---|---|---|
| **STEPSS GUI** | a desktop application: an installer for Windows, macOS or Linux | Interactive work: load a network, run it, plot curves, build models |
| **STEPSS in Python** | the `stepss` Python package | Scripting, parameter sweeps, and the scientific Python stack |

Neither edition wraps the other. Both are front ends onto the same Fortran
engines, so a case built in one runs unchanged in the other.

They do not carry identical toolchains. The GUI bundles all three modules plus
the DYNGRAPH trajectory extractor. `stepss` bundles RAMSES and Helios,
so **CODEGEN is the one capability it lacks**: writing your own models needs the
GUI, or the [CODEGEN toolchain](/developer/user-models/) directly.

Both editions plot the simulated curves: the GUI through the DYNGRAPH viewer, STEPSS in Python through Matplotlib.

Install either from [Installation](/getting-started/installation/).

## Helios Module

Helios solves the AC power flow of the network and produces the operating point that initialises a RAMSES dynamic simulation. It takes as input:

- Network data (buses, lines, transformers, etc.)
- Power flow data specified at PV, PQ, and slack buses
- Control parameters (tolerances, reactive power limits, etc.), optional, defaults are used if not provided

### Solution Method

The power flow equations are solved by the Newton-Raphson method in polar coordinates. A solution is accepted when the active and reactive power mismatches are below their thresholds, all transformer ratio and phase-shift controls are satisfied, and all generators and static var compensators are within their reactive limits.

### Controls and Limits

During the solution Helios:

- enforces the reactive power limits of generators and static var compensators;
- adjusts the ratios of in-phase transformers to bring voltage magnitudes inside specified deadbands;
- adjusts phase-shifting transformers to bring active power flows inside specified deadbands.

### AC/DC Networks

Helios solves a combined AC-DC power flow. The AC network, the DC buses and lines of one or more DC grids, and the voltage-source converters joining them are solved together in the same Newton iteration, with optional DC voltage droop and converter losses.

### Results

Helios produces an output file including:

- the voltage magnitudes and phase angles at all buses of the network;
- the adjustable transformer data with updated values of their ratios.

It can also aggregate results by zone and by cut, and render a solved case onto an SVG one-line diagram of the network.

[Power Flow](/user-guide/power-flow/) is the complete record and parameter reference.

## RAMSES Module

RAMSES simulates the dynamic response of power system models under the phasor (RMS) approximation. It takes as input:

- Network data (shared with the power flow, with a few exceptions detailed in this documentation)
- Dynamic component data
- Solver control parameters (tolerances, time steps, reference speed, etc.)
- Sequence of disturbances and actions

### Solution Method

Three implicit integration methods are available: Backward Euler, Trapezoidal and BDF2. BDF2 allows larger time steps when fast transients are not of interest.

### Solver Acceleration

The solver was developed for simulations that last longer (long-term stability studies) or involve larger models (to account for active distribution networks). It gets its speed from two techniques:

- **Parallel processing.** The model is decomposed into the network, the injectors and the two-ports, and the work on injectors and two-ports is distributed among threads. A Schur-complement approach for the network equations gives exactly the same solution as a non-decomposed scheme. The implementation is general: there is no hand-crafted optimization particular to the computer system, the power system, or the disturbance.
- **Localization.** After a disturbance, components show different levels of dynamic activity. At each time step RAMSES skips Newton iterations on converged injectors and two-ports, and replaces latent (inactive) injectors with sensitivity-based models. Injectors switch between categories according to their activity.

### Results

RAMSES records the trajectories of the observed variables during the simulation, for plotting in either edition. It can also perform a [small-signal stability analysis](/user-guide/eigenanalysis/) of an operating point.

The papers describing these methods are listed under [Publications](/resources/references/).

## CODEGEN Module

CODEGEN allows incorporating user-defined models in RAMSES. The user describes a model in a text file, and CODEGEN translates it into Fortran 2003 code for compilation and linking.

Four types of user-defined models are supported:

- **Excitation controllers** (EXC): excitation system and automatic voltage regulator
- **Torque controllers** (TOR): turbine and speed governor
- **Injectors** (INJ): components connected to a single AC bus
- **Two-ports** (TWOP): components connecting two buses

The user model is **compiled, not interpreted**, resulting in efficient number-crunching code. While the solver code is proprietary, the models are designed to be freely shared, making STEPSS an **open-source simulation software** for the modeling part.

### CODEGEN Studio

[CODEGEN Studio](/developer/cg-studio/) is a browser-based visual editor for building CODEGEN models. Instead of writing DSL files by hand, you drag blocks onto a canvas, connect them, and export a valid model file. It can also import existing DSL files for visual inspection and editing.

## Platform Support

| Feature | Details |
|---------|---------|
| **STEPSS GUI** | Windows, Linux and macOS (Apple Silicon), Java bundled |
| **stepss** | Windows, Linux and macOS (Apple Silicon), Python 3.x |
| **Command-line executables** | Windows, Linux and macOS (Apple Silicon) for ramses, helios, codegen and dyngraph |
| **Custom model compilation** | gfortran, GNU make and OpenBLAS (MSYS2 on Windows) |
| **Free version limits** | 1000 buses max, 2 OpenMP cores |

## Next Steps

- [Installation](/getting-started/installation/), Set up STEPSS on your system
- [Quick Start](/getting-started/quickstart/), Run your first simulation
- [License](/getting-started/license/), Terms and the free-version limits above
- [Publications](/resources/references/), Papers describing the methods used here
- [Repositories](/resources/repositories/), Source for every STEPSS component
