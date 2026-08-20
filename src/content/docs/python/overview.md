---
title: Python API Overview
description: Python interface to the RAMSES dynamic simulator and Helios power-flow engine
---

**stepss** is the package that delivers [STEPSS in Python](/getting-started/overview/#two-editions), one of the platform's two editions. It provides an interface to the RAMSES dynamic simulator and the Helios AC power-flow engine, covering the full workflow: defining test cases, launching simulations, querying system states at runtime, extracting and plotting results, and running power flows. The package embeds pre-compiled RAMSES and Helios libraries for Windows, Linux, and macOS and exposes them through a clean Python API.

## Package-Level Attributes

After importing the package, the following attributes are available:

| Attribute | Description |
|-----------|-------------|
| `stepss.__version__` | Current version string |
| `stepss.__ramses_version__` | Version of the bundled RAMSES library |
| `stepss.__helios_version__` | Version of the bundled Helios library |
| `stepss.__url__` | Documentation URL |
| `stepss.__runTimeObs__` | Always `True`, and deprecated. Do not branch on it |

## Main Classes

| Class | Description |
|-------|-------------|
| `stepss.cfg` | Defines a test case: data files, disturbance file, output files, observables, and runtime options. |
| `stepss.sim` | Runs simulations. Supports start/pause/continue, runtime queries, and disturbance injection. |
| `stepss.extractor` | Extracts and visualises time-series results from trajectory files produced by a simulation. |
| `stepss.monitor` | Plots chosen quantities while a simulation runs, one panel per observable. |
| `stepss.helios.HeliosSession` | Runs AC power flows with the Helios engine: load, modify with redispatch, solve, contingency screening, and file exports. |

## Platform Support

stepss supports Windows, Linux, and macOS for both dynamic simulation and power flows. All binaries are bundled directly in the package, no separate simulator installation is required. See the [installation guide](/python/installation/) for per-platform system prerequisites.

## Further Reading

- [API Reference](/python/api-reference/), Detailed documentation for `cfg`, `sim`, `extractor` and `monitor`
- [Power Flow (Helios)](/python/helios/), Running AC power flows from Python with `HeliosSession`
- [Examples](/python/examples/), Practical simulation examples and notebooks

## Repository

Source code: [SPS-L/stepss-python-ui](https://github.com/SPS-L/stepss-python-ui)
