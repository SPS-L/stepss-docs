---
title: Induction Machines
description: Single-cage and double-cage induction machine injector models in RAMSES
---

Injector models for induction machines, used as motors or generators.

The `INJEC` record these models are entered with, and the rules on model names, are on the [Injector Models](/models/injectors/) page.

## INDMACH1 (`inj_indmach1`): Single-Cage Induction Machine

### Description

A single-cage (single-rotor-circuit) induction machine model for motor loads. The machine is represented on its own MVA base (or inferred from load factor `LF`) with a shunt capacitor $B_{\mathrm{sh}}$ to represent power factor correction. The mechanical torque is a quadratic function of rotor speed. At initialization, the model solves nonlinear algebraic equations to find the operating-point slip and flux linkages.

<img src="/images/models/inj-indmach1-light.svg"
     alt="Single-cage induction machine block diagram. The terminal voltage drives the stator equations to give the machine currents, which with the rotor flux linkages give the electromagnetic torque. The load torque, a quadratic function of rotor speed, is subtracted and the difference is integrated through twice the inertia constant to give the rotor speed, which returns both to the load torque and to the rotor circuit as slip against the network frame."
     class="dark:sl-hidden" />
<img src="/images/models/inj-indmach1-dark.svg"
     alt="Single-cage induction machine block diagram. The terminal voltage drives the stator equations to give the machine currents, which with the rotor flux linkages give the electromagnetic torque. The load torque, a quadratic function of rotor speed, is subtracted and the difference is integrated through twice the inertia constant to give the rotor speed, which returns both to the load torque and to the rotor circuit as slip against the network frame."
     class="light:sl-hidden" />

### Scientific Description

The machine uses the standard $d$-$q$ reference-frame formulation with $L_{ss} = L_{sr} + L_{ls}$ and $L_{rr} = L_{sr} + L_{lr}$. The rotor flux-linkage equations are:

$$\frac{d\psi_{dr}}{dt} = \omega_0\left(-\frac{R_r}{L_{rr}}\psi_{dr} + \frac{L_{sr} R_r}{L_{rr}} i_{ym} - (\omega - \omega_m)\psi_{qr}\right)$$

$$\frac{d\psi_{qr}}{dt} = \omega_0\left(-\frac{R_r}{L_{rr}}\psi_{qr} + \frac{L_{sr} R_r}{L_{rr}} i_{xm} + (\omega - \omega_m)\psi_{dr}\right)$$

where $\omega_0 = 2\pi f_{\mathrm{nom}}$ and $\omega_m$ is the rotor mechanical speed. The equations for the stator (with shunt susceptance $B_{\mathrm{sh}}$) are:

$$R_s i_{ym} + \left(L_{ss} - \frac{L_{sr}^2}{L_{rr}}\right)\omega\, i_{xm} + \frac{L_{sr}}{L_{rr}}\omega\,\psi_{qr} = v_y$$

$$R_s i_{xm} - \left(L_{ss} - \frac{L_{sr}^2}{L_{rr}}\right)\omega\, i_{ym} - \frac{L_{sr}}{L_{rr}}\omega\,\psi_{dr} = v_x$$

The rotor speed dynamics follow the swing equation:

$$\frac{d\omega_m}{dt} = \frac{T_e - T_m}{2H}$$

where the electromagnetic torque is:

$$T_e = \frac{L_{sr}}{L_{rr}}\left(-\psi_{dr} i_{xm} + \psi_{qr} i_{ym}\right)$$

and the mechanical torque is the quadratic load curve:

$$T_m = T_{m0}\left(A\,\omega_m^2 + B\,\omega_m + 1 - A - B\right)$$

### Parameters

| # | Name | Description | Unit |
|---|------|-------------|------|
| 1 | `SNOM` | Machine nominal apparent power (0 = infer from `LF`) | MVA |
| 2 | `RS` | Stator resistance | pu |
| 3 | `Lls` | Stator leakage inductance | pu |
| 4 | `LSR` | Magnetizing inductance | pu |
| 5 | `RR` | Rotor resistance | pu |
| 6 | `Llr` | Rotor leakage inductance | pu |
| 7 | `H` | Machine inertia constant | s |
| 8 | `A` | Quadratic torque-speed coefficient | |
| 9 | `B` | Linear torque-speed coefficient | |
| 10 | `LF` | Load factor (for SNOM inference) | |

### State Variables

| Variable | Description |
|----------|-------------|
| `iy` | $y$-component of stator current | pu |
| `ix` | $x$-component of stator current | pu |
| `psidr` | $d$-axis rotor flux linkage | pu |
| `psiqr` | $q$-axis rotor flux linkage | pu |
| `omegam` | Rotor mechanical speed | pu |

**Observables:** `P`, `Qmot+comp`, `Qmot`, `omega`, `Tm`

### Usage Example

<details>
<summary>Show the data record</summary>

