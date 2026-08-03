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

For the complete mathematical model, per unit system, and detailed parameter descriptions, see the [Synchronous Machine Model](/models/synchronous-machine/) page.

### Available Exciter Models

RAMSES adds the `exc_` prefix to the model name automatically, so both `AC1A` and `exc_AC1A` are accepted.

Uppercase short names (no prefix): `CONSTANT`, `1ST_ORDER`, `GENERIC1`, `GENERIC2`.

Prefixed names (either form): `kundur` / `exc_kundur`, `ENTSOE_simp`, `ST1A`, `SEXS`, `SEXS_IEEEST`, `GENERIC3` / `exc_GENERIC3`, `GENERIC4` / `exc_GENERIC4`, `AC1A`, `AC4A`, `IEEET5`, `ST1A_IEEEST`, `ST1A_PSS4B`, `ST1A_PSS2B`, `EXPIC1_PSS2B`.

All names above are built into every RAMSES distribution (standalone executable and shared library used by PyRAMSES). Additional IEEE variants listed in the [IEEE Exciter Models](/models/ieee-exciters/) page (`AC1A_MAXEX2`, `AC1A_RETRO*`, `AC8B*`, `DC3A`, `EXPIC1`, `SEXS_STAB3_lim`, `ST1A_lim`, etc., and the `EXHQSC*` family) are not callable out of the box and require extending RAMSES through URAMSES.

For detailed documentation of each model, see the [Model Reference](/models/ieee-exciters/) section.

### Available Torque Controller Models

Uppercase short names (no prefix): `CONSTANT`, `1ST_ORDER`, `HYDRO_GENERIC1`, `THERMAL_GENERIC1`.

Prefixed names (either form, `tor_` is added automatically): `ENTSOE_simp` / `tor_ENTSOE_simp`, `HYGOV` / `tor_HYGOV`, `GAST` / `tor_GAST`, `TGOV1` / `tor_TGOV1` (internally `tor_TGOV1D`), `DEGOV1` / `tor_DEGOV1`.

All names above are built into every RAMSES distribution. Additional governors listed in the [Custom Governor Models](/models/custom-governors/) page (`tor_gasturbm`, `tor_govclasm`, `tor_govhydr`, `tor_govnuc`) are not callable out of the box and require extending RAMSES through URAMSES.

For detailed documentation of each model, see the [Model Reference](/models/ieee-exciters/) section.

## Injectors

An injector is a component connected to a single AC bus:

```
INJEC INJ_TYPE NAME BUS_NAME FP FQ P Q parameters_passed_to_INJ ;
```

### Available Injector Models

Uppercase short names take no prefix; the prefixed names accept either `inj_` or no prefix (RAMSES adds it automatically).

| Data-file name | Equivalent | Description |
|----------------|-----------|-------------|
| `LOAD` | | Generic exponential-recovery load |
| `RESTLD` | | Restorative load |
| `INDMACH1`, `INDMACH2` | | Single-cage / double-cage induction machines |
| `SVC_GENERIC1` | | Generic SVC model |
| `THEVEQ` | | Thévenin equivalent (infinite bus) |
| `PQ` | `inj_PQ` | Constant PQ load |
| `IBG` | `inj_IBG` | Generic inverter-based generator |
| `WT3` | `inj_WT3` | Type 3 wind turbine |
| `WT4` | `inj_WT4` | Type 4 wind turbine |
| `BESS` | `inj_BESS` | Battery energy storage |
| `GFOL` | `inj_GFOL` | Grid-following converter |
| `GFOR` | `inj_GFOR` | Grid-forming converter |
| `vfd_load` | `inj_vfd_load` | Variable-frequency-drive load |
| `VFAULT` | `inj_VFAULT` | Internal voltage-fault injector (auto-added by RAMSES) |

All injectors listed in the table above are compiled into every RAMSES build. Additional injector variants documented in the [Injector Models](/models/custom-injectors/) page (`inj_INDM1`, `inj_norton`, `inj_PVG`) are not callable out of the box and require extending RAMSES through URAMSES.

## Thévenin Equivalent (Infinite Bus)

```
INJEC THEVEQ INJEC_NAME BUS_NAME FP FQ P Q MVA ;
```

A Thévenin equivalent imposes a constant-frequency voltage source and forces the synchronous reference frame.

| Parameter | Description | Unit |
|-----------|-------------|------|
| `FP`, `FQ` | Fractions of bus injection (active, reactive) | |
| `P`, `Q` | Initial powers (used if fractions are zero) | pu |
| `MVA` | Apparent power base used for per-unit values of the Thévenin equivalent | MVA |

The FP, FQ, P, Q fields are power participation fractions and initial power values used during initialization. See [Reference Frames & Initialization](/user-guide/reference-frames/) for detailed explanation.

## Impedance Loads

```
IMPLOAD loadname BUS_NAME FP FQ P Q ;
```

