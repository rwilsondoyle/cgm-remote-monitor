"""Embedded browser widgets for GrayHaired Desktop."""

from __future__ import annotations

import logging

from PySide6.QtCore import QUrl, Slot
from PySide6.QtGui import QAction
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile, QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QToolBar

LOGGER = logging.getLogger(__name__)


class BrowserPage(QWebEnginePage):
    """Application web page that logs navigation and JavaScript console events."""

    def javaScriptConsoleMessage(
        self,
        level: QWebEnginePage.JavaScriptConsoleMessageLevel,
        message: str,
        line_number: int,
        source_id: str,
    ) -> None:
        """Forward web content console messages to Python logging."""
        LOGGER.debug("Web console %s at %s:%s: %s", level.name, source_id, line_number, message)


class BrowserView(QWebEngineView):
    """QtWebEngine view configured for the GrayHaired web application."""

    def __init__(self, home_url: str, parent=None) -> None:
        super().__init__(parent)
        self._home_url = QUrl(home_url)
        self.setPage(BrowserPage(QWebEngineProfile.defaultProfile(), self))
        self._configure_settings()
        self.loadStarted.connect(self._on_load_started)
        self.loadFinished.connect(self._on_load_finished)

    def load_home(self) -> None:
        """Load the configured GrayHaired Desktop entry point."""
        self.load(self._home_url)

    def create_navigation_toolbar(self, parent) -> QToolBar:
        """Create a simple desktop browser toolbar."""
        toolbar = QToolBar("Navigation", parent)
        toolbar.setMovable(False)

        back_action = QAction("Back", toolbar)
        back_action.triggered.connect(self.back)
        toolbar.addAction(back_action)

        forward_action = QAction("Forward", toolbar)
        forward_action.triggered.connect(self.forward)
        toolbar.addAction(forward_action)

        reload_action = QAction("Reload", toolbar)
        reload_action.triggered.connect(self.reload)
        toolbar.addAction(reload_action)

        home_action = QAction("Home", toolbar)
        home_action.triggered.connect(self.load_home)
        toolbar.addAction(home_action)

        return toolbar

    def _configure_settings(self) -> None:
        """Apply production-friendly QtWebEngine settings."""
        settings = self.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, False)
        profile = self.page().profile()
        profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.DiskHttpCache)
        profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)

    @Slot()
    def _on_load_started(self) -> None:
        """Log the beginning of a page load."""
        LOGGER.info("Loading %s", self.url().toString() or self._home_url.toString())

    @Slot(bool)
    def _on_load_finished(self, ok: bool) -> None:
        """Log the result of a page load."""
        if ok:
            LOGGER.info("Loaded %s", self.url().toString())
        else:
            LOGGER.error("Failed to load %s", self.url().toString())
