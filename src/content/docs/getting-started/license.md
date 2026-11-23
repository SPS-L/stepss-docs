---
title: License
description: Licensing information for the STEPSS suite
---

STEPSS is not under one license. The interfaces and tools are open source. The three engines, Helios, RAMSES and CODEGEN, are free of charge for non-commercial use and need a license for anything commercial.

## Component Licenses

**Open-source components**

| Component | License | Repository |
|-----------|---------|------------|
| STEPSS GUI | Apache License 2.0 | [SPS-L/stepss-java-ui](https://github.com/SPS-L/stepss-java-ui) |
| stepss | Apache License 2.0 | [SPS-L/stepss-python-ui](https://github.com/SPS-L/stepss-python-ui) |
| URAMSES | Apache License 2.0 | [SPS-L/stepss-uramses](https://github.com/SPS-L/stepss-uramses) |
| stepss-eigenanalysis | Apache License 2.0 | [SPS-L/stepss-eigenanalysis](https://github.com/SPS-L/stepss-eigenanalysis) |
| CODEGEN Studio | Apache License 2.0 | [SPS-L/stepss-cg-studio](https://github.com/SPS-L/stepss-cg-studio) |
| stepss-dyngraph | Apache License 2.0 | SPS-L/stepss-dyngraph (private) |
| RamsesNN | MIT License | [SPS-L/stepss-RamsesNN](https://github.com/SPS-L/stepss-RamsesNN) |

**Engines**

| Engine | Role | Owner | License |
|--------|------|-------|---------|
| Helios | Power flow | Dr. Petros Aristidou | [STEPSS-Helios Academic Public License](#helios-license) |
| RAMSES | Dynamic simulation | University of Liège, Belgium | [Proprietary](#ramses-solver-license) |
| CODEGEN | Model generator | Dr. Thierry Van Cutsem | [Academic Public License for the use of STEPSS](#codegen-license) |

An open-source license covers the code written in that repository, not an engine shipped alongside it. See [Packages That Bundle an Engine](#packages-that-bundle-an-engine).

## Engine Licenses

The three engines share these terms:

- **Non-commercial use is free of charge.** This covers teaching and research at universities, colleges and other educational institutions, research at non-profit research institutions, and personal non-profit purposes.
- **Commercial use needs a license.** This includes, but is not restricted to, consulting activities, the design of commercial hardware or software products, and participation by a commercial entity in research projects. See [Requesting a Commercial License](#requesting-a-commercial-license).
- **No warranty.** Each engine is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement.

What follows is specific to each engine.

### RAMSES Solver License

RAMSES, the solver of differential-algebraic equations, is the property of the University of Liège, which has granted to both [Authors](#authors) a personal, royalty-free, limited, non-exclusive, non-transferable and non-assignable license to distribute an executable version of it free of charge.

The free-of-charge version is limited to:

- power system models of up to **1000 buses** (or nodes);
- execution with parallelization on no more than **2 cores**.

For larger models or execution on more than two cores, contact the Authors.

### Helios License

STEPSS-Helios is distributed under the STEPSS-Helios Academic Public License. Its license sets no limit on system size or number of cores.

### CODEGEN License

CODEGEN is distributed under the Academic Public License for the use of STEPSS, as a compiled executable only. Its source code is not in any of the public STEPSS repositories.

## Packages That Bundle an Engine

Some open-source components ship engine executables. Installing one means accepting the terms of each engine it carries.

| Package | Engines it carries |
|---------|--------------------|
| STEPSS GUI | Helios, RAMSES and CODEGEN |
| `stepss` (PyPI) | RAMSES and Helios |
| CODEGEN Studio (PyPI, `stepss-cg-studio`) | CODEGEN |

The CODEGEN Studio wheel bundles the CODEGEN executables for Linux, Windows and macOS so that its Run Codegen action works on a fresh install. The license text ships inside the wheel as `cg_studio/bin/LICENSE-CODEGEN`, and the two leading components of the package's version name the CODEGEN release it carries: every `stepss-cg-studio` X.Y.z runs CODEGEN X.Y.

## Requesting a Commercial License

Which license, and from whom, depends on which engines you use, since they have different owners. A use that involves one engine is a narrower question than one that involves all three.

Write to **stepss@sps-lab.org**. The Helios license text names info@sps-lab.org for a request that concerns Helios alone.

A first message that covers the following can be answered without a round of questions first:

- **Which engines** the work needs. If you are unsure, describe what you want to do.
- **What the use is**: consulting for a client, a product you sell, an internal tool, or a funded project with a commercial partner.
- **How large the systems are** and **how many cores** you need to run on. The limits of the free RAMSES are usually the reason for the request.
- **Your timeframe.**
- **The organisation** the license would be granted to, which is not always the one asking.

## Documentation License

The STEPSS documentation, this website and the PDF user guide, is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). You may share and adapt it, including for commercial purposes, provided you give appropriate credit.

This applies to the documentation only. It grants no rights over the STEPSS software.

## Authors

STEPSS has been developed by:

- **Dr. Petros Aristidou** (petros.aristidou@cut.ac.cy)
- **Dr. Thierry Van Cutsem** (thierry.h.van.cutsem@gmail.com)

For general inquiries, use **stepss@sps-lab.org**.
