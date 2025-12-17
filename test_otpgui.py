#!/usr/bin/env python3

import re

from otpgui import OtpStore


def createotp():
    otp = OtpStore(config_file=".test-otp.yml", encryption_method="plain")
    otp.getlabel(otp.otplist[0])
    otp.getgenerator()
    return otp


def test_otp():
    otp = createotp()
    assert otp.label == "testlabel"
    assert otp.tooltip == "test name"
    assert otp.genstring == "ABCDEFGHIJKLMNOP"
    otpcode = otp.otpcode()
    otpcheck = re.compile("^[0-9]{6}$")
    assert otpcheck.match(otpcode)
