---
title: Protection and Control
description: Protection, ride-through and control discrete controllers in RAMSES
---

The `DCTL` record these models are entered with, and the rules on model names, are on the [Discrete Controller Models](/models/discrete-controllers/) page.

The protection and ride-through models share a definite-time sequence: the
monitored quantity crosses a threshold, a timer runs, and the trip is issued only
if the quantity is still beyond the threshold when the timer expires. A quantity
that recovers first resets the timer, so a transient dip passes without action.

<img src="/images/models/dctl-relay-timing-light.svg"
     alt="Definite-time relay timing diagram. The monitored voltage dips below the threshold and a timer starts, but the voltage recovers before the delay expires and the timer resets with no trip. A second, deeper dip keeps the voltage below the threshold for the full delay, and the output goes to trip when the timer completes."
     class="dark:sl-hidden" />
<img src="/images/models/dctl-relay-timing-dark.svg"
     alt="Definite-time relay timing diagram. The monitored voltage dips below the threshold and a timer starts, but the voltage recovers before the delay expires and the timer resets with no trip. A second, deeper dip keeps the voltage below the threshold for the full delay, and the output goes to trip when the timer completes."
     class="light:sl-hidden" />

## UVPROT (`dctl_uvprot`): Under-Voltage Protection Relay

### Description

Trips a **generator or injector** when the voltage at a monitored bus falls below a threshold for a sustained time delay. This models definite-time under-voltage protection relays.

### Logic Description

The relay monitors voltage $V_{meas}$ at a specified bus:

$$
\text{if } V_{meas} < V_{\min}: \quad \text{start timer}
$$
$$
\text{if timer} \ge T_{delay}: \quad \text{trip generator}, \quad \text{state} \leftarrow -1 \text{ (latched)}
$$

Once tripped (`w(8) = -1`), the controller is permanently latched and takes no further action.

### Parameters

| Field | Working variable | Description |
|-------|-----------------|-------------|
| `bus_name` | `w(1)` | Monitored bus name |
| `gen_name` | `w(2)` | Generator/injector to trip |
| `Vmin` | `w(3)` | Under-voltage pickup threshold (pu) |
| `T_delay` | `w(4)` | Time delay before tripping (s) |

Internal variables: `w(5)` = measured voltage, `w(6)` = start time of violation, `w(7)` = simulation time, `w(8)` = controller state.

### Usage Example

<details>
<summary>Show the data record</summary>

```
DCTL  UVPROT  UV_GEN1
      # bus: monitored bus
      BUS_HV
      # generator: must name an existing synchronous machine; RAMSES 3.84 does not use it to pick the tripped unit
      GEN1
      # Vmin: voltage threshold, 0 < Vmin <= 1 (pu)
      0.85
      # T_delay: time below Vmin before tripping, > 0 (s)
      0.5
;
```

</details>

---

## UVLS (`dctl_uvls`): Under-Voltage Load Shedding

### Description

Sheds load in **multiple steps** in response to sustained voltage depression. The controller integrates the area between the measured voltage and a threshold (energy integral criterion) and triggers load shedding when the area exceeds a limit $C$. This prevents unnecessary shedding for short transient dips.

After each shedding step, the controller resets the integral and waits a minimum delay before the next step.

### Logic Description

Area integral (trapezoidal):

$$
A(t) = \int_{t_{start}}^{t} \max(V_{th} - V_{meas}, 0) \, dt'
$$

Shedding condition:

$$
\text{if } A \ge C \text{ and } (t - t_{last}) \ge T_{\min}: \quad \text{shed load step}
$$

Amount shed per step (bounded):

$$
\Delta P_{shed} = \text{clip}\left(K \cdot A, \; P_{\min,step}, \; P_{\max,step}\right)
$$

Controller terminates when total shedding reaches the fraction `frac_load` of initial load or when `max_steps` is exhausted.

### Parameters

| Field | Working variable | Description |
|-------|-----------------|-------------|
| `bus_name` | `w(1)` | Monitored bus |
| `load_name` | `w(2)` | Controlled load (injector) |
| `V_th` | `w(3)` | Voltage threshold (pu) |
| `C` | `w(4)` | Maximum area $\int(V_{th}-V) \, dt$ before shedding (pu·s) |
| `T_min` | `w(5)` | Minimum delay between steps (s) |
| `T_max` | `w(6)` | Maximum delay between steps (s) |
| `frac_load` | `w(7)` | Maximum fraction of load that may be shed |
| `K` | `w(8)` | Gain: area → shed amount |
| `P_min_step` | `w(9)` | Minimum load shedding per step (MW) |
| `P_max_step` | `w(10)` | Maximum load shedding per step (MW) |
| `max_steps` | `w(11)` | Maximum number of shedding steps |

