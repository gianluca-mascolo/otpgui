#!/usr/bin/python3
"""
otpgui.py is an OTP generator compatible with TOTP.
Copyright (C) 2018 Gianluca Mascolo <gianluca@gurutech.it>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import argparse
import os
import subprocess
import sys
import time

import pyotp
import yaml

from otpversion import program_version


class SopsDecryptionError(Exception):
    """Raised when SOPS fails to decrypt the OTP secrets."""

    pass


class OtpSettings:
    def __init__(self):
        homedir = os.environ["HOME"]
        xdg_config_home = os.environ.get("XDG_CONFIG_HOME", f"{homedir}/.config")
        otp_settings_home = xdg_config_home + "/otpgui"
        otp_settings_file = otp_settings_home + "/settings.yml"
        if not os.path.isdir(otp_settings_home):
            os.makedirs(otp_settings_home)
        if not os.path.isfile(otp_settings_file):
            self.otp_settings_data = {"config_file": f"{otp_settings_home}/otp.yml", "encryption_method": "plain"}
            with open(otp_settings_file, "w") as f:
                yaml.dump(self.otp_settings_data, f)
        else:
            try:
                with open(otp_settings_file, "r") as f:
                    self.otp_settings_data = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                print(f"Cannot read settings file: {exc}")
                self.otp_settings_data = None

        if not os.path.isfile(self.otp_settings_data["config_file"]):
            default_config_file = {"otp": {"default": {"name": "default tooltip", "genstring": "ABCDEFGHIJKLMNOP"}}}
            with open(self.otp_settings_data["config_file"], "w") as f:
                yaml.dump(default_config_file, f)

    def settings(self):
        return self.otp_settings_data


class OtpStore:
    def __init__(self, config_file, encryption_method):
        self.config_file = config_file
        self.sops_cmd = "sops -d --extract"
        self.encryption_method = encryption_method
        try:
            with open(config_file, "r") as file:
                config_yaml = yaml.safe_load(file)
                self.config_data = config_yaml["otp"]
                self.otplist = sorted(config_yaml["otp"])
        except yaml.YAMLError as exc:
            print(f"Error in configuration file: {exc}")
            self.config_data = None
            self.otplist = None

    def getlabel(self, label):
        self.label = label
        self.tooltip = self.config_data[label]["name"]

    def _get_sops_key_id(self):
        """Try to read the GPG key ID from .sops.yaml in the config directory."""
        config_dir = os.path.dirname(self.config_file)
        sops_yaml_path = os.path.join(config_dir, ".sops.yaml")
        if os.path.isfile(sops_yaml_path):
            try:
                with open(sops_yaml_path, "r") as f:
                    sops_config = yaml.safe_load(f)
                    for rule in sops_config.get("creation_rules", []):
                        pgp_key = rule.get("pgp", "")
                        if pgp_key:
                            return f"0x{pgp_key[-16:]}"
            except (yaml.YAMLError, KeyError, TypeError):
                pass
        return None

    def getgenerator(self):
        if self.encryption_method == "sops":
            gensel = f"['otp']['{self.label}']['genstring']"
            try:
                gen_decrypt = subprocess.run(f'{self.sops_cmd} "{gensel}" {self.config_file}', capture_output=True, shell=True, universal_newlines=True, check=True)
                self.genstring = gen_decrypt.stdout
            except subprocess.CalledProcessError as err:
                error_output = err.stderr.strip() if err.stderr else "No error details available"
                key_id = self._get_sops_key_id()
                key_msg = f"  • You must load GPG key {key_id}\n" if key_id else ""
                raise SopsDecryptionError(
                    f"Failed to decrypt OTP secret for label '{self.label}'.\n\n"
                    f"━━━ Possible causes ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"{key_msg}"
                    f"  • GPG key not loaded (run: gpg --card-status or gpg-connect-agent reloadagent /bye)\n"
                    f"  • gpg-agent not running (run: gpg-agent --daemon)\n"
                    f"  • Wrong GPG key configured in .sops.yaml\n\n"
                    f"━━━ SOPS error details ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"{error_output}"
                ) from None
        elif self.encryption_method == "plain":
            self.genstring = self.config_data[self.label]["genstring"]

    def otpcode(self):
        totp = pyotp.TOTP(self.genstring)
        return totp.now()

    def timeout(self):
        return int(30 - time.time() % 30)

    def progress(self):
        return (30 - time.time() % 30) / 30


def main():
    otp_settings_init = OtpSettings()
    otp_settings = otp_settings_init.settings()

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config-file", help="Path to otp.yml configuration file", type=str, default=otp_settings["config_file"])
    parser.add_argument("-e", "--encryption-method", help="Encryption method to use.", choices=["plain", "sops"], default=otp_settings["encryption_method"])
    parser.add_argument("-i", "--interface", help="Interface to use. Default: gtk", choices=["gtk", "script"], default="gtk")
    parser.add_argument("-l", "--label", help="Otp label to display on startup or script. Default to first label (sorted alphabetical) in configuration file.", type=str)
    parser.add_argument("-v", "--version", help="show version", action="store_true")

    args = parser.parse_args()
    if args.version:
        print(f"{program_version}")
        sys.exit(0)
    config_file = args.config_file
    encryption_method = args.encryption_method
    interface = args.interface
    otplabel = args.label

    if encryption_method == "sops":
        try:
            subprocess.run("sops -v", capture_output=True, shell=True, universal_newlines=True, check=True)
        except subprocess.CalledProcessError as err:
            print("Cannot run sops executable. Is it in your PATH?")
            print(f"{err}")
            sys.exit(1)
    otp = OtpStore(config_file=config_file, encryption_method=encryption_method)
    if otplabel is None:
        otp.getlabel(otp.otplist[0])
    else:
        try:
            otp.getlabel(otplabel)
        except KeyError as err:
            print(f"Label not found\nError: {err}")
            sys.exit(1)
    try:
        otp.getgenerator()
    except SopsDecryptionError as err:
        if interface == "gtk":
            import gi

            gi.require_version("Gtk", "3.0")
            from gi.repository import Gtk

            dialog = Gtk.MessageDialog(
                transient_for=None,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="Decryption Error",
            )
            dialog.format_secondary_text(str(err))
            dialog.run()
            dialog.destroy()
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)
    if interface == "gtk":
        from gi.repository import Gtk

        from otpgtk import MyWindow

        win = MyWindow(otp)
        win.connect("destroy", Gtk.main_quit)
        win.show_all()
        Gtk.main()
    elif interface == "script":
        print("OTP_LABEL={otplabel}\nOTP_CODE={otpcode}\nOTP_TIMEOUT={otptimeout}".format(otplabel=otp.label, otpcode=otp.otpcode(), otptimeout=otp.timeout()))


if __name__ == "__main__":
    main()
