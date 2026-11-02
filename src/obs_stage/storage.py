from __future__ import annotations

import hashlib
import io
import os
import tempfile
from pathlib import Path

from PIL import Image, ImageOps

MAX_AVATAR_BYTES = 16 * 1024 * 1024
DEFAULT_AVATAR_PATH = Path(__file__).parent / "static" / "assets" / "default-avatar.png"


class AvatarStore:
    def __init__(self, data_dir: Path) -> None:
        self.directory = data_dir / "avatar"
        self.directory.mkdir(parents=True, exist_ok=True)
        self.path = self.directory / "avatar.png"
        if not self.path.is_file():
            self.reset()

    def save(self, data: bytes) -> Path:
        if not data:
            raise ValueError("头像文件为空")
        if len(data) > MAX_AVATAR_BYTES:
            raise ValueError("头像文件不能超过 16 MB")
        try:
            loaded = Image.open(io.BytesIO(data))
            loaded.load()
        except Exception as exc:
            raise ValueError("无法识别头像图片") from exc
        image = ImageOps.exif_transpose(loaded).convert("RGBA")
        image.thumbnail((512, 512), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        left = (512 - image.width) // 2
        top = (512 - image.height) // 2
        canvas.alpha_composite(image, (left, top))

        fd, temp_name = tempfile.mkstemp(prefix=".avatar-", suffix=".png", dir=self.directory)
        os.close(fd)
        try:
            canvas.save(temp_name, format="PNG", optimize=True)
            os.replace(temp_name, self.path)
        finally:
            try:
                Path(temp_name).unlink()
            except FileNotFoundError:
                pass
        return self.path

    def reset(self) -> Path:
        return self.save(DEFAULT_AVATAR_PATH.read_bytes())

    def delete(self) -> None:
        self.reset()

    def exists(self) -> bool:
        return self.path.is_file()

    def revision(self) -> str:
        if not self.path.exists():
            return "none"
        return hashlib.sha256(self.path.read_bytes()).hexdigest()[:12]
