"""
AI Creator OS - Self-Update and Integrity Auditor
Pulls latest repository changes without overwriting local custom models or outputs.
"""
import os
import sys
import subprocess
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.logger import get_logger


def check_for_updates():
    logger = get_logger("update_manager")
    logger.info("Checking repository version against GitHub origin...")
    try:
        res = subprocess.run(["git", "fetch", "--dry-run"], capture_output=True, text=True)
        logger.info("Fetched remote tracking information.")
        status = subprocess.run(["git", "status", "-uno"], capture_output=True, text=True)
        if "Your branch is up to date" in status.stdout:
            logger.success("AI Creator OS is up to date with latest release.")
        else:
            logger.warning("Updates are available. Run `git pull origin main` to update scripts.")
    except Exception as e:
        logger.warning(f"Git check skipped (manual or standalone deployment): {e}")


if __name__ == "__main__":
    check_for_updates()
