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

Inside the record, the keyword, fields, and semicolon are separated by at least one space. Anything after the semicolon is ignored. The next record (or comment) starts with the next line.

:::caution
Missing spaces between fields will cause parsing errors:
```
LINE A-B BUS_ABUS_B 3.0 30.0 150.0 1400.0 1 ;    ❌ Missing space
LINE A-B BUS_A BUS_B 3.030.0 150.0 1400.0 1 ;     ❌ Missing space
```
:::

A record may **span multiple lines**; the semicolon indicates the end. Spanning over several lines is highly recommended for records that include many fields. Note that, depending on the text editor and its settings, a long record could appear truncated when displayed.

```
INJEC GFOL VSC1 A 1.0 1.0 0.0 0.0 0.005 0.15 1.00 1044.0 0.005 0.15 33.3
 10.0 0.002 -999.0 10.0 0.1667 50.0 0.10  0.4  0.5  1.0  0.95  0.5 99.0 1 ;
```

Some records have optional fields, which are always located at the end of the record.

### Numeric Fields

Numeric fields are written in free format: with or without a decimal point, with or without an exponent. The exponent can be denoted by `E` or `D`:

```
30   30.   30.0   3E01   3.E01   3.0E01   3.E1   3.e1
```

All of the above represent the same number.

### Character Fields

- Limited to **20 characters** (only first 20 are read; the rest is silently ignored without warning). It is discouraged to have more than 20 characters in a field
- Some fields are limited to **8 characters** (e.g., bus names); characters beyond 8 are ignored
- Uppercase letters are significant (case-sensitive)
- If a field includes a **space** or **slash** (`/`), enclose it in quotes (`'` or `"`). Between quotes, leading spaces are significant while trailing ones are ignored
- Keywords do not include spaces, so quoting them is unnecessary
- The semicolon (`;`) **must not** be included in any character field, even within quotes

## Comments

There are three ways to insert comments:

1. **Exclamation mark** (`!`): A line whose first non-blank character is `!` is memorized and reproduced on output (up to 130 characters after the `!`)
2. **Sharp** (`#`): A line whose first non-blank character is `#` is completely ignored — useful for field labels
3. **After semicolon**: Anything after the `;` terminator is ignored

```
# Example: using # comments to label fields
#           name bus FP  FQ  P   Q    SNOM  RS    LLS LSR   RR    LLR
INJEC INDMACH1  SM   2  0.2 0.2 0. 0. 0. 0.031 0.1 3.2 0.018 0.180
#              H   A   B   LF
               0.7 0.5 0.0 0.6 ;
```

Comments do not span multiple lines. If several lines are needed, each must start with `!` or `#`. Empty lines are ignored.

## Sharing Data Between Files

Records may be distributed over an **arbitrary number of data files**, read sequentially. The order of records inside files does not matter, and the order in which files are read does not matter either.

A typical organization:
- One file for network data
- One file for power flow data
- One file for dynamic component data
- One file for simulation control parameters

These files can be listed in any order in the command file. The second and third files, for instance, may be swapped in the list without any effect.

## Next Steps

- [Network Modeling](/user-guide/network/) — Define buses, lines, transformers, and shunts
- [Power Flow (PFC)](/user-guide/pfc/) — Set up and run power flow computations
