---
title: Eigenanalysis
description: Small-signal stability analysis with the RAMSES Eigenanalysis tool
---

The [RAMSES Eigenanalysis tool](https://github.com/SPS-L/RAMSES-Eigenanalysis) is a MATLAB-based tool for computing eigenvalues and eigenvectors of power system models in descriptor form, extracted from RAMSES simulations.

## Overview

The tool analyzes small-signal stability by computing eigenvalues of the system Jacobian matrix. It supports both differential-algebraic equation (DAE) systems and provides multiple computational methods.

## Features

- **Multiple analysis methods**: QZ (standard), ARPACK (sparse), Arnoldi (iterative), JDQR (targeted)
- **Interactive analysis**: dominant eigenvalue identification, mode shape analysis, participation factors, damping ratios
- **Automatic Jacobian extraction** from RAMSES simulation data

## Prerequisites

- **MATLAB** R2016a or later
- **PyRAMSES** for Jacobian matrix extraction

## Installation

```matlab
addpath('path/to/RAMSES-Eigenanalysis')
addpath('path/to/RAMSES-Eigenanalysis/scripts')
```

## Workflow

### 1. Extract Jacobian from RAMSES

Use PyRAMSES to run a simulation and export the Jacobian:

```python
import pyramses

ram = pyramses.sim()
case = pyramses.cfg('cmd.txt')
ram.execSim(case)
```

Ensure the disturbance file includes the Jacobian export command:

```
time(s) JAC 'jac'
```

And the solver settings include:

```
$OMEGA_REF SYN ;
$SCHEME IN ;
```

### 2. Run Eigenanalysis in MATLAB

```matlab
ssa('jac_val.dat', 'jac_eqs.dat', 'jac_var.dat', 'jac_struc.dat')
```

With custom parameters:

```matlab
ssa('jac_val.dat', 'jac_eqs.dat', 'jac_var.dat', 'jac_struc.dat', ...
    real_limit, damp_ratio, method)
```

### Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `jac_val.dat` | Matrix values in coordinate format | — |
| `jac_eqs.dat` | Equation descriptions (differential/algebraic) | — |
| `jac_var.dat` | Variable descriptions (differential/algebraic) | — |
| `jac_struc.dat` | Decomposed power system structure (optional) | — |
| `real_limit` | Real part threshold for dominant eigenvalues | $-\infty$ |
| `damp_ratio` | Damping ratio threshold | 1.0 |
| `method` | Analysis method: `'QZ'` or `'ARP'` | `'QZ'` |

## Analysis Methods

### QZ Method (Default)

- Uses MATLAB's `eig()` function with algebraic variable elimination
- Suitable for **small to medium systems** (< 50,000 states)
- Provides the complete eigenvalue spectrum
- Supports mode shape and participation factor analysis

### ARPACK Method

- Sparse descriptor approach using Krylov-Schur algorithm via MATLAB's `eigs()`
- Suitable for **large systems**
- Computes a subset of eigenvalues near a specified target

### JDQR Method

- Jacobi-Davidson QR method for targeted eigenvalue computation
- Useful for finding specific eigenvalues (e.g., poorly damped modes)

## Interactive Analysis

After computing eigenvalues, the tool provides an interactive menu to:

1. View dominant eigenvalues
2. Analyze mode shapes
3. Calculate participation factors
4. Examine damping ratios
5. Explore system structure

## Repository

Source code: [SPS-L/RAMSES-Eigenanalysis](https://github.com/SPS-L/RAMSES-Eigenanalysis)
