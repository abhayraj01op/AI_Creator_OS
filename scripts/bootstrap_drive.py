"""
AI Creator OS - Automated Google Drive Bootstrapper
Mounts Drive, creates the 5TB directory skeleton, checks permissions,
and initializes system manifests and configs.
"""
import os
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.hardware import HardwareDetector
from core.storage import StorageManager
from core.logger import get_logger


def bootstrap():
    logger = get_logger("bootstrap")
    logger.step(1, 4, "Detecting Google Drive mount state...")

    in_colab = os.path.exists("/content")
    if in_colab:
        if not os.path.exists("/content/drive/MyDrive"):
            logger.info("Attempting automatic Google Drive mount in Colab...")
            try:
                from google.colab import drive
                drive.mount('/content/drive')
                logger.success("Google Drive mounted at /content/drive/MyDrive")
            except Exception as e:
                logger.warning(f"Google Drive not mounted automatically: {e}. Using /content local fallback.")
        else:
            logger.success("Google Drive is already mounted.")
    else:
        logger.info("Running in standard local/server environment.")

    logger.step(2, 4, "Initializing 5TB persistent directory architecture...")
    sm = StorageManager()
    paths = sm.initialize_filesystem()
    logger.success(f"Storage tree verified at: {sm.root} ({len(paths)} folders ready)")

    logger.step(3, 4, "Performing system hardware audit...")
    HardwareDetector.print_summary()

    logger.step(4, 4, "Google Drive bootstrap completed successfully.")


if __name__ == "__main__":
    bootstrap()
