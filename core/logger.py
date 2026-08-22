"""
AI Creator OS - Unified Logging Facility
Writes structured logs with timestamps and severity levels (INFO, WARNING, ERROR, SUCCESS)
to both Google Drive persistent logs and terminal stdout.
"""
import os
import sys
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional


class CreatorLogger:
    """Unified logger ensuring logs are mirrored to Google Drive."""

    def __init__(self, module_name: str, log_dir: Optional[str] = None):
        self.module_name = module_name
        if not log_dir:
            if os.path.exists("/content/drive/MyDrive/AI_Creator_OS/logs"):
                log_dir = "/content/drive/MyDrive/AI_Creator_OS/logs"
            else:
                log_dir = "./logs"

        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / f"{module_name}.log"

        self.logger = logging.getLogger(f"AI_Creator_OS.{module_name}")
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:
            # File handler
            fh = logging.FileHandler(self.log_file, encoding="utf-8")
            fh.setLevel(logging.INFO)
            formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

    def info(self, msg: str) -> None:
        self.logger.info(msg)
        print(f"ℹ️  [INFO] {msg}")

    def success(self, msg: str) -> None:
        self.logger.info(f"[SUCCESS] {msg}")
        print(f"✅ [SUCCESS] {msg}")

    def warning(self, msg: str) -> None:
        self.logger.warning(msg)
        print(f"⚠️  [WARNING] {msg}")

    def error(self, msg: str, exc: Optional[Exception] = None) -> None:
        if exc:
            self.logger.error(f"{msg} | Exception: {str(exc)}", exc_info=True)
        else:
            self.logger.error(msg)
        print(f"❌ [ERROR] {msg}")

    def step(self, current: int, total: int, msg: str) -> None:
        formatted = f"[{current}/{total}] {msg}"
        self.logger.info(formatted)
        print(f"🚀 {formatted}")


def get_logger(module_name: str) -> CreatorLogger:
    return CreatorLogger(module_name)
