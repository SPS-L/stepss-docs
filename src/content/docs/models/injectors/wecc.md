---
title: WECC Wind and Storage
description: The WT3 and WT4 wind turbine models and the BESS model, built from WECC generic blocks
---

The three models on this page are assembled from WECC generic blocks: `WT3` and `WT4` from the second-generation renewable energy system blocks, and `BESS` from REPC_A, REEC_C and REGC_A. [WECC Model Status](#wecc-model-status) comes first because it applies to both wind turbine models: it lists the blocks RAMSES implements, their approval status and the newer blocks it does not implement.

The `INJEC` record these models are entered with, and the rules on model names, are on the [Injector Models](/models/injectors/) page.

## WECC Model Status

`WT3` and `WT4` are assembled from the WECC **second-generation** generic renewable energy system (RES) blocks. Their specification dates from January 2014 [1, 2, 3], and WECC approved the blocks on 19 March 2014 [4]. They are not the first-generation WECC wind models (`wt3g`, `wt3e`, `wt3t`, `wt3p`, `wt4g`, `wt4e`, `wt4t`), which WECC retired on 22 April 2020 [4]; the EPRI user guide [8] explains how to convert data written for those.

Every block that RAMSES implements is still on the WECC approved model list (version September 2026, effective 18 September 2026) [4]. WECC has specified and approved newer blocks since, and RAMSES implements none of them. Statuses and dates below are those of the approved list [4].

**Implemented in RAMSES**

| WECC block | Role | WECC status | WT3 | WT4 |
|---|---|---|---|---|
| REGC_A | Generator/converter interface, current source | Approved 19 March 2014 | Yes | Yes |
| REEC_A | Electrical control | Approved 19 March 2014 | Yes | Yes |
| REPC_A | Plant control | Approved 19 March 2014 | Yes | Yes |
| WTGT_A | Two-mass drivetrain | Approved 19 March 2014 | Yes | Yes |
| WTGA_A (`WTGAR_A` here) | Aerodynamics | Approved 19 March 2014 | Yes | No |
| WTGP_A (`WTGPT_A` here) | Pitch control | Approved 19 March 2014 | Yes | No |
| WTGQ_A (`WTGTRQ_A` here) | Torque control | Approved 19 March 2014 | Yes | No |

The PLL of both models (parameters `vPLL` to `wrefPLL`) is not one of the WECC blocks. RAMSES uses the block names of the 2014 reports, which are also those of PowerWorld; WECC's own names are in the first column.

**Not implemented in RAMSES**

| WECC block | Role | WECC status | Specification |
|---|---|---|---|
| REGC_B | Generator/converter interface, voltage source, for weak grids | Approved 25 August 2020 | [5] |
| REGC_C | Voltage source with a PLL and inner current loops | Not on the approved list | [5] |
| REEC_D | Electrical control with extended voltage-dependent current limits | Approved 25 August 2020 | [5] |
| REEC_E | REEC_D with local PI control of Q, power factor and P | Approved 11 September 2025 | [6] |
| REPC_C | Plant control with power factor control and switched shunts | Approved 1 December 2021 | [5] |
| REPC_D | REPC_C controlling several aggregated units | Approved 24 January 2024 | [6] |
| REPC_E | Plant control built on REPC_D | Approved 17 September 2026 | [4] |
| WTGT_B | Drivetrain for Type 4 turbines | Approved 1 December 2021 | [5] |
| WTGP_B | Pitch control with more flexible limits | Approved 1 December 2021 | [5] |
| WTGWGO_A | Weak-grid option, auxiliary control for Type 4 | Approved 1 December 2021 | [5] |
| WTGIBFFR_A | Inertia-based fast frequency response, auxiliary control | Approved 26 January 2022 | [5] |

REPC_B, the earlier hybrid-plant controller, was withdrawn from the approved list on 29 January 2026 and retired on 23 August 2026 [4]; RAMSES never implemented it. The storage and grid-forming blocks on the same list (REEC_C, REGFM_A1, REGFM_B1, REGFM_C1, REPCGFM_C1) are outside the scope of these two models.

**Type 4 drivetrain.** WECC states that a Type 4 turbine needs none of the mechanical blocks for stability studies, and recommends WTGT_B over WTGT_A when the torsional ripple in the electrical power is to be emulated, because of a problem seen with WTGT_A on Type 4 units [7]. RAMSES `WT4` has WTGT_A only. Set `PFlag` = 0 to take the drivetrain out of the output entirely.

### References

1. WECC, *WECC Second Generation Wind Turbine Models*, 23 January 2014. [PDF (BPA mirror)](https://transmission.bpa.gov/business/operations/GridModeling/WECC%20Second%20Generation%20Wind%20Turbine%20Models%20012314.pdf)
2. P. Pourbeik (EPRI), *WECC Type 3 Wind Turbine Generator Model, Phase II*, 23 January 2014. [PDF](https://www.powerworld.com/WebHelp/Content/Other_Documents/WECC-Type-3-Wind-Turbine-Generator-Model-Phase-II-012314.pdf)
3. P. Pourbeik (EPRI), *WECC Type 4 Wind Turbine Generator Model, Phase II*, 23 January 2013. [PDF](https://www.powerworld.com/WebHelp/Content/Other_Documents/WECC-Type-4-Wind-Turbine-Generator-Model-Phase-II-012313.pdf)
4. WECC, *Approved Dynamic Models*, version September 2026, effective 18 September 2026. [PDF](https://www.wecc.org/sites/default/files/documents/progress_report/2026/Approved%20Dynamic%20Models%20Sept%202026.pdf)
5. P. Pourbeik, *Proposal for New Features for the Renewable Energy System Generic Models*, memo to WECC REMWG, revision 27, 16 February 2023. [PDF](https://www.wecc.org/sites/default/files/documents/meeting/2024/Memo_RES_Modeling_Updates_021623_Rev27b.pdf)
6. P. Pourbeik, *Proposal for New Plant Controller and Electrical Controller*, memo to WECC REMWG, 15 January 2024. [PDF](https://www.wecc.org/sites/default/files/documents/progress_report/2025/Memo_RES_Modeling_Updates_For_New_Plant_and_Electrical_Controls_072525.pdf)
7. WECC REMWG, *Brief Summary of all 2nd Generation Generic Renewable Energy System Dynamic Models*, February 2021. [PDF](https://www.wecc.org/sites/default/files/documents/meeting/2024/Summary%20of%202nd%20Generation%20Generic%20RES%20Models%20%20Rev5.pdf)
8. EPRI, *Model User Guide for Generic Renewable Energy System Models*, product 3002014083, 2018. [PDF (BPA mirror)](https://transmission.bpa.gov/Business/Operations/GridModeling/Model%20User%20Guide%20for%20Generic%20Renewable%20Energy%20System%20Models.pdf)

---

## WT3 (`inj_WT3`): Type 3 Wind Turbine (DFIG)

The data-file model name is `WT3` (or `inj_WT3`).

:::note
Available from RAMSES 3.50. The parameter list below has not changed since that release.
:::

### Description

A generic Type 3 (doubly-fed induction generator) wind turbine built from the WECC second-generation renewable blocks. As in the WECC model, the machine and its rotor-side converter are not represented electrically: the generator/converter block injects a controlled current into the network, and the mechanical side only shapes the active power order. The model has six WECC blocks and a PLL, laid out in the data record in this order:

| Block | Role | WT3 # |
|---|---|---|
| `SNOM` | Rating, the per-unit base of the model | 1 |
| REPC_A | Plant controller: voltage or reactive power regulation, frequency droop | 2–32 |
| WTGTRQ_A | Torque controller: speed reference from a power-speed table, PI on speed or power error | 33–46 |
| WTGPT_A | Pitch controller: limits rotor over-speed and power | 47–56 |
| WTGAR_A | Aerodynamics: mechanical power as a function of pitch angle | 57–58 |
| WTGT_A | Two-mass drivetrain | 59–62 |
| REEC_A | Electrical controller: Q/V loops, voltage-dip logic, current limits, power order | 63–111 |
| REGC_A | Generator/converter interface: current lags, high- and low-voltage current management | 112–124 |
| PLL | Angle of the injected current | 125–128 |

**Per-unit base.** Every power, current and torque inside the model is in per unit on `SNOM` (MVA), not on the system base. Only the injected currents $i_x$, $i_y$ seen by the network are converted to the system base.

**Wind speed is not an input.** The aerodynamic block takes its available power $P_{mo}$ from the initial electrical power of the power flow, so the model represents a turbine running at constant wind.

<img src="/images/models/inj-wt3-light.svg"
     alt="WT3 block diagram. Across the top, the plant controller REPC_A feeds the electrical controller REEC_A, which feeds the generator interface REGC_A and the injected currents ix and iy. Along the bottom, the available power Pmo, equal to the initial electrical power, drives the aerodynamic rotor WTGAR_A, then the two-mass drivetrain WTGT_A, whose speed drives the torque controller WTGTRQ_A and the pitch controller WTGPT_A. The torque controller returns the torque order Pref to the electrical controller, multiplied by the generator speed when PFlag is 1, the pitch controller returns a pitch angle to the rotor, and the electrical torque acts on the drivetrain."
     class="dark:sl-hidden" />
<img src="/images/models/inj-wt3-dark.svg"
     alt="WT3 block diagram. Across the top, the plant controller REPC_A feeds the electrical controller REEC_A, which feeds the generator interface REGC_A and the injected currents ix and iy. Along the bottom, the available power Pmo, equal to the initial electrical power, drives the aerodynamic rotor WTGAR_A, then the two-mass drivetrain WTGT_A, whose speed drives the torque controller WTGTRQ_A and the pitch controller WTGPT_A. The torque controller returns the torque order Pref to the electrical controller, multiplied by the generator speed when PFlag is 1, the pitch controller returns a pitch angle to the rotor, and the electrical torque acts on the drivetrain."
     class="light:sl-hidden" />

### Scientific Description

The equations below are those coded in RAMSES. A flag "= 1" is tested in the dynamics as flag $\geq 0.5$, but initialization tests for exactly 1, so give every flag as exactly `0` or `1`.

**Measurements.** With $v_t = |\bar V|$ the terminal voltage:

$$P_e = (v_x i_x + v_y i_y)\frac{S_{\mathrm{base}}}{S_{\mathrm{nom}}}, \qquad Q_{\mathrm{gen}} = (v_y i_x - v_x i_y)\frac{S_{\mathrm{base}}}{S_{\mathrm{nom}}}$$

**REPC_A, plant controller: voltage or reactive power.** The regulated point is the terminal, shifted by a compensation impedance: $\bar v_{\mathrm{con}} = \bar V - (R_c + jX_c)\bar I$, and $P_{\mathrm{branch}}$, $Q_{\mathrm{branch}}$ are the powers through that point. The measured quantity is

$$Y_1 = \begin{cases} |\bar v_{\mathrm{con}}| & \text{vcompFlag} = 1 \\ v_t + K_c\,Q_{\mathrm{branch}} & \text{vcompFlag} = 0 \end{cases}$$

filtered by $1/(1+sT_{\mathrm{fltr}})$. The error is $v_{\mathrm{ref}} - Y_2$ when RefFlag = 1 and $Q_{\mathrm{ref}} - Q_{\mathrm{branch}}/(1+sT_{\mathrm{fltr}})$ when RefFlag = 0. It passes a symmetric deadband $\pm$`dbd`, the limits [`emin`, `emax`], and a PI controller (`Kp`, `Ki`) whose integrator and output are both limited to [`Qmin`, `Qmax`]. The integrator is frozen while $v_t <$ `vfrz`. A lead-lag $(1+sT_{ft})/(1+sT_{fv})$ follows; with $T_{fv} < 0.005$ s it is bypassed. Its output becomes the reactive power reference $Q_{\mathrm{ext}}$ of REEC_A only when QextFlag = 1; with QextFlag = 0, $Q_{\mathrm{ext}}$ stays at its initial value.

**REPC_A, plant controller: frequency.** The bus frequency is estimated from the rotation of the voltage phasor filtered with $T_m = \max(0.05, T_{\mathrm{mesf}})$:

$$f = \frac{(v_y - v_{yf})\,v_{xf} - (v_x - v_{xf})\,v_{yf}}{2\pi f_{\mathrm{nom}}\, T_m\,(v_{xf}^2 + v_{yf}^2)} + \omega_{\mathrm{ref}}$$

where $\omega_{\mathrm{ref}}$ is 1 or the centre-of-inertia speed, following `$OMEGA_REF`. The frequency error $\Delta f = 1 - f$ passes the deadband [`fdbd1`, `fdbd2`] and the droops:

$$e_P = P_{\mathrm{plantref}} - \frac{P_{\mathrm{branch}}}{1+sT_p} + \min(D_{dn}\Delta f, 0) + \max(D_{up}\Delta f, 0)$$

so `Ddn` acts on over-frequency and `Dup` on under-frequency. $e_P$ is limited to [`femin`, `femax`] and fed to a PI (`kpg`, `kig`) limited to [`Pmin`, `Pmax`], then a lag $1/(1+sT_{\mathrm{lag}})$. The result replaces the active power reference $P_{\mathrm{refo}}$ only when FreqFlag = 1.

**WTGTRQ_A, torque controller.** The electrical power is filtered, $x_{27} = P_e/(1+sT_p)$, and a piecewise-linear table through (`p1`, `spd1`) … (`p4`, `spd4`), flat outside its end points, gives the speed reference:

$$\omega_{\mathrm{ref}} = \frac{f_{\mathrm{spd}}(x_{27})}{1 + sT_{\mathrm{wref}}}$$

The error is $(P_{\mathrm{refo}} - x_{27})/\omega_g$ when Tflag = 1 (power error) and $\omega_g - \omega_{\mathrm{ref}}$ when Tflag = 0 (speed error). A PI (`Kpp`, `Kip`), integrator and output limited to [`Temin`, `Temax`], gives the torque order $P_{\mathrm{ref}}$. The integrator is frozen during a voltage dip.

**WTGPT_A, pitch controller.** Two PI controllers, each limited to [`ThetaMin`, `ThetaMax`], act on the speed error and on the power error:

$$e_\omega = \omega_t - \omega_{\mathrm{ref}} + K_{cc}(P_{\mathrm{ord}} - P_{\mathrm{refo}}), \qquad e_P = P_{\mathrm{ord}} - P_{\mathrm{refo}}$$

(`Kpw`, `Kiw`) on $e_\omega$ and (`Kpc`, `Kic`) on $e_P$. Their sum drives the actuator lag $1/(1+sT_\theta)$, with the rate limited to [`dThetaMin`, `dThetaMax`] and the angle to [`ThetaMin`, `ThetaMax`].

**WTGAR_A, aerodynamics.**

$$P_m = P_{mo} - K_a\,\theta\,(\theta - \theta_0), \qquad P_{mo} = P_{e0}$$

The pitch angle unit is whatever the data uses, conventionally degrees; `Ka` must be given per that unit squared.

**WTGT_A, two-mass drivetrain.** With $T_m = P_m/\omega_t$ and $T_e = P_e/\omega_g$:

$$2H_t\frac{d\Delta\omega_t}{dt} = T_m - K_{\mathrm{shaft}}\Delta\theta - D_{\mathrm{shaft}}(\Delta\omega_t - \Delta\omega_g)$$

$$2H_g\frac{d\Delta\omega_g}{dt} = K_{\mathrm{shaft}}\Delta\theta + D_{\mathrm{shaft}}(\Delta\omega_t - \Delta\omega_g) - T_e$$

$$\frac{d\Delta\theta}{dt} = \Delta\omega_t - \Delta\omega_g, \qquad \omega_t = \omega_o + \Delta\omega_t, \quad \omega_g = \omega_o + \Delta\omega_g$$

The twist equation carries no base angular frequency, so $\Delta\theta$ is in pu·s and `Kshaft` in pu torque per pu·s. A stiffness quoted per electrical radian must be multiplied by $2\pi f_{\mathrm{nom}}$. The initial speed $\omega_o$ is read off the power-speed table at $P_{e0}$, so it is generally not 1.

**REEC_A, electrical controller: voltage dip.** A dip is declared when the unfiltered $v_t <$ `vdip` or $v_t >$ `vup`. During a dip the integrators of the Q, V and torque PIs, the `Tiq` lag and the power order lag are frozen, and the reactive current injection

$$I_{q,\mathrm{inj}} = \mathrm{lim}_{[I_{ql1},\, I_{qh1}]}\Big(k_{qv}\,\mathrm{db}_{[dbd1,\, dbd2]}\big(v_{\mathrm{ref0}} - v_{t,\mathrm{filt}}\big)\Big)$$

is added to the reactive current command, with $v_{t,\mathrm{filt}} = v_t/(1+sT_{rv})$. After the dip ends, `Thld` selects what happens for $|$`Thld`$|$ seconds: with `Thld` $> 0$, $I_{q,\mathrm{inj}}$ is held at `Iqfrz`; with `Thld` $< 0$, the injection law above stays active; with `Thld` $= 0$, $I_{q,\mathrm{inj}}$ returns to zero at once. The active current limit $I_{p\max}$ is frozen during the dip and for `Thld2` seconds after it.

**REEC_A, reactive power chain.** The reactive power reference is

$$Q_r = \mathrm{lim}_{[q_{\min},\, q_{\max}]}\begin{cases} x_{27}\tan(\mathrm{pfaref}) & \text{PFFlag} = 1 \text{ (constant power factor)} \\ Q_{\mathrm{ext}} & \text{PFFlag} = 0 \end{cases}$$

With QFlag = 0 the reactive current command is $\big(Q_r/v_{t,\mathrm{filt}}\big)/(1+sT_{iq})$. With QFlag = 1 it is the output of a voltage PI (`kvp`, `kvi`) on $V_{\mathrm{ref}} - v_{t,\mathrm{filt}}$, limited to [$I_{q\min}$, $I_{q\max}$], where

$$V_{\mathrm{ref}} = \mathrm{lim}_{[v_{\min},\, v_{\max}]}\begin{cases} \text{Q PI } (k_{qp}, k_{qi}) \text{ on } Q_r - Q_{\mathrm{gen}} & \text{vFlag} = 1 \\ Q_r + v_{\mathrm{ref1}} & \text{vFlag} = 0 \end{cases}$$

In both cases $I_{q\mathrm{cmd}} = \mathrm{lim}_{[I_{q\min},\, I_{q\max}]}(I_{q,\mathrm{inj}} + \cdots)$.

**REEC_A, active power chain.** $P_{\mathrm{ref}}$ is rate-limited to [`dPmin`, `dPmax`] (per second). With PFlag = 1 it is multiplied by $\omega_g$, which makes $P_{\mathrm{ref}}$ a torque and lets drivetrain oscillations reach the output. Then

$$T_{\mathrm{pord}}\frac{dP_{\mathrm{ord}}}{dt} = P_{\mathrm{ref}}\,\omega_g^{\,\mathrm{PFlag}} - P_{\mathrm{ord}}, \quad P_{\mathrm{ord}} \in [p_{\min}, p_{\max}], \qquad I_{p\mathrm{cmd}} = \mathrm{lim}_{[0,\, I_{p\max}]}\frac{P_{\mathrm{ord}}}{\max(v_{t,\mathrm{filt}}, 0.01)}$$

**REEC_A, current limits.** `VDL1` (`vq1`…`Iq4`) and `VDL2` (`vp1`…`Ip4`) are piecewise-linear functions of $v_{t,\mathrm{filt}}$, flat beyond their end points. With $I_{q\min} = -I_{q\max}$:

| PQFlag | $I_{q\max}$ | $I_{p\max}$ |
|---|---|---|
| 0 (Q priority) | $\min(\mathrm{VDL1}, I_{\max})$ | $\min\big(\mathrm{VDL2}, \sqrt{I_{\max}^2 - I_{q\mathrm{cmd}}^2}\big)$ |
| 1 (P priority) | $\min\big(\mathrm{VDL1}, \sqrt{I_{\max}^2 - I_{p\mathrm{cmd}}^2}\big)$ | $\min(\mathrm{VDL2}, I_{\max})$ |

**REGC_A, generator/converter.** Both current commands pass a lag of time constant `Tg`. The rate of the reactive current is limited in one direction only, chosen from the sign of the initial reactive power: by `Iqrmax` if $Q_0 > 0$, by `Iqrmin` if $Q_0 < 0$, not at all if $Q_0 = 0$. The rise of the active current is limited to `rrpwr` per second at all times. High-voltage reactive current management and low-voltage active current management then give the injected currents:

$$I_{qf} = \frac{\max\big(I_q v_t - \max(0,\, K_{hv}(v_t - V_{olim})),\ \text{QMIN}\big)}{v_t/(1+sT_{\mathrm{fltr}})}, \qquad I_{pf} = m(v_t)\, I_p$$

where $K_{hv}$ is `accel`, $V_{olim}$ is `vtmax`, and $m$ rises linearly from 0 at `lvpnt0` to 1 at `lvpnt1`. When `Lvplsw` = 1, $I_p$ is also capped by the low-voltage power logic: zero below `zerox`, rising linearly to `Lvpl1` at `Brkpt`, no cap above `Brkpt`. The voltage it uses is $v_t/(1+sT_{\mathrm{fltr}})$.

**PLL.** The voltage components are filtered with $T_{\mathrm{fltr}}$ and

$$v_q = -v_{xf}\sin\theta_{\mathrm{pll}} + v_{yf}\cos\theta_{\mathrm{pll}}, \qquad \omega_{\mathrm{pll}} = k_{p,\mathrm{PLL}}\,v_q + k_{i,\mathrm{PLL}}\!\int v_q\,dt, \qquad \frac{d\theta_{\mathrm{pll}}}{dt} = \omega_{\mathrm{pll}} - \omega_{\mathrm{ref,PLL}}$$

The angle is frozen while the filtered voltage is below `vPLL`. The angle equation carries no base angular frequency, so `kpPLL` and `kiPLL` are in rad/s per pu. `wrefPLL` is also the initial value of $\omega_{\mathrm{pll}}$, so it cancels and has no effect on the response.

**Network interface.** The injected current is resolved with the PLL angle and rescaled to the system base:

$$i_x = \left(I_{pf}\cos\theta_{\mathrm{pll}} + I_{qf}\sin\theta_{\mathrm{pll}}\right)\frac{S_{\mathrm{nom}}}{S_{\mathrm{base}}}, \qquad i_y = \left(I_{pf}\sin\theta_{\mathrm{pll}} - I_{qf}\cos\theta_{\mathrm{pll}}\right)\frac{S_{\mathrm{nom}}}{S_{\mathrm{base}}}$$

A positive $I_{qf}$ injects reactive power. [WT4](#wt4-inj_wt4-type-4-wind-turbine-full-converter) and [BESS](#bess-inj_bess-battery-energy-storage-system) use the same interface.

**Reactive power control modes.** The flags combine as in the WECC specification:

| Mode | PFFlag | vFlag | QFlag | RefFlag | QextFlag |
|---|---|---|---|---|---|
| Constant power factor | 1 | any | 0 | any | 0 |
| Constant Q | 0 | any | 0 | any | 0 |
| Local voltage control | 0 | 0 | 1 | any | 0 |
| Local coordinated Q/V control | 0 | 1 | 1 | any | 0 |
| Plant Q control | 0 | any | 0 | 0 | 1 |
| Plant voltage control | 0 | any | 0 | 1 | 1 |
| Plant voltage control + local coordinated Q/V | 0 | 1 | 1 | 1 | 1 |
| Plant Q control + local coordinated Q/V | 0 | 1 | 1 | 0 | 1 |

### Parameters

RAMSES applies **no default values**: a `WT3` record must carry exactly 128 values, and one with more or fewer is refused. The *Example* column is the record in the usage example below. Per-unit values are on `SNOM` unless stated. The REPC_A, REEC_A, REGC_A and PLL blocks are the same code in WT4 at the indices given in the *WT4 #* column.

**Rating and REPC_A plant controller**

| WT3 # | WT4 # | Name | Description | Unit | Example |
|---|---|---|---|---|---|
| 1 | 1 | `SNOM` | Rating, base of every per-unit quantity in the model | MVA | 1.667 |
| 2 | 2 | `Rc` | Compensation resistance | pu | 0 |
| 3 | 3 | `Xc` | Compensation reactance (droop or line-drop) | pu | 0 |
| 4 | 4 | `vcompFlag` | 1: regulate $\lvert\bar v_{\mathrm{con}}\rvert$ (line-drop compensation); 0: regulate $v_t + K_c Q_{\mathrm{branch}}$ (droop) | | 0 |
| 5 | 5 | `Kc` | Reactive droop gain (used when `vcompFlag` = 0) | pu/pu | 0 |
| 6 | 6 | `Tfltr` | Voltage and Q measurement filter; also the REGC_A voltage filter and the PLL input filter | s | 0.02 |
| 7 | 7 | `RefFlag` | 1: voltage control; 0: reactive power control | | 1 |
| 8 | 8 | `dbd` | Deadband on the V/Q error, symmetric, $\geq 0$ | pu | 0 |
| 9 | 9 | `emax` | Upper limit on the V/Q error | pu | 0.1 |
| 10 | 10 | `emin` | Lower limit on the V/Q error | pu | -0.1 |
| 11 | 11 | `Kp` | V/Q PI proportional gain | pu/pu | 18 |
| 12 | 12 | `Ki` | V/Q PI integral gain | pu/(pu·s) | 5 |
| 13 | 13 | `Qmax` | Upper limit of the V/Q PI | pu | 0.44 |
| 14 | 14 | `Qmin` | Lower limit of the V/Q PI | pu | -0.44 |
| 15 | 15 | `Tft` | Lead time constant | s | 0 |
| 16 | 16 | `Tfv` | Lag time constant; below 0.005 the lead-lag is bypassed | s | 0.05 |
| 17 | 17 | `vfrz` | Voltage below which the V/Q integrator is frozen | pu | 0.7 |
| 18 | 18 | `Tp` | Filter on $P_{\mathrm{branch}}$; also the $P_e$ filter of WTGTRQ_A (WT3) and of the power-factor reference | s | 0.05 |
| 19 | 19 | `fdbd1` | Frequency deadband, lower edge, $\leq 0$ | pu | -0.0006 |
| 20 | 20 | `fdbd2` | Frequency deadband, upper edge, $\geq 0$ | pu | 0.0006 |
| 21 | 21 | `Ddn` | Droop for over-frequency | pu/pu | 20 |
| 22 | 22 | `Dup` | Droop for under-frequency | pu/pu | 0 |
| 23 | 23 | `femax` | Upper limit on the power error | pu | 999 |
| 24 | 24 | `femin` | Lower limit on the power error | pu | -999 |
| 25 | 25 | `kpg` | Power PI proportional gain | pu/pu | 0.05 |
| 26 | 26 | `kig` | Power PI integral gain | pu/(pu·s) | 0.1 |
| 27 | 27 | `Pmax` | Upper limit of the power PI | pu | 1 |
| 28 | 28 | `Pmin` | Lower limit of the power PI | pu | 0 |
| 29 | 29 | `Tlag` | Lag on the plant power output | s | 0.1 |
| 30 | 30 | `FreqFlag` | 1: plant power loop sets $P_{\mathrm{refo}}$; 0: $P_{\mathrm{refo}}$ held at its initial value | | 0 |
| 31 | 31 | `Tmesf` | Frequency measurement time constant, raised to 0.05 if smaller | s | 0.02 |
| 32 | 32 | `QextFlag` | 1: plant V/Q loop sets $Q_{\mathrm{ext}}$; 0: $Q_{\mathrm{ext}}$ held at its initial value | | 0 |

With `FreqFlag` = 0 and `QextFlag` = 0, as in the example, REPC_A is computed but drives nothing.

**WTGTRQ_A torque controller** (WT3 only)

| WT3 # | Name | Description | Unit | Example |
|---|---|---|---|---|
| 33 | `Twref` | Speed reference time constant | s | 30 |
| 34 | `Kip` | Torque PI integral gain | pu/(pu·s) | 0.6 |
| 35 | `Kpp` | Torque PI proportional gain | pu/pu | 3 |
| 36 | `Temax` | Maximum torque order | pu | 1.2 |
| 37 | `Temin` | Minimum torque order | pu | 0 |
| 38 | `p1` | Power-speed table, power of point 1 | pu | 0.2 |
| 39 | `spd1` | Power-speed table, speed of point 1 | pu | 0.58 |
| 40 | `p2` | Point 2, power | pu | 0.4 |
| 41 | `spd2` | Point 2, speed | pu | 0.72 |
| 42 | `p3` | Point 3, power | pu | 0.6 |
| 43 | `spd3` | Point 3, speed | pu | 0.86 |
| 44 | `p4` | Point 4, power | pu | 0.8 |
| 45 | `spd4` | Point 4, speed | pu | 1.0 |
| 46 | `Tflag` | 1: PI on power error; 0: PI on speed error | | 1 |

**WTGPT_A pitch controller** (WT3 only)

| WT3 # | Name | Description | Unit | Example |
|---|---|---|---|---|
| 47 | `Kcc` | Gain of the power error added to the speed error | pu/pu | 0 |
| 48 | `Kiw` | Pitch control integral gain | deg/(pu·s) | 0.6 |
| 49 | `Kpw` | Pitch control proportional gain | deg/pu | 0.3 |
| 50 | `ThetaMin` | Minimum pitch angle (also limits both PIs) | deg | 0 |
| 51 | `ThetaMax` | Maximum pitch angle (also limits both PIs) | deg | 27 |
| 52 | `Ttheta` | Pitch actuator time constant | s | 0.3 |
| 53 | `Kic` | Pitch compensation integral gain | deg/(pu·s) | 0.6 |
| 54 | `Kpc` | Pitch compensation proportional gain | deg/pu | 3 |
| 55 | `dThetaMin` | Minimum pitch rate | deg/s | -10 |
| 56 | `dThetaMax` | Maximum pitch rate | deg/s | 10 |

**WTGAR_A aerodynamics and WTGT_A drivetrain** (WT3 only; WT4 has its own drivetrain block, listed under [WT4](#wt4-inj_wt4-type-4-wind-turbine-full-converter))

| WT3 # | Name | Description | Unit | Example |
|---|---|---|---|---|
| 57 | `Ka` | Aerodynamic gain | pu/deg² | 0.007 |
| 58 | `Thetao` | Initial pitch angle $\theta_0$ | deg | 0 |
| 59 | `Ht` | Turbine inertia | s | 3.395 |
| 60 | `Hg` | Generator inertia | s | 0.962 |
| 61 | `Dshaft` | Shaft damping | pu/pu | 2.344 |
| 62 | `Kshaft` | Shaft stiffness, per pu·s of twist | pu | 1.387 |

**REEC_A electrical controller**

| WT3 # | WT4 # | Name | Description | Unit | Example |
|---|---|---|---|---|---|
| 63 | 38 | `vdip` | Voltage below which a dip is declared | pu | 0.9 |
| 64 | 39 | `vup` | Voltage above which a dip is declared | pu | 1.1 |
| 65 | 40 | `Trv` | Terminal voltage filter | s | 0.02 |
| 66 | 41 | `vref0` | Reference for the dip injection; used as given, so 0 is not replaced by the initial voltage | pu | 1 |
| 67 | 42 | `vref1` | Bias added to $Q_r$ when vFlag = 0 | pu | 1 |
| 68 | 43 | `dbd1` | Dip injection deadband, lower edge, $\leq 0$ | pu | -0.05 |
| 69 | 44 | `dbd2` | Dip injection deadband, upper edge, $\geq 0$ | pu | 0.05 |
| 70 | 45 | `kqv` | Dip reactive current gain | pu/pu | 2 |
| 71 | 46 | `Iqh1` | Upper limit of the dip injection | pu | 1.05 |
| 72 | 47 | `Iql1` | Lower limit of the dip injection | pu | -1.05 |
| 73 | 48 | `qmax` | Upper limit of $Q_r$ | pu | 0.44 |
| 74 | 49 | `qmin` | Lower limit of $Q_r$ | pu | -0.44 |
| 75 | 50 | `vmax` | Upper limit of $V_{\mathrm{ref}}$ and of the Q PI | pu | 1.1 |
| 76 | 51 | `vmin` | Lower limit of $V_{\mathrm{ref}}$ and of the Q PI | pu | 0.9 |
| 77 | 52 | `kqp` | Q PI proportional gain | pu/pu | 0 |
| 78 | 53 | `kqi` | Q PI integral gain | pu/(pu·s) | 0.1 |
| 79 | 54 | `kvp` | V PI proportional gain | pu/pu | 0 |
| 80 | 55 | `kvi` | V PI integral gain | pu/(pu·s) | 40 |
| 81 | 56 | `Tiq` | Reactive current lag (QFlag = 0) | s | 0.02 |
| 82 | 57 | `vq1` | VDL1, voltage of point 1 | pu | 0.2 |
| 83 | 58 | `Iq1` | VDL1, reactive current limit at point 1 | pu | 1 |
| 84 | 59 | `vq2` | VDL1, point 2 | pu | 0.4 |
| 85 | 60 | `Iq2` | | pu | 1 |
| 86 | 61 | `vq3` | VDL1, point 3 | pu | 0.8 |
| 87 | 62 | `Iq3` | | pu | 1 |
| 88 | 63 | `vq4` | VDL1, point 4 | pu | 1 |
| 89 | 64 | `Iq4` | | pu | 1 |
| 90 | 65 | `vp1` | VDL2, voltage of point 1 | pu | 0.2 |
| 91 | 66 | `Ip1` | VDL2, active current limit at point 1 | pu | 1 |
| 92 | 67 | `vp2` | VDL2, point 2 | pu | 0.4 |
| 93 | 68 | `Ip2` | | pu | 1 |
| 94 | 69 | `vp3` | VDL2, point 3 | pu | 0.8 |
| 95 | 70 | `Ip3` | | pu | 1 |
| 96 | 71 | `vp4` | VDL2, point 4 | pu | 1 |
| 97 | 72 | `Ip4` | | pu | 1 |
| 98 | 73 | `dPmax` | Upper rate limit of $P_{\mathrm{ref}}$ | pu/s | 999 |
| 99 | 74 | `dPmin` | Lower rate limit of $P_{\mathrm{ref}}$ | pu/s | -999 |
| 100 | 75 | `pmax` | Upper limit of $P_{\mathrm{ord}}$ | pu | 1 |
| 101 | 76 | `pmin` | Lower limit of $P_{\mathrm{ord}}$ | pu | 0 |
| 102 | 77 | `Tpord` | Power order lag | s | 0.02 |
| 103 | 78 | `Imax` | Converter current limit | pu | 1.11 |
| 104 | 79 | `Thld` | Post-dip hold of the reactive injection; its sign selects the mode | s | 0 |
| 105 | 80 | `Thld2` | Post-dip hold of $I_{p\max}$ | s | 0 |
| 106 | 81 | `Iqfrz` | Reactive injection held after a dip when `Thld` $> 0$ | pu | 0 |
| 107 | 82 | `PFFlag` | 1: constant power factor; 0: reactive power reference $Q_{\mathrm{ext}}$ | | 0 |
| 108 | 83 | `vFlag` | 1: $V_{\mathrm{ref}}$ from the Q PI; 0: $V_{\mathrm{ref}} = Q_r + v_{\mathrm{ref1}}$ | | 0 |
| 109 | 84 | `QFlag` | 1: reactive current from the voltage PI; 0: from $Q_r/v_t$ | | 0 |
| 110 | 85 | `PQFlag` | 1: active current priority; 0: reactive current priority | | 0 |
| 111 | 86 | `PFlag` | 1: power order is $P_{\mathrm{ref}}\,\omega_g$; 0: power order is $P_{\mathrm{ref}}$ | | 1 |

**REGC_A generator/converter and PLL**

| WT3 # | WT4 # | Name | Description | Unit | Example |
|---|---|---|---|---|---|
| 112 | 87 | `Iqrmax` | Reactive current rate limit, used when $Q_0 > 0$ | pu/s | 999 |
| 113 | 88 | `Iqrmin` | Reactive current rate limit, used when $Q_0 < 0$ | pu/s | -999 |
| 114 | 89 | `Tg` | Converter current lag | s | 0.02 |
| 115 | 90 | `vtmax` | High-voltage threshold (WECC `Volim`) | pu | 1.2 |
| 116 | 91 | `accel` | High-voltage reactive current gain (WECC `Khv`) | pu/pu | 0.7 |
| 117 | 92 | `QMIN` | Lower limit of $I_q v_t$ less the high-voltage term (WECC `Iolim`) | pu | -1.3 |
| 118 | 93 | `lvpnt0` | Active current is zero below this voltage | pu | 0.4 |
| 119 | 94 | `lvpnt1` | Active current is unreduced above this voltage | pu | 0.8 |
| 120 | 95 | `Brkpt` | Low-voltage power logic breakpoint | pu | 0.9 |
| 121 | 96 | `zerox` | Low-voltage power logic zero crossing | pu | 0.4 |
| 122 | 97 | `Lvpl1` | Low-voltage power logic limit at `Brkpt` | pu | 1.22 |
| 123 | 98 | `Lvplsw` | 1: low-voltage power logic on; 0: off | | 0 |
| 124 | 99 | `rrpwr` | Active current rise rate limit | pu/s | 10 |
| 125 | 100 | `vPLL` | Voltage below which the PLL angle is frozen | pu | 0.2 |
| 126 | 101 | `kpPLL` | PLL proportional gain | rad/s/pu | 3 |
| 127 | 102 | `kiPLL` | PLL integral gain | rad/s²/pu | 30 |
| 128 | 103 | `wrefPLL` | PLL frequency offset; cancels, no effect on the response | | 1 |

**Time constants.** A zero `Tfltr`, `Tp`, `Tlag`, `Twref` or `Trv` turns its block into a direct pass-through. `Ttheta` below 0.001 does the same for the pitch actuator but also removes every pitch limit, including those of the two PIs.

:::caution
Keep `Tiq`, `Tpord` and `Tg` at 0.005 s or more, and `Ht` and `Hg` well above zero. Below that threshold RAMSES switches these blocks to an algebraic form that does not reduce to a pass-through: `Tiq` and `Tpord` then give half the intended value, and `Tg` breaks the active current channel.
:::

Thirty-one further parameters are computed at initialization. Among them are the power-flow quantities `vto`, `Peo`, `Qgeno` and `pfaref` (the initial power factor angle, rad), the references `Qextini`, `Prefini`, `vref`, `Qref` and `Plantpref` held by REPC_A, and `wo`, the initial speed read off the power-speed table.

### Observables

All quantities are in pu on `SNOM`.

| Name | Description | Name | Description |
|---|---|---|---|
| `Pe`, `Qgen` | Terminal active and reactive power | `wg`, `wt` | Generator and turbine speed |
| `vt` | Terminal voltage | `wref` | Speed reference |
| `Freq` | Measured frequency | `Pref` | Torque order from WTGTRQ_A |
| `vcon` | Compensated voltage | `Pord` | Power order |
| `Pbranch`, `Qbranch` | Powers at the compensated point | `Theta` | Pitch angle (data unit, degrees by convention) |
| `Prefo`, `Qext` | Active and reactive references into WTGTRQ_A and REEC_A | `Pm`, `Tm`, `Te` | Mechanical power, mechanical and electrical torque |
| `Plantpref`, `Qref`, `vref` | REPC_A references, constant | `Iqinj` | Dip reactive current injection |
| `Ipcmd`, `Iqcmd` | Current commands | `Ipmax`, `Iqmax`, `Iqmin` | Current limits |
| `Ipf`, `Iqf` | Injected currents | `x59` | Low-voltage power logic limit on $I_p$; reads $10^9$ when inactive |

### Initialization

The model initializes from the power-flow voltage and injection: the PLL angle from the bus voltage angle, the converter currents by rotation into that frame, then every block backwards to its references. The mechanical side starts with $P_m = P_e$ and the speed read off the power-speed table.

RAMSES stops the simulation if the initial point violates the current limits or the dip thresholds: $I_{q\mathrm{cmd}}$ outside $\pm I_{q\max}$, $I_{p\mathrm{cmd}}$ outside $[0, I_{p\max}]$ (which also rejects a unit absorbing active power), or $v_t$ outside [`vdip`, `vup`]. No other limit is checked, so a PI or a lag can start on its limit without a warning. The initial voltage must also exceed `lvpnt0`.

### Usage Example

A 1.667 MVA unit taking its whole operating point from the power flow (`FP` = `FQ` = 1), with the plant controller disconnected (`FreqFlag` = `QextFlag` = 0), constant reactive power and the drivetrain coupled to the output (`PFlag` = 1). This is the record of the `3-bus` case in `stepss-test-systems`. Lines starting with `#` inside a record are ignored.

<details>
<summary>Show the data record</summary>

```
INJEC  WT3  DFIGB03  B03
      # FP FQ P Q: share of the power-flow injection (FP, FQ) or initial power (P in MW, Q in Mvar)
      1.  1.  0.  0.
      # SNOM: Rating, base of every per-unit quantity in the model (MVA)
      1.667
      # Rc: Compensation resistance (pu)
      0
      # Xc: Compensation reactance (droop or line-drop) (pu)
      0
      # vcompFlag: 1: regulate lvertbar v_conrvert (line-drop compensation); 0: regulate v_t + K_c Q_branch (droop)
      0
      # Kc: Reactive droop gain (used when vcompFlag = 0) (pu/pu)
      0
      # Tfltr: Voltage and Q measurement filter; also the REGC_A voltage filter and the PLL input filter (s)
      0.02
      # RefFlag: 1: voltage control; 0: reactive power control
      1
      # dbd: Deadband on the V/Q error, symmetric, geq 0 (pu)
      0
      # emax: Upper limit on the V/Q error (pu)
      0.1
      # emin: Lower limit on the V/Q error (pu)
      -0.1
      # Kp: V/Q PI proportional gain (pu/pu)
      18
      # Ki: V/Q PI integral gain (pu/(pu·s))
      5
      # Qmax: Upper limit of the V/Q PI (pu)
      0.44
      # Qmin: Lower limit of the V/Q PI (pu)
      -0.44
      # Tft: Lead time constant (s)
      0
      # Tfv: Lag time constant; below 0.005 the lead-lag is bypassed (s)
      0.05
      # vfrz: Voltage below which the V/Q integrator is frozen (pu)
      0.7
      # Tp: Filter on P_branch; also the P_e filter of WTGTRQ_A (WT3) and of the power-factor reference (s)
      0.05
      # fdbd1: Frequency deadband, lower edge, leq 0 (pu)
      -0.0006
      # fdbd2: Frequency deadband, upper edge, geq 0 (pu)
      0.0006
      # Ddn: Droop for over-frequency (pu/pu)
      20
      # Dup: Droop for under-frequency (pu/pu)
      0
      # femax: Upper limit on the power error (pu)
      999
      # femin: Lower limit on the power error (pu)
      -999
      # kpg: Power PI proportional gain (pu/pu)
      0.05
      # kig: Power PI integral gain (pu/(pu·s))
      0.1
      # Pmax: Upper limit of the power PI (pu)
      1
      # Pmin: Lower limit of the power PI (pu)
      0
      # Tlag: Lag on the plant power output (s)
      0.1
      # FreqFlag: 1: plant power loop sets P_refo; 0: P_refo held at its initial value
      0
      # Tmesf: Frequency measurement time constant, raised to 0.05 if smaller (s)
      0.02
      # QextFlag: 1: plant V/Q loop sets Q_ext; 0: Q_ext held at its initial value
      0
      # Twref: Speed reference time constant (s)
      30
      # Kip: Torque PI integral gain (pu/(pu·s))
      0.6
      # Kpp: Torque PI proportional gain (pu/pu)
      3
      # Temax: Maximum torque order (pu)
      1.2
      # Temin: Minimum torque order (pu)
      0
      # p1: Power-speed table, power of point 1 (pu)
      0.2
      # spd1: Power-speed table, speed of point 1 (pu)
      0.58
      # p2: Point 2, power (pu)
      0.4
      # spd2: Point 2, speed (pu)
      0.72
      # p3: Point 3, power (pu)
      0.6
      # spd3: Point 3, speed (pu)
      0.86
      # p4: Point 4, power (pu)
      0.8
      # spd4: Point 4, speed (pu)
      1
      # Tflag: 1: PI on power error; 0: PI on speed error
      1
      # Kcc: Gain of the power error added to the speed error (pu/pu)
      0
      # Kiw: Pitch control integral gain (deg/(pu·s))
      0.6
      # Kpw: Pitch control proportional gain (deg/pu)
      0.3
      # ThetaMin: Minimum pitch angle (also limits both PIs) (deg)
      0
      # ThetaMax: Maximum pitch angle (also limits both PIs) (deg)
      27
      # Ttheta: Pitch actuator time constant (s)
      0.3
      # Kic: Pitch compensation integral gain (deg/(pu·s))
      0.6
      # Kpc: Pitch compensation proportional gain (deg/pu)
      3
      # dThetaMin: Minimum pitch rate (deg/s)
      -10
      # dThetaMax: Maximum pitch rate (deg/s)
      10
      # Ka: Aerodynamic gain (pu/deg²)
      0.007
      # Thetao: Initial pitch angle theta_0 (deg)
      0
      # Ht: Turbine inertia (s)
      3.395
      # Hg: Generator inertia (s)
      0.962
      # Dshaft: Shaft damping (pu/pu)
      2.344
      # Kshaft: Shaft stiffness, per pu·s of twist (pu)
      1.387
      # vdip: Voltage below which a dip is declared (pu)
      0.9
      # vup: Voltage above which a dip is declared (pu)
      1.1
      # Trv: Terminal voltage filter (s)
      0.02
      # vref0: Reference for the dip injection; used as given, so 0 is not replaced by the initial voltage (pu)
      1
      # vref1: Bias added to Q_r when vFlag = 0 (pu)
      1
      # dbd1: Dip injection deadband, lower edge, leq 0 (pu)
      -0.05
      # dbd2: Dip injection deadband, upper edge, geq 0 (pu)
      0.05
      # kqv: Dip reactive current gain (pu/pu)
      2
      # Iqh1: Upper limit of the dip injection (pu)
      1.05
      # Iql1: Lower limit of the dip injection (pu)
      -1.05
      # qmax: Upper limit of the reactive power reference (pu)
      0.44
      # qmin: Lower limit of the reactive power reference (pu)
      -0.44
      # vmax: Upper limit of V_ref and of the Q PI (pu)
      1.1
      # vmin: Lower limit of V_ref and of the Q PI (pu)
      0.9
      # kqp: Q PI proportional gain (pu/pu)
      0
      # kqi: Q PI integral gain (pu/(pu·s))
      0.1
      # kvp: V PI proportional gain (pu/pu)
      0
      # kvi: V PI integral gain (pu/(pu·s))
      40
      # Tiq: Reactive current lag (QFlag = 0) (s)
      0.02
      # vq1: VDL1, voltage of point 1 (pu)
      0.2
      # Iq1: VDL1, reactive current limit at point 1 (pu)
      1
      # vq2: VDL1, point 2 (pu)
      0.4
      # Iq2:  (pu)
      1
      # vq3: VDL1, point 3 (pu)
      0.8
      # Iq3:  (pu)
      1
      # vq4: VDL1, point 4 (pu)
      1
      # Iq4:  (pu)
      1
      # vp1: VDL2, voltage of point 1 (pu)
      0.2
      # Ip1: VDL2, active current limit at point 1 (pu)
      1
      # vp2: VDL2, point 2 (pu)
      0.4
      # Ip2:  (pu)
      1
      # vp3: VDL2, point 3 (pu)
      0.8
      # Ip3:  (pu)
      1
      # vp4: VDL2, point 4 (pu)
      1
      # Ip4:  (pu)
      1
      # dPmax: Upper rate limit of P_ref (pu/s)
      999
      # dPmin: Lower rate limit of P_ref (pu/s)
      -999
      # pmax: Upper limit of the power order Pord (pu)
      1
      # pmin: Lower limit of the power order Pord (pu)
      0
      # Tpord: Power order lag (s)
      0.02
      # Imax: Converter current limit (pu)
      1.11
      # Thld: Post-dip hold of the reactive injection; its sign selects the mode (s)
      0
      # Thld2: Post-dip hold of I_pmax (s)
      0
      # Iqfrz: Reactive injection held after a dip when Thld > 0 (pu)
      0
      # PFFlag: 1: constant power factor; 0: reactive power reference Q_ext
      0
      # vFlag: 1: V_ref from the Q PI; 0: V_ref = Q_r + v_ref1
      0
      # QFlag: 1: reactive current from the voltage PI; 0: from Q_r/v_t
      0
      # PQFlag: 1: active current priority; 0: reactive current priority
      0
      # PFlag: 1: power order is P_ref,omega_g; 0: power order is P_ref
      1
      # Iqrmax: Reactive current rate limit, used when Q_0 > 0 (pu/s)
      999
      # Iqrmin: Reactive current rate limit, used when Q_0 < 0 (pu/s)
      -999
      # Tg: Converter current lag (s)
      0.02
      # vtmax: High-voltage threshold (WECC Volim) (pu)
      1.2
      # accel: High-voltage reactive current gain (WECC Khv) (pu/pu)
      0.7
      # QMIN: Lower limit of the converter reactive output after the high-voltage reduction (pu)
      -1.3
      # lvpnt0: Active current is zero below this voltage (pu)
      0.4
      # lvpnt1: Active current is unreduced above this voltage (pu)
      0.8
      # Brkpt: Low-voltage power logic breakpoint (pu)
      0.9
      # zerox: Low-voltage power logic zero crossing (pu)
      0.4
      # Lvpl1: Low-voltage power logic limit at Brkpt (pu)
      1.22
      # Lvplsw: 1: low-voltage power logic on; 0: off
      0
      # rrpwr: Active current rise rate limit (pu/s)
      10
      # vPLL: Voltage below which the PLL angle is frozen (pu)
      0.2
      # kpPLL: PLL proportional gain (rad/s/pu)
      3
      # kiPLL: PLL integral gain (rad/s²/pu)
      30
      # wrefPLL: PLL frequency offset; cancels, no effect on the response
      1
;
```

</details>

:::note
With this record RAMSES reports `INJECTORS NOT IN STEADY STATE` at initialization. The residuals are on the Q and V PI controllers of REEC_A, which `QFlag` = 0 takes out of the loop, and whose initial values the model does not yet set consistently; one of their limiters also toggles during the first time step.
:::

---

## WT4 (`inj_WT4`): Type 4 Wind Turbine (Full Converter)

The data-file model name is `WT4` (or `inj_WT4`).

:::note
Available from RAMSES 3.50. The parameter list below has not changed since that release.
:::

### Description

A generic Type 4 (full converter) wind turbine. It is [WT3](#wt3-inj_wt3-type-3-wind-turbine-dfig) without the torque controller, the pitch controller and the aerodynamic block: the generator is decoupled from the grid by the converter, the mechanical torque is constant, and a two-mass drivetrain is kept only so that its torsional oscillations can appear in the output. Its WECC blocks, their approval status and the newer blocks RAMSES does not implement are listed under [WECC Model Status](#wecc-model-status).

| Block | Role | WT4 # |
|---|---|---|
| `SNOM` | Rating, the per-unit base of the model | 1 |
| REPC_A | Plant controller, [as in WT3](#wt3-inj_wt3-type-3-wind-turbine-dfig) | 2–32 |
| WTGT_A | Two-mass drivetrain | 33–37 |
| REEC_A | Electrical controller, [as in WT3](#wt3-inj_wt3-type-3-wind-turbine-dfig) | 38–86 |
| REGC_A | Generator/converter interface, [as in WT3](#wt3-inj_wt3-type-3-wind-turbine-dfig) | 87–99 |
| PLL | Angle of the injected current, [as in WT3](#wt3-inj_wt3-type-3-wind-turbine-dfig) | 100–103 |

REPC_A, REEC_A, REGC_A, the PLL and the network interface are the same code as in WT3, and their equations are given in the [WT3 description](#wt3-inj_wt3-type-3-wind-turbine-dfig). Every power, current and torque is in per unit on `SNOM`.

<img src="/images/models/inj-wt4-light.svg"
     alt="WT4 block diagram. The plant controller REPC_A feeds a power order ramp limited by dPmax and dPmin, then the electrical controller REEC_A and the generator interface REGC_A, which injects ix and iy. Below, the constant mechanical torque Tmo drives the two-mass drivetrain WTGT_A to give the generator speed, which returns to the electrical controller when PFlag is 1, with the electrical torque acting on the drivetrain from the electrical controller. There is no pitch controller and no aerodynamic rotor."
     class="dark:sl-hidden" />
<img src="/images/models/inj-wt4-dark.svg"
     alt="WT4 block diagram. The plant controller REPC_A feeds a power order ramp limited by dPmax and dPmin, then the electrical controller REEC_A and the generator interface REGC_A, which injects ix and iy. Below, the constant mechanical torque Tmo drives the two-mass drivetrain WTGT_A to give the generator speed, which returns to the electrical controller when PFlag is 1, with the electrical torque acting on the drivetrain from the electrical controller. There is no pitch controller and no aerodynamic rotor."
     class="light:sl-hidden" />

### Scientific Description

**WTGT_A, two-mass drivetrain.** The mechanical torque is the constant $T_{mo} = P_{e0}/\omega_o$ and $T_e = P_e/\omega_g$:

$$2H_t\frac{d\Delta\omega_t}{dt} = T_{mo} - K_{\mathrm{shaft}}\Delta\theta - D_{\mathrm{shaft}}(\Delta\omega_t - \Delta\omega_g)$$

$$2H_g\frac{d\Delta\omega_g}{dt} = K_{\mathrm{shaft}}\Delta\theta + D_{\mathrm{shaft}}(\Delta\omega_t - \Delta\omega_g) - T_e$$

$$\frac{d\Delta\theta}{dt} = \Delta\omega_t - \Delta\omega_g, \qquad \omega_g = \omega_o + \Delta\omega_g$$

As in WT3, the twist equation carries no base angular frequency, so `Kshaft` is per pu·s of twist. Unlike WT3, the initial speed $\omega_o$ is a data parameter.

**Coupling to the output.** The drivetrain reaches the network only through `PFlag`. With PFlag = 1 the power order is $P_{\mathrm{ref}}\,\omega_g$, so a torsional oscillation of $\omega_g$ modulates the active current. With PFlag = 0 the drivetrain is still computed but has no effect on the injection. The active power reference $P_{\mathrm{ref}}$ is constant unless REPC_A drives it (FreqFlag = 1), and is rate-limited by `dPmax` and `dPmin`.

### Parameters

RAMSES applies **no default values**: a `WT4` record must carry exactly 103 values, and one with more or fewer is refused. Parameters 1–32 and 38–103 are listed in the parameter tables of [WT3](#wt3-inj_wt3-type-3-wind-turbine-dfig) under their *WT4 #*. The drivetrain block is specific to WT4:

| WT4 # | Name | Description | Unit | Example |
|---|---|---|---|---|
| 33 | `Ht` | Turbine inertia | s | 3.395 |
| 34 | `Hg` | Generator inertia | s | 0.962 |
| 35 | `wo` | Initial generator speed, the reference of $\Delta\omega_g$ | pu | 1 |
| 36 | `Dshaft` | Shaft damping | pu/pu | 2.344 |
| 37 | `Kshaft` | Shaft stiffness, per pu·s of twist | pu | 1.387 |

The time-constant caution under the [WT3 parameters](#wt3-inj_wt3-type-3-wind-turbine-dfig) applies here too.

Twenty-eight further parameters are computed at initialization, the same as WT3 less the mechanical ones, plus `Tmo`, the constant mechanical torque.

### Observables

All quantities are in pu on `SNOM`.

| Name | Description | Name | Description |
|---|---|---|---|
| `Pe`, `Qgen` | Terminal active and reactive power | `wg` | Generator speed |
| `vt` | Terminal voltage | `Te` | Electrical torque |
| `Freq` | Measured frequency | `Tmo` | Mechanical torque, constant |
| `vcon` | Compensated voltage | `Iqinj` | Dip reactive current injection |
| `Pbranch`, `Qbranch` | Powers at the compensated point | `Ipcmd`, `Iqcmd` | Current commands |
| `Pref`, `Qext` | Active and reactive references into REEC_A | `Ipmax`, `Iqmax`, `Iqmin` | Current limits |
| `Plantpref`, `Qref`, `vref` | REPC_A references, constant | `Ip`, `Iq` | Converter currents before the voltage management |
| `pfaref` | Initial power factor angle (rad), constant | `Ipf`, `Iqf` | Injected currents |
| | | `x59` | Low-voltage power logic limit on $I_p$; reads $10^9$ when inactive |

The initialization and its checks are those of [WT3](#wt3-inj_wt3-type-3-wind-turbine-dfig).

### Usage Example

The WT3 example unit as a full converter: the same REPC_A, REEC_A, REGC_A and PLL values, with the drivetrain block in place of WTGTRQ_A, WTGPT_A, WTGAR_A and WTGT_A.

<details>
<summary>Show the data record</summary>

```
INJEC  WT4  WT4B03  B03
      # FP FQ P Q: share of the power-flow injection (FP, FQ) or initial power (P in MW, Q in Mvar)
      1.  1.  0.  0.
      # SNOM: Rating, base of every per-unit quantity in the model (MVA)
      1.667
      # Rc: Compensation resistance (pu)
      0
      # Xc: Compensation reactance (droop or line-drop) (pu)
      0
      # vcompFlag: 1: regulate lvertbar v_conrvert (line-drop compensation); 0: regulate v_t + K_c Q_branch (droop)
      0
      # Kc: Reactive droop gain (used when vcompFlag = 0) (pu/pu)
      0
      # Tfltr: Voltage and Q measurement filter; also the REGC_A voltage filter and the PLL input filter (s)
      0.02
      # RefFlag: 1: voltage control; 0: reactive power control
      1
      # dbd: Deadband on the V/Q error, symmetric, geq 0 (pu)
      0
      # emax: Upper limit on the V/Q error (pu)
      0.1
      # emin: Lower limit on the V/Q error (pu)
      -0.1
      # Kp: V/Q PI proportional gain (pu/pu)
      18
      # Ki: V/Q PI integral gain (pu/(pu·s))
      5
      # Qmax: Upper limit of the V/Q PI (pu)
      0.44
      # Qmin: Lower limit of the V/Q PI (pu)
      -0.44
      # Tft: Lead time constant (s)
      0
      # Tfv: Lag time constant; below 0.005 the lead-lag is bypassed (s)
      0.05
      # vfrz: Voltage below which the V/Q integrator is frozen (pu)
      0.7
      # Tp: Filter on P_branch and on the power-factor reference (s)
      0.05
      # fdbd1: Frequency deadband, lower edge, leq 0 (pu)
      -0.0006
      # fdbd2: Frequency deadband, upper edge, geq 0 (pu)
      0.0006
      # Ddn: Droop for over-frequency (pu/pu)
      20
      # Dup: Droop for under-frequency (pu/pu)
      0
      # femax: Upper limit on the power error (pu)
      999
      # femin: Lower limit on the power error (pu)
      -999
      # kpg: Power PI proportional gain (pu/pu)
      0.05
      # kig: Power PI integral gain (pu/(pu·s))
      0.1
      # Pmax: Upper limit of the power PI (pu)
      1
      # Pmin: Lower limit of the power PI (pu)
      0
      # Tlag: Lag on the plant power output (s)
      0.1
      # FreqFlag: 1: plant power loop sets P_refo; 0: P_refo held at its initial value
      0
      # Tmesf: Frequency measurement time constant, raised to 0.05 if smaller (s)
      0.02
      # QextFlag: 1: plant V/Q loop sets Q_ext; 0: Q_ext held at its initial value
      0
      # Ht: Turbine inertia (s)
      3.395
      # Hg: Generator inertia (s)
      0.962
      # wo: Initial generator speed, the reference of Deltaomega_g (pu)
      1
      # Dshaft: Shaft damping (pu/pu)
      2.344
      # Kshaft: Shaft stiffness, per pu·s of twist (pu)
      1.387
      # vdip: Voltage below which a dip is declared (pu)
      0.9
      # vup: Voltage above which a dip is declared (pu)
      1.1
      # Trv: Terminal voltage filter (s)
      0.02
      # vref0: Reference for the dip injection; used as given, so 0 is not replaced by the initial voltage (pu)
      1
      # vref1: Bias added to Q_r when vFlag = 0 (pu)
      1
      # dbd1: Dip injection deadband, lower edge, leq 0 (pu)
      -0.05
      # dbd2: Dip injection deadband, upper edge, geq 0 (pu)
      0.05
      # kqv: Dip reactive current gain (pu/pu)
      2
      # Iqh1: Upper limit of the dip injection (pu)
      1.05
      # Iql1: Lower limit of the dip injection (pu)
      -1.05
      # qmax: Upper limit of the reactive power reference (pu)
      0.44
      # qmin: Lower limit of the reactive power reference (pu)
      -0.44
      # vmax: Upper limit of V_ref and of the Q PI (pu)
      1.1
      # vmin: Lower limit of V_ref and of the Q PI (pu)
      0.9
      # kqp: Q PI proportional gain (pu/pu)
      0
      # kqi: Q PI integral gain (pu/(pu·s))
      0.1
      # kvp: V PI proportional gain (pu/pu)
      0
      # kvi: V PI integral gain (pu/(pu·s))
      40
      # Tiq: Reactive current lag (QFlag = 0) (s)
      0.02
      # vq1: VDL1, voltage of point 1 (pu)
      0.2
      # Iq1: VDL1, reactive current limit at point 1 (pu)
      1
      # vq2: VDL1, point 2 (pu)
      0.4
      # Iq2:  (pu)
      1
      # vq3: VDL1, point 3 (pu)
      0.8
      # Iq3:  (pu)
      1
      # vq4: VDL1, point 4 (pu)
      1
      # Iq4:  (pu)
      1
      # vp1: VDL2, voltage of point 1 (pu)
      0.2
      # Ip1: VDL2, active current limit at point 1 (pu)
      1
      # vp2: VDL2, point 2 (pu)
      0.4
      # Ip2:  (pu)
      1
      # vp3: VDL2, point 3 (pu)
      0.8
      # Ip3:  (pu)
      1
      # vp4: VDL2, point 4 (pu)
      1
      # Ip4:  (pu)
      1
      # dPmax: Upper rate limit of P_ref (pu/s)
      999
      # dPmin: Lower rate limit of P_ref (pu/s)
      -999
      # pmax: Upper limit of the power order Pord (pu)
      1
      # pmin: Lower limit of the power order Pord (pu)
      0
      # Tpord: Power order lag (s)
      0.02
      # Imax: Converter current limit (pu)
      1.11
      # Thld: Post-dip hold of the reactive injection; its sign selects the mode (s)
      0
      # Thld2: Post-dip hold of I_pmax (s)
      0
      # Iqfrz: Reactive injection held after a dip when Thld > 0 (pu)
      0
      # PFFlag: 1: constant power factor; 0: reactive power reference Q_ext
      0
      # vFlag: 1: V_ref from the Q PI; 0: V_ref = Q_r + v_ref1
      0
      # QFlag: 1: reactive current from the voltage PI; 0: from Q_r/v_t
      0
      # PQFlag: 1: active current priority; 0: reactive current priority
      0
      # PFlag: 1: power order is P_ref,omega_g; 0: power order is P_ref
      1
      # Iqrmax: Reactive current rate limit, used when Q_0 > 0 (pu/s)
      999
      # Iqrmin: Reactive current rate limit, used when Q_0 < 0 (pu/s)
      -999
      # Tg: Converter current lag (s)
      0.02
      # vtmax: High-voltage threshold (WECC Volim) (pu)
      1.2
      # accel: High-voltage reactive current gain (WECC Khv) (pu/pu)
      0.7
      # QMIN: Lower limit of the converter reactive output after the high-voltage reduction (pu)
      -1.3
      # lvpnt0: Active current is zero below this voltage (pu)
      0.4
      # lvpnt1: Active current is unreduced above this voltage (pu)
      0.8
      # Brkpt: Low-voltage power logic breakpoint (pu)
      0.9
      # zerox: Low-voltage power logic zero crossing (pu)
      0.4
      # Lvpl1: Low-voltage power logic limit at Brkpt (pu)
      1.22
      # Lvplsw: 1: low-voltage power logic on; 0: off
      0
      # rrpwr: Active current rise rate limit (pu/s)
      10
      # vPLL: Voltage below which the PLL angle is frozen (pu)
      0.2
      # kpPLL: PLL proportional gain (rad/s/pu)
      3
      # kiPLL: PLL integral gain (rad/s²/pu)
      30
      # wrefPLL: PLL frequency offset; cancels, no effect on the response
      1
;
```

</details>

:::note
With this record, as with the WT3 one, RAMSES reports `INJECTORS NOT IN STEADY STATE` at initialization. The residuals are on the Q and V PI controllers of REEC_A, which `QFlag` = 0 takes out of the loop, and whose initial values the model does not yet set consistently; one of their limiters also toggles during the first time step.
:::

---

## BESS (`inj_BESS`): Battery Energy Storage System

The data-file model name is `BESS` (or `inj_BESS`).

### Description

A comprehensive BESS model implementing the full WECC framework (REPC_A + REEC_C + REGC_A) plus battery state of charge (SOC) tracking. The model supports both grid-following operation (bidirectional active power dispatch) and reactive power / voltage regulation. It is built on the same REPC_A plant controller as the wind turbine models, and uses the REEC_C converter electrical controller which handles a piecewise-linear $I_q$-vs-$V$ and $I_p$-vs-$V$ characteristic for fault ride-through.

The battery SOC evolves through integration of injected power:

$$\frac{d\mathrm{SOC}}{dt} = -\frac{P_{\mathrm{bess}}}{C_{\mathrm{bat}} \cdot S_{\mathrm{nom}}}$$

with hard clamps at `SOCmin` and `SOCmax` that modify the active power limits `Pmax`/`Pmin` dynamically:

$$P_{\max} = \begin{cases} 0 & \mathrm{SOC} \ge \mathrm{SOC}_{\max}\\ P_{\max,\mathrm{rated}} & \text{otherwise}\end{cases}$$

$$P_{\min} = \begin{cases} 0 & \mathrm{SOC} \le \mathrm{SOC}_{\min}\\ P_{\min,\mathrm{rated}} & \text{otherwise}\end{cases}$$

<img src="/images/models/inj-bess-light.svg"
     alt="Battery energy storage block diagram. The active power and voltage references pass the REPC_A plant controller, the REEC_C converter electrical controller with its piecewise current-versus-voltage characteristics, and the REGC_A generator interface, which injects ix and iy. The injected power is integrated into the state of charge, whose clamps at SOCmin and SOCmax drive the active power limits Pmax and Pmin of the converter controller to zero."
     class="dark:sl-hidden" />
<img src="/images/models/inj-bess-dark.svg"
     alt="Battery energy storage block diagram. The active power and voltage references pass the REPC_A plant controller, the REEC_C converter electrical controller with its piecewise current-versus-voltage characteristics, and the REGC_A generator interface, which injects ix and iy. The injected power is integrated into the state of charge, whose clamps at SOCmin and SOCmax drive the active power limits Pmax and Pmin of the converter controller to zero."
     class="light:sl-hidden" />

### Parameters (key parameters)

| # | Name | Sub-model | Description | Unit |
|---|------|-----------|-------------|------|
| 1 | `SNOM` | | Nominal power | MW |
| 2–32 | | REPC_A | Plant controller (same as WT3/WT4) | various |
| 33–76 | | REEC_C | Electrical controller with piecewise $I_q(V)$, $I_p(V)$ | various |
| 68 | `CapBat` | BESS | Battery energy capacity | MWh |
| 69 | `SOCini` | BESS | Initial state of charge | pu |
| 70 | `SOCmax` | BESS | Maximum SOC limit | pu |
| 71 | `SOCmin` | BESS | Minimum SOC limit | pu |
| 72–73 | `dPmax`, `dPmin` | BESS | Active power ramp rate limits | pu/s |
| 74–75 | `pmax`, `pmin` | REEC_C | Active current limits (pu on SNOM) | pu |
| 76 | `Tpord` | REEC_C | Active power order time constant | s |

Full parameter listing has approximately 125 parameters; refer to a working example data file for the complete ordering.

### State Variables

The BESS model uses over 40 internal states reflecting the three sub-models. Key states include:

| Variable | Description |
|----------|-------------|
| `SOC` | State of charge | pu |
| `Pref` | Active power reference | pu |
| `Qext` | Reactive power reference from REPC_A | pu |
| `Ip`, `Iq` | Active/reactive current outputs | pu |
| `PLLPhaseAngle` | PLL phase angle | rad |
| `Pgen`, `Qgen` | Generated powers | pu |

### Usage Example

<details>
<summary>Show the data record</summary>

```
INJEC  BESS  BESS1  BUS_ST
      # FP FQ P Q: share of the power-flow injection (FP, FQ) or initial power (P in MW, Q in Mvar)
      1.  1.  0.  0.
      # SNOM: Rating, base of every per-unit quantity in the model (MVA)
      100.
      # Rc: Compensation resistance (pu)
      0
      # Xc: Compensation reactance (droop or line-drop) (pu)
      0
      # vcompFlag: 1: regulate lvertbar v_conrvert (line-drop compensation); 0: regulate v_t + K_c Q_branch (droop)
      0
      # Kc: Reactive droop gain (used when vcompFlag = 0) (pu/pu)
      0
      # Tfltr: Voltage and Q measurement filter; also the REGC_A voltage filter and the PLL input filter (s)
      0.02
      # RefFlag: 1: voltage control; 0: reactive power control
      1
      # dbd: Deadband on the V/Q error, symmetric, geq 0 (pu)
      0
      # emax: Upper limit on the V/Q error (pu)
      0.1
      # emin: Lower limit on the V/Q error (pu)
      -0.1
      # Kp: V/Q PI proportional gain (pu/pu)
      18
      # Ki: V/Q PI integral gain (pu/(pu·s))
      5
      # Qmax: Upper limit of the V/Q PI (pu)
      0.44
      # Qmin: Lower limit of the V/Q PI (pu)
      -0.44
      # Tft: Lead time constant (s)
      0
      # Tfv: Lag time constant; below 0.005 the lead-lag is bypassed (s)
      0.05
      # vfrz: Voltage below which the V/Q integrator is frozen (pu)
      0.7
      # Tp: Filter on P_branch and on the power-factor reference (s)
      0.05
      # fdbd1: Frequency deadband, lower edge, leq 0 (pu)
      -0.0006
      # fdbd2: Frequency deadband, upper edge, geq 0 (pu)
      0.0006
      # Ddn: Droop for over-frequency (pu/pu)
      20
      # Dup: Droop for under-frequency (pu/pu)
      0
      # femax: Upper limit on the power error (pu)
      999
      # femin: Lower limit on the power error (pu)
      -999
      # kpg: Power PI proportional gain (pu/pu)
      0.05
      # kig: Power PI integral gain (pu/(pu·s))
      0.1
      # Pmax: Upper limit of the power PI (pu)
      1
      # Pmin: Lower limit of the power PI (pu)
      -1
      # Tlag: Lag on the plant power output (s)
      0.1
      # FreqFlag: 1: plant power loop sets P_refo; 0: P_refo held at its initial value
      0
      # Tmesf: Frequency measurement time constant, raised to 0.05 if smaller (s)
      0.02
      # QextFlag: 1: plant V/Q loop sets Q_ext; 0: Q_ext held at its initial value
      0
      # vdip: Voltage below which a dip is declared (pu)
      0.9
      # vup: Voltage above which a dip is declared (pu)
      1.1
      # Trv: Terminal voltage filter (s)
      0.02
      # vref0: Reference for the dip injection; used as given, so 0 is not replaced by the initial voltage (pu)
      1
      # dbd1: Dip injection deadband, lower edge, leq 0 (pu)
      -0.05
      # dbd2: Dip injection deadband, upper edge, geq 0 (pu)
      0.05
      # kqv: Dip reactive current gain (pu/pu)
      2
      # Iqh1: Upper limit of the dip injection (pu)
      1.05
      # Iql1: Lower limit of the dip injection (pu)
      -1.05
      # qmax: Upper limit of the reactive power reference (pu)
      0.44
      # qmin: Lower limit of the reactive power reference (pu)
      -0.44
      # vmax: Upper limit of V_ref and of the Q PI (pu)
      1.1
      # vmin: Lower limit of V_ref and of the Q PI (pu)
      0.9
      # kqp: Q PI proportional gain (pu/pu)
      0
      # kqi: Q PI integral gain (pu/(pu·s))
      0.1
      # kvp: V PI proportional gain (pu/pu)
      0
      # kvi: V PI integral gain (pu/(pu·s))
      40
      # Tiq: Reactive current lag (QFlag = 0) (s)
      0.02
      # vq1: VDL1, voltage of point 1 (pu)
      0.2
      # Iq1: VDL1, reactive current limit at point 1 (pu)
      1
      # vq2: VDL1, point 2 (pu)
      0.4
      # Iq2:  (pu)
      1
      # vq3: VDL1, point 3 (pu)
      0.8
      # Iq3:  (pu)
      1
      # vq4: VDL1, point 4 (pu)
      1
      # Iq4:  (pu)
      1
      # vp1: VDL2, voltage of point 1 (pu)
      0.2
      # Ip1: VDL2, active current limit at point 1 (pu)
      1
      # vp2: VDL2, point 2 (pu)
      0.4
      # Ip2:  (pu)
      1
      # vp3: VDL2, point 3 (pu)
      0.8
      # Ip3:  (pu)
      1
      # vp4: VDL2, point 4 (pu)
      1
      # Ip4:  (pu)
      1
      # Paux: Constant added to the active current command after dividing Pord by voltage (Ipcmd = Pord/V + Paux), on SNOM base (pu)
      0.
      # CapBat: Battery energy capacity (MWh)
      100.
      # SOCini: Initial state of charge as a fraction of CapBat; must lie strictly between SOCmin and SOCmax (pu)
      0.5
      # SOCmax: Upper SOC limit; at it the battery is full and charging current is blocked (Ipmin = 0) (pu)
      0.9
      # SOCmin: Lower SOC limit; at it the battery is empty and discharging current is blocked (Ipmax = 0) (pu)
      0.1
      # dPmax: Upper rate limit of P_ref (pu/s)
      999
      # dPmin: Lower rate limit of P_ref (pu/s)
      -999
      # pmax: Upper limit of the power order Pord (pu)
      1
      # pmin: Lower limit of the power order Pord (pu)
      -1
      # Tpord: Active power order time constant (s)
      0.02
      # Imax: Converter current limit (pu)
      1.11
      # PFFlag: 1: constant power factor; 0: reactive power reference Q_ext
      0
      # vFlag: 1: V_ref from the Q PI; 0: V_ref = Q_r + v_ref1
      0
      # QFlag: 1: reactive current from the voltage PI; 0: from Q_r/v_t
      0
      # PQFlag: 1: active current priority; 0: reactive current priority
      0
      # Iqrmax: Reactive current rate limit, used when Q_0 > 0 (pu/s)
      999
      # Iqrmin: Reactive current rate limit, used when Q_0 < 0 (pu/s)
      -999
      # Tg: Converter current lag (s)
      0.02
      # vtmax: High-voltage threshold (WECC Volim) (pu)
      1.2
      # accel: High-voltage reactive current gain (WECC Khv) (pu/pu)
      0.7
      # QMIN: Lower limit of the converter reactive output after the high-voltage reduction (pu)
      -1.3
      # lvpnt0: Active current is zero below this voltage (pu)
      0.4
      # lvpnt1: Active current is unreduced above this voltage (pu)
      0.8
      # Brkpt: Low-voltage power logic breakpoint (pu)
      0.9
      # zerox: Low-voltage power logic zero crossing (pu)
      0.4
      # Lvpl1: Low-voltage power logic limit at Brkpt (pu)
      1.22
      # Lvplsw: 1: low-voltage power logic on; 0: off
      0
      # rrpwr: Active current rise rate limit (pu/s)
      10
      # vPLL: Voltage below which the PLL angle is frozen (pu)
      0.2
      # kpPLL: PLL proportional gain (rad/s/pu)
      3
      # kiPLL: PLL integral gain (rad/s²/pu)
      30
      # wrefPLL: PLL frequency offset; cancels, no effect on the response
      1
;
```

</details>