```
INJEC  INDMACH1  MTR1  BUS_MV
      # FP FQ P Q: share of the power-flow injection (FP, FQ) or initial power (P in MW, Q in Mvar)
      1.  1.  0.  0.
      # SNOM: Machine nominal apparent power, 0 = infer from LF (MVA)
      10.0
      # RS: Stator resistance (pu (machine base))
      0.01
      # Lls: Stator leakage inductance (pu (machine base))
      0.10
      # LSR: Magnetizing inductance (pu (machine base))
      2.50
      # RR: Rotor resistance (pu (machine base))
      0.015
      # Llr: Rotor leakage inductance (pu (machine base))
      0.10
      # H: Inertia constant (s)
      1.5
      # A: Quadratic coefficient of load torque vs speed
      0.8
      # B: Linear coefficient of load torque vs speed
      0.1
      # LF: Load factor, initial P over SNOM, used only when SNOM = 0
      0.0
;
```

</details>

---

## INDMACH2 (`inj_indmach2`): Double-Cage Induction Machine

### Description

A double-cage (double-rotor-circuit) induction machine model following the Eurostag formulation. Two parallel rotor cages allow more accurate representation of the machine's impedance-vs-frequency characteristic, which is especially important for the starting transient. The model structure mirrors `inj_indmach1` but includes a second set of rotor flux states.

<img src="/images/models/inj-indmach2-light.svg"
     alt="Double-cage induction machine block diagram. The structure is that of INDMACH1 with the rotor doubled: the stator equations give the machine currents, two rotor cages carry their own flux linkages, and the electromagnetic torque sums a contribution from each. The load torque is subtracted and the difference integrated through twice the inertia constant to give the rotor speed, which returns to the load torque and to both cages as slip."
     class="dark:sl-hidden" />
<img src="/images/models/inj-indmach2-dark.svg"
     alt="Double-cage induction machine block diagram. The structure is that of INDMACH1 with the rotor doubled: the stator equations give the machine currents, two rotor cages carry their own flux linkages, and the electromagnetic torque sums a contribution from each. The load torque is subtracted and the difference integrated through twice the inertia constant to give the rotor speed, which returns to the load torque and to both cages as slip."
     class="light:sl-hidden" />

### Scientific Description

The machine has parameters: stator resistance $R_1$, stator leakage $L_1$, magnetizing inductance $L_m$, cage-1 resistance $R_2$ and leakage $L_2$, cage-2 resistance $R_3$ and leakage $L_3$. The state vector is $(\psi_{dr1},\psi_{qr1},\psi_{dr2},\psi_{qr2},\omega_m)$ with flux-linkage equations for each cage:

$$\frac{d\psi_{dr1}}{dt} = \omega_0\left(-\frac{R_2}{L_{A}}\psi_{dr1} + \frac{L_m R_2}{L_{A}} i_{ym} - (\omega - \omega_m)\psi_{qr1}\right)$$

$$\frac{d\psi_{dr2}}{dt} = \omega_0\left(-\frac{R_3}{L_{B}}\psi_{dr2} + \frac{L_m R_3}{L_{B}} i_{ym} - (\omega - \omega_m)\psi_{qr2}\right)$$

where $L_A = L_m + L_2$ and $L_B = L_m + L_3$. The total electromagnetic torque combines contributions from both cages:

$$T_e = \frac{L_m}{L_A}\left(-\psi_{dr1} i_{xm} + \psi_{qr1} i_{ym}\right) + \frac{L_m}{L_B}\left(-\psi_{dr2} i_{xm} + \psi_{qr2} i_{ym}\right)$$

The swing equation is identical to `inj_indmach1`.

### Parameters

| # | Name | Description | Unit |
|---|------|-------------|------|
| 1 | `SNOM` | Machine MVA rating (0 = infer from `LF`) | MVA |
| 2 | `R1` | Stator resistance | pu |
| 3 | `L1` | Stator leakage inductance | pu |
| 4 | `Lm` | Magnetizing inductance | pu |
| 5 | `R2` | First cage resistance | pu |
| 6 | `L2` | First cage leakage inductance | pu |
| 7 | `R3` | Second cage resistance | pu |
| 8 | `L3` | Second cage leakage inductance | pu |
| 9 | `H` | Inertia constant | s |
| 10 | `A` | Quadratic torque-speed coefficient | |
| 11 | `B` | Linear torque-speed coefficient | |
| 12 | `LF` | Load factor (for SNOM inference) | |

### State Variables

| Variable | Description |
|----------|-------------|
| `iy` | $y$-component of stator current | pu |
| `ix` | $x$-component of stator current | pu |
| `psidr1` | $d$-axis flux of first rotor cage | pu |
| `psiqr1` | $q$-axis flux of first rotor cage | pu |
| `psidr2` | $d$-axis flux of second rotor cage | pu |
| `psiqr2` | $q$-axis flux of second rotor cage | pu |
| `omegam` | Rotor mechanical speed | pu |

**Observables:** `P`, `Qmot+comp`, `Qmot`, `omega`

### Usage Example

<details>
<summary>Show the data record</summary>

