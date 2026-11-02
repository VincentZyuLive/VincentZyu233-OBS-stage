from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class SceneId(StrEnum):
    NO_SCREEN = "no-screen"
    HALF_SCREEN = "half-screen"
    FULL_SCREEN = "full-screen"


class BackgroundStyle(StrEnum):
    WATERCOLOR = "watercolor"
    AURORA = "aurora"
    MINIMAL = "minimal"


class Palette(BaseModel):
    background: str = "#08111F"
    surface: str = "#101C30"
    primary: str = "#7FA8E8"
    highlight: str = "#DCEBFF"
    pink: str = "#F4C6D7"
    cream: str = "#FFF3DE"
    text: str = "#F4F7FF"
    muted: str = "#93A4BD"


class ThemeConfig(BaseModel):
    preset: str = "mizuiro"
    palette: Palette = Field(default_factory=Palette)
    background_style: BackgroundStyle = BackgroundStyle.WATERCOLOR
    frame_radius: int = Field(default=34, ge=8, le=80)
    frame_width: int = Field(default=2, ge=0, le=8)
    glow_strength: float = Field(default=0.62, ge=0, le=1)
    particle_count: int = Field(default=14, ge=0, le=40)
    grain_strength: float = Field(default=0.08, ge=0, le=0.3)
    font_family: str = "LXGW WenKai Mono"


class Branding(BaseModel):
    title: str = "VincentZyu"
    subtitle: str = "点点关注点点三连谢谢喵Thanks♪(･ω･)ﾉ"
    show_avatar: bool = True
    show_clock: bool = True
    show_scene_label: bool = True


class Rect(BaseModel):
    x: int
    y: int
    width: int
    height: int
    radius: int = 30


class StageSlot(BaseModel):
    name: str
    label: str
    rect: Rect
    placeholder: str = ""


class SceneLayout(BaseModel):
    scene: SceneId
    label: str
    slots: list[StageSlot]


class ObsConnectionConfig(BaseModel):
    url: str = "ws://127.0.0.1:4455"


class LiveStatusConfig(BaseModel):
    room_id: str = "5861873"
    refresh_seconds: int = Field(default=10, ge=5, le=60)


class AppConfig(BaseModel):
    theme: ThemeConfig = Field(default_factory=ThemeConfig)
    branding: Branding = Field(default_factory=Branding)
    layouts: dict[SceneId, SceneLayout]
    obs: ObsConnectionConfig = Field(default_factory=ObsConnectionConfig)
    status: LiveStatusConfig = Field(default_factory=LiveStatusConfig)


class ObsRequest(BaseModel):
    password: str = Field(default="", max_length=4096)


class ObsApplyRequest(BaseModel):
    scene: SceneId | None = None
    password: str = Field(default="", max_length=4096)
