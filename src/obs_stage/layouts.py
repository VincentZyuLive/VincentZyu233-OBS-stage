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
                    rect=Rect(x=183, y=267, width=1233, height=369, radius=33),
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
                    rect=Rect(x=360, y=60, width=1160, height=605, radius=35),
                    placeholder="显示器采集",
                ),
                StageSlot(
                    name="media",
                    label="SPlayer / 播放器",
                    rect=Rect(x=500, y=700, width=600, height=150, radius=24),
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
                    rect=Rect(x=17, y=17, width=1566, height=866, radius=32),
                    placeholder="全屏采集",
                ),
                StageSlot(
                    name="media",
                    label="SPlayer / 悬浮播放器",
                    rect=Rect(x=475, y=708, width=650, height=175, radius=22),
                    placeholder="SPlayer 悬浮卡",
                ),
            ],
        ),
    }
