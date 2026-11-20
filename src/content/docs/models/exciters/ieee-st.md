---
title: IEEE ST and Other Exciters
description: The IEEE 421.5 ST1A and ST2A static exciters, IEEET5, SEXS and the ENTSO-E simplified exciter in RAMSES
---

The static (ST) exciters of IEEE Std 421.5, the IEEET5 and SEXS models, and the ENTSO-E simplified exciter.

The `EXC` sub-record these models are entered with, and the table of IEEE model variants, are on the [Exciter Models](/models/exciters/) page.

## ST1A

The ST1A is a static (thyristor) excitation system with two cascaded lead-lag networks in the voltage regulator path and an inner field current limiter (KLR/ILR). It corresponds to IEEE Std 421.5-2016 Type ST1A. The output limits are proportional to terminal voltage $V_t$, and field current derating applies through $K_C$: $uplim = V_t \cdot V_{RMAX} - K_C \cdot I_{fd}$.

<img src="/images/models/exc-st1a-light.svg"
     alt="ST1A block diagram. The compensated and filtered terminal voltage is subtracted from VREF along with the stabiliser signal and the rate feedback. The error is limited between VIMIN and VIMAX, passes a high-value gate against the under-excitation limiter and two lead-lag stages, then an amplifier of gain KA limited between VAMIN and VAMAX. A field current limiter is subtracted, further gates apply the under- and over-excitation limiters, and the output limits are scaled by the terminal voltage to give Efd. The rate feedback of gain KF over TF closes back on the summation."
     class="dark:sl-hidden" />
<img src="/images/models/exc-st1a-dark.svg"
     alt="ST1A block diagram. The compensated and filtered terminal voltage is subtracted from VREF along with the stabiliser signal and the rate feedback. The error is limited between VIMIN and VIMAX, passes a high-value gate against the under-excitation limiter and two lead-lag stages, then an amplifier of gain KA limited between VAMIN and VAMAX. A field current limiter is subtracted, further gates apply the under- and over-excitation limiters, and the output limits are scaled by the terminal voltage to give Efd. The rate feedback of gain KF over TF closes back on the summation."
     class="light:sl-hidden" />

### Mathematical Description

The voltage regulator with dual lead-lag and instantaneous field current limiting:

$$\Delta V = V_{REF} - V_c + V_{PSS} + V_{UEL,path} + V_F$$

$$V_1 = \text{clamp}(\Delta V, V_{IMIN}, V_{IMAX})$$

$$V_2(s) = V_1 \cdot \frac{1 + sT_C}{1 + sT_B}$$

$$V_3(s) = V_2 \cdot \frac{1 + sT_{C1}}{1 + sT_{B1}}$$

$$V_A(s) = V_3 \cdot \frac{K_A}{1 + sT_A}, \quad V_{AMIN} \le V_A \le V_{AMAX}$$

Instantaneous field current limiter:

$$V_{LR} = K_{LR}(I_{fd} - I_{LR})$$

$$V_5 = V_A - \max(V_{LR}, 0)$$

Final output with terminal-voltage-dependent limits:

$$E_{fd} = \text{clamp}(V_5, V_t \cdot V_{RMIN}, V_t \cdot V_{RMAX} - K_C \cdot I_{fd})$$

Derivative feedback:

$$V_F(s) = E_{fd} \cdot \frac{sK_F/T_F}{1 + sT_F}$$

### Signal Flow

