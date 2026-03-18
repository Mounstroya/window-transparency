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

# Copy default config if not already present
if [ ! -f "$CONFIG_DIR/config.ini" ]; then
    mkdir -p "$CONFIG_DIR"
    cp config/default.ini "$CONFIG_DIR/config.ini"
    echo "Default config installed at $CONFIG_DIR/config.ini"
fi

# Optional: add to autostart
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

echo "Done! Run 'window-transparency' to start."
