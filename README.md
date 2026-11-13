# Local AI Hardware Scanner

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/github/actions/workflow/status/yourusername/local-ai-hardware-scanner/python-app.yml?branch=main)](https://github.com/yourusername/local-ai-hardware-scanner/actions)
[![Stars](https://img.shields.io/github/stars/yourusername/local-ai-hardware-scanner?style=social)](https://github.com/yourusername/local-ai-hardware-scanner/stargazers)

## Description

**Local AI Hardware Scanner** is a lightweight Python service that scans your machine’s CPU, GPU, and RAM, then recommends the most suitable locally‑run AI models. It bridges the gap between powerful AI capabilities and the often‑complex configuration required for on‑device inference, making it easy for developers, data scientists, and hobbyists to leverage local hardware for AI workloads.

## Features

- **Hardware detection** – Automatic identification of CPU cores, GPU type & memory, and total RAM.
- **Model recommendation engine** – Suggests compatible open‑source AI models (e.g., LLaMA, Stable Diffusion, Whisper) based on detected resources.
- **REST API** – Simple HTTP endpoint for integration with other tools or CI pipelines.
- **Extensible** – Add custom model profiles via a JSON/YAML config file.
- **Zero‑dependency runtime** – Only standard scientific Python packages required.
- **Cross‑platform** – Works on Linux, macOS, and Windows.

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/local-ai-hardware-scanner.git
cd local-ai-hardware-scanner

# Install dependencies
pip install -r requirements.txt

# Run the service
python app.py
```

## Usage

### Command‑line

```bash
# Quick scan and recommendation
python scanner.py
```

**Example output**

```
Detected hardware:
  CPU: 12 cores (Intel(R) Core(TM) i7-12700K)
  GPU: NVIDIA RTX 3080 (10 GB VRAM)
  RAM: 32 GB

Recommended models:
  - LLaMA 7B (requires ≥ 8 GB VRAM)
  - Stable Diffusion v1.5 (requires ≥ 6 GB VRAM)
  - Whisper Base (CPU‑only, ≤ 16 GB RAM)
```

### REST API

The service exposes a single endpoint:

```
GET /api/scan
```

**Response (JSON)**

```json
{
  "cpu": {
    "model": "Intel(R) Core(TM) i7-12700K",
    "cores": 12,
    "threads": 20
  },
  "gpu": {
    "name": "NVIDIA RTX 3080",
    "memory_gb": 10,
    "driver_version": "525.85.12"
  },
  "ram_gb": 32,
  "recommendations": [
    {
      "model": "LLaMA 7B",
      "min_vram_gb": 8,
      "notes": "Fits your GPU"
    },
    {
      "model": "Stable Diffusion v1.5",
      "min_vram_gb": 6,
      "notes": "Fits your GPU"
    },
    {
      "model": "Whisper Base",
      "cpu_only": true,
      "notes": "Runs on CPU, low RAM usage"
    }
  ]
}
```

**Curl example**

```bash
curl http://localhost:8000/api/scan
```

## Roadmap

- **v1.1** – Add support for AMD GPUs and Apple Silicon.
- **v1.2** – Interactive web UI dashboard.
- **v2.0** – Auto‑download and configure recommended models.
- **v2.1** – Plugin system for third‑party model catalogs.
- **v3.0** – Distributed hardware scanning across a LAN.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/awesome-feature`).
3. Write tests and ensure they pass (`pytest`).
4. Update documentation as needed.
5. Submit a Pull Request with a clear description of changes.

See `CONTRIBUTING.md` for detailed guidelines and code style conventions.

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

## Keywords

`AI` `hardware detection` `model recommendation` `local inference` `Python` `REST API` `CPU` `GPU` `RAM` `open‑source models` `edge AI`
