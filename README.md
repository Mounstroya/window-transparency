# window-transparency

A lightweight system tray tool to control the transparency of the active window on X11.

## Features

- **Toggle transparency** with a single left click on the tray icon
- **Presets** (Light / Medium / Strong) accessible from the right-click menu
- **Custom opacity** dialog with a slider
- **Per-application rules** — save a default opacity level for each app
- **Settings panel** to configure default opacity and presets
- Config stored in `~/.config/window-transparency/config.ini`

## Requirements

- X11 display server
- `xdotool`
- `xprop`
- Python 3 with PyGObject (`python3-gi`)

Install dependencies on Debian/Ubuntu:

```bash
sudo apt install xdotool x11-utils python3-gi
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
4. Optionally add an autostart entry

## Usage

```bash
window-transparency
```

- **Left click** — toggle transparency on the active window
- **Right click** — open menu with presets, custom opacity, per-app rules, and settings

## Configuration

Edit `~/.config/window-transparency/config.ini`:

```ini
[general]
default_opacity = 85

[presets]
light = 90
medium = 80
strong = 70

[apps]
firefox = 90
xterm = 80
```

## Uninstall

```bash
bash uninstall.sh
```

## License

MIT
