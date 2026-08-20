---
title: API Reference
description: stepss Python API, complete reference for stepss.cfg, stepss.sim, and stepss.extractor
---

## `stepss.cfg`: Test Case Configuration

The `stepss.cfg` class defines a simulation scenario: data files, disturbance file, output files, observables, and runtime options.

---

### Initializing

Create an empty configuration or load one from a previously saved command file:

```python
import stepss

case = stepss.cfg()             # empty configuration
case = stepss.cfg("cmd.txt")    # load from command file
```

Load multiple cases in a loop:

```python
import stepss

list_of_cases = []
for i in range(12):
    list_of_cases.append(stepss.cfg('cmd' + str(i) + '.txt'))
```

#### `writeCmdFile(filename=None)`

Save the current configuration to a command file. Useful for reproducing a run later. When called without an argument, it returns the command-file content as a string instead of writing a file.

```python
case.writeCmdFile('cmd.txt')
```

Save multiple cases in a loop:

```python
for i in range(12):
    list_of_cases[i].writeCmdFile('cmd' + str(i) + '.txt')
```

---

### Data Files

Data files describe the network topology, dynamic models, and solver settings. At least one must be provided.

#### `addData(filename)`

Add a data file to the case.

```python
case.addData('dyn_A.dat')
case.addData('settings1.dat')
```

#### `delData(filename)`

Remove a specific data file from the case.

```python
case.delData('dyn_A.dat')
```

#### `getData()`

Return the list of currently registered data files.

```python
files = case.getData()
```

#### `clearData()`

Remove all data files from the case.

```python
case.clearData()
```

:::caution
At least one data file must be provided, otherwise the simulator will raise an exception.
:::

---

### Initialization File

Specifies where the simulator writes initialization procedure output.

#### `addInit(filename)`

```python
case.addInit('init.trace')
```

#### `getInit()`

Return the currently registered initialization file path.

```python
path = case.getInit()
```

:::note
This is optional. If omitted, the simulator skips writing initialization output.
:::

---

### Disturbance File

Describes the disturbances to be simulated (generator trips, faults, parameter changes, etc.).

#### `addDst(filename)`

```python
case.addDst('events.dst')
```

#### `getDst()`

Return the currently registered disturbance file path.

```python
path = case.getDst()
```

#### `clearDst()`

Remove the disturbance file from the case.

```python
case.clearDst()
```

:::caution
A disturbance file must be provided, otherwise the simulator will raise an exception.
:::

---

### Trajectory File

Specifies the file where time-series simulation results (trajectories) are saved for post-processing. This file is used by `stepss.extractor` to access results after the simulation completes.

#### `addTrj(filename)`

```python
case.addTrj('output.trj')
```

#### `getTrj()`

Return the currently registered trajectory file path.

```python
path = case.getTrj()
```

:::note
This is optional. If omitted, no trajectory file is written and result extraction via `stepss.extractor` will not be possible.
:::

---

### Observables File

Defines which components and quantities are recorded in the trajectory file.

#### `addObs(filename)`

```python
case.addObs('obs.dat')
```

#### `getObs()`

Return the currently registered observables file path.

```python
path = case.getObs()
```

:::note
Required when a trajectory file is specified. Defines what data is stored in the trajectory.
:::

---

### Output/Trace Files

#### `addOut(filename)`

Set the main output trace file for simulation progress logging.

```python
case.addOut('output.trace')
```

#### `getOut()`

Return the currently registered output trace file path.

```python
path = case.getOut()
```

#### `addCont(filename)`

Set the continuous trace file. Records Newton solver convergence information at each step. Useful for debugging but can slow down the simulation.

```python
case.addCont('cont.trace')
```

#### `getCont()`

Return the currently registered continuous trace file path.

```python
path = case.getCont()
```

#### `addDisc(filename)`

Set the discrete trace file. Records discrete events: switching actions from disturbance files, discrete controllers, or discrete variables in injector/torque/exciter/two-port models.

```python
case.addDisc('disc.trace')
```

#### `getDisc()`

Return the currently registered discrete trace file path.

```python
path = case.getDisc()
```

