---
title: Python API
description: stepss, the Python package that scripts RAMSES and Helios from Python
---

**STEPSS for Python** is one of the platform's [two editions](/getting-started/overview/#two-editions),
distributed as the `stepss` package on PyPI. The other is STEPSS for Java, a
desktop application; both drive the same engines and read the same data files,
so a case built in one runs unchanged in the other.

This edition is not a simulator itself. It is a scriptable interface to the
RAMSES dynamic simulation engine and the Helios AC power-flow engine, bundling
both engines' pre-compiled binaries so no separate installation is required.
Trajectory plotting is built in, implemented in Python on top of Matplotlib
rather than by launching the DYNGRAPH viewer the Java edition uses. CODEGEN is
the one capability carried only by that edition.

| Page | Covers |
|------|--------|
| [Overview](/python/overview/) | What the package provides, package-level attributes, main classes |
| [Installation](/python/installation/) | Installing stepss, version numbering, platform prerequisites |
| [Examples](/python/examples/) | Worked simulation scripts |
| [API Reference](/python/api-reference/) | Complete reference for `cfg`, `sim`, and `extractor` |
| [Helios Power-Flow API](/python/helios/) | Running AC power flows from Python with `HeliosSession` |

## Next Steps

- [Quick Start](/getting-started/quickstart/), a first simulation end to end
- [Test Systems](/test-systems/), ready-to-run networks to try stepss against
