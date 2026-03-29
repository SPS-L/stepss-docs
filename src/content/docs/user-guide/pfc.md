---
title: Power Flow (PFC)
description: Power flow computation data and settings
---

PFC uses the following network records documented in [Network Modeling](/stepss-docs/user-guide/network/): BUS, LINE, SWITCH, TRANSFO, TRFO, NRTP.

The additional records specific to power flow computations are documented below.

## Load and Shunt Data

Load and shunt data are specified in an extended version of the BUS record:

```
BUS NAME VNOM PLOAD QLOAD BSHUNT QSHUNT ;
```

| Field | Description | Unit |
|-------|-------------|------|
| `NAME` | Bus name (max 8 characters) | — |
| `VNOM` | Nominal voltage | kV |
| `PLOAD` | Total active power load (positive = consumed) | MW |
| `QLOAD` | Total reactive power load (positive = consumed) | Mvar |
| `BSHUNT` | Nominal reactive power of constant-susceptance shunt (positive = capacitor) | Mvar |
| `QSHUNT` | Reactive power of constant-power shunt (positive = capacitor) | Mvar |

The total reactive power $Q$ produced by both shunt components:

$$
Q = \text{BSHUNT} \cdot \left(\frac{V}{V_{nom}}\right)^2 + \text{QSHUNT}
$$

:::note
The PLOAD, QLOAD, BSHUNT, and QSHUNT fields are **ignored by RAMSES**.
:::

## Generator Data

```
GENER NAME BUS P Q VIMP SNOM QMIN QMAX BR ;
```

| Field | Description | Unit |
|-------|-------------|------|
| `NAME` | Generator name (max 20 characters) | — |
| `BUS` | Connection bus name | — |
| `P` | Active power produced | MW |
| `Q` | Reactive power produced (ignored if VIMP ≠ 0) | Mvar |
| `VIMP` | Imposed voltage (0 = PQ bus, nonzero = PV bus) | pu |
| `SNOM` | Nominal apparent power | MVA |
| `QMIN` | Lower reactive power limit | Mvar |
| `QMAX` | Upper reactive power limit | Mvar |
| `BR` | Breaker status (0 = open) | — |

For PV buses, if reactive limits are exceeded, the bus switches to PQ type with the limit enforced. It switches back to PV if the voltage returns past the setpoint.

A variant with additional fields `PMIN` and `PMAX` exists but these are currently ignored by STEPSS.

Only one generator is allowed per bus.

:::note
A generator producing constant active and reactive powers can be modeled as a negative load using the BUS record (negative PLOAD/QLOAD) without a GENER record.
:::

## Slack Bus

A slack bus is **mandatory** for power flow. A PV-type generator must be connected to it.

```
SLACK NAME ;
```

PFC can handle only one connected network. If the graph is disconnected, only the sub-network containing the slack bus is treated.

## Static Var Compensators (SVC)

The SVC is modeled with a controllable susceptance $B$ at a controlled bus $i$, regulating the voltage at a monitored bus $j$:

$$
I_{Qi} = G(V_j^o - V_j) V_i \quad \text{(voltage control)}
$$

$$
I_{Qi} = B_{max} V_i \quad \text{(upper limit)} \quad\quad I_{Qi} = B_{min} V_i \quad \text{(lower limit)}
$$

### Data Format

```
SVC NAME CON_BUS MON_BUS V0 Q0 SNOM BMAX BMIN G BR ;
```

| Field | Description | Unit |
|-------|-------------|------|
| `NAME` | SVC name | — |
| `CON_BUS` | Controlled bus | — |
| `MON_BUS` | Monitored bus | — |
| `V0` | Voltage setpoint (0 = constant power mode) | pu |
| `Q0` | Reactive power setpoint (ignored if V0 ≠ 0) | Mvar |
| `SNOM` | Nominal reactive power | Mvar |
| `BMAX` | Max nominal reactive power | Mvar |
| `BMIN` | Min nominal reactive power | Mvar |
| `G` | Gain | pu |
| `BR` | Breaker status | — |

It is not allowed to connect both a generator and an SVC to the same bus.

## Transformer Ratio Adjustment

PFC can adjust transformer ratios to bring a controlled voltage inside a deadband $[V_{des} - \epsilon,\; V_{des} + \epsilon]$.

### Via TRFO Record

The ratio corresponding to tap position $p$ ($1 \le p \le \text{NBPOS}$):

$$
n = \frac{\text{NFIRST}}{100} + \frac{p-1}{\text{NBPOS}-1} \cdot \frac{\text{NLAST} - \text{NFIRST}}{100}
$$

Relevant fields in the TRFO record: `CONBUS`, `NFIRST`, `NLAST`, `NBPOS`, `TOLV`, `VDES`.

### Via LTC-V Record

```
LTC-V NAME CON_BUS NFIRST NLAST NBPOS TOLV VDES ;
```

## Phase-Shifting Transformer Adjustment (PSHIFT-P)

For phase-shifting transformers, PFC can adjust the phase angle to bring the active power flow in a monitored branch inside a deadband $[P_{des} - \epsilon,\; P_{des} + \epsilon]$.

