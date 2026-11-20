---
title: Stabilizers and Limiters
description: Power system stabilizer and over-excitation limiter blocks combined with the IEEE exciters in RAMSES
---

The power system stabilizers and over-excitation limiters that the IEEE exciter variants are combined with. They are not entered on their own: each is part of a variant such as `ST1A_PSS2B` or `AC1A_MAXEX2`.

The `EXC` sub-record these models are entered with, and the table of IEEE model variants, are on the [Exciter Models](/models/exciters/) page.

## PSS Models

Power System Stabilizers (PSS) inject an additional signal $V_{PSS}$ at the AVR summation point to damp electromechanical oscillations. All variants listed in the [IEEE model variants table](/models/exciters/#ieee-model-variants) include one of the PSS types described here.

### PSS2B: Dual-Input Stabilizer

PSS2B accepts two input signals (typically speed $\omega$ and electrical power $P_e$) and processes them through independent washout chains before combining. It corresponds to IEEE Std 421.5-2016 Type PSS2B.

:::note[Differences from other vendors' PSS2B]
Implementations of PSS2B vary, so parameter lists do not transfer between tools unchanged. Three differences are worth knowing when porting data in:

- RAMSES names the two transducer lags $T_6$ and $T_7$, following IEEE 421.5. Some tools name the same two constants $T_{W6}$ and $T_{W7}$, which is easy to misread as a third and fourth washout.
- RAMSES has no $K_{S4}$ and no ramp-tracking filter ($AA$, $T_A$, $T_B$). Data sets carrying those come from an extended PSS2B and cannot be transferred field by field.
- RAMSES adds a leading `speedinput` selector that chooses the speed signal source. It has no counterpart elsewhere and must be supplied as the first stabiliser parameter.
:::

$$V_{S1} = \text{clamp}(VSI_1, V_{S1MIN}, V_{S1MAX})$$

Channel 1 (input 1 washout):

$$V_{S1} \xrightarrow{sT_{W1}/(1+sT_{W1})} \xrightarrow{sT_{W2}/(1+sT_{W2})} \xrightarrow{1/(1+sT_6)} pss_{3}$$

Channel 2 (input 2 washout):

$$V_{S2} \xrightarrow{sT_{W3}/(1+sT_{W3})} \xrightarrow{sT_{W4}/(1+sT_{W4})} \xrightarrow{K_{S2}/(1+sT_7)} pss_{6}$$

Combination and lead-lag chain (variant M=5, N=1 implemented):

$$pss_7 = pss_3 - K_{S3} \cdot pss_6$$

$$pss_7 \xrightarrow{(1+sT_8)/(1+sT_9)} \xrightarrow{1/(1+sT_9)^4} pss_{12}$$

$$pss_{13} = pss_{12} + pss_6$$

$$pss_{13} \xrightarrow{K_{S1}(1+sT_1)/(1+sT_2)} \xrightarrow{(1+sT_3)/(1+sT_4)} \xrightarrow{(1+sT_{10})/(1+sT_{11})} V_{PSS}$$

$$V_{PSS} = \text{clamp}(V_{PSS,unlim}, V_{STMIN}, V_{STMAX})$$

**PSS2B Parameters (additional to base exciter):**

| Parameter | Description |
|---|---|
| `speedinput` | Input selection (1=speed+power, 2=power+speed) |
| `TW1`, `TW2` | Channel 1 washout time constants |
| `T6` | Channel 1 filter |
| `TW3`, `TW4` | Channel 2 washout time constants |
| `T7`, `KS2` | Channel 2 filter gain and time constant |
| `KS3` | Channel coupling gain |
| `T8`, `T9` | Ramp-tracking filter |
| `KS1` | Overall PSS gain |
| `T1`–`T4`, `T10`, `T11` | Lead-lag time constants |
| `VS1MIN`, `VS1MAX` | Input 1 limits |
| `VS2MIN`, `VS2MAX` | Input 2 limits |
| `VSTMIN`, `VSTMAX` | Output limits |

---

<img src="/images/models/pss-pss2b-light.svg"
     alt="PSS2B block diagram. Speed passes two washouts with TW1 and TW2 and a transducer lag T6; electrical power passes two washouts with TW3 and TW4 and a transducer lag T7. The two channels are summed, then pass a ramp-tracking filter of N and M stages, two lead-lag stages with T1 to T4, and output limits VSTMIN and VSTMAX."
     class="dark:sl-hidden" />
<img src="/images/models/pss-pss2b-dark.svg"
     alt="PSS2B block diagram. Speed passes two washouts with TW1 and TW2 and a transducer lag T6; electrical power passes two washouts with TW3 and TW4 and a transducer lag T7. The two channels are summed, then pass a ramp-tracking filter of N and M stages, two lead-lag stages with T1 to T4, and output limits VSTMIN and VSTMAX."
     class="light:sl-hidden" />

### PSS3B: Two-Input Second-Order Filter Stabilizer

PSS3B processes two input channels through measurement filters and washout stages, then combines them and applies two cascaded second-order lead-lag filters. It corresponds to IEEE Std 421.5-2016 Type PSS3B.

$$V_{SI1} \xrightarrow{1/(1+sT_1)} \xrightarrow{K_{S1} sT_{W1}/(1+sT_{W1})} pss_2$$

$$V_{SI2} \xrightarrow{1/(1+sT_2)} \xrightarrow{K_{S2} sT_{W2}/(1+sT_{W2})} pss_4$$

$$pss_5 = pss_2 - pss_4$$

$$pss_5 \xrightarrow{K_S sT_{W3}/(sT_{W4}+1)} pss_6$$

$$pss_6 \xrightarrow{\text{TF1: } \frac{A_2 + sA_1 + s^2/A_4}{A_4 + sA_3 + s^2/A_4}} \xrightarrow{\text{TF2: } \frac{A_6+sA_5+s^2/A_8}{A_8+sA_7+s^2/A_8}} V_{PSS}$$

$$V_{PSS} = \text{clamp}(V_{PSS,unlim}, V_{STMIN}, V_{STMAX})$$

**PSS3B Parameters (additional):**

| Parameter | Description |
|---|---|
| `speedinput` | Input mode selection |
| `T1`, `KS1`, `TW1` | Channel 1 filter, gain, washout |
| `T2`, `KS2`, `TW2` | Channel 2 filter, gain, washout |
| `KS`, `TW3`, `TW4` | Combined washout gain and time constants |
| `A1`–`A8` | Second-order filter coefficients |
| `VSTMIN`, `VSTMAX` | Output limits |

---

<img src="/images/models/pss-pss3b-light.svg"
     alt="PSS3B block diagram. Each of the two input signals passes a measurement lag and a washout with its own gain, the second is subtracted from the first, and the difference passes a further washout with TW3 and TW4 and two second-order lead-lag filters TF1 and TF2 to give VPSS."
     class="dark:sl-hidden" />
<img src="/images/models/pss-pss3b-dark.svg"
     alt="PSS3B block diagram. Each of the two input signals passes a measurement lag and a washout with its own gain, the second is subtracted from the first, and the difference passes a further washout with TW3 and TW4 and two second-order lead-lag filters TF1 and TF2 to give VPSS."
     class="light:sl-hidden" />

### PSS4B: Three-Band Multi-Input Stabilizer

PSS4B is a three-band stabilizer that separates the speed deviation signal into low-, intermediate-, and high-frequency components. Each band uses a pair of lead-lag filters. This model corresponds to IEEE Std 421.5-2016 Type PSS4B.

The speed signal $\Delta\omega = \omega - 1$ passes through a digital transducer (`tf2p2z`) to obtain the low/intermediate input. Electrical power $P_e$ passes through two washouts and a low-pass filter to derive the high-frequency component $\Delta\omega_H$.

**Low-frequency band** ($\Delta\omega_{L-I}$ input):

$$pss_4 = \Delta\omega_{L-I} \cdot \frac{K_{L1}(K_{L11} + sT_{L1})}{1 + sT_{L2}}$$

$$pss_5 = \Delta\omega_{L-I} \cdot \frac{K_{L2}(K_{L17} + sT_{L7})}{1 + sT_{L8}}$$

$$V_{PSSL} = \text{clamp}\!\left(K_L(pss_4 - pss_5),\, V_{LMin}, V_{LMax}\right)$$

**Intermediate-frequency band** (same $\Delta\omega_{L-I}$ input):

$$V_{PSSI} = \text{clamp}\!\left(K_I(pss_7 - pss_8),\, V_{IMin}, V_{IMax}\right)$$

**High-frequency band** ($\Delta\omega_H$ input):

$$V_{PSSH} = \text{clamp}\!\left(K_H(pss_{10} - pss_{11}),\, V_{HMin}, V_{HMax}\right)$$

$$V_{PSS} = \text{clamp}(V_{PSSL} + V_{PSSI} + V_{PSSH},\, V_{STMin}, V_{STMax})$$

**PSS4B Parameters (additional):**

| Parameter | Description |
|---|---|
| `H` | Generator inertia constant (for high-freq path) |
| `KL1`, `KL11`, `TL1`, `TL2` | Low-band filter 1 |
| `KL2`, `KL17`, `TL7`, `TL8` | Low-band filter 2 |
| `KL`, `VLMax`, `VLMin` | Low-band gain and limits |
| `KI1`, `KI11`, `TI1`, `TI2` | Intermediate-band filter 1 |
| `KI2`, `KI17`, `TI7`, `TI8` | Intermediate-band filter 2 |
| `KI`, `VIMax`, `VIMin` | Intermediate-band gain and limits |
| `KH1`, `KH11`, `TH1`, `TH2` | High-band filter 1 |
| `KH2`, `KH17`, `TH7`, `TH8` | High-band filter 2 |
| `KH`, `VHMax`, `VHMin` | High-band gain and limits |
| `VSTMax`, `VSTMin` | Total output limits |

---

<img src="/images/models/pss-pss4b-light.svg"
     alt="PSS4B block diagram. The speed deviation passes a digital transducer and electrical power passes two washouts and a low-pass filter. Three bands, low, intermediate and high, each with its own gains and time constants, are summed and limited between VSTMIN and VSTMAX to give VPSS."
     class="dark:sl-hidden" />
<img src="/images/models/pss-pss4b-dark.svg"
     alt="PSS4B block diagram. The speed deviation passes a digital transducer and electrical power passes two washouts and a low-pass filter. Three bands, low, intermediate and high, each with its own gains and time constants, are summed and limited between VSTMIN and VSTMAX to give VPSS."
     class="light:sl-hidden" />

### IEEEST: Single-Input Stabilizer

The IEEEST is a general-purpose single-input PSS with selectable input signal (speed deviation, electrical power, or computed accelerating power). It corresponds to IEEE Std 421.5-2016 Type PSS1A. Two second-order lead-lag filters provide frequency shaping before two first-order lead-lags and a washout stage.

$$VS_1 \xrightarrow{\frac{1}{A_2 + sA_1 + s^2/(A_1 A_2)}} \xrightarrow{\frac{A_6 + sA_5 + s^2/(A_3 A_4)}{A_4 + sA_3 + s^2/(A_3 A_4)}} VS_3$$

$$VS_3 \xrightarrow{\frac{1+sT_1}{1+sT_2}} \xrightarrow{\frac{1+sT_3}{1+sT_4}} \xrightarrow{\frac{K_S sT_5/T_6}{1+sT_6}} V_{PSS}$$

$$V_{PSS} = \text{clamp}(V_{PSS,unlim}, V_{LSMIN}, V_{LSMAX})$$

Input selection (`speedinput`): 1 = rotor speed deviation, 3 = electrical power, 4 = computed accelerating power ($2H \, d\omega/dt$).

**IEEEST Parameters (additional):**

| Parameter | Description |
|---|---|
| `speedinput` | Input mode (1, 3, or 4) |
| `A1`–`A6` | Second-order filter coefficients |
| `T1`–`T6` | Lead-lag and washout time constants |
| `KS` | Overall PSS gain |
| `LSMIN`, `LSMAX` | Output limits |
| `KS4` | Inertia constant for accelerating power (= 2H) |
| `TW4` | Derivative filter time constant |

---

<img src="/images/models/pss-ieeest-light.svg"
     alt="IEEEST block diagram. The selected input signal passes two second-order filters set by the A coefficients, two first-order lead-lag stages with T1 to T4, and a washout of gain KS with T5 and T6, and is finally clamped between LSMIN and LSMAX."
     class="dark:sl-hidden" />
<img src="/images/models/pss-ieeest-dark.svg"
     alt="IEEEST block diagram. The selected input signal passes two second-order filters set by the A coefficients, two first-order lead-lag stages with T1 to T4, and a washout of gain KS with T5 and T6, and is finally clamped between LSMIN and LSMAX."
     class="light:sl-hidden" />

### STAB3: Power-Input Stabilizer

The STAB3 is a simplified PSS that takes electrical power $P_e$ as input, applies two sequential first-order filters and a washout-type derivative block, producing a stabilizing signal.

$$P_e \xrightarrow{1/(1+sT_t)} stab_1 \xrightarrow{1/(1+sT_{X1})} stab_2 \xrightarrow{-K_X s/(1+sT_{X2})} stab_3$$

$$V_{PSS} = \text{clamp}(stab_3, -V_{LIM}, V_{LIM})$$

**STAB3 Parameters:**

| Parameter | Description |
|---|---|
| `Tt` | Input measurement time constant |
| `TX1` | First filter time constant |
| `KX` | Stabilizer gain |
| `TX2` | Washout time constant |
| `VLIM` | Output limit |

---

## OEL and Limiter Models

Over-Excitation Limiters (OEL) prevent sustained field current overloads that would thermally damage the field winding. They generate a signal $V_{OEL}$ that reduces the AVR output when field current exceeds thermal limits.

<img src="/images/models/pss-stab3-light.svg"
     alt="STAB3 block diagram. Electrical power passes a lag of time constant Tt, a second lag TX1, and a washout-type derivative of gain minus KX with time constant TX2, and the result is clamped to plus or minus VLIM."
     class="dark:sl-hidden" />
<img src="/images/models/pss-stab3-dark.svg"
     alt="STAB3 block diagram. Electrical power passes a lag of time constant Tt, a second lag TX1, and a washout-type derivative of gain minus KX with time constant TX2, and the result is clamped to plus or minus VLIM."
     class="light:sl-hidden" />

### MAXEX2: Field Current Limiter with Timer and Hysteresis

The MAXEX2 is a field current limiter derived from IEEE work, using a simplified three-point piece-wise linear timer It is designed for the EXST1/ST1A topology where the OEL output is injected at the reference summation point (not the LV gate).

**Timer phase:** The measured current $I_{fd,mes}$ (selected as either field current or $E_{fd}$ via parameter `IC`) drives a `timer3` block with three $(I_{fd}, T)$ operating points. The `hyst` block latches when timer ≥ 1.

**Integral phase:** Once latched, the error drives a limited integrator:

$$e_{IFD} = I_{fd,ref} - I_{fd,mes}$$

$$\dot{V}_{OEL} = \frac{e_{IFD}}{K_{MX}}, \quad V_{LOW} \le V_{OEL} \le 0$$

$V_{OEL}$ is subtracted from the reference ($V_{REF} - V_{OEL}$, i.e. Negative reduces reference).

**MAXEX2 Parameters:**

| Parameter | Description |
|---|---|
| `IC` | Input selection: 0 = $E_{fd}$, 1 = $I_{fd}$ |
| `IFDrated` | Rated field current (reference) |
| `IFD1`, `TIME1` | Timer point 1 (current level, allowable duration) |
| `IFD2`, `TIME2` | Timer point 2 |
| `IFD3`, `TIME3` | Timer point 3 |
| `IFDDES` | Desired steady-state field current after limiting |
| `KMX` | Integrator time constant inverse (1/KMX = integration rate) |
| `VLOW` | Lower limit of OEL output (e.g. −1.0 pu) |

---

<img src="/images/models/exc-maxex2-light.svg"
     alt="MAXEX2 block diagram. The measured field current, or Efd, drives a timer defined by three current and time points, and a hysteresis block latches once the timer reaches one. Once latched, the error between the reference and measured field currents drives a limited integrator of gain one over KOEL, whose output VOEL is injected at the reference summation rather than at a low-value gate."
     class="dark:sl-hidden" />
<img src="/images/models/exc-maxex2-dark.svg"
     alt="MAXEX2 block diagram. The measured field current, or Efd, drives a timer defined by three current and time points, and a hysteresis block latches once the timer reaches one. Once latched, the error between the reference and measured field currents drives a limited integrator of gain one over KOEL, whose output VOEL is injected at the reference summation rather than at a low-value gate."
     class="light:sl-hidden" />

### Integral OEL (\_lim variants)

The simple integral OEL used in `AC8B_lim`, `ST1A_lim`, `SEXS_STAB3_lim`, and `ENTSOE_lim` variants computes the over-excitation signal through a clamped integrator acting on the difference between measured field current and $1.05 \cdot I_{FDN}$, with an input clamp at $0.35 \cdot I_{FDN}$.

$$\Delta I_{fd,1} = I_{fd} - 1.05 \cdot I_{FDN}$$

$$\Delta I_{fd,2} = \min(\Delta I_{fd,1},\, 0.35 \cdot I_{FDN})$$

$$\dot{x}_{OEL} = \frac{\Delta I_{fd,2}}{T_{OEL}}, \quad L_{OEL} \le x_{OEL} \le U_{OEL}$$

$$V_{OEL} = \text{clamp}(K_{OEL} \cdot x_{OEL},\, OEL_{LI},\, 0)$$

A stator current limiter (SCL) with analogous structure acts on $I_{st} = \sqrt{P^2 + Q^2}/V_t$ relative to $1.025 \cdot I_{GN}$.

**Integral OEL Parameters (in \_lim variants):**

| Parameter | Description |
|---|---|
| `IFDN` | Nominal field current (OEL trigger at 1.05×) |
| `TOEL` | OEL integrator time constant |
| `LOEL` | OEL integrator lower limit |
| `UOEL` | OEL integrator upper limit |
| `KOEL` | OEL output gain |
| `OELLI` | OEL output lower limit |
| `IGN` | Nominal stator current (SCL trigger at 1.025×) |
| `TSCL` | SCL integrator time constant |
| `LSCL` | SCL integrator lower limit |
| `USCL` | SCL integrator upper limit |
| `KSCL` | SCL output gain |
| `SCLLI` | SCL output lower limit |

---

For full documentation of the CODEGEN DSL primitives used in these models (`tf1p`, `tf1p1z`, `tf1plim`, `inlim`, `pictl`, etc.), see the [CODEGEN Blocks](/developer/codegen-blocks/) reference.
<img src="/images/models/exc-integral-oel-light.svg"
     alt="Integral over-excitation limiter block diagram. The field current less 1.05 times the rated field current is clamped above at 0.35 times the rated value, integrated with time constant TOEL between the limits LOEL and UOEL, then scaled by KOEL and clamped between OELLI and zero to give VOEL. The stator current limiter has the same structure on the stator current."
     class="dark:sl-hidden" />
<img src="/images/models/exc-integral-oel-dark.svg"
     alt="Integral over-excitation limiter block diagram. The field current less 1.05 times the rated field current is clamped above at 0.35 times the rated value, integrated with time constant TOEL between the limits LOEL and UOEL, then scaled by KOEL and clamped between OELLI and zero to give VOEL. The stator current limiter has the same structure on the stator current."
     class="light:sl-hidden" />
