---
title: User-Defined Models
description: Creating custom models with CODEGEN
---

CODEGEN allows you to define custom models that are compiled into Fortran 2003 code and linked with RAMSES. This page covers the model framework, state variables, equations, discrete transitions, and the complete model file syntax specification.

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

![Input, internal, and output states](/images/states.svg)

### Input and Output States by Category

| Model Type | Input States | Output States |
|------------|-------------|---------------|
| exc | `[v]`, `[p]`, `[q]`, `[omega]`, `[if]` | `[vf]` |
| tor | `[p]`, `[omega]` | `[tm]` |
| inj | `[vx]`, `[vy]`, `[omega]` | `[ix]`, `[iy]` |
| twop | `[vx1]`, `[vy1]`, `[vx2]`, `[vy2]`, `[omega1]`, `[omega2]` | `[ix1]`, `[iy1]`, `[ix2]`, `[iy2]` |

**Notation**:
- `[v]`: terminal voltage (pu), `[p]`/`[q]`: active/reactive power (pu on $S_{nom}$)
- `[omega]`: rotor speed (pu), `[if]`/`[vf]`: field current/voltage (pu on exciter base)
- `[tm]`: mechanical torque (pu on turbine rated torque)
- `[vx]`, `[vy]`: rectangular voltage components, `[ix]`, `[iy]`: rectangular current components
- `[omega]` (for `inj`): center-of-inertia angular frequency (pu)
- `[omega1]`, `[omega2]` (for `twop`): COI angular frequency for each subsystem (pu)

Note that not all input states need to be used by a given model.

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

The model must have a number of equations at least equal to the number of output states.

### Initialization

At initialization ($t = 0$, steady state assumed):

1. **Input states**: given from power flow solution
2. **Output states**: also given (from machine/network equations)
3. **Internal states**: initialized explicitly or automatically
4. **Parameters $\mathbf{u}$**: determined from the initial state (the number of $\mathbf{u}$ parameters equals the number of output states)

During simulation, the input, internal, and output states are computed together with the other system states. The operating-point dependent parameters remain constant unless modified by a user action.

### Example: Simple AVR

A simple excitation system with gain $G$ and time constant $T$:

![Simple AVR block diagram](/images/simple_AVR.svg)

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

![Discrete transition identification and treatment](/images/disc_steps.svg)

### Example: AVR with Non-Windup Limits

When the integrator output $v_f$ is limited between $v_f^{min}$ and $v_f^{max}$:

![AVR with non-windup limits](/images/simple_AVR2.svg)

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

A CODEGEN model file is a text description containing six mandatory sections, which must appear in the following exact order:

1. **Header**: model type and name
2. **%data**: input data values read from the simulation data file
3. **%parameters**: operating-point dependent parameters computed at initialization
4. **%states**: internal and output state declarations with initial conditions
5. **%observables**: quantities available for plotting
6. **%models**: modelling blocks and their interconnections

All keywords must be written exactly as specified (case-sensitive, no extra spaces).

## Model File Syntax Specification

### Header

The header consists of exactly two lines:

```
<type of model>
<name of model>
```

- **Line 1**: model type — must be `exc`, `tor`, `inj`, or `twop`
- **Line 2**: model name — a string of at most **16 characters**

The output file will be named `{type}_{name}.f90`. For example, type `exc` and name `simple_avr` produces `exc_simple_avr.f90`. This combined name is also used in the simulation data files to reference the model.

### Data Section

Starts with the keyword `%data`.

Each data item must be given a unique name. That name, enclosed with curly braces `{name}`, is used everywhere else in the model description.

**Important**: braces must **not** be used when a data name is first defined (i.e., before the `=` sign). If braces are used at definition, they become part of the name and will cause an error.

Each name may be followed by a comment on the same line, starting with `!`.

At initialization, RAMSES maps the data values from the simulation data file to the names declared in this section, in the order they are listed.

#### Reserved Base Power Names

The following base power names are available by default in `inj` and `twop` models and must not be used for other data:

| Model Type | Name | Meaning |
|-----------|------|---------|
| exc | — | — |
| tor | — | — |
| inj | `{sbase}` | System base power (MVA) |
| twop | `{sbase1}` | Base power of subnetwork including bus 1 (MVA) |
| twop | `{sbase2}` | Base power of subnetwork including bus 2 (MVA) |

### Parameter Section

Starts with the keyword `%parameters`.

Each parameter is defined with:
```
<name> = <mathematical expression>
```

Parameter names are enclosed with `{name}` when referenced in expressions, but **not** at the point of definition (before `=`).