1. **Line drop** (`algeq`): $V_{c1}$
2. **Measurement filter** (`tf1p`): $V_c$ with $T_R$
3. **AVR summation** (`algeq`): $\Delta V$, including UEL (mode 1), PSS, and VF
4. **Error limiter** (`lim`): $V_1 \in [V_{IMIN}, V_{IMAX}]$
5. **UEL gate (mode 2)** (`max1v1c`): HV gate $V_2$
6. **First lead-lag** (`tf1p1z`): $V_3$ with $(T_C, T_B)$
7. **Second lead-lag** (`tf1p1z`): $V_4$ with $(T_{C1}, T_{B1})$
8. **Amplifier** (`tf1plim`): $V_A$ with $K_A$, $T_A$, $[V_{AMIN}, V_{AMAX}]$
9. **Field current limiter** (`algeq`, `lim`): $V_{LR}$, $V_{LRlim}$
10. **Limiter subtraction** (`algeq`): $V_5 = V_A - V_{LRlim}$
11. **UEL gate (mode 3)** (`max1v1c`): $V_6$
12. **OEL gate** (`min2v`): $V_7 = \min(V_6, V_{OEL})$
13. **Variable-limit output** (`limvb`): $E_{fd}$ with terminal-voltage-scaled limits
14. **Derivative feedback** (`tfder1p`): $V_F$

### Parameters

| Parameter | Description | Unit/Type |
|---|---|---|
| `Kv` | Voltage compensation gain | pu |
| `Rc` | Line drop resistance | pu |
| `Xc` | Line drop reactance | pu |
| `TR` | Measurement filter time constant | s |
| `UEL` | UEL connection mode (1=summation, 2=HV gate after V1, 3=HV gate after VA) | integer |
| `VIMIN` | Input error lower limit | pu |
| `VIMAX` | Input error upper limit | pu |
| `VUEL` | UEL signal value | pu |
| `TC` | First lead-lag numerator | s |
| `TB` | First lead-lag denominator | s |
| `TC1` | Second lead-lag numerator | s |
| `TB1` | Second lead-lag denominator | s |
| `KA` | Regulator gain | pu |
| `TA` | Regulator time constant | s |
| `VAMIN` | Regulator lower limit | pu |
| `VAMAX` | Regulator upper limit | pu |
| `VRMIN` | Output lower limit scaling factor | pu |
| `VRMAX` | Output upper limit scaling factor | pu |
| `KC` | Field current derating factor | pu |
| `KF` | Rate feedback gain | pu |
| `TF` | Rate feedback time constant | s |
| `KLR` | Field current limiter gain | pu |
| `ILR` | Field current limiter reference | pu |

### Variants

| Model | Description |
|---|---|
| `ST1A` | Base model, IEEE Type ST1A |
| `ST1A_IEEEST` | Adds IEEEST single-input PSS (speed or power input, selectable) |
| `ST1A_IEEEST_MAXEX2` | Adds IEEEST PSS + MAXEX2 field current limiter |
| `ST1A_PSS2B` | Adds PSS2B dual-input stabilizer |
| `ST1A_PSS2B_MAXEX2` | Adds PSS2B + MAXEX2 |
| `ST1A_PSS3B` | Adds PSS3B two-channel second-order filter stabilizer |
| `ST1A_PSS4B` | Adds PSS4B three-band stabilizer |
| `ST1A_PSS4B_MAXEX2` | Adds PSS4B + MAXEX2 |
| `ST1A_lim` | Integral OEL + stator current limiter (SCL), simplified structure without Kv/Rc/Xc |

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
EXC  ST1A
      # Kv: weight of the terminal voltage in the measured voltage |Kv V + (Rc+jXc) I|; 1 = terminal voltage
      1.
      # Rc: Line drop resistance
      0.
      # Xc: Line drop reactance
      0.
      # TR: Measurement filter time constant
      0.02
      # UEL: UEL connection mode (1=summation, 2=HV gate after V1, 3=HV gate after VA)
      1
      # VIMIN: Input error lower limit
      -0.87
      # VIMAX: Input error upper limit
      0.87
      # VUEL: UEL signal value
      0.0
      # TC: First lead-lag numerator
      1.0
      # TB: First lead-lag denominator
      10.0
      # TC1: Second lead-lag numerator
      0.0
      # TB1: Second lead-lag denominator
      0.0
      # KA: Regulator gain
      200.0
      # TA: Regulator time constant
      0.001
      # VAMIN: Regulator lower limit
      -999.0
      # VAMAX: Regulator upper limit
      999.0
      # VRMIN: Output lower limit scaling factor
      -6.7
      # VRMAX: Output upper limit scaling factor
      7.8
      # KC: Field current derating factor
      0.038
      # KF: Rate feedback gain
      0.0
      # TF: Rate feedback time constant
      1.0
      # KLR: Field current limiter gain
      0.0
      # ILR: Field current limiter reference
      0.0
