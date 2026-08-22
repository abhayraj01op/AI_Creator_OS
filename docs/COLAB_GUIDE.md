# GOOGLE COLAB OPTIMIZATION & RUN GUIDE

## Hardware Tiers on Google Colab

| Colab Tier | Hardware Detected | Recommended Precision | Optimizations Applied |
|---|---|---|---|
| **Colab Pro+** | NVIDIA A100 (40GB/80GB) | `bf16` / `fp16` | FlashAttention-2, Batch Size x2, 4K Upscale |
| **Colab Pro** | NVIDIA L4 (24GB) or V100 (16GB) | `fp16` | xFormers, SDXL 1024x1024 Native |
| **Colab Free** | NVIDIA T4 (15GB/16GB) | `fp16` | Sequential CPU Offload, VAE Tiling |
| **CPU Fallback** | Intel Xeon (2 Cores, 12GB RAM) | `fp32` / `int8` | Model Quantization, Lightweight Synthesizers |

## 1-Click Execution Procedure
1. Open desired notebook via Colab badge or GitHub repository link.
2. Select **Runtime → Change runtime type → T4 GPU** (or A100 if subscribed).
3. Click **Runtime → Run all** (`Ctrl + F9`).
4. Accept Google Drive authorization prompt when prompted.
5. Watch the 10-step progress output in real-time.
6. Click the generated **public Gradio URL** (e.g. `https://xxxx.gradio.live`) to open the web studio.
