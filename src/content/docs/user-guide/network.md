---
title: Network Modeling
description: Buses, lines, cables, transformers, switches, and shunts
---

The network model includes buses, lines, cables, transformers, switches, and shunts.

## Buses

In dynamic simulations with RAMSES, the only parameter associated with a bus is its **nominal voltage** (RMS line-to-line voltage), used as base voltage for per-unit conversions.

Two buses with different nominal voltages **cannot** be connected through lines or switches.

### Data Format

```
BUS NAME VNOM ;
```

| Field | Description |
|-------|-------------|
| `NAME` | Bus name (max 8 characters) |
| `VNOM` | Nominal voltage in kV |

Only one BUS record per bus is allowed. All buses must be declared before being referenced.

:::note
For power flow computations with PFC, an extended version of the BUS record with six fields is used (see [PFC Data](/user-guide/pfc/)). When RAMSES encounters the extended format, only the first two fields are read.
:::

## Lines and Cables

### Modeling

Lines and cables use the same **pi-equivalent** model with series resistance $R$, series reactance $X$, and half-shunt susceptance $\omega C/2$. Shunt conductances are neglected.

<img src="/images/netw-line.svg" alt="Pi-equivalent of lines and cables" style="width:60%" />

Under the phasor approximation, **series capacitors** can also be modeled with this pi-equivalent by setting $R = 0$, $C = 0$, and $X$ to a negative value.

### Data Format

```
LINE NAME BUS1 BUS2 R X WC2 SNOM BR ;
```

| Field | Description | Unit |
|-------|-------------|------|
| `NAME` | Line name (max 20 characters) | — |
| `BUS1` | First bus name | — |
| `BUS2` | Second bus name | — |
| `R` | Series resistance | Ω |
| `X` | Series reactance | Ω |
| `WC2` | Half shunt susceptance $\omega C/2$ | μS |
| `SNOM` | Nominal apparent power, used to display line loading or in user-defined models (0 = infinite) | MVA |
| `BR` | Breaker status (0 = open, other = closed) | — |

Line orientation is arbitrary: BUS1 and BUS2 may be swapped. Only one LINE record per line is allowed.

Lines must not connect two buses with different nominal voltages.

:::note
To connect a line through a single end, add a bus at the open end and set BR to a nonzero value.
:::

:::note
All lines are memorized, even those out of service. An out-of-service line has zero power flow but can be put into service during dynamic simulation.
:::

## Switches

A switch is a connection **without impedance** between two buses, treated internally as a very short line with $R = 0$, $\omega C/2 = 0$, and $X$ set to a very small value. Thus it has no active power losses and negligible reactive power losses.

### Data Format

```
SWITCH NAME BUS1 BUS2 BR ;
```

| Field | Description |
|-------|-------------|
| `NAME` | Switch name (max 20 characters) |
| `BUS1` | First bus name (max 8 characters) |
| `BUS2` | Second bus name (max 8 characters) |
| `BR` | Status (0 = open, other = closed) |

Switch orientation is arbitrary: BUS1 and BUS2 may be swapped. Only one SWITCH record per switch is allowed.

Switches must not connect two buses with different nominal voltages.

All switches are memorized, even those which are open. An open switch has zero power flow but can be put into service during dynamic simulation.

## Transformers

### Modeling

Transformers are represented by a two-port model with:
- Series resistance $R$ (copper losses)
- Leakage reactance $X$
- Magnetizing susceptances $B_1$ and $B_2$ (negative values). Usually one of them is zero.
- Transformer ratio magnitude $n$ and phase angle $\phi$. A phase-shifting transformer is characterized by a nonzero value of $\phi$.

<img src="/images/netw-transfo.svg" alt="Two-port model of transformers" style="width:60%" />

Iron losses are neglected (no shunt resistance). $R$, $X$, $B_1$, and $B_2$ are specified on the "from" side.

### Base Conversions

#### Manufacturer Data Conversion

The values of $R$, $X$, $B_1$, and $B_2$ relate to the following characteristics from manufacturer data:

