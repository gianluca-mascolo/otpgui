#!/usr/bin/env python3

import re
import tempfile

import pytest

from otpgui import OtpStore


def createotp():
    otp = OtpStore(config_file=".test-otp.yml", encryption_method="plain")
    otp.getlabel(otp.otplist[0])
    otp.getgenerator()
    return otp


def test_otp():
    otp = createotp()
    assert otp.label == "secondlabel"
    assert otp.tooltip == "second test"
    assert otp.genstring == "PONMLKJIHGFEDCBA"
    otpcode = otp.otpcode()
    otpcheck = re.compile("^[0-9]{6}$")
    assert otpcheck.match(otpcode)


def test_timeout():
    otp = createotp()
    timeout = otp.timeout()
    assert isinstance(timeout, int)
    assert 0 <= timeout <= 30


def test_progress():
    otp = createotp()
    progress = otp.progress()
    assert isinstance(progress, float)
    assert 0.0 <= progress <= 1.0


def test_multiple_labels():
    otp = OtpStore(config_file=".test-otp.yml", encryption_method="plain")
    assert len(otp.otplist) == 2
    assert "testlabel" in otp.otplist
    assert "secondlabel" in otp.otplist
    assert otp.otplist == sorted(otp.otplist)


def test_select_specific_label():
    otp = OtpStore(config_file=".test-otp.yml", encryption_method="plain")
    otp.getlabel("testlabel")
    otp.getgenerator()
    assert otp.label == "testlabel"
    assert otp.tooltip == "test name"
    assert otp.genstring == "ABCDEFGHIJKLMNOP"


def test_invalid_config_file():
    with pytest.raises(FileNotFoundError):
        OtpStore(config_file="nonexistent.yml", encryption_method="plain")


def test_invalid_yaml_content():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as f:
        f.write("invalid: yaml: content: [")
        f.flush()
        otp = OtpStore(config_file=f.name, encryption_method="plain")
        assert otp.config_data is None
        assert otp.otplist is None


def test_invalid_label():
    otp = OtpStore(config_file=".test-otp.yml", encryption_method="plain")
    with pytest.raises(KeyError):
        otp.getlabel("nonexistent_label")
