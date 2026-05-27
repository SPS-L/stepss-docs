---
title: Synchronous Machine Model
description: Mathematical model of the synchronous machine in RAMSES — flux-current relationships, saturation, Park equations, and per unit system
---

This page documents the mathematical model of the synchronous machine implemented in RAMSES. The model uses the Equal-Mutual-Flux-Linkage (EMFL) per unit system and supports detailed (round rotor, salient pole) and simplified (no damper) configurations through model switches.

---

## Model Switches

To accommodate different rotor configurations within a single model, integer "model switches" are defined:

| Switch | Meaning |
|--------|---------|
| $S_{d1}$ | 1 if there is a damper winding $d1$, 0 otherwise |
| $S_{q1}$ | 1 if there is a damper winding $q1$, 0 otherwise |
| $S_{q2}$ | 1 if there is an equivalent winding $q2$, 0 otherwise |

| Model | Switches |
|-------|----------|
| Detailed, round rotor | $S_{d1} = 1,\; S_{q1} = 1,\; S_{q2} = 1$ |
| Detailed, salient pole | $S_{d1} = 1,\; S_{q1} = 1,\; S_{q2} = 0$ |
| Simplified, no damper | $S_{d1} = 0,\; S_{q1} = 0,\; S_{q2} = 0$ |

---

## Flux-Current Relationships

Using the EMFL per unit system, the relationship between magnetic flux linkages and currents is:

$$
\begin{pmatrix} \psi_d \\ \psi_f \\ \psi_{d1} \end{pmatrix} = \begin{pmatrix} L_\ell + M_d & M_d & S_{d1} M_d \\ M_d & L_{\ell f} + M_d & S_{d1} M_d \\ S_{d1} M_d & S_{d1} M_d & L_{\ell d1} + S_{d1} M_d \end{pmatrix} \begin{pmatrix} i_d \\ i_f \\ i_{d1} \end{pmatrix}
$$

$$
\begin{pmatrix} \psi_q \\ \psi_{q1} \\ \psi_{q2} \end{pmatrix} = \begin{pmatrix} L_\ell + M_q & S_{q1} M_q & S_{q2} M_q \\ S_{q1} M_q & L_{\ell q1} + S_{q1} M_q & S_{q2} M_q \\ S_{q2} M_q & S_{q2} M_q & L_{\ell q2} + S_{q2} M_q \end{pmatrix} \begin{pmatrix} i_q \\ i_{q1} \\ i_{q2} \end{pmatrix}
$$

The $d$ and $q$ components of the air-gap flux are:

$$
\psi_{ad} = M_d(i_d + i_f + S_{d1} i_{d1})
$$

$$
\psi_{aq} = M_q(i_q + S_{q1} i_{q1} + S_{q2} i_{q2})
$$

Individual flux linkages in terms of air-gap flux:

$$
\psi_d = L_\ell i_d + \psi_{ad}
$$

$$
\psi_f = L_{\ell f} i_f + \psi_{ad}
$$

$$
\psi_{d1} = L_{\ell d1} i_{d1} + S_{d1} \psi_{ad}
$$

$$
\psi_q = L_\ell i_q + \psi_{aq}
$$

$$
\psi_{q1} = L_{\ell q1} i_{q1} + S_{q1} \psi_{aq}
$$

$$
\psi_{q2} = L_{\ell q2} i_{q2} + S_{q2} \psi_{aq}
$$

Rotor currents from flux linkages:

$$
i_f = \frac{\psi_f - \psi_{ad}}{L_{\ell f}}, \qquad i_{d1} = \frac{\psi_{d1} - S_{d1} \psi_{ad}}{L_{\ell d1}}, \qquad i_{q1} = \frac{\psi_{q1} - S_{q1} \psi_{aq}}{L_{\ell q1}}, \qquad i_{q2} = \frac{\psi_{q2} - S_{q2} \psi_{aq}}{L_{\ell q2}}
$$

---

## Saturation Model

Let $M_d^u$ and $M_q^u$ be the unsaturated direct- and quadrature-axis mutual inductances. The saturated values $M_d$ and $M_q$ are:

$$
M_d = \frac{M_d^u}{1 + m \left(\sqrt{\psi_{ad}^2 + \psi_{aq}^2}\right)^n}
$$

$$
M_q = \frac{M_q^u}{1 + m \left(\sqrt{\psi_{ad}^2 + \psi_{aq}^2}\right)^n}
$$

where $m$ and $n$ are the saturation exponents specified in the `SYNC_MACH` record.

Substituting into the air-gap flux expressions yields the algebraic equations:

