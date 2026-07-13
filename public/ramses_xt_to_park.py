"""
ramses_xt_to_park.py

Standalone port of the XT branch of get_sync_mach() from the RAMSES source
file sync.f90 (SPS-Lab). Converts synchronous machine characteristic
reactances and open-circuit time constants (the "XT" input format) into the
Park model inductances and resistances (the "RL" input format), in per unit.

Faithful to the source on the details that break hand calculations:
  * open-circuit time constants are normalised by tb = 1/(2*pi*fnom)
  * the two-circuit axes solve a quadratic for TF/TD1 (TQ1/TQ2)
  * RF is recovered as -RD1/(1 - d*RD1), not by algebraic subtraction
  * puf = rf/ibratio ties the field circuit base to IBRATIO
  * a single rotor circuit on an axis is selected by passing None

Reference: SPS-L RAMSES sync.f90 ; Sync_mach_Octave
           https://github.com/SPS-L/Sync_mach_Octave
"""

import math


def ramses_xt_to_park(fnom, ibratio, ll, ra,
                      xd, xpd, xq,
                      tpd0, xsd=None, tsd0=None,
                      xpq=None, tpq0=None, xsq=None, tsq0=None):
    """Convert XT-format data to RL-format Park parameters (all pu).

    Parameters
    ----------
    fnom   : nominal frequency [Hz]
    ibratio: field base current ratio IBRATIO [-]
    ll     : stator leakage reactance XL [pu]
    ra     : armature resistance RA [pu]
    xd,xpd : d-axis synchronous and transient reactance XD, XPD [pu]
    xq     : q-axis synchronous reactance XQ [pu]
    tpd0   : d-axis transient open-circuit time constant TPD0 [s]
    xsd    : d-axis subtransient reactance XSD [pu] or None (single circuit)
    tsd0   : d-axis subtransient open-circuit time constant TSD0 [s] or None
    xpq    : q-axis transient reactance XPQ [pu] or None
    tpq0   : q-axis transient open-circuit time constant TPQ0 [s] or None
    xsq    : q-axis subtransient reactance XSQ [pu] or None
    tsq0   : q-axis subtransient open-circuit time constant TSQ0 [s] or None

    Returns
    -------
    dict with keys:
      ll, ra, mdu, mqu, llf, rf, lld1, rd1, llq1, rq1, llq2, rq2, puf,
      sd1, sq1, sq2  (winding-present flags, as in RAMSES)
    """
    tb = 1.0 / (2.0 * math.pi * fnom)
    out = {"ll": ll, "ra": ra}

    # ---- unsaturated mutuals ----
    mdu = xd - ll
    mqu = xq - ll
    out["mdu"] = mdu
    out["mqu"] = mqu

    # ---------------- d axis ----------------
    tpd0n = tpd0 / tb
    sd1 = 0 if xsd is None else 1
    if sd1 == 0:
        lff = mdu ** 2 / (xd - xpd)
        llf = lff - mdu
        rf = lff / tpd0n
        lld1, rd1 = 1.0, 1.0
    else:
        if xpd >= xd:
            raise ValueError("XPD must be strictly smaller than XD")
        tsd0n = tsd0 / tb
        tpd = tpd0n * xpd / xd
        tsd = (xsd * tpd0n * tsd0n) / (xd * tpd)
        a = (xd * tpd * tsd - ll * tpd0n * tsd0n) / (xd - ll)
        b = (xd * (tpd + tsd) - ll * (tpd0n + tsd0n)) / (xd - ll)
        c = (xd * (tpd0n * tsd0n - tpd * tsd)) / ((xd - ll) ** 2)
        d = (xd * (tpd0n + tsd0n - tpd - tsd)) / ((xd - ll) ** 2)
        tf = (b + math.sqrt(b ** 2 - 4.0 * a)) / 2.0
        td1 = b - tf
        rd1 = (tf - td1) / (c - d * td1)
        rf = -rd1 / (1.0 - d * rd1)
        llf = tf * rf
        lld1 = td1 * rd1
        if min(rd1, rf, llf, lld1) < 0.0:
            print("WARNING: unrealistic Park inductances or resistances in d axis")
    out.update({"sd1": sd1, "llf": llf, "rf": rf, "lld1": lld1, "rd1": rd1})
    out["puf"] = rf / ibratio

    # ---------------- q axis ----------------
    sq1 = 0 if xpq is None else 1
    sq2 = 0 if xsq is None else 1
    if sq1 == 1:
        tpq0n = tpq0 / tb
        if xpq >= xq:
            raise ValueError("XPQ must be strictly smaller than XQ")
        if sq2 == 0:
            lq1q1 = mqu ** 2 / (xq - xpq)
            llq1 = lq1q1 - mqu
            rq1 = lq1q1 / tpq0n
            llq2, rq2 = 1.0, 1.0
        else:
            tsq0n = tsq0 / tb
            tpq = tpq0n * xpq / xq
            tsq = (xsq * tpq0n * tsq0n) / (xq * tpq)
            a = (xq * tpq * tsq - ll * tpq0n * tsq0n) / (xq - ll)
            b = (xq * (tpq + tsq) - ll * (tpq0n + tsq0n)) / (xq - ll)
            c = (xq * (tpq0n * tsq0n - tpq * tsq)) / ((xq - ll) ** 2)
            d = (xq * (tpq0n + tsq0n - tpq - tsq)) / ((xq - ll) ** 2)
            tq1 = (b + math.sqrt(b ** 2 - 4.0 * a)) / 2.0
            tq2 = b - tq1
            rq2 = (tq1 - tq2) / (c - d * tq2)
            rq1 = -rq2 / (1.0 - d * rq2)
            llq1 = tq1 * rq1
            llq2 = tq2 * rq2
            if min(rq1, rq2, llq1, llq2) < 0.0:
                print("WARNING: unrealistic Park inductances or resistances in q axis")
    else:
        llq1, rq1 = 1.0, 1.0
        if sq2 != 0:
            tsq0n = tsq0 / tb
            lq2q2 = mqu ** 2 / (xq - xsq)
            llq2 = lq2q2 - mqu
            rq2 = lq2q2 / tsq0n
        else:
            llq2, rq2 = 1.0, 1.0
    out.update({"sq1": sq1, "sq2": sq2, "llq1": llq1, "rq1": rq1,
                "llq2": llq2, "rq2": rq2})
    return out


if __name__ == "__main__":
    # Round-rotor example (two circuits per axis), 50 Hz, IBRATIO = 1
    p = ramses_xt_to_park(
        fnom=50.0, ibratio=1.0,
        ll=0.15, ra=0.003,
        xd=1.81, xpd=0.30, xsd=0.23, tpd0=8.0, tsd0=0.03,
        xq=1.76, xpq=0.65, xsq=0.25, tpq0=1.0, tsq0=0.07)

    order = ["ll", "mdu", "llf", "lld1", "mqu", "llq1", "llq2",
             "ra", "rf", "rd1", "rq1", "rq2", "puf"]
    print("Park parameters [pu] from XT branch:")
    for k in order:
        print("  {:5s} = {: .6f}".format(k, p[k]))
