---
title: Reference Frames & Initialization
description: Phasor approximation, reference frames, and initialization procedures
---

## Phasor Approximation

Under the phasor approximation, the network equations are:

$$
\bar{\mathbf{I}} = \mathbf{Y} \bar{\mathbf{V}}
$$

where $\bar{\mathbf{I}}$ is the vector of complex currents, $\bar{\mathbf{V}}$ is the vector of complex voltages, and $\mathbf{Y}$ is the bus admittance matrix.

In dynamic regime, each synchronous machine defines a local frequency. In most cases, those frequencies remain close to the nominal frequency $f_N$. The admittances in $\mathbf{Y}$ are computed at frequency $f_N$.

The voltage at bus $i$ takes the form:

$$
v_i(t) = \sqrt{2}\, V_i(t) \cos(\omega_N t + \phi_i(t)) = \sqrt{2}\, \text{Re}\left[V_i(t)\, e^{j\phi_i(t)}\, e^{j\omega_N t}\right]
$$

In rectangular coordinates on the $(x,y)$ axes rotating at $\omega_N = 2\pi f_N$:

$$
v_i(t) = \sqrt{2}\, \text{Re}\left[(v_{xi}(t) + j\,v_{yi}(t))\, e^{j\omega_N t}\right]
$$

where $v_{xi} + j\,v_{yi}$ is the voltage phasor in rectangular coordinates on $(x,y)$ axes rotating at $\omega_N = 2\pi f_N$.

In RAMSES, the rectangular components $(v_{xi}, v_{yi})$ are used rather than the polar components $(V_i, \phi_i)$.

<img src="/images/phasor.svg" alt="Phasor approximation and reference frames" style="width:60%" />

## Synchronous Reference Frame

The $(x,y)$ axes rotating at $\omega_N$ form a **synchronous reference**. After a disturbance, the system may settle at a different frequency $f$, unless its model includes an infinite bus imposing $f_N$. Phasor components then oscillate at $|f - f_N|$, although the system is at equilibrium from a practical viewpoint. Tracking these oscillations requires a small time step, making the synchronous reference unsuitable for long-term simulations.

This reference is suited for **short-term simulations** or when the model includes an infinite bus driving the frequency back to $f_N$.

In fact, any speed can be considered for the reference axes $(x,y)$. The only constraint is that all voltage and current phasors refer to the same axes.

## Center of Inertia (COI) Reference

In the COI reference, the axes rotate at:

$$
\omega_{coi} = \frac{\sum_{i=1}^m M_i \omega_i}{\sum_{i=1}^m M_i}
$$

where $m$ is the total number of synchronous machines, $\omega_i$ is the rotor speed of the $i$-th machine, and $S_{Ni}$ is its nominal apparent power (in MVA).

$M_i = 2H_i \frac{S_{Ni}}{S_B}$ is the inertia coefficient of the $i$-th machine.

When the system reaches equilibrium at frequency $f$, all phasor components tend to constant values, enabling larger time steps. The COI reference is well suited for **long-term simulations**.

### Implementation

To preserve model sparsity despite the global coupling in the COI equation, the value of $\omega_{coi}$ at the previous time step is used.

See: D. Fabozzi and T. Van Cutsem, "On angle references in long-term time-domain simulations," *IEEE Trans. Power Systems*, Vol. 26, No. 1, pp. 483-484, Feb. 2011.

The COI frequency can be used as an average system frequency in injector and two-port models.

### Specifying the Reference Frame

The reference is specified in [Solver Settings](/user-guide/solver-settings/) via:
```
$OMEGA_REF SYN ;    # Synchronous reference
$OMEGA_REF COI ;    # Center of inertia reference
```

The presence of a Thévenin equivalent (infinite bus) forces the synchronous reference.

## Network Equations

With all phasors referred to the $(x,y)$ axes, the network equations decompose into:

$$
\mathbf{i}_x + j\,\mathbf{i}_y = (\mathbf{G} + j\,\mathbf{B})(\mathbf{v}_x + j\,\mathbf{v}_y)
$$

where $\mathbf{G}$ is the conductance matrix and $\mathbf{B}$ the susceptance matrix. Decomposing into real and imaginary parts yields:

$$
\begin{bmatrix} \mathbf{i}_x \\ \mathbf{i}_y \end{bmatrix} = \begin{bmatrix} \mathbf{G} & -\mathbf{B} \\ \mathbf{B} & \mathbf{G} \end{bmatrix} \begin{bmatrix} \mathbf{v}_x \\ \mathbf{v}_y \end{bmatrix}
$$

For a network with $N$ buses, there are $2N$ equations involving $4N$ variables.

## Initialization Procedure

The dynamic simulation is initialized as follows:

<img src="/images/init-pflow.svg" alt="Initialization from power flow" style="width:60%" />

1. **Start from initial bus voltages** (from the power flow solution)
2. **Compute power flows** in network branches and shunts
3. **Determine bus power injections** by summing flows at incident branches

   A positive value of $P^{inj}_i$ (resp. $Q^{inj}_i$) corresponds to power entering the network.

4. **Share bus injection among components** using one of two methods:
   - **(i) Explicit powers**: $P^c_j = P^{c0}_j$, $Q^c_j = Q^{c0}_j$
   - **(ii) Fractions**: $P^c_j = f_{Pj} \cdot P^{inj}_i$, $Q^c_j = f_{Qj} \cdot Q^{inj}_i$

   These methods are mutually exclusive: $f_{Pj} \times P^{c0}_j = 0$ and $f_{Qj} \times Q^{c0}_j = 0$.

   Although $f_{Pj}$ and $f_{Qj}$ are typically in the interval $[0, 1]$, negative values or values larger than one are allowed.

5. **Assign remaining power** to an impedance load:

$$
P_i^r = P^{inj}_i - \sum_{j=1}^{n} P^c_j \qquad Q_i^r = Q^{inj}_i - \sum_{j=1}^{n} Q^c_j
$$

   If the unassigned power is above an internal tolerance, an automatic constant-admittance load (named `M_bus`) is created:

$$
(G_i^r - jB_i^r) \cdot V_i(0)^2 = -(P_i^r + jQ_i^r)
$$

A large value of $G_i^r$ or $B_i^r$ may be intentional (when a load is modeled as a constant shunt admittance), but it may also result from a mistake in the initial power balance.

:::tip
For a single component taking the whole bus injection, set $f_P = 1$, $P^{c0} = 0$, $f_Q = 1$, $Q^{c0} = 0$. This allows reusing data at different operating points.
:::

:::note
Names starting with `M_` are reserved for automatic impedance loads. Check their values through the "Load Initialization" menu in the STEPSS GUI.
:::

### Initialization Output Example

```
NUMBER OF IMPEDANCE LOADS :     3  (M_ type:     3 )

load name              bus name                  P          Q

M_2                    2                       90.002     17.997
M_3                    3                        0.013     -0.011
M_4                    4                       -0.017     -0.022
```

Here, `M_3` and `M_4` are negligible (rounding artifacts), while `M_2` suggests a missing load specification at bus 2.

## Next Steps

- [Dynamic Models](/user-guide/dynamic-models/) — Define SYNC_MACH, INJEC, and TWOP records
- [Disturbances](/user-guide/disturbances/) — Define simulation events
