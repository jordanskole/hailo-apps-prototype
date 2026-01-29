"""Core helpers: arch detection, parser, buffer utils, model resolution."""

import os
import queue
import sys
from pathlib import Path
from typing import Optional, Tuple
from dataclasses import dataclass
from dotenv import load_dotenv
from . import parser as common_parser
import argparse

from .defines import (
    DEFAULT_DOTENV_PATH,
    DEFAULT_LOCAL_RESOURCES_PATH,
    DEPTH_MODEL_NAME,
    DEPTH_PIPELINE,
    DETECTION_MODEL_NAME_H8,
    DETECTION_MODEL_NAME_H8L,
    DETECTION_PIPELINE,
    DIC_CONFIG_VARIANTS,
    FACE_DETECTION_MODEL_NAME_H8,
    FACE_DETECTION_MODEL_NAME_H8L,
    FACE_DETECTION_PIPELINE,
    FACE_RECOGNITION_MODEL_NAME_H8,
    FACE_RECOGNITION_MODEL_NAME_H8L,
    FACE_RECOGNITION_PIPELINE,
    HAILO8_ARCH,
    HAILO8L_ARCH,
    HAILO10H_ARCH,
    HAILO_ARCH_KEY,
    HAILO_FILE_EXTENSION,
    INSTANCE_SEGMENTATION_MODEL_NAME_H8,
    INSTANCE_SEGMENTATION_MODEL_NAME_H8L,
    INSTANCE_SEGMENTATION_PIPELINE,
    POSE_ESTIMATION_MODEL_NAME_H8,
    POSE_ESTIMATION_MODEL_NAME_H8L,
    POSE_ESTIMATION_PIPELINE,
    RESOURCES_JSON_DIR_NAME,
    RESOURCES_MODELS_DIR_NAME,
    RESOURCES_NPY_DIR_NAME,
    # for get_resource_path
    RESOURCES_PHOTOS_DIR_NAME,
    RESOURCES_ROOT_PATH_DEFAULT,
    RESOURCES_SO_DIR_NAME,
    RESOURCES_VIDEOS_DIR_NAME,
    SIMPLE_DETECTION_MODEL_NAME,
    SIMPLE_DETECTION_PIPELINE,
    CAMERA_RESOLUTION_MAP,
    RESOURCE_TYPE_IMAGE,
    RESOURCE_TYPE_VIDEO,
    RESOURCE_TYPE_MODEL,
    CAMERA_KEYWORDS,
    # Gen AI apps and models
    AGENT_APP,
    LLM_CHAT_APP,
    VLM_CHAT_APP,
    WHISPER_CHAT_APP,
    LLM_MODEL_NAME_H10,
    VLM_MODEL_NAME_H10,
    WHISPER_MODEL_NAME_H10,
)

from .logger import get_logger
from .installation import detect_hailo_arch

hailo_logger = get_logger(__name__)


def load_environment(env_file=DEFAULT_DOTENV_PATH, required_vars=None) -> bool:
    hailo_logger.debug(f"Loading environment from: {env_file}")
    if env_file is None:
        env_file = DEFAULT_DOTENV_PATH
    load_dotenv(dotenv_path=env_file)

    env_path = Path(env_file)
    if not os.path.exists(env_path):
        hailo_logger.warning(f".env file not found: {env_file}")
        return False
    if not os.access(env_path, os.R_OK):
        hailo_logger.warning(f".env file not readable: {env_file}")
        return False
    if not os.access(env_path, os.W_OK):
        hailo_logger.warning(f".env file not writable: {env_file}")
        return False
    if not os.access(env_path, os.F_OK):
        hailo_logger.warning(f".env file not found (F_OK): {env_file}")
        return False

    if required_vars is None:
        required_vars = DIC_CONFIG_VARIANTS
    missing = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing.append(var)

    if missing:
        hailo_logger.warning(f"Missing environment variables: {missing}")
        return False
    hailo_logger.info("All required environment variables loaded successfully.")
    return True


