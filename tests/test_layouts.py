from obs_stage.layouts import default_layouts
from obs_stage.models import SceneId


def test_scene_slots_fit_canvas() -> None:
    for scene, layout in default_layouts().items():
        assert layout.scene == scene
        for slot in layout.slots:
            rect = slot.rect
            assert rect.x >= 0
            assert rect.y >= 0
            assert rect.x + rect.width <= 1920
            assert rect.y + rect.height <= 1080
            assert rect.radius > 0


def test_each_scene_has_a_primary_content_slot() -> None:
    layouts = default_layouts()
    assert layouts[SceneId.NO_SCREEN].slots[0].name == "media"
    assert layouts[SceneId.HALF_SCREEN].slots[0].name == "capture"
    assert layouts[SceneId.FULL_SCREEN].slots[0].name == "capture"