#### `clearDisc()`

Remove the discrete trace file from the case.

```python
case.clearDisc()
```

:::note
All output/trace files are optional.
:::

---

### Runtime Observables

Runtime observables are recorded by the engine while a simulation runs, into a
curve file you can read with `cur` and plot with `curplot`. Nothing has to be
installed for this.

#### `addRunObs(obs_string)`

Add a runtime observable. The following observable types are supported:

**`BV BUSNAME`**, Voltage magnitude of a bus:

```python
case.addRunObs('BV 1041')
```

**`MS MACHINE_NAME`**, Rotor speed of a synchronous machine:

```python
case.addRunObs('MS g1')
```

**`BPE / BQE / BPO / BQO BRANCH_NAME`**, Active (P) or reactive (Q) power at the origin (O) or extremity (E) of a branch:

```python
case.addRunObs('BPO 1041-01')   # active power at origin of branch 1041-01
case.addRunObs('BQO 1041-01')   # reactive power at origin
case.addRunObs('BPE 1041-01')   # active power at extremity
case.addRunObs('BQE 1041-01')   # reactive power at extremity
```

**`ON INJECTOR_NAME OBSERVABLE_NAME`**, Named observable from an injector model:

```python
case.addRunObs('ON WT1a Pw')    # observable Pw from injector WT1a
```

**`TO TWOP_NAME OBSERVABLE_NAME`**, Named observable from a two-port model:

```python
case.addRunObs('TO hvdc1 P1')   # observable P1 from two-port hvdc1
```

**`RT RT`**, Real-time versus simulated-time plot (useful to gauge simulation speed):

```python
case.addRunObs('RT RT')
```

#### `clearRunObs()`

Remove all runtime observables.

```python
case.clearRunObs()
```

:::note
Nothing needs to be installed for run-time observables.
:::

---

## `stepss.sim`: Simulation Control

The `stepss.sim` class runs simulations. It wraps the RAMSES dynamic library and supports start/pause/continue, runtime queries, and disturbance injection.

---

### Initializing

```python
import stepss

ram = stepss.sim()                        # use bundled RAMSES libraries
ram = stepss.sim(custLibDir='/path/to/')  # use custom library directory
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `custLibDir` | `str` or `None` | Custom path to the RAMSES library directory. Default: use bundled libraries. |

---

### Running Simulations

A properly configured `stepss.cfg` test case is required before running a simulation.

#### `execSim(case)`: run to completion

```python
ram.execSim(case)
```

#### `execSim(case, t)`: start and pause at time t

Start the simulation and pause at a specific time (in seconds):

```python
ram.execSim(case, 10.0)    # start and pause at t = 10 s
```

#### `contSim(t)`: continue to time t

Resume a paused simulation until a specified time:

```python
ram.contSim(20.0)                     # resume until t = 20 s
ram.contSim(ram.getSimTime() + 60.0)  # advance by 60 s from current time
ram.contSim(ram.getInfTime())         # run to the end of the time horizon
```

#### `endSim()`: terminate early

Terminate the simulation before reaching the time horizon:

```python
ram.endSim()
```

#### `pauseSim(t_pause)`: schedule a pause

Schedule a pause at a given simulated time; it takes effect on the next `execSim()` or `contSim()` call:

```python
ram.pauseSim(10.0)
ram.execSim(case)   # will pause at t = 10 s
```

#### `getEndSim()`

Return `0` while the simulation is still running, `1` once it has ended:

```python
if ram.getEndSim():
    print('simulation finished')
