# -*- coding: utf-8 -*-

"""
Configuration management for the AutoCards addon using a local config.json file.
"""

import os
import json
from aqt import mw
from aqt.utils import showWarning

# Define path for config file within the addon directory
addon_path = os.path.dirname(__file__)
config_path = os.path.join(addon_path, "config.json")

# Default configuration
DEFAULT_CONFIG = {
    "api_keys": [],
    "current_api_key_index": 0,
    "model_name": "gemini-2.5-flash-preview-04-17",
    "prompt1": "",
    "prompt2": "",
    "output_placement": "top" # Options: "replace", "top", "below"
}

# Global variable to hold the current configuration
config = {}

def load_config():
    """Loads the addon configuration from config.json."""
    global config
    loaded_config = None
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            loaded_config = json.load(f)
    except FileNotFoundError:
        # Config file doesn't exist yet, will use defaults
        pass
    except json.JSONDecodeError as e:
        showWarning(f"Error reading AutoCards config.json: {e}\nUsing default settings.")
    except Exception as e:
        showWarning(f"Unexpected error reading AutoCards config.json: {e}\nUsing default settings.")

    # If no config loaded or error occurred, start with defaults
    if loaded_config is None:
        config = DEFAULT_CONFIG.copy()
    else:
        config = loaded_config
        # Merge with defaults in case new settings were added to the addon
        for key, default_value in DEFAULT_CONFIG.items():
            if key not in config:
                config[key] = default_value

def save_config():
    """Saves the current addon configuration to config.json."""
    global config
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    except Exception as e:
        # Show a warning dialog to the user if saving fails
        showWarning(f"Failed to save AutoCards configuration to config.json.\n\nError details: {e}")

def get_config():
    """Returns the current configuration."""
    return config

def update_config(new_config_data):
    """Updates the configuration with new data and saves it."""
    global config
    config.update(new_config_data)
    save_config()