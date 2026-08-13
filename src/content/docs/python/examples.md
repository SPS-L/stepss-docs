---
title: Examples
description: Practical examples using stepss
---

All examples assume the working directory contains the relevant data and disturbance files.

## Running a Basic Simulation

Define the test case, run the simulation, and extract results:

```python
import stepss

case = stepss.cfg()
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

ram = stepss.sim()
ram.execSim(case)                # run to completion

ext = stepss.extractor(case.getTrj())
ext.getBus('1041').mag.plot()    # voltage magnitude at bus 1041
```

:::note
Set `$NB_THREADS 0 ;` in the solver settings file to use all available CPU cores for parallel simulation.
:::

## Pause and Continue

Pause the simulation at intermediate time points to inspect state or add disturbances:

```python
ram = stepss.sim()
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
phases   = ram.getBusPha(busNames)    # list of phase angles (deg)

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

For full disturbance syntax, see the [Disturbances reference](/user-guide/disturbances/).

## Plotting Results

Extract and plot time-series results after the simulation:

```python
import stepss
ext = stepss.extractor('output.trj')

# Single curve
ext.getSync('g5').S.plot()       # rotor speed of generator g5
ext.getBus('4044').mag.plot()    # voltage magnitude at bus 4044

# Multiple curves on the same plot
curves = [ext.getSync(f'g{i}').S for i in range(1, 5)]
stepss.curplot(curves)

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
import stepss
import numpy as np

results = {}
for disturbance_time in [5.0, 10.0, 20.0]:
    case = stepss.cfg('cmd.txt')
    trj_file = f'output_{disturbance_time:.0f}.trj'
    case.addTrj(trj_file)
    case.addObs('obs.dat')

    ram = stepss.sim()
    ram.execSim(case, 0.0)
    ram.addDisturb(disturbance_time, 'BREAKER SYNC_MACH g7 0')
    ram.contSim(ram.getInfTime())
    ram.endSim()

    ext = stepss.extractor(trj_file)
    min_freq = np.min(ext.getSync('g5').S.value)
    results[disturbance_time] = min_freq
    print(f't_dist={disturbance_time:5.1f}s  min_speed={min_freq:.5f} pu')
```

## Eigenanalysis Workflow

RAMSES performs the small-signal analysis itself. Schedule an `EIG` event at the
operating point and it writes the modes, participation factors and mode shapes:

```python
import stepss

case = stepss.cfg('cmd.txt')
ram = stepss.sim()

ram.execSim(case, 0.0)               # pause at the steady-state operating point
ram.addDisturb(0.001, "EIG 'ssa'")   # writes ssa_modes.dat, ssa_pf.dat, ssa_ms.dat
ram.contSim(0.01)                    # advance past the event so it fires
ram.endSim()
```

Reading the result needs nothing beyond numpy:

```python
import numpy as np

m = np.loadtxt('ssa_modes.dat', comments='#')
freq, zeta = m[:, 4], m[:, 3]

interarea = m[(freq > 0.4) & (freq < 0.9) & (m[:, 2] > 0)]
print('inter-area mode: %.4f Hz, zeta = %+.4f' % (interarea[0, 4], interarea[0, 3]))
```

A complete annotated walkthrough ships with the package under
`examples/eigenanalysis/`.

**To drive your own solver instead**, `getJac()` returns the descriptor-form pair
as SciPy sparse matrices. This is the route for systems above `$EIG_MAX_STATES`,
where the engine's dense solve is not practical and sparse shift-invert methods
are needed:

```python
ram.execSim(case, 0.0)
A, E = ram.getJac()   # scipy.sparse.csc_matrix
ram.endSim()
```

:::note
Both routes need `$OMEGA_REF SYN ;` and `$SCHEME DE ;` in the solver settings.
`EIG` refuses without them, exiting 78 with the reason in the log; the `JAC`
export skips with a warning under COI. See
[Eigenanalysis](/user-guide/eigenanalysis/).
:::

## Test System Examples

The following examples use the ready-to-run test systems. For system descriptions, data files, and disturbance scenarios, see the [Test Systems](/test-systems/) section.

### Nordic Test System: Generator Trip

Trips generator g7 at $t = 10$ s on the heavily-stressed Operating Point B and observes the voltage collapse dynamics over 150 seconds. See the [Nordic Test System](/test-systems/nordic/) page for full system details and file descriptions.

```python
import stepss
import os

case = stepss.cfg()
case.addData('dyn_B.dat')
case.addData('volt_rat_B.dat')
case.addData('settings1.dat')
case.addDst('nothing.dst')
case.addObs('obs.dat')
case.addTrj('output.trj')

for f in os.listdir('.'):
    if f.endswith('.trj') or f.endswith('.trace'):
        os.remove(f)

ram = stepss.sim()
ram.execSim(case, 0.0)
ram.addDisturb(10.0, 'BREAKER SYNC_MACH g7 0')
ram.contSim(150.0)
ram.endSim()

ext = stepss.extractor(case.getTrj())
ext.getSync('g7').S.plot()    # rotor speed
ext.getBus('1041').mag.plot()  # voltage at central bus
```

### 5-Bus System: Exciter Parameter Change

Applies a step change to the exciter voltage setpoint at $t = 1$ s and plots the generator response. See the [5-Bus Test System](/test-systems/5bus/) page for details.

```python
import stepss
import os

case = stepss.cfg()
case.addData('dyn.dat')
case.addData('lf1solv.dat')
case.addData('solveroptions.dat')
case.addDst('nothing.dst')
case.addObs('obs.dat')
case.addTrj('output.trj')

for f in os.listdir('.'):
    if f.endswith('.trj') or f.endswith('.trace'):
        os.remove(f)

ram = stepss.sim()
ram.execSim(case, 0.0)
ram.addDisturb(1.0, 'CHGPRM EXC G Vo 0.05 2')
ram.contSim(60.0)
ram.endSim()

ext = stepss.extractor(case.getTrj())
ext.getSync('G').P.plot()
ext.getSync('G').Q.plot()
```
