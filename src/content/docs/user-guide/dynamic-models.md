---
title: Dynamic Models
description: Synchronous machines, injectors, two-ports, and discrete controllers
---

## Synchronous Machines

A synchronous machine is specified with its excitation controller (EXC) and torque controller (TOR):

```
SYNC_MACH Name BUS_NAME FP FQ P Q Snom Pnom H D ibratio
  XT/RL Xl Xd X'd X"d Xq X'q X"q m n Ra T'do T"do T'qo T"qo

EXC EXC_TYPE parameters_passed_to_EXC

TOR TOR_TYPE parameters_passed_to_TOR ;
```

| Parameter | Description | Unit |
|-----------|-------------|------|
| `FP`, `FQ` | Fractions of bus injection (active, reactive) | — |
| `P`, `Q` | Initial powers (used if fractions are zero) | pu |
| `Snom` | Nominal apparent power | MVA |
| `Pnom` | Nominal active power | MW |
| `H` | Inertia constant | s |
| `D` | Damping coefficient | pu |
| `Xd`, `X'd`, `X"d` | d-axis reactances (synchronous, transient, subtransient) | pu |
| `Xq`, `X'q`, `X"q` | q-axis reactances | pu |
| `T'do`, `T"do` | d-axis time constants (open-circuit transient, subtransient) | s |
| `T'qo`, `T"qo` | q-axis time constants | s |
| `Ra` | Armature resistance | pu |
| `Xl` | Leakage reactance | pu |

### Available Exciter Models

The following exciter types are available in the current version:

`1storder`, `constant`, `kundur`, `generic1`, `generic2`, `GENERIC3`, `GENERIC4`, `ST1A`, `ST1A_lim`, `ST1A_OELHQ`, `ST1A_PSS2B`, `ST1A_PSS3B`, `ST1A_PSS4B`, `ST1A_IEEEST`, `ST2A`, `AC1A`, `AC1A_RETRO`, `AC4A`, `AC8B`, `DC3A`, `IEEET5`, `EXPIC1`, `EXHQSC`, `ENTSOE_simp`, and many more with combinations of PSS and OEL models.

### Available Torque Controller Models

`1storder`, `constant`, `DEGOV1`, `hydro_generic1`, `thermal_generic1`, `HQRVC`, `HQRVM`, `HQRVN`, `HQRVW`, `hq_generic`, `hq_generic1`, `ENTSOE_simp`, `ENTSOE_simp_consensus`

## Injectors

An injector is a component connected to a single AC bus:

```
INJEC INJ_TYPE NAME BUS_NAME FP FQ P Q parameters_passed_to_INJ ;
```

### Available Injector Models

| Model | Description |
|-------|-------------|
| `load` | Generic load model |
| `PQ` | Constant PQ load |
| `restld` | Restorative load |
| `indmach1`, `indmach2` | Induction machine models |
| `IBG` | Inverter-based generator |
| `WT3WithChanges`, `WT4WithChanges` | Wind turbine models |
| `BESSWithChanges` | Battery energy storage system |
| `vfd_load` | Variable frequency drive load |
| `svc_hq_generic1` | SVC model |
| `theveq` | Thévenin equivalent (infinite bus) |

## Thévenin Equivalent (Infinite Bus)

```
INJEC THEVEQ INJEC_NAME BUS_NAME FP FQ P Q MVA ;
```

A Thévenin equivalent imposes a constant-frequency voltage source and forces the synchronous reference frame.

## Impedance Loads

```
IMPLOAD loadname BUS_NAME FP FQ P Q ;
```

Constant-impedance loads maintain the power factor at the initial voltage.

## Two-Port Components

Two-port components connect two buses:

### Available Two-Port Models

| Model | Description |
|-------|-------------|
| `HQSVC` | SVC model (Hydro-Quebec type) |
| `HVDC_LCC` | Line-commutated converter HVDC |
| `HVDC_VSC` | Voltage source converter HVDC |
| `HVDC_VSC_SC` | VSC-HVDC with short-circuit contribution |
| `DC_BHPM`, `DC_CHAAUT` | DC link models |
| `CSVGN5` | SVC variant |
| `CHENIER` | HVDC link (Chenier) |
| `DCL_WCL` | DC link model |
| `vsc_hq` | VSC model (Hydro-Quebec type) |

## Discrete Controllers

```
DCTL CTRL_TYPE CTLNAME parameters ;
```

### Available Discrete Controller Models

| Model | Description |
|-------|-------------|
| `ltc`, `ltc2`, `ltcinv` | Load tap changer controllers |
| `oltc2` | On-load tap changer |
| `uvls` | Under-voltage load shedding |
| `uvprot` | Under-voltage protection |
| `pst` | Phase-shifting transformer controller |
| `rt` | Real-time synchronizer |
| `mais`, `HQmais` | Multi-area islanding schemes |
| `FRT` | Fault ride-through |
| `sim_minmaxvolt` | Voltage stopping criteria |
| `sim_minmaxspeed` | Speed stopping criteria |
| `voltage_variability` | Voltage variability monitor |

### Real-Time Synchronizer

```
DCTL RT CTLNAME ratio_to_rt ;
```

Setting `ratio_to_rt = 1.0` slows the simulation to match real-time. Setting it to `2.0` means twice faster than real-time (if possible).

### Stopping Criteria

**Voltage-based**:
```
DCTL SIM_MINMAXVOLT CTRL_Name VMAX(pu) VMIN(pu) DEADTIME(s) Stop_Simulation(T/F) ;
```

**Speed-based**:
```
DCTL SIM_MINMAXSPEED CTRL_Name MAX_SPEED(pu) MIN_SPEED(pu) DEADTIME(s) Stop_Simulation(T/F) ;
```
