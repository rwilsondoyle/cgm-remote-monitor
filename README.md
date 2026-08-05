# GrayHaired Desktop

GrayHaired Desktop is a production-ready Linux desktop wrapper for the GrayHaired web experience at <https://grayhaired.tech/desktop-c/>. It embeds the site with PySide6 QtWebEngine and does **not** use Electron, an external Chromium binary, or a separate browser process controlled by the application.

## Milestone 1 features

- Python 3.12+ package with a `src/` layout.
- PySide6 and QtWebEngine embedded browser.
- Modular object-oriented architecture for the application entry point, main window, browser, logging, and settings.
- Persistent settings using `QSettings` for native desktop window geometry and state.
- Console and file logging for startup, navigation, and page-load diagnostics.
- Bundled SVG application icon.
- Linux desktop launcher metadata.
- `pyproject.toml` with a `grayhaired-desktop` console entry point.

## Requirements

- Linux desktop environment with Qt-supported display stack.
- Python 3.12 or newer.
- System libraries required by QtWebEngine for your distribution.

## Installation for development

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

## Running

```bash
grayhaired-desktop
```

For verbose diagnostics:

```bash
grayhaired-desktop --debug
```

The application opens <https://grayhaired.tech/desktop-c/> in a QtWebEngine view. Cookies, HTTP cache, local storage, and window placement are persisted through Qt platform services.

## Linux desktop integration

A starter desktop entry is provided at `packaging/linux/tech.grayhaired.desktop.desktop`. After installing the package, copy it to a desktop entry directory such as `~/.local/share/applications/` and adjust `Icon=` if your packaging system installs the icon to a theme path.

## Project layout

```text
src/grayhaired_desktop/
  browser.py          QtWebEngine page and browser view
  config.py           Application constants
  logging_config.py   Logging setup
  main.py             CLI and Qt application bootstrap
  settings.py         QSettings wrapper
  window.py           Main desktop window
  resources/          Bundled application assets
packaging/linux/      Desktop integration files
```

## Packaging notes

The project is intentionally standard Python packaging. Linux distributors can build a wheel from `pyproject.toml`, install the `grayhaired-desktop` entry point, install the SVG icon into an icon theme, and install the desktop entry under the application ID `tech.grayhaired.desktop`.
