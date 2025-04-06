import os
import pathlib
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango
from ks_includes.screen_panel import ScreenPanel

class Panel(ScreenPanel):
    def __init__(self, screen, title):
        title = title or _("About")
        super().__init__(screen, title)

        self.create_qrcode_display()

    def create_qrcode_display(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_vexpand(True)
        vbox.set_valign(Gtk.Align.CENTER)
        vbox.set_hexpand(True)
        vbox.set_halign(Gtk.Align.CENTER)

        klipperscreendir = pathlib.Path(__file__).parent.parent.resolve()
        image_path = os.path.join(klipperscreendir, "styles", "qrcode.png")
        image = Gtk.Image.new_from_file(image_path)
        vbox.pack_start(image, False, False, 10)

        text_label = Gtk.Label()
        name = _("Scan this QR Code to access the Wiki")
        text_label.set_markup(f"<big>{name}</big>")
        text_label.set_justify(Gtk.Justification.CENTER)
        text_label.set_halign(Gtk.Align.CENTER)
        text_label.set_valign(Gtk.Align.CENTER)
        vbox.pack_start(text_label, False, False, 10)

        self.content.add(vbox)
