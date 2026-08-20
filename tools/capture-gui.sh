#!/usr/bin/env bash
# Drives STEPSS GUI through one complete session and captures every figure the
# documentation uses, in one theme. Run it twice, light and dark.
#
#   capture-gui.sh light
#   capture-gui.sh dark
#
# The window is pinned to 1600x760 by seeded preferences, so every coordinate
# below is a fixed point in that window and both runs traverse the same pixels.
# Windows the application opens by itself are found by name and measured at
# capture time, never assumed.

set -u
THEME=${1:-light}
WORK="${SHOT_WORK:-${TMPDIR:-/tmp}/stepss-shots}"
EXAMPLES=$HOME/stepss-examples
CASE="$EXAMPLES/kundur-two-area"
SRC="${STEPSS_SRC:-$(cd "$(dirname "$0")/../.." && pwd)}"   # the umbrella checkout

source "$WORK/shotlib.sh"
# shot names carry the theme as a subdirectory; OUT stays the shots root
mkdir -p "$OUT/$THEME"

# Window origin, and the offset from window coordinates to screen coordinates.
WX=60
WY=60
c() { click $((WX + $1)) $((WY + $2)); }   # click at window coordinates

# --- fixed points in the 1600x760 window ------------------------------------
MENU_FILE_X=20;   MENU_FILE_Y=47
MENU_TOOLS_X=65;  MENU_TOOLS_Y=47
FILE_EXAMPLES_X=81; FILE_EXAMPLES_Y=130
TAB_Y=79
TAB_SYSDATA=54; TAB_OBS=161; TAB_PF=302; TAB_DYN=469; TAB_ANA=588; TAB_CG=669
BANNER_DISMISS_X=1543; BANNER_DISMISS_Y=82
OBS_TYPE1_X=103; OBS_TYPE1_Y=166
OBS_NAME1_X=900; OBS_NAME1_Y=166
OBS_NAME2_X=900; OBS_NAME2_Y=196
OBS_WIZ_X=24;    OBS_WIZ_Y=423
BTN_Y=706
PF_RUN=76; PF_BUSOV=637; PF_BRANCH=761; PF_GEN=903; PF_BAL=1274
DYN_RUN=105
ANA_EXTRACT=78; ANA_SSA=145
CG_LOAD=99; CG_RUN=256

banner() { echo; echo "=== $* ==="; }

# ---------------------------------------------------------------- 1. licence
banner "$THEME: launch"
rm -rf "$CASE"
mkdir -p "$EXAMPLES"
"$WORK/launch.sh" "$THEME" first >/dev/null
L=$(wait_win "License Agreement" 60) || exit 1
sleep 2
shot "$THEME/gui-license" "$L" 1.0
click_in "$L" 589 548          # Accept
sleep 4

M=$(wait_win "^STEPSS" 40) || exit 1
sleep 3
echo "main window: $(xdotool getwindowgeometry --shell "$M" | tr '\n' ' ')"

# ------------------------------------------------------- 2. open the example
banner "$THEME: open example"
raise_win "$M"
c $MENU_FILE_X $MENU_FILE_Y; sleep 1
c $FILE_EXAMPLES_X $FILE_EXAMPLES_Y; sleep 3
E=$(wait_win "Open Examples" 30) || exit 1
sleep 1.5
shot "$THEME/gui-open-examples" "$E" 1.0
click_in "$E" 530 542          # Open example
sleep 8

M=$(win "^STEPSS")
shot "$THEME/gui-example-banner" "$M" 1.5
raise_win "$M"
c $BANNER_DISMISS_X $BANNER_DISMISS_Y; sleep 1.5
shot "$THEME/gui-system-data" "$M" 1.0

cp "$SRC/stepss-ramses/models/exc/ieee/exc_AC1A.txt" "$CASE/" 2>/dev/null

# ----------------------------------------------------------- 3. observables
banner "$THEME: observables"
raise_win "$M"
c $TAB_OBS $TAB_Y; sleep 1.2
c $OBS_TYPE1_X $OBS_TYPE1_Y; key Escape; key Down; key Return; sleep 0.6
c $OBS_NAME1_X $OBS_NAME1_Y; type_text "G1"
c $OBS_NAME2_X $OBS_NAME2_Y; type_text "9"
sleep 0.8
shot "$THEME/gui-observables" "$M" 1.0

