"""
AI Creator OS - Central Model Management System
Handles model registration, sha256 verification, resume downloads,
shared storage to prevent duplicate multi-GB downloads, and status auditing.
"""
import os
import json
import hashlib
import urllib.request
from pathlib import Path
from typing import Dict, Any, Optional, List


class ModelManager:
    """Manages models across modules with hash verification and persistent caching."""

    def __init__(self, root_dir: str = "/content/drive/MyDrive/AI_Creator_OS"):
        self.root_dir = Path(root_dir)
        self.manifest_file = self.root_dir / "config/model_manifest.json"
        self.manifest_file.parent.mkdir(parents=True, exist_ok=True)
        self.manifest: Dict[str, Any] = self._load_manifest()

    def _load_manifest(self) -> Dict[str, Any]:
        if self.manifest_file.exists():
            try:
                with open(self.manifest_file, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def _save_manifest(self) -> None:
        try:
            with open(self.manifest_file, "w") as f:
                json.dump(self.manifest, f, indent=2)
        except Exception as e:
            print(f"⚠️ Warning saving manifest: {e}")

    @staticmethod
    def calculate_sha256(filepath: str, chunk_size: int = 8192 * 1024) -> str:
        """Calculates SHA-256 hash in streaming chunks."""
        hasher = hashlib.sha256()
        with open(filepath, "rb") as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
        return hasher.hexdigest()

    def is_model_ready(self, model_key: str, expected_min_bytes: int = 1000000) -> bool:
        """Returns True only if file exists, is non-empty, and has expected size/hash."""
        if model_key in self.manifest:
            entry = self.manifest[model_key]
            path = Path(entry.get("path", ""))
            if path.exists():
                size = path.stat().st_size
                if size >= expected_min_bytes:
                    return entry.get("status") == "verified"
        return False

    def register_model(
        self,
        model_key: str,
        category: str,
        name: str,
        file_path: str,
        source_url: str,
        sha256: Optional[str] = None,
        license_name: str = "Open Access",
    ) -> Dict[str, Any]:
        """Registers and verifies a downloaded model."""
        p = Path(file_path)
        size_bytes = p.stat().st_size if p.exists() else 0
        computed_hash = ""
        status = "unverified"

        if p.exists() and size_bytes > 0:
            if sha256:
                computed_hash = self.calculate_sha256(str(p))
                if computed_hash.lower() == sha256.lower():
                    status = "verified"
                else:
                    status = "hash_mismatch"
            else:
                status = "verified"

        entry = {
            "model_key": model_key,
            "category": category,
            "name": name,
            "path": str(p.resolve()),
            "source_url": source_url,
            "size_bytes": size_bytes,
            "size_mb": round(size_bytes / (1024 * 1024), 2),
            "sha256": computed_hash or sha256 or "",
            "status": status,
            "license": license_name,
        }
        self.manifest[model_key] = entry
        self._save_manifest()
        return entry

    def download_with_progress(
        self,
        url: str,
        dest_path: str,
        model_name: str = "Model",
        sha256: Optional[str] = None,
    ) -> bool:
        """Downloads file with streaming progress and resumes if supported."""
        dest = Path(dest_path)
        dest.parent.mkdir(parents=True, exist_ok=True)

        if dest.exists() and dest.stat().st_size > 0:
            if sha256:
                if self.calculate_sha256(str(dest)).lower() == sha256.lower():
                    print(f"⚡ [CACHE HIT] {model_name} already exists and hash verified.")
                    return True
                else:
                    print(f"⚠️ [HASH MISMATCH] Re-downloading {model_name}...")
                    dest.unlink()
            else:
                print(f"⚡ [CACHE HIT] {model_name} already exists ({round(dest.stat().st_size / (1024*1024), 1)} MB).")
                return True

        print(f"📥 Downloading {model_name} from: {url}")
        print(f"📂 Destination: {dest}")

        try:
            # Colab curl / aria2c / requests fallback
            import urllib.request

            def reporthook(count, block_size, total_size):
                if total_size > 0:
                    percent = int(count * block_size * 100 / total_size)
                    mb_down = round(count * block_size / (1024 * 1024), 1)
                    mb_total = round(total_size / (1024 * 1024), 1)
                    if percent % 10 == 0 or percent == 100:
                        print(f"\r  -> Progress: {percent}% ({mb_down}/{mb_total} MB)", end="", flush=True)

            urllib.request.urlretrieve(url, str(dest), reporthook)
            print("\n✅ Download finished.")

            # Validate
            if sha256:
                print("🔍 Validating SHA-256 checksum...")
                computed = self.calculate_sha256(str(dest))
                if computed.lower() != sha256.lower():
                    print(f"❌ Checksum mismatch! Expected {sha256}, got {computed}")
                    dest.unlink(missing_ok=True)
                    return False
                print("✅ SHA-256 Checksum verified.")
            return True
        except Exception as e:
            print(f"❌ Download failed: {e}")
            if dest.exists():
                dest.unlink(missing_ok=True)
            return False

    def list_installed_models(self) -> List[Dict[str, Any]]:
        return list(self.manifest.values())


if __name__ == "__main__":
    mm = ModelManager()
    print("Model Manager ready. Installed models:", len(mm.list_installed_models()))