- $S_{nom}$: nominal apparent power
- $V_{N1}$ (resp. $V_{N2}$): nominal voltage on the "from" (resp. "to") side
- $R_{baseV_{N1}}$ (resp. $X_{baseV_{N1}}$): series resistance (resp. leakage reactance) in per unit on the $(S_{nom}, V_{N1})$ base
- $B_{1\,baseV_{N1}}$ and $B_{2\,baseV_{N1}}$: shunt susceptances in per unit on the $(S_{nom}, V_{N1})$ base
- $V_{o1}$ and $V_{o2}$: open-circuit voltages corresponding to the transformer ratio (very often $V_{o1} = V_{N1}$ and $V_{o2} = V_{N2}$)

Let $V_{B1}$ and $V_{B2}$ be the nominal voltages of the "from" and "to" buses, as specified in their BUS records.

Parameters are specified in **percent** on the $(S_{nom}, V_{B1})$ base:

$$
R = 100 \cdot R_{baseV_{N1}} \left(\frac{V_{N1}}{V_{B1}}\right)^2 \quad\quad X = 100 \cdot X_{baseV_{N1}} \left(\frac{V_{N1}}{V_{B1}}\right)^2
$$

$$
B_1 = 100 \cdot B_{1\,baseV_{N1}} \left(\frac{V_{B1}}{V_{N1}}\right)^2 \quad\quad B_2 = 100 \cdot B_{2\,baseV_{N1}} \left(\frac{V_{B1}}{V_{N1}}\right)^2
$$

$$
n = 100 \cdot \frac{V_{o2} \cdot V_{B1}}{V_{o1} \cdot V_{B2}}
$$

### Data Format — Full Model (TRANSFO)

```
TRANSFO NAME FROMBUS TOBUS R X B1 B2 N PHI SNOM BR ;
```

| Field | Description | Unit |
|-------|-------------|------|
| `NAME` | Transformer name (max 20 characters) | — |
| `FROMBUS` | "From" bus name | — |
| `TOBUS` | "To" bus name | — |
| `R` | Series resistance | % |
| `X` | Leakage reactance | % |
| `B1` | Shunt susceptance (from side) | % |
| `B2` | Shunt susceptance (to side) | % |
| `N` | Transformer ratio magnitude | % |
| `PHI` | Transformer ratio phase angle | degree |
| `SNOM` | Nominal apparent power (must not be zero) | MVA |
| `BR` | Breaker status | — |

Only one TRANSFO or TRFO record per transformer is allowed.

:::caution
The orientation is **not arbitrary**: FROMBUS and TOBUS cannot be swapped.
:::

:::note
All transformers are memorized, even those out of service. An out-of-service transformer has zero power flow but can be put into service during dynamic simulation.
:::

:::note
To connect a transformer through a single end, add a bus at the open end and set BR to a nonzero value.
:::

### Data Format — Combined Model (TRFO)

```
TRFO NAME FROMBUS TOBUS CONBUS R X B N SNOM NFIRST NLAST NBPOS TOLV VDES BR ;
```

This simplified model has $B_2 = 0$ and $\phi = 0$, and **combines the transformer model with load tap changer (LTC) data for PFC** in a single record. The LTC fields (`CONBUS`, `NFIRST`, `NLAST`, `NBPOS`, `TOLV`, `VDES`) provide PFC with the information needed to adjust the transformer ratio during power flow computation. These fields are not used by RAMSES during dynamic simulation. It cannot be used for phase-shifting transformers.

