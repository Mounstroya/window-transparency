#!/bin/bash
set -e

VERSION="1.0.0"
PKG="window-transparency_${VERSION}"
BUILD_DIR="/tmp/${PKG}"

echo "Building .deb package v${VERSION}..."

# Clean previous build
rm -rf "$BUILD_DIR"

# Create directory structure
mkdir -p "$BUILD_DIR/DEBIAN"
mkdir -p "$BUILD_DIR/usr/share/window-transparency"
mkdir -p "$BUILD_DIR/usr/share/doc/window-transparency"

# Copy packaging metadata
cp debian/control "$BUILD_DIR/DEBIAN/control"
cp debian/postinst "$BUILD_DIR/DEBIAN/postinst"
cp debian/prerm    "$BUILD_DIR/DEBIAN/prerm"
chmod 755 "$BUILD_DIR/DEBIAN/postinst" "$BUILD_DIR/DEBIAN/prerm"

# Copy app files
cp src/*.py              "$BUILD_DIR/usr/share/window-transparency/"
cp config/default.ini    "$BUILD_DIR/usr/share/window-transparency/"
cp LICENSE               "$BUILD_DIR/usr/share/doc/window-transparency/copyright"

# Build
dpkg-deb --build "$BUILD_DIR" "${PKG}_all.deb"

echo ""
echo "Done: ${PKG}_all.deb"
echo "Install with: sudo dpkg -i ${PKG}_all.deb"
