"""
AI Creator OS - Automated Model Downloader & Registry Sync
Downloads open-source models directly into Google Drive with resuming,
progress tracking, and sha256 checksum verification.
"""
import os
import sys
import yaml
import json
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.model_manager import ModelManager
from core.storage import StorageManager
from core.logger import get_logger


POPULAR_MODELS = {
    "kokoro_tts": {
        "name": "Kokoro-82M TTS v0.19",
        "category": "audio_models",
        "filename": "kokoro-v0_19.pth",
        "url": "https://github.com/hexgrad/kokoro/releases/download/v0.19/kokoro-v0_19.pth",
        "size_mb": 320,
        "sha256": None,
        "license": "Apache-2.0",
    },
    "whisper_base": {
        "name": "OpenAI Whisper Base English",
        "category": "audio_models",
        "filename": "base.pt",
        "url": "https://openaipublic.azureedge.net/main/whisper/models/ed3a0b6b1c0edf879ad9b11996ab15d6e935206c1cad539c088778f73b64f8de/base.pt",
        "size_mb": 140,
        "sha256": "ed3a0b6b1c0edf879ad9b11996ab15d6e935206c1cad539c088778f73b64f8de",
        "license": "MIT",
    },
    "sdxl_turbo": {
        "name": "SDXL Turbo 1-Step Fast Generation",
        "category": "checkpoints",
        "filename": "sd_xl_turbo_1.0_fp16.safetensors",
        "url": "https://huggingface.co/stabilityai/sdxl-turbo/resolve/main/sd_xl_turbo_1.0_fp16.safetensors",
        "size_mb": 6900,
        "sha256": None,
        "license": "Stability AI Community",
    },
    "realesrgan_x4": {
        "name": "RealESRGAN_x4plus Image Upscaler",
        "category": "models",
        "filename": "RealESRGAN_x4plus.pth",
        "url": "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth",
        "size_mb": 67,
        "sha256": None,
        "license": "BSD-3-Clause",
    },
}


def download_model_key(model_key: str) -> bool:
    logger = get_logger("model_downloader")
    if model_key not in POPULAR_MODELS:
        logger.error(f"Unknown model key '{model_key}'. Available: {list(POPULAR_MODELS.keys())}")
        return False

    spec = POPULAR_MODELS[model_key]
    sm = StorageManager()
    target_dir = sm.get_model_dir(spec["category"])
    target_file = target_dir / spec["filename"]

    mm = ModelManager(str(sm.root))
    logger.info(f"Targeting: {spec['name']} -> {target_file}")

    success = mm.download_with_progress(
        url=spec["url"],
        dest_path=str(target_file),
        model_name=spec["name"],
        sha256=spec.get("sha256"),
    )

    if success:
        mm.register_model(
            model_key=model_key,
            category=spec["category"],
            name=spec["name"],
            file_path=str(target_file),
            source_url=spec["url"],
            sha256=spec.get("sha256"),
            license_name=spec.get("license", "Open"),
        )
        logger.success(f"Registered model {spec['name']} in manifest.")
        return True
    else:
        logger.error(f"Failed to download {spec['name']}.")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1:
        download_model_key(sys.argv[1])
    else:
        print("Specify model key to download, e.g. python model_downloader.py kokoro_tts")