Constant-impedance loads maintain the power factor at the initial voltage.

| Parameter | Description | Unit |
|-----------|-------------|------|
| `FP`, `FQ` | Fractions of bus injection (active, reactive) | |
| `P`, `Q` | Initial powers (used if fractions are zero) | pu |

The FP, FQ, P, Q fields are power participation fractions and initial power values used during initialization. See [Reference Frames & Initialization](/user-guide/reference-frames/) for detailed explanation.

## Two-Port Components

Two-port components connect two buses:

### Available Two-Port Models

RAMSES adds the `twop_` prefix to the model name automatically, so both `HVDC_LCC` and `twop_HVDC_LCC` are accepted.

| Data-file name | Equivalent | Description |
|----------------|-----------|-------------|
| `HVDC_LCC` | `twop_HVDC_LCC` | Line-commutated converter HVDC |
| `HVDC_VSC_SC` | `twop_HVDC_VSC_SC` | Self-commutating (grid-forming) VSC-HVDC |
| `DCL_WCL` | `twop_DCL_WCL` | DC link with wind-converter link (offshore wind HVDC) |

The three models above are built into every RAMSES distribution. Other two-port models documented in the [Two-Port Models](/models/two-port-models/) page (`twop_HVDC_VSC` and the Hydro-Québec family `twop_CHENIER`, `twop_CSVGN5`, `twop_HQSVC`, `twop_DC_BHPM`, `twop_DC_CHAAUT`, `twop_DC_CHTFWX`, `twop_DC_LVCL_1`) are not callable out of the box and require extending RAMSES through URAMSES.

For detailed documentation of each model, see the [Model Reference](/models/ieee-exciters/) section.

### Data Format

User-defined two-port models use a `TWOP` record:

```
TWOP MODEL_NAME TWOP_NAME BUS1 BUS2 IND FP1 FQ1 P1 Q1 FP2 FQ2 P2 Q2 DATA1 DATA2 ... ;
```

For details on each field, see [User-Defined Models, TWOP Record](/developer/user-models/#twop-record-user-defined-two-ports).

## Discrete Controllers

```
DCTL CTRL_TYPE CTLNAME parameters ;
```

### Available Discrete Controller Models

The following discrete-controller names are built into every RAMSES distribution (use them uppercase, with no `dctl_` prefix):

| Model | Description |
|-------|-------------|
| `LTC`, `LTC2`, `LTCINV` | Load tap changer controllers |
| `OLTC2` | On-load tap changer |
| `UVLS` | Under-voltage load shedding |
| `UVPROT` | Under-voltage protection |
| `PST` | Phase-shifting transformer controller |
| `RT` | Real-time synchronizer |
| `MAIS` | Multi-area islanding scheme |
| `FRT` | Fault ride-through |
| `SIM_MINMAXVOLT` | Voltage stopping criteria |
| `SIM_MINMAXSPEED` | Speed stopping criteria |
| `VOLT_VAR` | Voltage variability monitor |
| `line_prot` | Line overcurrent protection (`dctl_line_prot` also accepted) |

### Load Tap Changer (LTC)

```
DCTL LTC CTLNAME TRFONAME BUS_NAME DIR NMIN NMAX NBPOS TOL DELAY1 DELAY2 ;
```

| Field | Description |
|-------|-------------|
| `CTLNAME` | Name of the controller |
| `TRFONAME` | Name of the controlled transformer |
| `BUS_NAME` | Name of the controlled bus |
| `DIR` | Direction of tap change |
| `NMIN` | Minimum tap ratio (% of nominal, e.g. `85.`) |
| `NMAX` | Maximum tap ratio (% of nominal, e.g. `115.`) |
| `NBPOS` | Number of tap positions |
| `TOL` | Voltage tolerance |
| `DELAY1` | First delay (initial action) |
| `DELAY2` | Subsequent delay (between steps) |

### Real-Time Synchronizer

```
DCTL RT CTLNAME ratio_to_rt ;
```

Setting `ratio_to_rt = 1.0` synchronizes the simulation with real-time: the simulation is slowed down when it runs faster than real-time, but nothing is done when it is slower. Setting it to `2.0` means twice faster than real-time (if possible).

### Stopping Criteria

**Voltage-based**:
```
DCTL SIM_MINMAXVOLT CTRL_Name VMAX(pu) VMIN(pu) DEADTIME(s) Stop_Simulation(T/F) ;
```

**Speed-based**:
```
DCTL SIM_MINMAXSPEED CTRL_Name MAX_SPEED(pu) MIN_SPEED(pu) DEADTIME(s) Stop_Simulation(T/F) ;
```

## Next Steps

- [Disturbances](/user-guide/disturbances/), Define faults, trips, and parameter changes
- [Solver Settings](/user-guide/solver-settings/), Configure the numerical solver
- [Model Reference](/models/ieee-exciters/), Browse available exciter, governor, and injector models
