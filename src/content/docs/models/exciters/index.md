---
title: Exciter Models
description: Excitation system, stabilizer and limiter models available in RAMSES
---

RAMSES excitation models cover the IEEE Std 421.5-2016 excitation systems (and selected ENTSO-E variants) with their stabilizers and limiters, and a set of simpler and generic regulators. The IEEE models are written in the CODEGEN language and compiled into Fortran; the basic and generic ones are implemented directly in Fortran.

:::note[Usage in Dynamic Data Files]
Exciter models in RAMSES are defined as sub-records within a `SYNC_MACH` block using the `EXC` keyword, followed by the model name and its parameters. They are not standalone records. The `EXC` line appears after the machine parameters and before the `TOR` (torque/governor) line. The entire block ends with a single `;` after the `TOR` record.

```
SYNC_MACH name bus FP FQ P Q SNOM Pnom H D IBRATIO
                    XT  Xl  Xd  X'd  X"d  Xq  X'q  X"q  m  n  Ra  T'do  T"do  T'qo  T"qo
              EXC model_name  param1  param2  ...
              TOR model_name  param1  param2  ... ;
```

RAMSES adds the `exc_` prefix to the model name automatically, so both `AC1A` and `exc_AC1A` are accepted.

The **State** column of the [IEEE Model Variants](#ieee-model-variants) table says whether a model is compiled and callable, or only a DSL description:

- **Registered**, callable from a data file as it stands. Every compiled exciter has been registered since 3.79; before that, fifteen of them were mapped to no name and RAMSES rejected them in a data file.
- **DSL only**, present as a CODEGEN model description but not as compiled Fortran. `ENTSOE_lim` exists only as an example model description, to be compiled as a [user-defined model](/developer/user-models/); `AC8B_lim` is listed for reference only and is not distributed.

The [Model Reference index](/models/) carries the same information across all model families.
:::

## Model Families

The models are documented by family, one page each.

| Page | Models |
|------|--------|
| [IEEE AC and DC Exciters](/models/exciters/ieee-ac-dc/) | [`AC1A`](/models/exciters/ieee-ac-dc/#ac1a), [`AC4A`](/models/exciters/ieee-ac-dc/#ac4a), [`AC8B`](/models/exciters/ieee-ac-dc/#ac8b), [`DC3A`](/models/exciters/ieee-ac-dc/#dc3a) |
| [IEEE ST and Other Exciters](/models/exciters/ieee-st/) | [`ST1A`](/models/exciters/ieee-st/#st1a), [`ST2A`](/models/exciters/ieee-st/#st2a-via-expic1), [`IEEET5`](/models/exciters/ieee-st/#ieeet5), [`SEXS`](/models/exciters/ieee-st/#sexs), [`ENTSOE_simp`](/models/exciters/ieee-st/#entsoe_simp) |
| [Stabilizers and Limiters](/models/exciters/stabilizers-limiters/) | [`PSS2B`](/models/exciters/stabilizers-limiters/#pss2b-dual-input-stabilizer), [`PSS3B`](/models/exciters/stabilizers-limiters/#pss3b-two-input-second-order-filter-stabilizer), [`PSS4B`](/models/exciters/stabilizers-limiters/#pss4b-three-band-multi-input-stabilizer), [`IEEEST`](/models/exciters/stabilizers-limiters/#ieeest-single-input-stabilizer), [`STAB3`](/models/exciters/stabilizers-limiters/#stab3-power-input-stabilizer), [`MAXEX2`](/models/exciters/stabilizers-limiters/#maxex2-field-current-limiter-with-timer-and-hysteresis), [integral OEL](/models/exciters/stabilizers-limiters/#integral-oel-_lim-variants) |
| [Basic Exciters](/models/exciters/basic/) | [`CONSTANT`](/models/exciters/basic/#constant-exc_constant), [`1ST_ORDER`](/models/exciters/basic/#1st_order-exc_1storder), [`kundur`](/models/exciters/basic/#kundur-exc_kundur) |
| [Generic Exciters](/models/exciters/generic/) | [`GENERIC1`](/models/exciters/generic/#generic1-exc_generic1), [`AVR_DG`](/models/exciters/generic/#avr_dg-exc_avr_dg), [`GENERIC2`](/models/exciters/generic/#generic2-exc_generic2), [`GENERIC`](/models/exciters/generic/#generic-exc_generic) |

---

## IEEE Model Variants

| Model Name | State | Base Type | PSS | OEL / Limiter | IEEE Reference |
|---|---|---|---|---|---|
| `AC1A` | Registered | AC type 1 | | | IEEE 421.5 Type AC1A |
| `AC1A_MAXEX2` | Registered | AC type 1 | | MAXEX2 field current limiter | IEEE 421.5 Type AC1A |
| `AC1A_RETRO` | Registered | AC type 1 (retrofit) | PSS4B (internal) | | |
| `AC1A_RETRO_PSS4B` | Registered | AC type 1 (retrofit) | PSS4B | | |
| `AC4A` | Registered | AC type 4 | | | IEEE 421.5 Type AC4A |
| `AC8B` | Registered | AC type 8 | | | IEEE 421.5 Type AC8B |
| `AC8B_PSS3B_lim` | Registered | AC type 8 | PSS3B | Integral OEL + SCL | IEEE 421.5 Type AC8B |
| `AC8B_lim` | DSL only | AC type 8 | | Integral OEL + SCL | IEEE 421.5 Type AC8B |
| `DC3A` | Registered | DC type 3 | | | IEEE 421.5 Type DC3A |
| `ENTSOE_simp` | Registered | ENTSO-E simplified | IEEEST (internal) | | ENTSO-E |
| `ENTSOE_lim` | DSL only | ENTSO-E simplified | IEEEST (internal) | Integral OEL | ENTSO-E |
| `EXPIC1` | Registered | AC/ST (PIC type) | | | |
| `EXPIC1_PSS2B` | Registered | AC/ST (PIC type) | PSS2B | | |
| `EXPIC1_PSS2B_MAXEX2` | Registered | AC/ST (PIC type) | PSS2B | MAXEX2 | |
| `IEEET5` | Registered | DC type 5 | | | IEEE 421.5 Type DC5A (legacy) |
| `SEXS` | Registered | ST simplified | | | CIGRÉ simplified |
| `SEXS_IEEEST` | Registered | ST simplified | IEEEST | | CIGRÉ simplified |
| `SEXS_STAB3_lim` | Registered | ST simplified | STAB3 | Integral OEL | |
| `ST1A` | Registered | ST type 1 | | | IEEE 421.5 Type ST1A |
| `ST1A_IEEEST` | Registered | ST type 1 | IEEEST | | IEEE 421.5 Type ST1A |
| `ST1A_IEEEST_MAXEX2` | Registered | ST type 1 | IEEEST | MAXEX2 | IEEE 421.5 Type ST1A |
| `ST1A_PSS2B` | Registered | ST type 1 | PSS2B | | IEEE 421.5 Type ST1A |
| `ST1A_PSS2B_MAXEX2` | Registered | ST type 1 | PSS2B | MAXEX2 | IEEE 421.5 Type ST1A |
| `ST1A_PSS3B` | Registered | ST type 1 | PSS3B | | IEEE 421.5 Type ST1A |
| `ST1A_PSS4B` | Registered | ST type 1 | PSS4B | | IEEE 421.5 Type ST1A |
| `ST1A_PSS4B_MAXEX2` | Registered | ST type 1 | PSS4B | MAXEX2 | IEEE 421.5 Type ST1A |
| `ST1A_lim` | Registered | ST type 1 | | Integral OEL + SCL | IEEE 421.5 Type ST1A |
| `ST2A` | Registered | ST type 2 | | | IEEE 421.5 Type ST2A (via EXPIC1) |

A variant combines a base exciter with the stabilizer and limiter named in its row. The base types are on the two IEEE pages above, and the stabilizer and limiter blocks on [Stabilizers and Limiters](/models/exciters/stabilizers-limiters/).

## See Also

- [Model Reference](/models/), the full model catalogue
- [Dynamic Data Records](/user-guide/dynamic-models/), the `SYNC_MACH` record these models sit in