Internal variables: `w(12)`–`w(18)` (previous voltage, timers, area accumulator, step counter, total shed).

### Usage Example

<details>
<summary>Show the data record</summary>

```
DCTL  UVLS  UVLS1
      # bus: monitored bus
      BUS_MV
      # load: injector shed by the controller (needs parameters P0 and Q0)
      LOAD1
      # V_th: voltage threshold (pu)
      0.90
      # C: area of voltage deficit that triggers shedding (pu s)
      0.5
      # T_min: minimum delay from arming to shedding (s)
      5.0
      # T_max: maximum delay from arming; shedding is forced after it (s)
      20.0
      # frac_load: fraction of the load that may be shed, capped at 1
      0.3
      # K: gain: shed amount per unit of mean voltage deficit (MW/pu)
      2.0
      # P_min_step: minimum load shed per step (MW)
      5.0
      # P_max_step: maximum load shed per step (MW)
      50.0
      # max_steps: maximum number of shedding steps
      5
;
```

</details>

---

## `FRT` (`dctl_FRT`): Fault Ride-Through Controller

### Description

Implements a **piecewise-linear voltage–time FRT envelope** for an inverter-based generator (IBG). It monitors the bus voltage of the controlled injector and trips the unit if the voltage stays below the FRT envelope longer than allowed by the characteristic.

The FRT envelope is defined by four (voltage, time) breakpoints: $(V_1, t_1), (V_2, t_2), (V_3, t_3), (V_4)$. If the voltage is above the envelope at all times, no action is taken. If it falls below the envelope for more than the corresponding time limit, the unit is tripped.

### Logic Description

The FRT curve defines the minimum voltage $V(t)$ that must be sustained:

| Segment | Condition |
|---------|-----------|
| $V \ge V_1$ | Always ride-through |
| $V_2 \le V < V_1$ | Must recover within $t_1$ s |
| $V_3 \le V < V_2$ | Must recover within $t_2$ s |
| $V_4 \le V < V_3$ | Must recover within $t_3$ s |
| $V < V_4$ | Immediate trip |

Two internal timers (`w(8)`, `w(9)`) track time spent in violation zones.

### Parameters

| Field | Working variable | Description |
|-------|-----------------|-------------|
| `inj_name` | `w(10)` | Controlled injector |
| `Val1` | `w(1)` | Voltage threshold 1 (pu), upper FRT boundary |
| `t1` | `w(2)` | Time limit for zone 1 (s) |
| `Val2` | `w(3)` | Voltage threshold 2 (pu) |
| `t2` | `w(4)` | Time limit for zone 2 (s) |
| `Val3` | `w(5)` | Voltage threshold 3 (pu) |
| `t3` | `w(6)` | Time limit for zone 3 (s) |
| `Val4` | `w(7)` | Voltage threshold 4 (pu), below this: trip immediately |

8 fields required. Field 1 is the injector name, fields 2–8 map to `Val1, t1, Val2, t2, Val3, t3, Val4`.

### Usage Example

<details>
<summary>Show the data record</summary>

```
DCTL  FRT  FRT_WTG1
      # injector: injector tripped by the relay
      WT1
      # Val1: trip voltage between t1 and t2 after timer 1 starts (pu)
      0.30
      # t1: end of the no-trip period of timer 1 (s)
      0.15
      # Val2: trip voltage after t2 on timer 1 (pu)
      0.70
      # t2: time on timer 1 from which Val2 applies (s)
      0.5
      # Val3: voltage below which timer 1 starts; must be below Val4 (pu)
      0.50
      # t3: time on timer 2 from which Val4 applies (s)
      1.5
      # Val4: voltage below which timer 2 starts; both timers reset when the voltage rises above it (pu)
      0.90
;
```

</details>

---

## dctl_injprot: Injector Protection

:::note
Callable since 3.79. Earlier releases compiled this model under no name, so a data file referring to it was rejected.
:::

