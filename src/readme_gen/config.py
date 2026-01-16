# Configuration handling for readme-gen
import yaml
from pathlib import Path
from typing import Dict, Any

DEFAULT_CONFIG_PATH = Path("readme-config.yaml")

def load_config(config_path: Path = DEFAULT_CONFIG_PATH) -> Dict[str, Any]:
    """Loads the configuration from a YAML file."""
    if not config_path.exists():
        # Handle case where config file doesn't exist
        # Maybe create a default one or raise an error
        print(f"Warning: Configuration file not found at {config_path}. Using defaults.")
        return {} # Or return some default structure

    try:
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)
        return config_data if config_data else {}
    except yaml.YAMLError as e:
        print(f"Error parsing configuration file {config_path}: {e}")
        # Consider raising an exception or returning defaults
        return {}
    except Exception as e:
        print(f"Error reading configuration file {config_path}: {e}")
        return {}

# Example usage (optional, can be removed)
if __name__ == "__main__":
    config = load_config()
    print("Loaded configuration:")
    print(config)