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
import yaml,time,pyotp,subprocess,argparse,sys,os
from otpversion import program_version

class OtpSettings:
    def __init__(self):
        homedir = os.environ["HOME"]
        xdg_config_home = os.environ.get("XDG_CONFIG_HOME",f"{homedir}/.config")
        otp_settings_home = xdg_config_home + "/otpgui"
        otp_settings_file = otp_settings_home + "/settings.yml"
        if not os.path.isdir(otp_settings_home):
            os.makedirs(otp_settings_home)
        if not os.path.isfile(otp_settings_file):
            self.otp_settings_data = {"config_file": f"{otp_settings_home}/otp.yml","encryption_method": "plain"}
            with open(otp_settings_file, 'w') as f:
                yaml.dump(self.otp_settings_data, f)
        else:
            try:
                with open(otp_settings_file, 'r') as f:
                    self.otp_settings_data = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                print(f"Cannot read settings file: {exc}")
                self.otp_settings_data = None

        if not os.path.isfile(self.otp_settings_data['config_file']):
            default_config_file = {"otp": 
                                    { "default":
                                        {
                                            "name": "default tooltip",
                                            "genstring":"ABCDEFGHIJKLMNOP"
                                        }
                                    }
                                }
            with open(self.otp_settings_data['config_file'], 'w') as f:
                yaml.dump(default_config_file, f)

    def settings(self):
        return self.otp_settings_data

class OtpStore:
    def __init__(self,config_file,encryption_method):
        self.config_file = config_file
        self.sops_cmd = f"sops -d --extract"
        self.encryption_method=encryption_method
        try:
            with open(config_file, 'r') as file:
                config_yaml = yaml.safe_load(file)
                self.config_data = config_yaml['otp']
                self.otplist = sorted(config_yaml['otp'])
        except yaml.YAMLError as exc:
            print(f"Error in configuration file: {exc}")
            self.config_data = None
            self.otplist = None

    def getlabel(self,label):
        self.label = label
        self.tooltip = self.config_data[label]['name']

    def getgenerator(self):
        if self.encryption_method == "sops":
            gensel = f"['otp']['{self.label}']['genstring']"
            gen_decrypt = subprocess.run(f"{self.sops_cmd} \"{gensel}\" {self.config_file}",capture_output=True,shell=True,universal_newlines=True,check=True)
            self.genstring = gen_decrypt.stdout
        elif self.encryption_method == "plain":
            self.genstring = self.config_data[self.label]['genstring']

    def otpcode(self):
        totp = pyotp.TOTP(self.genstring)
        return totp.now()

    def progress(self):
        return ((30-time.time()%30)/30)

def main():
    otp_settings_init = OtpSettings()
    otp_settings = otp_settings_init.settings()

    parser = argparse.ArgumentParser()
    parser.add_argument("-c","--config-file", help="Path to otp.yml configuration file", type=str,default=otp_settings['config_file'])
    parser.add_argument("-e","--encryption-method", help="Encryption method to use.",choices=["plain", "sops"],default=otp_settings['encryption_method'])
    parser.add_argument("-i","--interface", help="Interface to use. Default: gtk",choices=["gtk", "script"], default="gtk")
    parser.add_argument("-l","--label", help="Otp label to display on startup or script. Default to first label (sorted alphabetical) in configuration file.", type=str)
    parser.add_argument("-v","--version", help="show version",action="store_true")

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
            subprocess.run(f"sops -v",capture_output=True,shell=True,universal_newlines=True,check=True)
        except subprocess.CalledProcessError as err:
            print("Cannot run sops executable. Is it in your PATH?")
            print(f"{err}")
            sys.exit(1)
    otp = OtpStore(config_file=config_file,encryption_method=encryption_method)
    if otplabel == None:
        otp.getlabel(otp.otplist[0])
    else:
        try:
            otp.getlabel(otplabel)
        except KeyError as err:
            print(f"Label not found\nError: {err}")
            sys.exit(1)
    otp.getgenerator()
    if interface == "gtk":
        from otpgtk import MyWindow
        win = MyWindow(otp)
        win.connect("destroy", Gtk.main_quit)
        win.show_all()
        Gtk.main()
    elif interface == "script":
        print("OTP_LABEL={otplabel}\nOTP_CODE={otpcode}".format(otplabel=otp.label,otpcode=otp.otpcode()))

if __name__ == '__main__':
    main()
