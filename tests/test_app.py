from __future__ import annotations

from io import BytesIO
from pathlib import Path

from fastapi.testclient import TestClient
from PIL import Image

from obs_stage.app import Runtime, create_app
from obs_stage.config import ConfigStore


def _avatar() -> bytes:
    image = Image.new("RGB", (128, 128), "#7FA8E8")
    output = BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()


def test_pages_config_background_and_avatar(tmp_path: Path) -> None:
    runtime = Runtime(ConfigStore(tmp_path), 6162)
    app = create_app(runtime)
    with TestClient(app) as client:
        assert client.get("/admin").status_code == 200
        assert client.get("/stage/full-screen").status_code == 200
        assert client.get("/stage/unknown").status_code == 422
        config = client.get("/api/config").json()
        assert config["stage_urls"]["no-screen"] == "http://127.0.0.1:6162/stage/no-screen"
        for scene in ("no-screen", "half-screen", "full-screen"):
            for mode in ("corner", "bottom", "top", "none"):
                assert (
                    config["hud_stage_urls"][scene][mode]
                    == f"http://127.0.0.1:6162/stage/{scene}?hud={mode}"
                )
        assert "verbose_stage_urls" not in config
        response = client.get("/api/background/half-screen.png")
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"
        upload = client.post(
            "/api/avatar", files={"file": ("avatar.png", _avatar(), "image/png")}
        )
        assert upload.status_code == 200
        assert client.get("/api/avatar").status_code == 200
        assert client.delete("/api/avatar").status_code == 200


def test_config_can_be_updated(tmp_path: Path) -> None:
    runtime = Runtime(ConfigStore(tmp_path), 6162)
    app = create_app(runtime)
    with TestClient(app) as client:
        config = runtime.config.model_dump(mode="json")
        config["branding"]["title"] = "Updated"
        response = client.put("/api/config", json=config)
        assert response.status_code == 200
        assert response.json()["branding"]["title"] == "Updated"


def test_live_status_api_returns_normalized_status(tmp_path: Path, monkeypatch) -> None:
    runtime = Runtime(ConfigStore(tmp_path), 6162)

    async def fake_status(room_id: str, refresh_seconds: int) -> dict[str, object]:
        assert room_id == "5861873"
        assert refresh_seconds == 10
        return {
            "available": True,
            "stale": False,
            "room_id": room_id,
            "live_status": 1,
            "status_text": "直播中",
            "title": "测试直播",
            "online": 19,
            "followers": 698,
        }

    monkeypatch.setattr(runtime.bili_status, "get_status", fake_status)
    app = create_app(runtime)
    with TestClient(app) as client:
        response = client.get("/api/live-status")
        assert response.status_code == 200
        assert response.json()["status_text"] == "直播中"
        assert response.json()["followers"] == 698
