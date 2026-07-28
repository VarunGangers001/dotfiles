#!/bin/bash

set -e

echo "Installing Daedalus dotfiles..."

mkdir -p ~/.local/bin
mkdir -p ~/.config/weather
mkdir -p ~/.local/share/omarchy/bin

cp ../bin/weather-location ~/.local/bin/
chmod +x ~/.local/bin/weather-location

cp ../config/weather/location ~/.config/weather/

cp ../omarchy/bin/omarchy-weather-icon \
~/.local/share/omarchy/bin/

cp ../omarchy/bin/omarchy-weather-status \
~/.local/share/omarchy/bin/

echo "Done."
