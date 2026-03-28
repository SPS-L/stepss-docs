---
title: Examples
description: Practical examples using PyRAMSES
---

## Nordic Test System

The Nordic test system is included in the [stepss-PyRAMSES repository](https://github.com/SPS-L/stepss-PyRAMSES/tree/master/examples/Nordic) as a ready-to-run example.

### Running the Example

```python
import pyramses
import os

# Change to the example directory
os.chdir("examples/Nordic")

# Load the case configuration
case = pyramses.cfg("cmd.txt")

# Initialize the simulator
ram = pyramses.sim()

# Run the simulation
ram.execSim(case)

# Extract and visualize results
ext = pyramses.extractor(case.getTrj())

# Plot bus voltage magnitudes
ext.getBus('1041').mag.plot()
ext.getBus('1044').mag.plot()
```

## Step-by-Step: Building a Case Programmatically

### 1. Define the Test Case

```python
import pyramses

# Create case from scratch
case = pyramses.cfg()

# Add data files
case.addData("network.dat")        # Network topology
case.addData("dynamic_data.dat")   # Dynamic models
case.addData("settings.dat")       # Solver settings

# Set disturbance file
case.addDst("fault_scenario.dst")

# Set output files
case.addInit("init.trace")
case.addTrj("results.rtrj")
case.addObs("observables.obs")
case.addCont("continuous.trace")
case.addDisc("discrete.trace")
```

### 2. Run with Pause Points

```python
ram = pyramses.sim()

# Start simulation paused at t = 0
ram.execSim(case, 0)

# Read an observable
v = ram.getObs('BUS', '1041', 'mag')
print(f"Initial voltage at bus 1041: {v:.4f} pu")

# Continue to t = 10 s
ram.contSim(10.0)

# Check voltage after disturbance
v = ram.getObs('BUS', '1041', 'mag')
print(f"Voltage at t=10s: {v:.4f} pu")

# Continue to end
ram.contSim()
```

### 3. Extract and Plot Results

```python
ext = pyramses.extractor(case.getTrj())

# Bus voltages
import matplotlib.pyplot as plt

bus_1041 = ext.getBus('1041')
bus_1044 = ext.getBus('1044')

plt.figure(figsize=(10, 6))
plt.plot(bus_1041.mag.time, bus_1041.mag.value, label='Bus 1041')
plt.plot(bus_1044.mag.time, bus_1044.mag.value, label='Bus 1044')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (pu)')
plt.title('Bus Voltage Magnitudes')
plt.legend()
plt.grid(True)
plt.show()
```

## Eigenanalysis with PyRAMSES

Combining PyRAMSES with the [RAMSES Eigenanalysis tool](https://github.com/SPS-L/RAMSES-Eigenanalysis):

### 1. Export Jacobian

Create a disturbance file that exports the Jacobian at $t = 1$ s:

```
0.000 CONTINUE SOLVER BD 0.0200 0.001 0. ALL
1.000 JAC 'jac'
2.000 STOP
```

Ensure the solver settings include:
```
$OMEGA_REF SYN ;
$SCHEME IN ;
```

### 2. Run Simulation

```python
import pyramses

ram = pyramses.sim()
case = pyramses.cfg("cmd_jac.txt")
ram.execSim(case)
```

### 3. Analyze in MATLAB

```matlab
addpath('path/to/RAMSES-Eigenanalysis')
addpath('path/to/RAMSES-Eigenanalysis/scripts')

% Run eigenanalysis (QZ method)
ssa('jac_val.dat', 'jac_eqs.dat', 'jac_var.dat', 'jac_struc.dat')

% With custom filtering (eigenvalues with real part > -2, damping < 10%)
ssa('jac_val.dat', 'jac_eqs.dat', 'jac_var.dat', 'jac_struc.dat', ...
    -2.0, 0.10, 'QZ')
```

## Runtime Observables

Display real-time plots during simulation (requires Gnuplot):

```python
import pyramses

case = pyramses.cfg()
case.addData("network.dat")
case.addData("dynamic.dat")
case.addDst("disturbance.dst")

# Add runtime observables
case.addRunObs("BUS 1041 mag")
case.addRunObs("BUS 1044 mag")
case.addRunObs("SYNC g1 speed")

ram = pyramses.sim()
ram.execSim(case)   # Gnuplot windows will show live traces
```

## Writing Command Files

Export the case configuration to a standard command file:

```python
case = pyramses.cfg()
case.addData("network.dat")
case.addData("dynamic.dat")
case.addDst("scenario.dst")
case.addTrj("result.rtrj")
case.addObs("obs.obs")

# Save to file
case.writeCmdFile("generated_cmd.txt")

# Or get as string
cmd_string = case.writeCmdFile()
print(cmd_string)
```
