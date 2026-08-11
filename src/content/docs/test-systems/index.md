---
title: Test Systems
description: The four benchmark networks distributed for STEPSS, and which to pick
---

Four benchmark networks ship as ready-to-run RAMSES data sets, each in its own
repository. They are ordered here from smallest to largest, which is also the
order in which they are worth meeting.

| System | Buses | Machines | Frequency | Best for |
|--------|------:|---------:|-----------|----------|
| [5-Bus](/test-systems/5bus/) | 5 | 1 | 50 Hz | Learning the tools |
| [Kundur Two-Area](/test-systems/kundur/) | 11 | 4 | 60 Hz | Inter-area oscillations, PSS tuning |
| [Nordic](/test-systems/nordic/) | 74 | 20 | 50 Hz | Long-term voltage stability |
| [GB Network](/test-systems/gb-network/) | 87 | 37 | 50 Hz | HVDC, wide-area monitoring |

## Which One to Start With

- **New to STEPSS**: the [5-bus system](/test-systems/5bus/) is small enough to
  trace every computation by hand while still exercising the whole workflow, from
  power flow through disturbance to trajectory extraction.
- **Small-signal and damping studies**: the
  [Kundur two-area system](/test-systems/kundur/) ships two dynamic data variants,
  with and without PSS, so the inter-area mode can be compared directly. Pair it
  with [Eigenanalysis](/user-guide/eigenanalysis/).
- **Voltage stability and long-term dynamics**: the
  [Nordic system](/test-systems/nordic/) is the IEEE PES-TR19 benchmark, with
  several operating points and a Jupyter tutorial that walks through a voltage
  collapse.
- **Converter-dominated and HVDC studies**: the
  [GB network](/test-systems/gb-network/) models its interconnections as two-port
  converters and carries ready-made disturbance templates.

## Running Any of Them

All four follow the same pattern: clone the repository, then point a stepss
`cfg` at its data files.

```python
import stepss

case = stepss.cfg()
case.addData('dyn.dat')            # dynamic data
case.addData('lf.dat')             # power-flow solution
case.addData('solveroptions.dat')  # solver settings
case.addDst('disturb.dst')         # disturbance scenario
case.addObs('obs.dat')             # observables to record

sim = stepss.sim()
sim.execSim(case)
```

The exact file names differ per system; each page lists them. See
[Python API Examples](/python/examples/) for complete worked scripts, and
[Installation](/python/installation/) if stepss is not set up yet.

## Next Steps

- [Python API Examples](/python/examples/), full simulation workflows
- [Disturbances](/user-guide/disturbances/), write your own scenarios
- [Model Reference](/models/), the models these systems use