```

#### `getLastErr()`

Return the last error message issued by RAMSES as a string. Useful after catching a `RAMSESError`:

```python
msg = ram.getLastErr()
```

---

### Querying State

When the simulation is paused, the following methods query the current system state.

#### `getSimTime()`

Return the current simulation time in seconds.

```python
t = ram.getSimTime()
```

#### `getInfTime()`

Return the value used as "infinity" (i.e., the end of the simulation time horizon). Pass this to `contSim()` to run to completion.

```python
t_inf = ram.getInfTime()
ram.contSim(ram.getInfTime())
```

#### `getAllCompNames(type)`

Return a list of all component names of the given type.

```python
buses    = ram.getAllCompNames('BUS')     # list of all bus names
gens     = ram.getAllCompNames('SYNC')    # list of all generator names
injs     = ram.getAllCompNames('INJ')     # list of all injector names
dctls    = ram.getAllCompNames('DCTL')    # list of all discrete controller names
branches = ram.getAllCompNames('BRANCH')  # list of all branch names
twops    = ram.getAllCompNames('TWOP')    # list of all two-port names
shunts   = ram.getAllCompNames('SHUNT')   # list of all shunt names
loads    = ram.getAllCompNames('LOAD')    # list of all load names
```

Supported component types: `BUS`, `SYNC`, `INJ`, `DCTL`, `BRANCH`, `TWOP`, `SHUNT`, `LOAD`.

#### `getCompName(comp_type, num)`

Return the name of the `num`-th component (1-based) of the given type. Accepts the same component types as `getAllCompNames()`.

```python
first_bus = ram.getCompName('BUS', 1)   # e.g. 'B1'
```

#### `getBusVolt(names)`

Return voltage magnitudes (in pu) for a list of bus names.

```python
ram.execSim(case, 10.0)
bus_names = ['g1', 'g2', '4032']
voltages = ram.getBusVolt(bus_names)
```

#### `getBusPha(names)`

Return voltage phase angles (in degrees) for a list of bus names.

```python
phases = ram.getBusPha(bus_names)
```

#### `getBranchPow(names)`

Return power flows for a list of branch names. Each entry is `[P_from, Q_from, P_to, Q_to]` in MW and Mvar.

```python
powers = ram.getBranchPow(['1041-01'])
# powers[0] == [P_from, Q_from, P_to, Q_to]
```

#### `getBranchCur(names)`

Return branch currents for a list of branch names. Each entry contains the x–y current components at the origin and extremity: `[ix_orig, iy_orig, ix_extr, iy_extr]`.

```python
currents = ram.getBranchCur(['1011-1013', '1012-1014'])
```

#### `getObs(comp_types, comp_names, obs_names)`

Get the current value of named observables for a list of components. Lists must be the same length.

```python
comp_type = ['INJ', 'EXC', 'TOR']
comp_name = ['L_11', 'g2',  'g3']
obs_name  = ['P',    'vf',  'Pm']
obs = ram.getObs(comp_type, comp_name, obs_name)
```

Supported model types: `EXC` (exciter), `TOR` (governor), `INJ` (injector), `TWOP` (two-port), `DCTL` (discrete controller), `SYN` (synchronous generator).

#### `getPrm(comp_types, comp_names, prm_names)`

Get parameter values for a list of components. Lists must be the same length.

```python
comp_type = ['EXC', 'EXC']
comp_name = ['g1',  'g2']
prm_name  = ['V0',  'KPSS']
prms = ram.getPrm(comp_type, comp_name, prm_name)
```

#### `getPrmNames(comp_types, comp_names)`

List the parameter names of one or more model instances. Accepts single strings or equal-length lists; component types are `EXC`, `TOR`, `INJ`, `DCTL`, `TWOP`.

```python
names = ram.getPrmNames('EXC', 'g1')   # list of parameter names of g1's exciter
```

---

### Runtime Observable Recording

Observables can also be selected programmatically after the simulation starts, instead of via an observables file. Call the three methods in order, after `execSim(case, 0.0)`:

#### `initObserv(traj_filenm)`

Initialize the runtime observable recording system and set the output trajectory file.

#### `addObserv(string)`

Register one observable selector in RAMSES format (e.g. `'BUS *'`, `'SYNC g1'`). Call once per selector.

#### `finalObserv()`

Finalize the selection, allocate the recording buffers, and write the trajectory file header.

```python
ram.execSim(case, 0.0)
ram.initObserv('obs.trj')
ram.addObserv('BUS *')      # record all bus voltages
ram.addObserv('SYNC g1')    # record machine g1
ram.finalObserv()
ram.contSim(ram.getInfTime())
```

---

### Subsystems

Subsystems select a group of buses for aggregate queries.

#### `defineSS(ssID, filter1, filter2, filter3)`

Define subsystem `ssID` as the intersection of three filters: voltage levels, zones, and bus names. Each filter is a list of strings; an empty list deactivates that filter.

```python
ram.defineSS(1, ['735'], [], [])   # subsystem 1 = all 735 kV buses
```

#### `getSS(ssID)`

Return the list of buses belonging to a subsystem.

```python
buses = ram.getSS(1)
```

#### `getTrfoSS(ssID, location, in_service, rettype)`

Return transformer information for a subsystem. `location`: `1` = both ends inside the subsystem, `2` = tie transformers, `3` = both. `in_service`: `1` = in-service only, `2` = all. `rettype` selects the returned quantity: `NAME`, `From`, `To`, `Status`, `Tap`, `Currentf`, `Currentt`, `Pf`, `Qf`, `Pt`, `Qt`.

```python
status = ram.getTrfoSS(1, 3, 2, 'Status')
```

---

### Runtime Disturbances

Disturbances can be added dynamically while the simulation is paused, enabling interactive scenario analysis.

#### `addDisturb(time, description)`

Schedule a disturbance to occur at a given simulation time.

The disturbance description string follows the same syntax as the disturbance file format. See [Disturbances](/user-guide/disturbances/) for the complete reference.

```python
ram.execSim(case, 80.0)

