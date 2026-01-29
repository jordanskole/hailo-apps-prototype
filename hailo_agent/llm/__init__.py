"""
LLM utilities package.

Provides modules for LLM interactions, message formatting, context management,
tool discovery, and response streaming.
"""

# Import modules with their expected names
from hailo_agent.llm import context as context_manager
from hailo_agent.llm import messages as message_formatter
from hailo_agent.llm import (
    agent_utils,
    streaming,
    tool_discovery,
    tool_execution,
    tool_parsing,
    tool_selection,
    terminal_ui,
)

__all__ = [
    "agent_utils",
    "context_manager",
    "message_formatter",
    "streaming",
    "tool_discovery",
    "tool_execution",
    "tool_parsing",
    "tool_selection",
    "terminal_ui",
]
