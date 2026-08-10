---
title: "Synchronous Machine Parameter Conversion (XT ↔ RL)"
description: How STEPSS/RAMSES converts characteristic reactances and open-circuit time constants (XT format) into Park inductances and resistances (RL format), with the exact algorithm, known traps, and a reference Python implementation.
---

A `SYNC_MACH` record can be entered using one of two equivalent parameter formats, selected by the `TYPE_MOD` keyword:

- **`RL`**: the Park-model inductances and resistances are supplied directly.
- **`XT`**: characteristic reactances and open-circuit time constants are supplied; STEPSS/RAMSES converts them internally.

Both formats describe the same machine. `XT` is convenient when data comes from manufacturer datasheets or Kundur-style standard parameters. This page documents exactly how that conversion is done, so it can be reproduced by hand or cross-checked against external simulators (e.g. Typhoon HIL EMT).

:::caution[Common pitfalls]
Two details that break hand calculations against STEPSS:
1. Open-circuit time constants are normalised to **radians** by $t_b = 1/(2\pi f_{nom})$ before use in the resistance formulas.
2. The field circuit base is tied to `IBRATIO` via $p_{uf} = R_f / \text{IBRATIO}$; a wrong assumption here corrupts $M_d$, $L_{\ell f}$, and $R_f$ after per-unit → Henry conversion.
:::

---

## Authoritative field order

From the RAMSES source (`sync.f90`, `get_sync_mach`):

```text
SYNC_MACH NAME BUS FP FQ P Q SNOM PNOM H D IBRATIO
  RL  LL MDU  LLF  LLD1 MQU LLQ1 LLQ2 M N RA RF   RD1  RQ1  RQ2
  XT  LL XD   XPD  XSD  XQ  XPQ  XSQ  M N RA TPD0 TSD0 TPQ0 TSQ0
  EXC <model> ... TOR <model> ... ;
```

A rotor circuit the machine does not have is skipped with `*` in **both** its reactance/inductance and its resistance/time-constant field.

---

## Conversion algorithm (XT → RL)

All parameters are in per unit; time constants are entered in seconds and normalised internally.

**Time base**

$$
t_b = \frac{1}{2\pi f_{nom}}
$$

All time constants (TPD0, TSD0, TPQ0, TSQ0) are divided by $t_b$ before entering the resistance formulas.

**Unsaturated mutuals**

$$
M_d^u = X_d - L_\ell, \qquad M_q^u = X_q - L_\ell
$$

**d axis, two rotor circuits (field + damper, XSD/TSD0 present)**

$$
T'_d = T'_{d0}\frac{X'_d}{X_d}, \qquad T''_d = \frac{X''_d \, T'_{d0} \, T''_{d0}}{X_d \, T'_d}
$$

$$
a = \frac{X_d T'_d T''_d - L_\ell T'_{d0} T''_{d0}}{X_d - L_\ell}, \quad
b = \frac{X_d(T'_d + T''_d) - L_\ell(T'_{d0} + T''_{d0})}{X_d - L_\ell}
$$

$$
c = \frac{X_d(T'_{d0} T''_{d0} - T'_d T''_d)}{(X_d - L_\ell)^2}, \quad
d = \frac{X_d(T'_{d0} + T''_{d0} - T'_d - T''_d)}{(X_d - L_\ell)^2}
$$

$$
T_f = \frac{b + \sqrt{b^2 - 4a}}{2}, \qquad T_{d1} = b - T_f
$$

$$
R_{d1} = \frac{T_f - T_{d1}}{c - d \, T_{d1}}, \qquad R_f = \frac{-R_{d1}}{1 - d \, R_{d1}}
$$

$$
L_{\ell f} = T_f R_f, \qquad L_{\ell d1} = T_{d1} R_{d1}
$$

**d axis, single rotor circuit (XSD/TSD0 skipped)**

$$
L_{ff} = \frac{(M_d^u)^2}{X_d - X'_d}, \qquad L_{\ell f} = L_{ff} - M_d^u, \qquad R_f = \frac{L_{ff}}{T'_{d0}}
$$

**q axis** is fully symmetric to the d axis. Two circuits (XPQ/TPQ0 and XSQ/TSQ0) use the same quadratic with $X_q, L_\ell, T'_{q0}, T''_{q0}, X'_q, X''_q$. Single-circuit fallbacks:

- Transient only (XPQ/TPQ0): $L_{\ell q1} = M_q^u{}^2/(X_q - X'_q) - M_q^u$, $R_{q1} = (M_q^u{}^2/(X_q - X'_q))/T'_{q0}$
- Subtransient only (XSQ/TSQ0): same with $X''_q, T''_{q0}$, result assigned to $L_{\ell q2}, R_{q2}$