Rules:
- A data and a parameter **cannot share the same name**
- Expressions may involve data names (in `{}`) or previously defined parameter names (in `{}`)
- Mathematical expressions use **FORTRAN syntax**:
  - Exponent: `**` (not `^` as in MATLAB)
  - Boolean operators: `.lt.` (less than), `.le.` (less or equal), `.gt.` (greater than), `.ge.` (greater or equal), `.eq.` (equal), `.ne.` (not equal)
  - Standard math functions (`cos`, `sqrt`, `abs`, etc.) follow Intel Fortran syntax

### State Section

Starts with the keyword `%states`.

Only **internal states** are declared here. Input and output states (whose initial values are known from the power flow) are not declared.

Each internal state is defined with:
```
<name> = <initial value expression>
```

State names are enclosed with `[name]` when referenced in expressions, but **not** at the point of definition (before `=`).

Rules:
- A state **cannot share a name** with a data or parameter
- Initial value expressions may involve data (`{}`), parameters (`{}`), or previously defined states (`[]`)
- Input and output states are also referenced with brackets (e.g., `[vf]`, `[vx]`) in expressions

#### Reserved State Names

The following names are reserved for input and output states and must not be used for internal states:

| Model Type | Name | Meaning |
|-----------|------|---------|
| exc | `[v]` | Terminal voltage (pu) |
| exc | `[p]` | Active power produced (pu on Snom) |
| exc | `[q]` | Reactive power produced (pu on Snom) |
| exc | `[omega]` | Rotor speed (pu) |
| exc | `[if]` | Field current (pu on exciter base) |
| exc | `[vf]` | Field voltage (pu on exciter base) |
| tor | `[p]` | Mechanical power (pu on turbine rated) |
| tor | `[omega]` | Rotor speed (pu) |
| tor | `[tm]` | Mechanical torque (pu on turbine rated) |
| inj | `[vx]` | x-component of bus voltage |
| inj | `[vy]` | y-component of bus voltage |
| inj | `[omega]` | COI angular frequency (pu) |
| inj | `[ix]` | x-component of injected current |
| inj | `[iy]` | y-component of injected current |
| twop | `[vx1]`, `[vy1]` | Voltage at bus 1 |
| twop | `[vx2]`, `[vy2]` | Voltage at bus 2 |
| twop | `[omega1]` | COI frequency of subsystem with bus 1 (pu) |
| twop | `[omega2]` | COI frequency of subsystem with bus 2 (pu) |
| twop | `[ix1]`, `[iy1]` | Current injected at bus 1 |
| twop | `[ix2]`, `[iy2]` | Current injected at bus 2 |

### Observable Section

Starts with the keyword `%observables`.

Observables are quantities that can be plotted as functions of time. They may be input, output, or internal states, as well as data or parameters (useful for plotting a controller setpoint, for instance).

Observable names must be written **without** enclosing braces or brackets — exactly as defined in their respective sections.

### Model Section

Starts with the keyword `%models`.

Modelling blocks and their arguments are listed sequentially. Order does not matter.

![Interconnected modelling blocks](/images/states-links.svg)

Each block is identified by:

```
& <block name>
```

**The `&` symbol must be followed by a space**, then the block name. Each block declaration may be followed by a comment starting with `!`.

After the block name, list the states (inputs/outputs of the block) followed by the data, parameters, or expressions required by the block, in the order specified by the block's definition (see [CODEGEN Blocks Library](/developer/codegen-library/)).

The model section ends at the end of the file.

### Time Variable

Time is neither a data, parameter, nor a state. When needed in expressions, use `t` (without brackets or braces).

### Complete File Format

```
<type of model>
<name of model>
%data
<name of data 1>       ! optional comment
<name of data 2>
...
%parameters
<name of parameter 1> = <math expression>
...
%states
<name of state 1> = <initial value expression>
...
%observables
<name of observable 1>
...
%models
& <block name>         ! optional comment
<state name>
<state name>
<data, parameter, or expression>
...
& <block name 2>
...
```

### Complete Example: simple_avr

The following is the complete model file for the simple AVR with non-windup limits described above. The model type is `exc`, the name is `simple_avr`, and it has three observables: one parameter (`Vo`), one internal state (`dv`), and one output state (`vf`).

```
exc
simple_avr
%data
G                   ! gain of exciter
T                   ! time constant of the exciter
vfmin               ! lower field voltage
vfmax               ! upper field voltage
%parameters
Vo = [v]+ [vf]/{G}  ! voltage setpoint of AVR
%states
dv = [vf]/{G}       ! voltage error
%observables
Vo
dv
vf
%models
& algeq             ! calculation of voltage error
{Vo}-[v]-[dv]
& tf1plim           ! exciter transfer function
dv
vf
{G}
{T}
{vfmin}
{vfmax}
```

