---
title: File Formats
description: Data file syntax and conventions used in STEPSS
---

Data files are organized into **records** and **comments**. The
[observables file](#observables-file) is the one file a case needs that is
neither: it is described at the end of this page.

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
INJEC GFOL VSC1 A 1.0 1.0 0.0 0.0 0.005 0.15 1.02 1200.0 0.005 0.15 0.573 6.0
 0.0033 0.0333 10.0 0.002 -999.0 10.0 0.1667 50.0 0.10 0.4 0.5 1.0 -1000. -2000. 1.001 1 ;
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
2. **Sharp** (`#`): A line whose first non-blank character is `#` is completely ignored, useful for field labels
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

## Observables File

The observables file is not a data file. It carries no records, none of the
keywords above and no semicolons: it is a plain list, one request per line,
naming the equipment whose variables the trajectory file is to contain. STEPSS
GUI takes it on the [Observables tab](/gui/interface/#recording-to-file), where
it is required whenever a trajectory is saved.

Each line is a type and a name:

```
SYNC g1
```

The name is the equipment's own, read into 20 characters and case-sensitive; a
longer one is truncated silently. A `*` in place of a name selects every
component of that type.

### Types

| Keyword | Selects | Recorded per component |
|---|---|---|
| `BUS` | buses | 2: voltage magnitude (pu), phase angle (deg) |
| `SHUNT` | shunts | 1: reactive power produced (Mvar) |
| `IMPLOAD` | impedance loads | 2: active (MW) and reactive (Mvar) power consumed |
| `BRANCH` | lines and transformers | 6: P and Q entering at each end (MW, Mvar), then transformer ratio magnitude and its angle (deg) |
| `SYNC` | synchronous machines | 15, plus whatever the machine's exciter and torque models publish |
| `INJEC` | injectors | whatever the injector model publishes |
| `TWOP` | two-port injectors | whatever the two-port model publishes |
| `DCTL` | discrete controllers | whatever the controller publishes |

A keyword is read all-uppercase or all-lowercase, so `Bus` is neither and is
rejected. Dynamic loads are injectors and belong under `INJEC`; `IMPLOAD` is
for the impedance loads alone.

DYNGRAPH lists three of these categories under other names: `IMPLOAD` appears
as `LOAD`, `INJEC` as `INJ` and `TWOP` as `LINK`. Those spellings belong to the
listing, not to this file.

:::caution
An unknown keyword, and a name matching no equipment in the case, are both
skipped with a warning rather than refused. The run then finishes normally with
fewer curves in the trajectory than were asked for, so a missing curve is worth
looking for in the log before it is blamed on the simulation.
:::

### Coordinates

Two of the types take a three-letter suffix on the keyword, choosing what the
recorded numbers mean:

| Written | Records |
|---|---|
| `BUS-POL`, or plain `BUS` | voltage as magnitude and angle |
| `BUS-REC` | voltage as real and imaginary parts (pu) |
| `BRANCH-POW`, or plain `BRANCH` | flows as P and Q |
| `BRANCH-CUR` | the current at each end, as real and imaginary parts (pu) |

The suffix does not change how many values are recorded, only what they are.

:::caution
`BUS-REC *` does not do what it reads like. The wildcard sets polar coordinates
outright and never looks at the suffix, so rectangular coordinates have to be
asked for one bus at a time. `BRANCH-CUR *` has no such problem and is honoured.
:::

### Comments and an example

A line whose first non-blank character is `#` or `!` is ignored, as is an empty
line.

```
# what to record from the Kundur two-area run
SYNC    g1
SYNC    g2
BUS     b7
BUS-REC b9
BRANCH  *
```

At least one request has to be accepted. A file where none is leaves the
trajectory without a header, and nothing is recorded.

## Scenario File (`.cfg`)

A scenario file records **which files a case is made of**, not what is in them.
STEPSS GUI writes one with **File > Save configuration** and reads it back with
**Load configuration**, so a case set up once reopens in two clicks. It is a
plain text file and is meant to be writable by hand or by a script.

It carries exactly what the two engines are told to read: the ten system data
rows, the disturbance file, the one-line diagram, the observables file, the
three run-time observable rows, and the four recording checkboxes. Nothing
else, and what is left out is left out on purpose; see [What the file
deliberately does not carry](#what-the-file-deliberately-does-not-carry).

### Syntax

`key = value`, one per line, UTF-8, with `#` starting a comment line. Blank
lines are ignored. A key that appears twice keeps the last value.

Values are read with Java's properties parser, so a hand-written file has three
rules to respect:

- `=` and `:` both separate a key from its value. A key containing either must
  escape it; no key defined below does.
- `#` and `!` start a comment only at the beginning of a line.
- A backslash escapes: write `\\` for a literal backslash, and `\t`, `\n`,
  `\r`, `\f` for the control characters. A **leading** space in a value must
  be written `\ `; spaces anywhere else are literal, which is why
  `runtime.1.type = Bus Voltage` needs no quoting.

Windows paths are the case that bites: write `C:/cases/lf.dat` or
`C:\\cases\\lf.dat`, never `C:\cases\lf.dat`.

### Keys

**`stepss.format` is the only mandatory key.** Without it the file is refused
outright, and no other key in it is read. Every other key is optional *to the
loader*: an absent key means an empty field or a cleared tick, and the load
still succeeds. Whether the scenario that comes back can be **run** is a
separate question, answered under [What a runnable scenario
needs](#what-a-runnable-scenario-needs).

| Key | Required | Value |
|---|---|---|
| `stepss.format` | **Yes** | Format number. **`1`** today |
| `data.1` … `data.10` | To run | The ten system data rows, in order. Empty rows are not written |
| `disturbance` | To simulate | The disturbance `.dst` |
| `observables.file` | If recording | The [observables file](#observables-file) |
| `diagram` | No | The annotated one-line diagram SVG |
| `runtime.1.type` … `runtime.3.type` | No | Run-time plot row: the observable type, **by its label** (see below) |
| `runtime.1.name` … `runtime.3.name` | No | Run-time plot row: the bus, machine, branch or injector name |
| `record.trajectory` | No | `true` to write the output trajectory (`output.trj`) |
| `record.continuous` | No | `true` to write the continuous trace (`cont.trace`) |
| `record.discrete` | No | `true` to write the discrete trace (`disc.trace`) |
| `record.init` | No | `true` to write the initialisation trace (`init.trace`) |

The four `record.*` keys default to `false`, so a file that omits them loads
with all four ticks cleared and the run writes nothing but its log. The three
`runtime.N` rows default to empty, which is a row that plots nothing; a type
with no name, or a name with no type, is an incomplete row rather than an
error, and it is simply not plotted.

Booleans are `true` or `false`. Anything else is reported and the field is left
at its default.

`runtime.N.type` stores the **label** shown in the dropdown, not a code: one of
`Bus Voltage`, `Machine Speed`, `Omega-delta of machine`, `Active power-delta
of machine`, `Center of Inertia`, `Wall Time`, `Injector solutions`,
`Latency`, `Branch Active Power Origin`, `Branch Active Power
Extremity`, `Branch Reactive Power Origin`, `Branch Reactive Power Extremity`,
`Injector Observable`, `Two-port injector Observable`. A label this build does
not know is reported and that row is left empty.

### What a runnable scenario needs

Loading is tolerant; running is not. These are checked when you press **Run**,
not when the file is loaded, so a `.cfg` missing one of them loads without a
word and then refuses to start:

- **At least one `data.N`.** Both the dynamic simulation and the power flow
  refuse a case with no system data at all.
- **`disturbance`, to simulate.** A dynamic run needs one; a power flow does
  not. The `.dst` must also end in a `STOP` record, which is checked when the
  run starts rather than when the path is set, because the file can be edited
  in between.
- **`observables.file`, whenever `record.trajectory` is `true`.** The
  trajectory needs something to say which quantities it should contain. Setting
  `record.trajectory = true` with no observables file is the one combination
  that is refused outright.

`diagram` is needed only by the power flow's one-line diagram output, and only
when it is set; an unreadable template stops that run, an absent one does not.

### What the file deliberately does not carry

A scenario records **which files a case is made of**, and nothing about the
session it was saved in. Absent by design, not by omission:

- **The Analysis tab's small-signal parameters**, the working directory and the
  window geometry. A run does not depend on them.
- **Show observable dialog**, and the eight picker lists behind it. The lists
  are session state that no `.cfg` has ever carried, so saving the tick alone
  restored a choice whose other half was gone: the tab came back ticked over
  eight empty lists. The tick is left exactly as you set it when a
  configuration is loaded.

Two key names retired with that last change. A file saved by STEPSS 3.81 or
earlier may carry them, and both now get one sentence in the load report and
are otherwise ignored:

| Retired key | What happened to it |
|---|---|
| `record.dump` | Renamed `record.init`, matching the `init.trace` it writes |
| `observables.wizard` | Dropped; see above |

Nothing else about such a file is affected, and re-saving the scenario writes
it without them.

### Paths

**A path inside the `.cfg`'s own folder is stored relative to it, with forward
slashes on every platform.** Anything outside that folder is stored absolute.
Relative paths are resolved against the `.cfg`'s directory, never against the
working directory, and never leave the file: everything downstream of a load
sees an absolute path.

That rule is what makes a case folder portable. Keep the `.cfg` beside the data
it names and the whole folder can be moved, copied or sent to a colleague. A
path that would need `..` to express is stored absolute instead, so a file
outside the folder is never silently repointed at a different one after a move.

### Example

A Kundur two-area case, saved beside its data:

```ini
# STEPSS scenario. Save configuration wrote this; Load configuration reads it.
# Paths inside this file's own directory are stored relative to it, so the
# folder can be moved or copied whole. Everything else is absolute.
# Saved by STEPSS 3.81

stepss.format = 1

# System data
data.1 = lf.dat
data.2 = dyn.dat
data.3 = solveroptions.dat
disturbance = disturb.dst
diagram = kundur.svg

# Observables
observables.file = obs.dat
runtime.1.type = Bus Voltage
runtime.1.name = 9
runtime.2.type = Machine Speed
runtime.2.name = G1
runtime.3.type = 
runtime.3.name = 

# Recording
record.trajectory = true
record.continuous = false
record.discrete = false
record.init = false
```

The section comments and the blank lines are for the reader. Nothing depends on
them and a file without them loads identically.

### What a loader should do with a bad file

Loading is deliberately tolerant, and a hand-written file benefits from the same
rule: **apply every key you understand and report the rest**, rather than
refusing the file over one bad line. A key nobody knows, a boolean that is not
a boolean, an observable label that has been retired, a file that has since been
deleted: each is one sentence to the user, and the rest of the scenario still
loads.

Only three things are fatal, and all three are about the format number:

| `stepss.format` | Outcome |
|---|---|
| Absent | Refused, as not being a scenario file |
| Not a number | Refused, as not being a scenario file |
| Higher than this build reads | Refused, naming the version needed |

## Next Steps

- [Network Modeling](/user-guide/network/), Define buses, lines, transformers, and shunts
- [Power Flow](/user-guide/power-flow/), Set up and run power flow computations
