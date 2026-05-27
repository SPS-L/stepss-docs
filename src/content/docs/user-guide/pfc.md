---
title: Power Flow (PFC)
description: Power flow computation data and settings
---

PFC uses the following network records documented in [Network Modeling](/user-guide/network/): BUS, LINE, SWITCH, TRANSFO, TRFO, NRTP.

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
| `BSHUNT` | Nominal reactive power of constant-susceptance shunt: the reactive power produced under the nominal voltage of the bus (positive = capacitor, negative = reactor) | Mvar |
| `QSHUNT` | Reactive power of constant-power shunt (positive = capacitor) | Mvar |

If no load is connected to the bus, set PLOAD and QLOAD to zero. If no shunt is connected, set BSHUNT and QSHUNT to zero.

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

For PV buses, if the upper reactive power limit QMAX is exceeded, the bus switches to PQ type with QMAX enforced, and Newton iterations continue. If subsequently the bus voltage rises above VIMP, the bus switches back to PV type. Similarly, if QMIN is exceeded, the bus switches to PQ type with QMIN enforced; it switches back to PV if the voltage subsequently drops below VIMP.

QMIN and QMAX are used only if VIMP is nonzero (PV bus).

A variant with additional fields exists:

```
GENER NAME BUS P Q VIMP SNOM QMIN QMAX PMIN PMAX BR ;
```

The `PMIN` and `PMAX` fields (minimum/maximum active power in MW) are currently ignored by STEPSS.

Only one generator is allowed per bus.

All generators are memorized, even those which are disconnected. A disconnected generator has zero power output but can be put into service during dynamic simulation.

:::note
A generator producing constant active and reactive powers can be modeled as a negative load using the BUS record (negative PLOAD/QLOAD) without a GENER record.
:::

## Slack Bus

A slack bus is **mandatory** for power flow computations: not all buses can be of PV or PQ type, since this would require knowing the active power losses in the network before performing the calculation.

A PV-type generator must be connected to the slack bus. Its voltage magnitude (from the GENER record) is imposed, and the voltage phase angle is set to zero.

```
SLACK NAME ;
```

| Field | Description |
|-------|-------------|
| `NAME` | Bus name (max 8 characters) |

There must be **exactly one** SLACK record in the data.

PFC can handle only one connected network (island). If the graph is disconnected, only the sub-network containing the slack bus is treated; the rest is ignored with a warning.

## Static Var Compensators (SVC)

Although reference is made to an SVC, the model can be used in general for any component controlling voltage with a droop. The SVC is assumed lossless: the active current injected at the controlled bus is zero.

The SVC is modeled with a controllable susceptance $B$ at a controlled bus $i$, regulating the voltage at a monitored bus $j$:

<img src="/images/SVC.svg" alt="SVC model" style="width:60%" />

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
| `NAME` | SVC name (max 20 characters) | — |
| `CON_BUS` | Controlled bus where the susceptance $B$ is varied (max 8 characters) | — |
| `MON_BUS` | Monitored bus whose voltage is regulated (max 8 characters) | — |
| `V0` | Voltage setpoint $V_j^o$ (0 = constant power mode with $P=0$, $Q=Q0$, no limits tested) | pu |
| `Q0` | Reactive power setpoint (ignored if V0 ≠ 0) | Mvar |
| `SNOM` | Nominal reactive power | Mvar |
| `BMAX` | Maximal nominal reactive power: reactive power produced under $V_i = 1$ pu when $B = B_{max}$ | Mvar |
| `BMIN` | Minimal nominal reactive power: reactive power produced under $V_i = 1$ pu when $B = B_{min}$ | Mvar |
| `G` | Gain, in pu on the ($V_B$, SNOM) base, where $V_B$ is the nominal voltage at the controlled bus | pu |
| `BR` | Breaker status (0 = open, other = closed) | — |

It is common for BMAX to be positive and BMIN negative, but other combinations are allowed.

For SVCs with nonzero V0, the voltage control equation is solved initially. If the susceptance upper limit BMAX is exceeded, the limit is enforced and Newton iterations continue. The SVC reverts to voltage control when $G(V_j^o - V_j) < B_{max}$. Similarly, if BMIN is exceeded, the lower limit is enforced; the SVC reverts when $G(V_j^o - V_j) > B_{min}$.

Only one SVC is allowed per bus. It is not allowed to connect both a generator and an SVC to the same bus.

All SVCs are memorized, even those which are disconnected. A disconnected SVC can be put into service during dynamic simulation.

## Transformer Ratio Adjustment for Voltage Control

PFC can adjust the ratio of a designated transformer to bring a controlled voltage inside a deadband $[V_{des} - \epsilon,\; V_{des} + \epsilon]$, where $V_{des}$ is the desired voltage and $\epsilon$ is the tolerance.

The ratio is changed in **discrete steps** between a minimum and maximum value. During computation, the ratio is changed by one step at a time, after which Newton iterations run until convergence. The process repeats until the controlled voltage falls in the deadband. When multiple transformers are adjusted, some may reach their deadbands before others.

### Via TRFO Record

The controlled bus is `CONBUS` in the TRFO record. This must be one of the two ending buses of the transformer. An empty or blank string **enclosed within quotes** indicates that the transformer ratio is not to be adjusted; in this case, dummy values must still be provided for the remaining fields.

The ratio corresponding to tap position $p$ ($1 \le p \le \text{NBPOS}$):

