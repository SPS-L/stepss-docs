---
title: IEEE AC and DC Exciters
description: The IEEE 421.5 AC1A, AC4A, AC8B and DC3A excitation system models in RAMSES
---

The rotating-exciter models of IEEE Std 421.5 available in RAMSES: three alternator-supplied (AC) types and one DC type.

The `EXC` sub-record these models are entered with, and the table of IEEE model variants, are on the [Exciter Models](/models/exciters/) page.

## AC1A

The AC1A is a rotating AC exciter with a self-excited field winding and non-linear saturation. It corresponds to IEEE Std 421.5-2016 Type AC1A. The generator terminal voltage $V_t$ is compensated for line drop and filtered before being compared with the reference. An AC alternator supplies the field through a rectifier whose output depends on the commutation voltage $V_E$ and field current $I_{fd}$.

<img src="/images/models/exc-ac1a-light.svg"
     alt="AC1A block diagram. The terminal quantities pass line-drop compensation and a transducer of time constant TR to give Vc, which is subtracted from VREF together with the rate feedback VF. The error drives a lead-lag with TC and TB, an amplifier of gain KA and time constant TA limited between VAMIN and VAMAX, high- and low-value gates against the under- and over-excitation limiters, and an output limiter between VRMIN and VRMAX. The exciter integrator of time constant TE, held at or above zero, gives VE, which the rectifier converts to Efd. The demagnetisation and saturation term VFE feeds the rate feedback of gain KF over TF."
     class="dark:sl-hidden" />
<img src="/images/models/exc-ac1a-dark.svg"
     alt="AC1A block diagram. The terminal quantities pass line-drop compensation and a transducer of time constant TR to give Vc, which is subtracted from VREF together with the rate feedback VF. The error drives a lead-lag with TC and TB, an amplifier of gain KA and time constant TA limited between VAMIN and VAMAX, high- and low-value gates against the under- and over-excitation limiters, and an output limiter between VRMIN and VRMAX. The exciter integrator of time constant TE, held at or above zero, gives VE, which the rectifier converts to Efd. The demagnetisation and saturation term VFE feeds the rate feedback of gain KF over TF."
     class="light:sl-hidden" />

### Mathematical Description

The voltage regulator processes the error signal through a lead-lag network and a limited amplifier:

$$\Delta V = V_{REF} - V_c - V_F - \Delta V_{PSS}$$

$$V_1(s) = \Delta V \cdot \frac{1 + sT_C}{1 + sT_B}$$

$$V_A(s) = V_1 \cdot \frac{K_A}{1 + sT_A}, \quad V_{AMIN} \le V_A \le V_{AMAX}$$

The AC exciter integrator with saturation and demagnetization:

$$V_{FE} = K_D \cdot I_{fd} + \left(K_E + S_E(V_E)\right) V_E$$

$$\dot{V}_E = \frac{1}{T_E}(V_R - V_{FE}), \quad 0 \le V_E$$

$$E_{fd} = V_E \cdot \left(1 - \frac{K_C \cdot I_{fd}}{V_E}\right)$$

The derivative feedback (rate feedback) path:

$$V_F(s) = E_{fd} \cdot \frac{sK_F/T_F}{1 + sT_F}$$

where $S_E(V_E)$ is the saturation function interpolated from the two-point saturation characteristic $(V_{E1}, SE_1)$ and $(V_{E2}, SE_2)$.

### Signal Flow

1. **Line drop compensation** (`algeq`): $V_{c1} = vcomp(V_t, P, Q, K_v, R_c, X_c)$
2. **Voltage measurement filter** (`tf1p`): $V_c \leftarrow V_{c1}$ with time constant $T_R$
3. **AVR summation** (`algeq`): $\Delta V = V_{REF} - V_c - V_F$
4. **Lead-lag compensator** (`tf1p1z`): $V_1 \leftarrow \Delta V$ with $(T_C, T_B)$
5. **Amplifier with limits** (`tf1plim`): $V_2 \leftarrow V_1$ with gain $K_A$, time constant $T_A$, limits $[V_{AMIN}, V_{AMAX}]$
6. **UEL high-value gate** (`max1v1c`): $V_3 = \max(V_2, V_{UEL})$
7. **OEL low-value gate** (`min1v1c`): $V_4 = \min(V_3, V_{OEL})$
8. **Output limiter** (`lim`): $V_R = \text{clamp}(V_4, V_{RMIN}, V_{RMAX})$
9. **Exciter integrator** (`inlim`): $V_E \leftarrow (V_R - V_{FE})/T_E$
10. **Saturation computation** (`algeq`): $V_{FE}$ from $K_D$, $K_E$, $S_E(V_E)$
11. **Rectifier output** (`algeq`): $E_{fd} = vrectif(I_{fd}, V_E, K_C)$
12. **Derivative feedback** (`tfder1p`): $V_F \leftarrow V_{FE}$ with gain $K_F/T_F$, time constant $T_F$

