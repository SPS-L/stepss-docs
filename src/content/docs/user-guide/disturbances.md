---
title: Disturbances
description: Specifying disturbances and actions in dynamic simulations
---

Disturbances define the sequence of events during a dynamic simulation. Disturbances need to have a continuity. All disturbance commands follow the format:

```
time(s) COMMAND parameters
```

## Continue Solver

Defines solver settings. **Must be the first line** of the disturbance file:

```
time(s) CONTINUE SOLVER disc_meth max_h(s) min_h(s) latency(pu) upd_over
```

**Discretization method** (`disc_meth`):
- `TR`: Trapezoidal
- `BE`: Backward Euler
- `BD`: BDF2

**Jacobian update override** (`upd_over`):
- `ALL`: Force a full Jacobian refactorisation
- `NET`: Force a refactorisation of the network Jacobian
- `ABL`: Force an update of the injector Jacobian at every bus
- `IBL`: Force nothing in addition, but keep the bus Jacobian updates already requested by the other disturbances applied at this time instant
- `NOT`: Override, discarding even those; the bus Jacobian flags are restored to their values on entry

**Example**:
```
0.000 CONTINUE SOLVER BD 0.0200 0.001 0. ALL
```

## Continue Display

Changes the sampling time step used for the output of observed variables from that point of the simulation onwards:

```
time(s) CONTINUE DISPLAY new_plot_step(s)
```

**Example**, reducing the output sampling to one point per second after $t = 20$ s:
```
20.000 CONTINUE DISPLAY 1.0
```

## Stop

Signals the end of the simulation. **Must be the last line**:

```
time(s) STOP
```

**Example**:
```
100.000 STOP
```

## Trip Line (BREAKER BRANCH)

Open or close breakers of a line:

```
time(s) BREAKER BRANCH name_of_line orig_break(0/1) extrem_break(0/1)
```

**Example**, opening both ends of a line at $t = 10$ s:
```
10.000 BREAKER BRANCH 1044-4032 0 0
```

## Trip Machine / Injector

Open or close the breaker of a synchronous machine or injector:

```
time(s) BREAKER SYNC_MACH name_of_machine breaker(0/1)
time(s) BREAKER INJ name_of_injector breaker(0/1)
```

**Example**:
```
10.000 BREAKER INJ L_11 0
```

## Trip Two-Port

Disconnect a two-port component (e.g. an HVDC link) at both ends. Only opening is supported, so the breaker status must be `0`:

```
time(s) BREAKER TWOP name_of_twoport 0
```

**Example**:
```
10.000 BREAKER TWOP hvdc1 0
```

## Three-Phase Short-Circuit (Impedance)

Apply a three-phase fault with specified impedance to ground. This requires two commands, one to apply the fault and one to clear it.

```
time(s) FAULT BUS name_of_bus rfault [xfault]
time(s) CLEAR BUS name_of_bus
```

The fault has an impedance of `rfault + j*xfault` to ground:
- `rfault` and `xfault` are in Ω
- If `xfault` is omitted, a fully resistive fault is assumed

**Example**, 100 ms bolted fault:
```
10.000 FAULT BUS 1044 0. 0.
10.100 CLEAR BUS 1044
```

## Three-Phase Short-Circuit (Voltage)

Apply a fault where the post-fault voltage is specified. Internally, RAMSES creates a temporary shunt admittance $B_{fault}$ at the faulted bus and iteratively adjusts it using a secant method until the bus voltage matches the target value to within $\pm 0.5\%$. The injected currents are $i_x = B_{fault}\, v_x$ and $i_y = -B_{fault}\, v_y$. Up to 10 correction steps are attempted; if convergence is not reached, the simulation halts with an error message.

```
time(s) VFAULT BUS name_of_bus Voltage_after_fault(pu)
time(s) CLEAR BUS name_of_bus
```

**Example**, 100 ms fault with 0.5 pu residual voltage:
```
10.000 VFAULT BUS 1044 0.5
10.100 CLEAR BUS 1044
```

## Change Parameters (CHGPRM)

Modify model parameters during the simulation.

### Branch Parameters

```
time(s) CHGPRM BRANCH name_of_line MAGN/PHAN ±increment
```

### Shunt Parameters

```
time(s) CHGPRM SHUNT name_of_shunt QNOM ±increment
```

The increment is in MVAr and is per-unitized internally by RAMSES.

