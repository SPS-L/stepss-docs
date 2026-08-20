#!/usr/bin/env python3
"""Renders the figures the Python API pages show, light and dark.

Every figure here is the literal output of a call the documentation prints:
cur.plot, stepss.curplot and stepss.monitor. Nothing is drawn by hand, so a
figure cannot drift from the API that produced it.

The two themes come from a matplotlib style applied around the same call, so
the pair is the same plot on two backgrounds rather than two different plots.
"""

import os
import pathlib
import shutil
import sys

os.environ.setdefault("MPLCONFIGDIR", str(pathlib.Path(
    os.environ.get("TMPDIR", "/tmp")) / "stepss-shots" / "mpl"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import stepss

WORK = pathlib.Path(os.environ.get(
    "SHOT_WORK", pathlib.Path(os.environ.get("TMPDIR", "/tmp")) / "stepss-shots"))
OUT = WORK / "shots" / "python"
EX = pathlib.Path.home() / "stepss-examples"
RUNROOT = WORK / "pyrun"

OUT.mkdir(parents=True, exist_ok=True)

# Starlight's own surfaces, so a figure sits on the page rather than on it.
LIGHT = {"figure.facecolor": "#ffffff", "axes.facecolor": "#ffffff",
         "text.color": "#23262f", "axes.labelcolor": "#23262f",
         "axes.edgecolor": "#c2c8d4", "xtick.color": "#4b5162",
         "ytick.color": "#4b5162", "grid.color": "#e3e6ee",
         "legend.facecolor": "#ffffff", "legend.edgecolor": "#c2c8d4"}
DARK = {"figure.facecolor": "#16181d", "axes.facecolor": "#16181d",
        "text.color": "#e5e7eb", "axes.labelcolor": "#e5e7eb",
        "axes.edgecolor": "#464c58", "xtick.color": "#b8bdc9",
        "ytick.color": "#b8bdc9", "grid.color": "#2b2f38",
        "legend.facecolor": "#16181d", "legend.edgecolor": "#464c58"}
COMMON = {"figure.figsize": (8.0, 4.5), "figure.dpi": 130,
          "savefig.dpi": 130, "font.size": 11, "axes.grid": True,
          "grid.linewidth": 0.6, "lines.linewidth": 1.4,
          "legend.framealpha": 1.0}


def workdir(name):
    """A clean copy of an example, so a run never reads a previous one's output."""
    src = EX / name
    if not src.is_dir():
        raise SystemExit(
            f"{src} not found. These figures run the bundled examples, which the\n"
            f"application unpacks: open {name} once from File > Open Examples\n"
            f"with the examples directory set to {EX}, or unzip\n"
            f"my/stepss/payload/example-*.zip out of the installed stepss.jar into it."
        )
    d = RUNROOT / name
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(src, d)
    os.chdir(d)
    return d


def save(theme, name):
    plt.savefig(OUT / f"{name}-{theme}.png", bbox_inches="tight",
                facecolor=plt.rcParams["figure.facecolor"])
    plt.close("all")
    print(f"  {name}-{theme}.png")


def figure(theme, name, draw):
    """Draw one figure under one theme. `draw` makes the plot and nothing else."""
    plt.close("all")
    with plt.rc_context({**COMMON, **(DARK if theme == "dark" else LIGHT)}):
        draw()
        save(theme, name)


# ---------------------------------------------------------------- the runs
def run_kundur():
    """The same case and the same disturbance as every GUI figure."""
    workdir("kundur-two-area")
    case = stepss.cfg()
    case.addData("lf.dat")
    case.addData("dyn.dat")
    case.addData("solveroptions.dat")
    case.addDst("disturb.dst")
    case.addObs("obs.dat")
    case.addTrj("output.trj")

    ram = stepss.sim()
    ram.execSim(case)
    return stepss.extractor(case.getTrj())


def run_five_bus():
    """The exciter set-point step the Python examples page prints."""
    workdir("five-bus")
    case = stepss.cfg()
    case.addData("dyn.dat")
    case.addData("lf1solv.dat")
    case.addData("solveroptions.dat")
    case.addDst("nothing.dst")
    case.addObs("obs.dat")
    case.addTrj("output.trj")

    ram = stepss.sim()
    ram.execSim(case, 0.0)
    ram.addDisturb(1.0, "CHGPRM EXC G Vo 0.05 2")
    ram.contSim(60.0)
    ram.endSim()
    return stepss.extractor(case.getTrj())


def run_monitor(theme):
    """The live monitor, driven exactly as the Live Plotting section shows."""
    workdir("kundur-two-area")
    case = stepss.cfg()
    case.addData("lf.dat")
    case.addData("dyn.dat")
    case.addData("solveroptions.dat")
    case.addDst("disturb.dst")
    case.addObs("obs.dat")
    case.addTrj("output.trj")

    ram = stepss.sim()
    ram.execSim(case, 0.0)
    with plt.rc_context({**COMMON, "figure.figsize": (8.0, 6.0),
                         **(DARK if theme == "dark" else LIGHT)}):
        mon = stepss.monitor(ram, [
            "MS G1",
            "BV 9",
            "BPO 7-8#1",
            "RT RT",
        ], title="Kundur two-area", refresh=0.5)
        mon.run(step=1.0, until=60.0)
        mon.savefig(str(OUT / f"py-monitor-{theme}.png"),
                    bbox_inches="tight",
                    facecolor=plt.rcParams["figure.facecolor"])
        print(f"  py-monitor-{theme}.png")
    ram.endSim()
    plt.close("all")


def main():
    ext = run_kundur()

    for theme in ("light", "dark"):
        # cur.plot() - one curve
        figure(theme, "py-plot-single",
               lambda: ext.getSync("G1").P.plot())
        # stepss.curplot() - several curves on one axes. Active power rather
        # than speed: on this case the four speeds sit within 6e-4 pu of each
        # other and the figure reads as a single line.
        figure(theme, "py-plot-multi", lambda: (
            stepss.curplot([ext.getSync(f"G{i}").P for i in range(1, 5)]),
            # curplot asks for loc='best'; four long labels leave nowhere
            # inside the axes that does not cover a curve or a tick label
            plt.legend(loc="upper center", bbox_to_anchor=(0.5, -0.16),
                       ncol=2, fontsize=9, frameon=False)))
        # a bus voltage, the other quantity the examples plot
        figure(theme, "py-plot-bus",
               lambda: ext.getBus("9").mag.plot())

    ext5 = run_five_bus()
    for theme in ("light", "dark"):
        figure(theme, "py-five-bus-exciter", lambda: (
            stepss.curplot([ext5.getSync("G").P, ext5.getSync("G").Q]),
            # curplot asks for loc='best', which lands on the data here
            plt.legend(loc="center right", ncol=1)))

    for theme in ("light", "dark"):
        run_monitor(theme)


if __name__ == "__main__":
    sys.exit(main())
