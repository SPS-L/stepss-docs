---
title: File Formats
description: Data file syntax and conventions used in STEPSS
---

Data files are organized into **records** and **comments**.

## Records

Each record includes:
- A leading **keyword** that identifies the information provided
- One or more **fields** (numeric or character)
- A **terminating semicolon** (`;`) that marks the end of the record

```
LINE A-B BUS_A BUS_B 3.0 30.0 150.0 1400.0 1 ;
```

Inside the record, the keyword, fields, and semicolon are separated by at least one space. Anything after the semicolon is ignored.

:::caution
Missing spaces between fields will cause parsing errors:
```
LINE A-B BUS_ABUS_B 3.0 30.0 150.0 1400.0 1 ;    ❌ Missing space
LINE A-B BUS_A BUS_B 3.030.0 150.0 1400.0 1 ;     ❌ Missing space
```
:::

A record may **span multiple lines**; the semicolon indicates the end:

```
INJEC GFOL VSC1 A 1.0 1.0 0.0 0.0 0.005 0.15 1.00 1044.0 0.005 0.15 33.3
 10.0 0.002 -999.0 10.0 0.1667 50.0 0.10  0.4  0.5  1.0  0.95  0.5 99.0 1 ;
```

### Numeric Fields

Numeric fields are written in free format, using floating-point notation. The exponent can be denoted by `E` or `D` (Fortran-style):

```
30   30.   30.0   3E01   3.E01   3.0E01   3.E1   3.e1
```

All of the above represent the same number.

### Character Fields

- Limited to **20 characters** (only first 20 are read)
- Some fields are limited to **8 characters** (e.g., bus names)
- Uppercase letters are significant (case-sensitive)
- If a field includes a **space** or **slash** (`/`), enclose it in quotes (`'` or `"`)
- The semicolon (`;`) **must not** be included in any character field

## Comments

There are three ways to insert comments:

1. **Exclamation mark** (`!`): A line starting with `!` is memorized and reproduced on output (up to 130 characters)
2. **Sharp** (`#`): A line starting with `#` is completely ignored — useful for field labels
3. **After semicolon**: Anything after the `;` terminator is ignored

```
# Example: using # comments to label fields
#           name bus FP  FQ  P   Q    SNOM  RS    LLS LSR   RR    LLR
INJEC INDMACH1  SM   2  0.2 0.2 0. 0. 0. 0.031 0.1 3.2 0.018 0.180
#              H   A   B   LF
               0.7 0.5 0.0 0.6 ;
```

Comments do not span multiple lines. Empty lines are ignored.

## Sharing Data Between Files

Records may be distributed over an **arbitrary number of data files**, read sequentially. The order of records inside files does not matter, and the order in which files are read does not matter either.

A typical organization:
- One file for network data
- One file for power flow data
- One file for dynamic component data
- One file for simulation control parameters

These files can be listed in any order in the command file.

## Next Steps

- [Network Modeling](/user-guide/network/) — Define buses, lines, transformers, and shunts
- [Power Flow (PFC)](/user-guide/pfc/) — Set up and run power flow computations
