# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

otpgui is a GTK3-based TOTP (Time-based One-Time Password) generator for GNU/Linux. It provides both a graphical interface and CLI/script mode for generating 2FA codes, serving as a desktop alternative to mobile authenticator apps.

## Development Commands

```bash
# Install dependencies
poetry install

# Run the application
poetry run otpgui

# Run tests
poetry run pytest

# Code formatting
poetry run black .
poetry run isort .

# Linting
poetry run flake8
```

## Building Packages

The project uses Docker containers for building distribution packages:

```bash
# Build Python wheel
make python

# Build Debian package (requires Docker)
make deb

# Build Arch Linux package (requires Docker)
make arch
```

## Code Style

- Line length: 200 characters
- Formatter: black with isort (black-compatible profile)
- Linter: flake8 (max complexity: 15)

## Architecture

The codebase consists of two main modules:

- **otpgui.py**: Core application logic
  - `OtpSettings`: Manages settings from `~/.config/otpgui/settings.yml`
  - `OtpStore`: Handles OTP configuration, decryption (plain/SOPS), and TOTP code generation via pyotp
  - `main()`: CLI argument parsing and interface dispatch

- **otpgtk.py**: GTK3 GUI implementation
  - `MyWindow`: Main window with OTP code button, progress bar (30-second countdown), and account selector dropdown
  - Auto-refreshes every 1000ms via `GLib.timeout_add`
  - Click-to-copy clipboard integration

The GTK interface is lazily imported only when `--interface gtk` is used (default), allowing script mode to run without GTK dependencies being loaded.

## Configuration

OTP secrets are stored in YAML format with optional SOPS encryption:

```yaml
otp:
  label:
    name: "tooltip description"
    genstring: "BASE32SECRET"
```
