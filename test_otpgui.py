#!/usr/bin/env python2
import yaml,time,pyotp

def getconf():
    try:
        config_data = yaml.safe_load(file('.test-otp.yml', 'r'))
    except yaml.YAMLError, exc:
        print "Error in configuration file:", exc
        sys.exit(1)

    return config_data
    
def test_getconf():
    print "loading test configuration"
    assert getconf().keys()[0] == 'label'
    print "getting config section 'name'"
    assert getconf()['label']['name'] == 'test name'
    print "getting config section 'genstring'"
    assert getconf()['label']['genstring'] == 'ABCDEFGHIJKLMNOP'

def test_genotp():
    print "generating well known otp from configuration"
    totp = pyotp.TOTP(getconf()['label']['genstring'])
    assert totp.at(1529158509) == '045859'
