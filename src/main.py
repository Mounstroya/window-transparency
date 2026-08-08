#!/usr/bin/env python3
"""
window-transparency — Systray tool to manage active window opacity on X11.
"""

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # noqa: E402

from config import load_config  # noqa: E402
from tray import TransparencyTray  # noqa: E402


def main():
    config = load_config()
    TransparencyTray(config)
    Gtk.main()


if __name__ == "__main__":
    main()
