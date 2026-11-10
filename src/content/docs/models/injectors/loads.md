---
title: Loads and Equivalents
description: Load models and the Thévenin equivalent among the RAMSES injectors
---

Injector models for loads (exponential, restorative, constant power, variable frequency drive) and for a Thévenin equivalent of an external system.

The `INJEC` record these models are entered with, and the rules on model names, are on the [Injector Models](/models/injectors/) page.

## LOAD (`inj_load`): Exponential Recovery Load

### Description

The exponential recovery load model captures the transient and steady-state voltage and frequency dependency of aggregated loads. Immediately after a voltage disturbance, the load behaves according to a transient voltage exponent; it then recovers exponentially to a steady-state behaviour described by a different exponent. The model supports separate active ($P$) and reactive ($Q$) power recovery dynamics, each with individual minimum/maximum limiters on the recovery variable.

<img src="/images/models/inj-load-light.svg"
     alt="Exponential recovery load block diagram. The bus voltage and frequency drive a steady-state term (V/V0) raised to alpha-s times one plus DP times the speed deviation. From it is subtracted the recovery state xP scaled by the transient term (V/V0) raised to alpha-t. The difference feeds an integrator of time constant Tr, limited between xPmin and xPmax, whose state xP sets the injected power P0 times xP times (V/V0) squared times one plus DP times the speed deviation. The reactive side has the same structure with exponents beta-s and beta-t."
     class="dark:sl-hidden" />
<img src="/images/models/inj-load-dark.svg"
     alt="Exponential recovery load block diagram. The bus voltage and frequency drive a steady-state term (V/V0) raised to alpha-s times one plus DP times the speed deviation. From it is subtracted the recovery state xP scaled by the transient term (V/V0) raised to alpha-t. The difference feeds an integrator of time constant Tr, limited between xPmin and xPmax, whose state xP sets the injected power P0 times xP times (V/V0) squared times one plus DP times the speed deviation. The reactive side has the same structure with exponents beta-s and beta-t."
     class="light:sl-hidden" />

### Scientific Description

The model is parameterized in terms of initial active and reactive conductance/susceptance, $G_0 = P_0/V_0^2$ and $B_0 = -Q_0/V_0^2$. Two recovery state variables $x_P$ and $x_Q$ evolve according to:

$$\dot{x}_P = \frac{1}{T_r}\left[\left(\frac{V}{V_0}\right)^{\alpha_s} \left(1 + D_P\,\Delta\omega\right) - x_P \left(\frac{V}{V_0}\right)^{\alpha_t}\right]$$

$$\dot{x}_Q = \frac{1}{T_r}\left[\left(\frac{V}{V_0}\right)^{\beta_s} \left(1 + D_Q\,\Delta\omega\right) - x_Q \left(\frac{V}{V_0}\right)^{\beta_t}\right]$$

where $\Delta\omega = \omega_{\mathrm{COI}} - 1$ is the per-unit speed deviation, $V$ is the bus voltage magnitude, $V_0$ is the initial voltage, $\alpha_t, \beta_t$ are transient exponents, $\alpha_s, \beta_s$ are steady-state exponents, and $T_r$ is the load recovery time constant. The injected currents are then:

$$i_x = G_0\, x_P\, v_x\left(1 + D_P\,\Delta\omega\right) - B_0\, x_Q\, v_y\left(1 + D_Q\,\Delta\omega\right)$$

$$i_y = G_0\, x_P\, v_y\left(1 + D_P\,\Delta\omega\right) + B_0\, x_Q\, v_x\left(1 + D_Q\,\Delta\omega\right)$$

When the recovery variable hits its limit (due to e.g. Stalling or complete voltage collapse), the limit is held until the direction of the derivative reverses.

### Parameters

