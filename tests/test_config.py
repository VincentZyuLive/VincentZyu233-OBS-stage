from __future__ import annotations

from pathlib import Path

from obs_stage.config import ConfigStore, default_config
from obs_stage.models import SceneId


def test_default_config_has_three_scenes() -> None:
    config = default_config()
    assert set(config.layouts) == set(SceneId)
    assert config.theme.preset == "mizuiro"
    assert config.status.room_id == "5861873"
    assert config.status.refresh_seconds == 10
    assert config.assets.cache_bust is True


def test_config_round_trip(tmp_path: Path) -> None:
    store = ConfigStore(tmp_path)
    config = store.load()
    config.branding.title = "Test Channel"
    config.theme.particle_count = 7
    config.assets.cache_bust = False
    store.save(config)
    loaded = store.load()
    assert loaded.branding.title == "Test Channel"
    assert loaded.theme.particle_count == 7
    assert loaded.assets.cache_bust is False


def test_broken_config_is_replaced(tmp_path: Path) -> None:
    store = ConfigStore(tmp_path)
    store.path.write_text("{broken", encoding="utf-8")
    loaded = store.load()
    assert loaded.branding.title == "VincentZyu"
    assert store.path.with_suffix(".broken.json").exists()
