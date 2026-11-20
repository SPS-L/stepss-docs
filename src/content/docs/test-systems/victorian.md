---
title: Victorian Transmission System
description: Dynamic model of the Victorian (Australia) transmission system for fast frequency response studies, with scripts that generate operating points
---

The Victorian Transmission System is a 50 Hz model of the transmission grid of Victoria, Australia, with 125 buses from 500 kV down to generator terminals, 11 synchronous generating units (8 thermal on `TGOV1` governors, 3 hydro on `HYGOV`, each with an `ENTSOE_simp` or `ST1A` exciter), the interconnectors to New South Wales and South Australia modelled as synchronous machines, and 23 wind and solar plants on the `WT4` converter model. It was built by J. Vorwerk to study fast frequency response in a system with high renewable and electrified-heat shares. Beside one ready-to-run operating point, it carries the scripts and scenario data that generate the power flow and dynamic data for any half-hour of five study days at three levels of heating electrification.

**Repository:** [SPS-L/stepss-VICSystem](https://github.com/SPS-L/stepss-VICSystem), a fork of the author's [JohannaVorwerk/VICSystem](https://github.com/JohannaVorwerk/VICSystem) carrying the changes it needs to run with current STEPSS.

---

## Quick Start

```python
import stepss

case = stepss.cfg()
case.addData('pyRdat_ss.dat')      # network and power-flow solution
case.addData('pyRdat_dyn.dat')     # machines, exciters, governors, WT4 plants
case.addData('SOLVEROPTIONS.dat')  # solver settings
case.addDst('trip_SM35G1.dst')     # loss of a 500 MW unit at t = 0.5 s, 20 s horizon
case.addObs('obs.dat')             # observables to record

sim = stepss.sim()
sim.execSim(case)
```

`nothing.dst` runs the same 20 s with no disturbance, and `VICSystem.cfg` opens the trip in the STEPSS desktop application. `TNSingleSim.py` runs the full example study: it trips the unit, plots generator, reserve and wind-farm responses, and estimates the kinetic energy supplied by generators and interconnectors.

## Other Operating Points

The shipped data is one half-hour of one study day. `GenerateOPs/TNLoadFlow.py` solves the power flow of every half-hour of a chosen day and electrification level with Helios, and `GenerateOPs/TNDynamicData.py` turns one of those solutions into the two data files above. Both are run from inside `GenerateOPs/`; the repository README lists the days, levels and steps.

---

## Download

The test system files are available in the [stepss-VICSystem repository](https://github.com/SPS-L/stepss-VICSystem).

## Citation

If you use this test system in your research, please cite the publications it was developed for:

> J. Vorwerk, *Integration of Fast Demand Response into Renewable Power Systems*, PhD thesis, ETH Zurich, [doi:10.3929/ethz-b-000643071](https://doi.org/10.3929/ethz-b-000643071).

> J. Vorwerk, I. Saedi, P. Mancarella, G. Hug, "Electrifying thermal loads vs. installing batteries: A case study on fast frequency resource potentials of the Victorian power system", *Electric Power Systems Research*, vol. 235, 110622, 2024, [doi:10.1016/j.epsr.2024.110622](https://doi.org/10.1016/j.epsr.2024.110622).

## See Also

- [Test Systems](/test-systems/), the other benchmark networks
- [Static Exciters](/models/exciters/ieee-st/#entsoe_simp), the `ENTSOE_simp` and `ST1A` exciters used here
- [IEEE Governors](/models/governors/ieee/#tgov1-tor_tgov1d), the `TGOV1` and `HYGOV` governors
- [WECC Models](/models/injectors/wecc/#wt4-inj_wt4-type-4-wind-turbine-full-converter), the `WT4` converter plants
- [Power Flow](/user-guide/power-flow/), the Helios input format the operating-point scripts write