def get_base_parser():
    """Proxy to the shared base parser implementation."""
    return common_parser.get_base_parser()


def get_pipeline_parser():
    """Proxy to the shared pipeline parser implementation."""
    return common_parser.get_pipeline_parser()


def get_standalone_parser():
    """Proxy to the shared standalone parser implementation."""
    return common_parser.get_standalone_parser()


def get_default_parser():
    """Legacy proxy preserved for backward compatibility."""
    return common_parser.get_default_parser()


def configure_multi_model_hef_path(parser):
    """Proxy to configure --hef-path for multi-model apps."""
    return common_parser.configure_multi_model_hef_path(parser)


def get_model_name(pipeline_name: str, arch: str) -> str:
    hailo_logger.debug(f"Getting model name for pipeline={pipeline_name}, arch={arch}")
    is_h8 = arch in (HAILO8_ARCH, HAILO10H_ARCH)
    pipeline_map = {
        DEPTH_PIPELINE: DEPTH_MODEL_NAME,
        SIMPLE_DETECTION_PIPELINE: SIMPLE_DETECTION_MODEL_NAME,
        DETECTION_PIPELINE: DETECTION_MODEL_NAME_H8 if is_h8 else DETECTION_MODEL_NAME_H8L,
        INSTANCE_SEGMENTATION_PIPELINE: INSTANCE_SEGMENTATION_MODEL_NAME_H8 if is_h8 else INSTANCE_SEGMENTATION_MODEL_NAME_H8L,
        POSE_ESTIMATION_PIPELINE: POSE_ESTIMATION_MODEL_NAME_H8 if is_h8 else POSE_ESTIMATION_MODEL_NAME_H8L,
        FACE_DETECTION_PIPELINE: FACE_DETECTION_MODEL_NAME_H8 if is_h8 else FACE_DETECTION_MODEL_NAME_H8L,
        FACE_RECOGNITION_PIPELINE: FACE_RECOGNITION_MODEL_NAME_H8 if is_h8 else FACE_RECOGNITION_MODEL_NAME_H8L,
        # Gen AI apps (Hailo10H only)
        AGENT_APP: LLM_MODEL_NAME_H10,
        LLM_CHAT_APP: LLM_MODEL_NAME_H10,
        VLM_CHAT_APP: VLM_MODEL_NAME_H10,
        WHISPER_CHAT_APP: WHISPER_MODEL_NAME_H10,
    }
    name = pipeline_map[pipeline_name]
    hailo_logger.debug(f"Resolved model name: {name}")
    return name


def get_resource_path(
    pipeline_name: str, resource_type: str, arch: str | None = None, model: str | None = None
) -> Path | None:
    hailo_logger.debug(
        f"Getting resource path for pipeline={pipeline_name}, resource_type={resource_type}, model={model}"
    )
    root = Path(RESOURCES_ROOT_PATH_DEFAULT)
    # Auto-detect arch if not provided and needed for RESOURCES_MODELS_DIR_NAME
    if arch is None and resource_type == RESOURCES_MODELS_DIR_NAME:
        arch = os.getenv(HAILO_ARCH_KEY) or detect_hailo_arch()
        hailo_logger.debug(f"Auto-detected arch: {arch}")

    if not arch and resource_type == RESOURCES_MODELS_DIR_NAME:
        hailo_logger.error("Could not detect Hailo architecture.")
        assert False, "Could not detect Hailo architecture."

    if resource_type == RESOURCES_SO_DIR_NAME and model:
        return root / RESOURCES_SO_DIR_NAME / model
    if resource_type == RESOURCES_VIDEOS_DIR_NAME and model:
        return root / RESOURCES_VIDEOS_DIR_NAME / model
    if resource_type == RESOURCES_PHOTOS_DIR_NAME and model:
        return root / RESOURCES_PHOTOS_DIR_NAME / model
    if resource_type == RESOURCES_JSON_DIR_NAME and model:
        return root / RESOURCES_JSON_DIR_NAME / model
    if resource_type == RESOURCES_NPY_DIR_NAME and model:
        return root / RESOURCES_NPY_DIR_NAME / model
    if resource_type == DEFAULT_LOCAL_RESOURCES_PATH and model:
        return root / DEFAULT_LOCAL_RESOURCES_PATH / model

    if resource_type == RESOURCES_MODELS_DIR_NAME:
        if model:
            model_path = root / RESOURCES_MODELS_DIR_NAME / arch / model
            if "." in model:
                return model_path.with_name(model_path.name + HAILO_FILE_EXTENSION)
            return model_path.with_suffix(HAILO_FILE_EXTENSION)
        if pipeline_name:
            name = get_model_name(pipeline_name, arch)
            name_path = root / RESOURCES_MODELS_DIR_NAME / arch / name
            if "." in name:
                return name_path.with_name(name_path.name + HAILO_FILE_EXTENSION)
            return name_path.with_suffix(HAILO_FILE_EXTENSION)
    return None