| # | Name | Description | Unit |
|---|------|-------------|------|
| 1 | `DP` | Frequency sensitivity of active power | pu/pu |
| 2 | `A1` | Proportion of type-1 component in $P$ | |
| 3 | `alpha1` | Transient voltage exponent for $P$ (type 1) | |
| 4 | `A2` | Proportion of type-2 component in $P$ | |
| 5 | `alpha2` | Transient voltage exponent for $P$ (type 2) | |
| 6 | `alpha3` | Transient voltage exponent for $P$ (type 3, proportion $= 1-A_1-A_2$) | |
| 7 | `DQ` | Frequency sensitivity of reactive power | pu/pu |
| 8 | `B1` | Proportion of type-1 component in $Q$ | |
| 9 | `beta1` | Transient voltage exponent for $Q$ (type 1) | |
| 10 | `B2` | Proportion of type-2 component in $Q$ | |
| 11 | `beta2` | Transient voltage exponent for $Q$ (type 2) | |
| 12 | `beta3` | Transient voltage exponent for $Q$ (type 3) | |

Internal computed parameters include the steady-state exponents for each component (derived from the transient exponents), initial conductance $G_0$, susceptance $B_0$, and initial voltage $V_0$.

### State Variables

| Variable | Description |
|----------|-------------|
| `iy` | $y$-component of injected current (pu on system base) |
| `ix` | $x$-component of injected current (pu on system base) |
| `xp` | Active power recovery variable (dimensionless) |
| `xq` | Reactive power recovery variable (dimensionless) |

**Observables:** `P`, `Q`, `xp`, `xq`

### Usage Example

<details>
<summary>Show the data record</summary>

```
INJEC  LOAD  LOAD1  BUS1
      # FP FQ P Q: share of the power-flow injection (FP, FQ) or initial power (P in MW, Q in Mvar)
      1.  1.  0.  0.
      # DP: Frequency sensitivity of active power (pu/pu)
      1.5
      # A1: Proportion of type-1 component in P
      0.3
      # alpha1: Voltage exponent of the A1 term of P
      1.0
      # A2: Proportion of type-2 component in P
      0.2
      # alpha2: Voltage exponent of the A2 term of P
      2.0
      # alpha3: Voltage exponent of the remaining (1-A1-A2) term of P
      0.5
      # DQ: Frequency sensitivity of reactive power (pu/pu)
      1.8
      # B1: Proportion of type-1 component in Q
      0.4
      # beta1: Voltage exponent of the B1 term of Q
      2.5
      # B2: Proportion of type-2 component in Q
      0.1
      # beta2: Voltage exponent of the B2 term of Q
      3.0
      # beta3: Voltage exponent of the remaining (1-B1-B2) term of Q
      2.0
;
```

</details>
*Parameters: `DP A1 alpha1 A2 alpha2 alpha3 DQ B1 beta1 B2 beta2 beta3`*

---

## vfd_load (`inj_vfd_load`): Variable Frequency Drive Load

### Description

The VFD load model represents aggregate industrial loads driven by variable-frequency drives, where the power consumption exhibits a composite voltage-dependent characteristic with multiple exponential components and frequency sensitivity. It also includes low-voltage protection: below a configurable threshold $V_{\min}$, the load switches to a constant-admittance representation, preventing numerical difficulties during deep voltage sags.

<img src="/images/models/inj-vfd-load-light.svg"
     alt="Variable frequency drive load block diagram. The bus voltage passes a 3 ms filter and is multiplied by the frequency factor, then by a three-component exponential blend with fractions a1 and a2 and exponents alpha1, alpha2 and alpha3, normalised at the initial voltage. Below the threshold Vlow the model switches to an equivalent constant admittance Geq and Beq, whose values are set at initialisation so the two regimes meet at Vlow. The frequency deviation comes either from the local bus, measured with time constant Tmes, or from the centre-of-inertia speed."
     class="dark:sl-hidden" />
<img src="/images/models/inj-vfd-load-dark.svg"
     alt="Variable frequency drive load block diagram. The bus voltage passes a 3 ms filter and is multiplied by the frequency factor, then by a three-component exponential blend with fractions a1 and a2 and exponents alpha1, alpha2 and alpha3, normalised at the initial voltage. Below the threshold Vlow the model switches to an equivalent constant admittance Geq and Beq, whose values are set at initialisation so the two regimes meet at Vlow. The frequency deviation comes either from the local bus, measured with time constant Tmes, or from the centre-of-inertia speed."
     class="light:sl-hidden" />

