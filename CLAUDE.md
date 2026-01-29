# CLAUDE.md - AI Assistant Guide for hailo-agent

This document provides context and guidelines for AI assistants working on this repository.

## Project Overview

**hailo-agent** is an interactive CLI chat agent that uses Hailo LLM models with function calling capabilities. The agent automatically discovers tools and allows the LLM to call them during conversations.

This project was extracted from the larger `hailo-ai/hailo-apps` repository and restructured into a clean, flat package layout.

### Key Features

- **Tool Discovery**: Automatic discovery of tools from the `tools/` directory
- **Function Calling**: LLM can invoke tools during conversations
- **Voice Support**: Optional voice input/output mode (requires additional dependencies)
- **Hardware Control**: Support for RGB LEDs, servos, and other hardware on Raspberry Pi
- **Context Management**: Token-based context management with automatic cleanup

## Repository Structure

```
hailo-apps-prototype/
├── hailo_agent/
│   ├── __init__.py
│   ├── agent.py              # Main entry point
│   ├── config.py             # LLM configuration
│   ├── state_manager.py      # Context state management
│   ├── system_prompt.py      # System prompt generation
│   ├── yaml_config.py        # YAML config loader
│   ├── cli_state.py          # CLI state utilities
│   ├── core/                 # Core utilities
│   │   ├── logger.py         # Logging infrastructure
│   │   ├── parser.py         # CLI argument parser
│   │   ├── defines.py        # Constants and defaults
│   │   ├── utils.py          # General utilities, model resolution
│   │   ├── installation.py   # Device detection
│   │   └── hef_utils.py      # HEF model utilities
│   ├── tools/                # Tool implementations
│   │   ├── base.py           # Base tool class
│   │   ├── math/             # Math operations tool
│   │   ├── weather/          # Weather API tool
│   │   ├── rgb_led/          # RGB LED control
│   │   ├── servo/            # Servo motor control
│   │   ├── elevator/         # Elevator demo tool
│   │   └── _template/        # Template for new tools
│   ├── llm/                  # LLM utilities
│   │   ├── __init__.py       # Module exports with aliases
│   │   ├── context.py        # Token management (alias: context_manager)
│   │   ├── messages.py       # Message formatting (alias: message_formatter)
│   │   ├── streaming.py      # Response streaming
│   │   ├── tool_discovery.py # Auto-discover tools
│   │   ├── tool_execution.py # Execute tool calls
│   │   ├── tool_parsing.py   # Parse tool calls from LLM
│   │   ├── tool_selection.py # Interactive tool selection
│   │   └── terminal_ui.py    # Terminal UI helpers
│   ├── voice/                # Voice input/output (optional)
│   │   ├── speech_to_text.py # Whisper transcription
│   │   ├── text_to_speech.py # Piper TTS
│   │   ├── interaction.py    # Voice interaction manager
│   │   ├── vad.py            # Voice activity detection (lazy imports)
│   │   └── audio_*.py        # Audio utilities
│   └── testing/              # Test framework
│       ├── harness.py        # Test harness
│       ├── benchmark.py      # Benchmarking
│       └── metrics.py        # Test metrics
├── resources/                # Symlink to /usr/local/hailo/resources (created by setup.sh)
├── setup.sh                  # Setup script (creates symlink, venv, installs package)
├── pyproject.toml            # Project configuration
├── README.md                 # User documentation
├── CLAUDE.md                 # This file
└── .gitignore
```

## Development Guidelines

### Quick Start

```bash
# Run setup script (creates resources symlink, venv, installs package)
./setup.sh

# Activate the virtual environment
source venv/bin/activate

# Run the agent with a tool
python -m hailo_agent.agent --tool math --hef-path Qwen2.5-Coder-1.5B-Instruct
```

### Running the Agent

```bash
# Text mode with specific model (recommended)
python -m hailo_agent.agent --tool math --hef-path Qwen2.5-Coder-1.5B-Instruct

# Interactive tool selection (omit --tool)
python -m hailo_agent.agent --hef-path Qwen2.5-Coder-1.5B-Instruct

# Voice mode (requires voice dependencies)
python -m hailo_agent.agent --voice --hef-path Qwen2.5-Coder-1.5B-Instruct

# List available models
ls resources/models/hailo10h/*.hef
```

**Note:** The `--hef-path` flag is required unless the default model (`Qwen2.5-1.5B-Instruct`) is installed. Available models depend on what's in `/usr/local/hailo/resources/models/hailo10h/`.

### Installation

```bash
# Recommended: Use setup script
./setup.sh

# Or manual installation:
# 1. Create resources symlink
ln -s /usr/local/hailo/resources resources

# 2. Create venv and install
python3 -m venv venv
source venv/bin/activate
pip install -e .

# With voice support
pip install -e ".[voice]"

# With hardware support (Raspberry Pi)
pip install -e ".[hardware]"

# Development dependencies
pip install -e ".[dev]"
```

