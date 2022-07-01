# otpgui
An OTP generator compatible with totp written in python.

## About

**otpgui** provides a graphical application for GNU/Linux that display TOTP codes for two-factor-authentication (2FA). It can be used as a replacement or companion for mobile apps like Google Authenticator or Microsoft Autenticator.

<p align="center">![otpgui](https://user-images.githubusercontent.com/20320073/41290428-1fe3d8ba-6e4d-11e8-83c9-530ca252910e.png) *otpgui showing a one time password for gmail*
</p>

## Installation

### Debian and Ubuntu

Download the deb package from [release](https://github.com/gianluca-mascolo/otpgui/releases/tag/0.2.2) page. Double click on the package or use
```
sudo apt install ./python3-otpgui_*_all.deb
```
from the command line.
#### Supported versions:
* Debian 10 (buster) and later
* Ubuntu 20.04 and later

### Arch Linux

Download the zst package from [release](https://github.com/gianluca-mascolo/otpgui/releases/tag/0.2.2) page. Install with
```
sudo pacman -U ./otpgui-*-any.pkg.tar.zst 
```
Alternatively you can build it yourself from [AUR](https://aur.archlinux.org/packages/otpgui).

### Other Distributions

otpgui should work with any distro with a recent version of python 3.7+ and gtk3. You can try installing the pip wheel from [release](https://github.com/gianluca-mascolo/otpgui/releases/tag/0.2.2) page. pip installation require development packages for python, gobject and cairo (e.g. on debian like distros: `apt install python3-pip pkg-config libgirepository1.0-dev libcairo2-dev gir1.2-gtk-3.0`)
```
pip install --user ./otpgui-*-py3-none-any.whl
```
Alternatively you can install it in a virtual env using [python poetry](https://python-poetry.org/).
```
poetry install
poetry run otpgui
```
## Usage
You can install the 
Secrets to generate codes are stored in a YAML file (optionally encrypted by sops)


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

You can:
- select the label for the otp you want to generate
- stay with mouse over the otpcode to see a secret tooltip
- click the otp code to copy it to the clipboard
