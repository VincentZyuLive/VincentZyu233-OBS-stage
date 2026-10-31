from pathlib import Path

from PIL import Image

from obs_stage.config import default_config
from obs_stage.models import SceneId
from obs_stage.renderer import BackgroundRenderer


def test_background_is_rendered_and_cached(tmp_path: Path) -> None:
    renderer = BackgroundRenderer(tmp_path)
    config = default_config()
    first = renderer.render(SceneId.HALF_SCREEN, config)
    second = renderer.render(SceneId.HALF_SCREEN, config)
    assert first == second
    assert first.exists()
    with Image.open(first) as image:
        assert image.size == (1920, 1080)
        assert image.mode == "RGB"


def test_theme_change_creates_new_background(tmp_path: Path) -> None:
    renderer = BackgroundRenderer(tmp_path)
    config = default_config()
    first = renderer.render(SceneId.NO_SCREEN, config)
    config.theme.palette.primary = "#00A8FF"
    second = renderer.render(SceneId.NO_SCREEN, config)
    assert first != second
