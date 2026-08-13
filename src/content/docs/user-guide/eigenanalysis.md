---
title: Eigenanalysis
description: Small-signal stability analysis in RAMSES, computed by the engine itself
---

RAMSES computes small-signal stability analysis internally. It reduces the
linearised differential-algebraic model to a state matrix, solves the dense
eigenproblem, and writes eigenvalues, damping ratios, participation factors and
mode shapes to file. No external tool is involved.

:::note[Requires a RAMSES newer than v3.60]
The `EIG` disturbance was added after the v3.60 release. On an older engine it is
accepted and no results files appear. The `stepss` package version's leading
components name the bundled RAMSES, so `stepss.__version__` tells you directly.
:::

## What is computed

The linearised model is a set of differential-algebraic equations,

$$
\begin{aligned}
\Delta\dot{x} &= f_x\,\Delta x + f_y\,\Delta y \\
0 &= g_x\,\Delta x + g_y\,\Delta y
\end{aligned}
$$

with states $x$ and algebraic variables $y$. Eliminating $\Delta y$ gives the
state matrix

$$A_{sys} = f_x - f_y\,g_y^{-1}\,g_x$$

whose eigenvalues are the system modes. RAMSES assembles the unreduced Jacobian,
factorises $g_y$ once with KLU, forms $A_{sys}$, and solves it with LAPACK.
The elimination exists only if $g_y$ is nonsingular, which is what makes the
model index-1; a singular $g_y$ is reported rather than worked around.

For each eigenvalue $\lambda = \sigma \pm j\omega$:

| Quantity | Definition |
|---|---|
| Frequency | $f = \lvert\omega\rvert / 2\pi$ in Hz |
| Damping ratio | $\zeta = -\sigma / \lvert\lambda\rvert$ |

A mode with $\zeta < 0$ grows rather than decays: the operating point is
small-signal unstable.

## Running an analysis

Add an `EIG` event to the disturbance file:

```
1.000 EIG 'ssa'
```

or inject it from Python:

```python
import stepss

case = stepss.cfg()
case.addData('lf.dat')
case.addData('dyn.dat')
case.addData('solveroptions.dat')
case.addDst('nothing.dst')
case.addObs('obs.dat')
case.addTrj('out.trj')

ram = stepss.sim()
ram.execSim(case, 0.0)               # pause at the operating point
ram.addDisturb(0.001, "EIG 'ssa'")   # schedule the analysis
ram.contSim(0.01)                    # advance past it so the event fires
ram.endSim()
```

Results are computed at the instant the event fires, so where you pause
determines what you get. Small-signal results are only meaningful at an
operating point: pausing mid-swing linearises about a non-equilibrium.

### Required settings

| Setting | Why |
|---|---|
| `$OMEGA_REF SYN` | Under the centre-of-inertia frame the COI equations are computed by finite differences and never enter the assembled Jacobian, so reducing under COI would silently hold COI speed constant and produce a plausible, wrong spectrum |
| `$SCHEME DE` | Under the integrated scheme the pure differential-algebraic values exist only briefly inside the Newton loop |

