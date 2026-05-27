---
title: 5-Bus Test System
description: A small 5-bus test system for learning PyRAMSES and power system dynamics
---

The 5-bus test system is a minimal power system suitable for learning PyRAMSES and experimenting with dynamic simulation concepts. It is small enough to trace every computation step while still demonstrating the full simulation workflow.

**Repository:** [SPS-L/5_bus_test_system](https://github.com/SPS-L/5_bus_test_system)

---

## Quick Start

```python
import pyramses
import os

# Configure the test case
case = pyramses.cfg()
case.addData('dyn.dat')           # dynamic model data
case.addData('lf1solv.dat')       # power-flow solution
case.addData('solveroptions.dat') # solver settings
case.addDst('nothing.dst')        # no pre-defined disturbances
case.addObs('obs.dat')            # observables to record
case.addTrj('output.trj')        # trajectory output file

# Remove stale output files from previous runs
for f in os.listdir('.'):
    if f.endswith('.trj') or f.endswith('.trace'):
        os.remove(f)

# Run simulation with exciter setpoint change
ram = pyramses.sim()
ram.execSim(case, 0.0)
ram.addDisturb(1.0, 'CHGPRM EXC G Vo 0.05 2')  # +0.05 pu step on Vo at t=1 s
ram.contSim(60.0)
ram.endSim()

# Extract and plot results
ext = pyramses.extractor(case.getTrj())
ext.getSync('G').P.plot()     # active power
ext.getSync('G').Q.plot()     # reactive power
```

---

## Download

The test system files are available in the [5_bus_test_system repository](https://github.com/SPS-L/5_bus_test_system).

## See Also

- [PyRAMSES Examples](/pyramses/examples/#5-bus-system-exciter-parameter-change) — Complete Python simulation workflow with this test system
