---
title: PyRAMSES Overview
description: Python-based RApid Multithreaded Simulation of Electric power Systems
---

**PyRAMSES** is a Python module that provides an interface to the RAMSES dynamic simulator. It covers the full simulation workflow: defining test cases, launching simulations, querying system states at runtime, and extracting and plotting results. The package embeds pre-compiled RAMSES binaries (dynamic libraries) for both Windows and Linux and exposes them through a clean Python API.

For more information, visit the [PyRAMSES project page](https://sps-lab.org/project/pyramses/) and the [PyRAMSES documentation site](https://pyramses.sps-lab.org/).

## Package-Level Attributes

After importing the package, the following attributes are available:

| Attribute | Description |
|-----------|-------------|
| `pyramses.__version__` | Current version string (e.g., `'0.0.65'`) |
| `pyramses.__url__` | Documentation URL (`https://pyramses.sps-lab.org`) |
| `pyramses.__runTimeObs__` | `True` if Gnuplot was found in PATH at import time; runtime observables will be active |

## Main Classes

| Class | Description |
|-------|-------------|
| `pyramses.cfg` | Defines a test case: data files, disturbance file, output files, observables, and runtime options. |
| `pyramses.sim` | Runs simulations. Supports start/pause/continue, runtime queries, and disturbance injection. |
| `pyramses.extractor` | Extracts and visualises time-series results from trajectory files produced by a simulation. |

## Platform Support

PyRAMSES supports both Windows and Linux operating systems. Pre-compiled RAMSES binaries are bundled directly in the package — no separate simulator installation is required.

## Further Reading

- [API Reference](/pyramses/api-reference/) — Detailed documentation for `cfg`, `sim`, and `extractor`
- [Examples](/pyramses/examples/) — Practical simulation examples and notebooks

## Repository

Source code: [SPS-L/stepss-PyRAMSES](https://github.com/SPS-L/stepss-PyRAMSES)
