#!/usr/bin/env python3
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
import yaml,gi,time,pyotp,subprocess,argparse,sys
gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gdk,Gtk,GObject,GLib
from otpversion import program_version

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
class MyWindow(Gtk.Window):

    def __init__(self,otp):
        self.otp = otp
        Gtk.Window.__init__(self, title="OTP")
        
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)
        
        self.OtpCode = Gtk.Button.new_with_label(otp.otpcode())
        self.OtpCode.set_tooltip_text(otp.tooltip)
        self.OtpCode.connect("clicked", self.on_otp_clicked)
        vbox.pack_start(self.OtpCode, True, True, 0)

        self.ProgressBar = Gtk.ProgressBar(fraction=otp.progress())
        vbox.pack_start(self.ProgressBar, True, True, 0)

        self.timeout_id = GLib.timeout_add(1000, self.on_timeout)
        self.activity_mode = False
        
        self.OtpLabelStore = Gtk.ListStore(str)
        for key in otp.otplist:
                self.OtpLabelStore.append([key])

        self.OtpCombo = Gtk.ComboBox.new_with_model(self.OtpLabelStore)
        self.OtpCombo.set_active(otp.otplist.index(otp.label))
        self.OtpCombo.connect("changed", self.on_otp_changed)
        renderer_text = Gtk.CellRendererText()
        self.OtpCombo.pack_start(renderer_text, True)
        self.OtpCombo.add_attribute(renderer_text, "text", 0)
        vbox.pack_start(self.OtpCombo, False, False, 0)
        
    def on_timeout(self):
        new_value = self.otp.progress()
        self.ProgressBar.set_fraction(new_value)
        self.OtpCode.set_label(self.otp.otpcode())
        self.OtpCode.set_tooltip_text(self.otp.tooltip)
        return True
        
    def on_otp_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            SelectedLabel = model[tree_iter][0]
            self.otp.getlabel(SelectedLabel)
            self.otp.getgenerator()
    
    def on_otp_clicked(self,OtpCode):
        self.clipboard.set_text(self.OtpCode.get_label(), -1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c","--config-file", help="Path to otp.yml configuration file", type=str,required=True)
    parser.add_argument("-e","--encryption-method", help="Encryption method to use. Default: sops",choices=["plain", "sops"], default="sops")
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
        win = MyWindow(otp)
        win.connect("destroy", Gtk.main_quit)
        win.show_all()
        Gtk.main()
    elif interface == "script":
        print("OTP_LABEL={otplabel}\nOTP_CODE={otpcode}".format(otplabel=otp.label,otpcode=otp.otpcode()))

if __name__ == '__main__':
    main()
