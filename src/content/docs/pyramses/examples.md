---
title: Examples
description: Practical examples using PyRAMSES
---

All examples assume the working directory contains the relevant data and disturbance files.

## Running a Basic Simulation

Define the test case, run the simulation, and extract results:

```python
import pyramses

case = pyramses.cfg()
case.addData('dyn_A.dat')        # dynamic models
case.addData('volt_rat_A.dat')   # power-flow initialisation
case.addData('settings1.dat')    # solver settings
case.addDst('short_trip_branch.dst')
case.addInit('init.trace')
case.addTrj('output.trj')        # save trajectories for post-processing
case.addObs('obs.dat')           # define which observables to record
case.addCont('cont.trace')
case.addDisc('disc.trace')
case.addRunObs('BV 4044')        # live voltage display (requires Gnuplot)
case.addRunObs('BV 1041')
case.writeCmdFile('cmd.txt')     # save for future reuse

ram = pyramses.sim()
ram.execSim(case)                # run to completion

ext = pyramses.extractor(case.getTrj())
ext.getBus('1041').mag.plot()    # voltage magnitude at bus 1041
```

:::note
Set `$NB_THREADS 0 ;` in the solver settings file to use all available CPU cores for parallel simulation.
:::

## Pause and Continue

Pause the simulation at intermediate time points to inspect state or add disturbances:

```python
ram = pyramses.sim()
ram.execSim(case, 0.0)                        # initialise, paused at t=0
ram.contSim(10.0)                             # simulate to t=10 s
ram.contSim(ram.getSimTime() + 60.0)          # advance 60 s from current time
ram.contSim(ram.getInfTime())                 # run to end of time horizon
```

## Querying System State

Query bus voltages, branch flows, observables, and parameters while paused:

```python
ram.execSim(case, 10.0)

# Bus voltages
busNames = ['g1', 'g2', 'g3']
voltages = ram.getBusVolt(busNames)   # list of voltage magnitudes (pu)
phases   = ram.getBusPha(busNames)    # list of phase angles (rad)

# Branch power flows
branch_pq = ram.getBranchPow(['1041-01'])  # [[P_from, Q_from, P_to, Q_to]]

# Component observables: P of injector L_11, vf of exciter g2, Pm of governor g3
comp_type = ['INJ',  'EXC', 'TOR']
comp_name = ['L_11', 'g2',  'g3']
obs_name  = ['P',    'vf',  'Pm']
obs = ram.getObs(comp_type, comp_name, obs_name)

# Component parameters: V0 of exciter g1, KPSS of exciter g2
comp_type = ['EXC', 'EXC']
comp_name = ['g1',  'g2']
prm_name  = ['V0',  'KPSS']
prms = ram.getPrm(comp_type, comp_name, prm_name)

# All component names of a type
all_buses = ram.getAllCompNames('BUS')
all_gens  = ram.getAllCompNames('SYNC')
```

## Adding Disturbances at Runtime

Inject disturbances and parameter changes while the simulation is running:

```python
ram.execSim(case, 80.0)

# LTC voltage setpoint changes at t=100 s (ramp)
for i in range(1, 6):
    ram.addDisturb(100.0, f'CHGPRM DCTL {i}-104{i}  Vsetpt -0.05 0')

# Fault and clearance
ram.addDisturb(100.0, 'FAULT BUS 4032 0. 0.')         # 3-phase short circuit
ram.addDisturb(100.1, 'CLEAR BUS 4032')                # clear fault
ram.addDisturb(100.1, 'BREAKER BRANCH 4032-4044 0 0')  # trip line

# Generator trip
ram.addDisturb(100.0, 'BREAKER SYNC_MACH g7 0')

ram.contSim(ram.getInfTime())
```

For full disturbance syntax, see the [Disturbances reference](/stepss-docs/user-guide/disturbances/).

## Plotting Results

Extract and plot time-series results after the simulation:

```python
import pyramses
ext = pyramses.extractor('output.trj')

# Single curve
ext.getSync('g5').S.plot()       # rotor speed of generator g5
ext.getBus('4044').mag.plot()    # voltage magnitude at bus 4044

# Multiple curves on the same plot
curves = [ext.getSync(f'g{i}').S for i in range(1, 5)]
pyramses.curplot(curves)

# Exciter and governor outputs
ext.getExc('g1').vf.plot()       # field voltage
ext.getTor('g1').Pm.plot()       # mechanical power

# Branch power flows
ext.getBranch('1041-01').PF.plot()

# Injector (wind/PV/BESS)
ext.getInj('WT1a').Pw.plot()

# Two-port (HVDC)
ext.getTwop('hvdc1').P1.plot()
```

## Parameter Sweep

Run multiple simulations with varying parameters and collect results:

