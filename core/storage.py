"""
AI Creator OS - Storage and Directory Manager
Manages the persistent 5TB Google Drive structure, local fallbacks,
and guarantees directory trees exist for models, configs, outputs, and cache.
"""
import os
import shutil
from pathlib import Path
from typing import Dict, Optional


class StorageManager:
    """Configures and validates directory topology across Google Drive and local paths."""

    DEFAULT_DRIVE_ROOT = "/content/drive/MyDrive/AI_Creator_OS"
    LOCAL_FALLBACK_ROOT = "/content/AI_Creator_OS_local"

    DIRECTORIES = [
        "modules",
        "models",
        "checkpoints",
        "loras",
        "vae",
        "embeddings",
        "controlnet",
        "audio_models",
        "video_models",
        "llm_models",
        "tools",
        "environments",
        "cache",
        "outputs/media",
        "outputs/writer",
        "outputs/coding",
        "outputs/voice",
        "outputs/youtube",
        "outputs/animation",
        "outputs/video",
        "outputs/agents",
        "projects",
        "datasets",
        "temp",
        "logs",
        "backups",
        "config",
    ]

    def __init__(self, custom_root: Optional[str] = None):
        self.drive_connected = os.path.exists("/content/drive/MyDrive")
        if custom_root:
            self.root = Path(custom_root)
        elif self.drive_connected:
            self.root = Path(self.DEFAULT_DRIVE_ROOT)
        else:
            self.root = Path(self.LOCAL_FALLBACK_ROOT)

    def initialize_filesystem(self) -> Dict[str, str]:
        """Creates all required folder hierarchies."""
        created_paths = {}
        self.root.mkdir(parents=True, exist_ok=True)

        for rel_dir in self.DIRECTORIES:
            full_path = self.root / rel_dir
            full_path.mkdir(parents=True, exist_ok=True)
            created_paths[rel_dir] = str(full_path)

        # Temporary local fast cache on /content if on Colab
        if os.path.exists("/content"):
            local_cache = Path("/content/temp_cache")
            local_cache.mkdir(exist_ok=True)
            created_paths["local_fast_cache"] = str(local_cache)

        return created_paths

    def get_path(self, relative_path: str) -> Path:
        """Returns the full resolved path inside the storage root."""
        return self.root / relative_path

    def get_output_dir(self, module_name: str) -> Path:
        """Returns the output directory for a specific module."""
        out_dir = self.root / f"outputs/{module_name}"
        out_dir.mkdir(parents=True, exist_ok=True)
        return out_dir

    def get_model_dir(self, category: str = "models") -> Path:
        """Returns model category directory."""
        m_dir = self.root / category
        m_dir.mkdir(parents=True, exist_ok=True)
        return m_dir


if __name__ == "__main__":
    sm = StorageManager()
    paths = sm.initialize_filesystem()
    print(f"✅ Storage initialized at: {sm.root}")
    print(f"Created {len(paths)} core structural directories.")