### Parameters

| Parameter | Description | Unit/Type |
|---|---|---|
| `Kv` | Voltage compensation gain | pu |
| `Rc` | Resistance for line drop compensation | pu |
| `Xc` | Reactance for line drop compensation | pu |
| `TR` | Voltage transducer time constant | s |
| `KA` | Voltage regulator gain | pu |
| `TA` | Voltage regulator time constant | s |
| `TB` | Lead-lag denominator time constant | s |
| `TC` | Lead-lag numerator time constant | s |
| `VAMAX` | Maximum regulator output | pu |
| `VAMIN` | Minimum regulator output | pu |
| `KE` | Exciter constant (self-excitation term) | pu |
| `TE` | Exciter time constant | s |
| `KF` | Rate feedback gain | pu |
| `TF` | Rate feedback time constant | s |
| `VRMAX` | Maximum field voltage | pu |
| `VRMIN` | Minimum field voltage | pu |
| `VE1` | Saturation factor voltage point 1 | pu |
| `SE1` | Saturation factor at $V_{E1}$ | pu |
| `VE2` | Saturation factor voltage point 2 | pu |
| `SE2` | Saturation factor at $V_{E2}$ | pu |
| `KC` | Commutation factor (rectifier regulation) | pu |
| `KD` | Demagnetization factor | pu |
| `VUEL` | UEL input signal | pu |

### Variants

| Model | Description |
|---|---|
| `AC1A` | Base model, IEEE Type AC1A |
| `AC1A_MAXEX2` | Adds MAXEX2 field current limiter; VOEL moves to reference summation point (LV gate removed) |
| `AC1A_RETRO` | Retrofit variant with internal PSS4B; uses first-order AVR without separate exciter block |
| `AC1A_RETRO_PSS4B` | Retrofit variant with external PSS4B speed input |

### Usage Example

<details>
<summary>Show the data record</summary>

```
SYNC_MACH  g1  g1
      # FP FQ P Q: share of the power-flow injection (FP, FQ) or initial power (P in MW, Q in Mvar)
      1.  1.  0.  0.
      # SNOM: Nominal apparent power, used as base power in the machine model (MVA)
      800.
      # Pnom: Nominal active power of the turbine, used as base power for the turbine model (MW)
      760.
      # H: Inertia constant (s)
      3.
      # D: Damping coefficient (usually set to zero when the damper windings are modelled) (pu)
      0.
      # IBRATIO: Field current base ratio I_fB^mac/I_fB^exc (see above) (pu)
      0.95
      # TYPE_MOD: Parameter format keyword: RL or XT (case-insensitive)
      XT
      # Xl: Leakage reactance L_l (pu)
      0.15
      # Xd: d-axis synchronous reactance (pu)
      1.1
      # X'd: d-axis transient reactance (must be smaller than Xd) (pu)
      0.25
      # X"d: d-axis subtransient reactance (pu)
      0.2
      # Xq: q-axis synchronous reactance (pu)
      0.7
      # X'q: q-axis transient reactance (pu)
      *
      # X"q: q-axis subtransient reactance (pu)
      0.2
      # m: Saturation coefficient (set to 0 to neglect saturation)
      0.1
      # n: Saturation exponent (ignored when m = 0)
      6.0257
      # Ra: Armature resistance (pu)
      0.
      # T'do: d-axis open-circuit transient time constant (s)
      5.00
      # T"do: d-axis open-circuit subtransient time constant (s)
      0.05
      # T'qo: q-axis open-circuit transient time constant (s)
      *
      # T"qo: q-axis open-circuit subtransient time constant (s)
      0.1
EXC  AC1A
      # Kv: weight of the terminal voltage in the measured voltage |Kv V + (Rc+jXc) I|; 1 = terminal voltage
      1.
      # Rc: Resistance for line drop compensation
      0.
      # Xc: Reactance for line drop compensation
      0.
      # TR: Voltage transducer time constant
      0.02
      # KA: Voltage regulator gain
      200.0
      # TA: Voltage regulator time constant
      0.02
      # TB: Lead-lag denominator time constant
      10.0
      # TC: Lead-lag numerator time constant
      1.0
      # VAMAX: Maximum regulator output
      7.32
      # VAMIN: Minimum regulator output
      -7.32
      # KE: Exciter constant (self-excitation term)
      1.0
      # TE: Exciter time constant
      1.0
      # KF: Rate feedback gain
      0.03
      # TF: Rate feedback time constant
      1.0
      # VRMAX: upper limit of the regulator output after the UEL and OEL gates (pu)
      6.03
      # VRMIN: lower limit of the regulator output after the UEL and OEL gates (pu)
      -5.43
      # VE1: Saturation factor voltage point 1
      4.18
      # SE1: Saturation factor at V_E1
      0.1
      # VE2: Saturation factor voltage point 2
      3.14
      # SE2: Saturation factor at V_E2
      0.033
      # KC: Commutation factor (rectifier regulation)
      0.2
      # KD: Demagnetization factor
      0.38
      # VUEL: UEL signal into the high-value gate; a large negative value disables it (pu)
      -99999
TOR  CONSTANT
;
```