TOR  CONSTANT
;
```

</details>

---

## ST2A (via EXPIC1)

The EXPIC1 model implements a static exciter with an AC rotating bus-fed rectifier and an integrating (PI-type) amplifier path: $K_A(1 + sT_A)/s$. The output $V_B$ is proportional to the AC voltage phasor magnitude, creating a bus-fed topology analogous to IEEE Type ST2A. When $K_P = K_I = 0$, the rectifier gain is unity.

<img src="/images/models/exc-st2a-light.svg"
     alt="ST2A block diagram. The filtered terminal voltage is subtracted from VREF along with the stabiliser signal and the rate feedback, a high-value gate applies the under-excitation limiter, and a PI amplifier with gains KA times TA and KA drives an output limiter between VRMIN and VRMAX. A field integrator forms Efd from VR times VB less KE times Efd, where VB comes from the rectifier voltage. The rate feedback of gain KF over TF closes back on the summation."
     class="dark:sl-hidden" />
<img src="/images/models/exc-st2a-dark.svg"
     alt="ST2A block diagram. The filtered terminal voltage is subtracted from VREF along with the stabiliser signal and the rate feedback, a high-value gate applies the under-excitation limiter, and a PI amplifier with gains KA times TA and KA drives an output limiter between VRMIN and VRMAX. A field integrator forms Efd from VR times VB less KE times Efd, where VB comes from the rectifier voltage. The rate feedback of gain KF over TF closes back on the summation."
     class="light:sl-hidden" />

### Mathematical Description

The AC exciter voltage and rectifier:

$$V_E = |K_P V_t + jK_I V_t|, \quad V_B = V_E \cdot \left(1 - \frac{K_C I_{fd}}{V_E}\right)^+$$

The integrating amplifier:

$$G_{amp}(s) = K_A \cdot \frac{1 + sT_A}{s}$$

The field voltage integrator:

$$\dot{E}_{fd} = \frac{1}{T_E}\left[V_R \cdot V_B - K_E \cdot E_{fd}\right], \quad E_{FDMIN} \le E_{fd} \le E_{FDMAX}$$

### Signal Flow

1. **Voltage measurement** (`tf1p`): $V_c$ with $T_R$
2. **Summation** (`algeq`): $\Delta V = V_{REF} - V_c - V_F - \Delta V_{PSS}$
3. **UEL gate** (`max1v1c`): clamped to $V_{UEL}$
4. **PI amplifier** (`pictl`): $V_A$ with $K_{gain} = K_A \cdot T_A$ and $K_A$
5. **Output limiter** (`lim`): $V_R \in [V_{RMIN}, V_{RMAX}]$
6. **Rectifier voltage** (`algeq`): $V_E$, $V_B$
7. **Field integrator** (`inlim`): $E_{fd}$ from $V_R \cdot V_B - K_E \cdot E_{fd}$
8. **Derivative feedback** (`tfder1p`): $V_F$

### Parameters

| Parameter | Description | Unit/Type |
|---|---|---|
| `Kvcomp` | Voltage compensation gain | pu |
| `Rc` | Line drop resistance | pu |
| `Xc` | Line drop reactance | pu |
| `TR` | Measurement time constant | s |
| `VUEL` | UEL signal | pu |
| `KA` | Amplifier gain | pu |
| `TA` | Amplifier time constant | s |
| `VRMAX` | Maximum regulator output | pu |
| `VRMIN` | Minimum regulator output | pu |
| `KF` | Rate feedback gain | pu |
| `TF` | Rate feedback time constant | s |
| `KE` | Exciter self-excitation constant | pu |
| `EFDMAX` | Maximum field voltage | pu |
| `EFDMIN` | Minimum field voltage | pu |
| `TE` | Field integrator time constant | s |
| `KP` | AC source voltage proportional factor | pu |
| `KI` | AC source voltage quadrature factor | pu |
| `KC` | Commutation voltage drop factor | pu |

### Variants

| Model | Description |
|---|---|
| `EXPIC1` | Base bus-fed static exciter |
| `EXPIC1_PSS2B` | Adds PSS2B dual-input stabilizer |
| `EXPIC1_PSS2B_MAXEX2` | Adds PSS2B + MAXEX2 field current limiter |

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
EXC  EXPIC1
      # Kvcomp: weight of the terminal voltage in the measured voltage |Kv V + (Rc+jXc) I|; 1 = terminal voltage
      1.
      # Rc: Compensation resistance (pu)
      0.
      # Xc: Compensation reactance (pu)
      0.
      # TR: Voltage measurement time constant (s)
      0.02
      # VUEL: UEL signal, lower bound of the voltage error (pu)
      -99999
      # KA: PI amplifier integral gain, KA(1+sTA)/s (1/s)
      200.0
      # TA: PI amplifier time constant (s)
      0.02
      # VRMAX: Maximum regulator output (pu)
      99.0
      # VRMIN: Minimum regulator output (pu)
      -99.0
      # KF: Rate feedback gain (pu)
      0.0
      # TF: Rate feedback time constant (s)
      1.0
      # KE: Exciter self-excitation constant (pu)
      1.0
      # EFDMAX: Maximum field voltage (pu)
      8.0
      # EFDMIN: Minimum field voltage (pu)
      -8.0
      # TE: Field integrator time constant (s)
      0.5
      # KP: Potential source gain on terminal voltage (pu)
      0.0
      # KI: Current source gain on terminal current (pu)
      1.0
      # KC: Rectifier commutation factor (pu)
      0.0
TOR  CONSTANT
;
```

