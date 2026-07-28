# Rebuilding A Machine

> The guide for recreating my Linux environment on a new computer.

---

# Goal

The purpose of this guide is not to create an identical copy of a machine.

The goal is to recreate my workflow.

A fresh machine should eventually become:

- comfortable to use
- familiar
- productive
- customised to my needs

---

# Before Starting

Make sure:

- I have access to my GitHub account.
- Important files are backed up.
- This repository is up to date.

On the old machine:

```bash
cd ~/dotfiles

git status

git add .
git commit -m "Final backup before rebuild"

git push
```

---

# Step 1 - Install Omarchy

Install a fresh Omarchy Linux system.

Complete the normal installation process.

At this point the system will be a clean default installation.

---

# Step 2 - Install Git

Make sure Git is available:

```bash
git --version
```

If needed:

```bash
sudo pacman -S git
```

---

# Step 3 - Clone This Repository

Clone the repository:

```bash
git clone https://github.com/VarunGangers001/dotfiles.git ~/dotfiles
```

Enter it:

```bash
cd ~/dotfiles
```

---

# Step 4 - Install Applications

Install packages from:

```
packages/
```

Run:

```bash
./install/packages.sh
```

This installs:

- Pacman applications
- Flatpak applications

---

# Step 5 - Restore Configuration

Run:

```bash
./install/install.sh
```

This restores:

- custom scripts
- configuration files
- symlinks
- personal tools

---

# Step 6 - Check Everything

Test important parts:

## Terminal

Check:

- shell setup
- aliases
- terminal appearance

---

## Desktop

Check:

- Hyprland
- Waybar
- Walker
- notifications

---

## Custom Scripts

Test:

```bash
weather-location Hyderabad
```

Check:

- weather display
- timezone
- notifications

---

# Step 7 - Install Remaining Software

Some software may require manual setup.

Examples:

- DaVinci Resolve
- NVIDIA drivers
- creative software
- development tools

These should eventually be documented or automated.

---

# Step 8 - Personal Files

Restore:

- documents
- projects
- media
- creative files

Do not store large personal files inside this repository.

This repository stores the environment, not personal data.

---

# After Setup

Make a first backup:

```bash
cd ~/dotfiles

git status

git add .

git commit -m "Initial setup on new machine"

git push
```

---

# Achilles Setup

When building Achilles:

The intended process:

1. Install Omarchy.
2. Clone this repository.
3. Install packages.
4. Run setup scripts.
5. Install GPU/creative software.
6. Fine tune hardware-specific settings.
7. Document improvements.

---

# Things That Still Need Improving

Future improvements:

- fully automate application installation
- automate DaVinci Resolve setup
- document NVIDIA configuration
- add hardware-specific setup notes
- create a backup strategy

---

# Final Reminder

The repository is the memory of the machine.

The machine can change.

The workflow should stay.
