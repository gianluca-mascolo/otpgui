#!/bin/bash

set -euo pipefail

# SCRIPT_DIR: This is a reimplementation of 'realpath' in pure Python.
# This will improve compatibility with operating systems where realpath is not available (e.g. MacOSX)
# and since Python is required anyway to run the otpgui script, it is not an issue to use Python here.

SCRIPT_DIR="$(python -c 'import pathlib, sys; print(pathlib.Path((sys.argv[1])).resolve().parent)' "${BASH_SOURCE[0]}")"

# SCRIPT_NAME: script filename
SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"

# By default assume that otptui.sh is in PATH
OTPTUI_PATH=""

# Fallback OTPTUI_PATH to local directory if found
[[ -f "./otptui.sh" ]] && OTPTUI_PATH="./"

# Try to detect if we are running inside a git repository.
# If so, let's set OTPTUI_PATH to the examples dir to run otptui.sh from there.

if [[ -d "$SCRIPT_DIR" ]] && [[ -f "${SCRIPT_DIR}/${SCRIPT_NAME}" ]] && git --version >/dev/null 2>&1; then
    pushd "$SCRIPT_DIR" >/dev/null 2>&1 || true
    GIT_TOP="$(git rev-parse --show-toplevel 2>/dev/null || true)"
    if [[ "${GIT_TOP:-null}" != "null" ]]; then
        OTPTUI_PATH="${GIT_TOP}/examples/"
    fi
    popd >/dev/null 2>&1 || true
fi

# Finally set the OTPTUI_SCRIPT location according to detected OTPTUI_PATH
OTPTUI_SCRIPT="${OTPTUI_PATH}otptui.sh"

TMPMENU="$(mktemp)"
TMPOTP="$(mktemp)"
(
    echo "--menu otp 50 70 30 \\"
    yq .otp "$HOME/develop/otp/otp.yml" -o json |
        jq -Mrcs '.[] | to_entries | sort_by(.key) | map([.key, .value.name] | join(";"))[]' |
        awk -F';' 'NR>1{print p" \\"}{p="\t\""$1"\" \""$2"\""}END{print p}'
) >"$TMPMENU"
dialog --file "$TMPMENU" 2>"$TMPOTP"
SELECTED_OTP="$(cat "$TMPOTP")"
clear
$OTPTUI_SCRIPT "$SELECTED_OTP"
[[ -f "$TMPMENU" ]] && rm -f "$TMPMENU"
[[ -f "$TMPOTP" ]] && rm -f "$TMPOTP"
reset
clear