</details>

---

## IEEET5

The IEEET5 (also referenced as DC5A in some conventions) is a non-continuously acting exciter similar to DC3A but uses an inner limiter block `lim_civ` that gates the integrator holding signal within a deadband $\pm K_V$. This creates the three-state (hold/raise/lower) behavior of rheostatic controllers.

<img src="/images/models/exc-ieeet5-light.svg"
     alt="IEEET5 block diagram. The error between VREF and the filtered terminal voltage passes a deadband gate of width plus or minus KV, which allows the integrator of time constant TRH to run only while the error is outside the band. The integrator output, limited between VRMIN and VRMAX, drives a DC exciter of time constant TE with the saturation term KE plus SE."
     class="dark:sl-hidden" />
<img src="/images/models/exc-ieeet5-dark.svg"
     alt="IEEET5 block diagram. The error between VREF and the filtered terminal voltage passes a deadband gate of width plus or minus KV, which allows the integrator of time constant TRH to run only while the error is outside the band. The integrator output, limited between VRMIN and VRMAX, drives a DC exciter of time constant TE with the saturation term KE plus SE."
     class="light:sl-hidden" />

### Mathematical Description

$$V_{ERR} = V_{REF} - V_c$$

The integrator for rheostat position:

$$\dot{V}_{RH} = \frac{1}{T_{RH}} \cdot V_{ERR}, \quad V_{RMIN} \le V_{RH} \le V_{RMAX}$$

The `lim_civ` block implements the deadband gating so that integration is active only when $|V_{ERR}| > K_V$:

$$V_R = \begin{cases} V_{RMIN} & V_{ERR} < -K_V \\ V_{RH} & |V_{ERR}| \le K_V \\ V_{RMAX} & V_{ERR} > K_V \end{cases}$$