### Code Style

- Python 3.10+ required
- Follow PEP 8 style guide
- Use `ruff` for linting: `ruff check .`
- Use `ruff format` for formatting

### Creating New Tools

1. Copy `hailo_agent/tools/_template/` to `hailo_agent/tools/your_tool_name/`
2. Implement the tool interface in `tool.py`:
   - `name: str` - Unique identifier
   - `description: str` - Instructions for the LLM
   - `schema: dict` - JSON schema for parameters
   - `run(input: dict) -> dict` - Execution function
3. Configure tool in `config.yaml`
4. Tools are auto-discovered - no code changes needed

### Tool Return Format

```python
{
    "ok": bool,      # Success status
    "result": Any,   # Result if ok=True
    "error": str     # Error message if ok=False
}
```

## Key Files Reference

| File | Purpose |
|------|---------|
| `agent.py` | Main entry point, CLI handling, chat loop |
| `config.py` | LLM parameters, hardware mode settings |
| `state_manager.py` | Context persistence, save/load snapshots |
| `system_prompt.py` | Generate system prompts with tool definitions |
| `tools/base.py` | `BaseTool` abstract class, `ToolResult` dataclass |
| `llm/__init__.py` | Module exports with aliases (see below) |
| `llm/streaming.py` | Response generation with streaming |
| `llm/tool_discovery.py` | Auto-discover and load tools |
| `core/utils.py` | Model resolution, resource paths |
| `core/defines.py` | Constants, default model names |

### LLM Module Aliases

The `llm/__init__.py` exports modules with legacy-compatible aliases:

```python
from hailo_agent.llm import context_manager  # Actually llm/context.py
from hailo_agent.llm import message_formatter  # Actually llm/messages.py
```

This allows existing code to use familiar names while the actual files have cleaner names.

### Available Models

Models are stored in `/usr/local/hailo/resources/models/hailo10h/` (symlinked to `resources/`).

Common Gen AI models:
- `Qwen2.5-1.5B-Instruct` - Default LLM (may not be installed)
- `Qwen2.5-Coder-1.5B-Instruct` - Coder variant (commonly available)
- `Qwen2-VL-2B-Instruct` - Vision-Language model
- `Whisper-Base` - Speech-to-text

Check available models with: `ls resources/models/hailo10h/*.hef`

## Dependencies

### Required
- `hailo-platform` - Hailo SDK (installed separately)
- `numpy` - Array operations
- `pyyaml` - Configuration files
- `python-dotenv` - Environment variables

### Optional (Voice Mode)
- `sounddevice` - Audio I/O
- `piper-tts` - Text-to-speech
- `PyAudio` - Audio interface
- `webrtcvad-wheels` - Voice activity detection

### Optional (Hardware)
- `rpi5-ws2812` - RGB LED control on Raspberry Pi
- `rpi-hardware-pwm` - Servo control on Raspberry Pi

## Architecture Notes

### Tool Discovery Flow
1. `llm/tool_discovery.py` scans `tools/` directory
2. Each tool package must have `tool.py` with required interface
3. Tools are loaded dynamically at runtime
4. Tool schemas are combined into system prompt

### LLM Interaction Flow
1. User input received
2. System prompt + tools sent to LLM
3. LLM response parsed for tool calls (`<tool_call>JSON</tool_call>`)
4. Tool executed if present
5. Result added to context
6. LLM generates final response

### Context Management
- Token-based (not message-based)
- Clears at 80% capacity
- Supports save/load of context snapshots
- Caches system prompts for faster startup

## AI Assistant Guidelines

### When Implementing Features

1. Read existing code before making changes
2. Follow established patterns in the codebase
3. Keep implementations simple and focused
4. Test changes when possible

### Code Quality

- Prefer clarity over cleverness
- Handle errors appropriately but don't over-engineer
- Use meaningful variable and function names
- Keep functions focused and single-purpose

### Common Tasks

**Adding a new tool:**
- Copy `tools/_template/` directory
- Implement required interface
- Add tests if complex

**Modifying LLM behavior:**
- Edit `system_prompt.py` for general behavior
- Edit tool `description` for tool-specific behavior

**Changing hardware settings:**
- Edit `config.py` for default values
- Use CLI arguments for runtime changes

## Resources

- [Hailo Developer Zone](https://hailo.ai/developer-zone/)
- [HailoRT Documentation](https://hailo.ai/developer-zone/documentation/)

---

*Last updated: 2026-01-28*
*Session notes: Fixed import errors, added setup.sh, resources symlink support*
