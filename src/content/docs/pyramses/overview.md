---
title: PyRAMSES Overview
description: Python-based RApid Multithreaded Simulation of Electric power Systems
---

**PyRAMSES** (Python-based RApid Multithreaded Simulation of Electric power Systems) is a Python interface to the RAMSES dynamic simulation engine. It provides researchers, engineers, and students with an accessible and powerful tool for large-scale power system analysis.

For more information, visit the [PyRAMSES project page](https://sps-lab.org/project/pyramses/) and the [PyRAMSES documentation site](https://pyramses.sps-lab.org/).

## Key Features

### Python Integration
- Native Python interface with seamless scientific computing integration
- Jupyter Notebook support for interactive analysis
- NumPy/SciPy compatibility for numerical computing
- Simple `pip` installation

### Parallel Processing
- **Domain decomposition** using Schur-complement-based algorithms
- Multi-core optimization with OpenMP shared-memory parallelism
- Two-level partitioning for coarse- and fine-grained parallelization

### Computational Acceleration
- Localization techniques exploiting the localized response to disturbances
- Time-scale decomposition for multi-rate phenomena
- Acceleration on both single and multi-processing units

### Comprehensive Modeling
- Transmission and distribution networks
- Combined T&D systems
- AC/DC hybrid systems
- Dynamic Security Assessment (DSA)

## Built-in Models

PyRAMSES includes a comprehensive library of power system models:

| Category | Models |
|----------|--------|
| **Injectors** | `load`, `PQ`, `restld`, `indmach1`, `indmach2`, `IBG`, `WT3WithChanges`, `WT4WithChanges`, `BESSWithChanges`, `vfd_load`, `svc_hq_generic1`, `theveq` |
| **Exciters** | `ST1A`, `AC1A`, `AC4A`, `AC8B`, `DC3A`, `IEEET5`, `EXPIC1`, `EXHQSC`, `ENTSOE_simp`, `GENERIC3`, `GENERIC4`, and many variants with PSS/OEL |
| **Speed Governors** | `DEGOV1`, `hydro_generic1`, `thermal_generic1`, `HQRVC`, `HQRVM`, `HQRVN`, `HQRVW`, `ENTSOE_simp`, `ENTSOE_simp_consensus` |
| **Two-Ports** | `HQSVC`, `HVDC_LCC`, `HVDC_VSC`, `HVDC_VSC_SC`, `DC_BHPM`, `CHENIER`, `CSVGN5`, `DCL_WCL`, `vsc_hq` |
| **Discrete Controllers** | `ltc`, `ltc2`, `ltcinv`, `oltc2`, `uvls`, `uvprot`, `pst`, `rt`, `mais`, `FRT`, `sim_minmaxvolt`, `sim_minmaxspeed`, `voltage_variability` |

## Applications

- **Research**: Algorithm development, model validation, performance benchmarking
- **Real-time operations**: Dynamic Security Assessment (DSA), transfer limit determination
- **Planning**: System reinforcement evaluation, renewable integration studies
- **Education**: Operator training, simulation-based teaching

## References

- P. Aristidou, D. Fabozzi, and T. Van Cutsem, "Dynamic simulation of large-scale power systems using a parallel Schur-complement-based decomposition method," *IEEE Trans. on Parallel and Distributed Systems*, 25(10):2561–2570, 2014. doi: [10.1109/TPDS.2013.252](https://doi.org/10.1109/TPDS.2013.252)
- P. Aristidou, S. Lebeau, and T. Van Cutsem, "Power system dynamic simulations using a parallel two-level Schur-complement decomposition," *IEEE Trans. on Power Systems*, 31(5):3984–3995, 2016. doi: [10.1109/TPWRS.2015.2509023](https://doi.org/10.1109/TPWRS.2015.2509023)
- P. Aristidou and T. Van Cutsem, "A parallel processing approach to dynamic simulations of combined transmission and distribution systems," *Int. J. of Electrical Power & Energy Systems*, 72:58–65, 2015.

## Repository

Source code: [SPS-L/stepss-PyRAMSES](https://github.com/SPS-L/stepss-PyRAMSES)