</details>

---

## AC4A

The AC4A is a simplified static representation of an AC exciter system with an inner-loop voltage-dependent output limit. It corresponds to IEEE Std 421.5-2016 Type AC4A. The upper output limit is a function of field current: $V_{RMAX,eff} = V_{RMAX} - K_C \cdot I_{fd}$.

<img src="/images/models/exc-ac4a-light.svg"
     alt="AC4A block diagram. The compensated and filtered terminal voltage Vc is subtracted from VREF, the error is limited between VIMIN and VIMAX, passes a lead-lag with TC and TB and a high-value gate against the under-excitation limiter, and drives an amplifier of gain KA and time constant TA. The upper limit of that amplifier is not fixed: it is VRMAX minus KC times the field current."
     class="dark:sl-hidden" />
<img src="/images/models/exc-ac4a-dark.svg"
     alt="AC4A block diagram. The compensated and filtered terminal voltage Vc is subtracted from VREF, the error is limited between VIMIN and VIMAX, passes a lead-lag with TC and TB and a high-value gate against the under-excitation limiter, and drives an amplifier of gain KA and time constant TA. The upper limit of that amplifier is not fixed: it is VRMAX minus KC times the field current."
     class="light:sl-hidden" />

### Mathematical Description

$$\Delta V = V_{REF} - V_c$$

$$V_I = \text{clamp}(\Delta V, V_{IMIN}, V_{IMAX})$$

$$V_1(s) = V_I \cdot \frac{1 + sT_C}{1 + sT_B}$$

$$E_{fd}(s) = V_1 \cdot \frac{K_A}{1 + sT_A}, \quad V_{RMIN} \le E_{fd} \le V_{RMAX} - K_C \cdot I_{fd}$$

The variable upper limit is updated algebraically at each time step, making AC4A a time-varying limited integrator system.

### Signal Flow

1. **Line drop compensation** (`algeq`): $V_{c1}$ from terminal measurements
2. **Voltage measurement filter** (`tf1p`): $V_c$ with $T_R$
3. **AVR summation** (`algeq`): $\Delta V = V_{REF} - V_c$
4. **Input limiter** (`lim`): $V_I = \text{clamp}(\Delta V, V_{IMIN}, V_{IMAX})$
5. **Lead-lag** (`tf1p1z`): $V_1 \leftarrow V_I$ with $(T_C, T_B)$
6. **UEL high-value gate** (`max1v1c`): $V_2 = \max(V_1, V_{UEL})$
7. **Variable upper limit** (`algeq`): $uplim = V_{RMAX} - K_C \cdot I_{fd}$
8. **Variable-limit amplifier** (`tf1pvlim`): $E_{fd} \leftarrow V_2$ with $K_A$, $T_A$, limits $[V_{RMIN}, uplim]$

### Parameters

