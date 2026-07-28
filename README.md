# Daedalus Dotfiles

Personal configuration repository for my Omarchy Linux setup.

This repository contains my custom scripts, application configurations, package lists, and system tweaks so that my Linux environment can be recreated on future machines.

The primary goal is to make moving from **Daedalus** (current laptop) to future machines such as **Achilles** (desktop PC) simple and repeatable.

---

# Repository Structure

```
dotfiles/
│
├── bin/
│   ├── weather-location
│   ├── weather-icon
│   ├── weather-status
│   ├── weather-waybar
│   │
│   └── omarchy/
│       └── omarchy-battery-monitor
│
├── config/
│   ├── btop/
│   ├── fastfetch/
│   ├── git/
│   ├── ghostty/
│   ├── hypr/
│   ├── walker/
│   ├── waybar/
│   └── starship.toml
│
├── packages/
│   ├── pacman.txt
│   └── flatpak.txt
│
├── install/
│   ├── install.sh
│   └── packages.sh
│
└── README.md
```

---

# Installation

## 1. Install Omarchy

Install a fresh Omarchy Linux system.

---

## 2. Clone this repository

```bash
git clone https://github.com/VarunGangers001/dotfiles.git ~/dotfiles
cd ~/dotfiles
```

---

## 3. Install packages

Run:

```bash
./install/packages.sh
```

This installs the required Pacman and Flatpak applications stored in:

```
packages/
```

---

## 4. Install configuration

Run:

```bash
./install/install.sh
```

This will:

- install custom scripts
- create required directories
- create symbolic links for tracked configurations
- restore weather configuration
- restore Omarchy custom scripts

---

# Custom Features

## Weather System

A custom location-based weather system.

Commands:

```bash
weather-location <city>
```

Example:

```bash
weather-location Hyderabad
```

This updates the current weather location.

The system provides:

- Waybar weather module
- weather status command
- weather icons
- location persistence

Scripts:

```
bin/weather-location
bin/weather-status
bin/weather-icon
bin/weather-waybar
```

---

# Battery Monitor

Customised Omarchy battery warning system.

Location:

```
bin/omarchy/omarchy-battery-monitor
```

Features:

- checks battery level automatically
- warns when battery is low
- integrates with Omarchy notifications
- runs through a systemd user timer

The service and timer are provided by Omarchy:

```
~/.config/systemd/user/

omarchy-battery-monitor.service
omarchy-battery-monitor.timer
```

---

# Configuration Management

Tracked configurations are stored in:

```
config/
```

and restored using symbolic links.

This means changes made in:

```
~/.config/
```

are actually changes inside this repository.

Tracked applications include:

- Hyprland
- Waybar
- Ghostty
- Walker
- Fastfetch
- btop
- Git
- Starship

---

# Updating The Repository

After making changes:

```bash
cd ~/dotfiles

git status

git add .

git commit -m "Describe changes"

git push
```

---

# Adding A New Configuration

To track a new configuration:

1. Copy it into `config/`

Example:

```bash
cp -r ~/.config/example ~/dotfiles/config/
```

2. Add a symlink entry inside:

```
install/install.sh
```

3. Commit the changes.

---

# Device Setup

## Daedalus

Current laptop.

Runs:

- Omarchy Linux
- Hyprland
- custom scripts
- tracked configurations from this repository

---

## Achilles

Future desktop PC.

The intended setup process:

1. Install Omarchy
2. Clone this repository
3. Run installation scripts
4. Restore the same workflow

---

# Notes

This repository intentionally does not manage Omarchy's core configuration directly.

Omarchy updates should remain responsible for:

```
~/.config/omarchy
```

while this repository manages personal customisations and additions.

---

# Future Improvements

Possible additions:

- more automated setup scripts
- NVIDIA/DaVinci Resolve setup notes
- backup automation
- additional systemd services
- further Hyprland customisation