# Trip generator g7 at t = 100 s
ram.addDisturb(100.0, 'BREAKER SYNC_MACH g7 0')

# Apply a 3-phase fault at bus 4032 and clear it 100 ms later
ram.addDisturb(100.0, 'FAULT BUS 4032 0. 0.')
ram.addDisturb(100.1, 'CLEAR BUS 4032')

# Step change in an LTC setpoint
ram.addDisturb(100.0, 'CHGPRM DCTL 1-1041 Vsetpt -0.05 0')

ram.contSim(ram.getInfTime())
```

---

### Jacobian Export

#### `getJac()`

Export the system Jacobian in descriptor form at the current pause point. Returns a tuple `(A, E)` of `scipy.sparse.csc_matrix` objects, where `A` holds the numerical Jacobian values and `E` is the structural incidence matrix of the descriptor system. Two intermediate text files are also written to the working directory:

| File | Contents |
|------|----------|
| `py_val.dat` | Jacobian values (parsed into `A`) |
| `py_eqs.dat` | Structural incidence matrix (parsed into `E`) |

```python
ram.execSim(case, 10.0)
A, E = ram.getJac()
```

Use this when you want to drive your own solver, for instance the sparse
shift-invert methods in `scipy.sparse.linalg` that large systems need. To have
RAMSES do the analysis instead, schedule an `EIG` disturbance; see
[Eigenanalysis](/user-guide/eigenanalysis/).

:::note
Set `$OMEGA_REF SYN ;` in the solver settings data file when exporting the Jacobian for eigenanalysis.
:::

---

## `stepss.extractor`: Result Extraction

The `stepss.extractor` class extracts and visualises time-series results from a trajectory file produced during simulation.

---

### Initializing

Pass the trajectory file path to the extractor:

```python
import stepss