When CODEGEN processes this file it produces `exc_simple_avr.f90` and prints an execution trace showing the counts of equations and states as each block is assembled.

## Error Detection

CODEGEN performs sanity checks to detect common mistakes.

### Errors CODEGEN catches

- Unbalanced braces `{}` or brackets `[]`
- Missing section keywords (`%data`, `%parameters`, `%states`, `%observables`, `%models`)
- Multiply defined data, states, or parameters
- Reserved name used for an internal state
- Unknown state or block name (likely a typo)
- Output variable not appearing in any equation
- Number of states ≠ number of equations

### Errors CODEGEN does NOT catch (cause compiler errors)

- Typos in math function names (e.g., `cus` instead of `cos`)
- Exponent written as `^` instead of `**`
- Forgotten `{}` around data or parameter names
- Forgotten `[]` around state names

## Data Record Formats

### INJEC Record (User-Defined Injectors)

User-defined injector models are instantiated in the simulation data file using an `INJEC` record:

```
INJEC MODEL_NAME INJ_NAME BUS FP FQ P Q DATA1 DATA2 ... ;
```

| Field | Description |
|-------|-------------|
| `MODEL_NAME` | Name of the injector model, as defined in the model file header (max 20 characters) |
| `INJ_NAME` | Name of this particular instance of the model (max 20 characters) |
| `BUS` | Name of the bus to which the injector is connected (max 8 characters) |
| `FP` | Power participation fraction $f_{Pj}$ for active power |
| `FQ` | Power participation fraction $f_{Qj}$ for reactive power |
| `P` | Initial active power. Constraint: `FP` × `P` = 0 |
| `Q` | Initial reactive power. Constraint: `FQ` × `Q` = 0 |
| `DATA1 DATA2 ...` | Successive data values, in the order defined in the `%data` section of the model |

### TWOP Record (User-Defined Two-Ports)

User-defined two-port models are instantiated using a `TWOP` record:

```
TWOP MODEL_NAME TWOP_NAME BUS1 BUS2 IND FP1 FQ1 P1 Q1 FP2 FQ2 P2 Q2 DATA1 DATA2 ... ;
```

| Field | Description |
|-------|-------------|
| `MODEL_NAME` | Name of the two-port model, as defined in the model file header (max 20 characters) |
| `TWOP_NAME` | Name of this particular instance of the model (max 20 characters) |
| `BUS1` | Name of the first connection bus (max 8 characters) |
| `BUS2` | Name of the second connection bus (max 8 characters) |
| `IND` | Synchronization indicator: `S` = synchronous (same frequency, e.g. AC link); `A` = asynchronous (different frequencies, e.g. HVDC) |
| `FP1` | Active power participation fraction at BUS1 |
| `FQ1` | Reactive power participation fraction at BUS1 |
| `P1` | Initial active power at BUS1. Constraint: `FP1` × `P1` = 0 |
| `Q1` | Initial reactive power at BUS1. Constraint: `FQ1` × `Q1` = 0 |
| `FP2` | Active power participation fraction at BUS2 |
| `FQ2` | Reactive power participation fraction at BUS2 |
| `P2` | Initial active power at BUS2. Constraint: `FP2` × `P2` = 0 |
| `Q2` | Initial reactive power at BUS2. Constraint: `FQ2` × `Q2` = 0 |
| `DATA1 DATA2 ...` | Successive data values, in the order defined in the `%data` section of the model |

The `IND` field is operationally important: setting `IND = S` causes RAMSES to treat the two subnetworks as operating at the same frequency (appropriate for AC interconnections), while `IND = A` allows them to operate at different frequencies (required for HVDC links, where `[omega1]` and `[omega2]` will differ).

## Building User Models

After writing a model file, CODEGEN translates it into Fortran 2003 code. The workflow is:

1. Write the model description file
2. Run CODEGEN (via GUI or command line) to generate Fortran source
3. Compile with Intel Fortran compiler
4. Link with RAMSES to create a custom executable or DLL

For compilation details, see [URAMSES](/developer/uramses/).

See the [CODEGEN Blocks Library](/developer/codegen-library/) for the available modelling blocks.

## Next Steps

- [CODEGEN Blocks Library](/developer/codegen-library/) — Reference for all modeling blocks
- [CODEGEN Model Examples](/developer/codegen-examples/) — Complete model files for each type
- [URAMSES](/developer/uramses/) — Compile and link custom models with RAMSES