$$
n = \frac{\text{NFIRST}}{100} + \frac{p-1}{\text{NBPOS}-1} \cdot \frac{\text{NLAST} - \text{NFIRST}}{100}
$$

The initial ratio from the `N` field of the TRFO record is adjusted to the nearest tap position before starting the power flow computation.

Relevant fields in the TRFO record:

| Field | Description | Unit |
|-------|-------------|------|
| `NFIRST` | Ratio at first tap position (lower bound) | % |
| `NLAST` | Ratio at last tap position (upper bound) | % |
| `NBPOS` | Total number of tap positions (including first and last) | — |
| `TOLV` | Voltage tolerance $\epsilon$ | pu |
| `VDES` | Desired voltage $V_{des}$ | pu |

### Via LTC-V Record

The second way to specify ratio adjustment is through a separate LTC-V record. This is more natural in association with a TRANSFO record.

```
LTC-V NAME CON_BUS NFIRST NLAST NBPOS TOLV VDES ;
```

| Field | Description | Unit |
|-------|-------------|------|
| `NAME` | Name of the controlled transformer (max 20 characters) | — |
| `CON_BUS` | Controlled bus (max 8 characters) | — |
| `NFIRST` | Ratio at first tap position (lower bound) | % |
| `NLAST` | Ratio at last tap position (upper bound) | % |
| `NBPOS` | Total number of tap positions (including first and last) | — |
| `TOLV` | Voltage tolerance $\epsilon$ | pu |
| `VDES` | Desired voltage $V_{des}$ | pu |

A transformer can be controlled by a **single tap changer only**. The LTC-V record can also be associated with a TRFO record, provided that no adjustment is specified in the TRFO record itself.

## Phase-Shifting Transformer Adjustment (PSHIFT-P)

PFC can adjust the phase angle of a transformer to bring the active power flow in a monitored branch inside a deadband $[P_{des} - \epsilon,\; P_{des} + \epsilon]$. The adjustment mechanism is similar to the in-phase ratio adjustment described above.

```
PSHIFT-P CONTRFO MONBRANCH PHAFIRST PHALAST NBPOS SIGN PDES TOLP ;
```

| Field | Description | Unit |
|-------|-------------|------|
| `CONTRFO` | Name of the transformer whose phase angle is adjusted (max 20 characters, defined in a TRFO or TRANSFO record). If the transformer does not exist, the record is ignored with a warning | — |
| `MONBRANCH` | Name of the branch where active power $P$ is monitored (max 20 characters, defined in a LINE, TRFO, or TRANSFO record). $P$ is the active power leaving the first bus of the branch record | — |
| `PHAFIRST` | Phase angle $\phi$ at first tap position (lower bound) | degrees |
| `PHALAST` | Phase angle $\phi$ at last tap position (upper bound) | degrees |
| `NBPOS` | Number of tap positions | — |
| `SIGN` | Direction indicator: `1` means $\phi$ must increase to increase power flow; `-1` means decrease. Any other value causes the program to stop | — |
| `PDES` | Desired active power flow | MW |
| `TOLP` | Tolerance $\epsilon$ | MW |

The phase angle $\phi$ at tap position $p$ ($1 \le p \le \text{NBPOS}$) is:

$$
\phi = \text{PHAFIRST} + \frac{p-1}{\text{NBPOS}-1}(\text{PHALAST} - \text{PHAFIRST})
$$

The initial phase angle from the `PHI` field of the TRANSFO record is adjusted to the nearest tap position before starting the power flow computation.

PFC performs a sensitivity analysis to determine whether the phase angle should be increased or decreased. If this analysis indicates a direction opposite to SIGN, a warning is issued and SIGN is ignored. On output, PFC sets SIGN to the value from its sensitivity analysis.

Only one PSHIFT-P record per transformer is allowed. The PSHIFT-P record is intended for use with a TRANSFO record, but can also be used with a TRFO record (in which case the angle is initialized to zero).

A transformer cannot be controlled by both an LTC-V and a PSHIFT-P record.

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
The output LFRESV records from PFC can be fed back as input — this results in zero Newton iterations (round-trip property). This is an easy way to verify that system data come with their corresponding voltages.
:::

:::note
LFRESV is the output of PFC that initializes RAMSES dynamic simulation.
:::

## PFC Computation Control Parameters

PFC uses Newton–Raphson iterations to solve the power flow equations. Convergence is achieved when both the active and reactive power mismatches fall below specified thresholds, all transformer ratio and phase-shift controls are satisfied, and all generators and SVCs are within their reactive limits.

Three convergence indices are used:
- $\epsilon_P$: largest absolute mismatch of the active power equations
- $\epsilon_Q$: largest absolute mismatch of the reactive power equations
- $\epsilon_S$: largest apparent power mismatch, used to trigger limit checks (via `$MISQLIM`), Jacobian freezing (via `$MISBLOC`), and transformer adjustments (via `$MISADJ`)

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
Divergence is detected when $\varphi(k) > 1.1\,\varphi(k-1)$, where:

$$\varphi(k) = \sum_i \sqrt{(f_i - P_i^o)^2 + (g_i - Q_i^o)^2}$$

Under normal convergence, $\varphi$ decreases at each iteration; an increase signals divergence. The test is temporarily suspended following limit adjustments or transformer ratio changes, as these cause increases in $\varphi$ unrelated to divergence.
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

- [Reference Frames & Initialization](/user-guide/reference-frames/) — Understand how RAMSES initializes from the PFC solution
- [Dynamic Models](/user-guide/dynamic-models/) — Define synchronous machines, injectors, and controllers