### Scientific Description

The active and reactive powers depend on bus voltage $V$ and frequency deviation $\Delta f = f/f_0 - 1$:

$$P = \left(1 + D_P\,\Delta f\right) P_0 \cdot \frac{a_1 V^{\alpha_1} + a_2 V^{\alpha_2} + (1-a_1-a_2)\, V^{\alpha_3}}{a_1 V_0^{\alpha_1} + a_2 V_0^{\alpha_2} + (1-a_1-a_2)\, V_0^{\alpha_3}}$$

$$Q = \left(1 + D_Q\,\Delta f\right) Q_0 \cdot \frac{b_1 V^{\beta_1} + b_2 V^{\beta_2} + (1-b_1-b_2)\, V^{\beta_3}}{b_1 V_0^{\beta_1} + b_2 V_0^{\beta_2} + (1-b_1-b_2)\, V_0^{\beta_3}}$$

Below $V_{\min}$, an equivalent constant admittance is used:

$$P_{\mathrm{low}} = G_{\mathrm{eq}}\, V^2, \qquad Q_{\mathrm{low}} = -B_{\mathrm{eq}}\, V^2$$

where $G_{\mathrm{eq}}$ and $B_{\mathrm{eq}}$ are computed at initialization to ensure continuity at $V = V_{\min}$. The switch between the two regimes is governed by a piecewise-linear function of $V$:

$$u = \begin{cases} 0 & V < V_{\min} \\ 1 & V \geq V_{\min} \end{cases}$$

A small voltage filter (time constant 0.003 s) smooths the transition. The frequency deviation can optionally be computed from the local bus frequency (measured via an `f_inj` block with time constant $T_{\mathrm{mes}}$) or from the system centre-of-inertia speed.

The initial voltage $V_0$ can differ from the transmission bus voltage if a distribution transformer ratio is implied (set $V_{\mathrm{init}} \ne 0$ to specify the distribution-side voltage; otherwise the transmission voltage is used directly).

### Parameters

| # | Name | Description | Unit |
|---|------|-------------|------|
| 1 | `Dp` | Frequency sensitivity of active power | pu/pu |
| 2 | `a1` | Fraction of type-1 component in $P$ | |
| 3 | `alpha1` | Voltage exponent of type-1 $P$ component | |
| 4 | `a2` | Fraction of type-2 component in $P$ | |
| 5 | `alpha2` | Voltage exponent of type-2 $P$ component | |
| 6 | `alpha3` | Voltage exponent of type-3 $P$ component (fraction $= 1-a_1-a_2$) | |
| 7 | `Dq` | Frequency sensitivity of reactive power | pu/pu |
| 8 | `b1` | Fraction of type-1 component in $Q$ | |
| 9 | `beta1` | Voltage exponent of type-1 $Q$ component | |
| 10 | `b2` | Fraction of type-2 component in $Q$ | |
| 11 | `beta2` | Voltage exponent of type-2 $Q$ component | |
| 12 | `beta3` | Voltage exponent of type-3 $Q$ component | |
| 13 | `Vinit` | Initial distribution-bus voltage (0 = use transmission voltage) | pu |
| 14 | `Vlow` | Voltage threshold for constant-admittance regime (recommended 0.5–0.7) | pu |
| 15 | `foption` | 1 = use local bus frequency; 0 = use COI speed | flag |
| 16 | `Tmes` | Frequency measurement time constant | s |

### State Variables

| Variable | Description |
|----------|-------------|
| `Vreal` | Voltage at equivalent distribution bus | pu |
| `V` | Filtered distribution-bus voltage (3 ms filter) | pu |
| `P` | Active power consumed | pu |
| `Q` | Reactive power consumed | pu |
| `fbus` | Local bus frequency (used if `foption=1`) | pu |
| `df` | Frequency deviation $\Delta f$ | pu |
| `u` | Regime switch (1 = above $V_{\min}$, 0 = constant admittance) | |

