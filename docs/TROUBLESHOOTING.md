# TROUBLESHOOTING & ERROR RECOVERY

## Common Scenarios & Automated Recovery

### 1. "CUDA out of memory" (OOM Error)
- **Likely Cause**: Generating 1024x1024 batch sizes exceeding GPU VRAM budget.
- **Automated Fix**: The system detects high VRAM usage and enables `enable_sequential_cpu_offload()` and `vae.enable_tiling()`.
- **Manual Action**: In the notebook, reduce resolution to 768x768 or switch batch size to 1.

### 2. "Google Drive transport endpoint is not connected"
- **Likely Cause**: Colab session timed out or network disconnected.
- **Resolution**: Re-run Cell 2 (`drive.mount('/content/drive')`). All existing files remain preserved.

### 3. "Port 7860 already in use"
- **Likely Cause**: A previous Gradio instance remained bound.
- **Resolution**: `core/error_handler.py` cleans up stale gradio instances and binds to the next free port automatically.
