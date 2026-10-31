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


def test_avatar_is_squared_and_stored(tmp_path: Path) -> None:
    store = AvatarStore(tmp_path)
    path = store.save(_image_bytes())
    assert path.exists()
    with Image.open(path) as image:
        assert image.size == (512, 512)
        assert image.mode == "RGBA"
    assert store.exists()
    assert store.revision() != "none"


def test_avatar_rejects_invalid_data(tmp_path: Path) -> None:
    store = AvatarStore(tmp_path)
    with pytest.raises(ValueError):
        store.save(b"not an image")
