---
title: Injector Models
description: Load, machine, renewable generation, and BESS injector models in RAMSES
---

RAMSES injector models represent loads, induction machines, inverter-based resources (IBR), and battery energy storage systems (BESS) connected to network buses.

:::note[Usage in Dynamic Data Files]
Injector models are defined with the `INJEC` keyword as standalone records in the dynamic data file. The syntax is:

```
INJEC model_name inj_name bus FP FQ P Q param1 param2 ... ;
```

Where `model_name` is the model identifier, `inj_name` is a unique instance name, `bus` is the connection bus, `FP`/`FQ` are participation factors, and `P`/`Q` are initial values in MW/Mvar (one of each pair must be zero, either the fraction or the absolute power).

Recognised injector model names (case-sensitive):

- **Uppercase short names** (no prefix): `LOAD`, `RESTLD`, `THEVEQ`, `INDMACH1`, `INDMACH2`, `SVC_GENERIC1`.
- **Prefixed names**: RAMSES adds the `inj_` prefix automatically: `VFAULT`/`inj_VFAULT`, `vfd_load`/`inj_vfd_load`, `PQ`/`inj_PQ`, `IBG`/`inj_IBG`, `WT3`/`inj_WT3`, `WT4`/`inj_WT4`, `BESS`/`inj_BESS`, `GFOL`/`inj_GFOL`, `GFOR`/`inj_GFOR`, `PMU`/`inj_PMU`.

All of the above are built into every RAMSES distribution (standalone executable and shared library used by stepss). `INDM1` and `PV` have been callable since 3.79; before that they were compiled under no name. `inj_norton` is excluded from the build entirely and is not available: it calls a Python bridge (`initialize_model_instance`, `call_python_evaluate`) that is not part of this source tree.

**Note on case sensitivity.** Match the case used above exactly. The uppercase short names must be uppercase. For the prefixed family, `vfd_load` and `VFAULT` use those exact cases. Most others follow the convention `inj_<UPPERCASE>` (e.g. `inj_PQ`, `inj_GFOR`).
:::

## Model Families

The models are documented by family, one page each. Which names are built in or registered, and since which release, is stated once, on the [Model Index](/models/#injectors).

| Page | Models |
|------|--------|
| [Loads and Equivalents](/models/injectors/loads/) | [`LOAD`](/models/injectors/loads/#load-inj_load-exponential-recovery-load), [`vfd_load`](/models/injectors/loads/#vfd_load-inj_vfd_load-variable-frequency-drive-load), [`RESTLD`](/models/injectors/loads/#restld-inj_restld-restorative-load), [`PQ`](/models/injectors/loads/#pq-inj_pq-constant-pq-load), [`THEVEQ`](/models/injectors/loads/#theveq-inj_theveq-thévenin-equivalent) |
| [Induction Machines](/models/injectors/induction-machines/) | [`INDMACH1`](/models/injectors/induction-machines/#indmach1-inj_indmach1-single-cage-induction-machine), [`INDMACH2`](/models/injectors/induction-machines/#indmach2-inj_indmach2-double-cage-induction-machine), [`INDM1`](/models/injectors/induction-machines/#indm1-inj_indm1-alternative-induction-machine) |
| [WECC Wind and Storage](/models/injectors/wecc/) | [`WT3`](/models/injectors/wecc/#wt3-inj_wt3-type-3-wind-turbine-dfig), [`WT4`](/models/injectors/wecc/#wt4-inj_wt4-type-4-wind-turbine-full-converter), [`BESS`](/models/injectors/wecc/#bess-inj_bess-battery-energy-storage-system) |
| [Converter Models](/models/injectors/converters/) | [`IBG`](/models/injectors/converters/#ibg-inj_ibg-inverter-based-generator-generic-ibr), [`PV`](/models/injectors/converters/#pv-inj_pv-photovoltaic-generator), [`GFOR`](/models/injectors/converters/#gfor-inj_gfor-grid-forming-converter-vsm), [`GFOL`](/models/injectors/converters/#gfol-inj_gfol-grid-following-converter) |
| [Compensation and Measurement](/models/injectors/compensation-measurement/) | [`SVC_GENERIC1`](/models/injectors/compensation-measurement/#svc_generic1-inj_svc_generic1-generic-static-var-compensator), [`PMU`](/models/injectors/compensation-measurement/#pmu-inj_pmu-phasor-measurement-unit) |
