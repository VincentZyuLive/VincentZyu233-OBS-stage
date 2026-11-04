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
                    rect=Rect(x=190, y=286, width=1221, height=330, radius=33),
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
                    rect=Rect(x=360, y=40, width=1200, height=625, radius=35),
                    placeholder="显示器采集",
                ),
                StageSlot(
                    name="media",
                    label="SPlayer / 播放器",
                    rect=Rect(x=386, y=680, width=629, height=170, radius=24),
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
                    rect=Rect(x=430, y=683, width=740, height=200, radius=22),
                    placeholder="SPlayer 悬浮卡",
                ),
            ],
        ),
    }
