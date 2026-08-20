#!/usr/bin/env python3
"""Captures the CODEGEN Studio figures the documentation uses.

Driven with Playwright rather than xdotool: CG Studio loads a model through a
hidden file input, and a native file chooser cannot be filled reliably off an
Xvfb display. Playwright sets the input directly, and its viewport screenshot
is exactly the 1600x913 the existing figures use, with no window chrome to
crop off.

The application has one theme, so these figures have no light/dark pair.
"""

import os
import pathlib
import sys
import time

from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/"
WORK = pathlib.Path(os.environ.get(
    "SHOT_WORK", pathlib.Path(os.environ.get("TMPDIR", "/tmp")) / "stepss-shots"))
OUT = WORK / "shots" / "cgstudio"
EXAMPLES = pathlib.Path(__file__).resolve().parents[2] / "stepss-cg-studio" / "examples"
VIEWPORT = {"width": 1600, "height": 913}

OUT.mkdir(parents=True, exist_ok=True)


def wait_modal(page, overlay="modal-overlay"):
    """The overlay is shown by dropping a class, which Playwright's visibility
    check does not always settle on; poll the class itself instead."""
    page.wait_for_function(
        "id => !document.getElementById(id).classList.contains('hidden')",
        arg=overlay,
        timeout=15000,
    )


def shot(page, name):
    path = OUT / f"{name}.png"
    page.screenshot(path=str(path))
    print(f"  {name}.png")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport=VIEWPORT, device_scale_factor=1)
        page.goto(URL, wait_until="networkidle")
        page.wait_for_selector("#palette-tree .pal-cat, #palette-tree", timeout=30000)
        time.sleep(2)

        # --- the New-model type picker -------------------------------------
        page.click("#btn-new")
        wait_modal(page)
        time.sleep(1)
        shot(page, "cg-studio-new-model")
        page.click("#modal-cancel")
        time.sleep(1)

        # --- the editor, on the shipped VFD load model ----------------------
        page.set_input_files("#file-input-dsl", str(EXAMPLES / "inj_vfd_load.txt"))
        page.wait_for_function(
            "() => document.querySelectorAll('#drawflow .drawflow-node').length > 5",
            timeout=30000,
        )
        time.sleep(3)
        page.click("#btn-fit")
        time.sleep(2)
        shot(page, "cg-studio-editor")

        # --- an inspector on a selected block -------------------------------
        node = page.query_selector("#drawflow .drawflow-node")
        if node:
            node.click()
            time.sleep(1.5)
            shot(page, "cg-studio-inspector")

        # --- the %parameters metadata table ---------------------------------
        page.click("#meta-tabs >> text=%parameters")
        time.sleep(1.5)
        shot(page, "cg-studio-parameters")
        page.click("#meta-tabs >> text=%data")
        time.sleep(1)

        # --- Check Model, with the Issues panel open ------------------------
        page.click("#btn-check")
        time.sleep(2)
        if page.query_selector("#issues-wrap.collapsed"):
            page.click("#issues-header")
            time.sleep(1.5)
        shot(page, "cg-studio-check")

        # --- the Settings modal ---------------------------------------------
        page.click("#btn-settings")
        wait_modal(page, "settings-overlay")   # its own overlay, not #modal-overlay
        time.sleep(1.5)
        shot(page, "cg-studio-settings")

        browser.close()


if __name__ == "__main__":
    sys.exit(main())