### Description

A **generic injector protection** relay that monitors any observable variable of an injector (e.g., current magnitude, active power, reactive power) and trips the injector if the variable goes outside prescribed bounds for a sustained time.

The controller identifies the variable to monitor by name from the injector's observable list, making it flexible and applicable to any injector model.

### Logic Description

$$
\text{if } x_{obs} < L_{lower} \text{ or } x_{obs} > L_{upper}: \quad \text{start timer}
$$
$$
\text{if timer} \ge T_{trip}: \quad \text{trip injector}, \quad \text{state} \leftarrow -1
$$

The controller latches once tripped and cannot reset. State variable `w(7)`:
- `1` = active (monitoring)
- `0` = idle (within bounds)
- `−1` = already tripped

### Parameters

| Field | Working variable | Description |
|-------|-----------------|-------------|
| `inj_name` | `w(1)` | Monitored/controlled injector name |
| `var_name` | `w(2)` | Observable variable name (from injector's observable list) |
| `lower_bound` | `w(3)` | Lower bound for the variable |
| `upper_bound` | `w(4)` | Upper bound for the variable |
| `T_trip` | `w(5)` | Time out-of-bounds before tripping (s) |

5 fields required.

### Usage Example

<details>
<summary>Show the data record</summary>

```
DCTL  injprot  PROT_WTG1
      # injector: injector tripped by the relay
      WT1
      # observable: name of an observable of that injector's model
      vt
      # lower_bound: lower bound on the observable, below upper_bound
      0.85
      # upper_bound: upper bound on the observable
      1.15
      # T_trip: read but not used in RAMSES 3.84, where the trip delay is fixed at 1 s (s)
      1.0
;
```

</details>

---

## dctl_losprot: Loss-of-Synchronism Protection

:::note
Callable since 3.79. Earlier releases compiled this model under no name, so a data file referring to it was rejected.
:::

### Description

Trips a **synchronous generator** when its rotor speed exceeds a maximum threshold for a sustained time, detecting loss of synchronism (pole slipping). The controller monitors the machine's per-unit rotor speed $\omega$ and triggers disconnection when $\omega > \omega_{max}$ for longer than the specified time delay.

### Logic Description

$$
\text{if } \omega > \omega_{max}: \quad \text{start timer}
$$
$$
\text{if timer} \ge T_{delay}: \quad \text{trip generator}, \quad \text{state} \leftarrow -1
$$

The timer resets if the speed returns within bounds. The controller latches permanently after tripping.

### Parameters

| Field | Working variable | Description |
|-------|-----------------|-------------|
| `gen_name` | `w(1)` | Controlled synchronous generator name |
| `omega_max` | `w(2)` | Maximum rotor speed threshold (pu) |
| `T_delay` | `w(3)` | Time delay before tripping (s) |

3 fields required. Internal variables: `w(4)` = measured speed, `w(5)` = violation start time, `w(6)` = current time, `w(7)` = state.

### Usage Example

<details>
<summary>Show the data record</summary>

```
DCTL  LOSPROT  LOS_GEN2
      # generator: synchronous machine tripped by the relay
      GEN2
      # omega_max: speed threshold, > 0 (pu)
      1.05
      # T_delay: time above omega_max before tripping, >= 0 (s)
      0.2
;
```

</details>

---

## line_prot (`dctl_line_prot`): Line Overcurrent Protection

The data-file model name is `line_prot` (or `dctl_line_prot`). RAMSES adds the `dctl_` prefix automatically.

### Description

Monitors the **apparent power flow on a set of lines** and trips them if they exceed their thermal rating (with a configurable oversize factor). It is designed to protect multiple lines simultaneously and disconnects any line whose flow exceeds `oversize_factor × S_max`.

The controller uses RAMSES' internal `smax_bra` array (maximum apparent power ratings from the network data) and reads real-time power flows via `pqbra`.

### Logic Description

For each monitored branch $k$:

$$
\text{if } |S_k| > \text{oversize\_factor} \times S_{max,k}: \quad \text{disconnect branch } k
$$

The action is immediate (no time delay); the oversize factor allows temporary overloads.

### Parameters

| Field | Working variable | Description |
|-------|-----------------|-------------|
| `oversize_factor` | `w(1)` | Allowed overload factor (e.g., 1.05 = 5% overload permitted) |
| `nb_lines` | `w(2)` | Number of protected lines |
| `line_1`, ... | `w(3-)` | Names of protected branches (space-separated) |

### Usage Example

<details>
<summary>Show the data record</summary>

```
DCTL  line_prot  LINEPROT1
      # oversize: trip threshold as a multiple of the branch rating
      1.05
      # nb_lines: number of protected branches
      2
      # branch: protected branch
      L1-L2
      # branch: protected branch
      L3-L4
;
```

</details>

---

## `PST` (`dctl_pst`): Phase-Shifting Transformer Control

### Description

Controls the phase angle (and thus the **active power flow**) of a phase-shifting transformer (PST) to regulate power flow on a monitored branch. It is structurally identical to `dctl_ltc` but acts on the PST angle rather than on voltage: the deadband is in MW (or pu power), and the controller moves the tap to keep active power within a band around the setpoint.

### Logic Description

Let $P_{meas}$ be the active power flow on the monitored branch and $P_{set}$ the setpoint (initialised at $t=0$):

$$
\text{if } |P_{meas} - P_{set}| > \delta P: \quad \text{start timer}
$$
$$
\text{if timer} \ge \tau_{delay}: \quad \text{advance/retard PST angle by } \Delta\phi
$$

The direction parameter defines whether increasing the tap increases or decreases power flow.

### Parameters

| Field | Working variable | Description |
|-------|-----------------|-------------|
| `pst_branch` | `w(1)` | PST branch name (must be type `trfo`) |
| `mon_branch` | `w(2)` | Monitored branch for power flow |
| `direction` | `w(3)` | Sign convention for power vs. Angle |
| `ratio_min` | `w(4)` | Minimum PST ratio (pu) |
| `ratio_max` | `w(5)` | Maximum PST ratio (pu) |
| `nb_positions` | `w(6)` | Number of positions |
| `half_deadband` | `w(7)` | Power half-deadband (pu) |
| `delay_first` | `w(8)` | First change delay (s) |
| `delay_next` | `w(9)` | Subsequent change delay (s) |

9 fields required. Internal variables: `w(10)` = power setpoint, `w(11)` = time of last change, `w(12)` = active delay, `w(13)` = state.

### Usage Example

<details>
<summary>Show the data record</summary>

```
DCTL  PST  PST_L1
      # branch: phase-shifting transformer, which is also the branch whose power is controlled
      PST-TR1
      # mon_branch: not read by RAMSES 3.84: any name
      LINE-MON
      # direction: sign of the phase change that raises the power (only the sign is used, 0 is refused)
      1
      # phase_min: minimum phase angle (deg)
      -30.
      # phase_max: maximum phase angle (deg)
      30.
      # nb_positions: number of tap positions, at least 2
      21
      # half_deadband: half of the power deadband (pu)
      0.02
      # delay_first: delay before the first tap change (s)
      30.0
      # delay_next: delay between subsequent tap changes (s)
      10.0
;
```

</details>

---

## `RT` (`dctl_rt`): Real-Time Simulation Control

### Description

Forces the RAMSES simulation to track **wall-clock time** at a configurable ratio, enabling hardware-in-the-loop (HIL) or real-time simulation testing. A ratio of 1.0 means the simulation runs in exact real time; a ratio of 2.0 allows the simulation to run up to twice as fast as real time (useful for digital twin applications).

An optional over-run tolerance parameter `allowed_overrun` specifies how far the simulation may lag behind real time before an error is triggered.

### Parameters

| Field | Working variable | Description |
|-------|-----------------|-------------|
| `ratio` | `w(1)` | Ratio to real time (1.0 = real time, >1 = faster) |
| `allowed_overrun` | `w(2)` | Allowed over-run before error (s), optional |

1 or 2 fields. Only one `DCTL RT` controller may be active per simulation.

Observable: `elapsed` (wall-clock elapsed time in seconds).

### Usage Example

<details>
<summary>Show the data record</summary>

```
DCTL  RT  RT_CTL
      # ratio: simulated time per second of wall time
      1.0
      # lead_time: how far the simulation may run ahead of scaled wall time (optional, default 0) (s)
      0.01
;
```

</details>

---

## `dctl_hvdc_lim`: HVDC LCC Limiter/Controller

:::note
Callable since 3.79. Earlier releases compiled this model under no name, so a data file referring to it was rejected.
:::

### Description

A discrete controller that **supervises and adjusts an LCC-HVDC link** (`twop_HVDC_LCC`) by:
- Moving rectifier and inverter transformer tap changers to maintain firing and extinction angles within desired ranges
- Triggering reduced-current or blocked operation when AC voltages are too low for normal commutation
- Setting the `alphamin`, `gammamin`, and `Idred` parameters of the HVDC model

It interacts directly with the HVDC two-port model's internal parameters.

### Logic Description

**Rectifier tap changer**: if $\alpha$ is outside $[\alpha_{min,des}, \alpha_{max,des}]$ for longer than `delay_rect`, move rectifier transformer tap.

**Inverter tap changer**: if $\gamma$ is outside $[\gamma_{min,des}, \gamma_{max,des}]$ for longer than `delay_inv`, move inverter transformer tap.

**Reduced-current control**: when $V_{dc}$ falls below $V_{min,des}$ or $V_{max,des}$ the controller switches the inverter to reduced-current mode (`inv_ctl = -1`) and sets $I_{red}$.

**Blocked operation**: if conditions are unrecoverable (very low AC voltage), the HVDC is blocked (`rec_ctl = 3`, `inv_ctl = 3`).

### Parameters

| Field | Working variable | Description |
|-------|-----------------|-------------|
| `hvdc_name` | `w(1)` | Target HVDC two-port device name |
| `nr_min` | `w(2)` | Minimum rectifier transformer ratio |
| `nr_max` | `w(3)` | Maximum rectifier transformer ratio |
| `nr_step` | `w(4)` | Rectifier tap step size |
| `ni_min` | `w(5)` | Minimum inverter transformer ratio |
| `ni_max` | `w(6)` | Maximum inverter transformer ratio |
| `ni_step` | `w(7)` | Inverter tap step size |
| `alpha_min_des` | `w(8)` | Desired minimum firing angle (degrees) |
| `alpha_max_des` | `w(9)` | Desired maximum firing angle (degrees) |
| `gamma_min_des` | `w(10)` | Desired minimum extinction angle (degrees) |
| `gamma_max_des` | `w(11)` | Desired maximum extinction angle (degrees) |
| `V_min_des` | `w(12)` | Minimum desired DC voltage (kV) |
| `V_max_des` | `w(13)` | Maximum desired DC voltage (kV) |
| `delay_rect` | `w(14)` | Delay between rectifier tap changes (s) |
| `delay_inv` | `w(15)` | Delay between inverter tap changes (s) |
| `alphamin` | `w(16)` | Minimum firing angle limit (degrees) |
| `Idred` | `w(17)` | Reduced DC current (kA) |
| `gammamin` | `w(18)` | Minimum extinction angle (degrees) |

18 fields required. Internal variables: `w(19)`–`w(22)` (operation modes and tap-change timers).

### Usage Example

<details>
<summary>Show the data record</summary>

```
DCTL  HVDC_LIM  HVDCLIM1
      # twop: HVDC_LCC two-port controlled
      HVDClink
      # nr_min: minimum rectifier transformer ratio
      0.85
      # nr_max: maximum rectifier transformer ratio
      1.15
      # nr_step: rectifier ratio step
      0.00625
      # ni_min: minimum inverter transformer ratio
      0.85
      # ni_max: maximum inverter transformer ratio
      1.15
      # ni_step: inverter ratio step
      0.00625
      # alpha_min_des: lower edge of the desired firing angle band (deg)
      15.0
      # alpha_max_des: upper edge of the desired firing angle band (deg)
      18.0
      # gamma_min_des: lower edge of the desired extinction angle band (deg)
      15.0
      # gamma_max_des: upper edge of the desired extinction angle band (deg)
      18.0
      # V_min_des: lower edge of the desired DC voltage band (kV)
      400.0
      # V_max_des: upper edge of the desired DC voltage band (kV)
      600.0
      # delay_rect: delay between rectifier tap changes (s)
      10.0
      # delay_inv: delay between inverter tap changes (s)
      10.0
      # alphamin: minimum firing angle (deg)
      5.0
      # deltaI: DC current reduction when alpha reaches alphamin and the inverter takes current control (kA)
      0.0
      # gammamin: minimum extinction angle (deg)
      15.0
;
```

</details>