case = stepss.cfg('cmd.txt')
# ... run simulation ...
ext = stepss.extractor(case.getTrj())
```

Or provide the file path directly:

```python
ext = stepss.extractor('output.trj')
```

---

### Curve Objects

All extraction methods return objects whose attributes are **curve objects** (`stepss.cur` named tuples). Every curve object has:

| Attribute | Type | Description |
|-----------|------|-------------|
| `time` | `numpy.ndarray` | Time values in seconds |
| `value` | `numpy.ndarray` | Observable values |
| `msg` | `str` | Description string (used as plot legend label) |

#### `.plot()`

Display the curve using Matplotlib:

```python
bus = ext.getBus('4044')
bus.mag.plot()
```

---

### Extraction Methods

#### `getBus(name)`

Retrieve voltage time series for a bus. Returns an object with:

| Attribute | Description |
|-----------|-------------|
| `.mag` | Voltage magnitude (pu) |
| `.pha` | Voltage phase angle (deg) |

```python
bus = ext.getBus('4044')
bus.mag.plot()   # voltage magnitude (pu)
bus.pha.plot()   # voltage phase angle (deg)
```

---

#### `getSync(name)`

Retrieve the full set of synchronous machine observables. Returns an object with:

| Attribute | Description |
|-----------|-------------|
| `.P` | Active power (MW) |
| `.Q` | Reactive power (Mvar) |
| `.S` | Rotor speed (pu; 1 = nominal) |
| `.A` | Rotor angle w.r.t. COI (deg) |
| `.FV` | Field voltage (pu) |
| `.FC` | Field current (pu) |
| `.T` | Mechanical torque (pu) |
| `.ET` | Electromagnetic torque (pu) |
| `.FW` | Field winding flux |
| `.DD` | d1 damper flux |
| `.QD` | q1 damper flux |
| `.QW` | q2 winding flux |
| `.SC` | COI speed **deviation** (pu; 0 = nominal) |

:::note
The two speed observables use different conventions: `.S` is the whole rotor
speed (1 = nominal), while `.SC` is the deviation of the centre-of-inertia
(COI) speed from nominal (0 = nominal). The system frequency in Hz is
`fnom * (1 + SC)` or, per machine, `fnom * S`.
:::

```python
gen = ext.getSync('g1')
gen.P.plot()    # active power (MW)
gen.Q.plot()    # reactive power (Mvar)
gen.S.plot()    # rotor speed (pu)
gen.A.plot()    # rotor angle w.r.t. COI (deg)
gen.FV.plot()   # field voltage (pu)
gen.FC.plot()   # field current (pu)
gen.T.plot()    # mechanical torque (pu)
gen.ET.plot()   # electromagnetic torque (pu)
```

---

#### `getExc(name)`

Retrieve exciter observables. Available observables depend on the exciter model.

| Attribute | Description |
|-----------|-------------|
| `.obsdict` | `dict` mapping observable name → description |
| *(model-dependent)* | Access by observable name, e.g. `.vf` |

```python
exc = ext.getExc('g1')
print(exc.obsdict)   # list available observables for this model
exc.vf.plot()        # field voltage (model-dependent name)
```

---

#### `getTor(name)`

Retrieve governor/torque model observables. Available observables depend on the governor model.

| Attribute | Description |
|-----------|-------------|
| `.obsdict` | `dict` mapping observable name → description |
| *(model-dependent)* | Access by observable name, e.g. `.Pm` |

```python
gov = ext.getTor('g1')
print(gov.obsdict)   # list available observables for this model
gov.Pm.plot()        # mechanical power (pu)
```

---

#### `getInj(name)`

Retrieve injector observables. Injectors include renewable energy sources (wind, PV, BESS), loads, and other single-bus components.

| Attribute | Description |
|-----------|-------------|
| `.obsdict` | `dict` mapping observable name → description |
| *(model-dependent)* | Access by observable name, e.g. `.Pw` |

```python
inj = ext.getInj('WT1a')
print(inj.obsdict)   # list available observables
inj.Pw.plot()        # wind power (model-dependent name)
```

---

#### `getTwop(name)`

Retrieve two-port model observables. Two-port models include HVDC links (LCC and VSC), SVCs, and DC systems.

| Attribute | Description |
|-----------|-------------|
| `.obsdict` | `dict` mapping observable name → description |
| *(model-dependent)* | Access by observable name, e.g. `.P1`, `.P2` |

```python
twop = ext.getTwop('hvdc1')
print(twop.obsdict)  # list available observables
twop.P1.plot()       # active power at terminal 1
twop.P2.plot()       # active power at terminal 2
```

---

#### `getDctl(name)`

Retrieve discrete controller observables. Discrete controllers include LTC transformers, under-voltage load shedding, phase shifters, etc.

| Attribute | Description |
|-----------|-------------|
| `.obsdict` | `dict` mapping observable name → description |

```python
dctl = ext.getDctl('1-1041')
print(dctl.obsdict)  # list available observables
```

---

#### `getBranch(name)`

Retrieve branch (line/transformer) power flow time series.

| Attribute | Description |
|-----------|-------------|
| `.PF` | Active power at FROM end (MW) |
| `.QF` | Reactive power at FROM end (Mvar) |
| `.PT` | Active power at TO end (MW) |
| `.QT` | Reactive power at TO end (Mvar) |
| `.RM` | Transformer ratio magnitude |
| `.RA` | Transformer phase angle (deg) |

```python
branch = ext.getBranch('1041-01')
branch.PF.plot()   # active power at FROM end (MW)
branch.QF.plot()   # reactive power at FROM end (Mvar)
branch.PT.plot()   # active power at TO end (MW)
branch.QT.plot()   # reactive power at TO end (Mvar)
branch.RM.plot()   # transformer ratio magnitude
branch.RA.plot()   # transformer phase angle (deg)
```

---

#### `getShunt(name)`

Retrieve shunt compensation time series.

| Attribute | Description |
|-----------|-------------|
| `.Q` | Reactive power produced (Mvar) |

```python
ext.getShunt('sh1').Q.plot()
```

---

#### `getLoad(name)`

Retrieve load time series.

| Attribute | Description |
|-----------|-------------|
| `.P` | Active power consumed (MW) |
| `.Q` | Reactive power consumed (Mvar) |

```python
ext.getLoad('L_1').P.plot()
```

---

### Multi-Curve Plotting

#### `stepss.curplot(curves)`

Display multiple curve objects on the same axes. Each curve's `msg` field is used as the legend label.

```python
import stepss

