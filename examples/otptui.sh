#!/bin/bash
SELECTED_OTP="$1"
set -euo pipefail
if [[ "${SELECTED_OTP:-null}" == "null" ]]; then
    # shellcheck disable=2086
    cat <<EOM
Error: you must select an otp label
Usage: $(basename $0) [OTP LABEL]
Example: $(basename $0) mylabel
EOM
    exit 1
fi
while [[ "${KEY:-null}" != 'q' ]]; do
    # shellcheck disable=2046
    eval $(otpgui -i script -l "$SELECTED_OTP" | tr \\n ";")
    echo $((${OTP_TIMEOUT:-0} * 100 / 30))
    echo "XXX"
    echo -e "Code: ${OTP_CODE:-null}\nExpire: ${OTP_TIMEOUT:-0}\nPress 'q' to exit\n"
    echo "XXX"
    read -r -s -n 1 -t .5 KEY || true
done |
    dialog --title "$SELECTED_OTP" --gauge "otp_widget" 8 30 0
