"""
AI Creator OS - Hardware and Environment Detector
Accurately identifies GPU, VRAM, CUDA, CPU cores, RAM, and storage.
Provides tier recommendations: HIGH (>=24GB VRAM), MEDIUM (>=12GB), LOW (>=8GB), CPU_ONLY.
"""
import os
import sys
import shutil
import platform
from typing import Dict, Any, Optional

try:
    import torch
except ImportError:
    torch = None

try:
    import psutil
except ImportError:
    psutil = None


class HardwareDetector:
    """Inspects runtime hardware and returns structured compute profile."""

    @staticmethod
    def get_hardware_info() -> Dict[str, Any]:
        info: Dict[str, Any] = {
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "cpu_count": os.cpu_count() or 1,
            "system_ram_gb": 0.0,
            "has_gpu": False,
            "gpu_name": "None",
            "gpu_count": 0,
            "vram_total_gb": 0.0,
            "vram_free_gb": 0.0,
            "cuda_available": False,
            "cuda_version": "None",
            "tier": "CPU_ONLY",
            "recommended_precision": "fp32",
            "drive_mounted": os.path.exists("/content/drive/MyDrive"),
            "drive_free_gb": 0.0,
            "content_free_gb": 0.0,
        }

        # System RAM
        if psutil:
            mem = psutil.virtual_memory()
            info["system_ram_gb"] = round(mem.total / (1024 ** 3), 2)
        else:
            try:
                with open("/proc/meminfo", "r") as f:
                    for line in f:
                        if "MemTotal" in line:
                            kb = int(line.split()[1])
                            info["system_ram_gb"] = round(kb / (1024 ** 2), 2)
                            break
            except Exception:
                info["system_ram_gb"] = 12.0

        # Disk space
        try:
            content_stat = shutil.disk_usage("/content" if os.path.exists("/content") else ".")
            info["content_free_gb"] = round(content_stat.free / (1024 ** 3), 2)
        except Exception:
            pass

        if os.path.exists("/content/drive/MyDrive"):
            info["drive_mounted"] = True
            try:
                drive_stat = shutil.disk_usage("/content/drive/MyDrive")
                info["drive_free_gb"] = round(drive_stat.free / (1024 ** 3), 2)
            except Exception:
                pass

        # GPU & CUDA
        if torch and torch.cuda.is_available():
            info["has_gpu"] = True
            info["cuda_available"] = True
            info["cuda_version"] = torch.version.cuda or "Unknown"
            info["gpu_count"] = torch.cuda.device_count()
            info["gpu_name"] = torch.cuda.get_device_name(0)

            total_bytes = torch.cuda.get_device_properties(0).total_memory
            info["vram_total_gb"] = round(total_bytes / (1024 ** 3), 2)

            try:
                free_bytes, _ = torch.cuda.mem_get_info()
                info["vram_free_gb"] = round(free_bytes / (1024 ** 3), 2)
            except Exception:
                info["vram_free_gb"] = info["vram_total_gb"]

            # Tier classification
            vram = info["vram_total_gb"]
            if vram >= 23.0:
                info["tier"] = "HIGH"  # A100 (40GB/80GB), L4 (24GB), RTX 3090/4090
                info["recommended_precision"] = "bf16" if torch.cuda.is_bf16_supported() else "fp16"
            elif vram >= 14.0:
                info["tier"] = "MEDIUM"  # T4 16GB, V100 16GB
                info["recommended_precision"] = "fp16"
            elif vram >= 7.0:
                info["tier"] = "LOW"  # 8GB VRAM
                info["recommended_precision"] = "fp16"
            else:
                info["tier"] = "MINIMAL_GPU"
                info["recommended_precision"] = "fp16"
        else:
            info["has_gpu"] = False
            info["tier"] = "CPU_ONLY"
            info["recommended_precision"] = "fp32"

        return info

    @classmethod
    def print_summary(cls) -> None:
        info = cls.get_hardware_info()
        print("=" * 60)
        print("⚡ AI CREATOR OS — HARDWARE AUDIT")
        print("=" * 60)
        print(f"• Python:       {info['python_version']} on {info['platform']}")
        print(f"• System RAM:   {info['system_ram_gb']} GB (CPU Cores: {info['cpu_count']})")
        if info["has_gpu"]:
            print(f"• GPU Device:   {info['gpu_name']} (Total: {info['vram_total_gb']} GB VRAM)")
            print(f"• CUDA Version: {info['cuda_version']} | Precision: {info['recommended_precision']}")
            print(f"• Hardware Tier: {info['tier']} VRAM PROFILE")
        else:
            print("• GPU Device:   None (CPU Fallback Mode Active)")
            print("• Hardware Tier: CPU_ONLY (Quantized & Optimized Models Selected)")
        print(f"• Google Drive: {'CONNECTED (Free: ' + str(info['drive_free_gb']) + ' GB)' if info['drive_mounted'] else 'NOT MOUNTED (/content temp storage)'}")
        print(f"• Local Space:  {info['content_free_gb']} GB free")
        print("=" * 60)


if __name__ == "__main__":
    HardwareDetector.print_summary()