ext = stepss.extractor(case.getTrj())

curves = [
    ext.getSync('g1').S,
    ext.getSync('g2').S,
    ext.getSync('g3').S,
]
stepss.curplot(curves)
```

---

## `stepss.monitor`: Live Plotting

`monitor` plots chosen quantities while a simulation runs. It steps the engine
forward in slices, reads those quantities at every pause, and redraws a stacked
figure: one panel per observable, all sharing the time axis.

The engine is polled in process, so nothing is read from disk and nothing has to
be installed beyond matplotlib, which pip installs with the package. Runtime
observables, above, are a separate mechanism in which the engine writes a curve
file of its own; the two are independent and can be used together.

```python
import stepss

ram = stepss.sim()
case = stepss.cfg('cmd.txt')
ram.execSim(case, 0.0)                    # initialise, paused at t = 0

mon = stepss.monitor(ram, ['BV 4044', 'MS g6', 'RT RT'], title='Nordic')
curves = mon.run(step=0.5)                # run to the end of the scenario
```

The simulation must already be initialised and paused, which `execSim` does when
given a `pause` time.

### `monitor(ram, observables, title=None, refresh=0.2, show=True)`

| Argument | Description |
|-----------|-------------|
| `ram` | The `stepss.sim` driving the run. |
| `observables` | What to plot: descriptor strings, `(label, callable)` pairs, or bare callables. A single observable need not be wrapped in a list. |
| `title` | Figure title. |
| `refresh` | Minimum wall-clock seconds between redraws. Samples are never skipped, only draws; `0` redraws at every sample. |
| `show` | `False` collects the samples and builds no figure. |

### Observable descriptors

The vocabulary is the one `addRunObs` uses, plus `BA` and the generic `OBS`:

| Descriptor | Quantity | Unit |
|-----------|-------------|------|
| `BV BUSNAME` | Voltage magnitude of a bus | pu |
| `BA BUSNAME` | Voltage phase of a bus | deg |
| `MS MACHINE_NAME` | Rotor speed of a synchronous machine | pu |
| `BPO / BQO / BPE / BQE BRANCH_NAME` | Active or reactive power at the origin or extremity of a branch | MW, Mvar |
| `ON INJECTOR_NAME OBSERVABLE_NAME` | Named observable of an injector model | set by the model |
| `TO TWOP_NAME OBSERVABLE_NAME` | Named observable of a two-port model | set by the model |
| `OBS TYPE NAME OBSERVABLE_NAME` | Named observable of any component type `getObs` accepts | set by the model |
| `RT RT` | Elapsed wall-clock time, to gauge simulation speed | s |

Anything the descriptors do not cover is a callable, taking the simulator and
returning one number:

```python
mon = stepss.monitor(ram, [
    'BV 4044',
    ('4044 reactive reserve (Mvar)', lambda r: r.getObs('SYN', 'g6', 'Q')[0]),
])
```

### `run(step=1.0, until=None)`

Advance the simulation, sampling and redrawing at each pause, and return one
`cur` per observable. Returns when the engine reports the end of the scenario,
when `until` is reached, or when a slice fails to advance the simulated time.

```python
curves = mon.run(step=0.1, until=30.0)    # 30 s of simulated time, sampled every 0.1 s
```

`step` is simulated seconds per slice, so it sets both the sampling resolution
and the redraw cadence. The engine pauses at the first internal step at or after
the requested time, so the samples land on or just after the multiples of `step`.

If the engine raises, the samples taken up to that point stay available from
`curves()`:

```python
from stepss.globals import RAMSESError

