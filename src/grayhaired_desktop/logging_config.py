"""Logging configuration for the desktop application."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

from PySide6.QtCore import QStandardPaths

from grayhaired_desktop.config import APP_ID

LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"


def configure_logging(debug: bool = False) -> Path:
    """Configure console and rotating-file friendly application logging."""
    level = logging.DEBUG if debug else logging.INFO
    log_dir = Path(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppLocalDataLocation))
    if not log_dir.as_posix().strip("/"):
        log_dir = Path.home() / ".local" / "state" / APP_ID
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "grayhaired-desktop.log"

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers.clear()

    formatter = logging.Formatter(LOG_FORMAT)
    stream_handler = logging.StreamHandler(sys.stderr)
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(level)

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    root_logger.addHandler(stream_handler)
    root_logger.addHandler(file_handler)
    logging.getLogger(__name__).debug("Logging initialized at %s", log_file)
    return log_file
