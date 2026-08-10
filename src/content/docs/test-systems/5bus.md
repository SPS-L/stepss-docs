---
title: 5-Bus Test System
description: A small 5-bus test system for learning PyRAMSES and power system dynamics
---

The 5-bus test system is a minimal power system suitable for learning the STEPSS tools and experimenting with dynamic simulation concepts. It is small enough to trace every computation step while still demonstrating the full simulation workflow, and runs with either PyRAMSES (shown below) or the [STEPSS Java interface](https://github.com/SPS-L/stepss-java-ui).

**Repository:** [SPS-L/stepss-5-bus-test-system](https://github.com/SPS-L/stepss-5-bus-test-system)

## One-line Diagram

<img src="/images/5bus_oneline.png" alt="One-line diagram of the 5-bus test system" style="width:70%" />

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

The test system files are available in the [stepss-5-bus-test-system repository](https://github.com/SPS-L/stepss-5-bus-test-system).

## See Also

- [Test Systems](/test-systems/), the other benchmark networks
- [PyRAMSES Examples](/pyramses/examples/#5-bus-system-exciter-parameter-change), Complete Python simulation workflow with this test system
