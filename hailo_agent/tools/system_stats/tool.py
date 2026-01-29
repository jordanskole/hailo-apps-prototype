"""
System stats tool for reading hardware sensor data.

Reads temperatures and other system statistics from the Raspberry Pi.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

name: str = "system_stats"

display_description: str = (
    "Read system statistics such as CPU and GPU temperatures from the device."
)

description: str = (
    "Use this tool to read system statistics from the device. "
    "Currently supports reading CPU and GPU temperatures.\n\n"
    "The function name is 'system_stats' (use this exact name in tool calls).\n\n"
    "TOOL CALL FORMAT - This is the ONLY format allowed:\n"
    "<tool_call>\n"
    '{"name": "system_stats", "arguments": {"stat": "STAT_NAME"}}\n'
    "</tool_call>\n\n"
    "Available stats:\n"
    "- 'cpu_temp' - Read the CPU temperature\n"
    "- 'gpu_temp' - Read the GPU temperature\n"
    "- 'all_temps' - Read all available temperatures\n\n"
    "DEFAULT OPTION: If the user requests a stat that is not supported, "
    "set 'default' to true."
)

schema: dict[str, Any] = {
    "type": "object",
    "properties": {
        "stat": {
            "type": "string",
            "enum": ["cpu_temp", "gpu_temp", "all_temps"],
            "description": (
                "The system statistic to read. "
                "Options: 'cpu_temp', 'gpu_temp', 'all_temps'."
            ),
        },
        "default": {
            "type": "boolean",
            "description": (
                "Set to true when the user requests an unsupported stat. "
                "The tool will return an appropriate error message."
            ),
        },
    },
    "required": [],
}

TOOLS_SCHEMA: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": schema,
        },
    }
]


CPU_THERMAL_PATH = Path("/sys/class/thermal/thermal_zone0/temp")


def _read_cpu_temp() -> dict[str, Any]:
    """Read CPU temperature from thermal zone."""
    try:
        millidegrees = int(CPU_THERMAL_PATH.read_text().strip())
        temp_c = millidegrees / 1000.0
        return {"ok": True, "result": f"CPU temperature: {temp_c:.1f}\u00b0C"}
    except FileNotFoundError:
        return {"ok": False, "error": "CPU thermal sensor not found"}
    except (ValueError, OSError) as e:
        return {"ok": False, "error": f"Failed to read CPU temperature: {e}"}


def _read_gpu_temp() -> dict[str, Any]:
    """Read GPU temperature via vcgencmd."""
    try:
        result = subprocess.run(
            ["vcgencmd", "measure_temp"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode != 0:
            return {"ok": False, "error": f"vcgencmd failed: {result.stderr.strip()}"}

        # Parse output like "temp=52.1'C"
        output = result.stdout.strip()
        temp_str = output.split("=")[1].rstrip("'C")
        temp_c = float(temp_str)
        return {"ok": True, "result": f"GPU temperature: {temp_c:.1f}\u00b0C"}
    except FileNotFoundError:
        return {"ok": False, "error": "vcgencmd not found (not a Raspberry Pi?)"}
    except (IndexError, ValueError) as e:
        return {"ok": False, "error": f"Failed to parse GPU temperature: {e}"}
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "Timed out reading GPU temperature"}


def _read_all_temps() -> dict[str, Any]:
    """Read all available temperatures."""
    results = []

    cpu = _read_cpu_temp()
    if cpu["ok"]:
        results.append(cpu["result"])
    else:
        results.append(f"CPU: {cpu['error']}")

    gpu = _read_gpu_temp()
    if gpu["ok"]:
        results.append(gpu["result"])
    else:
        results.append(f"GPU: {gpu['error']}")

    if not results:
        return {"ok": False, "error": "No temperature sensors available"}

    return {"ok": True, "result": "\n".join(results)}


_STAT_HANDLERS = {
    "cpu_temp": _read_cpu_temp,
    "gpu_temp": _read_gpu_temp,
    "all_temps": _read_all_temps,
}


def run(input_data: dict[str, Any]) -> dict[str, Any]:
    """
    Read the requested system statistic.

    Args:
        input_data: Dictionary with keys:
            - stat: Which statistic to read (required unless default is used).
            - default: Set to true for unsupported stat requests.

    Returns:
        Dictionary with 'ok' and 'result' (if successful) or 'error' (if failed).
    """
    if input_data.get("default") is True:
        return {
            "ok": True,
            "error": (
                "That stat is not supported. "
                "Available stats: cpu_temp, gpu_temp, all_temps."
            ),
        }

    stat = input_data.get("stat", "").strip()
    if not stat:
        return {"ok": False, "error": "The 'stat' parameter is required."}

    handler = _STAT_HANDLERS.get(stat)
    if handler is None:
        return {
            "ok": False,
            "error": (
                f"Unknown stat '{stat}'. "
                f"Available stats: {', '.join(_STAT_HANDLERS.keys())}."
            ),
        }

    return handler()
