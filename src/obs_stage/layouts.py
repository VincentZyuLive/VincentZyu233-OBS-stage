from __future__ import annotations

from .models import Rect, SceneId, SceneLayout, StageSlot


def default_layouts() -> dict[SceneId, SceneLayout]:
    return {
        SceneId.NO_SCREEN: SceneLayout(
            scene=SceneId.NO_SCREEN,
            label="No Screen",
            slots=[
                StageSlot(
                    name="media",
                    label="SPlayer / 主内容",
                    rect=Rect(x=220, y=320, width=1480, height=443, radius=40),
                    placeholder="SPlayer 内容槽",
                )
            ],
        ),
        SceneId.HALF_SCREEN: SceneLayout(
            scene=SceneId.HALF_SCREEN,
            label="Half Screen",
            slots=[
                StageSlot(
                    name="capture",
                    label="显示器采集",
                    rect=Rect(x=480, y=96, width=960, height=540, radius=38),
                    placeholder="显示器采集",
                ),
                StageSlot(
                    name="media",
                    label="SPlayer / 播放器",
                    rect=Rect(x=530, y=660, width=820, height=245, radius=30),
                    placeholder="SPlayer 内容槽",
                ),
            ],
        ),
        SceneId.FULL_SCREEN: SceneLayout(
            scene=SceneId.FULL_SCREEN,
            label="Full Screen",
            slots=[
                StageSlot(
                    name="capture",
                    label="显示器采集",
                    rect=Rect(x=20, y=20, width=1880, height=1040, radius=38),
                    placeholder="全屏采集",
                ),
                StageSlot(
                    name="media",
                    label="SPlayer / 悬浮播放器",
                    rect=Rect(x=570, y=790, width=700, height=210, radius=26),
                    placeholder="SPlayer 悬浮卡",
                ),
            ],
        ),
    }
