from obs_stage.layouts import default_layouts
from obs_stage.models import SceneId


def test_scene_slots_fit_canvas() -> None:
    for scene, layout in default_layouts().items():
        assert layout.scene == scene
        for slot in layout.slots:
            rect = slot.rect
            assert rect.x >= 0
            assert rect.y >= 0
            assert rect.x + rect.width <= 1600
            assert rect.y + rect.height <= 900
            assert rect.radius > 0


def test_each_scene_has_a_primary_content_slot() -> None:
    layouts = default_layouts()
    assert layouts[SceneId.NO_SCREEN].slots[0].name == "media"
    assert layouts[SceneId.HALF_SCREEN].slots[0].name == "capture"
    assert layouts[SceneId.FULL_SCREEN].slots[0].name == "capture"


def test_half_screen_emphasizes_capture_area() -> None:
    slots = default_layouts()[SceneId.HALF_SCREEN].slots
    capture = slots[0].rect
    media = slots[1].rect
    assert (capture.x, capture.y, capture.width, capture.height) == (360, 60, 880, 495)
    assert (media.x, media.y, media.width, media.height) == (470, 585, 660, 197)
    assert capture.width > media.width


def test_full_screen_player_slot_aligns_with_capture_bottom() -> None:
    slots = default_layouts()[SceneId.FULL_SCREEN].slots
    capture = slots[0].rect
    media = slots[1].rect
    assert (media.x, media.y, media.width, media.height, media.radius) == (475, 708, 650, 175, 22)
    assert media.x + media.width / 2 == 800
    assert capture.y + capture.height == media.y + media.height == 883
