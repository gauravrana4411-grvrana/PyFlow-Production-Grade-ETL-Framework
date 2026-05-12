import yaml
import json
from typing import Dict

def load_config(file_path: str)-> Dict:
    if file_path.endswith('.yaml') or file_path.endswith('.yml'):
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    elif file_path.endswith('.json'):
        with open(file_path, 'r') as file:
            return json.load(file)
    else:
        raise ValueError("Unsupported config format")