try:
    mon.run(step=1.0)
except RAMSESError:
    stepss.curplot(mon.curves())          # everything up to the failure
```

### `curves()`

Return everything sampled so far, one `cur` per observable, in the order given
to the constructor. These are the same objects `extractor` produces, so
`curplot` and the rest of the post-processing accept them unchanged.

### `sample()`

Read every observable once, at the current simulated time. Call it directly when
driving the simulation yourself:

```python
mon = stepss.monitor(ram, ['BV 4044'])
for target in [10.0, 20.0, 30.0]:
    ram.contSim(target)
    ram.addDisturb(target + 1.0, 'CHGPRM DCTL 1-1041 Vsetpt -0.01 0')
    mon.sample()
    mon.refresh()
```

### `refresh(force=False)`

Push the samples into the figure and redraw it. A draw falling inside the
`refresh` interval is skipped unless `force` is set.

### `savefig(fname, **kwargs)`

Redraw and write the figure to a file, forwarding to
`matplotlib.figure.Figure.savefig`.

### `close()`

Close the figure. The samples are unaffected: `curves()` keeps working.

:::note
On a file-only matplotlib backend such as `Agg`, and in Jupyter's inline mode,
there is no window to animate: the monitor collects the samples and builds the
figure, and `savefig` writes the same chart a window would have shown. Closing
the window mid-run stops the redraws and leaves the run going.
:::

---

## Complete Example

```python
import stepss

# --- Build test case ---
case = stepss.cfg()
case.addData('dyn_A.dat')
case.addData('settings1.dat')
case.addInit('init.trace')
case.addDst('events.dst')
case.addTrj('output.trj')
case.addObs('obs.dat')
case.addOut('output.trace')
case.addCont('cont.trace')
case.addDisc('disc.trace')

# Runtime observables, recorded by the engine into a curve file
case.addRunObs('BV 1041')
case.addRunObs('MS g1')
case.addRunObs('RT RT')

# Save configuration
case.writeCmdFile('cmd.txt')

# --- Run simulation ---
ram = stepss.sim()

# Start and pause at t = 80 s
ram.execSim(case, 80.0)

# Inject a disturbance dynamically
ram.addDisturb(100.0, 'FAULT BUS 4032 0. 0.')
ram.addDisturb(100.1, 'CLEAR BUS 4032')

# Export Jacobian at this operating point
A, E = ram.getJac()

# Run to end
ram.contSim(ram.getInfTime())

# --- Extract results ---
ext = stepss.extractor(case.getTrj())

# Bus voltages
ext.getBus('4044').mag.plot()

# Generator observables
gen = ext.getSync('g1')
gen.S.plot()    # rotor speed
gen.A.plot()    # rotor angle

# Branch flows
ext.getBranch('1041-01').PF.plot()

# Plot multiple rotor speeds together
stepss.curplot([
    ext.getSync('g1').S,
    ext.getSync('g2').S,
    ext.getSync('g3').S,
])
```

## Next Steps

- [Examples](/python/examples/), Practical simulation examples and workflows
- [Test Systems](/test-systems/), Ready-to-run benchmark systems