### Exciter Parameters

```
time(s) CHGPRM EXC name_of_equipment name_of_parameter ±increment [MVAr/%] duration(s)
```

**Units**: No unit = absolute, `MVAr` = per-unitized by $S_{nom}$, `%` = percentage of original.

**Duration**: `0` = step change, `> 0` = ramp over given duration.

**Example**, ramp voltage setpoint by +10% over 10 seconds:
```
10.000 CHGPRM EXC g1 V0 +10 % 10
```

This means the parameter V0 of the exciter of synchronous machine g1 is ramped by +10% between 10 and 20 seconds.

### Torque Controller Parameters

```
time(s) CHGPRM TOR name_of_equipment name_of_parameter ±increment [MW/%] duration(s)
```

**Units**: No unit = absolute, `MW` = per-unitized by $P_{nom}$ of the machine, `%` = percentage of original value.

**Duration**: `0` = step change, `> 0` = ramp over given duration.

**Example**, ramp active power setpoint by +1 MW over 10 seconds:
```
10.000 CHGPRM TOR g1 P0 +1 MW 10
```

This means the parameter P0 of the torque controller of synchronous machine g1 is ramped by +1 MW between 10 and 20 seconds.

### Injector / Two-Port / Discrete Controller Parameters

```
time(s) CHGPRM INJ/TWOP/DCTL name_of_equipment name_of_parameter ±increment [MW/MVAr/%/SETP] duration(s)
```

**Units**: No unit = absolute, `MW` or `MVAr` = per-unitized using the system's $S_{base}$, `%` = percentage of original value, `SETP` = the increment is the new setpoint value.

**Duration**: `0` = step change, `> 0` = ramp over given duration.

**Example**, load increase of 50% active and 30% reactive over 60 seconds:
```
10.000 CHGPRM INJ L_11 P0 +50 % 60
10.000 CHGPRM INJ L_11 Q0 +30 % 60
```

This means the parameter P0 (resp. Q0) of the injector L\_11 is ramped by +50% (resp. 30%) between 10 and 70 seconds. If L\_11 is a load model, this simulates a load increase.

## Export Jacobian Matrix

```
time(s) JAC 'name_of_filename'
```

Required solver setting:
```
$OMEGA_REF SYN ;
```

Under the COI reference frame RAMSES logs a warning and skips the export, because
the feature has not been validated there.

The number of files written depends on the integration scheme:

| Scheme | Files written |
|--------|---------------|
| `$SCHEME IN` (integrated) | `<name>_val.dat`, `<name>_eqs.dat`, `<name>_var.dat` |
| `$SCHEME DE` (decomposed) | the same three, plus `<name>_struc.dat` |

These files are the raw matrices. To have RAMSES analyse them instead, use `EIG`
below. A run that does both keeps the matrices and the analysis together if you
[save it as one archive](/user-guide/eigenanalysis/#saving-a-run-as-one-archive).

## Run Small-Signal Analysis

```
time(s) EIG 'name_of_filename'
```

Reduces the linearised model to a state matrix, solves the eigenproblem, and
writes `<name>_modes.dat`, `<name>_pf.dat` and `<name>_ms.dat`, all three
carrying every mode.

The record takes a basename and nothing else. It used to accept an optional
`real_limit` and `pf_threshold` pair; `real_limit` chose which modes got
participation and mode-shape output, which is now decided when the results are
read, and `pf_threshold` became the
[`$PF_THRES`](/user-guide/solver-settings/#participation-factor-floor) solver
setting. A record still carrying either is refused rather than having it
ignored.

Required solver settings:
```
$OMEGA_REF SYN ;
$SCHEME DE ;
```

Unlike `JAC`, which skips with a warning, `EIG` **refuses** when it cannot
produce a result it can justify: it writes nothing, states the reason in the
log, and exits with code 78. See
[Eigenanalysis](/user-guide/eigenanalysis/) for the output format, the
`$EIG_MAX_STATES` limit and the full list of refusal conditions.

## Export Load Flow Snapshot

Takes a snapshot and exports the load flow at a specific time:

```
time(s) LFRESV 'name_of_filename'
```

## Next Steps

- [Solver Settings](/user-guide/solver-settings/), Configure time steps, tolerances, and parallelism
- [Python API Examples](/python/examples/). See complete simulation workflows in Python