**Observables:** `P`, `Q`, `df`, `u`

### Usage Example

<details>
<summary>Show the data record</summary>

```
INJEC  vfd_load  VFD1  BUS_IND
      # FP FQ P Q: share of the power-flow injection (FP, FQ) or initial power (P in MW, Q in Mvar)
      1.  1.  0.  0.
      # Dp: Frequency sensitivity of active power (pu/pu)
      1.5
      # a1: Fraction of type-1 component in P
      0.7
      # alpha1: Voltage exponent of type-1 P component
      2.0
      # a2: Fraction of type-2 component in P
      0.2
      # alpha2: Voltage exponent of type-2 P component
      1.0
      # alpha3: Voltage exponent of type-3 P component
      0.5
      # Dq: Frequency sensitivity of reactive power (pu/pu)
      1.2
      # b1: Fraction of type-1 component in Q
      0.5
      # beta1: Voltage exponent of type-1 Q component
      2.5
      # b2: Fraction of type-2 component in Q
      0.1
      # beta2: Voltage exponent of type-2 Q component
      1.5
      # beta3: Voltage exponent of type-3 Q component
      0.8
      # Vinit: Initial distribution-bus voltage (0 = use transmission voltage) (pu)
      0.0
      # Vlow: Voltage threshold for constant-admittance regime (recommended 0.5–0.7) (pu)
      0.6
      # foption: 1 = use local bus frequency; 0 = use COI speed (flag)
      0
      # Tmes: Frequency measurement time constant (s)
      0.1
;
```

</details>

---

## RESTLD (`inj_restld`): Restorative Load

### Description

The restorative load model represents loads that self-restore toward a nominal characteristic after a voltage disturbance. The load's active and reactive powers are governed by two internal recovery variables that evolve dynamically, allowing the simulation to capture the slow restoration of thermostatically controlled loads (heating, cooling) and similar self-restoring demand.

<img src="/images/models/inj-restld-light.svg"
     alt="Restorative load block diagram. The steady-state term, the voltage raised to alpha-s times one plus DP times the speed deviation, has the recovery state multiplied by the transient term subtracted from it. The difference drives an integrator of time constant Tr limited between xPmin and xPmax, whose state scales the injected currents through the initial conductance and susceptance. The reactive side has the same structure with exponents beta-s and beta-t."
     class="dark:sl-hidden" />
<img src="/images/models/inj-restld-dark.svg"
     alt="Restorative load block diagram. The steady-state term, the voltage raised to alpha-s times one plus DP times the speed deviation, has the recovery state multiplied by the transient term subtracted from it. The difference drives an integrator of time constant Tr limited between xPmin and xPmax, whose state scales the injected currents through the initial conductance and susceptance. The reactive side has the same structure with exponents beta-s and beta-t."
     class="light:sl-hidden" />

### Scientific Description

The recovery variable $x_P$ for active power satisfies:

$$\dot{x}_P = \frac{1}{T_r}\left[V^{\alpha_s}\left(1 + D_P\,\Delta\omega\right) - x_P\, V^{\alpha_t}\right]$$

with analogous equation for $x_Q$. Here $\alpha_s$ and $\alpha_t$ are the steady-state and transient voltage exponents respectively. Limiters $[x_{P,\min},\, x_{P,\max}]$ are applied. The injected currents are expressed as:

$$i_y = -B_0\left(1 + D_Q\,\Delta\omega\right) x_Q\, v_x + G_0\left(1 + D_P\,\Delta\omega\right) x_P\, v_y$$

$$i_x = \phantom{-}B_0\left(1 + D_Q\,\Delta\omega\right) x_Q\, v_y + G_0\left(1 + D_P\,\Delta\omega\right) x_P\, v_x$$

where the ratio $V/V_0$ governs the voltage dependence through `vrat`.

### Parameters

