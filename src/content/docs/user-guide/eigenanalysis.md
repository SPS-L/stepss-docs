---
title: Eigenanalysis
description: Small-signal stability analysis in RAMSES, computed by the engine itself
---

RAMSES computes small-signal stability analysis internally. It reduces the
linearised differential-algebraic model to a state matrix, solves the dense
eigenproblem, and writes eigenvalues, damping ratios, participation factors and
mode shapes to file. No external tool is involved.

:::note[Requires a RAMSES newer than v3.60]
An older engine accepts the `EIG` disturbance and writes no results files. The
`stepss` package version's leading components name the bundled RAMSES, so
`stepss.__version__` tells you directly.
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

## Saving a run as one archive

The three files above are only useful together, and a spectrum is only worth
much beside the matrix it was reduced from. **STEPSS GUI** writes all of
them, plus the Jacobian that the [`JAC`
disturbance](/user-guide/disturbances/#export-jacobian-matrix) dumped at the
same instant, into a single `.zip` or `.tar.gz`: **Save dynamic Jacobian...** on
the Analysis tab, with the format chosen in the dialog. **Load dynamic
Jacobian...** beside it opens one back into the same results window.

| In the archive | |
|---|---|
| `stepss-ssa.txt` | The manifest: the basename, the engine version, `t`, `real_limit` and `pf_threshold` |
| `<name>_modes.dat`, `<name>_pf.dat`, `<name>_ms.dat` | The results above |
| `<name>_eqs.dat`, `<name>_var.dat`, `<name>_val.dat`, `<name>_struc.dat` | The unreduced Jacobian |

**An archive is a record of a result, not an input that reproduces one.** The
data files, the solver settings and the disturbance that produced the run are
not in it. It is something to hand to a colleague, attach to an issue, or come
back to in a year and still be able to read; re-running the analysis needs the
case, which is a separate thing to keep.

The manifest is what makes it readable that much later. None of the results
files records which engine wrote them, so an archive analysed by an older build
is otherwise indistinguishable from one made today: STEPSS names the recorded
version when it opens one, and says so when it differs from the engine now in
use. An archive carrying no manifest is refused with a reason rather than opened
into an empty window.

Both formats are ordinary archives that `unzip` and `tar xzf` read, and
everything sits under one directory named for the run. A directory of results
that arrived some other way, from a run made at a terminal for instance, opens
with **View results...**, which takes a directory rather than a file.

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

In STEPSS GUI the same run is read from the small-signal results window, opened
with **View results** on the [Analysis tab](/gui/interface/#analysis):

<img src="/images/screenshots/gui-ssa-results-light.png"
     alt="The small-signal results window for the Kundur case with stabilisers. A table lists the seven electromechanical modes with frequency, damping ratio and real and imaginary parts; the 0.6237 Hz inter-area mode at a damping ratio of 0.1087 is selected. An s-plane plot on the right places every mode against a stability boundary at the imaginary axis. Below, the Participation panel lists the selected mode's largest contributions, all four machines' speed and angle states, and a polar mode-shape plot shows G1 and G2 pointing opposite to G3 and G4."
     class="shot-single" />

Reading that window across is the whole method in one view. The table gives the
frequency and damping of each mode; the s-plane shows how much margin each one
has, with the boundary drawn at the imaginary axis, so a mode crossing it is the
instability. The **Participation** panel answers which machines make up the
selected mode, and the mode shape answers how they move relative to each other:
here G1 and G2 swing against G3 and G4, which is what makes 0.62 Hz the
inter-area mode rather than a local one.

Ticking **electromechanical only** restricts the table to the 0.1 to 2.5 Hz band,
which is where rotor-angle modes live. The full spectrum for this case is 70
states, most of them fast controller and network dynamics that no rotor
participates in.

:::note
This screenshot is light in both site themes. The window itself follows the
application's theme from v3.74.20, plot panels included; before that release the
s-plane and the mode shape stayed white under the dark theme. A plot saved with
**Save plot...** is drawn on white whatever theme is in use, since it is meant
for a report rather than the screen.
:::

## See Also

- [Export Jacobian Matrix](/user-guide/disturbances/#export-jacobian-matrix), the
  `JAC` disturbance, for exporting the matrices instead of analysing them
- [`getJac()`](/python/api-reference/#getjac), the descriptor matrices as SciPy
  sparse objects, for driving your own solver
- [Kundur Two-Area System](/test-systems/kundur/)