$$
\psi_{ad} \left( \frac{1 + m(\sqrt{\psi_{ad}^2 + \psi_{aq}^2})^n}{M_d^u} + \frac{1}{L_{\ell f}} + \frac{S_{d1}}{L_{\ell d1}} \right) - i_d - \frac{1}{L_{\ell f}} \psi_f - \frac{S_{d1}}{L_{\ell d1}} \psi_{d1} = 0
$$

$$
\psi_{aq} \left( \frac{1 + m(\sqrt{\psi_{ad}^2 + \psi_{aq}^2})^n}{M_q^u} + \frac{S_{q1}}{L_{\ell q1}} + \frac{S_{q2}}{L_{\ell q2}} \right) - i_q - \frac{S_{q1}}{L_{\ell q1}} \psi_{q1} - \frac{S_{q2}}{L_{\ell q2}} \psi_{q2} = 0
$$

---

## Reference Frame

The $d$ and $q$ components of the stator voltage and current relate to the network $(x, y)$ components through the rotor angle $\delta$:

$$
\begin{pmatrix} v_d \\ v_q \end{pmatrix} = \begin{pmatrix} -\sin\delta & \cos\delta \\ \cos\delta & \sin\delta \end{pmatrix} \begin{pmatrix} v_x \\ v_y \end{pmatrix}
$$

$$
\begin{pmatrix} i_d \\ i_q \end{pmatrix} = \begin{pmatrix} -\sin\delta & \cos\delta \\ \cos\delta & \sin\delta \end{pmatrix} \begin{pmatrix} i_x \\ i_y \end{pmatrix}
$$

After transformation, the air-gap flux algebraic equations in $(x, y)$ coordinates become:

$$
\psi_{ad} \left( \frac{1 + m(\sqrt{\psi_{ad}^2 + \psi_{aq}^2})^n}{M_d^u} + \frac{1}{L_{\ell f}} + \frac{S_{d1}}{L_{\ell d1}} \right) + \sin\delta\, i_x - \cos\delta\, i_y - \frac{1}{L_{\ell f}} \psi_f - \frac{S_{d1}}{L_{\ell d1}} \psi_{d1} = 0
$$

$$
\psi_{aq} \left( \frac{1 + m(\sqrt{\psi_{ad}^2 + \psi_{aq}^2})^n}{M_q^u} + \frac{S_{q1}}{L_{\ell q1}} + \frac{S_{q2}}{L_{\ell q2}} \right) - \cos\delta\, i_x - \sin\delta\, i_y - \frac{S_{q1}}{L_{\ell q1}} \psi_{q1} - \frac{S_{q2}}{L_{\ell q2}} \psi_{q2} = 0
$$

---

## Park Equations

### Stator equations (algebraic, in $x$-$y$ frame)

$$
0 = \sin\delta\, v_x - \cos\delta\, v_y + (R_a \sin\delta - \omega L_\ell \cos\delta)\, i_x - (R_a \cos\delta + \omega L_\ell \sin\delta)\, i_y - \omega \psi_{aq}
$$

$$
0 = -\cos\delta\, v_x - \sin\delta\, v_y - (R_a \cos\delta + \omega_N L_\ell \sin\delta)\, i_x - (R_a \sin\delta - \omega L_\ell \cos\delta)\, i_y + \omega \psi_{ad}
$$

### Rotor equations (differential)

$$
\frac{d\psi_f}{dt} = \omega_N \left( K_f v_f - R_f \frac{\psi_f - \psi_{ad}}{L_{\ell f}} \right)
$$

$$
\frac{d\psi_{d1}}{dt} = -\omega_N R_{d1} \frac{\psi_{d1} - S_{d1} \psi_{ad}}{L_{\ell d1}}
$$

$$
\frac{d\psi_{q1}}{dt} = -\omega_N R_{q1} \frac{\psi_{q1} - S_{q1} \psi_{aq}}{L_{\ell q1}}
$$

$$
\frac{d\psi_{q2}}{dt} = -\omega_N R_{q2} \frac{\psi_{q2} - S_{q2} \psi_{aq}}{L_{\ell q2}}
$$

---

## Rotor Motion

$$
\frac{1}{\omega_N} \frac{d\delta}{dt} = \omega - \omega_{coi}
$$

$$
2H \frac{d\omega}{dt} = K_m T_m - T_e - D(\omega - \omega_{coi})
$$

where the electromagnetic torque $T_e$ is:

$$
T_e = \psi_{ad} i_q - \psi_{aq} i_d = \psi_{ad}(\cos\delta\, i_x + \sin\delta\, i_y) - \psi_{aq}(-\sin\delta\, i_x + \cos\delta\, i_y)
$$

---

## State Variables and Equations Summary

