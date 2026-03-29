---
title: API Reference
description: PyRAMSES Python API — complete reference for pyramses.cfg, pyramses.sim, and pyramses.extractor
---

## `pyramses.cfg` — Test Case Configuration

The `pyramses.cfg` class defines a simulation scenario: data files, disturbance file, output files, observables, and runtime options.

---

### Initializing

Create an empty configuration or load one from a previously saved command file:

```python
import pyramses

case = pyramses.cfg()             # empty configuration
case = pyramses.cfg("cmd.txt")    # load from command file
```

Load multiple cases in a loop:

```python
import pyramses

list_of_cases = []
for i in range(12):
    list_of_cases.append(pyramses.cfg('cmd' + str(i) + '.txt'))
```

#### `writeCmdFile(filename)`

Save the current configuration to a command file. Useful for reproducing a run later.

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

Specifies the file where time-series simulation results (trajectories) are saved for post-processing. This file is used by `pyramses.extractor` to access results after the simulation completes.

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
This is optional. If omitted, no trajectory file is written and result extraction via `pyramses.extractor` will not be possible.
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

Runtime observables are displayed live during simulation using Gnuplot.

#### `addRunObs(obs_string)`

Add a runtime observable. The following observable types are supported:

**`BV BUSNAME`** — Voltage magnitude of a bus:

```python
case.addRunObs('BV 1041')
```

**`MS MACHINE_NAME`** — Rotor speed of a synchronous machine:

```python
case.addRunObs('MS g1')
```

**`BPE / BQE / BPO / BQO BRANCH_NAME`** — Active (P) or reactive (Q) power at the origin (O) or extremity (E) of a branch:

```python
case.addRunObs('BPE 1041-01')   # active power at origin of branch 1041-01
case.addRunObs('BQE 1041-01')   # reactive power at origin
case.addRunObs('BPO 1041-01')   # active power at extremity
case.addRunObs('BQO 1041-01')   # reactive power at extremity
```

**`ON INJECTOR_NAME OBSERVABLE_NAME`** — Named observable from an injector model:

```python
case.addRunObs('ON WT1a Pw')    # observable Pw from injector WT1a
```

**`TO TORQUE_NAME OBSERVABLE_NAME`** — Named observable from a governor/torque model:

```python
case.addRunObs('TO g1 Pm')      # mechanical power from governor of g1
```

**`RT RT`** — Real-time versus simulated-time plot (useful to gauge simulation speed):

```python
case.addRunObs('RT RT')
```

#### `clearRunObs()`

Remove all runtime observables.

```python
case.clearRunObs()
```

:::caution
Gnuplot must be installed and available in the system PATH for runtime observables to work.
:::

---

## `pyramses.sim` — Simulation Control

The `pyramses.sim` class runs simulations. It wraps the RAMSES dynamic library and supports start/pause/continue, runtime queries, and disturbance injection.

---

### Initializing

```python
import pyramses

ram = pyramses.sim()                        # use bundled RAMSES libraries
ram = pyramses.sim(custLibDir='/path/to/')  # use custom library directory
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `custLibDir` | `str` or `None` | Custom path to the RAMSES library directory. Default: use bundled libraries. |

---

### Running Simulations

A properly configured `pyramses.cfg` test case is required before running a simulation.

#### `execSim(case)` — run to completion

```python
ram.execSim(case)
```

#### `execSim(case, t)` — start and pause at time t

Start the simulation and pause at a specific time (in seconds):

```python
ram.execSim(case, 10.0)    # start and pause at t = 10 s
```

#### `contSim(t)` — continue to time t

Resume a paused simulation until a specified time:

```python
ram.contSim(20.0)                     # resume until t = 20 s
ram.contSim(ram.getSimTime() + 60.0)  # advance by 60 s from current time
ram.contSim(ram.getInfTime())         # run to the end of the time horizon
```

#### `endSim()` — terminate early

Terminate the simulation before reaching the time horizon:

```python
ram.endSim()
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

#### `getBusVolt(names)`

Return voltage magnitudes (in pu) for a list of bus names.

```python
ram.execSim(case, 10.0)
bus_names = ['g1', 'g2', '4032']
voltages = ram.getBusVolt(bus_names)
```

#### `getBusPha(names)`

Return voltage phase angles (in radians) for a list of bus names.

```python
phases = ram.getBusPha(bus_names)
```

#### `getBranchPow(names)`

Return power flows for a list of branch names. Each entry is `[P_from, Q_from, P_to, Q_to]` in MW and Mvar.

