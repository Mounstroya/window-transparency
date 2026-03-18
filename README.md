# window-transparency

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org)
[![Platform](https://img.shields.io/badge/platform-X11%20%2F%20Linux-lightgrey.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A lightweight system tray tool to control the transparency of the active window on X11.

<!-- Demo GIF — replace with your own recording -->
<!-- ![demo](assets/demo.gif) -->

## Features

- **Toggle transparency** with a single left click on the tray icon
- **Presets** (Light / Medium / Strong) accessible from the right-click menu
- **Custom opacity** dialog with a slider
- **Per-application rules** — save a default opacity level for each app
- **Settings panel** to configure default opacity and presets
- **Global keyboard shortcut** to toggle transparency without touching the mouse (optional)
- Config stored in `~/.config/window-transparency/config.ini`

## Requirements

- X11 display server
- `xdotool`
- `xprop`
- Python 3.8+ with PyGObject (`python3-gi`)
- `gir1.2-keybinder-3.0` *(optional, recommended — enables keyboard shortcuts)*

> **Wayland:** not supported. This tool relies on `xprop` and `xdotool`, which are X11-only.
> Wayland support is not planned for now, but contributions are welcome.

Install dependencies on Debian/Ubuntu:

```bash
sudo apt install xdotool x11-utils python3-gi
```

For keyboard shortcut support (recommended):

```bash
sudo apt install gir1.2-keybinder-3.0
```

> **Without keybinder:** the app works normally — toggle, presets, and all menus function as usual.
> The only feature that won't be available is the global keyboard shortcut.
> No errors or warnings will appear; the shortcut option in Settings will simply show a notice.

## Installation

### Option A — .deb package (Debian/Ubuntu, recommended)

Download the latest `.deb` from the [Releases](https://github.com/Mounstroya/window-transparency/releases) page and install it:

```bash
sudo dpkg -i window-transparency_*.deb
sudo apt-get install -f   # fix any missing dependencies
```

### Option B — Manual install

```bash
git clone https://github.com/Mounstroya/window-transparency.git
cd window-transparency
bash install.sh
```

The installer will:
1. Copy files to `~/.local/share/window-transparency/`
2. Create a launcher at `~/.local/bin/window-transparency`
3. Copy default config to `~/.config/window-transparency/config.ini`
4. Ask for a keyboard shortcut (if `keybinder` is available)
5. Optionally add an autostart entry

## Usage

```bash
window-transparency
```

- **Left click** — toggle transparency on the active window
- **Right click** — open menu with presets, custom opacity, per-app rules, and settings
- **Keyboard shortcut** — toggle transparency without leaving the keyboard (configure in Settings)

## Configuration

Edit `~/.config/window-transparency/config.ini`:

```ini
[general]
default_opacity = 85
shortcut = <Ctrl><Alt>t

[presets]
light = 90
medium = 80
strong = 70

[apps]
firefox = 90
xterm = 80
```

The shortcut format follows GTK syntax: `<Ctrl>`, `<Alt>`, `<Shift>`, `<Super>` followed by a key.
No shortcut is set by default to avoid conflicts — set one during installation or from the Settings menu.

## Uninstall

### If installed via .deb

```bash
sudo dpkg -r window-transparency
```

### If installed manually

```bash
bash uninstall.sh
```

## License

MIT