```
INJEC  INDMACH2  MTR2  BUS_MV
      # FP FQ P Q: share of the power-flow injection (FP, FQ) or initial power (P in MW, Q in Mvar)
      1.  1.  0.  0.
      # SNOM: Machine nominal apparent power, 0 = infer from LF (MVA)
      10.0
      # R1: Stator resistance (pu (machine base))
      0.01
      # L1: Stator leakage inductance (pu (machine base))
      0.08
      # Lm: Magnetizing inductance (pu (machine base))
      2.00
      # R2: First cage resistance (pu (machine base))
      0.02
      # L2: First cage leakage inductance (pu (machine base))
      0.06
      # R3: Second cage resistance (pu (machine base))
      0.04
      # L3: Second cage leakage inductance (pu (machine base))
      0.10
      # H: Inertia constant (s)
      1.5
      # A: Quadratic coefficient of load torque vs speed
      0.8
      # B: Linear coefficient of load torque vs speed
      0.1
      # LF: Load factor, initial P over SNOM, used only when SNOM = 0
      0.0
;
```

</details>

---

## INDM1 (`inj_INDM1`): Alternative Induction Machine

The data-file model name is `INDM1` (or `inj_INDM1`).

:::note
Callable since 3.79. Earlier releases compiled this model under no name, so a data file referring to it was rejected. For built-in single-cage motors, use `INDMACH1` instead.
:::

### Description

An alternative single-cage induction machine model that uses the `INI_indmach1` helper function for initialization. It is equivalent in physics to `inj_indmach1` but implements the equations using RAMSES `.txt`-style model syntax with explicit state initialization calls. This can simplify parameterization when the helper function's output is directly used.

### Scientific Description

The model equations match those of [`inj_indmach1`](#indmach1-inj_indmach1-single-cage-induction-machine), whose block diagram applies here unchanged. The key distinction is the use of the `INI_indmach1` function at parameter-evaluation time to pre-compute $B_{\mathrm{sh}}$, $T_{m0}$, and the initial flux linkages and rotor speed, rather than solving the initialization system in Fortran. With $L_{ss} = L_{sr} + L_{ls}$ and $L_{rr} = L_{sr} + L_{lr}$, the rotor flux equations are:

$$\frac{d\psi_{dr}}{dt} = 2\pi f_0 \left[ -\frac{R_R}{L_{rr}}\psi_{dr} + \frac{L_{SR} R_R}{L_{rr}} i_{ym} - (\omega - \omega_m)\psi_{qr} \right]$$

$$\frac{d\psi_{qr}}{dt} = 2\pi f_0 \left[ -\frac{R_R}{L_{rr}}\psi_{qr} + \frac{L_{SR} R_R}{L_{rr}} i_{xm} + (\omega - \omega_m)\psi_{dr} \right]$$

The rotor speed integral uses:

$$\frac{d\omega_m}{dt} = \frac{1}{2H}\left[\frac{L_{SR}}{L_{rr}}(-\psi_{dr} i_{xm} + \psi_{qr} i_{ym}) - T_{m0}(A\omega_m^2 + B\omega_m + 1 - A - B)\right]$$

with a lower limit of $\omega_m \ge 0$.

### Parameters

| # | Name | Description | Unit |
|---|------|-------------|------|
| 1 | `SNOM` | Machine MVA rating | MVA |
| 2 | `RS` | Stator resistance | pu |
| 3 | `Lls` | Stator leakage inductance | pu |
| 4 | `LSR` | Magnetizing inductance | pu |
| 5 | `RR` | Rotor resistance | pu |
| 6 | `Llr` | Rotor leakage inductance | pu |
| 7 | `H` | Inertia constant | s |
| 8 | `A` | Quadratic torque-speed coefficient | |
| 9 | `B` | Linear torque-speed coefficient | |
| 10 | `LF` | Load factor | |

Computed internally: `BSH` (shunt susceptance), `TM0` (initial mechanical torque), `LSS`, `LRR`.

### State Variables

| Variable | Description |
|----------|-------------|
| `Psidr` | $d$-axis rotor flux linkage | pu |
| `Psiqr` | $q$-axis rotor flux linkage | pu |
| `omegam` | Rotor mechanical speed | pu |
| `iym`, `ixm` | Stator current components (on machine base) | pu |
| `dPsidr`, `dPsiqr`, `domegam` | Time-derivative auxiliary states | |

**Observables:** `omegam`

### Usage Example

<details>
<summary>Show the data record</summary>

```
INJEC  INDM1  MTR3  BUS_MV
      # FP FQ P Q: share of the power-flow injection (FP, FQ) or initial power (P in MW, Q in Mvar)
      1.  1.  0.  0.
      # SNOM: Machine MVA rating (MVA)
      10.0
      # RS: Stator resistance (pu)
      0.01
      # Lls: Stator leakage inductance (pu)
      0.10
      # LSR: Magnetizing inductance (pu)
      2.50
      # RR: Rotor resistance (pu)
      0.015
      # Llr: Rotor leakage inductance (pu)
      0.10
      # H: Inertia constant (s)
      1.5
      # A: Quadratic torque-speed coefficient
      0.8
      # B: Linear torque-speed coefficient
      0.1
      # LF: Load factor
      0.0
;
```

</details>
