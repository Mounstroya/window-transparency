# window-transparency

A lightweight system tray tool to control the transparency of the active window on X11.

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
- Python 3 with PyGObject (`python3-gi`)
- `gir1.2-keybinder-3.0` *(optional, recommended — enables keyboard shortcuts)*

Install dependencies on Debian/Ubuntu:

```bash
sudo apt install xdotool x11-utils python3-gi
```

For keyboard shortcut support (recommended):

```bash
sudo apt install gir1.2-keybinder-3.0
```

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/window-transparency.git
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

```bash
bash uninstall.sh
```

## License

MIT