class FIFODropQueue(queue.Queue):
    def put(self, item, block=False, timeout=None):
        if self.full():
            hailo_logger.debug("Queue full, dropping oldest item.")
            self.get_nowait()
        super().put(item, block, timeout)


# =============================================================================
# Model Resolution and Listing
# =============================================================================

def list_models_for_app(app_name: str, arch: str | None = None) -> None:
    """
    List all available models for an application and exit.

    Args:
        app_name: The app name from resources config (e.g., 'detection', 'vlm_chat')
        arch: Hailo architecture. If None, auto-detects.
    """
    # Detect architecture if not provided
    if arch is None:
        arch = os.getenv(HAILO_ARCH_KEY) or detect_hailo_arch()

    print(f"\n{'=' * 60}")
    print(f"Model listing for: {app_name}")
    print(f"{'=' * 60}")

    if arch:
        print(f"\nDetected architecture: {arch}")
    else:
        print("\nNo Hailo device detected.")

    print("\nFor Gen-AI apps (agent, llm_chat, vlm_chat), available models include:")
    print("   - Qwen2.5-Coder-1.5B-Instruct (default for LLM)")
    print("   - Qwen2.5-1.5B-Instruct")
    print("   - Qwen2-VL-2B-Instruct (for VLM)")

    print("\nUsage: --hef-path <model_name_or_path>")
    print("       Provide the path to your .hef model file.")
    print()
    sys.exit(0)


def resolve_hef_path(
    hef_path: str | None,
    app_name: str,
    arch: str | None = None,
) -> Path | None:
    """
    Resolve HEF (Hailo Executable Format) file paths.

    Args:
        hef_path: User-provided path or model name (None uses default model)
        app_name: Application name (e.g., 'agent', 'llm_chat')
        arch: Hailo architecture ('hailo8', 'hailo8l', or 'hailo10h')

    Returns:
        Path to the HEF file, or None if not found
    """
    resources_root = Path(RESOURCES_ROOT_PATH_DEFAULT)

    # Auto-detect arch if not provided
    if arch is None:
        arch = os.getenv(HAILO_ARCH_KEY) or detect_hailo_arch()
        if arch:
            hailo_logger.debug(f"Auto-detected arch: {arch}")

    # If no hef_path provided, try legacy resolution
    if hef_path is None:
        legacy_path = get_resource_path(app_name, RESOURCES_MODELS_DIR_NAME, arch)
        if legacy_path and legacy_path.exists():
            return legacy_path
        hailo_logger.warning(f"No default model found for {app_name}")
        return None

    # Normalize model name
    candidate_name = Path(hef_path).name
    if candidate_name.endswith(HAILO_FILE_EXTENSION):
        model_name = candidate_name[: -len(HAILO_FILE_EXTENSION)]
    else:
        model_name = candidate_name

    # Case 1: Check if it's an existing path
    hef_full_path = Path(hef_path)
    if hef_full_path.exists():
        resolved = hef_full_path.resolve()
        hailo_logger.info(f"Using HEF from path: {resolved}")
        return resolved

    # Case 2: Check with .hef extension
    if not hef_path.endswith(HAILO_FILE_EXTENSION):
        hef_full_path = Path(hef_path + HAILO_FILE_EXTENSION)
        if hef_full_path.exists():
            hailo_logger.info(f"Using HEF from path: {hef_full_path}")
            return hef_full_path

    # Case 3: Check in resources folder
    if arch:
        models_dir = resources_root / RESOURCES_MODELS_DIR_NAME / arch
        resource_path = models_dir / f"{model_name}{HAILO_FILE_EXTENSION}"
        if resource_path.exists():
            hailo_logger.info(f"Found HEF in resources: {resource_path}")
            return resource_path

    hailo_logger.error(f"Model '{hef_path}' not found. Please provide a valid path to the .hef file.")
    return None


