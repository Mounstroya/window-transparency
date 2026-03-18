#!/bin/bash
set -e

INSTALL_DIR="$HOME/.local/share/window-transparency"
BIN="$HOME/.local/bin/window-transparency"
AUTOSTART="$HOME/.config/autostart/window-transparency.desktop"

echo "Uninstalling window-transparency..."

rm -rf "$INSTALL_DIR"
rm -f "$BIN"
rm -f "$AUTOSTART"

read -p "Remove config (~/.config/window-transparency)? [y/N] " answer
if [[ "$answer" =~ ^[Yy]$ ]]; then
    rm -rf "$HOME/.config/window-transparency"
    echo "Config removed."
fi

echo "Done."
