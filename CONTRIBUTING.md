# Contributing to AI Creator OS

We welcome community contributions, custom pipeline modules, new model integrations, and performance optimizations!

## Contribution Guidelines
1. **Fork the Repository**: Clone your fork locally or work directly in Colab.
2. **Branching**: Create feature branches (`git checkout -b feature/new-engine`).
3. **Module Compliance**: Ensure any new module implements:
   - Automated Google Drive mount & directory verification
   - Persistent dependency caching via `installation_state.json`
   - Hardware tier fallback (GPU / CPU)
   - Gradio web interface with shareable link
4. **Code Quality**: Keep notebooks clean, documented, and tested with `scripts/health_check.py`.
