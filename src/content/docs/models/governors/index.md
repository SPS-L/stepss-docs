---
title: Governor Models
description: Turbine and speed-governor models available in RAMSES
---

RAMSES turbine-governor (torque) models cover the IEEE-standard diesel, gas, steam and hydro governors, a set of basic and generic ones, and four plant-specific models.

:::note[Usage in Dynamic Data Files]
Governor/torque models in RAMSES are defined as sub-records within a `SYNC_MACH` block using the `TOR` keyword, followed by the model name and its parameters. They are not standalone records. The `TOR` line appears after the `EXC` (exciter) line, and the `;` at the end closes the entire `SYNC_MACH` block.

```
SYNC_MACH name bus FP FQ P Q SNOM Pnom H D IBRATIO
                    XT  Xl  Xd  X'd  X"d  Xq  X'q  X"q  m  n  Ra  T'do  T"do  T'qo  T"qo
              EXC model_name  param1  param2  ...
              TOR model_name  param1  param2  ... ;
```

RAMSES adds the `tor_` prefix to the model name automatically, so both `DEGOV1` and `tor_DEGOV1` resolve to the same model. The built-in governors (`CONSTANT`, `1ST_ORDER`, `HYDRO_GENERIC1`, `THERMAL_GENERIC1`) take no prefix and are written in uppercase.
:::

## Model Families

The models are documented by family, one page each. Which names are built in or registered, and since which release, is stated once, on the [Model Index](/models/#governors).

| Page | Models |
|------|--------|
| [IEEE Governors](/models/governors/ieee/) | [`DEGOV1`](/models/governors/ieee/#degov1-tor_degov1), [`ENTSOE_simp`](/models/governors/ieee/#entsoe_simp-tor_entsoe_simp), [`GAST`](/models/governors/ieee/#gast-tor_gast), [`TGOV1`](/models/governors/ieee/#tgov1-tor_tgov1d), [`HYGOV`](/models/governors/ieee/#hygov-tor_hygov) |
| [Basic and Generic Governors](/models/governors/generic/) | [`CONSTANT`](/models/governors/generic/#constant-tor_constant), [`1ST_ORDER`](/models/governors/generic/#1st_order-tor_1storder), [`THERMAL_GENERIC1`](/models/governors/generic/#thermal_generic1-tor_thermal_generic1), [`HYDRO_GENERIC1`](/models/governors/generic/#hydro_generic1-tor_hydro_generic1), [`HYDRO_DG`](/models/governors/generic/#hydro_dg-tor_hydro_dg) |
| [Plant Governors](/models/governors/plant/) | [`GASTURBM`](/models/governors/plant/#tor_gasturbm), [`GOVCLASM`](/models/governors/plant/#tor_govclasm), [`GOVHYDR`](/models/governors/plant/#tor_govhydr), [`GOVNUC`](/models/governors/plant/#tor_govnuc) |

## See Also

- [Model Reference](/models/), the full model catalogue
- [Dynamic Data Records](/user-guide/dynamic-models/), the `SYNC_MACH` record these models sit in
