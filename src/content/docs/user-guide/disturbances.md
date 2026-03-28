---
title: Disturbances
description: Specifying disturbances and actions in dynamic simulations
---

Disturbances define the sequence of events during a dynamic simulation. All disturbance commands follow the format:

```
time(s) COMMAND parameters
```

## Continue Solver

Defines solver settings. **Must be the first line** of the disturbance file:

```
time(s) CONTINUE SOLVER disc_meth max_h(s) min_h(s) latency(pu) upd_over
```

**Discretization method** (`disc_meth`):
- `TR` — Trapezoidal
- `BE` — Backward Euler
- `BD` — BDF2

**Jacobian update override** (`upd_over`):
- `ALL` — Update all injectors and network
- `NET` — Update only network
- `ABL` — Update only injectors
- `IBL` — Update all injectors and network
- `NOT` — Do not override

**Example**:
```
0.000 CONTINUE SOLVER BD 0.0200 0.001 0. ALL
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

**Example** — opening both ends of a line at $t = 10$ s:
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

## Three-Phase Short-Circuit (Impedance)

Apply a three-phase fault with specified impedance to ground:

```
time(s) FAULT BUS name_of_bus rfault [xfault]
time(s) CLEAR BUS name_of_bus
```

- `rfault` and `xfault` are in Ω
- If `xfault` is omitted, a fully resistive fault is assumed

**Example** — 100 ms bolted fault:
```
10.000 FAULT BUS 1044 0. 0.
10.100 CLEAR BUS 1044
```

## Three-Phase Short-Circuit (Voltage)

Apply a fault where the post-fault voltage is specified:

```
time(s) VFAULT BUS name_of_bus Voltage_after_fault(pu)
time(s) CLEAR BUS name_of_bus
```

**Example** — 100 ms fault with 0.5 pu residual voltage:
```
10.000 VFAULT BUS 1044 0.5
10.100 CLEAR BUS 1044
```

:::note
Supported from version 3.13 onwards.
:::

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

The increment is in MVAr.

### Exciter Parameters

```
time(s) CHGPRM EXC name_of_equipment name_of_parameter ±increment [MVAr/%] duration(s)
```

**Units**: No unit = absolute, `MVAr` = per-unitized by $S_{nom}$, `%` = percentage of original.

**Duration**: `0` = step change, `> 0` = ramp over given duration.

**Example** — ramp voltage setpoint by +10% over 10 seconds:
```
10.000 CHGPRM EXC g1 V0 +10 % 10
```

### Torque Controller Parameters

```
time(s) CHGPRM TOR name_of_equipment name_of_parameter ±increment [MW/%] duration(s)
```

**Example** — ramp active power setpoint by +1 MW:
```
10.000 CHGPRM TOR g1 P0 +1 MW 10
```

### Injector / Two-Port / Discrete Controller Parameters

```
time(s) CHGPRM INJ/TWOP/DCTL name ±increment [MW/MVAr/%/SETP] duration(s)
```

**Units**: `SETP` = the increment is the new setpoint value.

**Example** — load increase of 50% active and 30% reactive over 60 seconds:
```
10.000 CHGPRM INJ L_11 P0 +50 % 60
10.000 CHGPRM INJ L_11 Q0 +30 % 60
```

## Export Jacobian Matrix

```
time(s) JAC 'name_of_filename'
```

Required solver settings:
```
$OMEGA_REF SYN ;
$SCHEME IN ;
```

## Export Load Flow Snapshot

Takes a snapshot and exports the load flow at a specific time:

```
time(s) LFRESV 'name_of_filename'
```
