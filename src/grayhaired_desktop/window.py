"""Main window for GrayHaired Desktop."""

from __future__ import annotations

import logging

from PySide6.QtGui import QCloseEvent, QIcon
from PySide6.QtWidgets import QMainWindow, QStatusBar

from grayhaired_desktop.browser import BrowserView
from grayhaired_desktop.config import APP_NAME, DEFAULT_WINDOW_HEIGHT, DEFAULT_WINDOW_WIDTH, HOME_URL
from grayhaired_desktop.settings import SettingsStore

LOGGER = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Top-level application window hosting the embedded QtWebEngine browser."""

    def __init__(self, settings: SettingsStore, icon: QIcon, parent=None) -> None:
        super().__init__(parent)
        self._settings = settings
        self._browser = BrowserView(HOME_URL, self)

        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(icon)
        self.setCentralWidget(self._browser)
        self.setStatusBar(QStatusBar(self))
        self.addToolBar(self._browser.create_navigation_toolbar(self))
        self._restore_window_state()
        self._browser.titleChanged.connect(self._update_title)
        self._browser.load_home()

    def closeEvent(self, event: QCloseEvent) -> None:
        """Persist window state before the application exits."""
        self._settings.save_window(self.saveGeometry(), self.saveState())
        LOGGER.info("Saved main window geometry and state")
        super().closeEvent(event)

    def _restore_window_state(self) -> None:
        """Restore persisted state or fall back to sensible desktop defaults."""
        geometry = self._settings.restore_geometry()
        state = self._settings.restore_state()
        if geometry and self.restoreGeometry(geometry):
            LOGGER.debug("Restored main window geometry")
        else:
            self.resize(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)
        if state:
            self.restoreState(state)

    def _update_title(self, title: str) -> None:
        """Include the web page title in the desktop title bar."""
        self.setWindowTitle(f"{title} - {APP_NAME}" if title else APP_NAME)
