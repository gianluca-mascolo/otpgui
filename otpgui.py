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
import yaml,gi,time,pyotp
from os.path import expanduser
gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gdk,Gtk,GObject

class MyWindow(Gtk.Window):

    def __init__(self):
        global totp
        global config_data
        global SelectedLabel
        Gtk.Window.__init__(self, title="OTP")
        
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)
        
        self.OtpCode = Gtk.Button.new_with_label(totp.now())
        self.OtpCode.set_tooltip_text(config_data[SelectedLabel]['name'])
        self.OtpCode.connect("clicked", self.on_otp_clicked)
        vbox.pack_start(self.OtpCode, True, True, 0)

        self.ProgressBar = Gtk.ProgressBar(fraction=( ( 30 - time.time() % 30 ) / 30))
        vbox.pack_start(self.ProgressBar, True, True, 0)

        self.timeout_id = GObject.timeout_add(1000, self.on_timeout, None)
        self.activity_mode = False
        
        self.OtpLabelStore = Gtk.ListStore(str)
        for key in config_data:
                self.OtpLabelStore.append([key])

        self.OtpLabelStoreSorted = Gtk.TreeModelSort(self.OtpLabelStore)
        self.OtpLabelStoreSorted.set_sort_column_id(0, Gtk.SortType.ASCENDING)

        self.OtpCombo = Gtk.ComboBox.new_with_model(self.OtpLabelStoreSorted)
        self.OtpCombo.set_active(0)
        self.OtpCombo.connect("changed", self.on_otp_changed)
        renderer_text = Gtk.CellRendererText()
        self.OtpCombo.pack_start(renderer_text, True)
        self.OtpCombo.add_attribute(renderer_text, "text", 0)
        vbox.pack_start(self.OtpCombo, False, False, 0)
        
    def on_timeout(self, user_data):
        global totp
        global config_data
        global SelectedLabel
        new_value = ( ( 30 - time.time() % 30 ) / 30)
        self.ProgressBar.set_fraction(new_value)
        self.OtpCode.set_label(totp.now())
        self.OtpCode.set_tooltip_text(config_data[SelectedLabel]['name'])
        return True
        
    def on_otp_changed(self, combo):
        global totp
        global config_data
        global SelectedLabel
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            SelectedLabel = model[tree_iter][0]
            totp = pyotp.TOTP(config_data[SelectedLabel]['genstring'])
    
    def on_otp_clicked(self,OtpCode):
        self.clipboard.set_text(self.OtpCode.get_label(), -1)

# MAIN

home = expanduser("~")

try:
    with open(home + '/.otp.yml', 'r') as file:
        config_data = yaml.safe_load(file)
except yaml.YAMLError as exc:
    print(f"Error in configuration file: {exc}")
    sys.exit(1)

SelectedLabel = list(config_data.keys())[0]
totp = pyotp.TOTP(config_data[SelectedLabel]['genstring'])
win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
