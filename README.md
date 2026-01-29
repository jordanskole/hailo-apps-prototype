# Hailo Agent

Interactive CLI chat agent that uses Hailo LLM models with function calling capabilities. The agent automatically discovers tools and allows the LLM to call them during conversations.

## Overview

This project provides an AI agent framework for Hailo accelerators with:

- **Tool Discovery**: Automatic discovery of tools from `tools/` directory
- **Function Calling**: LLM can invoke tools during conversations
- **Voice Support**: Optional voice input/output mode
- **Hardware Control**: Support for RGB LEDs, servos, and other hardware

## Requirements

- Python 3.10+
- Hailo SDK (HailoRT) with LLM support
- Hailo AI accelerator hardware (or virtual device for testing)

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd hailo-apps-prototype

# Recommended: use the setup script (creates resources symlink, venv, installs package)
./setup.sh
source venv/bin/activate

# Or install manually
pip install -e .

# Optional extras
pip install -e ".[voice]"      # Voice mode support
pip install -e ".[hardware]"   # Raspberry Pi hardware control
pip install -e ".[dev]"        # Development dependencies
```

## Quick Start

```bash
# Run with the default model (Qwen2.5-Coder-1.5B-Instruct)
python -m hailo_agent.agent --tool math

# Specify a different model
python -m hailo_agent.agent --tool math --hef-path Qwen2.5-1.5B-Instruct

# Interactive tool selection (omit --tool)
python -m hailo_agent.agent

# Voice mode
python -m hailo_agent.agent --voice

# List available models
ls resources/models/hailo10h/*.hef
```

## Available Tools

| Tool | Description |
|------|-------------|
| **math** | Basic arithmetic operations (add, subtract, multiply, divide) |
| **weather** | Current weather and forecasts via Open-Meteo API |
| **rgb_led** | RGB LED control (color, brightness, on/off) |
| **servo** | Servo motor control (absolute/relative positioning) |
| **elevator** | Abstract elevator control demonstration |

## Interactive Commands

| Command | Description |
|---------|-------------|
| `/exit` | Exit the chat |
| `/clear` | Clear conversation context |
| `/context` | Show context token usage |

## Creating New Tools

1. Create a new directory in `hailo_agent/tools/`
2. Add `__init__.py`, `tool.py`, and `config.yaml`
3. Implement the tool interface (see `tools/_template/` for reference)

Tools are automatically discovered - no code changes needed in the agent.

## Project Structure

```
hailo-apps-prototype/
├── hailo_agent/
│   ├── agent.py          # Main entry point
│   ├── config.py         # Configuration
│   ├── core/             # Core utilities (logging, parser, etc.)
│   ├── tools/            # Tool implementations
│   │   ├── base.py
│   │   ├── math/
│   │   ├── weather/
│   │   ├── rgb_led/
│   │   ├── servo/
│   │   └── elevator/
│   ├── llm/              # LLM utilities
│   ├── voice/            # Voice input/output (optional)
│   └── testing/          # Test framework
├── pyproject.toml
├── CLAUDE.md
└── README.md
```

## License

See [LICENSE](LICENSE) for details.
