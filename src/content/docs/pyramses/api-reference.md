---
title: API Reference
description: PyRAMSES Python API documentation
---

## Module Structure

```python
import pyramses

# Core classes
pyramses.sim        # Simulator interface
pyramses.cfg        # Test case configuration
pyramses.extractor  # Result extraction
pyramses.cur        # Curve data container
pyramses.curplot    # Curve plotting utility
```

---

## `pyramses.sim` — Simulator

The main simulation interface. Wraps the RAMSES dynamic library (DLL/SO).

### Constructor

```python
ram = pyramses.sim(custLibDir=None)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `custLibDir` | `str` or `None` | Custom path to RAMSES library directory. Default: use bundled libraries. |

### Methods

#### `execSim(case, t_pause=None)`

Execute a simulation.

```python
ram.execSim(case)           # Run full simulation
ram.execSim(case, 0)        # Start simulation paused
ram.execSim(case, 10.0)     # Pause at t = 10 s
```

#### `contSim(t_pause=None)`

Continue a paused simulation.

```python
ram.contSim()               # Continue to end
ram.contSim(20.0)           # Continue until t = 20 s
```

#### `getLastErr()`

Return the last error message issued by RAMSES.

```python
err = ram.getLastErr()
print(err)
```

#### `getJac()`

Export the system Jacobian matrix. Returns sparse matrices `(E, A)` in descriptor form.

```python
E, A = ram.getJac()
```

#### `getObs(comp_type, comp_name, obs_name)`

Get the current value of an observable during a paused simulation.

```python
voltage = ram.getObs('BUS', '1041', 'mag')
```

#### `addObs(comp_type, comp_name, obs_name)`

Add a runtime observable for real-time plotting (requires Gnuplot).

```python
ram.addObs('BUS', '1041', 'mag')
```

#### `chgPrm(comp_type, comp_name, param_name, value)`

Change a parameter during a paused simulation.

```python
ram.chgPrm('EXC', 'g1', 'V0', 1.05)
```

---

## `pyramses.cfg` — Test Case Configuration

Defines the input files and configuration for a simulation.

### Constructor

```python
case = pyramses.cfg()            # Empty configuration
case = pyramses.cfg("cmd.txt")   # Load from command file
```

### Methods

#### `addData(filename)`

Add a data file (network, dynamic models, settings).

```python
case.addData("network.dat")
case.addData("dynamic.dat")
```

#### `addDst(filename)`

Set the disturbance file.

```python
case.addDst("disturbance.dst")
```

#### `addInit(filename)`

Set the initialization output file.

```python
case.addInit("init.trace")
```

#### `addTrj(filename)`

Set the trajectory output file.

```python
case.addTrj("result.rtrj")
```

#### `addObs(filename)`

Set the observables definition file (required when trajectory file is set).

```python
case.addObs("obs.obs")
```

#### `addCont(filename)` / `addDisc(filename)`

Set continuous/discrete trace output files.

```python
case.addCont("cont.trace")
case.addDisc("disc.trace")
```

#### `addRunObs(obs_string)`

Add a runtime observable (for real-time Gnuplot display).

```python
case.addRunObs("BUS 1041 mag")
```

#### `addOut(filename)`

Set the output file path.

```python
case.addOut(os.path.join(os.getcwd(), 'output.trace'))
```

#### `writeCmdFile(userFile=None)`

Write the command file to disk. Returns the command string if no file given.

```python
case.writeCmdFile("my_cmd.txt")    # Write to file
cmd_str = case.writeCmdFile()       # Return as string
```

#### Getters

```python
case.getTrj()     # Get trajectory file path
case.getInit()    # Get initialization file path
case.getOut()     # Get output file path
```

---

## `pyramses.extractor` — Result Extraction

Extract and plot time-series data from RAMSES trajectory files.

### Constructor

```python
ext = pyramses.extractor(case.getTrj())
```

### Methods

#### `getBus(busname)`

Returns bus-level data.

```python
bus = ext.getBus('1041')
bus.mag.plot()     # Voltage magnitude (pu)
bus.pha.plot()     # Voltage phase angle (deg)
```

#### `getSync(syncname)`

Returns synchronous machine data.

```python
sync = ext.getSync('g1')
sync.speed.plot()    # Rotor speed
sync.angle.plot()    # Rotor angle
sync.P.plot()        # Active power
sync.Q.plot()        # Reactive power
```

#### `getInj(injname)`

Returns injector observable data.

```python
inj = ext.getInj('L_11')
```

#### `getTwop(twopname)`

Returns two-port observable data.

#### `getDctl(dctlname)`

Returns discrete controller observable data.

#### `getBranch(branchname)`

Returns branch (line/transformer) data.

#### `getShunt(shuntname)` / `getLoad(loadname)`

Returns shunt or load data.

---

## `pyramses.cur` — Curve Container

A named tuple storing time-series data.

```python
from pyramses import cur

# Attributes
curve.time      # numpy array of time values
curve.value     # numpy array of data values
curve.msg       # description string
```

### Plotting

```python
curve.plot()                     # Plot single curve
pyramses.curplot([c1, c2, c3])   # Plot multiple curves
```

---

## Complete Example

```python
import pyramses
import os

# Create test case
case = pyramses.cfg()
case.addData("network.dat")
case.addData("dynamic.dat")
case.addData("settings.dat")
case.addInit("init.trace")
case.addDst("disturbance.dst")
case.addTrj("result.rtrj")
case.addObs("obs.obs")
case.addCont("cont.trace")
case.addDisc("disc.trace")

# Run simulation
ram = pyramses.sim()
ram.execSim(case)

# Extract results
ext = pyramses.extractor(case.getTrj())

# Plot bus voltages
ext.getBus('1041').mag.plot()
ext.getBus('1042').mag.plot()

# Plot generator speed
ext.getSync('g1').speed.plot()

# Clean up
del ram
```
