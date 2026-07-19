---
title: GB Network
description: Reduced Great Britain transmission system with HVDC-LCC links for dynamic simulation and wide-area monitoring studies
---

The GB Network is a 50 Hz reduced-order representation of the Great Britain transmission grid with 87 buses and 37 synchronous machines (thermal and CCGT units with AVR/PSS and governor models), shunt compensation, and HVDC interconnections modelled as two-port converter injectors. It is used for dynamic simulation and wide-area monitoring/control studies; a one-line diagram is included in the repository.

**Repository:** [SPS-L/stepss-GB-Network](https://github.com/SPS-L/stepss-GB-Network)

## One-line Diagram

<img src="/images/gb_oneline.png" alt="One-line diagram of the GB network with HVDC-LCC links" style="width:80%" />

---

## Quick Start

```python
import pyramses

case = pyramses.cfg()
case.addData('GBdyn.dat')      # dynamic data: machines, exciters/PSS, governors, loads
case.addData('GBhvdc.txt')     # HVDC interconnection two-port models
case.addData('GBvoltrat.dat')  # power-flow solution
case.addData('settings.dat')   # solver settings
case.addDst('disturb.dst')     # 180 s run with commented disturbance templates
case.addObs('obs.dat')         # observables to record

sim = pyramses.sim()
sim.execSim(case)
```

The disturbance file contains ready-made (commented) templates for line and machine trips, bus faults, and HVDC parameter changes — uncomment and adapt them as needed. Alternatively, run the RAMSES executable directly with the included `cmd.txt`.

---

## Download

The test system files are available in the [stepss-GB-Network repository](https://github.com/SPS-L/stepss-GB-Network).
