"""Typed QSettings access for persistent desktop preferences."""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import QByteArray, QSettings

from grayhaired_desktop.config import DEFAULT_WINDOW_HEIGHT, DEFAULT_WINDOW_WIDTH


@dataclass(slots=True)
class WindowDefaults:
    """Default dimensions used before a user has saved window state."""

    width: int = DEFAULT_WINDOW_WIDTH
    height: int = DEFAULT_WINDOW_HEIGHT


class SettingsStore:
    """Small object-oriented wrapper around Qt's platform-native QSettings."""

    GEOMETRY_KEY = "main_window/geometry"
    STATE_KEY = "main_window/state"

    def __init__(self, qsettings: QSettings | None = None) -> None:
        self._settings = qsettings or QSettings()

    def restore_geometry(self) -> QByteArray | None:
        """Return persisted main-window geometry, if available."""
        value = self._settings.value(self.GEOMETRY_KEY)
        return value if isinstance(value, QByteArray) and not value.isEmpty() else None

    def restore_state(self) -> QByteArray | None:
        """Return persisted main-window state, if available."""
        value = self._settings.value(self.STATE_KEY)
        return value if isinstance(value, QByteArray) and not value.isEmpty() else None

    def save_window(self, geometry: QByteArray, state: QByteArray) -> None:
        """Persist main-window geometry and state."""
        self._settings.setValue(self.GEOMETRY_KEY, geometry)
        self._settings.setValue(self.STATE_KEY, state)
        self._settings.sync()
