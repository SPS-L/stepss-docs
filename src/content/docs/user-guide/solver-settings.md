---
title: Solver Settings
description: Configuration parameters for the RAMSES solver
---

Solver settings control the behavior of the RAMSES simulation engine. They are specified as records starting with `$` in the data files.

## Sampling and Output

### Plot Step

Sampling time for observed variables:

```
$PLOT_STEP time(s) ;
```

### Display Profiling

Display profiling results after simulation:

```
$DISP_PROF T/F ;
```

### Run-Time Refresh Rate

Refresh interval for runtime observable plots (requires Gnuplot):

```
$GP_REFRESH_RATE time_interval(s) ;
```

### Observable Buffer Size

Internal memory reserved for storing observables during simulation:

```
$OBS_BUFFER_SIZE size(GB) ;
```

Default: 8 GB. Set this to less than half of your available RAM for large simulations.

### Sparse Solver

Selects the sparse linear solver used for Jacobian factorization:

```
$SPARSE_SOLVER name ;
```

- `KLU` — SuiteSparse KLU solver (default)
- `ma41` — HSL MA41 solver

## System Parameters

### Base Power

Sets the global base power of the system:

```
$S_BASE BASE(MVA) ;
```

### Nominal Frequency

```
FNOM Frequency(Hz) ;
```

### Reference Frame

```
$OMEGA_REF SYN/COI ;
```

- `SYN` — Synchronous reference frame (suitable for short-term simulations)
- `COI` — Center of inertia reference (suitable for long-term simulations)

See [Reference Frames](/user-guide/reference-frames/) for details.

## Numerical Parameters

### Newton Tolerance

```
$NEWTON_TOLER NETWORK_TOLERANCE INJ_RELATIVE_TOLERANCE INJ_ABSOLUTE_TOLERANCE ;
```

Default values: `1e-03`, `5e-04`, `5e-04`.

### Finite Difference Values

Values used to compute Jacobian matrices of injectors numerically:

```
$FIN_DIFFER proportional_value absolute_value ;
```

### Full Jacobian Update

Disable partial Jacobian updates (force full update at every step):

```
$FULL_UPDATE T/F ;
```

### Skip Converged Blocks

Activate/deactivate skipping of converged injectors in Newton iterations:

```
$SKIP_CONV T/F ;
```

### Maximum Fault Value

```
$MAX_FAULT value ;
```

## Advanced Solver Options

### Solution Scheme

```
$SCHEME DE/IN ;
```

- `DE` — Decomposed scheme
- `IN` — Integrated scheme

### Latency Settings

```
$LATENCY OBS_TIME_WINDOW(s) EARLY_STOP(T/F) ;
```

### Load Restoration Time Constant

```
$T_LOAD_REST time(s) ;
```

### Network Frequency Update

Update network elements (admittances) with frequency:

<img src="/images/freq_upd_vminmax.svg" alt="Network frequency update model" style="width:60%" />

```
$NET_FREQ_UPD T/F ;
```

## Parallel Computing

### Number of Threads

```
$NB_THREADS Number ;
```

:::note
The free academic version is limited to **2 threads**.
:::

### Thread Distribution Strategy

```
$OMP STA/DYN/GUI chunk ;
```

| Option | Description |
|--------|-------------|
| `STA` | Static assignment (better for NUMA architectures) |
| `DYN` | Dynamic assignment (better for UMA architectures) |
| `GUI` | Guided assignment |

`chunk` is the number of consecutive injectors assigned to each thread.

## Typical Configuration

```
# System base
$S_BASE 100. ;
FNOM 50. ;

# Reference frame (COI for long-term)
$OMEGA_REF COI ;

# Solution scheme
$SCHEME IN ;

# Solver tolerances
$NEWTON_TOLER 1e-03 5e-04 5e-04 ;

# Plotting
$PLOT_STEP 0.01 ;

# Parallel computing
$NB_THREADS 2 ;
$OMP DYN 50 ;

# Acceleration features
$SKIP_CONV T ;
$FULL_UPDATE F ;
```

## Next Steps

- [PyRAMSES API](/pyramses/api-reference/) — Run simulations programmatically from Python
- [Test Systems](/test-systems/nordic/) — Try the Nordic or 5-bus benchmark systems
