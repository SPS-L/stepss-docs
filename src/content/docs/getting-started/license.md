---
title: License
description: Licensing information for the STEPSS suite
---

## Component Licenses

| Component | License | Repository |
|-----------|---------|------------|
| STEPSS GUI | Apache License 2.0 | [SPS-L/stepss-java-ui](https://github.com/SPS-L/stepss-java-ui) |
| stepss | Apache License 2.0 | [SPS-L/stepss-python-ui](https://github.com/SPS-L/stepss-python-ui) |
| URAMSES | Apache License 2.0 | [SPS-L/stepss-uramses](https://github.com/SPS-L/stepss-uramses) |
| stepss-eigenanalysis | Apache License 2.0 | [SPS-L/stepss-eigenanalysis](https://github.com/SPS-L/stepss-eigenanalysis) |
| CODEGEN Studio | Apache License 2.0 | [SPS-L/stepss-cg-studio](https://github.com/SPS-L/stepss-cg-studio) |
| stepss-dyngraph | Apache License 2.0 | SPS-L/stepss-dyngraph (private) |
| RamsesNN | MIT License | [SPS-L/stepss-RamsesNN](https://github.com/SPS-L/stepss-RamsesNN) |
| Helios | Academic Public License (free for non-commercial use), with a commercial option | See [Helios License](#helios-license) below |
| RAMSES | Proprietary, free for non-commercial use | See [RAMSES Solver License](#ramses-solver-license) below |
| CODEGEN | Proprietary, free executables (Academic Public License) | See [CODEGEN License](#codegen-license) below |

## Documentation License

The STEPSS **documentation**, this website and the PDF user guide, is licensed
under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
You may share and adapt it, including for commercial purposes, provided you give
appropriate credit.

This applies to the documentation only. It grants **no rights over the STEPSS
software itself**, which remains under the terms set out below.

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

## Helios License

**STEPSS-Helios** (the modern power-flow engine, also bundled as `libhelios_api` in stepss) is the property of **Dr. Petros Aristidou**, and is distributed under the **STEPSS-Helios Academic Public License**:

- Permission is granted to use Helios **free of charge** for any **non-commercial purpose**, including teaching and research at universities, colleges, and other educational institutions, research at non-profit research institutions, and personal non-profit purposes.
- For **commercial use**, a commercial license is required: contact **info@sps-lab.org**.
- Helios is provided **"as is"**, without warranty of any kind.

## CODEGEN License

**CODEGEN** (the model generator) is the property of **Dr. Thierry Van Cutsem**. It is distributed under the **Academic Public License for the use of STEPSS** as a compiled executable that is **free to use for non-commercial purposes**; commercial use requires contacting the Authors. It is not open-source: its source code is not included in any of the public STEPSS repositories.

## Authors

STEPSS has been developed by:
- **Dr. Petros Aristidou** (petros.aristidou@cut.ac.cy)
- **Dr. Thierry Van Cutsem** (thierry.h.van.cutsem@gmail.com)

For general inquiries, licensing questions, and commercial use, please use the default contact: **stepss@sps-lab.org**.

## Intellectual Property Rights

STEPSS is made up of three modules: **Helios** (power flow computations), **RAMSES** (the solver of differential-algebraic equations), and **CODEGEN** (a tool to develop models).

Helios is the property of Dr. Petros Aristidou. CODEGEN is the property of Dr. Thierry Van Cutsem, distributed as a compiled executable free to use. RAMSES is the property of the **University of Liège, Belgium**, which has granted to both Authors a personal, royalty-free, limited, non-exclusive, non-transferable and non-assignable license to distribute free of charge an executable version of RAMSES.
