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
