#!/bin/bash
set -e

INSTALL_DIR="$HOME/.local/share/window-transparency"
BIN_DIR="$HOME/.local/bin"
CONFIG_DIR="$HOME/.config/window-transparency"
AUTOSTART_DIR="$HOME/.config/autostart"

echo "Installing window-transparency..."

# Check dependencies
for cmd in xdotool xprop python3; do
    if ! command -v "$cmd" &>/dev/null; then
        echo "Error: '$cmd' is required but not installed."
        exit 1
    fi
done

# Check python gi module
if ! python3 -c "import gi" &>/dev/null; then
    echo "Error: python3-gi (PyGObject) is required."
    echo "Install with: sudo apt install python3-gi"
    exit 1
fi

# Copy source files
mkdir -p "$INSTALL_DIR"
cp -r src/* "$INSTALL_DIR/"

# Create launcher script
mkdir -p "$BIN_DIR"
cat > "$BIN_DIR/window-transparency" <<EOF
#!/bin/bash
cd "$INSTALL_DIR"
exec python3 main.py "\$@"
EOF
chmod +x "$BIN_DIR/window-transparency"

# Build config from default and ask for shortcut
mkdir -p "$CONFIG_DIR"
if [ ! -f "$CONFIG_DIR/config.ini" ]; then
    cp config/default.ini "$CONFIG_DIR/config.ini"
fi

# Ask for keyboard shortcut
echo ""
if python3 -c "import gi; gi.require_version('Keybinder','3.0'); from gi.repository import Keybinder" 2>/dev/null; then
    echo "Keyboard shortcut (optional)."
    echo "Format examples: <Ctrl><Alt>t   <Super>t   <Shift><Alt>o"
    read -p "Enter shortcut or leave empty to skip: " shortcut
    if [ -n "$shortcut" ]; then
        sed -i "s|^shortcut =.*|shortcut = $shortcut|" "$CONFIG_DIR/config.ini"
        echo "Shortcut set to: $shortcut"
    else
        echo "No shortcut set. You can add one later from the Settings menu."
    fi
else
    echo "Note: install 'gir1.2-keybinder-3.0' to enable keyboard shortcuts."
    echo "      sudo apt install gir1.2-keybinder-3.0"
fi

# Optional: add to autostart
echo ""
read -p "Add to autostart? [y/N] " answer
if [[ "$answer" =~ ^[Yy]$ ]]; then
    mkdir -p "$AUTOSTART_DIR"
    cat > "$AUTOSTART_DIR/window-transparency.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=Window Transparency
Exec=$BIN_DIR/window-transparency
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
EOF
    echo "Autostart entry created."
fi

echo ""
echo "Done! Run 'window-transparency' to start."
