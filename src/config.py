import os
import configparser

CONFIG_DIR = os.path.expanduser("~/.config/window-transparency")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.ini")

DEFAULTS = {
    "general": {
        "default_opacity": "85",
        "toggle_restore": "true",
    },
    "presets": {
        "light": "90",
        "medium": "80",
        "strong": "70",
    },
    "apps": {},
}


def load_config():
    config = configparser.ConfigParser()

    # Load defaults
    for section, values in DEFAULTS.items():
        config[section] = values

    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)

    return config


def save_config(config):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        config.write(f)


def get_default_opacity(config):
    return int(config["general"].get("default_opacity", "85"))


def get_presets(config):
    return {
        k: int(v) for k, v in config["presets"].items()
    }


def get_app_opacity(config, app_name):
    if "apps" in config and app_name in config["apps"]:
        return int(config["apps"][app_name])
    return None


def set_app_opacity(config, app_name, opacity):
    if "apps" not in config:
        config["apps"] = {}
    config["apps"][app_name] = str(opacity)
    save_config(config)


def set_default_opacity(config, opacity):
    config["general"]["default_opacity"] = str(opacity)
    save_config(config)
