---
title: Kundur Two-Area System
description: The classic Kundur two-area four-machine test system for small-signal and transient stability studies
---

The Kundur two-area system is the standard benchmark for inter-area oscillation studies: two symmetric areas connected by a weak tie, each with two 900 MVA synchronous generators (11 buses, 4 machines, 60 Hz). The RAMSES implementation uses the Kundur-book machine models with `exc_kundur` AVR/PSS and thermal governors, and ships two dynamic data variants, with and without power system stabilizers, so the damping of the inter-area mode can be compared directly.

**Repository:** [SPS-L/stepss-Kundur-Two-Area-System](https://github.com/SPS-L/stepss-Kundur-Two-Area-System)

---

## Quick Start

```python
import pyramses

case = pyramses.cfg()
case.addData('lf.dat')            # power-flow data
case.addData('dyn.dat')           # dynamic data (use dyn_noPSS.dat for the no-PSS variant)
case.addData('solveroptions.dat') # solver settings
case.addDst('disturb.dst')        # +0.5 pu load step on L9 at t = 1 s, 60 s horizon
case.addObs('obs.dat')            # observables to record

sim = pyramses.sim()
sim.execSim(case)
```

Running the same disturbance with `dyn.dat` and `dyn_noPSS.dat` (PSS gain set to zero) demonstrates the poorly damped inter-area oscillation and its stabilization by the PSS.

---

## Download

The test system files are available in the [stepss-Kundur-Two-Area-System repository](https://github.com/SPS-L/stepss-Kundur-Two-Area-System).

## Citation

If you use this test system in your research, please cite the original source of the system data:

> P. Kundur, *Power System Stability and Control*, McGraw-Hill, 1994 (two-area system, Example 12.6).
