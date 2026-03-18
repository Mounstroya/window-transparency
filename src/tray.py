import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

from transparency import (
    get_active_window_id,
    get_window_class,
    toggle_opacity,
    set_window_opacity,
    get_window_opacity,
)
from config import (
    get_default_opacity,
    get_presets,
    get_app_opacity,
    set_app_opacity,
    set_default_opacity,
    save_config,
)


class TransparencyTray:
    def __init__(self, config):
        self.config = config
        self.icon = Gtk.StatusIcon()
        self.icon.set_from_icon_name("view-fullscreen")
        self.icon.set_tooltip_text("Window Transparency")
        self.icon.connect("activate", self.on_left_click)
        self.icon.connect("popup-menu", self.on_right_click)
        self.icon.set_visible(True)

    def on_left_click(self, icon):
        """Left click: toggle transparency on active window."""
        try:
            window_id = get_active_window_id()
            app_name = get_window_class(window_id)
            opacity = (
                get_app_opacity(self.config, app_name)
                if app_name
                else None
            ) or get_default_opacity(self.config)
            new_opacity = toggle_opacity(window_id, opacity)
            self.icon.set_tooltip_text(
                f"Window Transparency — {app_name or 'unknown'}: {new_opacity}%"
            )
        except RuntimeError as e:
            self._show_error(str(e))

    def on_right_click(self, icon, button, time):
        menu = Gtk.Menu()

        # --- Apply preset section ---
        presets = get_presets(self.config)
        for name, value in presets.items():
            item = Gtk.MenuItem(label=f"{name.capitalize()} ({value}%)")
            item.connect("activate", self._apply_preset, value)
            menu.append(item)

        menu.append(Gtk.SeparatorMenuItem())

        # --- Custom opacity ---
        custom_item = Gtk.MenuItem(label="Custom opacity...")
        custom_item.connect("activate", self._custom_opacity_dialog)
        menu.append(custom_item)

        menu.append(Gtk.SeparatorMenuItem())

        # --- Per-app rule ---
        app_item = Gtk.MenuItem(label="Save rule for this app...")
        app_item.connect("activate", self._save_app_rule)
        menu.append(app_item)

        # --- Settings ---
        settings_item = Gtk.MenuItem(label="Settings...")
        settings_item.connect("activate", self._open_settings)
        menu.append(settings_item)

        menu.append(Gtk.SeparatorMenuItem())

        # --- Quit ---
        quit_item = Gtk.MenuItem(label="Quit")
        quit_item.connect("activate", Gtk.main_quit)
        menu.append(quit_item)

        menu.show_all()
        menu.popup(None, None, None, None, button, time)

    def _apply_preset(self, item, percent):
        try:
            window_id = get_active_window_id()
            set_window_opacity(window_id, percent)
        except RuntimeError as e:
            self._show_error(str(e))

    def _custom_opacity_dialog(self, item):
        dialog = Gtk.Dialog(
            title="Custom Opacity",
            flags=Gtk.DialogFlags.MODAL,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK,
        )
        box = dialog.get_content_area()
        box.set_spacing(8)
        box.set_margin_top(12)
        box.set_margin_bottom(12)
        box.set_margin_start(12)
        box.set_margin_end(12)

        label = Gtk.Label(label="Opacity (1–100):")
        box.add(label)

        try:
            window_id = get_active_window_id()
            current = get_window_opacity(window_id)
        except RuntimeError:
            current = get_default_opacity(self.config)

        adjustment = Gtk.Adjustment(
            value=current, lower=1, upper=100,
            step_increment=1, page_increment=5
        )
        scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=adjustment)
        scale.set_size_request(250, -1)
        scale.set_digits(0)
        box.add(scale)

        dialog.show_all()
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            value = int(scale.get_value())
            try:
                window_id = get_active_window_id()
                set_window_opacity(window_id, value)
            except RuntimeError as e:
                self._show_error(str(e))
        dialog.destroy()

    def _save_app_rule(self, item):
        try:
            window_id = get_active_window_id()
            app_name = get_window_class(window_id)
            current = get_window_opacity(window_id)
        except RuntimeError as e:
            self._show_error(str(e))
            return

        if not app_name:
            self._show_error("Could not detect application name.")
            return

        dialog = Gtk.Dialog(
            title=f"Rule for '{app_name}'",
            flags=Gtk.DialogFlags.MODAL,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK,
        )
        box = dialog.get_content_area()
        box.set_spacing(8)
        box.set_margin_top(12)
        box.set_margin_bottom(12)
        box.set_margin_start(12)
        box.set_margin_end(12)

        label = Gtk.Label(label=f"Default opacity for {app_name} (1–100):")
        box.add(label)

        adjustment = Gtk.Adjustment(
            value=current, lower=1, upper=100,
            step_increment=1, page_increment=5
        )
        scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=adjustment)
        scale.set_size_request(250, -1)
        scale.set_digits(0)
        box.add(scale)

        dialog.show_all()
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            value = int(scale.get_value())
            set_app_opacity(self.config, app_name, value)
        dialog.destroy()

    def _open_settings(self, item):
        default_opacity = get_default_opacity(self.config)
        presets = get_presets(self.config)

        dialog = Gtk.Dialog(title="Settings", flags=Gtk.DialogFlags.MODAL)
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK,
        )
        box = dialog.get_content_area()
        box.set_spacing(10)
        box.set_margin_top(12)
        box.set_margin_bottom(12)
        box.set_margin_start(12)
        box.set_margin_end(12)

        # Default opacity
        box.add(Gtk.Label(label="Default opacity (%):"))
        adj_default = Gtk.Adjustment(
            value=default_opacity, lower=1, upper=100,
            step_increment=1, page_increment=5
        )
        scale_default = Gtk.Scale(
            orientation=Gtk.Orientation.HORIZONTAL, adjustment=adj_default
        )
        scale_default.set_size_request(300, -1)
        scale_default.set_digits(0)
        box.add(scale_default)

        box.add(Gtk.Separator())

        # Presets
        preset_scales = {}
        for name, value in presets.items():
            box.add(Gtk.Label(label=f"Preset '{name.capitalize()}' (%):"))
            adj = Gtk.Adjustment(
                value=value, lower=1, upper=100,
                step_increment=1, page_increment=5
            )
            scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=adj)
            scale.set_size_request(300, -1)
            scale.set_digits(0)
            box.add(scale)
            preset_scales[name] = scale

        dialog.show_all()
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            set_default_opacity(self.config, int(scale_default.get_value()))
            for name, scale in preset_scales.items():
                self.config["presets"][name] = str(int(scale.get_value()))
            save_config(self.config)
        dialog.destroy()

    def _show_error(self, message):
        dialog = Gtk.MessageDialog(
            flags=Gtk.DialogFlags.MODAL,
            type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            message_format=message,
        )
        dialog.run()
        dialog.destroy()
