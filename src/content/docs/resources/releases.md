---
title: Releases
description: How STEPSS is versioned, where releases are published, and how to find the version you are running
---

## Where releases are published

Every STEPSS release is published on GitHub, with its changelog and its
installers:

**[github.com/SPS-L/stepss-java-ui/releases](https://github.com/SPS-L/stepss-java-ui/releases)**

This site does not mirror that changelog. Releases are frequent and the notes are
generated with them, so a copy here would be behind within the week. Read them at
the source, or from inside the application: **Help**, then **Changelog** (`F2`).

## What the version number means

A STEPSS version identifies a **tested combination of components**, not the
history of any one of them. The engines version independently and on their own
cadences, and each STEPSS release pins one release of each: RAMSES, Helios,
CODEGEN, DYNGRAPH and URAMSES, plus the three bundled
[test systems](/test-systems/). Those pins live in `versions.properties` in
[stepss-java-ui](https://github.com/SPS-L/stepss-java-ui).

So the engine version you see at work is not the STEPSS version. The status bar
naming `RAMSES 3.74` inside a STEPSS 3.74.15 is correct, not a mismatch.

`stepss`, the Python package, is versioned on the engine line rather than the
application's patch level, so its number tracks the engines it carries.

## Finding the version you have

| Where | How |
|---|---|
| STEPSS GUI | **Help**, then **About** (`F4`) |
| `stepss` | `python -c "import stepss; print(stepss.__version__)"` |
| The engine directly | `ramses -v` |

The GUI also checks for new releases on startup, and **Help**, then **Check for
updates** (`F3`) asks immediately. Whether it checks at startup is a setting in
the **Tools** menu.

## The four ways to get it

Each is set up on the [Installation](/getting-started/installation/) page; this is
only a map of what exists.

| Channel | Gets you | Updates |
|---|---|---|
| Platform installer | STEPSS GUI with its own Java | Download the new one |
| `stepss.jar` | STEPSS GUI, needing a Java you supply | Download the new one |
| APT repository | STEPSS GUI, on Debian and Ubuntu | `apt upgrade`, with the rest of the system |
| Scoop bucket | STEPSS GUI, on Windows | `scoop update stepss` |
| PyPI | STEPSS in Python | `pip install --upgrade stepss` |

The package-manager routes track the same releases as the installers, so which one
you use is a question of how you prefer to update, not of what you get.

## Which version this site documents

The **current release**. Where a feature does not exist in every release, the page
documenting it states the version it arrived in, so a reader on an older build is
not left following instructions their binary cannot satisfy. There is no archive of
documentation for superseded versions.

## See Also

- [Installation](/getting-started/installation/), setting up any of the channels above
- [Repositories](/resources/repositories/), the source for every component
- [License](/getting-started/license/), the terms each component is released under
