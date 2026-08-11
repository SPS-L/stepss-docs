---
title: Python API Overview
description: Python interface to the RAMSES dynamic simulator and Helios power-flow engine
---

**stepss** is a Python module that provides an interface to the RAMSES dynamic simulator and the Helios AC power-flow engine. It covers the full workflow: defining test cases, launching simulations, querying system states at runtime, extracting and plotting results, and running power flows. The package embeds pre-compiled RAMSES and Helios power-flow libraries for Windows, Linux, and macOS and exposes them through a clean Python API.

## Package-Level Attributes

After importing the package, the following attributes are available:

| Attribute | Description |
|-----------|-------------|
| `stepss.__version__` | Current version string |
| `stepss.__ramses_version__` | Version of the bundled RAMSES library |
| `stepss.__helios_version__` | Version of the bundled Helios library |
| `stepss.__url__` | Documentation URL |
| `stepss.__runTimeObs__` | `True` if Gnuplot was found in PATH at import time; runtime observables will be active |

## Main Classes

| Class | Description |
|-------|-------------|
| `stepss.cfg` | Defines a test case: data files, disturbance file, output files, observables, and runtime options. |
| `stepss.sim` | Runs simulations. Supports start/pause/continue, runtime queries, and disturbance injection. |
| `stepss.extractor` | Extracts and visualises time-series results from trajectory files produced by a simulation. |
| `stepss.helios.HeliosSession` | Runs AC power flows with the Helios engine: load, modify with redispatch, solve, contingency screening, and file exports. |

## Platform Support

stepss supports Windows, Linux, and macOS for both dynamic simulation and power flows. All binaries are bundled directly in the package, no separate simulator installation is required. See the [installation guide](/python/installation/) for per-platform system prerequisites.

## Further Reading

- [API Reference](/python/api-reference/), Detailed documentation for `cfg`, `sim`, and `extractor`
- [Power Flow (Helios)](/python/helios/), Running AC power flows from Python with `HeliosSession`
- [Examples](/python/examples/), Practical simulation examples and notebooks

## Repository

Source code: [SPS-L/stepss-python-ui](https://github.com/SPS-L/stepss-python-ui)

:::note[Renamed from PyRAMSES]
This package was published as `pyramses` up to version 3.58. Existing code
keeps working: `pip install pyramses` installs a shim that forwards to
`stepss`. New code should use `import stepss`.
:::
