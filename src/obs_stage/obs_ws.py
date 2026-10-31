from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import simpleobsws

from .models import SceneId


class ObsError(RuntimeError):
    pass


class ObsController:
    def __init__(self, url: str) -> None:
        self.url = url

    def _password(self, supplied: str) -> str:
        return supplied or os.environ.get("OBS_WEBSOCKET_PASSWORD", "")

    async def _connect(self, password: str) -> simpleobsws.WebSocketClient:
        client = simpleobsws.WebSocketClient(url=self.url, password=self._password(password))
        if not await client.connect():
            raise ObsError("无法连接 OBS WebSocket")
        if not await client.wait_until_identified(timeout=10):
            await client.disconnect()
            raise ObsError("OBS WebSocket 身份验证失败，请检查密码")
        return client

    async def _call(
        self,
        client: simpleobsws.WebSocketClient,
        request_type: str,
        request_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        response = await client.call(simpleobsws.Request(request_type, request_data))
        if not response.ok():
            comment = response.requestStatus.comment or "unknown OBS error"
            raise ObsError(f"{request_type} 失败：{comment}")
        return response.responseData or {}

    async def test_connection(self, password: str) -> dict[str, Any]:
        client = await self._connect(password)
        try:
            version = await self._call(client, "GetVersion")
            scenes = await self._call(client, "GetSceneList")
            return {
                "obs_version": version.get("obsVersion"),
                "websocket_version": version.get("obsWebSocketVersion"),
                "current_scene": scenes.get("currentProgramSceneName"),
                "scenes": [item.get("sceneName") for item in scenes.get("scenes", [])],
            }
        finally:
            await client.disconnect()

    async def _ensure_input(
        self,
        client: simpleobsws.WebSocketClient,
        scene_name: str,
        input_name: str,
        input_kind: str,
        settings: dict[str, Any],
    ) -> None:
        inputs = await self._call(client, "GetInputList")
        names = {item.get("inputName") for item in inputs.get("inputs", [])}
        if input_name in names:
            await self._call(
                client,
                "SetInputSettings",
                {"inputName": input_name, "inputSettings": settings, "overlay": True},
            )
            return
        await self._call(
            client,
            "CreateInput",
            {
                "sceneName": scene_name,
                "inputName": input_name,
                "inputKind": input_kind,
                "inputSettings": settings,
                "sceneItemEnabled": True,
            },
        )

    async def _scene_item_id(
        self, client: simpleobsws.WebSocketClient, scene_name: str, source_name: str
    ) -> int:
        data = await self._call(
            client,
            "GetSceneItemId",
            {"sceneName": scene_name, "sourceName": source_name},
        )
        return int(data["sceneItemId"])

    async def _place_full_canvas(
        self, client: simpleobsws.WebSocketClient, scene_name: str, source_name: str
    ) -> int:
        item_id = await self._scene_item_id(client, scene_name, source_name)
        await self._call(
            client,
            "SetSceneItemTransform",
            {
                "sceneName": scene_name,
                "sceneItemId": item_id,
                "sceneItemTransform": {
                    "positionX": 0,
                    "positionY": 0,
                    "rotation": 0,
                    "scaleX": 1,
                    "scaleY": 1,
                    "alignment": 5,
                    "boundsType": "OBS_BOUNDS_NONE",
                },
            },
        )
        return item_id

    async def apply_scene(
        self,
        scene: SceneId,
        background_path: Path,
        stage_url: str,
        password: str,
    ) -> dict[str, Any]:
        scene_name = scene.value
        bg_name = f"Stage BG [{scene_name}]"
        frame_name = f"Stage Frame [{scene_name}]"
        client = await self._connect(password)
        try:
            scenes = await self._call(client, "GetSceneList")
            names = {item.get("sceneName") for item in scenes.get("scenes", [])}
            if scene_name not in names:
                raise ObsError(f"OBS 中找不到场景 {scene_name}")

            await self._ensure_input(
                client,
                scene_name,
                bg_name,
                "image_source",
                {"file": str(background_path.resolve()), "unload": False},
            )
            await self._ensure_input(
                client,
                scene_name,
                frame_name,
                "browser_source",
                {
                    "url": stage_url,
                    "width": 1600,
                    "height": 900,
                    "fps_custom": True,
                    "fps": 30,
                    "shutdown": True,
                    "restart_when_active": False,
                    "css": "",
                },
            )
            bg_item = await self._place_full_canvas(client, scene_name, bg_name)
            frame_item = await self._place_full_canvas(client, scene_name, frame_name)

            items = await self._call(client, "GetSceneItemList", {"sceneName": scene_name})
            item_count = len(items.get("sceneItems", []))
            await self._call(
                client,
                "SetSceneItemIndex",
                {"sceneName": scene_name, "sceneItemId": bg_item, "sceneItemIndex": 0},
            )
            items = await self._call(client, "GetSceneItemList", {"sceneName": scene_name})
            source_items = items.get("sceneItems", [])
            protected = next(
                (
                    index
                    for index, item in enumerate(source_items)
                    if "浏览器 2" in str(item.get("sourceName", ""))
                    or "danmaku" in str(item.get("sourceName", "")).lower()
                    or "弹幕" in str(item.get("sourceName", ""))
                ),
                None,
            )
            frame_index = protected if protected is not None else max(1, item_count - 1)
            await self._call(
                client,
                "SetSceneItemIndex",
                {
                    "sceneName": scene_name,
                    "sceneItemId": frame_item,
                    "sceneItemIndex": frame_index,
                },
            )
            return {"scene": scene_name, "background": bg_name, "frame": frame_name}
        finally:
            await client.disconnect()

    async def capture_scene(self, scene: SceneId, password: str) -> str:
        client = await self._connect(password)
        try:
            result = await self._call(
                client,
                "GetSourceScreenshot",
                {
                    "sourceName": scene.value,
                    "imageFormat": "png",
                    "imageWidth": 1280,
                    "imageHeight": 720,
                },
            )
            image_data = result.get("imageData")
            if not isinstance(image_data, str):
                raise ObsError("OBS 没有返回截图数据")
            return image_data
        finally:
            await client.disconnect()