To control the transformer ratio during dynamic simulation, associate a [DCTL LTC](/models/discrete-controllers/#dctl_ltc--load-tap-changer-standard) controller with the transformer.

See [PFC Data](/user-guide/pfc/) for details on ratio adjustment.

| Field | Description | Unit |
|-------|-------------|------|
| `NAME` | Transformer name (max 20 characters) | — |
| `FROMBUS` | "From" bus name (max 8 characters) | — |
| `TOBUS` | "To" bus name (max 8 characters) | — |
| `CONBUS` | Controlled bus for PFC ratio adjustment (max 8 characters). Not used by RAMSES, but a dummy name must be provided | — |
| `R` | Series resistance | % |
| `X` | Leakage reactance | % |
| `B` | Shunt susceptance (from side; $B_2 = 0$) | % |
| `N` | Transformer ratio magnitude | % |
| `SNOM` | Nominal apparent power (must not be zero) | MVA |
| `NFIRST` | Ratio at first tap position (lower bound), used by PFC for ratio adjustment | % |
| `NLAST` | Ratio at last tap position (upper bound), used by PFC for ratio adjustment | % |
| `NBPOS` | Number of tap positions (including first and last), used by PFC for ratio adjustment | — |
| `TOLV` | Voltage tolerance for tap adjustment, used by PFC | pu |
| `VDES` | Desired controlled bus voltage, used by PFC | pu |
| `BR` | Breaker status (0 = open/out of service, other = closed/in service) | — |

## Non-Reciprocal Two-Ports

<img src="/images/netw-twop.svg" alt="A two-port connecting buses i and j" style="width:60%" />

A non-reciprocal two-port has a non-symmetric nodal admittance matrix:

$$
\mathbf{Y} = \begin{bmatrix}
(G_{si} + jB_{si}) + (G_{ij} + jB_{ij}) & -(G_{ij} + jB_{ij}) \\
-(G_{ji} + jB_{ji}) & (G_{ji} + jB_{ji}) + (G_{sj} + jB_{sj})
\end{bmatrix}
$$

with $G_{ij} \ne G_{ji}$ and $B_{ij} \ne B_{ji}$.

Typically, non-reciprocal two-ports are produced when reducing a network that includes phase-shifting transformers, to obtain an equivalent.

### Data Format

```
NRTP NAME FROMBUS TOBUS GIJ BIJ GJI BJI GSI BSI GSJ BSJ BR ;
```

| Field | Description |
|-------|-------------|
| `NAME` | Name of the two-port (max 20 characters) |
| `FROMBUS` | Name of bus $i$ (max 8 characters) |
| `TOBUS` | Name of bus $j$ (max 8 characters) |
| `GIJ` | Conductance from $i$ to $j$ (pu on nominal bus voltages and system base power) |
| `BIJ` | Susceptance from $i$ to $j$ (pu) |
| `GJI` | Conductance from $j$ to $i$ (pu) |
| `BJI` | Susceptance from $j$ to $i$ (pu) |
| `GSI` | Shunt conductance at bus $i$ (pu) |
| `BSI` | Shunt susceptance at bus $i$ (pu) |
| `GSJ` | Shunt conductance at bus $j$ (pu) |
| `BSJ` | Shunt susceptance at bus $j$ (pu) |
| `BR` | Breaker status (1 = closed/in service, 0 = open/out of service) |

The orientation is **not arbitrary**: FROMBUS and TOBUS cannot be swapped. Only one NRTP record per two-port is allowed.

A non-reciprocal two-port is treated as a piece of equipment; hence, the presence of the BR field.

:::note
Parameters are in per unit on nominal bus voltages and system base power (default 100 MVA, changeable via `$SBASE`).
:::

:::note
A non-reciprocal two-port **can** connect buses with different nominal voltages (unlike lines and switches).
:::

:::note
All non-reciprocal two-ports are memorized, even those out of service. An out-of-service two-port has zero power flow but can be put into service during dynamic simulation.
:::

## Shunts

### Modeling

The shunt element is a purely reactive, constant shunt admittance. The reactive power $Q$ it produces varies with the square of the voltage:

$$
Q = B \cdot V^2
$$

where $B$ is the susceptance. The element is a capacitor ($B > 0$) or a reactor ($B < 0$).

### Data Format

```
SHUNT NAME BUS_NAME QNOM BR ;
```

| Field | Description | Unit |
|-------|-------------|------|
| `NAME` | Shunt name (max 20 characters) | — |
| `BUS_NAME` | Name of the bus to which the shunt is connected (max 8 characters) | — |
| `QNOM` | Nominal reactive power produced by the shunt at the nominal bus voltage (positive = capacitor, negative = reactor) | Mvar |
| `BR` | Breaker status (1 = in service, 0 = out of service) | — |

Only one SHUNT record per named shunt is allowed. **Multiple shunts at the same bus** are allowed, each with its own name; in this case, the susceptances are added (taking signs into account).

All shunts are memorized, even those which are disconnected. A disconnected shunt has zero power flow but can be put into service during dynamic simulation.

:::caution
The SHUNT record is used by RAMSES. For PFC, shunt data is specified in the extended BUS record (see [PFC Data](/user-guide/pfc/)).
:::

## Next Steps

- [Power Flow (PFC)](/user-guide/pfc/) — Configure generators, loads, and compute the initial operating point
- [Dynamic Models](/user-guide/dynamic-models/) — Add synchronous machines and controllers
