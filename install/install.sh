#!/bin/bash

set -e

echo "Installing Daedalus dotfiles..."

DOTFILES="$HOME/dotfiles"

mkdir -p "$HOME/.local/bin"
mkdir -p "$HOME/.config/weather"

echo "Installing weather scripts..."

for script in weather-location weather-icon weather-status weather-waybar; do
    ln -sf "$DOTFILES/bin/$script" "$HOME/.local/bin/$script"
done

chmod +x "$DOTFILES/bin/"*

echo "Installing weather configuration..."

cp "$DOTFILES/config/weather/location" "$HOME/.config/weather/"

echo "Done."

