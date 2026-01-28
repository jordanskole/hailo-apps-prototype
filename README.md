# Hailo Agent Tools

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
git clone https://github.com/hailo-ai/hailo-apps-prototype.git
cd hailo-apps-prototype

# Install base dependencies
pip install -e .

# For voice mode support
pip install -e ".[voice]"

# For Raspberry Pi hardware control
pip install -e ".[hardware]"

# For development
pip install -e ".[dev]"
```

## Quick Start

```bash
# Text mode (default)
python -m hailo_apps.python.gen_ai_apps.agent_tools_example.agent

# Voice mode
python -m hailo_apps.python.gen_ai_apps.agent_tools_example.agent --voice

# Or use the installed command
hailo-agent
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

1. Create a new directory in `hailo_apps/python/gen_ai_apps/agent_tools_example/tools/`
2. Add `__init__.py`, `tool.py`, and `config.yaml`
3. Implement the tool interface (see `tools/_template/` for reference)

Tools are automatically discovered - no code changes needed in the agent.

## Project Structure

```
hailo-apps-prototype/
├── hailo_apps/
│   ├── python/
│   │   ├── core/common/          # Core utilities (logging, parser, etc.)
│   │   └── gen_ai_apps/
│   │       ├── agent_tools_example/  # Main agent application
│   │       │   ├── agent.py          # Entry point
│   │       │   ├── tools/            # Tool implementations
│   │       │   └── testing/          # Test framework
│   │       └── gen_ai_utils/
│   │           ├── llm_utils/        # LLM utilities
│   │           └── voice_processing/ # Voice input/output
│   └── config/                   # Configuration management
├── pyproject.toml
├── CLAUDE.md
└── README.md
```

## Documentation

- [Agent Tools Example README](hailo_apps/python/gen_ai_apps/agent_tools_example/README.md) - Detailed usage and configuration
- [Testing Guide](hailo_apps/python/gen_ai_apps/agent_tools_example/testing/TESTING.md) - Test framework documentation
- [LLM Utils README](hailo_apps/python/gen_ai_apps/gen_ai_utils/llm_utils/README.md) - LLM utility documentation

## License

See [LICENSE](LICENSE) for details.
