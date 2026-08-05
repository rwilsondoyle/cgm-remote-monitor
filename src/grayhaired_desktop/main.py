"""Command-line entry point for GrayHaired Desktop."""

from __future__ import annotations

import argparse
import logging
import sys
from importlib import resources

from PySide6.QtCore import QCoreApplication, QSettings, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from grayhaired_desktop.config import APP_ID, APP_NAME, APP_VERSION, ORGANIZATION_DOMAIN, ORGANIZATION_NAME
from grayhaired_desktop.logging_config import configure_logging
from grayhaired_desktop.settings import SettingsStore
from grayhaired_desktop.window import MainWindow

LOGGER = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(description="Launch GrayHaired Desktop.")
    parser.add_argument("--debug", action="store_true", help="Enable verbose debug logging.")
    return parser


def create_application(argv: list[str]) -> QApplication:
    """Create and identify the Qt application object."""
    QCoreApplication.setOrganizationName(ORGANIZATION_NAME)
    QCoreApplication.setOrganizationDomain(ORGANIZATION_DOMAIN)
    QCoreApplication.setApplicationName(APP_NAME)
    QCoreApplication.setApplicationVersion(APP_VERSION)
    QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeMenuBar, False)
    app = QApplication(argv)
    app.setDesktopFileName(APP_ID)
    app.setWindowIcon(load_icon())
    return app


def load_icon() -> QIcon:
    """Load the bundled SVG application icon."""
    icon_path = resources.files("grayhaired_desktop.resources").joinpath("grayhaired-desktop.svg")
    return QIcon(str(icon_path))


def main(argv: list[str] | None = None) -> int:
    """Run GrayHaired Desktop and return the process exit code."""
    args = build_parser().parse_args(argv)
    log_file = configure_logging(debug=args.debug)
    LOGGER.info("Starting %s %s; log file: %s", APP_NAME, APP_VERSION, log_file)
    app = create_application(sys.argv if argv is None else [sys.argv[0], *argv])
    window = MainWindow(SettingsStore(QSettings()), app.windowIcon())
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