def handle_list_models_flag(args, app_name: str) -> None:
    """
    Handle the --list-models flag if present.

    Args:
        args: Parsed arguments (or parser to parse)
        app_name: App name from resources config
    """
    # Parse args if it's a parser
    if hasattr(args, 'parse_known_args'):
        options, _ = args.parse_known_args()
    else:
        options = args

    # Check if --list-models flag is set
    if getattr(options, 'list_models', False):
        arch = getattr(options, 'arch', None)
        list_models_for_app(app_name, arch)

def app_requires_multiple_models(app_name: str, arch: str) -> bool:
    """Check if app requires multiple models. Returns False for standalone agent."""
    return False


@dataclass
class ResolvedModel:
    name: str
    path: Path


def resolve_hef_paths(
    hef_paths: list[str] | None,
    app_name: str,
    arch: str | None = None,
) -> list[ResolvedModel]:
    """
    Resolve one or more HEF paths for apps that require multiple models.

    For standalone agent, this resolves each provided path individually.
    """
    # Auto-detect arch if not provided
    if arch is None:
        arch = os.getenv(HAILO_ARCH_KEY) or detect_hailo_arch()
        if arch:
            hailo_logger.debug(f"Auto-detected arch: {arch}")

    # Normalize inputs
    if hef_paths in (None, [], ""):
        hailo_logger.warning("No HEF paths provided")
        return []
    elif isinstance(hef_paths, str):
        model_names = [hef_paths]
    else:
        model_names = list(hef_paths)

    resolved: list[ResolvedModel] = []

    for model_name in model_names:
        path = resolve_hef_path(
            hef_path=model_name,
            app_name=app_name,
            arch=arch,
        )
        if path is None:
            raise RuntimeError(f"Failed to resolve model: {model_name}")

        resolved.append(ResolvedModel(name=model_name, path=path))

    return resolved



# =============================================================================
# Input Resolution and Listing
# =============================================================================

def list_inputs_for_app(app_name: str) -> None:
    """
    List available inputs for an application and exit.
    Simplified for standalone agent - no config-based resource listing.
    """
    print(f"\n{'=' * 60}")
    print(f"Input options for: {app_name}")
    print(f"{'=' * 60}")
    print("\nSupported input sources:")
    print("   - Local file path (image or video)")
    print("   - 'usb' for USB camera")
    print("   - 'rpi' for Raspberry Pi camera")
    print(f"\n{'=' * 60}\n")
    sys.exit(0)


def resolve_input_arg(app: str, input_arg: str | None) -> str:
    """
    Resolve the CLI `--input` argument into a concrete input source.

    Simplified for standalone agent:
    - If no input provided, returns empty string
    - Camera keywords ('usb', 'rpi') returned as-is
    - Local paths returned as-is if they exist
    """
    # No input provided
    if input_arg is None:
        hailo_logger.warning("No input provided. Use --input to specify a source.")
        return ""

    # Camera keywords
    if input_arg in CAMERA_KEYWORDS:
        return input_arg

    # Local path
    path_candidate = Path(input_arg)
    if path_candidate.exists():
        return str(path_candidate)

    # Invalid input
    hailo_logger.error(
        f"Input '{input_arg}' does not exist as a local file or directory.\n"
        "Please provide a valid file path or camera source: 'usb' / 'rpi'."
    )
    sys.exit(1)



