#!/usr/bin/env bash
set -u

WORKSPACE_ROOT="/Applications/Antigravity/ROCKET CLICKS/ALL DIGITAL MARKETING"
LAUNCH_SCRIPT="$WORKSPACE_ROOT/apps/seo-benchmark-native/run_app.sh"

if [[ ! -d "$WORKSPACE_ROOT" ]]; then
  echo "[seo-benchmark-launcher] ERROR: Workspace path not found: $WORKSPACE_ROOT"
  read -n 1 -s -r -p "Press any key to close..."
  echo
  exit 1
fi

if [[ ! -f "$LAUNCH_SCRIPT" ]]; then
  echo "[seo-benchmark-launcher] ERROR: Launcher script not found: $LAUNCH_SCRIPT"
  read -n 1 -s -r -p "Press any key to close..."
  echo
  exit 1
fi

cd "$WORKSPACE_ROOT" || {
  echo "[seo-benchmark-launcher] ERROR: Failed to cd into workspace"
  read -n 1 -s -r -p "Press any key to close..."
  echo
  exit 1
}

"$LAUNCH_SCRIPT"
status=$?

if [[ $status -ne 0 ]]; then
  echo "[seo-benchmark-launcher] Launcher exited with status $status"
  read -n 1 -s -r -p "Press any key to close..."
  echo
fi

exit $status
