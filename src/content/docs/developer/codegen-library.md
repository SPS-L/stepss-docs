---
title: CODEGEN Blocks Library
description: Complete list of modeling blocks available in CODEGEN
---

CODEGEN provides a library of reusable modeling blocks for constructing user-defined models. Each block has input/output states and parameters (data values enclosed in braces `{}`).

:::caution
State names used as block inputs/outputs **must not** be enclosed in brackets. Brackets will be treated as part of the name, causing compilation errors.
:::

## Block Reference

### Algebraic & Mathematical

| Block | Description |
|-------|-------------|
| [`abs`](#abs) | Absolute value of input |
| [`algeq`](#algeq) | Algebraic equation |
| [`max1v1c`](#max1v1c) | Maximum between a state and a constant |
| [`max2v`](#max2v) | Maximum between two states |
| [`min1v1c`](#min1v1c) | Minimum between a state and a constant |
| [`min2v`](#min2v) | Minimum between two states |
| [`nint`](#nint) | Nearest integer to the input shifted by a constant |
| [`pwlin`](#pwlin) | Piecewise linear function of input |

### Transfer Functions

| Block | Description |
|-------|-------------|
| [`tf1p`](#tf1p) | First-order transfer function (one pole) |
| [`tf1plim`](#tf1plim) | First-order with non-windup output limits |
| [`tf1pvlim`](#tf1pvlim) | First-order with variable non-windup output limits |
| [`tf1p2lim`](#tf1p2lim) | First-order with rate limits and output limits |
| [`tf1p1z`](#tf1p1z) | Transfer function: one zero, one pole |
| [`tf2p2z`](#tf2p2z) | Transfer function: two real zeros, two real poles |
| [`tfder1p`](#tfder1p) | Derivative with one time constant |

### Integrators

| Block | Description |
|-------|-------------|
| [`int`](#int) | Integrator with time constant |
| [`inlim`](#inlim) | Integrator with non-windup limits |
| [`invlim`](#invlim) | Integrator with variable non-windup limits |

### Controllers

| Block | Description |
|-------|-------------|
| [`pictl`](#pictl) | Proportional-Integral (PI) controller |
| [`pictllim`](#pictllim) | PI with non-windup limit on integral term |
| [`pictl2lim`](#pictl2lim) | PI with limits on both integral and proportional terms |
| [`pictlieee`](#pictlieee) | PI with non-windup limit, IEEE-compliant |

### Limiters & Switching

| Block | Description |
|-------|-------------|
| [`lim`](#lim) | Limiter with constant bounds |
| [`limvb`](#limvb) | Limiter with variable bounds |
| [`db`](#db) | Deadband |
| [`hyst`](#hyst) | Hysteresis |
| [`switch`](#switch) | Select one of $n$ inputs based on a controlling state |
| [`swsign`](#swsign) | Switch between two inputs based on sign of a third |

### Frequency Estimation

| Block | Description |
|-------|-------------|
| [`f_inj`](#f_inj) | Estimate of frequency at bus of injector |
| [`ftwop_bus1`](#ftwop_bus1) | Estimate of frequency at first bus of two-port |
| [`ftwop_bus2`](#ftwop_bus2) | Estimate of frequency at second bus of two-port |

### Automata & Timers

| Block | Description |
|-------|-------------|
| [`fsa`](#fsa) | Finite State Automaton |
| [`tsa`](#tsa) | Two-state automaton (transitions based on signs of two inputs) |
| [`timer`](#timer) | Timer with piecewise-linear delay |
| [`timersc`](#timersc) | Timer with staircase delay |

---

## Block Details

### `abs`

Computes the absolute value: $y = |u|$

### `algeq`

Defines an algebraic equation: $0 = f(...)$

### `db`

Deadband block. Output is zero when input is within the deadband, otherwise the input minus the deadband threshold.

### `f_inj`

Estimates the local frequency at the connection bus of an injector, using voltage phasor derivatives.

### `fsa`

Finite State Automaton with user-defined states and transitions.

### `hyst`

Hysteresis block with upper and lower thresholds.

### `int`

Integrator: $T\dot{y} = u$, where $T$ is the time constant.

### `inlim`

Integrator with non-windup limits: $T\dot{y} = u$ with $y_{min} \le y \le y_{max}$.

### `invlim`

Integrator with variable (state-dependent) non-windup limits.

### `lim`

Static limiter: $y = \min(\max(u, y_{min}), y_{max})$

### `limvb`

Static limiter with variable bounds.

### `max1v1c` / `max2v`

Maximum between a state and a constant, or between two states.

### `min1v1c` / `min2v`

Minimum between a state and a constant, or between two states.

### `nint`

Nearest integer: $y = \text{nint}(u + c)$

### `pictl`

PI controller: $y = K_p \cdot e + K_i \int e \, dt$

### `pictllim`

PI controller with non-windup limit on the integral term.

### `pictl2lim`

PI controller with limits on both the integral term and the proportional + integral sum.

### `pictlieee`

PI controller with non-windup limit, following IEEE standard formulation.

### `pwlin`

Piecewise linear function defined by breakpoints.

### `switch`

Selects output from one of $n$ inputs based on the integer value of a controlling state.

### `swsign`

Switches between two input states based on the sign of a third input.

### `tf1p`

First-order transfer function: $\frac{Y(s)}{U(s)} = \frac{G}{1 + sT}$

### `tf1plim`

Same as `tf1p` with non-windup limits on the output.

### `tf1pvlim`

Same as `tf1p` with variable (state-dependent) non-windup limits.

### `tf1p2lim`

Same as `tf1p` with rate-of-change limits and non-windup output limits.

### `tf1p1z`

Transfer function with one zero and one pole: $\frac{Y(s)}{U(s)} = G \frac{1 + sT_z}{1 + sT_p}$

### `tf2p2z`

Transfer function with two real zeros and two real poles: $\frac{Y(s)}{U(s)} = G \frac{(1 + sT_{z1})(1 + sT_{z2})}{(1 + sT_{p1})(1 + sT_{p2})}$

### `tfder1p`

Derivative with one time constant (washout filter): $\frac{Y(s)}{U(s)} = \frac{sT}{1 + sT}$

### `timer`

Timer with delay that varies as a piecewise linear function of a monitored variable.

### `timersc`

Timer with delay that varies as a staircase function of a monitored variable.

### `tsa`

Two-state automaton. Transitions between states are based on the signs of two input variables.

## Parameter Specification

Block parameters can be specified as:

- **Literal values**: `2.0`
- **Named data**: `{T}` (data enclosed in braces)
- **Named parameters**: `{omegac}` (operating-point parameter in braces)
- **Expressions**: `1/{omegac}` (arithmetic expression with data/parameters)
