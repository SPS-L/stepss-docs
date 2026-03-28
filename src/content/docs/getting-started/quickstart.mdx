---
title: Quick Start
description: Run your first STEPSS simulation
---

import { Tabs, TabItem, Steps } from '@astrojs/starlight/components';

This guide walks through running a basic power system simulation using either the STEPSS GUI or PyRAMSES.

<Tabs>
<TabItem label="GUI">

<Steps>

1. **Launch STEPSS** by double-clicking `stepss.jar`
2. **Load a test case**: Use File → Open to load your data files
3. **Run Power Flow**: Execute PFC to compute the initial operating point
4. **Configure Simulation**: Set solver parameters and define disturbances
5. **Run Dynamic Simulation**: Execute RAMSES and observe results
6. **Analyze Results**: Use the built-in plotting tools to visualize voltage, frequency, and power traces

</Steps>

For detailed GUI usage, visit the [STEPSS website](https://sps-lab.org/project/stepss/).

</TabItem>
<TabItem label="Python (PyRAMSES)">

<Steps>

1. **Install PyRAMSES**:
   ```bash
   pip install pyramses
   ```

2. **Create a command file** (`cmd.txt`):
   ```
   data.dat
   
   init.trace
   dst.dst
   result.rtrj
   obs.obs
   cont.trace
   disc.trace
   ```

3. **Run a simulation**:
   ```python
   import pyramses
   
   # Initialize simulator
   ram = pyramses.sim()
   
   # Load test case from command file
   case = pyramses.cfg("cmd.txt")
   
   # Run full simulation
   ram.execSim(case)
   ```

4. **Extract and plot results**:
   ```python
   # Extract trajectory data
   ext = pyramses.extractor(case.getTrj())
   
   # Plot bus voltage magnitude
   ext.getBus('1041').mag.plot()
   
   # Plot synchronous machine speed
   ext.getSync('g1').speed.plot()
   ```

</Steps>

</TabItem>
<TabItem label="CLI">

<Steps>

1. **Prepare data files**: Create network data, dynamic data, disturbance, and solver settings files

2. **Run simulation via RAMSES executable**:
   ```bash
   dynsim.exe cmd.txt
   ```

3. **Process results** using MATLAB, Python, or other tools

</Steps>

</TabItem>
</Tabs>

## Command File Structure

The command file (`cmd.txt`) lists the input files for a simulation, separated by blank lines:

```
datafile1.dat        # Network + dynamic data files
datafile2.dat        # (one or more)

init.trace           # Initialization output (optional)
disturbance.dst      # Disturbance scenario
result.rtrj          # Trajectory output (optional)
obs.obs              # Observables definition (required if trajectory given)
cont.trace           # Continuous trace output (optional)
disc.trace           # Discrete trace output (optional)
```

Records can be distributed across an arbitrary number of data files, read sequentially. The order of records and files does not matter.

## Typical Workflow

1. **Define the network**: Specify buses, lines, transformers, and shunts
2. **Set up power flow data**: Define generators, loads, and the slack bus
3. **Add dynamic models**: Specify synchronous machines, excitation systems, speed governors, loads, and controllers
4. **Configure solver**: Set integration method, time steps, and tolerances
5. **Define disturbances**: Specify faults, line trips, parameter changes, etc.
6. **Run simulation**: Execute PFC for initialization, then RAMSES for dynamics
7. **Analyze results**: Extract and visualize trajectories of voltages, frequencies, and powers

## Next Steps

- [File Formats](/stepss-docs/user-guide/file-formats/) — Learn about data file syntax
- [Network Modeling](/stepss-docs/user-guide/network/) — Define your power system network
- [Dynamic Models](/stepss-docs/user-guide/dynamic-models/) — Add generators, loads, and controllers
- [PyRAMSES API](/stepss-docs/pyramses/api-reference/) — Full Python API documentation