```python
powers = ram.getBranchPow(['1041-01'])
# powers[0] == [P_from, Q_from, P_to, Q_to]
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

---

### Runtime Disturbances

Disturbances can be added dynamically while the simulation is paused, enabling interactive scenario analysis.

#### `addDisturb(time, description)`

Schedule a disturbance to occur at a given simulation time. The syntax for `description` follows the RAMSES disturbance file format.

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

Export the system Jacobian matrix in descriptor form (`E`, `A` matrices) at the current pause point. Writes four files to the working directory:

| File | Contents |
|------|----------|
| `jac_val.dat` | Non-zero values |
| `jac_eqs.dat` | Equation names |
| `jac_var.dat` | Variable names |
| `jac_struc.dat` | Sparsity structure |

```python
ram.execSim(case, 10.0)
ram.getJac()
```

These files can be used for small-signal stability analysis with the [RAMSES Eigenanalysis](https://github.com/SPS-L/RAMSES-Eigenanalysis) tool.

:::note
Set `$OMEGA_REF SYN ;` in the solver settings data file when exporting the Jacobian for eigenanalysis.
:::

---

## `pyramses.extractor` — Result Extraction

The `pyramses.extractor` class extracts and visualises time-series results from a trajectory file produced during simulation.

---

### Initializing

Pass the trajectory file path to the extractor:

```python
import pyramses

case = pyramses.cfg('cmd.txt')
# ... run simulation ...
ext = pyramses.extractor(case.getTrj())
```

Or provide the file path directly:

```python
ext = pyramses.extractor('output.trj')
```

---

### Curve Objects

All extraction methods return objects whose attributes are **curve objects** (`pyramses.cur` named tuples). Every curve object has:

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
| `.pha` | Voltage phase angle (rad) |

```python
bus = ext.getBus('4044')
bus.mag.plot()   # voltage magnitude (pu)
bus.pha.plot()   # voltage phase angle (rad)
```

---

#### `getSync(name)`

Retrieve the full set of synchronous machine observables. Returns an object with:

| Attribute | Description |
|-----------|-------------|
| `.P` | Active power (MW) |
| `.Q` | Reactive power (Mvar) |
| `.S` | Rotor speed (pu) |
| `.A` | Rotor angle w.r.t. COI (deg) |
| `.FV` | Field voltage (pu) |
| `.FC` | Field current (pu) |
| `.T` | Mechanical torque (pu) |
| `.ET` | Electromagnetic torque (pu) |
| `.FW` | Field winding flux |
| `.DD` | d1 damper flux |
| `.QD` | q1 damper flux |
| `.QW` | q2 winding flux |
| `.SC` | COI speed |

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

### Multi-Curve Plotting

#### `pyramses.curplot(curves)`

Display multiple curve objects on the same axes. Each curve's `msg` field is used as the legend label.

```python
import pyramses

ext = pyramses.extractor(case.getTrj())

curves = [
    ext.getSync('g1').S,
    ext.getSync('g2').S,
    ext.getSync('g3').S,
]
pyramses.curplot(curves)
```

---

## Complete Example

```python
import pyramses

# --- Build test case ---
case = pyramses.cfg()
case.addData('dyn_A.dat')
case.addData('settings1.dat')
case.addInit('init.trace')
case.addDst('events.dst')
case.addTrj('output.trj')
case.addObs('obs.dat')
case.addOut('output.trace')
case.addCont('cont.trace')
case.addDisc('disc.trace')

# Runtime observables (Gnuplot required)
case.addRunObs('BV 1041')
case.addRunObs('MS g1')
case.addRunObs('RT RT')

# Save configuration
case.writeCmdFile('cmd.txt')

# --- Run simulation ---
ram = pyramses.sim()

# Start and pause at t = 80 s
ram.execSim(case, 80.0)

# Inject a disturbance dynamically
ram.addDisturb(100.0, 'FAULT BUS 4032 0. 0.')
ram.addDisturb(100.1, 'CLEAR BUS 4032')

# Export Jacobian at this operating point
ram.getJac()

# Run to end
ram.contSim(ram.getInfTime())

# --- Extract results ---
ext = pyramses.extractor(case.getTrj())

# Bus voltages
ext.getBus('4044').mag.plot()

# Generator observables
gen = ext.getSync('g1')
gen.S.plot()    # rotor speed
gen.A.plot()    # rotor angle

# Branch flows
ext.getBranch('1041-01').PF.plot()

# Plot multiple rotor speeds together
pyramses.curplot([
    ext.getSync('g1').S,
    ext.getSync('g2').S,
    ext.getSync('g3').S,
])
```
