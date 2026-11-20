---
title: Monitoring
description: Discrete controllers that monitor speed and voltage and stop or annotate a RAMSES simulation
---

The `DCTL` record these models are entered with, and the rules on model names, are on the [Discrete Controller Models](/models/discrete-controllers/) page.

## SIM_MINMAXSPEED (`dctl_sim_minmaxspeed`): Speed Monitoring (Min/Max)

### Description

A **simulation monitoring** controller that checks whether any synchronous machine speed violates upper or lower bounds. If a violation persists beyond a deadtime, the controller logs a warning or stops the simulation, depending on the `stop_sim` flag. It is used to automatically terminate simulations that have become numerically unstable or that have reached an unacceptable operating state.

### Logic Description

At each evaluation, the controller scans all synchronous machines and checks:

$$
\text{if } \omega > \omega_{max} \text{ or } \omega < \omega_{min}: \quad \text{record violation time}
$$
$$
\text{if violation duration} > T_{deadtime}: \quad \text{warn or stop simulation}
$$

### Parameters

| Field | Working variable | Description |
|-------|-----------------|-------------|
| `omega_max` | `w(1)` | Upper speed limit (pu) |
| `omega_min` | `w(2)` | Lower speed limit (pu) |
| `deadtime` | `w(3)` | Deadtime before action (s) |
| `stop_sim` | `w(4)` | 1 = stop simulation on violation, 0 = warn only |

4 fields required. Internal: `w(5)` = last violation time.

Parameter names exported: `SPEEDMIN`, `SPEEDMAX`, `DEADTIME`.

### Usage Example

<details>
<summary>Show the data record</summary>

```
DCTL  SIM_MINMAXSPEED  SPEEDMON
      # SPEEDMIN: lowest machine speed allowed (pu)
      0.5
      # SPEEDMAX: highest machine speed allowed (pu)
      1.2
      # start_time: monitoring starts at this time (s)
      0.5
      # warn_only: 0 = stop the simulation on a violation, otherwise log a warning only
      0
;
```

</details>

---

## SIM_MINMAXVOLT (`dctl_sim_minmaxvolt`): Voltage Monitoring (Min/Max)

### Description

Analogous to `dctl_sim_minmaxspeed` but for **bus voltages**. The controller scans all buses and checks whether any voltage violates the specified bounds. If the violation persists for longer than the deadtime, a warning is logged or the simulation is terminated.

### Logic Description

$$
\text{if } V > V_{max} \text{ or } V < V_{min}: \quad \text{record violation time}
$$
$$
\text{if violation duration} > T_{deadtime}: \quad \text{warn or stop simulation}
$$

### Parameters

| Field | Working variable | Description |
|-------|-----------------|-------------|
| `V_max` | `w(1)` | Upper voltage limit (pu) |
| `V_min` | `w(2)` | Lower voltage limit (pu) |
| `deadtime` | `w(3)` | Deadtime before action (s) |
| `stop_sim` | `w(4)` | 1 = stop on violation, 0 = warn only |

4 fields required. Internal: `w(5)` = last violation time.

Parameter names exported: `VMIN`, `VMAX`, `DEADTIME`.

### Usage Example

<details>
<summary>Show the data record</summary>

```
DCTL  SIM_MINMAXVOLT  VOLTMON
      # VMIN: lowest bus voltage allowed (pu)
      0.80
      # VMAX: highest bus voltage allowed (pu)
      1.15
      # start_time: monitoring starts at this time (s)
      1.0
      # warn_only: 0 = stop the simulation on a violation, otherwise log a warning only
      0
;
```

</details>

---

## VOLT_VAR (`dctl_voltage_variability`): Voltage Variability Monitor

The data-file model name is `VOLT_VAR`.

### Description

Computes a **running Exponential Moving Average (EMA)** of voltage variability (variance) across a list of monitored buses. It is used to assess power quality metrics such as voltage flicker or ramping caused by variable renewable energy sources.

The EMA uses two decay constants ($\lambda_1$, $\lambda_2$) derived from the averaging time window, enabling a computationally efficient recursive estimation:

$$
\text{EMA}(t) = \lambda_1 \cdot \text{EMA}(t-1) + (1 - \lambda_1) \cdot V(t) + (\lambda_1 - \lambda_2)(V(t) - V(t-1))
$$

The controller accumulates per-bus variances and a system-wide sum.

### Parameters

| Field | Description |
|-------|-------------|
| `aver_time_window` | Averaging time window (s) for EMA computation |
| `nb_list` | Number of buses to monitor (bus names follow in subsequent RAMSES data records) |

2 fields required. Only one `VOLT_VAR` controller may exist per simulation. Parameters are stored in module-level variables (`volt_var_mod`) rather than `w(*)`.

### Usage Example

<details>
<summary>Show the data record</summary>

```
DCTL  VOLT_VAR  VVAR
      # window: averaging time window (s)
      60.0
      # nb_list: number of most variable buses written to the log at the end (an integer)
      5
;
```

</details>
