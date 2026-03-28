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
For power flow computations with PFC, an extended version of the BUS record with six fields is used (see [PFC Data](/stepss-docs/user-guide/pfc/)). When RAMSES encounters the extended format, only the first two fields are read.
:::

## Lines and Cables

### Modeling

Lines and cables use the same **pi-equivalent** model with series resistance $R$, series reactance $X$, and half-shunt susceptance $\omega C/2$. Shunt conductances are neglected.

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
| `SNOM` | Nominal apparent power (0 = infinite) | MVA |
| `BR` | Breaker status (0 = open, other = closed) | — |

Line orientation is arbitrary: BUS1 and BUS2 may be swapped.

:::note
To connect a line through a single end, add a bus at the open end and set BR to a nonzero value.
:::

:::note
All lines are memorized, even those out of service. An out-of-service line has zero power flow but can be put into service during dynamic simulation.
:::

## Switches

A switch is a connection **without impedance** between two buses, treated internally as a very short line with $R = 0$, $\omega C/2 = 0$, and $X$ set to a very small value.

### Data Format

```
SWITCH NAME BUS1 BUS2 BR ;
```

| Field | Description |
|-------|-------------|
| `NAME` | Switch name (max 20 characters) |
| `BUS1` | First bus name |
| `BUS2` | Second bus name |
| `BR` | Status (0 = open, other = closed) |

## Transformers

### Modeling

Transformers are represented by a two-port model with:
- Series resistance $R$ (copper losses)
- Leakage reactance $X$
- Magnetizing susceptances $B_1$ and $B_2$ (negative values)
- Transformer ratio magnitude $n$ and phase angle $\phi$

Iron losses are neglected (no shunt resistance). $R$, $X$, $B_1$, and $B_2$ are specified on the "from" side.

### Base Conversions

Parameters are specified in **percent** on the $(S_{nom}, V_{B1})$ base:

$$
R = 100 \cdot R_{pu} \left(\frac{V_{N1}}{V_{B1}}\right)^2 \quad\quad X = 100 \cdot X_{pu} \left(\frac{V_{N1}}{V_{B1}}\right)^2
$$

$$
n = 100 \cdot \frac{V_{o2} \cdot V_{B1}}{V_{o1} \cdot V_{B2}}
$$

where $V_{B1}$ and $V_{B2}$ are the nominal voltages of the "from" and "to" buses.

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

:::caution
The orientation is **not arbitrary**: FROMBUS and TOBUS cannot be swapped.
:::

:::note
To connect a transformer through a single end, add a bus at the open end and set BR to a nonzero value.
:::

### Data Format — Simplified Model (TRFO)

```
TRFO NAME FROMBUS TOBUS CONBUS R X B N SNOM NFIRST NLAST NBPOS TOLV VDES BR ;
```

This simplified model has $B_2 = 0$ and $\phi = 0$, and includes data for PFC to adjust the transformer ratio. It cannot be used for phase-shifting transformers. See [PFC Data](/stepss-docs/user-guide/pfc/) for details on ratio adjustment.

| Field | Description | Unit |
|-------|-------------|------|
| `NAME` | Transformer name (max 20 characters) | — |
| `FROMBUS` | "From" bus name (max 8 characters) | — |
| `TOBUS` | "To" bus name (max 8 characters) | — |
| `CONBUS` | Bus used by PFC for ratio adjustment (max 8 characters; a dummy name must be provided even if not used by RAMSES) | — |
| `R` | Series resistance | % |
| `X` | Leakage reactance | % |
| `B` | Shunt susceptance (from side; $B_2 = 0$) | % |
| `N` | Transformer ratio magnitude | % |
| `SNOM` | Nominal apparent power (must not be zero) | MVA |
| `NFIRST` | Initial (first) tap ratio value, used by PFC for ratio adjustment | % |
| `NLAST` | Final (last) tap ratio value, used by PFC for ratio adjustment | % |
| `NBPOS` | Number of tap positions, used by PFC for ratio adjustment | — |
| `TOLV` | Voltage tolerance for tap adjustment, used by PFC | pu |
| `VDES` | Desired controlled bus voltage, used by PFC | pu |
| `BR` | Breaker status (0 = open/out of service, other = closed/in service) | — |

## Non-Reciprocal Two-Ports

A non-reciprocal two-port has a non-symmetric nodal admittance matrix:

$$
\mathbf{Y} = \begin{bmatrix}
(G_{si} + jB_{si}) + (G_{ij} + jB_{ij}) & -(G_{ij} + jB_{ij}) \\
-(G_{ji} + jB_{ji}) & (G_{ji} + jB_{ji}) + (G_{sj} + jB_{sj})
\end{bmatrix}
$$

with $G_{ij} \ne G_{ji}$ and $B_{ij} \ne B_{ji}$.

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

:::note
Parameters are in per unit on nominal bus voltages and system base power (default 100 MVA).
:::

:::note
A non-reciprocal two-port can connect buses with different nominal voltages.
:::

## Shunts

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

:::caution
The SHUNT record is used by RAMSES. For PFC, shunt data is specified in the extended BUS record (see [PFC Data](/stepss-docs/user-guide/pfc/)).
:::
