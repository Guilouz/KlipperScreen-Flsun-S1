import logging
import subprocess
import os
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from ks_includes.screen_panel import ScreenPanel

class Panel(ScreenPanel):
    def __init__(self, screen, title):
        title = title or _("Brightness")
        super().__init__(screen, title)

        self.brightness_command = self._screen._config.get_main_config().get('brightness_command')
        self.brightness = 0
        self.min_brightness = 5
        self.max_brightness = 255

        backlight_devices = os.listdir("/sys/class/backlight/")
        logging.debug(f"Backlights: {backlight_devices}")

        if not self.brightness_command and not backlight_devices:
            self._screen.show_popup_message(_("Backlight not configured"), level=3)
            self.back()
            return

        if not self.brightness_command:
            device = backlight_devices[0] if backlight_devices else None
            brightness_path = f"/sys/class/backlight/{device}/brightness"
            max_brightness_path = f"/sys/class/backlight/{device}/max_brightness"
            min_brightness_path = f"/sys/class/backlight/{device}/min_brightness"
            self.brightness_command = f"echo {{value}} >{brightness_path}"
            try:
                self.max_brightness = int(subprocess.check_output(f"cat {max_brightness_path}", shell=True).strip())
            except Exception as e:
                logging.warning(f"Could not read max brightness: {e}")
            try:
                self.min_brightness = int(subprocess.check_output(f"cat {min_brightness_path}", shell=True).strip())
            except Exception as e:
                logging.warning(f"Could not read min brightness: {e}")
            try:
                self.brightness = int(subprocess.check_output(f"cat {brightness_path}", shell=True).strip())
            except Exception as e:
                logging.warning(f"Could not read current brightness: {e}")

        self.create_brightness_control()

    def create_brightness_control(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_vexpand(True)
        vbox.set_valign(Gtk.Align.CENTER)
        vbox.set_hexpand(True)

        name = _("Brightness")
        title_label = Gtk.Label()
        title_label.set_markup(f"\n<big><b>{name}</b></big>\n")
        title_label.set_justify(Gtk.Justification.CENTER)
        title_label.set_halign(Gtk.Align.CENTER)
        vbox.pack_start(title_label, False, False, 10)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)

        min_btn = self._gtk.Button("arrow-down", _("Min"), "color1")
        min_btn.set_hexpand(False)
        min_btn.connect("clicked", self.on_min_button_clicked)
        hbox.pack_start(min_btn, False, False, 0)

        step_increment = (self.max_brightness - self.min_brightness) / 32
        adj = Gtk.Adjustment(self.brightness, self.min_brightness, self.max_brightness, step_increment)

        self.scale = Gtk.Scale(adjustment=adj, digits=0, hexpand=True, valign=Gtk.Align.CENTER, has_origin=True)
        self.scale.get_style_context().add_class("option_slider")
        self.scale.connect("value-changed", self.change_brightness)

        max_btn = self._gtk.Button("arrow-up", _("Max"), "color2")
        max_btn.set_hexpand(False)
        max_btn.connect("clicked", self.on_max_button_clicked)
        hbox.pack_start(self.scale, True, True, 0)
        hbox.pack_start(max_btn, False, False, 0)

        vbox.pack_start(hbox, True, True, 0)
        self.content.add(vbox)

    def change_brightness(self, widget):
        value = widget.get_value()
        self.set_brightness(value)

    def on_min_button_clicked(self, button):
        self.set_brightness(self.min_brightness)

    def on_max_button_clicked(self, button):
        self.set_brightness(self.max_brightness)

    def set_brightness(self, value):
        value = int(value)
        bash_command = self.brightness_command.format(value=value)
        try:
            subprocess.run(bash_command, shell=True, check=True)
            logging.info(f"Brightness set to {value}")
            if self.scale:
                self.scale.set_value(value)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error setting brightness: {e}")
            self._screen.show_popup_message(_("Failed to set brightness"), level=3)
