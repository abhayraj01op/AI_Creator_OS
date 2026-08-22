"""
AI Creator OS - Lightweight Backup and Snapshot Manager
Backs up metadata, configuration, custom workflows, and prompts without duplicating multi-terabyte model weights.
"""
import os
import sys
import shutil
import time
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.storage import StorageManager
from core.logger import get_logger


def create_system_backup():
    logger = get_logger("backup")
    sm = StorageManager()
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    backup_dir = sm.get_path(f"backups/backup_{timestamp}")
    backup_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Initiating lightweight system backup to: {backup_dir}")

    # Copy config directory
    config_src = sm.get_path("config")
    if config_src.exists():
        shutil.copytree(config_src, backup_dir / "config", dirs_exist_ok=True)

    # Copy projects metadata
    projects_src = sm.get_path("projects")
    if projects_src.exists():
        for proj in projects_src.iterdir():
            if proj.is_dir():
                meta = proj / "project.json"
                if meta.exists():
                    dest_proj = backup_dir / f"projects/{proj.name}"
                    dest_proj.mkdir(parents=True, exist_ok=True)
                    shutil.copy(meta, dest_proj / "project.json")

    logger.success(f"Snapshot successfully saved at: {backup_dir}")
    return str(backup_dir)


if __name__ == "__main__":
    create_system_backup()
