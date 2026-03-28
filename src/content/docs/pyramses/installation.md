---
title: PyRAMSES Installation
description: Installing PyRAMSES and its dependencies
---

import { Tabs, TabItem, Steps, Aside } from '@astrojs/starlight/components';

## Installation

<Tabs>
<TabItem label="pip (Recommended)">

```bash
pip install pyramses
```

This installs PyRAMSES along with its core dependencies.

</TabItem>
<TabItem label="Full Environment">

Install PyRAMSES with all recommended packages:

```bash
pip install matplotlib scipy numpy mkl jupyter ipython pyramses
```

</TabItem>
</Tabs>

## Dependencies

PyRAMSES depends on the Intel MKL redistributable libraries for LAPACK/BLAS and OpenMP. These should be automatically installed as dependencies.

### Verifying MKL

To verify MKL is correctly installed:

```python
import numpy as np
np.__config__.show()
```

You should see output referencing `mkl_rt` in the BLAS/LAPACK configuration.

## Optional: Gnuplot for Real-Time Plots

PyRAMSES can display simulation outputs in real-time during execution. This requires [Gnuplot](http://www.gnuplot.info/) to be installed and available in the system PATH.

<Tabs>
<TabItem label="Windows">

Download and install from [gnuplot.info](http://www.gnuplot.info/). Make sure the installation directory is added to your system PATH.

</TabItem>
<TabItem label="Linux (Ubuntu/Debian)">

```bash
sudo apt-get install gnuplot-x11
```

</TabItem>
<TabItem label="Linux (Fedora/RHEL)">

```bash
sudo dnf install gnuplot
```

</TabItem>
</Tabs>

<Aside type="note">
If Gnuplot is not found, PyRAMSES will still work but runtime observable plots will be disabled.
</Aside>

## Platform Support

| Platform | Library | Notes |
|----------|---------|-------|
| **Windows** | `ramses.dll` | Primary platform, full support |
| **Linux** | `ramses.so` | Full support with gfortran/OpenBLAS |

## Custom Library Path

You can override the default library directory when creating a simulator instance:

```python
import pyramses
ram = pyramses.sim(custLibDir="/path/to/custom/libs")
```

<Aside type="caution">
The DLL in the custom location will be locked while the `pyramses.sim()` instance exists. To unlock it, delete the instance with `del(ram)` or restart the Python kernel.
</Aside>

## Version Information

```python
import pyramses
print(pyramses.__version__)  # Current version
print(pyramses.__url__)      # https://pyramses.sps-lab.org
```

## Next Steps

- [API Reference](/stepss-docs/pyramses/api-reference/) — Full API documentation
- [Examples](/stepss-docs/pyramses/examples/) — Practical usage examples
