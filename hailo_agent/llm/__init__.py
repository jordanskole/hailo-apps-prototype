# Re-export modules with their new and old names for compatibility
from hailo_agent.llm import messages as message_formatter
from hailo_agent.llm import context as context_manager
from hailo_agent.llm import streaming
from hailo_agent.llm import tool_discovery
from hailo_agent.llm import tool_execution
from hailo_agent.llm import tool_parsing
from hailo_agent.llm import tool_selection
from hailo_agent.llm import terminal_ui

# Also export with new names
from hailo_agent.llm import messages
from hailo_agent.llm import context

# Import agent_utils last to avoid circular imports
from hailo_agent.llm import agent_utils