| # | Name | Description | Unit |
|---|------|-------------|------|
| 1 | `DP` | Frequency sensitivity of active power | pu/pu |
| 2 | `alphat` | Transient active power voltage exponent | |
| 3 | `alphas` | Steady-state active power voltage exponent | |
| 4 | `xP_min` | Minimum limit for $x_P$ | |
| 5 | `xP_max` | Maximum limit for $x_P$ | |
| 6 | `DQ` | Frequency sensitivity of reactive power | pu/pu |
| 7 | `betat` | Transient reactive power voltage exponent | |
| 8 | `betas` | Steady-state reactive power voltage exponent | |
| 9 | `xQ_min` | Minimum limit for $x_Q$ | |
| 10 | `xQ_max` | Maximum limit for $x_Q$ | |
| 11 | `Tr` | Load recovery time constant | s |

### State Variables

| Variable | Description |
|----------|-------------|
| `iy` | $y$-component of injected current | pu |
| `ix` | $x$-component of injected current | pu |
| `xp` | Active power recovery variable | |
| `xq` | Reactive power recovery variable | |

**Observables:** `P`, `Q`, `xp`, `xq`

### Usage Example

<details>
<summary>Show the data record</summary>

```
INJEC  RESTLD  RESTLD1  BUS2
      # FP FQ P Q: share of the power-flow injection (FP, FQ) or initial power (P in MW, Q in Mvar)
      1.  1.  0.  0.
      # DP: Frequency sensitivity of active power (pu/pu)
      1.5
      # alphat: Active power exponent multiplying xP in the recovery equation
      2.0
      # alphas: Active power steady-state exponent in the recovery equation
      0.0
      # xP_min: Lower limit of active power recovery state xP
      0.0
      # xP_max: Upper limit of active power recovery state xP
      2.0
      # DQ: Frequency sensitivity of reactive power (pu/pu)
      1.2
      # betat: Reactive power exponent multiplying xQ in the recovery equation
      2.0
      # betas: Reactive power steady-state exponent in the recovery equation
      0.0
      # xQ_min: Lower limit of reactive power recovery state xQ
      0.0
      # xQ_max: Upper limit of reactive power recovery state xQ
      2.0
      # Tr: Load recovery time constant (s)
      60.0
;
```

</details>

---

## PQ (`inj_PQ`): Constant PQ Load

### Description

The simplest injector model: maintains constant active and reactive power consumption regardless of bus voltage or frequency. The power is fixed at its initial operating-point value. A small first-order filter (time constant `Tout`) drives the injected currents smoothly to their target values, preventing algebraic loops.

<img src="/images/models/inj-pq-light.svg"
     alt="Constant PQ load block diagram. The two current references are formed from the initial powers and the measured voltage components divided by the voltage squared, and each passes a first-order filter of time constant Tout to give the injected current. The initial powers are fixed, so the power drawn does not follow the voltage."
     class="dark:sl-hidden" />
<img src="/images/models/inj-pq-dark.svg"
     alt="Constant PQ load block diagram. The two current references are formed from the initial powers and the measured voltage components divided by the voltage squared, and each passes a first-order filter of time constant Tout to give the injected current. The initial powers are fixed, so the power drawn does not follow the voltage."
     class="light:sl-hidden" />

### Scientific Description

The current references are set to deliver the initial powers $P_0$ and $Q_0$ at the measured voltage $V$:

$$I_{x,\mathrm{set}} = \frac{P_0 v_x + Q_0 v_y}{V^2}, \qquad I_{y,\mathrm{set}} = \frac{P_0 v_y - Q_0 v_x}{V^2}$$

These references pass through a first-order filter with time constant $T_{\mathrm{out}}$ to produce the actual injected currents:

$$T_{\mathrm{out}}\,\dot{i}_x + i_x = I_{x,\mathrm{set}}, \qquad T_{\mathrm{out}}\,\dot{i}_y + i_y = I_{y,\mathrm{set}}$$

### Parameters

| # | Name | Description | Unit |
|---|------|-------------|------|
| 1 | `Tout` | Output filter time constant (recommended: 0.01 s) | s |

