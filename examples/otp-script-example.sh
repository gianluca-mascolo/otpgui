#!/bin/bash
# $1 is configuration filename
# $2 is label you want to retrieve
source <(./otpgui.py -c $1 -l $2 -i script)
echo "Otp label: $OTP_LABEL"
echo "Otp code: $OTP_CODE"