# =============================================================================
# Handle and Resolve Common Args
# =============================================================================
def handle_and_resolve_args(args: argparse.ArgumentParser, APP_NAME: str, multi_hef: bool = False) -> None:
    """
    Handle common CLI argument logic for Hailo applications.

    This function:
    - Handles early-exit flags such as --list-models and --list-inputs
    - Resolves the HEF path for the given application
    - Resolves the input source (camera / video / image)
    - Resolves output resolution if the flag exists
    - Ensures a valid output directory exists

    Notes:
    - This helper is intended mainly for standalone applications.

    Args:
        args: Parsed argparse.Namespace from the application
        APP_NAME: The application name for model/input resolution
    """

    #handle --list-models and exit
    if args.list_models:
        list_models_for_app(APP_NAME)
        sys.exit(0)

    # Handle --list-inputs and exit
    if args.list_inputs:
        list_inputs_for_app(APP_NAME)
        sys.exit(0)


    if multi_hef:
        # Resolve multiple HEF paths
        try:
            models = resolve_hef_paths(
                hef_paths=args.hef_path,
                app_name=APP_NAME
            )
            args.hef_path = [model.path for model in models]
        except Exception as e:
            hailo_logger.error(f"Failed to resolve HEF paths: {e}")
            sys.exit(1)
    else:
        # Resolve network path
        args.hef_path = resolve_hef_path(hef_path=args.hef_path, app_name=APP_NAME)
        if args.hef_path is None:
            hailo_logger.error("Failed to resolve HEF path for %s", APP_NAME)
            sys.exit(1)

    #resolve input source
    args.input = resolve_input_arg(APP_NAME, args.input)
    if args.input is None:
        hailo_logger.error("Failed to resolve input source for %s", APP_NAME)
        sys.exit(1)

    # Resolve output resolution if flag exists
    if hasattr(args, "output_dir"):
        try:
            if args.output_dir is None:
                args.output_dir = os.path.join(os.getcwd(), "output")
                os.makedirs(args.output_dir, exist_ok=True)
        except ValueError as e:
            hailo_logger.error(str(e))
            sys.exit(1)


    # Resolve output resolution if flag exists
    if hasattr(args, "output_resolution"):
        try:
            args.output_resolution = resolve_output_resolution_arg(args.output_resolution)
        except ValueError as e:
            hailo_logger.error(str(e))
            sys.exit(1)


def resolve_output_resolution_arg(res_arg: Optional[list[str]]) -> Optional[Tuple[int, int]]:
    """
    Parse --output-resolution argument.

    Supported:
      --output-resolution sd|hd|fhd
      --output-resolution 1920 1080
    """
    if res_arg is None:
        return None

    # Single token: preset name (sd/hd/fhd)
    if len(res_arg) == 1:
        key = res_arg[0]
        if key in CAMERA_RESOLUTION_MAP:
            return CAMERA_RESOLUTION_MAP[key]
        raise ValueError(
            f"Invalid --output-resolution value '{key}'. "
            "Use 'sd', 'hd', 'fhd' or two integers, e.g. '--output-resolution 1920 1080'."
        )

    # Two tokens: custom width/height
    if len(res_arg) == 2 and all(x.isdigit() for x in res_arg):
        w, h = map(int, res_arg)
        if w <= 0 or h <= 0:
            raise ValueError("Custom --output-resolution width/height must be positive integers.")
        return (w, h)

    raise ValueError(
        f"Invalid --output-resolution value: {res_arg}. "
        "Use 'sd', 'hd', 'fhd' or two integers, e.g. '--output-resolution 1920 1080'."
    )