```
PSHIFT-P CONTRFO MONBRANCH PHAFIRST PHALAST NBPOS SIGN PDES TOLP ;
```

| Field | Description | Unit |
|-------|-------------|------|
| `CONTRFO` | Name of the controlled phase-shifting transformer (max 20 characters) | — |
| `MONBRANCH` | Name of the monitored branch (max 20 characters) | — |
| `PHAFIRST` | Phase angle at first tap position | degrees |
| `PHALAST` | Phase angle at last tap position | degrees |
| `NBPOS` | Number of tap positions | — |
| `SIGN` | +1 or -1 — determines direction of power flow increase with phase angle increase | — |
| `PDES` | Desired active power on monitored branch | MW |
| `TOLP` | Tolerance on active power | MW |

The phase angle $\phi$ at tap position $p$ ($1 \le p \le \text{NBPOS}$) is:

$$
\phi = \text{PHAFIRST} + \frac{p-1}{\text{NBPOS}-1}(\text{PHALAST} - \text{PHAFIRST})
$$

:::note
PFC performs a sensitivity analysis to determine whether the phase angle should be increased or decreased. If this analysis indicates a direction opposite to SIGN, a warning is issued and SIGN is ignored.
:::

:::note
A transformer cannot be controlled by both an LTC-V and a PSHIFT-P record.
:::

## Bus Voltages: Initial Values and Results (LFRESV)

On output, PFC produces a file with the computed bus voltage magnitudes and phase angles. These are stored in LFRESV records. The syntax is:

```
LFRESV BUS MODV PHASV ;
```

| Field | Description | Unit |
|-------|-------------|------|
| `BUS` | Bus name (max 8 characters) | — |
| `MODV` | Voltage magnitude | pu |
| `PHASV` | Voltage phase angle, referenced to slack bus | radians |

:::note
If LFRESV records are provided as input, they are used as initial voltages for Newton iterations.
:::

:::note
Default initialization: PQ buses start at 1 pu magnitude and 0 angle; PV buses start at the generator-specified voltage and 0 angle.
:::

:::note
The output LFRESV records from PFC can be fed back as input — this results in zero Newton iterations (round-trip property).
:::

:::note
LFRESV is the output of PFC that initializes RAMSES dynamic simulation.
:::

## PFC Computation Control Parameters

PFC uses Newton–Raphson iterations to solve the power flow equations. Convergence is achieved when both the active and reactive power mismatches fall below specified thresholds, all transformer ratio and phase-shift controls are satisfied, and all generators and SVCs are within their reactive limits.

The following records control the computation. Each record starts with `$` and has a single numeric field.

| Parameter | Default | Unit | Description |
|-----------|---------|------|-------------|
| `$SBASE` | 100 | MVA | System base power (on which pu values are expressed) |
| `$TOLAC` | 0.1 | MW | Convergence tolerance on active power mismatch ($\epsilon_P$) |
| `$TOLREAC` | 0.1 | Mvar | Convergence tolerance on reactive power mismatch ($\epsilon_Q$) |
| `$NBITMA` | 20 | — | Maximum number of Newton iterations |
| `$MISQLIM` | 20 | MVA | Apparent power mismatch threshold below which generator/SVC reactive limits are checked and enforced (set to 0 to skip) |
| `$MISBLOC` | 10 | MVA | Apparent power mismatch threshold below which the Jacobian is kept constant |
| `$MISADJ` | 10 | MVA | Apparent power mismatch threshold below which transformer ratios and phase shifts are adjusted (set to 0 to skip) |
| `$DIVDET` | 0 | — | Set to 1 to activate divergence detection; 0 to skip |

:::note
Divergence is detected when $\varphi(k) > 1.1\,\varphi(k-1)$, where $\varphi$ is a norm of the power mismatches. The test is temporarily suspended following generator/SVC limit adjustments or transformer ratio/phase-shift adjustments.
:::

## Record Sharing Between PFC and RAMSES

The following table summarises which records are used by PFC and RAMSES respectively.

| Record | PFC | RAMSES |
|--------|-----|--------|
| BUS | All 6 fields | First 2 fields (NAME, VNOM) |
| LINE | All fields | All fields |
| SWITCH | All fields | All fields |
| NRTP | All fields | All fields |
| TRANSFO | All fields | All fields |
| TRFO | All fields | Fields 1–9 and 15 only |
| SHUNT | Ignored | All fields |
| GENER | All fields | Ignored |
| SVC | All fields | Ignored |
| SLACK | Used | Used |
| LFRESV | Input: initial values; Output: solution | Input: initial values for RAMSES |
| LTC-V | Used | Ignored |
| PSHIFT-P | Used | Ignored |

## Next Steps

- [Reference Frames & Initialization](/stepss-docs/user-guide/reference-frames/) — Understand how RAMSES initializes from the PFC solution
- [Dynamic Models](/stepss-docs/user-guide/dynamic-models/) — Define synchronous machines, injectors, and controllers
