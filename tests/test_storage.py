from io import BytesIO
from pathlib import Path

import pytest
from PIL import Image

from obs_stage.storage import AvatarStore


def _image_bytes(size: tuple[int, int] = (300, 200)) -> bytes:
    image = Image.new("RGB", size, "#7FA8E8")
    output = BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()


def test_default_avatar_is_created(tmp_path: Path) -> None:
    store = AvatarStore(tmp_path)
    path = tmp_path / "avatar" / "avatar.png"
    assert path.is_file()
    with Image.open(path) as image:
        assert image.size == (512, 512)
        assert image.format == "PNG"
        assert image.mode == "RGBA"
    assert store.exists()
    assert store.revision() != "none"


def test_avatar_is_squared_and_stored(tmp_path: Path) -> None:
    store = AvatarStore(tmp_path)
    initial_revision = store.revision()
    path = store.save(_image_bytes())
    assert path.exists()
    with Image.open(path) as image:
        assert image.size == (512, 512)
        assert image.mode == "RGBA"
    assert store.exists()
    assert store.revision() != initial_revision


def test_existing_avatar_is_not_overwritten_on_init(tmp_path: Path) -> None:
    store = AvatarStore(tmp_path)
    store.save(_image_bytes((200, 200)))
    revision = store.revision()

    reopened = AvatarStore(tmp_path)
    assert reopened.revision() == revision
    assert reopened.path.read_bytes() == store.path.read_bytes()


def test_reset_restores_default_avatar(tmp_path: Path) -> None:
    store = AvatarStore(tmp_path)
    default_revision = store.revision()
    store.save(_image_bytes((200, 300)))
    assert store.revision() != default_revision

    store.reset()
    assert store.revision() == default_revision
    with Image.open(store.path) as image:
        assert image.size == (512, 512)
        assert image.mode == "RGBA"


def test_avatar_rejects_invalid_data(tmp_path: Path) -> None:
    store = AvatarStore(tmp_path)
    with pytest.raises(ValueError):
        store.save(b"not an image")
