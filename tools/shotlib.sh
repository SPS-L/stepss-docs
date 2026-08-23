#!/usr/bin/env bash
# Helpers for capturing STEPSS GUI windows off an Xvfb display.
#
# The previous screenshot set was shot without backing store and without a
# window manager, so a window that was momentarily obscured came back from
# the X server as a black rectangle. Everything here exists to make a capture
# depend only on what the window contains: Xvfb runs with +bs, openbox keeps
# the stacking order sane, and every shot raises its target, waits for the
# repaint, then crops the target out of a full root capture rather than
# reading the window's own (possibly clipped) area.

set -u

export DISPLAY="${SHOT_DISPLAY:-:44}"
WORK="${SHOT_WORK:-${TMPDIR:-/tmp}/stepss-shots}"
OUT="$WORK/shots"
# The screen IS the main window. STEPSS calls setExtendedState(MAXIMIZED_BOTH)
# on every launch, and FlatLaf draws its own title bar inside the client area
# (setDefaultLookAndFeelDecorated), so openbox gives the frame no decoration
# and a maximised window is exactly the screen, at (0,0). Sizing the screen is
# therefore the only way left to size the window, and it is a reliable one:
# the assertion in start_x below fails the run if the server came up any other
# size, so a figure can never be captured at a size the coordinates were not
# written for.
#
# It also pins every other window, since anything larger than the screen loses
# whatever falls off it. That is affordable here and was checked: the largest
# window in the set is the one-line diagram at 902x636.
SCREEN_W=1600
SCREEN_H=830

mkdir -p "$OUT"

# ---------------------------------------------------------------- environment

start_x() {
    Xvfb "$DISPLAY" -screen 0 "${SCREEN_W}x${SCREEN_H}x24" +bs -nolisten tcp \
        > "$WORK/xvfb.log" 2>&1 &
    XVFB_PID=$!
    for _ in $(seq 1 60); do
        xdpyinfo >/dev/null 2>&1 && break
        sleep 0.2
    done
    # Confirm this display is the one we just started, not somebody else's.
    local dim
    dim=$(xdpyinfo | awk '/dimensions:/{print $2}')
    if [ "$dim" != "${SCREEN_W}x${SCREEN_H}" ]; then
        echo "display $DISPLAY is $dim, not ours" >&2
        return 1
    fi
    openbox --sm-disable > "$WORK/openbox.log" 2>&1 &
    OPENBOX_PID=$!
    sleep 2
    echo "X up on $DISPLAY (Xvfb $XVFB_PID, openbox $OPENBOX_PID)"
}

stop_x() {
    [ -n "${OPENBOX_PID:-}" ] && kill -9 "$OPENBOX_PID" 2>/dev/null
    [ -n "${XVFB_PID:-}" ] && kill -9 "$XVFB_PID" 2>/dev/null
    return 0
}

# ---------------------------------------------------------------- window utils

# win <name-regex> - id of the newest visible window whose name matches
win() {
    local id last=
    for id in $(xdotool search --onlyvisible --name "$1" 2>/dev/null); do
        last=$id
    done
    [ -n "$last" ] || return 1
    echo "$last"
}

# wait_win <name-regex> [timeout-s] - block until such a window exists
wait_win() {
    local t=${2:-30} id
    for _ in $(seq 1 $((t * 5))); do
        id=$(win "$1") && { echo "$id"; return 0; }
        sleep 0.2
    done
    echo "timed out waiting for window '$1'" >&2
    return 1
}

# frame_geom <id> - "X Y W H" of the window including its openbox decoration
frame_geom() {
    local id=$1 x y w h ext l r t b
    eval "$(xdotool getwindowgeometry --shell "$id")"
    x=$X; y=$Y; w=$WIDTH; h=$HEIGHT
    ext=$(xprop -id "$id" _NET_FRAME_EXTENTS 2>/dev/null \
          | sed 's/.*= //; s/,//g')
    if [ -n "$ext" ] && [ "$ext" != "_NET_FRAME_EXTENTS:  not found." ]; then
        set -- $ext
        l=${1:-0}; r=${2:-0}; t=${3:-0}; b=${4:-0}
        # xdotool reports the frame's origin under a reparenting WM, so the
        # position needs no correction; only the size gains the decoration.
        w=$((w + l + r)); h=$((h + t + b))
    fi
    echo "$x $y $w $h"
}

