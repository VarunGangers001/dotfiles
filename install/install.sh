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

echo "Installing configuration files..."

mkdir -p "$HOME/.config"

for config in btop fastfetch git ghostty hypr omarchy walker waybar; do
    ln -sfn "$DOTFILES/config/$config" "$HOME/.config/$config"
done

ln -sfn "$DOTFILES/config/starship.toml" "$HOME/.config/starship.toml"

echo "Installing weather configuration..."

mkdir -p "$HOME/.config/weather"
cp "$DOTFILES/config/weather/location" "$HOME/.config/weather/"

echo "Done."