Initial conditions $P_0$, $Q_0$, $V_0$ are computed automatically at initialization.

### State Variables

| Variable | Description |
|----------|-------------|
| `ix` | Injected $x$-current | pu |
| `iy` | Injected $y$-current | pu |
| `Ixset` | Current reference $x$ | pu |
| `Iyset` | Current reference $y$ | pu |
| `P` | Observed active power | pu |
| `Q` | Observed reactive power | pu |
| `V` | Bus voltage magnitude | pu |

**Observables:** `P`, `Q`

### Usage Example

<details>
<summary>Show the data record</summary>

```
INJEC  inj_PQ  LOAD_PQ  BUS3
      # FP FQ P Q: share of the power-flow injection (FP, FQ) or initial power (P in MW, Q in Mvar)
      1.  1.  0.  0.
      # Tout: Output filter time constant (recommended: 0.01 s) (s)
      0.01
;
```

</details>

---

## THEVEQ (`inj_theveq`): Thévenin Equivalent

### Description

Models an external network or generator cluster as a Thévenin equivalent: an ideal voltage source $\bar{E}_{\mathrm{th}}$ behind a pure reactance $X_{\mathrm{th}}$. The model computes the internal voltage magnitude and phase angle at initialization from the initial bus conditions and holds them constant during the simulation. It is useful for representing neighbouring system equivalents or simplified machine representations.

<img src="/images/models/inj-theveq-light.svg"
     alt="Thevenin equivalent block diagram. The internal voltage magnitude and phase angle are fixed at initialisation, and the injected currents follow directly from them, the terminal voltage and the Thevenin reactance. The model has no state."
     class="dark:sl-hidden" />
<img src="/images/models/inj-theveq-dark.svg"
     alt="Thevenin equivalent block diagram. The internal voltage magnitude and phase angle are fixed at initialisation, and the injected currents follow directly from them, the terminal voltage and the Thevenin reactance. The model has no state."
     class="light:sl-hidden" />

### Scientific Description

The Thévenin reactance is obtained from the specified short-circuit power $S_{\mathrm{sc}}$ (MVA):

$$X_{\mathrm{th}} = \frac{S_{\mathrm{base}}}{S_{\mathrm{sc}}}$$

The internal voltage phasor is computed at $t=0$:

$$E_{\mathrm{th},x} = v_x - X_{\mathrm{th}}\, i_y, \qquad E_{\mathrm{th},y} = v_y + X_{\mathrm{th}}\, i_x$$

$$E_{\mathrm{th}} = \sqrt{E_{\mathrm{th},x}^2 + E_{\mathrm{th},y}^2}, \qquad \phi = \arctan\!\left(\frac{E_{\mathrm{th},y}}{E_{\mathrm{th},x}}\right)$$

During simulation the injected currents satisfy:

$$i_y = -\frac{E_{\mathrm{th}}\cos\phi - v_x}{X_{\mathrm{th}}}, \qquad i_x = \frac{E_{\mathrm{th}}\sin\phi - v_y}{X_{\mathrm{th}}}$$

### Parameters

| # | Name | Description | Unit |
|---|------|-------------|------|
| 1 | `XTH` | Short-circuit power of the equivalent (converted to $X_{\mathrm{th}}$ at initialization) | MVA |

Internal parameters `ETH` (Thévenin voltage magnitude, pu) and `phase` (internal angle, rad) are computed automatically.

### State Variables

| Variable | Description |
|----------|-------------|
| `iy` | Injected $y$-current | pu |
| `ix` | Injected $x$-current | pu |

**Observables:** `P`, `Q` (in MW and Mvar at system base)

### Usage Example

<details>
<summary>Show the data record</summary>

```
INJEC  THEVEQ  EQUIV1  SLACK_BUS
      # FP FQ P Q: share of the power-flow injection (FP, FQ) or initial power (P in MW, Q in Mvar)
      1.  1.  0.  0.
      # XTH: Short-circuit power of the equivalent (MVA)
      2000.0
;
```

</details>