Both are refused rather than approximated. See [Refusals](#refusals) below.

## Output files

Three files per analysis, named from the basename given to `EIG`. All are plain
whitespace-separated text with `#` comment headers, so `numpy.loadtxt` reads
them directly. Names are left-justified and contain no spaces, so splitting on
whitespace is safe.

### `<name>_modes.dat`

One line per mode, every mode written.

| Column | Meaning |
|---|---|
| `index` | Mode number, 1-based |
| `re`, `im` | Real and imaginary parts of $\lambda$ |
| `zeta` | Damping ratio |
| `freq_hz` | Frequency in Hz |
| `dom` | 1 if $\mathrm{Re}(\lambda)$ exceeded the `real_limit` filter |
| `smp` | 1 if the eigenvalue is simple, 0 if degenerate |

The header records `nstates`, `nalg`, the time, and the `real_limit`,
`pf_threshold` and `gap_tol` values used.

### `<name>_pf.dat`

Participation factors, one line per mode and state:
`mode`, `state`, `pf`, `family`, `device`, `variable`.

The participation of state $k$ in mode $i$ is $p_{ki} = \lvert w_{ki}\,v_{ki}\rvert$,
built from the left and right eigenvectors and normalised so each mode's largest
entry is 1. Written only for dominant modes, and only for entries above
`pf_threshold`, so a state that is absent is below the threshold rather than
exactly zero.

### `<name>_ms.dat`

Mode shapes, one line per mode and machine:
`mode`, `state`, `magnitude`, `angle_deg`, `device`.

Rotor-speed components, normalised so the largest magnitude in each mode is 1,
with **angles relative to that largest entry**, because an eigenvector's absolute
phase is arbitrary.

## Degenerate modes, and why the `smp` column matters

Identical machine models with identical parameters produce identical poles, so
power system spectra are heavily degenerate. In the Kundur two-area system, 20
of 70 modes share an eigenvalue with another mode.

**In a degenerate eigenspace the individual eigenvectors are not unique.** The
participation factors and mode shape of such a mode are therefore
basis-dependent: real numbers that carry no physical meaning and that would come
out differently on another LAPACK build.

The `smp` column is 1 when the gap from this eigenvalue to every other exceeds
`gap_tol` (default `1e-6`, recorded in the header), and 0 otherwise. **Do not
interpret participation factors or mode shapes for a mode flagged 0.**

## Refusals

The analysis refuses rather than returning a result it cannot justify. Every
refusal writes no results files, states the reason in the log and through
[`getLastErr()`](/python/api-reference/), and exits with code **78**.

| Condition | Reason |
|---|---|
| `$OMEGA_REF COI` | The assembled Jacobian does not carry the COI equations |
| `$SCHEME IN` | The pure DAE values are not available at that point |
| States above `$EIG_MAX_STATES` | The dense solve is not practical at that size |
| Singular $g_y$ | The model is not index-1 |

A run that produced nothing and exited **0** is a different problem, most likely
an engine older than v3.60.

The size ceiling is
[`$EIG_MAX_STATES`](/user-guide/solver-settings/#small-signal-analysis-size-limit),
default 5000. Systems beyond it need sparse shift-invert methods, which
`scipy.sparse.linalg.eigs` can drive from the descriptor matrices
[`getJac()`](/python/api-reference/#getjac) returns.

## Worked example

The [Kundur two-area system](/test-systems/kundur/) is the standard inter-area
oscillation benchmark, and the `stepss` package ships an annotated notebook for
it under `examples/eigenanalysis/`. Analysed with and without its power system
stabilisers:

| | inter-area | area 1 local | area 2 local |
|---|---|---|---|
| **without PSS** | 0.625 Hz, $\zeta$ = **-0.0233** | 1.085 Hz, $\zeta$ = 0.099 | 1.116 Hz, $\zeta$ = 0.097 |
| **with PSS** | 0.624 Hz, $\zeta$ = **+0.1087** | 1.242 Hz, $\zeta$ = 0.288 | 1.295 Hz, $\zeta$ = 0.287 |

The inter-area damping ratio flips sign with the stabilisers: without them the
0.62 Hz oscillation between the two areas grows and the operating point is
small-signal unstable. This reproduces Kundur, *Power System Stability and
Control*, Example 12.6.

Participation factors separate the two local modes without any prior knowledge
of the topology: the 1.085 Hz mode lists only G1 and G2, the 1.116 Hz mode only
G3 and G4, and the inter-area mode lists all four.

## See Also

- [Export Jacobian Matrix](/user-guide/disturbances/#export-jacobian-matrix), the
  `JAC` disturbance, for exporting the matrices instead of analysing them
- [`getJac()`](/python/api-reference/#getjac), the descriptor matrices as SciPy
  sparse objects, for driving your own solver
- [Kundur Two-Area System](/test-systems/kundur/)