```python
import pyramses
import numpy as np

results = {}
for disturbance_time in [5.0, 10.0, 20.0]:
    case = pyramses.cfg('cmd.txt')
    trj_file = f'output_{disturbance_time:.0f}.trj'
    case.addTrj(trj_file)
    case.addObs('obs.dat')

    ram = pyramses.sim()
    ram.execSim(case, 0.0)
    ram.addDisturb(disturbance_time, 'BREAKER SYNC_MACH g7 0')
    ram.contSim(ram.getInfTime())
    ram.endSim()

    ext = pyramses.extractor(trj_file)
    min_freq = np.min(ext.getSync('g5').S.value)
    results[disturbance_time] = min_freq
    print(f't_dist={disturbance_time:5.1f}s  min_speed={min_freq:.5f} pu')
```

## Eigenanalysis Workflow

Export the system Jacobian for small-signal stability analysis:

```python
import pyramses

case = pyramses.cfg('cmd.txt')
ram = pyramses.sim()

# Pause at steady-state operating point
ram.execSim(case, 0.0)

# Export Jacobian matrices (writes jac_val.dat, jac_eqs.dat, jac_var.dat, jac_struc.dat)
ram.getJac()
ram.endSim()
```

The generated files can then be analysed in MATLAB using the [RAMSES Eigenanalysis](https://github.com/SPS-L/RAMSES-Eigenanalysis) tool:

```matlab
% In MATLAB:
ssa('jac_val.dat', 'jac_eqs.dat', 'jac_var.dat', 'jac_struc.dat')
```

:::note
Set `$OMEGA_REF SYN ;` in the solver settings file when exporting Jacobians for eigenanalysis.
:::

## Nordic Test System: Generator Trip

The following example is based on the [Nordic JHub starter notebook](https://github.com/SPS-L/Nordic_JhubStart). It simulates a generator trip at t = 10 s and plots the rotor speed of the tripped machine.

```python
import pyramses
import os

# --- Configure the test case ---
case = pyramses.cfg()
case.addData('dyn_B.dat')         # dynamic model data
case.addData('volt_rat_B.dat')    # power-flow initialisation
case.addData('settings1.dat')     # solver settings
case.addDst('nothing.dst')        # no pre-defined disturbances
case.addObs('obs.dat')            # observables to record
case.addTrj('output.trj')         # trajectory output file

# --- Remove stale output files from previous runs ---
for f in os.listdir('.'):
    if f.endswith('.trj') or f.endswith('.trace'):
        os.remove(f)

# --- Run simulation ---
ram = pyramses.sim()
ram.execSim(case, 0.0)                          # initialise, paused at t = 0
ram.addDisturb(10.0, 'BREAKER SYNC_MACH g7 0')  # trip generator g7 at t = 10 s
ram.contSim(150.0)                              # simulate to t = 150 s
ram.endSim()

# --- Extract and plot results ---
ext = pyramses.extractor(case.getTrj())
ext.getSync('g7').S.plot()    # rotor speed of generator g7
```

:::note
The Nordic test system files (`dyn_B.dat`, `volt_rat_B.dat`, etc.) are available in the [Nordic_JhubStart](https://github.com/SPS-L/Nordic_JhubStart) repository.
:::

## 5-Bus System: Exciter Parameter Change

The following example is based on the [5-bus test system Case 2 notebook](https://github.com/SPS-L/5_bus_test_system). It applies a step change to the exciter voltage setpoint at t = 1 s and plots the generator active power.

```python
import pyramses
import os

# --- Configure the test case ---
case = pyramses.cfg()
case.addData('dyn.dat')           # dynamic model data
case.addData('lf1solv.dat')       # power-flow solution
case.addData('solveroptions.dat') # solver settings
case.addDst('nothing.dst')        # no pre-defined disturbances
case.addObs('obs.dat')            # observables to record
case.addTrj('output.trj')         # trajectory output file

# --- Remove stale output files from previous runs ---
for f in os.listdir('.'):
    if f.endswith('.trj') or f.endswith('.trace'):
        os.remove(f)

# --- Run simulation ---
ram = pyramses.sim()
ram.execSim(case, 0.0)                              # initialise, paused at t = 0
ram.addDisturb(1.0, 'CHGPRM EXC G Vo 0.05 2')      # step +0.05 pu on Vo of exciter G at t = 1 s
ram.contSim(60.0)                                   # simulate to t = 60 s
ram.endSim()

# --- Extract and plot results ---
ext = pyramses.extractor(case.getTrj())
ext.getSync('G').P.plot()     # active power of generator G
ext.getSync('G').Q.plot()     # reactive power of generator G
```

:::note
The 5-bus test system files are available in the [5_bus_test_system](https://github.com/SPS-L/5_bus_test_system) repository.
:::
