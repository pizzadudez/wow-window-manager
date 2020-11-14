import json

from pathlib import Path


config_path = Path(__file__).parent.parent / "config.json"
with open(config_path, "r") as file:
    config = json.load(file)

ACCOUNT_FOLDERS_ROOT = config.get("ACCOUNT_FOLDERS_ROOT", None)


if __name__ == "__main__":
    # Debug config
    input()
