# otpgui
An OTP generator compatible with totp written in python.

## About

**otpgui** provides a graphical application for GNU/Linux that display TOTP codes for two-factor-authentication (2FA). It can be used as a replacement or companion for mobile apps like Google Authenticator or Microsoft Autenticator.

<p align="center">

![otpgui](https://user-images.githubusercontent.com/20320073/41290428-1fe3d8ba-6e4d-11e8-83c9-530ca252910e.png)

*otpgui showing a one time password for gmail*

</p>

## Quickstart
- Install otpgui package from [release](https://github.com/gianluca-mascolo/otpgui/releases/latest) page.
- Edit `~/.config/otpgui/otp.yml` to configure otp secrets
- Start OTP gui from your desktop menu

## Installation

### Debian and Ubuntu

Download the deb package from [release](https://github.com/gianluca-mascolo/otpgui/releases/latest) page. Double click on the package or use
```
sudo apt install ./python3-otpgui_*_all.deb
```
from the command line.
#### Supported versions:
* Debian 10 (buster) and later
* Ubuntu 20.04 (focal) and later

### Arch Linux

Download the zst package from [release](https://github.com/gianluca-mascolo/otpgui/releases/latest) page. Install with
```
sudo pacman -U ./otpgui-*-any.pkg.tar.zst 
```
Alternatively you can build it yourself from [AUR](https://aur.archlinux.org/packages/otpgui).

### Other Distributions

otpgui should work with any distro with a recent version of python 3.7+ and gtk3. You can try installing the pip wheel from [release](https://github.com/gianluca-mascolo/otpgui/releases/latest) page. pip installation require development packages for python, gobject and cairo (e.g. on debian like distros: `apt install python3-pip pkg-config libgirepository1.0-dev libcairo2-dev gir1.2-gtk-3.0`)
```
pip install --user ./otpgui-*-py3-none-any.whl
```
Alternatively you can install it in a virtual env using [python poetry](https://python-poetry.org/).
```
poetry install
poetry run otpgui
```

## Usage

- Start OTP gui from your main menu
- Select an otp to display from the dropdown menu
- Just click the otp code to copy it into the clipboard. Paste the otp code on the website requesting it
- If you stay with the mouse over the code a tooltip with additional information about that otp is displayed.

## Configuration

### General settings

Configuration file is stored into your home directory ~/.config/otpgui/settings.yml. Example:
```
config_file: /home/testuser/.config/otpgui/otp.yml
encryption_method: plain
```
| Setting             | Default                  | Description |
| ------------------- | ------------------------ | ----------- |
| `config_file`       | `~/.config/otpgui/otp.yml` | File where otp code secrets are stored | 
| `encryption_method` | `plain`                    | Encryption method for otp secrets store file (`plain` or `sops`) |

### Otp secrets file

The otp secrets file is a simple yaml file structured like the following example:
```yaml
otp:
  label1:
    name: "description for label1"
    genstring: "ABCDEFGHIJKLMNOP"
  label2:
    name: "description for label2"
    genstring: "ABCDEFGHIJKLMNOP"
  gmail:
    name: "account foo.bar@gmail.com"
    genstring: "ABCDEFGHIJKLMNOP"
  amazon:
    name: "account pinco.pallino@hotmail.com"
    genstring: "ABCDEFGHIJKLMNOP"
```
Each label will appear in the dropdown menu of otpgui. `name` is the tooltip you want to display about otp-code you are displaying, and `genstring` is the secret string used to generate the code.

### Getting the otp secret strings

If you are configuring a new service with 2FA, when the website shows up the QR-code to scan there is usually a link that will reveal you the secret string (e.g. click on _"I can't scan QR code"_ or similar under the QR-code you see on the screen).

If you already have OTP codes installed on your mobile phone, some applications allow you to show the QR code that generate the OTP. If this is your case you can use a QR-code scanner for desktop  (e.g. `zbarcam-gtk`) to read it and paste the code into `otp.yml`. Anyway if your mobile app does not allow you to show the QR code for a specific otp, as a workaround you can:
- authenticate to the website requiring 2FA using your mobile phone
- remove 2FA authentication and apply it again to regenerate the QR-code
- Save the secret string into `otp.yml` and take a screenshot so you can keep it both in mobile phone and otpgui.

### Encryption

To protect secrets in `otp.yml` you can optionally encrypt the file with [sops](https://github.com/mozilla/sops). Read the documentation on sops page to learn how to configure/use it. The only value that you need to encrypt in the YAML file is `genstring`. To do it create a dedicated directory for your `otp.yml` and `.sops.yaml`, for example in a directory `~/Documents/otp`:
```
]$ ls -1a ~/Documents/otp
otp.yml
.sops.yaml
```
To configure `.sops.yaml` you can use this [example file](examples/sops-example.yml).
Don't forget to change the location of `otp.yml` in `~/.config/otpgui/settings.yml` to use the new file.

## CLI interface

It is of course possible to start `otpgui` from cli. To access the help:
```
]$ otpgui -h
usage: otpgui [-h] [-c CONFIG_FILE] [-e {plain,sops}] [-i {gtk,script}]
              [-l LABEL] [-v]

options:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --config-file CONFIG_FILE
                        Path to otp.yml configuration file
  -e {plain,sops}, --encryption-method {plain,sops}
                        Encryption method to use.
  -i {gtk,script}, --interface {gtk,script}
                        Interface to use. Default: gtk
  -l LABEL, --label LABEL
                        Otp label to display on startup or script. Default to
                        first label (sorted alphabetical) in configuration
                        file.
  -v, --version         show version
```
Any parameter that you specify in the command line will take precedence over configuration stored in `~/.config/otpgui/settings.yml`.

### Scripted mode
There is a `script` mode you can use in your shell scripts, e.g.
```
]$ otpgui -i script -l amznit
OTP_LABEL=amznit
OTP_CODE=123456
```
Look at the [example script](examples/otp-script-example.sh) to import script output into shell variables.
