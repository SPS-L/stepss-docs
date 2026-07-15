---
title: PyRAMSES Overview
description: Python-based RApid Multithreaded Simulation of Electric power Systems
---

**PyRAMSES** is a Python module that provides an interface to the RAMSES dynamic simulator and the Helios AC power-flow engine. It covers the full workflow: defining test cases, launching simulations, querying system states at runtime, extracting and plotting results, and running power flows. The package embeds pre-compiled RAMSES binaries (Windows and Linux) plus Helios power-flow libraries (Windows, Linux, and macOS) and exposes them through a clean Python API.

For more information, visit the [PyRAMSES project page](https://sps-lab.org/project/pyramses/).

## Package-Level Attributes

After importing the package, the following attributes are available:

| Attribute | Description |
|-----------|-------------|
| `pyramses.__version__` | Current version string (e.g., `'0.1.0'`) |
| `pyramses.__url__` | Documentation URL |
| `pyramses.__runTimeObs__` | `True` if Gnuplot was found in PATH at import time; runtime observables will be active |

## Main Classes

| Class | Description |
|-------|-------------|
| `pyramses.cfg` | Defines a test case: data files, disturbance file, output files, observables, and runtime options. |
| `pyramses.sim` | Runs simulations. Supports start/pause/continue, runtime queries, and disturbance injection. |
| `pyramses.extractor` | Extracts and visualises time-series results from trajectory files produced by a simulation. |
| `pyramses.helios.HeliosSession` | Runs AC power flows with the Helios engine: load, modify with redispatch, solve, contingency screening, and file exports. |

## Platform Support

PyRAMSES supports Windows and Linux for dynamic simulation; the bundled Helios power-flow engine additionally runs on macOS. All binaries are bundled directly in the package, no separate simulator installation is required.

## Further Reading

- [API Reference](/pyramses/api-reference/), Detailed documentation for `cfg`, `sim`, and `extractor`
- [Power Flow (Helios)](/pyramses/helios/), Running AC power flows from Python with `HeliosSession`
- [Examples](/pyramses/examples/), Practical simulation examples and notebooks

## Repository

Source code: [SPS-L/stepss-pyramses](https://github.com/SPS-L/stepss-pyramses)
