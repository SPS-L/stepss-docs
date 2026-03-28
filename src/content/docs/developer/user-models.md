---
title: User-Defined Models
description: Creating custom models with CODEGEN
---

CODEGEN allows you to define custom models that are compiled into Fortran 2003 code and linked with RAMSES. This page covers the model framework, state variables, equations, and discrete transitions.

## Model Categories

| Category | Acronym | Description |
|----------|---------|-------------|
| Excitation controller | `EXC` | Excitation system and AVR (including PSS) |
| Torque controller | `TOR` | Turbine and speed governor |
| Injector | `INJ` | Component connected to a single AC bus |
| Two-port | `TWOP` | Component connecting two buses |

## States

Every model has three categories of states:

- **Input states** ($\mathbf{x}_{IN}$) — provided by the system
- **Internal states** ($\mathbf{x}_{ITL}$) — computed by the model
- **Output states** ($\mathbf{x}_{OUT}$) — returned to the system

### Input and Output States by Category

| Model Type | Input States | Output States |
|------------|-------------|---------------|
| Excitation controller | $V, P, Q, \omega, i_f$ | $v_f$ |
| Torque controller | $P, \omega$ | $T_m$ |
| Injector | $v_x, v_y, \omega_{coi}$ | $i_x, i_y$ |
| Two-port | $v_{x1}, v_{y1}, v_{x2}, v_{y2}, \omega_{coi}$ | $i_{x1}, i_{y1}, i_{x2}, i_{y2}$ |

**Notation**:
- $V$: terminal voltage (pu), $P$/$Q$: active/reactive power (pu on $S_{nom}$)
- $\omega$: rotor speed (pu), $i_f$/$v_f$: field current/voltage (pu on exciter base)
- $T_m$: mechanical torque (pu on rated torque)
- $v_x, v_y$: rectangular voltage components, $i_x, i_y$: rectangular current components
- $\omega_{coi}$: center-of-inertia angular frequency (pu)

## Equations

The model state vector is:

$$
\mathbf{x} = \begin{bmatrix} \mathbf{x}_{ITL} \\ \mathbf{x}_{OUT} \end{bmatrix}
$$

The differential-algebraic equations take the form:

$$
\mathbf{T}\dot{\mathbf{x}} = \mathbf{f}(\mathbf{x}, \mathbf{x}_{IN}, \mathbf{u}, \mathbf{z})
$$

where:
- $\mathbf{T}$ is a (mostly zero) matrix. Row $i$ is all zeros for algebraic equations, or contains a single $T_{ij}$ for differential equations.
- $\mathbf{u}$ contains operating-point dependent parameters
- $\mathbf{z}$ contains discrete variables

### Initialization

At initialization ($t = 0$, steady state assumed):

1. **Input states**: given from power flow solution
2. **Output states**: also given (from machine/network equations)
3. **Internal states**: initialized explicitly or automatically
4. **Parameters $\mathbf{u}$**: determined from the initial state (the number of $\mathbf{u}$ parameters equals the number of output states)

### Example: Simple AVR

A simple excitation system with gain $G$ and time constant $T$:

$$
0 = V^o - V - dV
$$
$$
T\frac{dv_f}{dt} = -v_f + G \cdot dV
$$

- Input: $V$ (terminal voltage)
- Internal: $dV$ (algebraic state)
- Output: $v_f$ (differential state)
- Parameter: $V^o$ (voltage setpoint)

At initialization ($\dot{v}_f = 0$): $dV(0) = v_f(0)/G$, then $V^o = V(0) + dV(0)$.

## Discrete Transitions

Discrete variables $\mathbf{z}$ control which set of equations is active. Transitions occur when inequality constraints are violated (e.g., a state exceeds its limit).

### Example: AVR with Non-Windup Limits

When the integrator output $v_f$ is limited between $v_f^{min}$ and $v_f^{max}$:

- **Normal** ($z = 0$): $T\dot{v}_f = -v_f + G \cdot dV$
- **Upper limit** ($z = 1$): $0 = v_f^{max} - v_f$
- **Lower limit** ($z = -1$): $0 = v_f^{min} - v_f$

Transition logic (pseudo-code):
```
if z == 0:
    if v_f > v_f_max:    z = 1     # hit upper limit
    elif v_f < v_f_min:  z = -1    # hit lower limit
elif z == 1:
    if (-v_f + G*dV)/T < 0:  z = 0  # release from upper
elif z == -1:
    if (-v_f + G*dV)/T > 0:  z = 0  # release from lower
```

:::note
Discrete transitions are handled automatically by STEPSS/RAMSES. Differential equations can be changed to algebraic and vice versa during transitions.
:::

## Model File Structure

A CODEGEN model file is a text description containing:

1. **Model declaration**: type (EXC, TOR, INJ, TWOP) and name
2. **Parameters**: data values and operating-point parameters
3. **State declarations**: internal and output states with initial conditions
4. **Equations**: using library blocks and arithmetic expressions
5. **Discrete transitions**: conditions and state changes

See the [CODEGEN Blocks Library](/stepss-docs/developer/codegen-library/) for the available building blocks.

## Building User Models

After writing a model file, CODEGEN translates it into Fortran 2003 code. The workflow is:

1. Write the model description file
2. Run CODEGEN (via GUI or command line) to generate Fortran source
3. Compile with Intel Fortran compiler
4. Link with RAMSES to create a custom executable or DLL

For compilation details, see [URAMSES](/stepss-docs/developer/uramses/).