| Parameter | Description | Unit/Type |
|---|---|---|
| `Kv` | Voltage compensation gain | pu |
| `Rc` | Line drop compensation resistance | pu |
| `Xc` | Line drop compensation reactance | pu |
| `TR` | Measurement filter time constant | s |
| `VIMAX` | Maximum input error signal | pu |
| `VIMIN` | Minimum input error signal | pu |
| `TC` | Lead numerator time constant | s |
| `TB` | Lag denominator time constant | s |
| `VUEL` | UEL signal value | pu |
| `KA` | Regulator gain | pu |
| `TA` | Regulator time constant | s |
| `VRMAX` | Maximum output (at zero field current) | pu |
| `VRMIN` | Minimum output | pu |
| `KC` | Field current derating factor | pu |

### Variants

| Model | Description |
|---|---|
| `AC4A` | Base model, IEEE Type AC4A, no PSS or OEL |

### Usage Example

<details>
<summary>Show the data record</summary>

```
SYNC_MACH  g1  g1
      # FP FQ P Q: share of the power-flow injection (FP, FQ) or initial power (P in MW, Q in Mvar)
      1.  1.  0.  0.
      # SNOM: Nominal apparent power, used as base power in the machine model (MVA)
      800.
      # Pnom: Nominal active power of the turbine, used as base power for the turbine model (MW)
      760.
      # H: Inertia constant (s)
      3.
      # D: Damping coefficient (usually set to zero when the damper windings are modelled) (pu)
      0.
      # IBRATIO: Field current base ratio I_fB^mac/I_fB^exc (see above) (pu)
      0.95
      # TYPE_MOD: Parameter format keyword: RL or XT (case-insensitive)
      XT
      # Xl: Leakage reactance L_l (pu)
      0.15
      # Xd: d-axis synchronous reactance (pu)
      1.1
      # X'd: d-axis transient reactance (must be smaller than Xd) (pu)
      0.25
      # X"d: d-axis subtransient reactance (pu)
      0.2
      # Xq: q-axis synchronous reactance (pu)
      0.7
      # X'q: q-axis transient reactance (pu)
      *
      # X"q: q-axis subtransient reactance (pu)
      0.2
      # m: Saturation coefficient (set to 0 to neglect saturation)
      0.1
      # n: Saturation exponent (ignored when m = 0)
      6.0257
      # Ra: Armature resistance (pu)
      0.
      # T'do: d-axis open-circuit transient time constant (s)
      5.00
      # T"do: d-axis open-circuit subtransient time constant (s)
      0.05
      # T'qo: q-axis open-circuit transient time constant (s)
      *
      # T"qo: q-axis open-circuit subtransient time constant (s)
      0.1
EXC  AC4A
      # Kv: weight of the terminal voltage in the measured voltage |Kv V + (Rc+jXc) I|; 1 = terminal voltage
      1.
      # Rc: Line drop compensation resistance
      0.
      # Xc: Line drop compensation reactance
      0.
      # TR: Measurement filter time constant
      0.02
      # VIMAX: Maximum input error signal
      8.0
      # VIMIN: Minimum input error signal
      -8.0
      # TC: Lead numerator time constant
      1.0
      # TB: Lag denominator time constant
      10.0
      # VUEL: UEL signal into the high-value gate; a large negative value disables it (pu)
      -99999
      # KA: Regulator gain
      200.0
      # TA: Regulator time constant
      0.015
      # VRMAX: Maximum output (at zero field current)
      4.44
      # VRMIN: Minimum output
      -4.44
      # KC: Field current derating factor
      0.0
TOR  CONSTANT
;
```

</details>

---

## AC8B

The AC8B is a rotating AC exciter with a PID voltage regulator (rather than the proportional-integral amplifier of earlier types). It corresponds to IEEE Std 421.5-2016 Type AC8B. The PID structure, proportional gain $K_{PR}$, integral gain $K_{IR}$, and derivative gain $K_{DR}$, provides improved transient response compared to Type AC1A.

<img src="/images/models/exc-ac8b-light.svg"
     alt="AC8B block diagram. The filtered terminal voltage is compared with VREF and the error drives a PID: a derivative branch of gain KDR over TDR and a proportional-integral branch with KPR and KIR, summed and limited between VPIDMIN and VPIDMAX. An amplifier of gain KA and time constant TA follows, then an exciter integrator of time constant TE limited by VFEMAX, and finally the saturation and rectifier stage giving Efd."
     class="dark:sl-hidden" />
