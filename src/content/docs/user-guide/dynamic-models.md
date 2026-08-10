---
title: Dynamic Data Records
description: Record syntax for machines, injectors, two-ports, and discrete controllers
---

This page is the reference for the **record syntax** of the dynamic data file: which
records exist, what their fields mean, and how a model name is resolved. The models
themselves (names, parameters, equations) are documented in the
[Model Reference](/models/), one page per family.

## Model Names and Prefixes

Every device record names a model. RAMSES adds the family prefix automatically, so
both forms resolve to the same model:

| Record | Prefix added | Example, equivalent forms |
|--------|--------------|---------------------------|
| `EXC` | `exc_` | `AC1A`, `exc_AC1A` |
| `TOR` | `tor_` | `HYGOV`, `tor_HYGOV` |
| `INJEC` | `inj_` | `GFOL`, `inj_GFOL` |
| `TWOP` | `twop_` | `HVDC_LCC`, `twop_HVDC_LCC` |
| `DCTL` | none | `LTC` |

Model names are **case sensitive**. A name that is compiled into RAMSES but not
registered in the dispatcher is rejected at load time; see
[User-Defined Models](/developer/user-models/) for how to register one through
URAMSES. The [Model Reference index](/models/) marks which models are callable
out of the box and which are not.

## Common Injection Fields

The `SYNC_MACH`, `INJEC` and `IMPLOAD` records all begin with the same four
initialization fields, which set the device's share of the bus injection computed
by the power flow:

| Field | Description | Unit |
|-------|-------------|------|
| `FP` | Fraction of the bus active injection taken by this device | - |
| `FQ` | Fraction of the bus reactive injection taken by this device | - |
| `P` | Initial active power, used when `FP` is zero | MW |
| `Q` | Initial reactive power, used when `FQ` is zero | Mvar |

:::caution[Give the fraction or the power, never both]
For each of the two pairs, exactly one member must be zero. RAMSES stops with
`either the fraction or the active power picked up must be zero` if both `FP` and
`P` are non-zero, and with the matching message for `FQ` and `Q`.
:::

`P` and `Q` are physical powers in MW and Mvar; RAMSES divides them by the system
base to obtain per unit. See
[Reference Frames & Initialization](/user-guide/reference-frames/) for how these
values feed the initialization.

## Synchronous Machines

A synchronous machine is specified with its excitation controller (`EXC`) and torque
controller (`TOR`):

```
SYNC_MACH Name BUS_NAME FP FQ P Q Snom Pnom H D ibratio
  XT/RL Xl Xd X'd X"d Xq X'q X"q m n Ra T'do T"do T'qo T"qo

EXC EXC_TYPE parameters_passed_to_EXC

TOR TOR_TYPE parameters_passed_to_TOR ;
```

For the complete mathematical model, the per unit system, and the parameter list,
see the [Synchronous Machine Model](/models/synchronous-machine/) page.

The `parameters_passed_to_EXC` and `parameters_passed_to_TOR` fields are the model's
data parameters, in the order the model declares them. That order is authoritative
per model:

- [IEEE Exciters](/models/ieee-exciters/) and [Custom Exciters](/models/custom-exciters/)
- [IEEE Governors](/models/ieee-governors/) and [Custom Governors](/models/custom-governors/)

## Injectors

An injector is a component connected to a single AC bus:

```
INJEC INJ_TYPE NAME BUS_NAME FP FQ P Q parameters_passed_to_INJ ;
```

The trailing fields are the model's data parameters in declaration order. For the
catalogue of injector models and their parameters, see
[Injector Models](/models/custom-injectors/).

Two injectors are worth noting here because they affect the whole simulation rather
than one bus:

- **`THEVEQ`** imposes a constant-frequency voltage source and forces the
  synchronous reference frame. Its single data parameter is the three-phase
  short-circuit power of the equivalent network, in MVA, which RAMSES converts to
  the Thévenin reactance at initialization. See
  [Thévenin Equivalent](/models/custom-injectors/#theveq-inj_theveq-thévenin-equivalent).
- **`VFAULT`** is added automatically by RAMSES to apply voltage faults; you do not
  write it yourself.

## Impedance Loads

`IMPLOAD` is a record in its own right, not an `INJEC` model, and takes no model
parameters:

```
IMPLOAD loadname BUS_NAME FP FQ P Q ;
```

A constant-impedance load holds its admittance fixed at the value implied by the
initial voltage, so its power varies with the square of the bus voltage. The record
has exactly six fields; the `FP`/`FQ`/`P`/`Q` group behaves as described in
[Common Injection Fields](#common-injection-fields).

Any bus injection left unclaimed after all `INJEC` and `IMPLOAD` records are
processed is converted into an impedance load automatically, named with an `M_`
prefix. Only residuals whose current magnitude exceeds `$NETTOL` are converted, so
a bus that balances exactly gains no extra load.

## Two-Port Components

Two-port components connect two buses, and carry an independent injection group for
each end:

```
TWOP MODEL_NAME TWOP_NAME BUS1 BUS2 IND FP1 FQ1 P1 Q1 FP2 FQ2 P2 Q2 DATA1 DATA2 ... ;
```

| Field | Description |
|-------|-------------|
| `MODEL_NAME` | Two-port model name, with or without the `twop_` prefix |
| `TWOP_NAME` | Name of this device |
| `BUS1`, `BUS2` | Names of the two connected buses |
| `IND` | Connection indicator |
| `FP1` … `Q1` | Injection group for end 1, as in [Common Injection Fields](#common-injection-fields) |
| `FP2` … `Q2` | Injection group for end 2 |
| `DATA1 DATA2 …` | Model data parameters, in declaration order |

For the available models and their parameters, see
[Two-Port Models](/models/two-port-models/).

## Discrete Controllers

Discrete controllers act on the system at discrete instants rather than through
differential equations:

```
DCTL CTRL_TYPE CTLNAME parameters ;
```

`DCTL` takes no prefix and the names are uppercase. For the catalogue, the field
lists, and the switching logic of each controller, see
[Discrete Controller Models](/models/discrete-controllers/).

## Next Steps

- [Model Reference](/models/), Browse the model catalogue
- [Disturbances](/user-guide/disturbances/), Define faults, trips, and parameter changes
- [Solver Settings](/user-guide/solver-settings/), Configure the numerical solver
