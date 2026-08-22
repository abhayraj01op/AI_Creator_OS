# MODEL REGISTRY & COMPATIBILITY GUIDE

## Supported Production Models

| Category | Model Name | Size | Default Location | License |
|---|---|---|---|---|
| **Audio / TTS** | Kokoro-82M v0.19 | 320 MB | `audio_models/kokoro-v0_19.pth` | Apache-2.0 |
| **Audio / STT** | Whisper Base | 140 MB | `audio_models/base.pt` | MIT |
| **Audio / STT** | Whisper Large v3 Turbo | 1.5 GB | `audio_models/large-v3-turbo.pt` | MIT |
| **Image Synth** | SDXL Turbo FP16 | 6.9 GB | `checkpoints/sd_xl_turbo_1.0_fp16.safetensors` | Stability AI Community |
| **Image Synth** | SDXL 1.0 Base | 6.9 GB | `checkpoints/sd_xl_base_1.0.safetensors` | CreativeML OpenRAIL++-M |
| **Upscaling** | RealESRGAN_x4plus | 67 MB | `models/RealESRGAN_x4plus.pth` | BSD-3-Clause |
| **Writer LLM** | Qwen 2.5 Coder 1.5B | 3.1 GB | `llm_models/qwen2.5-coder-1.5b` | Apache-2.0 |
| **Writer LLM** | Llama 3.2 3B Instruct | 6.2 GB | `llm_models/llama-3.2-3b` | Llama 3.2 Community |

## Adding Custom Checkpoints & LoRAs
Place your `.safetensors` files directly into:
- Checkpoints: `/content/drive/MyDrive/AI_Creator_OS/checkpoints/`
- LoRAs: `/content/drive/MyDrive/AI_Creator_OS/loras/`
- ControlNets: `/content/drive/MyDrive/AI_Creator_OS/controlnet/`