# raise <id> - put a window on top and give it focus, then let it repaint
raise_win() {
    local id=$1
    xdotool windowraise "$id" 2>/dev/null
    xdotool windowactivate "$id" 2>/dev/null
    sleep 0.6
}

# resize_client <id> <w> <h> - size so the decorated frame comes out w x h
resize_client() {
    local id=$1 want_w=$2 want_h=$3 ext l r t b
    ext=$(xprop -id "$id" _NET_FRAME_EXTENTS 2>/dev/null | sed 's/.*= //; s/,//g')
    set -- ${ext:-0 0 0 0}
    l=${1:-0}; r=${2:-0}; t=${3:-0}; b=${4:-0}
    xdotool windowsize "$id" $((want_w - l - r)) $((want_h - t - b))
    sleep 1
}

# move_win <id> <x> <y>
move_win() {
    xdotool windowmove "$1" "$2" "$3"
    sleep 0.4
}

# shot <name> <window-id> [extra-settle-s]
# Captures the whole root, then crops the window's frame out of it. Cropping a
# root capture rather than grabbing the window means a stale or clipped window
# buffer can never reach the file.
shot() {
    local name=$1 id=$2 settle=${3:-0.8} g
    raise_win "$id"
    sleep "$settle"
    g=$(frame_geom "$id")
    set -- $g
    import -window root -screen "$OUT/.root.png"
    convert "$OUT/.root.png" -crop "$3x$4+$1+$2" +repage "$OUT/$name.png"
    rm -f "$OUT/.root.png"
    echo "  $name.png  $(identify -format '%wx%h' "$OUT/$name.png")"
    check_black "$OUT/$name.png" "$name"
}

# shot_region <name> <x> <y> <w> <h> - a fixed rectangle of the root
shot_region() {
    local name=$1
    import -window root -screen "$OUT/.root.png"
    convert "$OUT/.root.png" -crop "$4x$5+$2+$3" +repage "$OUT/$name.png"
    rm -f "$OUT/.root.png"
    echo "  $name.png  $(identify -format '%wx%h' "$OUT/$name.png")"
    check_black "$OUT/$name.png" "$name"
}

# check_black <file> <name> - refuse to ship the failure the old set shipped
check_black() {
    local pct
    pct=$(python3 - "$1" <<'PY'
import sys
from PIL import Image
im = Image.open(sys.argv[1]).convert("RGB").resize((120, 70))
px = list(im.getdata())
blk = sum(1 for p in px if p[0] < 24 and p[1] < 24 and p[2] < 24)
print(round(100.0 * blk / len(px), 1))
PY
)
    awk -v p="$pct" -v n="$2" 'BEGIN{ if (p+0 > 12) printf "  !! %s is %.1f%% black - REJECT\n", n, p }'
}

# click <x> <y> - click a point on the focused screen
click() {
    xdotool mousemove "$1" "$2" click 1
    sleep 0.5
}

# key <keys...>
key() {
    xdotool key --clearmodifiers "$@"
    sleep 0.4
}

# type_text <text>
type_text() {
    xdotool type --clearmodifiers --delay 20 "$1"
    sleep 0.3
}

# click_in <window-id> <x> <y> - click a point given in window coordinates
click_in() {
    local id=$1 X Y WIDTH HEIGHT SCREEN
    eval "$(xdotool getwindowgeometry --shell "$id")"
    xdotool mousemove $((X + $2)) $((Y + $3)) click 1
    sleep 0.5
}

# xwin_geom <id> - absolute client geometry via xwininfo, which is right for
# windows that draw their own frame (Chrome) where xdotool's numbers are not
xwin_geom() {
    xwininfo -id "$1" | awk '
        /Absolute upper-left X/ {x=$NF}
        /Absolute upper-left Y/ {y=$NF}
        /^  Width:/  {w=$NF}
        /^  Height:/ {h=$NF}
        END {print x, y, w, h}'
}

# shot_client <name> <window-id> [settle] - capture a self-decorated window
shot_client() {
    local name=$1 id=$2 settle=${3:-1.0} g
    raise_win "$id"
    sleep "$settle"
    g=$(xwin_geom "$id")
    set -- $g
    import -window root -screen "$OUT/.root.png"
    convert "$OUT/.root.png" -crop "$3x$4+$1+$2" +repage "$OUT/$name.png"
    rm -f "$OUT/.root.png"
    echo "  $name.png  $(identify -format '%wx%h' "$OUT/$name.png")"
}