<img src="/images/models/exc-ac8b-dark.svg"
     alt="AC8B block diagram. The filtered terminal voltage is compared with VREF and the error drives a PID: a derivative branch of gain KDR over TDR and a proportional-integral branch with KPR and KIR, summed and limited between VPIDMIN and VPIDMAX. An amplifier of gain KA and time constant TA follows, then an exciter integrator of time constant TE limited by VFEMAX, and finally the saturation and rectifier stage giving Efd."
     class="light:sl-hidden" />

### Mathematical Description

The PID voltage regulator:

$$\Delta V = V_c - V_{REF}$$

$$V_{PID}(s) = K_{PR} \cdot \Delta V + \frac{K_{IR}}{s} \cdot \Delta V + \frac{sK_{DR}/T_{DR}}{1 + sT_{DR}} \cdot \Delta V$$

$$V_R(s) = V_{PID} \cdot \frac{K_A}{1 + sT_A}, \quad V_{RMIN} \le V_R \le V_{RMAX}$$

The AC exciter with variable limits based on maximum field excitation voltage $V_{FEMAX}$:

$$V_{FE} = K_D \cdot I_{fd} + \left(K_E + S_E(V_E)\right) V_E$$

$$\dot{V}_E = \frac{1}{T_E}(V_R - V_{FE}), \quad V_{EMIN} \le V_E \le \frac{V_{FEMAX} - K_D I_{fd}}{K_E + S_E(V_E)}$$

### Signal Flow

1. **Voltage measurement** (`tf1p`): $V_c$ with $T_R$
2. **Error signal** (`algeq`): $\Delta V = V_c - V_{REF}$
3. **PID derivative part** (`tfder1p`): $x_{der} \leftarrow \Delta V$ with gain $K_{DR}/T_{DR}$
4. **PID proportional-integral** (`pictl`): $x_{propint} \leftarrow \Delta V$ with $K_{IR}$, $K_{PR}$
5. **PID sum** (`algeq`): $x_{pid} = x_{propint} + x_{der}$, limited to $[V_{PIDMIN}, V_{PIDMAX}]$
6. **Amplifier** (`tf1plim`): $V_R \leftarrow x_{pid}$ with $K_A$, $T_A$
7. **Exciter integrator** (`invlim`): $V_E$ with variable limits from $V_{FEMAX}$
8. **Saturation and rectification** (`algeq`): $V_{FE}$, $E_{fd}$

### Parameters

| Parameter | Description | Unit/Type |
|---|---|---|
| `Kv` | Voltage compensation gain | pu |
| `Rc` | Line drop resistance | pu |
| `Xc` | Line drop reactance | pu |
| `TR` | Measurement time constant | s |
| `KPR` | PID proportional gain | pu |
| `KIR` | PID integral gain | pu/s |
| `KDR` | PID derivative gain | pu·s |
| `TDR` | PID derivative filter time constant | s |
| `VPIDMAX` | PID output upper limit | pu |
| `VPIDMIN` | PID output lower limit | pu |
| `KA` | Amplifier gain | pu |
| `TA` | Amplifier time constant | s |
| `VRMAX` | Maximum regulator output | pu |
| `VRMIN` | Minimum regulator output | pu |
| `KC` | Rectifier commutation factor | pu |
| `KD` | Demagnetization factor | pu |
| `KE` | Exciter self-excitation constant | pu |
| `TE` | Exciter time constant | s |
| `VFEMAX` | Maximum field excitation voltage | pu |
| `VEMIN` | Minimum exciter output | pu |
| `VE1` | Saturation voltage point 1 | pu |
| `SE1` | Saturation factor at $V_{E1}$ | pu |
| `VE2` | Saturation voltage point 2 | pu |
| `SE2` | Saturation factor at $V_{E2}$ | pu |

### Variants

| Model | Description |
|---|---|
| `AC8B` | Base model, IEEE Type AC8B |
| `AC8B_PSS3B_lim` | Adds PSS3B dual-input stabilizer and integral OEL + SCL (stator current limiter) |
| `AC8B_lim` | Adds integral OEL and SCL without PSS |

### Usage Example

<details>
<summary>Show the data record</summary>

