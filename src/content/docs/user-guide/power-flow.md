---
title: Power Flow
description: Power flow data records and solver settings for the Helios engine
---

**Helios** is the STEPSS AC power-flow engine. It solves the Newton-Raphson power
flow in polar coordinates with reactive limit enforcement, transformer tap
adjustment, SVC modelling and AC/DC converters joining DC grids to the AC
network, and it produces the operating point that
initialises a RAMSES dynamic simulation.

Helios is reached two ways, both reading the same data files:

- **Run power flow** on the [Power Flow Simulation tab](/gui/interface/#power-flow-simulation) of STEPSS GUI, which carries the engine rather than asking you to download it;
- `stepss.helios.HeliosSession` from Python, see [Power Flow with Helios](/python/helios/).

A C API shared library (`libhelios_api`) exists underneath both, for embedding the engine in another tool.

The power flow uses the following network records documented in [Network Modeling](/user-guide/network/): BUS, BUSDC, LINE, SWITCH, TRANSFO, TRFO, NRTP.

The additional records specific to power flow computations are documented below.

## Watch it

Episode 3 of the [video series](/resources/videos/), *Helios in Depth*, covers this page.

<div class="video-embed"><iframe src="https://www.youtube-nocookie.com/embed/gM7FrQYJ0l0" title="STEPSS Episode 3: Helios in Depth" loading="lazy" allowfullscreen allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"></iframe></div>

## Load and Shunt Data

Load and shunt data are specified in an extended version of the BUS record:

```
BUS NAME VNOM PLOAD QLOAD BSHUNT QSHUNT ;
```

| Field | Description | Unit |
|-------|-------------|------|
| `NAME` | Bus name (max 8 characters) | |
| `VNOM` | Nominal voltage | kV |
| `PLOAD` | Total active power load (positive = consumed) | MW |
| `QLOAD` | Total reactive power load (positive = consumed) | Mvar |
| `BSHUNT` | Nominal reactive power of constant-susceptance shunt: the reactive power produced under the nominal voltage of the bus (positive = capacitor, negative = reactor) | Mvar |
| `QSHUNT` | Reactive power of constant-power shunt (positive = capacitor) | Mvar |

If no load is connected to the bus, set PLOAD and QLOAD to zero. If no shunt is connected, set BSHUNT and QSHUNT to zero. `QSHUNT` is optional: a five-field BUS record is accepted and QSHUNT defaults to zero.

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
| `NAME` | Generator name (max 20 characters) | |
| `BUS` | Connection bus name | |
| `P` | Active power produced | MW |
| `Q` | Reactive power produced (ignored if VIMP ≠ 0) | Mvar |
| `VIMP` | Imposed voltage (0 = PQ bus, nonzero = PV bus) | pu |
| `SNOM` | Nominal apparent power | MVA |
| `QMIN` | Lower reactive power limit | Mvar |
| `QMAX` | Upper reactive power limit | Mvar |
| `BR` | Breaker status (0 = open) | |

For PV buses, if the upper reactive power limit QMAX is exceeded, the bus switches to PQ type with QMAX enforced, and Newton iterations continue. If subsequently the bus voltage rises above VIMP, the bus switches back to PV type. Similarly, if QMIN is exceeded, the bus switches to PQ type with QMIN enforced; it switches back to PV if the voltage subsequently drops below VIMP.

QMIN and QMAX are used only if VIMP is nonzero (PV bus).

An extended variant with active power limits and a participation factor exists:

```
GENER NAME BUS P Q VIMP SNOM QMIN QMAX PMIN PMAX PART BR ;
```

| Field | Description | Unit |
|-------|-------------|------|
| `PMIN` | Minimum active power the generator can produce | MW |
| `PMAX` | Maximum active power the generator can produce | MW |
| `PART` | Participation factor used when redistributing an active power imbalance | |

`PMIN`/`PMAX` are not enforced during Newton iterations. They are used to clamp the specified `P` before the computation (the slack generator is exempted by default; see `$PLIM` below), and together with `PART` when generation is redispatched after system modifications or contingencies.

Both variants also accept an additional bus-name field between `BUS` and `P` (making 10 or 13 fields in total); that field is accepted and ignored.

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

A SLACK record may appear once per AC island, where an island is a set of AC buses joined by in-service branches; two SLACK records in one island are an error. At least one SLACK record is required. SLACK records in separate AC islands are each solved, each slack generator balancing its own island, and the power balance reports the sum over all slack generators.

An island without a SLACK takes as its reference the first in-service [AC/DC converter](#acdc-converters-acdc) on it, in record order, with `VAC` given; that converter must have `VDC` `*`, and the log names it. Islands with neither a SLACK nor such a converter are ignored with a warning. Only islands with a reference, and the DC grids their converters energise, are solved.

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
| `NAME` | SVC name (max 20 characters) | |
| `CON_BUS` | Controlled bus where the susceptance $B$ is varied (max 8 characters) | |
| `MON_BUS` | Monitored bus whose voltage is regulated (max 8 characters) | |
| `V0` | Voltage setpoint $V_j^o$ (0 = constant power mode with $P=0$, $Q=Q0$, no limits tested) | pu |
| `Q0` | Reactive power setpoint (ignored if V0 ≠ 0) | Mvar |
| `SNOM` | Nominal reactive power | Mvar |
| `BMAX` | Maximal nominal reactive power: reactive power produced under $V_i = 1$ pu when $B = B_{max}$ | Mvar |
| `BMIN` | Minimal nominal reactive power: reactive power produced under $V_i = 1$ pu when $B = B_{min}$ | Mvar |
| `G` | Gain, in pu on the ($V_B$, SNOM) base, where $V_B$ is the nominal voltage at the controlled bus | pu |
| `BR` | Breaker status (0 = open, other = closed) | |

It is common for BMAX to be positive and BMIN negative, but other combinations are allowed.

For SVCs with nonzero V0, the voltage control equation is solved initially. If the susceptance upper limit BMAX is exceeded, the limit is enforced and Newton iterations continue. The SVC reverts to voltage control when $G(V_j^o - V_j) < B_{max}$. Similarly, if BMIN is exceeded, the lower limit is enforced; the SVC reverts when $G(V_j^o - V_j) > B_{min}$.

Only one SVC is allowed per bus. It is not allowed to connect both a generator and an SVC to the same bus.

All SVCs are memorized, even those which are disconnected. A disconnected SVC can be put into service during dynamic simulation.

## AC/DC Converters (ACDC)

Helios solves a combined AC-DC power flow: the AC network, the [DC buses](/user-guide/network/#dc-buses) and [DC lines](/user-guide/network/#dc-lines-and-cables) of one or more DC grids, and the static converters joining them are solved together in the same Newton iteration. The `ACDC` record describes a voltage-source converter between an AC bus and a DC bus, with optional DC voltage droop, quadratic converter losses and a converter station. It is read from Helios 1.6.0 onward.

The AC bus of the record is the point of common coupling (PCC), where the AC set-points apply. Without a station the converter sits directly at the PCC. With a station, a transformer ($R_{TF} + jX_{TF}$) runs from the PCC to a filter node carrying the filter susceptance $B_F$, and a phase reactor ($R_C + jX_C$) runs from the filter node to the converter node, whose voltage is $V_c$ and whose power into the converter is $P_c + jQ_c$. The losses of the conversion itself sit between the converter node and the DC bus.

### Data Format

The record always carries all 26 fields. A `*` marks a field that is free or absent; what `*` means differs per field and is given in the last column.

```
ACDC NAME ACBUS DCBUS PAC QAC VAC PDC VDC EFF QMIN QMAX KDROOP DVDB PMIN PMAX LOSSA LOSSB LOSSCR LOSSCI KVC RTF XTF BF RC XC BR ;
```

| Field | Description | Unit | `*` means |
|-------|-------------|------|-----------|
| `NAME` | Converter name, unique | | required |
| `ACBUS` | AC bus (a BUS record), the PCC | | required |
| `DCBUS` | DC bus (a BUSDC record) | | required |
| `PAC` | Active power drawn from the AC grid at the PCC, positive when rectifying | MW | free |
| `QAC` | Reactive power injected into the AC grid at the PCC | Mvar | 0 when fixed |
| `VAC` | AC voltage set-point at the PCC | pu | no AC voltage control |
| `PDC` | Active power delivered into the DC bus, positive when rectifying; for a droop converter, the power set-point $P_{SET}$ | MW | free |
| `VDC` | DC voltage set-point; for a droop converter, the voltage set-point $V_{SET}$ | pu | no DC voltage control |
| `EFF` | Efficiency, $0 < \text{EFF} \le 1$ | pu | use the `LOSS` fields |
| `QMIN` | Lower reactive limit at the PCC, used with `VAC` | Mvar | no lower limit |
| `QMAX` | Upper reactive limit at the PCC, used with `VAC` | Mvar | no upper limit |
| `KDROOP` | Droop gain, MW of `PDC` change per pu of DC voltage, > 0 | MW/pu | no droop |
| `DVDB` | Symmetric deadband around `VDC`, ≥ 0 | pu | 0 |
| `PMIN` | Lower `PDC` limit of a droop converter | MW | no lower limit |
| `PMAX` | Upper `PDC` limit of a droop converter | MW | no upper limit |
| `LOSSA` | Constant loss | MW | use `EFF` |
| `LOSSB` | Linear loss coefficient, multiplies the converter current | kV | use `EFF` |
| `LOSSCR` | Quadratic loss coefficient when the converter is physically rectifying, multiplies the current squared | Ω | use `EFF` |
| `LOSSCI` | Quadratic loss coefficient when inverting | Ω | use `EFF` |
| `KVC` | Converter-side line voltage base for the loss current, > 0 | kV | VNOM of `ACBUS` |
| `RTF` | Station transformer resistance, PCC to filter node | pu | 0 (absent) |
| `XTF` | Station transformer reactance | pu | 0 (absent) |
| `BF` | Filter susceptance at the filter node, capacitive positive | pu | 0 (absent) |
| `RC` | Phase reactor resistance, filter node to converter node | pu | 0 (absent) |
| `XC` | Phase reactor reactance | pu | 0 (absent) |
| `BR` | Status (1 = in service, 0 = out of service) | | required |

Powers are divided by `$SBASE`. The station impedances and `BF` are in pu on `$SBASE` and the VNOM of `ACBUS`. With every station field `*`, the converter node is the PCC.

### Control Modes

The given fields select how the converter behaves on each side.

**AC side**, from `VAC`:

- `VAC` `*`: `QAC` is fixed (PQ).
- `VAC` given: the PCC is a PV bus and `QAC` floats between `QMIN` and `QMAX`; a `*` in either limit leaves that side unbounded. `QMIN` greater than `QMAX` is an error.

**DC side**, from `VDC` and `KDROOP`:

- Both `*`: **fixed power**. One of `PAC` and `PDC` is given and the other follows.
- `VDC` given, `KDROOP` `*`: **constant DC voltage**. The DC bus is held at `VDC` and the power floats; any `PAC` or `PDC` given is only a starting guess. This converter is the DC slack of its grid.
- `VDC` and `KDROOP` given: **droop**. `PDC` (as $P_{SET}$) must be given, and the power follows the DC voltage.

A droop converter follows

$$
P_{DC} = P_{SET} - K_{DROOP}\, d(V_{DC} - V_{SET})
$$

where the deadband function $d(x)$ is $0$ for $|x| \le \text{DVDB}$, $x - \text{DVDB}$ above it and $x + \text{DVDB}$ below it. At `PMIN` or `PMAX` the converter holds that power.

The DC-side fields are refused when they do not form one of these modes: `KDROOP` with `VDC` `*`; `DVDB`, `PMIN` or `PMAX` without `KDROOP`; `PMIN` greater than `PMAX`; `KDROOP` ≤ 0; `DVDB` < 0; and a droop converter with `PDC` `*`.

### Losses

The coupling between the converter node and the DC bus takes exactly one of two forms. Any other combination of `EFF` and the four `LOSS` fields (both, neither, or only some of the four `LOSS` fields) is an error naming the record.

**Efficiency only**: `EFF` given and all four `LOSS` fields `*`. With $P_c$ the power flowing into the converter at the converter node, rectifying $P_{DC} = \text{EFF}\cdot P_c$ and inverting $P_c = \text{EFF}\cdot P_{DC}$.

**Quadratic losses**: `LOSSA`, `LOSSB`, `LOSSCR` and `LOSSCI` all given and `EFF` `*`:

$$
P_c - P_{DC} = \text{LOSSA} + \text{LOSSB}\cdot I + \text{LOSSC}\cdot I^2, \qquad I = \frac{|S_c|}{\sqrt{3}\,|V_c|\,\text{KVC}} \ \text{(kA)}
$$

where `LOSSC` is `LOSSCR` when the converter is physically rectifying ($P_c > 0$) and `LOSSCI` when it is inverting. Internally the coefficients are converted to pu on $S_B$ = `$SBASE` as $a = \text{LOSSA}/S_B$, $b = \text{LOSSB}/(\sqrt{3}\,\text{KVC})$ and $c = \text{LOSSC}\cdot S_B/(3\,\text{KVC}^2)$, and the droop gain as $K = K_{DROOP}/S_B$.

A converter whose `PAC` is free (fixed `PDC`, constant DC voltage or droop) can deliver at most a certain `PDC`: beyond it the losses grow faster than the power. A solve that ends with a converter asked for more stops with the status `CONVERTER_INFEASIBLE` (see [Solver Outcomes](#solver-outcomes)).

### Which Powers to Give

**Efficiency-only converter without a station, fixed power** (`VDC` `*`): `PAC`, `PDC` and `EFF` form a triplet, and two of the three must be given; the third is filled in from rectifying $P_{DC} = \text{EFF}\cdot P_{AC}$ or inverting $P_{AC} = \text{EFF}\cdot P_{DC}$.

- With both powers given, the direction follows their sign (zero counts as rectifying), the two must not have opposite signs, and the smaller magnitude must be the one leaving the converter, which fixes `EFF`.
- With all three given, the efficiency the two powers imply must match `EFF` within $10^{-4}$, or the record is refused.
- A record with only one of the three is refused.
- `PAC` and `PDC` both zero with `EFF` `*` is accepted with `EFF` = 1. Exactly one of them zero with `EFF` `*` is refused, since the efficiency cannot be determined.

**Efficiency-only converter with `VDC` given**: the solver finds the power. `EFF` must be given, unless `PAC` and `PDC` are both given and non-zero, in which case their ratio fixes it. `PAC` and `PDC` both zero with `EFF` `*` is refused.

**Converter with `LOSS` fields or a station**: `PDC`/`PAC` is no efficiency, so no ratio, sign or `EFF` inference applies.

- A free-power converter (constant DC voltage, droop, or the reference of its AC island) takes `PAC` and `PDC` as starting guesses only, with any values and signs. A droop converter's `PDC` is still its $P_{SET}$.
- A fixed-power converter takes exactly one of `PAC` and `PDC` as its set-point; the other follows through the station and the losses. Giving both is an error, except for a converter with `VAC` given and `VDC` `*` that becomes the reference of its AC island.
- With a station and no `LOSS` fields, `EFF` must be given, and it relates `PDC` to the converter-node power $P_c$, not to `PAC`.

A converter with `VAC` given and `VDC` `*` may leave both `PAC` and `PDC` as `*` when it becomes the reference of its AC island: its power then balances the island. If it does not become the reference, the record is refused, because nothing else fixes its power.

### DC Grids and AC Islands

- **Every DC grid needs at least one in-service converter with `VDC` given**, constant voltage or droop. Two constant-voltage converters on one DC bus are refused; two droop converters on one DC bus are allowed.
- A DC bus carries no equipment of its own: a SLACK, GENER or SVC on a DC bus is an error. Power enters and leaves a DC grid only through ACDC converters. LFRESV on a DC bus sets the voltage magnitude and ignores the angle.
- `VAC` is refused on a bus whose voltage something else already holds: the slack bus, a bus with an in-service PV generator, a bus whose voltage an SVC controls, or a bus where another converter sets `VAC`.
- A converter with `VAC` given can be the **reference of an AC island** that has no SLACK record (see [Slack Bus](#slack-bus)). Such a converter must not also hold the DC voltage, so a converter with `VDC` given, constant or droop, cannot be an island reference, and a droop converter that would become one is refused.

### Converter Results

In the Helios text interface, the display menu offers `C : AC/DC Converters` when the case has converters. It asks for a converter name or `A` for all. For each converter the table gives `PAC`, `QAC` and `PDC`, the converter-node voltage $V_c$ and powers $P_c$ and $Q_c$, the station loss $P_{AC} - P_c$, the converter loss $P_c - P_{DC}$ and their sum. Its mode column names how each converter's power is set:

| Mode | Meaning |
|------|---------|
| `PQ` | Fixed power, fixed `QAC` |
| `PV` | Fixed power, `VAC` given |
| `VDC` | Constant DC voltage |
| `REF` | Reference of its AC island |
| `DROOP` | Droop converter on its law, inside or outside its deadband |
| `LIMIT` | Droop converter held at `PMIN` or `PMAX` |

`X` (export) then writes the table to a file; a name ending in `.csv` gives the columns

```
name,ac_bus,dc_bus,status,mode,qctl,pac_mw,qac_mvar,pdc_mw,loss_mw,direction,vc_pu,pc_mw,qc_mvar,pstation_mw,pconv_mw
```

where `loss_mw` is $P_{AC} - P_{DC}$, the sum of the station and converter losses.

When the data are dumped, constant-voltage and island-reference converters are written with their solved `PAC` and `PDC`, which read back as starting guesses, so a dumped case solves to the same point. A droop converter keeps its $P_{SET}$ in `PDC`; its solved power appears in the converter table only.

### Solver Outcomes

Two outcomes are specific to AC-DC cases. Both end the solve as not converged and print a message naming the element:

| Status | Cause | Message |
|--------|-------|---------|
| `NO_DC_REGULATION` | A DC grid has no converter regulating its voltage: no constant-voltage converter, and every droop converter is inside its deadband or at `PMIN` or `PMAX` | `the DC grid containing BUSDC '<name>' has no converter regulating its voltage` |
| `CONVERTER_INFEASIBLE` | A converter cannot deliver the `PDC` it must through its losses and station, or free converter powers form a ring | `ACDC '<name>' cannot deliver PDC = <p> MW: its losses and station allow at most <pmax> MW at the PCC voltage reached` (for the first cause) |

In non-interactive use both exit with status `2`, see [Exit Status](#exit-status). In the C API, `helios_get_solver_status` returns `5` for `NO_DC_REGULATION` and `6` for `CONVERTER_INFEASIBLE`, and `helios_get_last_error` carries the message. A DC bus reports bus type `4` (DC).

### Example

The DC link of `case5_ptp`, one of the [MatACDC benchmark cases](/test-systems/#power-flow-benchmarks): converter `C1` at AC bus `2` draws 60 MW from the AC grid and injects -40 Mvar, while `C2` at AC bus `3` holds the DC voltage at 1 pu and the voltage of its PCC at 1 pu, starting from a `PAC` guess of 0. Both use quadratic losses and a station.

```
BUSDC D1 345 ;
BUSDC D2 345 ;
LINE LD1-2 D1 D2 61.893 0. 0. 0. 1 ;
ACDC C1 2 D1 60 -40 * * * * * * * * * * 1.103 0.887 4.371 2.885 345 0.0015 0.1121 0.0887 0.0001 0.16428 1 ;
ACDC C2 3 D2 0 * 1 * 1 * * * * * * * 1.103 0.887 4.371 2.885 345 0.0015 0.1121 0.0887 0.0001 0.16428 1 ;
```

### Validation and Converting MatACDC Data

The Helios AC-DC power flow is validated against MatACDC 1.0 (J. Beerten, KU Leuven) on its four published DC cases, run as published with converter stations, quadratic losses and droop: `case5_stagg_HVDCptp`, `case5_stagg_MTDCslack`, `case5_stagg_MTDCdroop` and `case24_ieee_rts1996_MTDC`. The largest differences are $9.1\times10^{-13}$ pu on AC, DC and converter-node voltages, $8.8\times10^{-11}$ degrees, $6.7\times10^{-12}$ MW and $1.2\times10^{-10}$ Mvar. The converted cases are listed under [Test Systems](/test-systems/#power-flow-benchmarks).

A MatACDC case maps onto the ACDC record field by field:

- `rtf xtf bf rc xc` go to `RTF XTF BF RC XC`, multiplied by `baseMVA/baseMVAac` (the factor MatACDC applies itself when it converts station data to the AC base; it is 1 in the four published cases). `basekVac` goes to `KVC`, and `LossA LossB` to `LOSSA LOSSB`.
- `LossCrec` goes to `LOSSCI` and `LossCinv` to `LOSSCR`: MatACDC applies `LossCrec` when the converter-node power it injects into the AC grid is positive, which is inverter operation, while `LOSSCR` here means physical rectification.
- `P_g` and `Q_g` are injections into the AC grid, so `PAC = -P_g` and `QAC = Q_g`; `Vtar` goes to `VAC`.
- A DC slack converter holds `VDC` at the `busdc` voltage. A droop converter takes `KDROOP = 1/DROOP` (MatACDC's unit is pu of voltage per MW), `PDC = -Pdcset`, `VDC = Vdcset` and `DVDB = dVdcset`.
- A PV converter on a bus with a PV generator becomes fixed `QAC = 0`, which is what MatACDC does with it internally.
- BUSDC `VNOM` is MatACDC's `basekVdc`. With `pol = 2` a DC line's `R` is `r * basekVdc^2 / baseMVAdc` Ω; with `pol = 1` it is twice that, because the pole-to-neutral base $2\,V_{NOM}^2/S_B$ equals MatACDC's `pol = 2`.

## Transformer Ratio Adjustment for Voltage Control

The ratio of a designated transformer can be adjusted to bring a controlled voltage inside a deadband $[V_{des} - \epsilon,\; V_{des} + \epsilon]$, where $V_{des}$ is the desired voltage and $\epsilon$ is the tolerance.

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
| `NBPOS` | Total number of tap positions (including first and last) | |
| `TOLV` | Voltage tolerance $\epsilon$ | pu |
| `VDES` | Desired voltage $V_{des}$ | pu |

### Via LTC-V Record

The second way to specify ratio adjustment is through a separate LTC-V record. This is more natural in association with a TRANSFO record.

```
LTC-V NAME CON_BUS NFIRST NLAST NBPOS TOLV VDES ;
```

| Field | Description | Unit |
|-------|-------------|------|
| `NAME` | Name of the controlled transformer (max 20 characters) | |
| `CON_BUS` | Controlled bus (max 8 characters) | |
| `NFIRST` | Ratio at first tap position (lower bound) | % |
| `NLAST` | Ratio at last tap position (upper bound) | % |
| `NBPOS` | Total number of tap positions (including first and last) | |
| `TOLV` | Voltage tolerance $\epsilon$ | pu |
| `VDES` | Desired voltage $V_{des}$ | pu |

A transformer can be controlled by a **single tap changer only**. The LTC-V record can also be associated with a TRFO record, provided that no adjustment is specified in the TRFO record itself.

Only this seven-field linear-ratio form is supported; there is no per-tap reactance variant.

## Phase-Shifting Transformer Adjustment (PSHIFT-P)

The phase angle of a transformer can be adjusted to bring the active power flow in a monitored branch inside a deadband $[P_{des} - \epsilon,\; P_{des} + \epsilon]$. The adjustment mechanism is similar to the in-phase ratio adjustment described above.

```
PSHIFT-P CONTRFO MONBRANCH PHAFIRST PHALAST NBPOS SIGN PDES TOLP ;
```

| Field | Description | Unit |
|-------|-------------|------|
| `CONTRFO` | Name of the transformer whose phase angle is adjusted (max 20 characters, defined in a TRFO or TRANSFO record). If the transformer does not exist, the record is ignored with a warning | |
| `MONBRANCH` | Name of the branch where active power $P$ is monitored (max 20 characters, defined in a LINE, TRFO, or TRANSFO record). $P$ is the active power leaving the first bus of the branch record | |
| `PHAFIRST` | Phase angle $\phi$ at first tap position (lower bound) | degrees |
| `PHALAST` | Phase angle $\phi$ at last tap position (upper bound) | degrees |
| `NBPOS` | Number of tap positions | |
| `SIGN` | Direction indicator: `1` means $\phi$ must increase to increase power flow; `-1` means decrease. Any other value causes the program to stop | |
| `PDES` | Desired active power flow | MW |
| `TOLP` | Tolerance $\epsilon$ | MW |

The phase angle $\phi$ at tap position $p$ ($1 \le p \le \text{NBPOS}$) is:

$$
\phi = \text{PHAFIRST} + \frac{p-1}{\text{NBPOS}-1}(\text{PHALAST} - \text{PHAFIRST})
$$

The initial phase angle from the `PHI` field of the TRANSFO record is adjusted to the nearest tap position before starting the power flow computation.

A sensitivity analysis determines whether the phase angle should be increased or decreased. If this analysis indicates a direction opposite to SIGN, a warning is issued and SIGN is ignored. On output, SIGN is set to the value from the sensitivity analysis.

Only one PSHIFT-P record per transformer is allowed. The PSHIFT-P record is intended for use with a TRANSFO record, but can also be used with a TRFO record (in which case the angle is initialized to zero).

A transformer cannot be controlled by both an LTC-V and a PSHIFT-P record.

A detailed form with per-tap data (10 + 4k fields) is also accepted.

:::caution[Records that are not supported]
Two records of the historical Fortran engine are rejected with a hard error rather than silently ignored:

- **`PSHIFT-I`** (current-controlled phase shifter): never adjusted by the old engine either, so nothing is lost by removing it from the data.
- **`TURLIM`** (legacy active power limit record): use the 12/13-field GENER variant above, which carries PMIN, PMAX and PART.

Records that are not part of the power-flow format at all (`SYNC_MACH`, `INJEC`, `DCTL`, and the rest of the dynamic data) are skipped with a warning, so a combined data file can be handed to the power flow unchanged.
:::

## Zone and Cut Aggregation

Two optional records group equipment for reporting. They do not affect the solution.

```
BUSPART ZONE_NAME BUS_NAME PARTP PARTQ ;
```

| Field | Description |
|-------|-------------|
| `ZONE_NAME` | Zone name; the zone is created on first use |
| `BUS_NAME` | Bus to include in the zone (max 8 characters) |
| `PARTP` | Active power participation weight of this bus in the zone |
| `PARTQ` | Reactive power participation weight of this bus in the zone |

Zones drive the zone-power display and the zone-wide load and generation changes of the modify menu. Buses with unrecognised names are skipped.

```
BRAPART CUT_NAME BRANCH_NAME BUS_NAME SIGN ;
```

| Field | Description |
|-------|-------------|
| `CUT_NAME` | Cut name; the cut is created on first use |
| `BRANCH_NAME` | Branch to include in the cut (max 20 characters) |
| `BUS_NAME` | One endpoint of the branch, fixing the direction of the flow that is summed |
| `SIGN` | `+1` or `-1`, applied to that branch's contribution |

The cut power is the signed sum of the member branch flows, reported per branch and as a total.

## Bus Voltages: Initial Values and Results (LFRESV)

On output, the power flow produces a file with the computed bus voltage magnitudes and phase angles. These are stored in LFRESV records. The syntax is:

```
LFRESV BUS MODV PHASV ;
```

| Field | Description | Unit |
|-------|-------------|------|
| `BUS` | Bus name (max 8 characters) | |
| `MODV` | Voltage magnitude | pu |
| `PHASV` | Voltage phase angle, referenced to slack bus | radians |

:::note
If LFRESV records are provided as input, they are used as initial voltages for Newton iterations.
:::

:::note
Default initialization: PQ buses start at 1 pu magnitude and 0 angle; PV buses start at the generator-specified voltage and 0 angle.
:::

:::note
The output LFRESV records can be fed back as input. This results in zero Newton iterations (round-trip property). This is an easy way to verify that system data come with their corresponding voltages.
:::

:::note
LFRESV is the output that initializes RAMSES dynamic simulation.
:::

:::note
The exported operating-point file (**Add Helios results to data** in the GUI, `write_voltrat()` in the API) contains one LFRESV record per bus plus one TRANSFO record per in-service LTC transformer, carrying its *solved* ratio. Hand-maintained operating-point files (e.g. `volt_rat_B.dat` of the Nordic test system) often use TRFO records instead. The two styles are interchangeable as RAMSES input: RAMSES ignores the LTC fields of a TRFO record (see the record-sharing table below), and dynamic tap-changer behaviour is defined by the DCTL LTC records of the dynamic data.
:::

## Computation Control Parameters

The power flow uses Newton-Raphson iterations to solve the power flow equations. Convergence is achieved when both the active and reactive power mismatches fall below specified thresholds, all transformer ratio and phase-shift controls are satisfied, and all generators and SVCs are within their reactive limits.

Three convergence indices are used:
- $\epsilon_P$: largest absolute mismatch of the active power equations
- $\epsilon_Q$: largest absolute mismatch of the reactive power equations
- $\epsilon_S$: largest apparent power mismatch, used to trigger limit checks (via `$MISQLIM`), factorization reuse (via `$MISBLOC`), and transformer adjustments (via `$MISADJ`)

The following records control the computation. Each record starts with `$` and has a single numeric field; a known `$` record with any other field count is a hard error, and an unknown `$` key is ignored.

| Parameter | Default | Unit | Description |
|-----------|---------|------|-------------|
| `$SBASE` | 100 | MVA | System base power (on which pu values are expressed) |
| `$TOLAC` | 0.1 | MW | Convergence tolerance on active power mismatch ($\epsilon_P$) |
| `$TOLREAC` | 0.1 | Mvar | Convergence tolerance on reactive power mismatch ($\epsilon_Q$) |
| `$NBITMA` | 20 | | Maximum number of Newton iterations |
| `$MISQLIM` | 20 | MVA | Apparent power mismatch threshold below which generator/SVC reactive limits are checked and enforced (set to 0 to skip) |
| `$MISBLOC` | 10 | MVA | Apparent power mismatch threshold below which the Jacobian factorization reuses the previous pivot ordering. Jacobian values are recomputed at every iteration regardless |
| `$MISADJ` | 10 | MVA | Apparent power mismatch threshold below which transformer ratios and phase shifts are adjusted (set to 0 to skip) |
| `$DIVDET` | 0 | | Set to 1 to activate divergence detection; 0 to skip |
| `$PLIM` | 1 | | 1 = the slack generator's PMIN/PMAX are bypassed during initial P clamping; 0 = the slack is clamped like any other generator |

:::note
Divergence is detected when $\varphi(k) > 1.1\,\varphi(k-1)$, where:

$$\varphi(k) = \sum_i \sqrt{(f_i - P_i^o)^2 + (g_i - Q_i^o)^2}$$

Under normal convergence, $\varphi$ decreases at each iteration; an increase signals divergence. The test is temporarily suspended following limit adjustments or transformer ratio changes, as these cause increases in $\varphi$ unrelated to divergence.
:::

`$PLIM` only affects 12/13-field GENER records, the only ones that carry real active power limits.

## Exit Status

In non-interactive use (`-t` command file mode and pipe mode), Helios reports the outcome of the run through its process exit status:

| Exit | Meaning |
|------|---------|
| `0` | Converged, the results are usable |
| `1` | Input or usage error: bad command file, unreadable data file, parse failure, unknown command |
| `2` | The solve ran but did not converge: maximum iterations, divergence, a singular Jacobian, or one of the two [AC-DC outcomes](#solver-outcomes). Results may still have been written, but they are **not** a valid power-flow solution |

Only `0` means the results can be trusted. Where a command file modifies the system and re-solves, the status reflects the final solve. The interactive TUI always exits `0`.

Each non-interactive run also writes one machine-readable line to stderr:

```
helios: status: CONVERGED (2 iterations)
helios: status: NOT_CONVERGED (max iterations)
helios: status: NOT_CONVERGED (diverged)
helios: status: NOT_CONVERGED (singular)
helios: status: NOT_CONVERGED (no DC voltage regulation)
helios: status: NOT_CONVERGED (converter power infeasible)
helios: status: NOT_RUN
```

`NOT_RUN` means no solve was requested (for example `$NBITMA 0`), which exits `0`. Scripts should use the exit status and this line rather than parsing stdout.

These values are shared with the Helios C API, where `HELIOS_OK` is `0` and `HELIOS_NOT_CONVERGED` is `2` (`1` is reserved and never returned by the API). `HELIOS_NOT_CONVERGED` is `2` from Helios 1.4.1 onward; in 1.3.0 and earlier it was `1`. The `stepss.helios.HeliosSession` wrapper exposes convergence as the boolean `pf.converged` and the `pf.solver_status` enum, neither of which is affected by the numbering.

## Record Sharing Between Power Flow and RAMSES

The following table summarises which records are used by the power flow and by RAMSES respectively.

| Record | Power flow | RAMSES |
|--------|-----|--------|
| BUS | All 6 fields (QSHUNT optional) | First 2 fields (NAME, VNOM) |
| BUSDC | All fields | All fields |
| LINE | All fields | All fields |
| SWITCH | All fields | All fields |
| NRTP | All fields | All fields |
| TRANSFO | All fields | All fields |
| TRFO | All fields | Fields 1 to 9 and 15 only |
| SHUNT | Ignored | All fields |
| GENER | All fields | Ignored |
| SVC | All fields | Ignored |
| ACDC | All fields | Ignored |
| SLACK | Used | Used |
| LFRESV | Input: initial values; Output: solution | Input: initial values for RAMSES |
| LTC-V | Used | Ignored |
| PSHIFT-P | Used | Ignored |
| BUSPART, BRAPART | Used for reporting | Ignored |

## Annotated One-line Diagram

Helios can render a solved case onto an SVG drawing of the network instead of, or alongside, reading the same numbers off a table.

A **template** is an SVG file with placeholder codes typed into its text elements as plain text. Any general-purpose SVG editor works: Helios finds a placeholder by its text content when it renders, not by any tool-specific metadata. A placeholder is a code letter directly followed by its argument, with no space, so `%A` (bus voltage magnitude) applied to bus `E` is written `%AE`. A branch code takes the branch name and the bus end separated by a comma: `%D` (P flow) on branch `D-E` at its `E` end is `%DD-E,E`.

| Code | Argument | Value |
|---|---|---|
| `%A` | bus | voltage magnitude (pu) |
| `%B` | bus | voltage (kV) |
| `%C` | bus | angle (degrees) |
| `%D` | branch, bus | P flow at that bus end (MW) |
| `%E` | branch, bus | Q flow at that bus end (Mvar) |
| `%F` | branch | loading fraction |
| `%G` | generator | P (MW) |
| `%H` | bus | shunt Q (Mvar) |
| `%J` | transformer | tap position |
| `%K` | generator | Q (Mvar) |
| `%L` | SVC | Q (Mvar) |
| `%R` | bus | load P (MW) |
| `%S` | bus | load Q (Mvar) |
| `%T` | branch | breaker status, blank or `X` |
| `%U` | generator | breaker status, blank or `X` |

:::caution[Codes that are not supported]
`%I` and `%M` through `%Q` are recognised but not implemented: they need zone and sensitivity data the model does not carry, and render as the literal word `unknown`. They are documented here, not omitted, so that a code written into a template by mistake has something explaining the `unknown` it produces rather than nothing.
:::

Every **Run power flow** in the GUI runs this substitution; from Python, `pf.write_diagram('template.svg', 'diagram.svg')` does the same, see [Power Flow with Helios](/python/helios/).

### In STEPSS GUI

The template is an optional third slot on the *System Data* tab, alongside the data and disturbance files (the disturbance file on that tab is optional too, which is what makes a power-flow-only case a normal thing to load). Its button opens the named file in the platform's default SVG viewer or editor, for authoring or checking placeholders.

Every **Run Power Flow** renders the template with the solved values and opens the result in a window of its own. Each run opens a new window, offset from the last one, so two runs can be compared side by side. The window offers Fit, Zoom in and Zoom out as buttons; the wheel zooms anchored at the pointer; dragging pans; double-click returns to Fit; and Save as PNG and Save as SVG save the result. Save as PNG saves the whole diagram, not only what is currently in view. A run that does not converge still opens a window, with a banner carrying the same status the main window's status bar shows.

**Worked example:** [SPS-L/stepss-6-bus-MG](https://github.com/SPS-L/stepss-6-bus-MG), bundled in STEPSS GUI under *File > Open Examples*, ships `6bus.svg`, a template carrying these placeholder codes; Run Power Flow fills it in with the solved voltages, angles and flows.

## Next Steps

- [Reference Frames & Initialization](/user-guide/reference-frames/), Understand how RAMSES initializes from the power flow solution
- [Dynamic Data Records](/user-guide/dynamic-models/), Define synchronous machines, injectors, and controllers
