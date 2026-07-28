#!/bin/bash

set -e

DOTFILES="$HOME/dotfiles"

echo "Installing pacman packages..."

sudo pacman -S --needed - < "$DOTFILES/packages/pacman.txt"

echo "Installing Flatpak applications..."

while read -r app; do
    flatpak install -y flathub "$app"
done < "$DOTFILES/packages/flatpak.txt"

echo "Packages installed."

