# Adding New Things To Daedalus

> How to save new applications, scripts and customisations permanently.

---

# The Basic Idea

When I customise my computer, there are two versions:

## The working version

The thing actually running on my machine.

Examples:

```
~/.config/waybar/
~/.local/bin/weather-location
```

---

## The saved version

The copy stored in Git.

Example:

```
~/dotfiles/config/waybar/
~/dotfiles/bin/weather-location
```

The saved version is what allows me to rebuild Daedalus or create Achilles later.

---

# Adding A New Script

If I create a useful command:

Example:

```
~/.local/bin/my-new-script
```

Move it into:

```
~/dotfiles/bin/
```

Example:

```bash
cp ~/.local/bin/my-new-script ~/dotfiles/bin/
```

Make sure it can run:

```bash
chmod +x ~/dotfiles/bin/my-new-script
```

Then add it to the installer if needed.

---

# Adding A Configuration

Most Linux application settings live here:

```
~/.config/
```

Example:

I customise Waybar:

```
~/.config/waybar/
```

Copy it into:

```
~/dotfiles/config/waybar/
```

Example:

```bash
cp -r ~/.config/waybar ~/dotfiles/config/
```

---

# Using Symlinks

A symlink means two locations point to the same files.

Example:

```
~/.config/waybar
        |
        v
~/dotfiles/config/waybar
```

Changes are automatically shared.

This means I don't have to remember to copy files every time.

---

# Adding A New Application

When installing a new application:

Ask:

## Is this just an app?

Examples:

- Firefox
- Spotify
- Steam

Add it to:

```
packages/
```

---

## Does it have important settings?

Examples:

- editor configuration
- terminal settings
- desktop settings

Save its configuration in:

```
config/
```

---

## Is it a custom tool?

Examples:

- scripts
- automation
- helpers

Save it in:

```
bin/
```

---

# Updating The Installer

If a new thing needs to be recreated automatically:

Update:

```
install/install.sh
```

Examples:

- creating folders
- creating symlinks
- copying files
- enabling services

---

# Adding Packages

If I install something I want on future machines:

Find whether it is:

Pacman:

```
packages/pacman.txt
```

Flatpak:

```
packages/flatpak.txt
```

Add it to the correct list.

---

# After Adding Something

Always check:

```bash
cd ~/dotfiles

git status
```

Then:

```bash
git add .
```

Commit:

```bash
git commit -m "Add new customisation"
```

Push:

```bash
git push
```

---

# The Rule Of Thumb

If losing it would annoy me:

Save it.

If rebuilding a machine would require remembering it:

Document it.

If I spent an hour making it work:

Put it in Git.
