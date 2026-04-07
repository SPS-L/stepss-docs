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

The voltage at bus $i$ takes the form:

$$
v_i(t) = \sqrt{2} \, \text{Re}\left[(v_{xi}(t) + j\,v_{yi}(t)) \, e^{j\omega_N t}\right]
$$

where $v_{xi} + j\,v_{yi}$ is the voltage phasor in rectangular coordinates on $(x,y)$ axes rotating at $\omega_N = 2\pi f_N$.

<img src="/images/phasor.svg" alt="Phasor approximation and reference frames" style="width:60%" />

## Synchronous Reference Frame

The $(x,y)$ axes rotating at $\omega_N$ form a **synchronous reference**. After a disturbance, the system may settle at frequency $f \ne f_N$, causing phasor components to oscillate at $|f - f_N|$.

This reference is suited for **short-term simulations** or when the model includes an infinite bus driving the frequency back to $f_N$.

## Center of Inertia (COI) Reference

In the COI reference, the axes rotate at:

$$
\omega_{coi} = \frac{\sum_{i=1}^m M_i \omega_i}{\sum_{i=1}^m M_i}
$$

where $M_i = 2H_i \frac{S_{Ni}}{S_B}$ is the inertia coefficient of the $i$-th machine.

When the system reaches equilibrium at frequency $f$, all phasor components tend to constant values, enabling larger time steps. The COI reference is well suited for **long-term simulations**.

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
\begin{bmatrix} \mathbf{i}_x \\ \mathbf{i}_y \end{bmatrix} = \begin{bmatrix} \mathbf{G} & -\mathbf{B} \\ \mathbf{B} & \mathbf{G} \end{bmatrix} \begin{bmatrix} \mathbf{v}_x \\ \mathbf{v}_y \end{bmatrix}
$$

For a network with $N$ buses, there are $2N$ equations involving $4N$ variables.

## Initialization Procedure

The dynamic simulation is initialized as follows:

<img src="/images/init-pflow.svg" alt="Initialization from power flow" style="width:60%" />

1. **Start from initial bus voltages** (from the power flow solution)
2. **Compute power flows** in network branches and shunts
3. **Determine bus power injections** by summing flows at incident branches
4. **Share bus injection among components** using one of two methods:
   - **(i) Explicit powers**: $P^c_j = P^{c0}_j$, $Q^c_j = Q^{c0}_j$
   - **(ii) Fractions**: $P^c_j = f_{Pj} \cdot P^{inj}_i$, $Q^c_j = f_{Qj} \cdot Q^{inj}_i$

   These methods are mutually exclusive: $f_{Pj} \times P^{c0}_j = 0$.

5. **Assign remaining power** to an impedance load: if the unassigned power is above an internal tolerance, an automatic constant-admittance load (named `M_bus`) is created:

$$
(G_i^r - jB_i^r) \cdot V_i(0)^2 = -(P_i^r + jQ_i^r)
$$

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
