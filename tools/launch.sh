#!/usr/bin/env bash
# Seeds a private preferences node and starts STEPSS GUI on the capture display.
#
# Private, because a screenshot run must not touch the operator's own theme,
# window geometry or working directory - and because seeding is the only way to
# get a deterministic 1600x760 window: windowMaximised defaults to true, so an
# unseeded launch fills the screen and openbox then refuses the resize.
#
# Usage: launch.sh light|dark

set -eu
THEME=${1:-light}
MODE=${2:-normal}   # "first" leaves the first-run flag out, so the licence shows
WORK="${SHOT_WORK:-${TMPDIR:-/tmp}/stepss-shots}"
PREFS="$WORK/prefs"
EXAMPLES="$HOME/stepss-examples"
NODE="$PREFS/.java/.userPrefs"

case "$THEME" in
    light) DARK=false ;;
    dark)  DARK=true ;;
    *) echo "usage: launch.sh light|dark" >&2; exit 1 ;;
esac

rm -rf "$PREFS"
DIR=$(python3 - "$NODE" <<'PY'
# Java mangles a node name into a directory name; reuse its own encoding by
# asking for the directory the JDK already created once, which is recorded
# here as a literal so the run does not depend on a previous session.
import os, sys
base = sys.argv[1]
name = "_!'0!e@!u!(:!d!\"l!(!!cw\"z!#4!`w\"0!'`!c!\"z!(:!_@\","
d = os.path.join(base, name)
os.makedirs(d, exist_ok=True)
print(d)
PY
)

FIRST_ENTRY='  <entry key="stepssFirstTime" value="false"/>'
if [ "$MODE" = first ]; then FIRST_ENTRY=""; fi

cat > "$DIR/prefs.xml" <<EOF
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE map SYSTEM "http://java.sun.com/dtd/preferences.dtd">
<map MAP_XML_VERSION="1.0">
  <entry key="examplesDirectory" value="$EXAMPLES"/>
  <entry key="showExamplesAtStartup" value="false"/>
$FIRST_ENTRY
  <entry key="checkUpdatesAtStartup" value="false"/>
  <entry key="darkTheme" value="$DARK"/>
  <entry key="windowMaximised" value="false"/>
  <entry key="windowX" value="60"/>
  <entry key="windowY" value="60"/>
  <entry key="windowWidth" value="1600"/>
  <entry key="windowHeight" value="760"/>
  <entry key="workingDirectory" value="$WORK/run"/>
</map>
EOF

mkdir -p "$WORK/run"
cd "$WORK/run"
DISPLAY=:44 nohup java \
    -Djava.util.prefs.userRoot="$PREFS" \
    -Djava.util.prefs.systemRoot="$PREFS" \
    -cp "/opt/stepss/lib/app/stepss.jar:/opt/stepss/lib/app/lib/*" \
    my.stepss.StepssUI > "$WORK/stepss-$THEME.log" 2>&1 &
echo "$!" > "$WORK/app.pid"
echo "started STEPSS ($THEME) pid $(cat "$WORK/app.pid")"
