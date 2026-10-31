from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

import obs_stage.obs_ws as obs_module
from obs_stage.models import SceneId
from obs_stage.obs_ws import ObsController


class FakeStatus:
    comment = ""


class FakeResponse:
    requestStatus = FakeStatus()

    def __init__(self, data: dict[str, Any] | None = None) -> None:
        self.responseData = data or {}

    def ok(self) -> bool:
        return True


class FakeClient:
    calls: list[tuple[str, dict[str, Any]]] = []

    def __init__(self, url: str, password: str) -> None:
        self.url = url
        self.password = password

    async def connect(self) -> bool:
        return True

    async def wait_until_identified(self, timeout: int = 10) -> bool:
        return True

    async def disconnect(self) -> bool:
        return True

    async def call(self, request: Any) -> FakeResponse:
        request_type = request.requestType
        data = request.requestData or {}
        self.calls.append((request_type, data))
        if request_type == "GetSceneList":
            return FakeResponse(
                {
                    "currentProgramSceneName": "full-screen",
                    "scenes": [
                        {"sceneName": "full-screen"},
                        {"sceneName": "half-screen"},
                        {"sceneName": "no-screen"},
                    ],
                }
            )
        if request_type == "GetInputList":
            return FakeResponse({"inputs": []})
        if request_type == "GetSceneItemId":
            source_name = data["sourceName"]
            return FakeResponse({"sceneItemId": 1 if source_name.startswith("Stage BG") else 2})
        if request_type == "GetSceneItemList":
            return FakeResponse(
                {
                    "sceneItems": [
                        {"sourceName": "Stage BG [full-screen]"},
                        {"sourceName": "显示器采集"},
                        {"sourceName": "浏览器"},
                        {"sourceName": "Stage Frame [full-screen]"},
                        {"sourceName": "浏览器 2"},
                    ]
                }
            )
        if request_type == "GetSourceScreenshot":
            return FakeResponse({"imageData": "data:image/png;base64,AAAA"})
        return FakeResponse({})


async def test_apply_scene_creates_only_stage_sources(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    FakeClient.calls = []
    monkeypatch.setattr(obs_module.simpleobsws, "WebSocketClient", FakeClient)
    controller = ObsController("ws://127.0.0.1:4455")
    background = tmp_path / "background.png"
    background.write_bytes(b"png")
    result = await controller.apply_scene(
        SceneId.FULL_SCREEN,
        background,
        "http://127.0.0.1:6162/stage/full-screen",
        "secret",
    )
    assert result["background"] == "Stage BG [full-screen]"
    creates = [data for name, data in FakeClient.calls if name == "CreateInput"]
    assert [item["inputKind"] for item in creates] == ["image_source", "browser_source"]
    assert all(item["inputName"].startswith("Stage ") for item in creates)
    assert any(name == "SetSceneItemIndex" for name, _ in FakeClient.calls)


async def test_test_connection_and_screenshot(monkeypatch: pytest.MonkeyPatch) -> None:
    FakeClient.calls = []
    monkeypatch.setattr(obs_module.simpleobsws, "WebSocketClient", FakeClient)
    controller = ObsController("ws://127.0.0.1:4455")
    status = await controller.test_connection("secret")
    assert status["current_scene"] == "full-screen"
    image = await controller.capture_scene(SceneId.HALF_SCREEN, "secret")
    assert image.startswith("data:image/png;base64,")
