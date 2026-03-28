---
title: License
description: Licensing information for the STEPSS suite
---

## Component Licenses

| Component | License | Repository |
|-----------|---------|------------|
| STEPSS GUI | Apache License 2.0 | [SPS-L/STEPSS](https://github.com/SPS-L/STEPSS) |
| PyRAMSES | Apache License 2.0 | [SPS-L/stepss-PyRAMSES](https://github.com/SPS-L/stepss-PyRAMSES) |
| URAMSES | Apache License 2.0 | [SPS-L/stepss-URAMSES](https://github.com/SPS-L/stepss-URAMSES) |
| RAMSES-Eigenanalysis | Apache License 2.0 | [SPS-L/RAMSES-Eigenanalysis](https://github.com/SPS-L/RAMSES-Eigenanalysis) |
| RAMSES | Proprietary — free for non-commercial use | See [RAMSES Solver License](#ramses-solver-license) below |
| PFC | Proprietary — free to use (compiled executable) | See [PFC and CODEGEN License](#pfc-and-codegen-license) below |
| CODEGEN | Proprietary — free to use (compiled executable) | See [PFC and CODEGEN License](#pfc-and-codegen-license) below |

## RAMSES Solver License

**The RAMSES dynamic simulator (the solver of differential-algebraic equations) is NOT covered by the Apache License 2.0.** RAMSES is the property of the **University of Liège, Belgium**, and is distributed under a separate proprietary license with the following terms:

- Permission is granted to use RAMSES **free of charge** for any **non-commercial purpose**, including:
  - Teaching and research at universities, colleges, and other educational institutions
  - Research at non-profit research institutions
  - Personal non-profit purposes

- For **commercial use** of RAMSES (including but not restricted to consulting activities, design of commercial hardware or software products, or participation by a commercial entity in research projects), you must contact the Authors for an appropriate license.

- The free-of-charge version of RAMSES is limited to:
  - Power system models of up to **1000 buses** (or nodes)
  - Execution with parallelization using no more than **2 cores**

- RAMSES is provided **"as is"**, without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement.

For extensions to larger models or execution using more than two cores, contact the Authors.

## PFC and CODEGEN License

**PFC** (power flow computation) and **CODEGEN** (model generator) are the property of **Dr. Thierry Van Cutsem**. They are distributed as compiled executables that are **free to use** but are not open-source. Their source code is not included in any of the STEPSS repositories.

## Authors

STEPSS has been developed by:
- **Dr. Petros Aristidou** (petros.aristidou@cut.ac.cy)
- **Dr. Thierry Van Cutsem** (thierry.h.van.cutsem@gmail.com)

## Intellectual Property Rights

STEPSS is made up of three modules: **PFC** (power flow computations), **RAMSES** (the solver of differential-algebraic equations), and **CODEGEN** (a tool to develop models).

PFC and CODEGEN are the property of Dr. Thierry Van Cutsem, distributed as compiled executables free to use. RAMSES is the property of the **University of Liège, Belgium**, which has granted to both Authors a personal, royalty-free, limited, non-exclusive, non-transferable and non-assignable license to distribute free of charge an executable version of RAMSES.
