---
title: Video Tutorials
description: A ten-episode video series covering STEPSS from installation to a voltage-collapse study on the Nordic system.
---

Ten episodes, in order, from a clean machine to a full study. Each one is ten to
fourteen minutes and is recorded against the current release, so what you see on
screen is what you get when you install it.

Every episode is also embedded on the page that owns its subject, so you can
watch the relevant one where you are reading.

:::note[About the narration]
Narration uses a synthetic voice.
:::

## 1. Installation and Setup

Install on Ubuntu, Windows and macOS, add the Python package, and finish with a
running application and a working import. What the engines are, how the desktop
and Python editions relate, and what the licence permits. See
[Installation](/getting-started/installation/).

<div class="video-embed"><iframe src="https://www.youtube-nocookie.com/embed/flSGsaKt7sU" title="STEPSS Episode 1: Installation and Setup" loading="lazy" allowfullscreen allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"></iframe></div>

## 2. Your First Power Flow and Dynamic Simulation

The six tabs in order on the bundled five-bus case: solve the power flow with
Helios, run the dynamic simulation with RAMSES, and open the saved trajectory.
See [Quick Start](/getting-started/quickstart/).

<div class="video-embed"><iframe src="https://www.youtube-nocookie.com/embed/tnsV2fuzOK8" title="STEPSS Episode 2: Your First Power Flow and Dynamic Simulation" loading="lazy" allowfullscreen allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"></iframe></div>

## 3. Helios in Depth

Helios through the Python session and the interface: the records it reads,
contingency and limit screening, the annotated one-line diagram, LFRESV output,
and how to tell a solved case from one that only produced numbers. See
[Power Flow](/user-guide/power-flow/).

<div class="video-embed"><iframe src="https://www.youtube-nocookie.com/embed/4ggqi35HkCI" title="STEPSS Episode 3: Helios in Depth" loading="lazy" allowfullscreen allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"></iframe></div>

## 4. Solvers, Tolerances and Parallelism

Solver settings separated into the ones that control accuracy and the ones that
save work, then parallel execution set realistically within the two-core limit
of the free licence. See [Solver Settings](/user-guide/solver-settings/).

<div class="video-embed"><iframe src="https://www.youtube-nocookie.com/embed/AkI3k0xcRuQ" title="STEPSS Episode 4: Solvers, Tolerances and Parallelism" loading="lazy" allowfullscreen allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"></iframe></div>

## 5. Observables, Trajectories and Plotting

The difference between watching a run live and recording it to file, what each
trace file holds and when you would open it, then extracting curves from a saved
trajectory. See [Running a Simulation](/gui/running/).

<div class="video-embed"><iframe src="https://www.youtube-nocookie.com/embed/2-oAjjBQnqY" title="STEPSS Episode 5: Observables, Trajectories and Plotting" loading="lazy" allowfullscreen allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"></iframe></div>

## 6. Writing Your Own Model with CODEGEN

An excitation controller read block by block in CODEGEN Studio, exported as a
model description, and compiled into a simulator of your own from the Codegen
tab. See [User-Defined Models](/developer/user-models/).

<div class="video-embed"><iframe src="https://www.youtube-nocookie.com/embed/7vs1fXFxm38" title="STEPSS Episode 6: Writing Your Own Model with CODEGEN" loading="lazy" allowfullscreen allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"></iframe></div>

## 7. Small Signal Stability and Eigenanalysis

RAMSES computes the eigenanalysis itself at a chosen operating point. Reading
the modes, the participation factors and the mode shapes, the live filters in
the results window, and a second case whose inter-area mode is unstable. See
[Eigenanalysis](/user-guide/eigenanalysis/).

<div class="video-embed"><iframe src="https://www.youtube-nocookie.com/embed/boL3wMKNC50" title="STEPSS Episode 7: Small Signal Stability and Eigenanalysis" loading="lazy" allowfullscreen allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"></iframe></div>

## 8. Scripting STEPSS in Python

A complete study in a notebook: the Kundur inter-area comparison, run twice with
one parameter changed, from the case files to the conclusion. See the
[Python API](/python/).

<div class="video-embed"><iframe src="https://www.youtube-nocookie.com/embed/Wk7kIkVsCWQ" title="STEPSS Episode 8: Scripting STEPSS in Python" loading="lazy" allowfullscreen allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"></iframe></div>

## 9. Inter-area Oscillations on Kundur Two-Area

The same study as episode 8, through the interface instead of a notebook, with
the eigenanalysis the notebook route cannot do. Watching the two routes side by
side is how you learn which one a given job wants. See the
[Kundur Two-Area System](/test-systems/kundur/).

<div class="video-embed"><iframe src="https://www.youtube-nocookie.com/embed/oqHgJd-A4cw" title="STEPSS Episode 9: Inter-area Oscillations on Kundur Two-Area" loading="lazy" allowfullscreen allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"></iframe></div>

## 10. Capstone: Voltage Collapse on the Nordic System

Everything in one notebook: Helios solves and stresses an operating point,
exports it, RAMSES trips a generator from it, and the extractor turns the result
into the curves that answer the question. See the
[Nordic Test System](/test-systems/nordic/).

<div class="video-embed"><iframe src="https://www.youtube-nocookie.com/embed/7vRwOjdbuIo" title="STEPSS Episode 10: Capstone: Voltage Collapse on the Nordic System" loading="lazy" allowfullscreen allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"></iframe></div>
