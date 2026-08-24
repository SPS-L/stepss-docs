---
title: Solver Settings
description: Configuration parameters for the RAMSES solver
---

Solver settings control the behavior of the RAMSES simulation engine. They are specified as records starting with `$` in the data files.

## Watch it

Episode 4 of the [video series](/resources/videos/), *Solvers, Tolerances and Parallelism*, covers this page.

<div class="video-embed"><iframe src="https://www.youtube-nocookie.com/embed/AkI3k0xcRuQ" title="STEPSS Episode 4: Solvers, Tolerances and Parallelism" loading="lazy" allowfullscreen allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"></iframe></div>

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

How often the engine flushes the run-time observable file, in seconds. A reader
watching that file, such as STEPSS GUI's run-time curve window, polls at this
rate, so it is also how often those curves advance:

```
$GP_REFRESH_RATE time_interval(s) ;
```

### Gnuplot Invocation

Whether the engine drives Gnuplot itself through a pipe. With `F` it writes the
observable file and the `.plt` script beside it and calls nothing, which is what
the STEPSS interfaces read. With `T` it pipes to Gnuplot, which must then be on
the `PATH`; STEPSS does not ship it.

```
$CALL_GP T/F ;
```

Default: `F`.

### Gnuplot Output Mode

Which terminal the `.plt` script names, for opening that script in Gnuplot. It
has no effect on the curves STEPSS draws:

```
$GP_MODE term/png ;
```

Default: `term`.

### Observable Buffer Size

Internal memory reserved for storing observables during simulation:

```
$OBS_BUFFER_SIZE size(GB) ;
```

Default: 8 GB. Set this to less than half of your available RAM for large simulations.

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

- `SYN`: Synchronous reference frame (suitable for short-term simulations)
- `COI`: Center of inertia reference (suitable for long-term simulations)

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

### Minimum Branch Impedance

Branches whose series impedance magnitude is below this threshold have their resistance/reactance floored to it, to avoid a singular network admittance matrix:

```
$ZMIN value(pu) ;
```

Default: `1e-05`.

## Advanced Solver Options

### Solution Scheme

```
$SCHEME DE/IN ;
```

- `DE`: Decomposed scheme
- `IN`: Integrated scheme

### Small-Signal Analysis Size Limit

Largest state count accepted by [small-signal analysis](/user-guide/eigenanalysis/):

```
$EIG_MAX_STATES Number ;
```

Default: `5000`. The reduced state matrix is solved densely, so the peak
workspace is roughly $9N_x^2$ doubles, about 1.8 GB at the default. Above the
limit the analysis refuses and exits 78 rather than attempting the allocation.

### Participation Factor Floor

Floor below which a participation entry is not written to `<name>_pf.dat` by
[small-signal analysis](/user-guide/eigenanalysis/#namepfdat):

```
$PF_THRES Number ;
```

Default: `1e-3`. This is a size guard rather than a parameter of the analysis,
which is why it sits here beside `$EIG_MAX_STATES` and not on the `EIG` record.
Participation is the one output quadratic in the state count, one row per
(mode, state) pair, so at the `$EIG_MAX_STATES` default an unfloored file would
be 25 million rows and roughly 2 GB.

No mode can be emptied by it for any value below 1: each mode's column is
normalised so its largest entry is exactly 1. Raise it to bound the file on a
large system; lower it to see smaller entries. Which entries are worth reading
is decided by whoever reads the file, not here.

### Latency Settings

```
$LATENCY OBS_TIME_WINDOW(s) EARLY_STOP(T/F) ;
```

### Subnetwork Latency

Apply the latency technique at the subnetwork level: subnetworks whose currents change less than the latency tolerance are not recomputed at each step. Only active when subnetworks exist:

```
$LAT_SUBNETS T/F ;
```

Default: `F`.

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

## License

Provide the licensee e-mail and the 64-character license key. A valid key unlocks the full version, removing the free-tier limit of 1000 buses:

```
$LICENSE email license_key ;
```

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

- [Python API](/python/api-reference/), Run simulations programmatically from Python
- [Test Systems](/test-systems/), Try one of the benchmark systems
