from __future__ import annotations

import json
import os
import platform
import tempfile
from pathlib import Path

from .layouts import default_layouts
from .models import AppConfig

APP_DIR_NAME = "VincentZyu-OBS-stage"


def default_data_dir() -> Path:
    override = os.environ.get("OBS_STAGE_DATA_DIR")
    if override:
        return Path(override).expanduser().resolve()
    if os.name == "nt":
        local = os.environ.get("LOCALAPPDATA")
        base = Path(local) if local else Path.home() / "AppData" / "Local"
    elif platform.system() == "Darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    return (base / APP_DIR_NAME).resolve()


def default_config() -> AppConfig:
    return AppConfig(layouts=default_layouts())


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass


class ConfigStore:
    def __init__(self, data_dir: Path | None = None) -> None:
        self.data_dir = (data_dir or default_data_dir()).resolve()
        self.path = self.data_dir / "config.json"
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def load(self) -> AppConfig:
        if not self.path.exists():
            config = default_config()
            self.save(config)
            return config
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            return AppConfig.model_validate(raw)
        except (OSError, ValueError):
            broken = self.path.with_suffix(".broken.json")
            try:
                self.path.replace(broken)
            except OSError:
                pass
            config = default_config()
            self.save(config)
            return config

    def save(self, config: AppConfig) -> None:
        atomic_write_text(self.path, config.model_dump_json(indent=2) + "\n")
