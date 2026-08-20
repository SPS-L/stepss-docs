---
title: Model Reference
description: Catalogue of every model RAMSES can load, and where each is documented
---

This is the catalogue of models RAMSES can load. Each family has its own page with
equations, parameters in declaration order, and worked examples. For the record
syntax that references these models, see
[Dynamic Data Records](/user-guide/dynamic-models/).

## How a Model Name Resolves

RAMSES adds the family prefix (`exc_`, `tor_`, `inj_`, `twop_`) automatically, so
`AC1A` and `exc_AC1A` are the same model. Names are **case sensitive**.

A model can be in one of three states, and the tables below say which:

| State | Meaning |
|-------|---------|
| **Built in** | Handled directly by the family dispatcher, no prefix |
| **Registered** | Compiled and mapped to a name, callable from a data file |
| **Not compiled** | Present as source but excluded from the build, so not reachable at all |

:::note[Every compiled model is reachable]
As of 3.79 every model compiled into the library is mapped to a name and can be
loaded by writing that name in a data file. Before 3.79 twenty-four of them
shipped under no name and could only be reached by adding a case through
[URAMSES](/developer/uramses/). The Hydro-Québec families (`models/*/hq/`) and
`inj_norton` are excluded from the build entirely and are not reachable by any
route.
:::

## Exciters

[IEEE Exciters](/models/ieee-exciters/) and [Custom Exciters](/models/custom-exciters/)

| Data-file name | State | Documented on |
|----------------|-------|---------------|
| `CONSTANT`, `1ST_ORDER` | Built in | [Custom Exciters](/models/custom-exciters/) |
| `GENERIC1`, `GENERIC2` | Built in | [Custom Exciters](/models/custom-exciters/) |
| `GENERIC` | Registered, since 3.57 | [Custom Exciters](/models/custom-exciters/) |
| `kundur` | Registered | [Custom Exciters](/models/custom-exciters/) |
| `AVR_DG` | Registered, since 3.76 | [Custom Exciters](/models/custom-exciters/) |
| `AC1A`, `AC4A`, `IEEET5` | Registered | [IEEE Exciters](/models/ieee-exciters/) |
| `ST1A`, `ST1A_IEEEST`, `ST1A_PSS2B`, `ST1A_PSS4B` | Registered | [IEEE Exciters](/models/ieee-exciters/) |
| `SEXS`, `SEXS_IEEEST` | Registered | [IEEE Exciters](/models/ieee-exciters/) |
| `EXPIC1_PSS2B` | Registered | [IEEE Exciters](/models/ieee-exciters/) |
| `ENTSOE_simp` | Registered | [IEEE Exciters](/models/ieee-exciters/) |
| `AC1A_MAXEX2`, `AC1A_RETRO`, `AC1A_RETRO_PSS4B`, `AC8B`, `AC8B_PSS3B_lim`, `DC3A`, `EXPIC1`, `EXPIC1_PSS2B_MAXEX2`, `SEXS_STAB3_lim`, `ST1A_IEEEST_MAXEX2`, `ST1A_lim`, `ST1A_PSS2B_MAXEX2`, `ST1A_PSS3B`, `ST1A_PSS4B_MAXEX2`, `ST2A` | Registered, since 3.79 | [IEEE Exciters](/models/ieee-exciters/) |

## Governors

[IEEE Governors](/models/ieee-governors/) and [Custom Governors](/models/custom-governors/)

| Data-file name | State | Documented on |
|----------------|-------|---------------|
| `CONSTANT`, `1ST_ORDER` | Built in | [Custom Governors](/models/custom-governors/) |
| `HYDRO_GENERIC1`, `THERMAL_GENERIC1` | Built in | [Custom Governors](/models/custom-governors/) |
| `HYDRO_DG` | Registered, since 3.76 | [Custom Governors](/models/custom-governors/) |
| `DEGOV1`, `ENTSOE_simp` | Registered, since 3.40 | [IEEE Governors](/models/ieee-governors/) |
| `GAST`, `TGOV1`, `HYGOV` | Registered, since 3.50 | [IEEE Governors](/models/ieee-governors/) |
| `GASTURBM`, `GOVCLASM`, `GOVHYDR`, `GOVNUC` | Built in, since 3.79 | [Custom Governors](/models/custom-governors/) |

## Injectors

[Injector Models](/models/custom-injectors/)

| Data-file name | State |
|----------------|-------|
| `LOAD`, `RESTLD` | Built in |
| `INDMACH1`, `INDMACH2` | Built in |
| `SVC_GENERIC1` | Built in |
| `THEVEQ` | Built in |
| `PQ`, `IBG` | Registered |
| `WT3`, `WT4` | Registered |
| `BESS`, `GFOL`, `GFOR` | Registered |
| `vfd_load`, `PMU` | Registered |
| `VFAULT` | Registered, added automatically by RAMSES |
| `INDM1`, `PV` | Registered, since 3.79 |
| `inj_norton` | Excluded from the build |

## Two-Port Models

[Two-Port Models](/models/two-port-models/)

| Data-file name | State |
|----------------|-------|
| `HVDC_LCC` | Registered |
| `HVDC_VSC_SC` | Registered |
| `DCL_WCL` | Registered |
| `HVDC_VSC` | Registered, since 3.79 |

## Discrete Controllers

[Discrete Controller Models](/models/discrete-controllers/)

Discrete controllers take no prefix in the data file, though the dispatcher
prepends `dctl_` internally.

| Data-file name | State |
|----------------|-------|
| `LTC`, `LTC2`, `LTCINV`, `OLTC2` | Built in |
| `PST` | Built in |
| `UVLS`, `UVPROT`, `FRT` | Built in |
| `MAIS` | Built in |
| `RT` | Built in |
| `SIM_MINMAXVOLT`, `SIM_MINMAXSPEED` | Built in |
| `VOLT_VAR` | Built in |
| `line_prot` | Registered as `dctl_line_prot` |

## The Synchronous Machine

The machine itself is not selected by name; every `SYNC_MACH` record uses the same
model, parameterised by the record's own fields.

- [Synchronous Machine Model](/models/synchronous-machine/), equations and parameters
- [Parameter Conversion](/models/synchronous-machine-param-conversion/), converting between the XT and RL forms

## Next Steps

- [Dynamic Data Records](/user-guide/dynamic-models/), the record syntax that references these models
- [User-Defined Models](/developer/user-models/), write and register a model of your own
