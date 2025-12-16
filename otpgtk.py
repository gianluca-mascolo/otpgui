import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gdk,Gtk,GObject,GLib

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