The model has **10 state variables**: $i_x$, $i_y$, $\psi_{ad}$, $\psi_{aq}$, $\psi_f$, $\psi_{d1}$, $\psi_{q1}$, $\psi_{q2}$, $\delta$, $\omega$.

These are balanced by:
- **4 algebraic equations**: air-gap flux (d and q), stator voltage (d and q)
- **6 differential equations**: field flux, d1 damper flux, q1 damper flux, q2 damper flux, rotor angle, rotor speed

---

## Per Unit System and IBRATIO

The synchronous machine model uses the EMFL per unit system, while the excitation system typically uses its own per unit system. The parameter `IBRATIO` bridges these two bases:

$$
IBRATIO = \frac{I_{fB}^{mac}}{I_{fB}^{exc}}
$$

where $I_{fB}^{mac}$ is the field winding base current in the machine model and $I_{fB}^{exc}$ is the base current in the excitation system model. The relationship between per-unit field currents in the two systems is:

$$
IBRATIO = \frac{i_{f,pu}^{exc}}{i_{f,pu}^{mac}}
$$

### Common per unit conventions for IBRATIO

**Open-circuit unsaturated machine** (most common): $I_{fB}^{exc}$ is the field current that produces nominal stator voltage ($V = 1$ pu) at nominal speed ($\omega = 1$ pu) with the stator open, neglecting saturation:

$$
IBRATIO = M_d^u = X_d^u - X_\ell
$$

**Open-circuit saturated machine**: Same conditions but with saturation:

$$
IBRATIO = \frac{M_d^u}{1 + m} = \frac{X_d^u - X_\ell}{1 + m}
$$

**Saturated machine at nominal operating conditions**: $I_{fB}^{exc}$ is the field current when the machine produces nominal active and reactive powers ($P = \cos\phi_N$, $Q = \sin\phi_N$) at nominal voltage and speed, with saturation.

---

## SYNC_MACH Record

The synchronous machine is declared in the data file with the `SYNC_MACH` record:

```
SYNC_MACH name bus FP FQ P Q SNOM Pnom H D IBRATIO
                XT/RL Xl Xd X'd X"d Xq X'q X"q m n Ra T'do T"do T'qo T"qo
          EXC exc_type param1 param2 ...
          TOR tor_type param1 param2 ... ;
```

### Parameter Descriptions

| Parameter | Description | Unit |
|-----------|-------------|------|
| `name` | Machine name (max 8 characters) | — |
| `bus` | Connection bus name (max 8 characters) | — |
| `FP` | Active power participation fraction (0–1) | — |
| `FQ` | Reactive power participation fraction (0–1) | — |
| `P` | Initial active power (used when FP = 0) | MW |
| `Q` | Initial reactive power (used when FQ = 0) | Mvar |
| `SNOM` | Nominal apparent power | MVA |
| `Pnom` | Nominal active power of the turbine | MW |
| `H` | Inertia constant | s |
| `D` | Damping coefficient | pu |
| `IBRATIO` | Field current base ratio $I_{fB}^{mac}/I_{fB}^{exc}$ (see above) | pu |
| `XT/RL` | Keyword: `XT` for step-up transformer reactance, `RL` for line resistance | — |
| Value after XT/RL | Step-up transformer reactance or line resistance | pu |
| `Xl` | Leakage reactance $L_\ell$ | pu |
| `Xd` | d-axis synchronous reactance | pu |
| `X'd` | d-axis transient reactance | pu |
| `X"d` | d-axis subtransient reactance | pu |
| `Xq` | q-axis synchronous reactance | pu |
| `X'q` | q-axis transient reactance (use `*` to set equal to `X'd`) | pu |
| `X"q` | q-axis subtransient reactance (use `*` to set equal to `X"d`) | pu |
| `m` | Saturation coefficient (use `*` for default) | — |
| `n` | Saturation exponent (use `*` for default) | — |
| `Ra` | Armature resistance | pu |
| `T'do` | d-axis open-circuit transient time constant | s |
| `T"do` | d-axis open-circuit subtransient time constant | s |
| `T'qo` | q-axis open-circuit transient time constant (use `*` for round-rotor default) | s |
| `T"qo` | q-axis open-circuit subtransient time constant | s |

All reactances and resistances are in per unit on the machine base ($S_{nom}$, nominal voltage).

The `EXC` and `TOR` sub-records specify the excitation system and turbine-governor models. See the [Model Reference](/models/ieee-exciters/) for available models.

:::note
The FP, FQ, P, Q fields control how the machine's initial operating point is determined from the power flow solution. See [Reference Frames & Initialization](/user-guide/reference-frames/) for details.
:::
