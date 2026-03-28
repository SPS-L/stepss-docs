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

### Phase Shifter Adjustment (LTC-P)

For phase-shifting transformers, controlling active power flow:

```
LTC-P NAME CON_BRANCH NFIRST NLAST NBPOS TOLP PDES ;
```
