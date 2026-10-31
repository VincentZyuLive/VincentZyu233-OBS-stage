from __future__ import annotations

import hashlib
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

from .models import AppConfig, BackgroundStyle, SceneId

WIDTH = 1600
HEIGHT = 900


def _color(value: str, alpha: int = 255) -> tuple[int, int, int, int]:
    text = value.lstrip("#")
    if len(text) != 6:
        text = "08111F"
    return (int(text[0:2], 16), int(text[2:4], 16), int(text[4:6], 16), alpha)


class BackgroundRenderer:
    def __init__(self, data_dir: Path) -> None:
        self.directory = data_dir / "backgrounds"
        self.directory.mkdir(parents=True, exist_ok=True)

    def render(self, scene: SceneId, config: AppConfig) -> Path:
        key = hashlib.sha256(
            (scene.value + config.theme.model_dump_json()).encode("utf-8")
        ).hexdigest()[:16]
        path = self.directory / f"{scene.value}-{key}.png"
        if path.exists():
            return path

        theme = config.theme
        palette = theme.palette
        gradient = Image.new("RGBA", (1, HEIGHT), _color(palette.background))
        gradient_pixels = gradient.load()
        if gradient_pixels is None:
            raise RuntimeError("could not access gradient pixels")
        surface = _color(palette.surface)
        for y in range(HEIGHT):
            ratio = y / max(1, HEIGHT - 1)
            gradient_color = tuple(
                round(_color(palette.background)[index] * (1 - ratio) + surface[index] * ratio)
                for index in range(3)
            )
            gradient_pixels[0, y] = (*gradient_color, 255)
        base = gradient.resize((WIDTH, HEIGHT), Image.Resampling.BILINEAR)

        glow = Image.new("RGBA", base.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(glow, "RGBA")
        anchors = {
            SceneId.NO_SCREEN: ((1490, 180), (380, 830)),
            SceneId.HALF_SCREEN: ((1650, 170), (500, 940)),
            SceneId.FULL_SCREEN: ((1430, 120), (260, 930)),
        }[scene]
        glow_alpha = round(78 + 78 * theme.glow_strength)
        for index, (center, glow_color) in enumerate(
            zip(anchors, (palette.primary, palette.pink), strict=True)
        ):
            radius = 420 if index == 0 else 320
            draw.ellipse(
                (
                    center[0] - radius,
                    center[1] - radius,
                    center[0] + radius,
                    center[1] + radius,
                ),
                fill=_color(glow_color, glow_alpha),
            )
        glow = glow.filter(ImageFilter.GaussianBlur(150))
        base.alpha_composite(glow)

        line_layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
        line_draw = ImageDraw.Draw(line_layer, "RGBA")
        rng = random.Random(scene.value)
        if theme.background_style == BackgroundStyle.WATERCOLOR:
            for band in range(7):
                points = []
                amplitude = 30 + band * 7
                baseline = 160 + band * 125
                for x in range(-40, WIDTH + 80, 24):
                    wave = math.sin(x / (150 + band * 18) + band * 0.9) * amplitude
                    points.append((x, baseline + wave))
                line_draw.line(
                    points,
                    fill=_color(palette.highlight if band % 2 == 0 else palette.primary, 17),
                    width=2,
                )
            for _ in range(26):
                x = rng.randint(80, WIDTH - 80)
                y = rng.randint(60, HEIGHT - 60)
                radius = rng.randint(20, 100)
                line_draw.ellipse(
                    (x - radius, y - radius, x + radius, y + radius),
                    fill=_color(palette.primary if rng.random() > 0.35 else palette.pink, 6),
                )
        elif theme.background_style == BackgroundStyle.AURORA:
            for index in range(8):
                offset = index * 180 - 450
                line_draw.polygon(
                    [
                        (offset, HEIGHT),
                        (offset + 220, 0),
                        (offset + 430, 0),
                        (offset + 170, HEIGHT),
                    ],
                    fill=_color(palette.primary if index % 2 else palette.highlight, 10),
                )
        else:
            for index in range(5):
                radius = 180 + index * 70
                line_draw.ellipse(
                    (WIDTH - radius - 80, -radius + 130, WIDTH + radius - 80, radius + 130),
                    outline=_color(palette.primary, 12),
                    width=2,
                )
        base.alpha_composite(line_layer.filter(ImageFilter.GaussianBlur(1.2)))

        if theme.grain_strength > 0:
            noise = Image.effect_noise((WIDTH // 3, HEIGHT // 3), 42).resize(base.size)
            noise = noise.convert("RGBA")
            noise.putalpha(round(255 * theme.grain_strength * 0.2))
            base.alpha_composite(noise)

        vignette = Image.new("RGBA", base.size, (0, 0, 0, 0))
        vignette_draw = ImageDraw.Draw(vignette, "RGBA")
        for step in range(24):
            inset = step * 18
            vignette_draw.rounded_rectangle(
                (inset, inset, WIDTH - inset, HEIGHT - inset),
                radius=40,
                outline=(0, 0, 0, 3),
                width=18,
            )
        base.alpha_composite(vignette)
        base.convert("RGB").save(path, format="PNG", optimize=True)
        return path