$$\dot{E}_{fd} = \frac{1}{T_E}\left[V_R - \left(K_E + S_E(E_{fd})\right) E_{fd}\right]$$

### Parameters

| Parameter | Description | Unit/Type |
|---|---|---|
| `Kvcomp` | Voltage compensation gain | pu |
| `Rc` | Line drop resistance | pu |
| `Xc` | Line drop reactance | pu |
| `TRH` | Rheostat time | s |
| `KV` | Controller sensitivity deadband | pu |
| `VRMAX` | Maximum field voltage | pu |
| `VRMIN` | Minimum field voltage | pu |
| `TE` | Exciter integrator time constant | s |
| `KE` | Exciter self-excitation constant | pu |
| `E1` | Saturation point 1 | pu |
| `SE1` | Saturation factor at $E_1$ | pu |
| `E2` | Saturation point 2 | pu |
| `SE2` | Saturation factor at $E_2$ | pu |

### Variants

| Model | Description |
|---|---|
| `IEEET5` | Base model, non-continuously acting DC exciter |

---

## SEXS

The SEXS (Simplified Excitation System) is a minimal two-parameter static exciter model from CIGRÉ publications, widely used for cases where detailed exciter data is unavailable. It has no measurement filter, no line drop compensation, and no rate feedback, just a lead-lag network and a limited first-order block.

<img src="/images/models/exc-sexs-light.svg"
     alt="SEXS block diagram. The terminal voltage plus the stabiliser signal is compared with Vo, the error passes a lead-lag with TA and TB and an exciter of gain KE and time constant TE limited between EMIN and EMAX, giving Efd. Vo is set at initialisation as the terminal voltage plus Efd0 over KE, so the initial error is zero."
     class="dark:sl-hidden" />
<img src="/images/models/exc-sexs-dark.svg"
     alt="SEXS block diagram. The terminal voltage plus the stabiliser signal is compared with Vo, the error passes a lead-lag with TA and TB and an exciter of gain KE and time constant TE limited between EMIN and EMAX, giving Efd. Vo is set at initialisation as the terminal voltage plus Efd0 over KE, so the initial error is zero."
     class="light:sl-hidden" />

### Mathematical Description

$$\Delta V_{AVR} = V_t - V_o + V_{PSS}$$

$$G_{lag}(s) = \frac{1 + sT_A}{1 + sT_B}$$

$$E_{fd}(s) = G_{lag}(\Delta V_{AVR}) \cdot \frac{K_E}{1 + sT_E}, \quad E_{MIN} \le E_{fd} \le E_{MAX}$$

where $V_o = V_t + E_{fd,0}/K_E$ is computed from initial conditions to achieve zero initial error.

### Parameters

| Parameter | Description | Unit/Type |
|---|---|---|
| `TA` | Lead-lag numerator time constant | s |
| `TB` | Lead-lag denominator time constant | s |
| `KE` | Exciter gain | pu |
| `TE` | Exciter time constant | s |
| `EMIN` | Minimum field voltage | pu |
| `EMAX` | Maximum field voltage | pu |

### Variants

| Model | Description |
|---|---|
| `SEXS` | Base simplified exciter |
| `SEXS_IEEEST` | Adds IEEEST PSS (multi-mode: speed, power, or accelerating power input) |
| `SEXS_STAB3_lim` | Adds STAB3 PSS + integral OEL |

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
EXC  SEXS
      # TA: Lead-lag numerator time constant
      0.1
      # TB: Lead-lag denominator time constant
      10.0
      # KE: Exciter gain
      25.0
      # TE: Exciter time constant
      0.5
      # EMIN: Minimum field voltage
      -5.0
      # EMAX: Maximum field voltage
      5.0
