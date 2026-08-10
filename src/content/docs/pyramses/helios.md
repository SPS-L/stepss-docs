---
title: Helios Power-Flow API
description: Running AC power flows from Python with pyramses.helios.HeliosSession
---

The `pyramses.helios` module wraps [Helios](/user-guide/power-flow/), the STEPSS AC power-flow engine. Pre-compiled libraries are bundled with the package for Windows, Linux, and macOS, so no separate installation is required.

Unlike the RAMSES classes (which follow the historical camelCase conventions), this module uses PEP 8 snake_case naming. Errors are raised as `pyramses.HeliosError`, carrying the engine's diagnostic message.

## Basic Workflow

`HeliosSession` follows a load → (modify) → solve → query lifecycle and works as a context manager:

```python
from pyramses.helios import HeliosSession

with HeliosSession() as pf:
    pf.load_file('network.dat')
    converged = pf.solve()

    v, angle = pf.get_bus_voltage('1041')     # one bus (pu, rad)
    p, q = pf.get_branch_flow('1042-1044')    # from-end flow (MW, Mvar)
```

Solve diagnostics are available after `solve()`: `pf.converged`, `pf.solver_status`, `pf.iterations`, and `pf.max_mismatch`.

## Solver Options

Options map to the `$PARAM` records of the data file and can be overridden after loading (loading overwrites them with the file's values, so set options *after* `load_file`):

```python
from pyramses.helios import Option

pf.load_file('network.dat')
pf.set_option(Option.TOLAC, 0.001)     # MW
pf.set_option(Option.MAX_ITER, 30)
pf.solve()
```

## Vectorized Results

Bulk getters return NumPy arrays indexed like the corresponding `*_names()` lists, with no text parsing needed:

```python
v_pu, angle_rad = pf.get_bus_voltages()
p_load, q_load = pf.get_bus_loads()
p_from, q_from, p_to, q_to = pf.get_branch_flows()
p_gen, q_gen, status = pf.get_generator_outputs()

names = pf.bus_names()
print(f"lowest voltage: {v_pu.min():.4f} pu at {names[v_pu.argmin()]}")
```

Per-element dataclasses are available via `get_bus_info()`, `get_branch_info()`, and `get_generator_info()`.

## Modifying the System

Modifications accumulate an active-power imbalance that `apply_changes()` settles: connectivity check, redispatch onto the remaining generators, and a re-solve (the same workflow as the interactive modify menu). `change_*` methods apply increments; `set_load()` sets absolute values:

```python
pf.trip_branch('1042-1044')
pf.change_load('1041', 50.0, 10.0)     # +50 MW, +10 Mvar
pf.set_generator_voltage('g6', 1.02)
pf.apply_changes()                     # redispatch + re-solve

pf.reset()                             # back to the state saved at load
```

## Contingency Screening

Run automatic N-1 over selected equipment classes, or a Fortran-format contingency file (`BT`/`GT`/`ST`/`HC` actions). Each result is a dataclass with convergence, acceptance, voltage/loading extremes, and violation strings; the base case is untouched afterwards:

```python
results = pf.run_contingencies(branches=True, generators=True,
                               v_min=0.95, v_max=1.05, overload=100.0)
for r in results:
    if not r.accepted:
        print(r.name, r.violations)

results = pf.run_contingencies(file='contingencies.txt')
```

## Exporting Results

```python
pf.write_dump('solved_case.dat')      # re-loadable data file
pf.write_voltrat('volt_rat.dat')      # LFRESV + TRANSFO records, RAMSES initial conditions
pf.write_matlab('system.m')           # operating point + Y-bus script
pf.write_diagram('template.svg', 'diagram.svg')
```

`volt_rat.dat` is the natural bridge to dynamic simulation: solve a power flow with Helios, export it, and pass it to a RAMSES case via `case.addData('volt_rat.dat')`.

:::note
`write_voltrat()` is the API form of the `VT` menu command, and writes the same
records. For what those records contain, and how they relate to the hand-written
`TRFO` style, see
[Exported Operating Point](/user-guide/power-flow/#bus-voltages-initial-values-and-results-lfresv).
:::

## Runnable Examples

Five self-contained scripts ship in the repository under [`examples/helios/`](https://github.com/SPS-L/stepss-pyramses/tree/master/examples/helios): basic solve, options and arrays, modify and re-solve, contingency screening, and exports.

## Further Reading

- [Power Flow user guide](/user-guide/power-flow/), data format, solver parameters, engine details
- Full method-level documentation: the docstrings on `HeliosSession`, e.g. `help(pyramses.HeliosSession)`
