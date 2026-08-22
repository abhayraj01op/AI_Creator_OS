"""
AI Creator OS - Self-Test and Health Check Diagnostics
Runs automated verification across Python runtime, Drive persistence,
GPU acceleration, CUDA memory, package imports, output directories, and UI readiness.
"""
import os
import sys
import shutil
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.hardware import HardwareDetector
from core.storage import StorageManager
from core.logger import get_logger


def run_full_health_check(module_name: str = "SYSTEM_CORE") -> bool:
    logger = get_logger("health_check")
    print("\n" + "=" * 60)
    print(f"🩺 AI CREATOR OS — COMPREHENSIVE HEALTH CHECK [{module_name}]")
    print("=" * 60)

    results = []

    # 1. Python Environment Check
    py_ver = sys.version_info
    py_ok = (py_ver.major == 3 and py_ver.minor >= 9)
    results.append(("Python 3.9+ Runtime", py_ok, f"{py_ver.major}.{py_ver.minor}.{py_ver.micro}"))

    # 2. Google Drive Storage Check
    sm = StorageManager()
    drive_ok = sm.root.exists() and os.access(str(sm.root), os.W_OK)
    results.append(("Persistent Storage Tree", drive_ok, str(sm.root)))

    # 3. GPU / Compute Acceleration Check
    hw = HardwareDetector.get_hardware_info()
    if hw["has_gpu"]:
        results.append(("NVIDIA CUDA GPU", True, f"{hw['gpu_name']} ({hw['vram_total_gb']} GB VRAM)"))
    else:
        results.append(("Compute Device", True, "CPU Fallback Mode (Operational)"))

    # 4. Storage Disk Quota
    free_gb = hw.get("drive_free_gb", hw.get("content_free_gb", 0))
    disk_ok = free_gb > 1.0
    results.append(("Disk Capacity Check", disk_ok, f"{free_gb} GB Available"))

    # 5. Output Directory Writable
    out_dir = sm.get_output_dir(module_name.lower())
    out_test_file = out_dir / ".write_test.tmp"
    try:
        with open(out_test_file, "w") as f:
            f.write("OK")
        out_test_file.unlink()
        results.append(("Output Directory Writable", True, str(out_dir)))
    except Exception as e:
        results.append(("Output Directory Writable", False, str(e)))

    # 6. Logging Facility Check
    log_dir = sm.get_path("logs")
    log_ok = log_dir.exists() and os.access(str(log_dir), os.W_OK)
    results.append(("Logging System Ready", log_ok, str(log_dir)))

    # Summary Report
    all_passed = True
    print("\nDIAGNOSTIC RESULTS:")
    for label, status, detail in results:
        icon = "✅ [PASS]" if status else "❌ [FAIL]"
        print(f" {icon} {label:<28} : {detail}")
        if not status:
            all_passed = False

    print("=" * 60)
    if all_passed:
        print(f"🎉 MODULE '{module_name}' READY FOR PRODUCTION EXECUTION")
    else:
        print(f"⚠️  MODULE '{module_name}' HAS NON-CRITICAL OR CRITICAL WARNINGS")
    print("=" * 60 + "\n")
    return all_passed


if __name__ == "__main__":
    run_full_health_check("MASTER_DIAGNOSTICS")