TOR  CONSTANT
;
```

</details>

---

## ENTSOE_simp

The ENTSO-E simplified exciter combines a built-in speed-signal PSS with a simple lead-lag AVR and first-order exciter block. It is the standard ENTSO-E model for dynamic studies where detailed exciter data is unavailable.

<img src="/images/models/exc-entsoe-simp-light.svg"
     alt="ENTSOE_simp block diagram. A built-in stabiliser takes the speed deviation through two washouts with TW1 and TW2, a gain KS1 and two lead-lag stages with T1 to T4 to give VPSS. That signal is summed with the terminal voltage and Vo, and the error drives a lead-lag with TA and TB and an exciter of gain KE and time constant TE limited between EMIN and EMAX."
     class="dark:sl-hidden" />
<img src="/images/models/exc-entsoe-simp-dark.svg"
     alt="ENTSOE_simp block diagram. A built-in stabiliser takes the speed deviation through two washouts with TW1 and TW2, a gain KS1 and two lead-lag stages with T1 to T4 to give VPSS. That signal is summed with the terminal voltage and Vo, and the error drives a lead-lag with TA and TB and an exciter of gain KE and time constant TE limited between EMIN and EMAX."
     class="light:sl-hidden" />

### Mathematical Description

The PSS (speed input $\omega - 1$) uses two washout stages and two lead-lag stages:

$$V_{PSS}(s) = (\omega - 1) \cdot \frac{sT_{W1}}{1+sT_{W1}} \cdot \frac{sT_{W2}}{1+sT_{W2}} \cdot K_{S1} \cdot \frac{1+sT_1}{1+sT_2} \cdot \frac{1+sT_3}{1+sT_4}$$

The AVR:

$$\Delta V_{AVR} = V_t - V_o + V_{PSS}$$

$$G_{lag}(s) = \frac{1 + sT_A}{1 + sT_B}$$

$$E_{fd}(s) = G_{lag}(\Delta V_{AVR}) \cdot \frac{K_E}{1 + sT_E}, \quad E_{MIN} \le E_{fd} \le E_{MAX}$$

### Parameters

| Parameter | Description | Unit/Type |
|---|---|---|
| `TW1` | First washout time constant | s |
| `TW2` | Second washout time constant | s |
| `KS1` | PSS gain | pu |
| `T1` | First lead-lag numerator | s |
| `T2` | First lead-lag denominator | s |
| `T3` | Second lead-lag numerator | s |
| `T4` | Second lead-lag denominator | s |
| `VSTMIN` | PSS output lower limit | pu |
| `VSTMAX` | PSS output upper limit | pu |
| `TA` | AVR lead-lag numerator | s |
| `TB` | AVR lead-lag denominator | s |
| `KE` | Exciter gain | pu |
| `TE` | Exciter time constant | s |
| `EMIN` | Minimum field voltage | pu |
| `EMAX` | Maximum field voltage | pu |

### Variants

| Model | Description |
|---|---|
| `ENTSOE_simp` | Base ENTSO-E simplified model with integrated PSS |
| `ENTSOE_lim` | Adds integral OEL (same structure as `AC8B_lim` OEL) |

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
EXC  ENTSOE_simp
      # TW1: First PSS washout time constant (s)
      10.0
      # TW2: Second PSS washout time constant (s)
      3.0
      # KS1: PSS gain, applied in the first lead-lag (pu/pu)
      10.0
      # T1: PSS first lead-lag numerator time constant (s)
      0.2
      # T2: PSS first lead-lag denominator time constant (s)
      0.1
      # T3: PSS second lead-lag numerator time constant (s)
      0.1
      # T4: PSS second lead-lag denominator time constant (s)
      0.1
      # VSTMIN: PSS output lower limit (pu)
      -0.05
      # VSTMAX: PSS output upper limit (pu)
      0.05
      # TA: AVR lead-lag numerator time constant (s)
      0.05
      # TB: AVR lead-lag denominator time constant (s)
      0.1
      # KE: Exciter gain (pu/pu)
      25.0
      # TE: Exciter time constant (s)
      1.0
      # EMIN: Minimum field voltage (pu)
      -10.0
      # EMAX: Maximum field voltage (pu)
      10.0
TOR  CONSTANT
;
```

</details>
