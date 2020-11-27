import json

from pathlib import Path


config_path = Path(__file__).parent.parent / "config.json"
with open(config_path, "r") as file:
    config = json.load(file)

ACCOUNT_FOLDERS_ROOT = config.get("ACCOUNT_FOLDERS_ROOT", None)
PASSWORD = config.get("PASSWORD", None)

DB_HOST = config.get("DB_HOST", None)
DB_USER = config.get("DB_USER", None)
DB_NAME = config.get("DB_NAME", None)
DB_PASSWORD = config.get("DB_PASSWORD", None)


if __name__ == "__main__":
    # Debug config
    input()
