---
title: Discrete Controller Models
description: Protection, tap changer, and discrete control models in RAMSES
---

Discrete controllers (DCTL) in RAMSES implement **event-driven logic** rather than continuous differential equations. They fire at specific simulation events (voltage crossing a threshold, a timer expiring, a tap position changing) and execute discrete actions such as tripping a generator, shedding load, or adjusting a transformer tap. They run inside RAMSES' event-driven loop and can call `disp_disc` to log switching actions.

The RAMSES data keyword is `DCTL`:

```
DCTL  model_name  controller_name  field1  field2  ... ;
```

:::note[Usage in Dynamic Data Files]
Discrete controllers are defined with the `DCTL` keyword as standalone records in the dynamic data file. The syntax is:

```
DCTL model_name ctl_name param1 param2 ... ;
```

Where `model_name` is the controller type, `ctl_name` is a unique instance name, and the remaining parameters are model-specific.

Recognised discrete-controller model names (case-sensitive):

- **Uppercase short names** (no prefix): `PST`, `LTC`, `LTC2`, `OLTC2`, `LTCINV`, `MAIS`, `UVLS`, `RT`, `UVPROT`, `FRT`, `VOLT_VAR`, `SIM_MINMAXVOLT`, `SIM_MINMAXSPEED`.
- **Prefixed name**: RAMSES adds the `dctl_` prefix automatically, so both `line_prot` and `dctl_line_prot` resolve to the line-protection model.

All of the above are built into every RAMSES distribution (standalone executable and shared library used by stepss). `MAIS` is an automatic shunt-reactor switching scheme (*Manoeuvre Automatique d'Inductances Shunt*) that switches susceptance at a monitored bus on under-voltage, voltage-drop and over-voltage thresholds; it does not have a dedicated documentation section below. `HVDC_LIM`, `injprot` and `LOSPROT`, documented below, have been callable since 3.79; before that they were compiled under no name.
:::

## Model Families

The controllers are documented by family, one page each.

| Page | Models |
|------|--------|
| [Tap Changers](/models/discrete-controllers/tap-changers/) | [`LTC`](/models/discrete-controllers/tap-changers/#ltc-dctl_ltc-load-tap-changer-standard), [`LTC2`](/models/discrete-controllers/tap-changers/#ltc2-dctl_ltc2-load-tap-changer-variant-2), [`LTCINV`](/models/discrete-controllers/tap-changers/#ltcinv-dctl_ltcinv-inverse-time-load-tap-changer), [`OLTC2`](/models/discrete-controllers/tap-changers/#oltc2-dctl_oltc2-on-load-tap-changer-type-2) |
| [Protection and Control](/models/discrete-controllers/protection/) | [`UVPROT`](/models/discrete-controllers/protection/#uvprot-dctl_uvprot-under-voltage-protection-relay), [`UVLS`](/models/discrete-controllers/protection/#uvls-dctl_uvls-under-voltage-load-shedding), [`FRT`](/models/discrete-controllers/protection/#frt-dctl_frt-fault-ride-through-controller), [`dctl_injprot`](/models/discrete-controllers/protection/#dctl_injprot-injector-protection), [`dctl_losprot`](/models/discrete-controllers/protection/#dctl_losprot-loss-of-synchronism-protection), [`line_prot`](/models/discrete-controllers/protection/#line_prot-dctl_line_prot-line-overcurrent-protection), [`PST`](/models/discrete-controllers/protection/#pst-dctl_pst-phase-shifting-transformer-control), [`RT`](/models/discrete-controllers/protection/#rt-dctl_rt-real-time-simulation-control), [`dctl_hvdc_lim`](/models/discrete-controllers/protection/#dctl_hvdc_lim-hvdc-lcc-limitercontroller) |
| [Monitoring](/models/discrete-controllers/monitoring/) | [`SIM_MINMAXSPEED`](/models/discrete-controllers/monitoring/#sim_minmaxspeed-dctl_sim_minmaxspeed-speed-monitoring-minmax), [`SIM_MINMAXVOLT`](/models/discrete-controllers/monitoring/#sim_minmaxvolt-dctl_sim_minmaxvolt-voltage-monitoring-minmax), [`VOLT_VAR`](/models/discrete-controllers/monitoring/#volt_var-dctl_voltage_variability-voltage-variability-monitor) |
