#!/usr/bin/env python3
"""
window-transparency — Systray tool to manage active window opacity on X11.
"""

import sys
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from config import load_config
from tray import TransparencyTray


def main():
    config = load_config()
    TransparencyTray(config)
    Gtk.main()


if __name__ == "__main__":
    main()