**Field base scaling**

$$
p_{uf} = R_f \,/\, \text{IBRATIO}
$$

The field current is then reconstructed internally as $i_f = (\psi_f - \psi_{ad}) \cdot (R_f/p_{uf}) / L_{\ell f}$.

:::note[Sanity check]
If any of $R_f, R_{d1}, L_{\ell f}, L_{\ell d1}$ (or q-axis equivalents) turns out negative, the supplied reactances/time constants are physically inconsistent. STEPSS emits an "unrealistic Park inductances or resistances" warning.
:::

---

## Reference Python implementation

A standalone Python port of the `XT` branch is available at
[`Sync_mach_Octave`](https://github.com/SPS-L/Sync_mach_Octave) (Octave) and
as `ramses_xt_to_park.py` (attached below). It reproduces the algorithm above
including the $t_b$ normalisation, the quadratic solve, the symmetric q axis,
and `puf = RF/IBRATIO`. Pass `None` for any rotor circuit the machine does not
have.

```python
from ramses_xt_to_park import ramses_xt_to_park

p = ramses_xt_to_park(
    fnom=50.0, ibratio=1.0,
    ll=0.15,  ra=0.003,
    xd=1.81,  xpd=0.30, xsd=0.23, tpd0=8.0, tsd0=0.03,
    xq=1.76,  xpq=0.65, xsq=0.25, tpq0=1.0, tsq0=0.07)
# → llf=0.169902, lld1=0.166338, rf=0.000741, rd1=0.033390, ...
```

---

## Worked examples

Inputs (both cases, 50 Hz, IBRATIO = 1): $L_\ell = 0.15$, $R_a = 0.003$, $X_d = 1.81$, $X'_d = 0.30$, $X''_d = 0.23$, $T'_{d0} = 8.0$ s, $T''_{d0} = 0.03$ s, $X_q = 1.76$, $X'_q = 0.65$, $T'_{q0} = 1.0$ s. The round-rotor case adds $X''_q = 0.25$, $T''_{q0} = 0.07$ s.

| Parameter | Round rotor (d2/q2) | Single q-damper (d2/q1) |
|-----------|--------------------:|------------------------:|
| $M_d^u$   | 1.660000 | 1.660000 |
| $L_{\ell f}$ | 0.169902 | 0.169902 |
| $L_{\ell d1}$ | 0.166338 | 0.166338 |
| $M_q^u$   | 1.610000 | 1.610000 |
| $L_{\ell q1}$ | 0.928153 | 0.725225 |
| $L_{\ell q2}$ | 0.120461 | n/a |
| $R_f$     | 0.000741 | 0.000741 |
| $R_{d1}$  | 0.033390 | 0.033390 |
| $R_{q1}$  | 0.009236 | 0.007433 |
| $R_{q2}$  | 0.028210 | n/a |
| $p_{uf}$  | 0.000741 | 0.000741 |

---

## Comparing with an EMT simulator

When cross-checking STEPSS (RMS/phasor) against an EMT tool such as Typhoon HIL:

1. **Per unit vs physical units.** STEPSS stays entirely in per unit. Converting to Henry/Ohm for the EMT tool requires a consistent per-unit base on the rotor side; use the same `IBRATIO` assumption on both sides.
2. **Radians vs seconds.** The $t_b$ normalisation is internal to STEPSS. Your hand calculation must divide every time constant by $t_b = 1/(2\pi f_{nom})$ before computing resistances.
3. **Expected post-fault difference.** STEPSS uses the phasor approximation and neglects stator transformer voltages ($d\psi_d/dt$, $d\psi_q/dt$), so it omits the DC-offset and high-frequency current components immediately after a short circuit. An EMT model retains them. Compare the **slow post-fault envelopes** first: envelope agreement with first-cycle differences indicates a modelling assumption, not a parameter error.

---

## See also

- [Synchronous Machine Model](/models/synchronous-machine/), equations, per unit system, and `SYNC_MACH` record reference
- [Octave reference implementation](https://github.com/SPS-L/Sync_mach_Octave)
- [Phasor approximation](https://thierryvancutsem.github.io/home/elec0047/phasor_approx.pdf)
- [Synchronous machine dynamics](https://thierryvancutsem.github.io/home/elec0047/dyn_of_sync_mac.pdf)
