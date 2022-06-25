# otpgui
An OTP generator compatible with totp written in python.

## Requirements:
- Python dependencies are managed with [poetry](https://python-poetry.org).
- Install the virtual environment with `poetry install`.
- `sops` is required to encrypt and decrypt the configuration file.

## Configuration file
The configuration file is a yaml file with this information:

- a label (to be shown in the dropdown menu)
- an extended "name" for that label
- the string that generate the otp code

Because the generator string is a sensitive data, it must be encrypted in the configuration file with [sops](https://github.com/mozilla/sops).
<!-- This is commented out. -->

## <!-- mark -->Encryption<!-- down -->
To create a new `otp.yml` configuration file:
- create a new directory, e.g. `mkdir ~/otp`
- copy the `sops-example.yml` into `~/otp/.sops.yaml`.
- edit `~/otp/.sops.yaml` to setup your preferred encryption method (e.g. use `gpg --fingerprint` to setup your gpg key)
- create the encrypted configuration with `sops otp.yml`
- Paste the `otp.yml` [sample](otp-example.yml) configuration or write your own.
## Usage:
Start otpgui with `otpgui.py -c <CONFIG_FILE>` or (for virtualenv) with `poetry run python otpgui.py -c <CONFIG_FILE>`.  
`CONFIG_FILE` is the full path to an `otp.yml` configuration file enrypted with `sops`. A window with otp code will appear.  
![otpgui](https://user-images.githubusercontent.com/20320073/41290428-1fe3d8ba-6e4d-11e8-83c9-530ca252910e.png)  
You can:
- select the label for the otp you want to generate
- stay with mouse over the otpcode to see a secret tooltip
- click the otp code to copy it to the clipboard
