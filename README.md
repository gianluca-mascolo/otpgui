# otpgui
An OTP generator compatible with totp. Written in python and gtk.

### How to install it:
- Install the necessary python requirements (use pip or your favorite distro package manager)
- Write a file `.otp.yml` in your home directory containing yout secrets.
- launch otpgui.py

### Configuration file
The configuration file is a simple yaml (see example) with this information:
- a label (to be shown in the dropdown menu)
- an extended "name" for that label
- the string that generate the otp code


### How to use it:
- select the label for the otp you want to generate
- if you stay with mouse over the otpcode you will see the extended secret name
- if you click the otp code it will be copied to clipboard

### Screenshot

![otpgui](https://user-images.githubusercontent.com/20320073/41290428-1fe3d8ba-6e4d-11e8-83c9-530ca252910e.png)