# The picker panel is taller than the tab, so this one figure gets a taller
# window rather than a clipped panel.
c $OBS_WIZ_X $OBS_WIZ_Y; sleep 1.2
xdotool windowsize "$M" 1600 830; sleep 1.5
c 446 480; type_text "9";  c 783 480; sleep 1     # Buses:  add bus 9
c 446 616; type_text "G1"; c 783 616; sleep 1.5   # Sync machines: add G1
shot "$THEME/gui-observable-picker" "$M" 1.0
c $OBS_WIZ_X $OBS_WIZ_Y; sleep 1                  # untick
xdotool windowsize "$M" 1600 760; sleep 1.5

# ------------------------------------------------------------ 4. power flow
banner "$THEME: power flow"
raise_win "$M"
c $TAB_PF $TAB_Y; sleep 1
c $PF_RUN $BTN_Y; sleep 16

D=$(win "One-line diagram") && {
    shot "$THEME/gui-one-line-diagram" "$D" 2.0
    xdotool windowminimize "$D"; sleep 1
}
raise_win "$M"
shot "$THEME/gui-power-flow" "$M" 1.0

for pair in "$PF_BUSOV:gui-bus-overview" "$PF_BRANCH:gui-branch-flows" \
            "$PF_GEN:gui-generators-svcs" "$PF_BAL:gui-power-balance"; do
    x=${pair%%:*}; name=${pair##*:}
    raise_win "$M"
    c "$x" $BTN_Y; sleep 2.5
    shot "$THEME/$name" "$M" 1.0
done

# ----------------------------------------------------- 5. dynamic simulation
banner "$THEME: dynamic simulation"
raise_win "$M"
c $TAB_DYN $TAB_Y; sleep 1
c $DYN_RUN $BTN_Y; sleep 20

R=$(win "Run-time curves") && {
    shot "$THEME/gui-runtime-curves" "$R" 2.0
    xdotool windowminimize "$R"; sleep 1
}
raise_win "$M"
shot "$THEME/gui-dynamic-simulation" "$M" 1.0

# ------------------------------------------------------------- 6. analysis
banner "$THEME: analysis"
raise_win "$M"
c $TAB_ANA $TAB_Y; sleep 1.2
shot "$THEME/gui-analysis" "$M" 1.0

c $ANA_EXTRACT 172; sleep 6
P=$(wait_win "Select Observables" 30) || exit 1
sleep 1.5
click_in "$P" 142 58; sleep 1.2      # Category
click_in "$P" 118 155; sleep 1.5     # SYNC
click_in "$P" 30 107; sleep 0.6      # G1
click_in "$P" 260 369; sleep 1.5     # Add  (list empty: button sits low)
click_in "$P" 30 152; sleep 0.6      # G3
click_in "$P" 260 323; sleep 1.5     # Add  (one row present: button moved up)
shot "$THEME/gui-select-observables" "$P" 1.0
click_in "$P" 398 569; sleep 10      # Plot

C=$(wait_win "^Curves" 30) && {
    xdotool windowsize "$C" 1000 600; sleep 2
    shot "$THEME/gui-plot" "$C" 2.0
    xdotool windowminimize "$C"; sleep 1
}

banner "$THEME: small-signal analysis"
raise_win "$M"
c $ANA_SSA 330; sleep 35
S=$(wait_win "Small-signal results" 60) && {
    sleep 3
    click_in "$S" 250 236; sleep 2.5     # the 0.62 Hz inter-area mode
    shot "$THEME/gui-ssa-results" "$S" 1.5
    xdotool windowminimize "$S"; sleep 1
}

# -------------------------------------------------------------- 7. codegen
banner "$THEME: codegen"
raise_win "$M"
c $TAB_CG $TAB_Y; sleep 1
c $CG_LOAD $BTN_Y; sleep 4
F=$(wait_win "Choose Data File" 30) && {
    click_in "$F" 350 263
    type_text "$CASE/exc_AC1A.txt"
    sleep 0.6
    click_in "$F" 463 337
    sleep 5
}
raise_win "$M"
c $CG_RUN $BTN_Y; sleep 12
shot "$THEME/gui-codegen" "$M" 1.0

# ---------------------------------------------------- 8. menus, status bar
banner "$THEME: menus and status bar"
raise_win "$M"
c $MENU_FILE_X $MENU_FILE_Y; sleep 1.5
shot_region "$THEME/gui-file-menu" $WX $WY 700 400
key Escape; sleep 0.8
c $MENU_TOOLS_X $MENU_TOOLS_Y; sleep 1.5
shot_region "$THEME/gui-tools-menu" $WX $WY 700 460
key Escape; sleep 0.8
shot_region "$THEME/gui-status-bar" $WX $((WY + 724)) 1600 36

banner "$THEME: done"
kill -9 "$(cat "$WORK/app.pid")" 2>/dev/null
sleep 2
ls -la "$OUT/$THEME" | tail -30