```
SYNC_MACH  g1  g1
      # FP FQ P Q: share of the power-flow injection (FP, FQ) or initial power (P in MW, Q in Mvar)
      1.  1.  0.  0.
      # SNOM: Nominal apparent power, used as base power in the machine model (MVA)
      800.
      # Pnom: Nominal active power of the turbine, used as base power for the turbine model (MW)
      760.
      # H: Inertia constant (s)
      3.
      # D: Damping coefficient (usually set to zero when the damper windings are modelled) (pu)
      0.
      # IBRATIO: Field current base ratio I_fB^mac/I_fB^exc (see above) (pu)
      0.95
      # TYPE_MOD: Parameter format keyword: RL or XT (case-insensitive)
      XT
      # Xl: Leakage reactance L_l (pu)
      0.15
      # Xd: d-axis synchronous reactance (pu)
      1.1
      # X'd: d-axis transient reactance (must be smaller than Xd) (pu)
      0.25
      # X"d: d-axis subtransient reactance (pu)
      0.2
      # Xq: q-axis synchronous reactance (pu)
      0.7
      # X'q: q-axis transient reactance (pu)
      *
      # X"q: q-axis subtransient reactance (pu)
      0.2
      # m: Saturation coefficient (set to 0 to neglect saturation)
      0.1
      # n: Saturation exponent (ignored when m = 0)
      6.0257
      # Ra: Armature resistance (pu)
      0.
      # T'do: d-axis open-circuit transient time constant (s)
      5.00
      # T"do: d-axis open-circuit subtransient time constant (s)
      0.05
      # T'qo: q-axis open-circuit transient time constant (s)
      *
      # T"qo: q-axis open-circuit subtransient time constant (s)
      0.1
EXC  AC8B
      # Kv: weight of the terminal voltage in the measured voltage |Kv V + (Rc+jXc) I|; 1 = terminal voltage
      1.
      # Rc: Line drop resistance
      0.
      # Xc: Line drop reactance
      0.
      # TR: Measurement time constant
      0.02
      # KPR: PID proportional gain
      1.0
      # KIR: PID integral gain
      5.0
      # KDR: PID derivative gain
      0.1
      # TDR: PID derivative filter time constant
      0.1
      # VPIDMAX: RAMSES 3.84 applies this value as the LOWER limit of the PID output (pu)
      -8.0
      # VPIDMIN: RAMSES 3.84 applies this value as the UPPER limit of the PID output (pu)
      8.0
      # KA: Amplifier gain
      1.0
      # TA: Amplifier time constant
      0.1
      # VRMAX: Maximum regulator output
      6.5
      # VRMIN: Minimum regulator output
      -6.5
      # KC: Rectifier commutation factor
      0.2
      # KD: Demagnetization factor
      1.0
      # KE: Exciter self-excitation constant
      1.0
      # TE: Exciter time constant
      0.5
      # VFEMAX: Maximum field excitation voltage
      6.5
      # VEMIN: Minimum exciter output
      0.0
      # VE1: Saturation voltage point 1
      4.0
      # SE1: Saturation factor at V_E1
      0.3
      # VE2: Saturation voltage point 2
      3.0
      # SE2: Saturation factor at V_E2
      0.1
TOR  CONSTANT
;
```

</details>

---

## DC3A

The DC3A represents a non-continuously acting (rheostat-type) DC excitation system. It corresponds to IEEE Std 421.5-2016 Type DC3A. Rather than a proportional amplifier, it uses a three-position switch (VRMIN / VRH / VRMAX) driven by an integrator that holds the rheostat position $V_{RH}$. The switch position is determined by whether the error signal $V_{ERR}$ falls inside or outside a deadband $\pm K_V$.

<img src="/images/models/exc-dc3a-light.svg"
     alt="DC3A block diagram. The error between VREF and the filtered terminal voltage drives a rheostat integrator limited between VRMIN and VRMAX. A three-position switch then selects VRMIN, the rheostat position VRH, or VRMAX according to whether the error is below the deadband, inside it, or above it. The selected voltage drives a DC exciter of time constant TE with the saturation term KE plus SE."
     class="dark:sl-hidden" />
<img src="/images/models/exc-dc3a-dark.svg"
     alt="DC3A block diagram. The error between VREF and the filtered terminal voltage drives a rheostat integrator limited between VRMIN and VRMAX. A three-position switch then selects VRMIN, the rheostat position VRH, or VRMAX according to whether the error is below the deadband, inside it, or above it. The selected voltage drives a DC exciter of time constant TE with the saturation term KE plus SE."
     class="light:sl-hidden" />

### Mathematical Description

$$V_{ERR} = V_{REF} - V_c$$

The rheostat integrator:

$$\dot{V}_{RH} = \frac{K_V \cdot T_{RH}}{V_{RMAX} - V_{RMIN}} \cdot \text{clamp}(V_{ERR}, -K_V, K_V), \quad V_{RMIN} \le V_{RH} \le V_{RMAX}$$

