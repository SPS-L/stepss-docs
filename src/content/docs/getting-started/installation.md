---
title: Installation
description: How to install STEPSS and its dependencies
---

import { Tabs, TabItem, Steps, Aside } from '@astrojs/starlight/components';

This guide covers the installation of STEPSS, including the Java GUI, Visual Studio, and the Intel Fortran compiler.

<Aside type="note">
The Java, Visual Studio, and OneAPI files are **not part of STEPSS**. They are provided only to ease the installation procedure.
</Aside>

All needed files can be downloaded from the [Google Drive folder](https://drive.google.com/drive/folders/1HcUSD-FOx6192HURJnxltYJuKuNA8Vwz?usp=drive_link).

## Installing Java

STEPSS comes with a Java-based Graphical User Interface (GUI) that requires **Java Version 20 (64-bit)**.

<Steps>

1. **Check existing installation**: Open a Windows Command prompt and enter:
   ```bash
   java -version
   ```

2. **Uninstall older versions** (if necessary):
   - Go to Windows Parameters → Applications
   - Locate Java and click Uninstall

3. **Install Java 20**:
   - Download `jdk-20_windows-x64_bin.exe` from the [Google Drive](https://drive.google.com/drive/folders/1HcUSD-FOx6192HURJnxltYJuKuNA8Vwz?usp=drive_link)
   - Double-click to install and follow the instructions

4. **Associate STEPSS with Java**:
   - Right-click on `stepss.jar`
   - Select "Open with" → "Always use this application"

</Steps>

## Installing STEPSS

<Steps>

1. Download `STEPSS.jar` from the [Google Drive](https://drive.google.com/drive/folders/1HcUSD-FOx6192HURJnxltYJuKuNA8Vwz?usp=drive_link)
2. Place it in any convenient location (e.g., your Desktop)
3. **Do not uncompress the archive**
4. Launch by double-clicking `STEPSS.jar`

</Steps>

When launched, STEPSS creates a temporary working folder and copies all needed executables and libraries. To remove STEPSS, simply delete the archive file — it leaves nothing on your computer.

Current version: **3.40**

## Installing Visual Studio

<Aside type="tip">
This step can be **skipped** if you do not plan to develop new models for RAMSES using CODEGEN.
</Aside>

The Intel OneAPI compiler requires **Microsoft Visual Studio Community 2022**.

<Steps>

1. Download the launcher from the [Google Drive](https://drive.google.com/drive/folders/1HcUSD-FOx6192HURJnxltYJuKuNA8Vwz?usp=drive_link):
   `vs_community__e942d3d4864d4a80b72975352289d007.exe`
2. Execute by double-clicking
3. During installation, under the "Workloads" view, select **"Desktop development with C++"**

</Steps>

## Installing the Fortran Compiler

<Aside type="tip">
This step can be **skipped** if you do not plan to develop new models for RAMSES.
</Aside>

Three packages need to be installed **in order**:

<Steps>

1. Download and install the **OneAPI BaseKit**:
   `w_BaseKit_p_2023.1.0.47256_offline.exe`

2. Download and install the **Fortran Compiler Classic** package:
   `w_ifort_runtime_p_2023.1.0.46319.exe`

3. Download and install the **HPC Toolkit**:
   `w_HPCKit_p_2023.1.0.46357_offline.exe`

4. **Restart your computer**

</Steps>

## Installing PyRAMSES

For the Python interface to RAMSES, see the [PyRAMSES Installation Guide](/stepss-docs/pyramses/installation/).
