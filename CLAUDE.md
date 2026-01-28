# CLAUDE.md - AI Assistant Guide for hailo-apps-prototype

This document provides context and guidelines for AI assistants working on this repository.

## Project Overview

**hailo-apps-prototype** is a prototype repository for developing applications that leverage Hailo AI accelerators. Hailo processors are designed for edge AI inference, enabling efficient deployment of neural networks on embedded devices.

### Project Status

This is a new prototype project. The codebase is being actively developed.

## Repository Structure

```
hailo-apps-prototype/
├── CLAUDE.md           # This file - AI assistant guidelines
└── (project files to be added)
```

As the project grows, expect the following common structure for Hailo applications:

```
hailo-apps-prototype/
├── src/                # Application source code
├── models/             # Hailo-compiled neural network models (.hef files)
├── configs/            # Configuration files
├── scripts/            # Build, deployment, and utility scripts
├── tests/              # Test files
├── docs/               # Documentation
└── requirements.txt    # Python dependencies (if applicable)
```

## Development Guidelines

### General Conventions

1. **Code Style**: Follow standard style guides for the language in use (PEP 8 for Python, etc.)
2. **Documentation**: Document all public APIs and complex logic
3. **Testing**: Write tests for new functionality
4. **Commits**: Use clear, descriptive commit messages

### Hailo-Specific Considerations

When working with Hailo hardware and SDKs:

1. **Model Files**: `.hef` (Hailo Executable Format) files are compiled neural network models
2. **HailoRT**: The Hailo Runtime library for inference on Hailo devices
3. **TAPPAS**: Hailo's application development framework for GStreamer-based pipelines
4. **Dataflow Compiler**: Used to compile models to HEF format

### Environment Setup

Hailo applications typically require:

- Hailo SDK (HailoRT, Dataflow Compiler)
- Python 3.8+ (for Python-based applications)
- GStreamer (for TAPPAS-based applications)
- Appropriate Hailo PCIe driver or USB driver installed

## Commands

### Common Development Commands

(To be updated as project develops)

```bash
# Install dependencies (example)
pip install -r requirements.txt

# Run tests (example)
pytest tests/

# Build/compile (example)
./scripts/build.sh
```

## Architecture Notes

### Typical Hailo Application Patterns

1. **Inference Pipeline**: Load HEF model → Configure input/output → Run inference → Post-process results
2. **GStreamer Pipeline**: Video source → Decode → Hailo inference element → Post-process → Display/output
3. **Multi-model Pipeline**: Chain multiple models for complex AI tasks

### Key Concepts

- **Virtual Device**: Software emulation when no hardware is present
- **HEF**: Compiled model format optimized for Hailo hardware
- **Quantization**: Models must be quantized for Hailo deployment

## AI Assistant Guidelines

### When Implementing Features

1. **Understand the task**: Read existing code before making changes
2. **Use existing patterns**: Follow established conventions in the codebase
3. **Keep it simple**: Avoid over-engineering; implement only what's requested
4. **Test changes**: Verify functionality when possible

### Code Quality

- Prefer clarity over cleverness
- Handle errors appropriately but don't over-engineer error handling
- Use meaningful variable and function names
- Keep functions focused and single-purpose

### File Organization

- Place new source files in appropriate directories
- Keep related functionality together
- Avoid creating unnecessary abstraction layers

### Git Workflow

1. Work on the designated feature branch
2. Make atomic commits with clear messages
3. Push changes to the feature branch when complete

## Resources

- [Hailo Developer Zone](https://hailo.ai/developer-zone/)
- [HailoRT Documentation](https://hailo.ai/developer-zone/documentation/)
- [Hailo Model Zoo](https://github.com/hailo-ai/hailo_model_zoo)
- [TAPPAS Documentation](https://github.com/hailo-ai/tappas)

---

*Last updated: 2026-01-28*
*Note: This file should be updated as the project evolves and new conventions are established.*