The three-position switch:

$$V_R = \begin{cases} V_{RMIN} & V_{ERR} < -K_V \\ V_{RH} & |V_{ERR}| \le K_V \\ V_{RMAX} & V_{ERR} > K_V \end{cases}$$

The DC exciter with saturation:

$$\dot{E}_{fd} = \frac{1}{T_E}\left[V_R - \left(K_E + S_E(E_{fd})\right) E_{fd}\right]$$

### Parameters

| Parameter | Description | Unit/Type |
|---|---|---|
| `Kvcomp` | Voltage compensation gain | pu |
| `Rc` | Line drop resistance | pu |
| `Xc` | Line drop reactance | pu |
| `TR` | Measurement time constant | s |
| `TRH` | Rheostat traversal time | s |
| `KV` | Sensitivity of non-continuously acting controller | pu |
| `VRMAX` | Maximum field voltage | pu |
| `VRMIN` | Minimum field voltage | pu |
| `TE` | Exciter time constant | s |
| `KE` | Exciter self-excitation constant | pu |
| `E1` | Saturation voltage point 1 | pu |
| `SE1` | Saturation factor at $E_1$ | pu |
| `E2` | Saturation voltage point 2 | pu |
| `SE2` | Saturation factor at $E_2$ | pu |

### Variants

| Model | Description |
|---|---|
| `DC3A` | Base model, IEEE Type DC3A, non-continuously acting rheostat controller |

### Usage Example

<details>
<summary>Show the data record</summary>

```
SYNC_MACH  g1  g1
      # FP FQ P Q: share of the power-flow injection (FP, FQ) or initial power (P in MW, Q in Mvar)
      1.  1.  0.  0.
      # SNOM: Nominal apparent power, used as base power in the machine model (MVA)
      800.
      # Pnom: Nominal active power of the turbine, used as base power for the turbine model (MW)
      760.
      # H: Inertia constant (s)
      3.
      # D: Damping coefficient (usually set to zero when the damper windings are modelled) (pu)
      0.
      # IBRATIO: Field current base ratio I_fB^mac/I_fB^exc (see above) (pu)
      0.95
      # TYPE_MOD: Parameter format keyword: RL or XT (case-insensitive)
      XT
      # Xl: Leakage reactance L_l (pu)
      0.15
      # Xd: d-axis synchronous reactance (pu)
      1.1
      # X'd: d-axis transient reactance (must be smaller than Xd) (pu)
      0.25
      # X"d: d-axis subtransient reactance (pu)
      0.2
      # Xq: q-axis synchronous reactance (pu)
      0.7
      # X'q: q-axis transient reactance (pu)
      *
      # X"q: q-axis subtransient reactance (pu)
      0.2
      # m: Saturation coefficient (set to 0 to neglect saturation)
      0.1
      # n: Saturation exponent (ignored when m = 0)
      6.0257
      # Ra: Armature resistance (pu)
      0.
      # T'do: d-axis open-circuit transient time constant (s)
      5.00
      # T"do: d-axis open-circuit subtransient time constant (s)
      0.05
      # T'qo: q-axis open-circuit transient time constant (s)
      *
      # T"qo: q-axis open-circuit subtransient time constant (s)
      0.1
EXC  DC3A
      # Kvcomp: weight of the terminal voltage in the measured voltage |Kv V + (Rc+jXc) I|; 1 = terminal voltage
      1.
      # Rc: Line drop resistance
      0.
      # Xc: Line drop reactance
      0.
      # TR: Measurement time constant
      0.0
      # TRH: Rheostat traversal time
      1.0
      # KV: voltage error band; beyond +/-KV the output is forced to VRMAX or VRMIN (pu)
      0.05
      # VRMAX: upper limit of the rheostat output, also the forced value when the error exceeds KV (pu)
      5.0
      # VRMIN: lower limit of the rheostat output, also the forced value when the error is below -KV (pu)
      0.0
      # TE: Exciter time constant
      0.8
      # KE: Exciter self-excitation constant
      1.0
      # E1: Saturation voltage point 1
      3.1
      # SE1: Saturation factor at E_1
      0.33
      # E2: Saturation voltage point 2
      2.3
      # SE2: Saturation factor at E_2
      0.1
TOR  CONSTANT
;
```

</details>
