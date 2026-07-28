# Daedalus Workflow Guide

> If I've forgotten how this repository works, start here.

---

# What This Repository Does

This repository is the memory of my Linux setup.

Instead of relying on remembering commands, locations and settings, important parts of my system are stored here.

The idea:

```
Experiment → Customise → Save → Commit → Push
```

If something is important enough that I would hate losing it, it belongs here.

---

# The Basic Rule

My home folder:

```
~
```

is where things actually run.

This repository:

```
~/dotfiles
```

is where important things are stored permanently.

Some files are copied here.

Some files are linked here.

The repository is the version I trust.

---

# Repository Layout

## bin/

Location:

```
~/dotfiles/bin/
```

Contains custom commands and scripts.

Examples:

```
weather-location
weather-status
weather-icon
weather-waybar
```

If I create a useful command that I want on future machines, it belongs here.

---

## config/

Location:

```
~/dotfiles/config/
```

Contains application settings.

Examples:

```
hypr/
waybar/
ghostty/
walker/
fastfetch/
btop/
```

These are the settings that make my desktop feel like my own.

---

## packages/

Location:

```
~/dotfiles/packages/
```

Contains lists of installed applications.

Examples:

```
pacman.txt
flatpak.txt
```

These allow a future machine to install the same software.

---

## install/

Location:

```
~/dotfiles/install/
```

Contains setup scripts.

These automate rebuilding a machine.

---

## docs/

Location:

```
~/dotfiles/docs/
```

Contains explanations and notes.

If I learn something important, write it here.

---

# Daily Git Workflow

After making changes:

Check what changed:

```bash
cd ~/dotfiles
git status
```

Add changes:

```bash
git add .
```

Create a save point:

```bash
git commit -m "Describe what changed"
```

Upload to GitHub:

```bash
git push
```

---

# Getting Updates

If I change something from another machine:

```bash
git pull
```

This downloads the latest version.

---

# Looking At History

See previous changes:

```bash
git log --oneline
```

This shows the evolution of the setup.

---

# If Something Goes Wrong

Check what changed:

```bash
git status
```

See previous versions:

```bash
git log --oneline
```

Restore a file:

```bash
git restore filename
```

The Git repository exists so experimenting is safe.

---

# Adding A New Customisation

When I customise something:

Ask:

> "Would I want this on Achilles?"

If yes:

1. Find where the configuration lives.
2. Copy or link it into this repository.
3. Update installation scripts if needed.
4. Commit the change.

---

# Before Major Changes

Before:

- major Omarchy updates
- changing important configs
- reinstalling Linux

Do:

```bash
cd ~/dotfiles
git status
git add .
git commit -m "Backup before changes"
git push
```

---

# Future Machine Setup

For a new computer:

1. Install Omarchy.
2. Clone this repository.
3. Install packages.
4. Run setup scripts.
5. Restore configuration.
6. Continue customising.

The goal is not to perfectly copy a machine.

The goal is to recreate my workflow.
