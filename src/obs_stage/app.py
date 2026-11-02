from __future__ import annotations

import asyncio
import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated, Any

from fastapi import FastAPI, File, HTTPException, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse

from .bili_status import BilibiliStatusService
from .config import ConfigStore
from .models import AppConfig, ObsApplyRequest, ObsRequest, SceneId
from .obs_ws import ObsController, ObsError
from .renderer import BackgroundRenderer
from .storage import MAX_AVATAR_BYTES, AvatarStore

STATIC_DIR = Path(__file__).parent / "static"


class BroadcastHub:
    def __init__(self) -> None:
        self.clients: set[WebSocket] = set()

    async def add(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.clients.add(websocket)

    def remove(self, websocket: WebSocket) -> None:
        self.clients.discard(websocket)

    async def broadcast(self, payload: object) -> None:
        dead: list[WebSocket] = []
        for client in tuple(self.clients):
            try:
                await client.send_json(payload)
            except Exception:
                dead.append(client)
        for client in dead:
            self.clients.discard(client)


class Runtime:
    def __init__(self, store: ConfigStore, port: int) -> None:
        self.store = store
        self.port = port
        self.config = store.load()
        self.avatar = AvatarStore(store.data_dir)
        self.renderer = BackgroundRenderer(store.data_dir)
        self.obs = ObsController(self.config.obs.url)
        self.bili_status = BilibiliStatusService()
        self.hub = BroadcastHub()

    def save_config(self, config: AppConfig) -> None:
        self.store.save(config)
        self.config = config
        self.obs = ObsController(config.obs.url)

    def stage_url(self, scene: SceneId) -> str:
        return f"http://127.0.0.1:{self.port}/stage/{scene.value}"


def create_app(runtime: Runtime) -> FastAPI:
    @asynccontextmanager
    async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
        try:
            yield
        finally:
            await runtime.bili_status.close()

    app = FastAPI(title="OBS Stage", lifespan=lifespan)
    app.state.runtime = runtime

    def render_shell(filename: str) -> HTMLResponse:
        html = (STATIC_DIR / filename).read_text(encoding="utf-8")
        version = (
            str(time.time_ns() // 1_000_000)
            if runtime.config.assets.cache_bust
            else "stable"
        )
        return HTMLResponse(
            html.replace("__ASSET_VERSION__", version),
            headers={"Cache-Control": "no-store"},
        )

    @app.get("/", include_in_schema=False)
    async def index() -> RedirectResponse:
        return RedirectResponse("/admin")

    @app.get("/admin", include_in_schema=False)
    async def admin_page() -> HTMLResponse:
        return render_shell("admin.html")

    @app.get("/stage/{scene}", include_in_schema=False)
    async def stage_page(scene: SceneId) -> HTMLResponse:
        if scene not in runtime.config.layouts:
            raise HTTPException(status_code=404, detail="未知场景")
        return render_shell("stage.html")

    @app.get("/static/{path:path}", include_in_schema=False)
    async def static_file(path: str) -> FileResponse:
        root = STATIC_DIR.resolve()
        target = (root / path).resolve()
        if not target.is_relative_to(root) or not target.is_file():
            raise HTTPException(status_code=404)
        cache = (
            "public, max-age=31536000, immutable"
            if target.suffix.lower() in {".ttf", ".otf", ".woff", ".woff2"}
            else "no-cache"
        )
        return FileResponse(target, headers={"Cache-Control": cache})

    @app.get("/api/config")
    async def get_config() -> dict[str, Any]:
        return {
            "config": runtime.config.model_dump(mode="json"),
            "avatar_revision": runtime.avatar.revision(),
            "stage_urls": {
                scene.value: runtime.stage_url(scene) for scene in SceneId
            },
            "hud_stage_urls": {
                scene.value: {
                    mode: f"{runtime.stage_url(scene)}?hud={mode}"
                    for mode in ("corner", "bottom", "top", "none")
                }
                for scene in SceneId
            },
        }

    @app.put("/api/config")
    async def put_config(config: AppConfig) -> AppConfig:
        runtime.save_config(config)
        await runtime.hub.broadcast(
            {"type": "config", "payload": runtime.config.model_dump(mode="json")}
        )
        return runtime.config

    @app.get("/api/avatar", include_in_schema=False)
    async def get_avatar() -> FileResponse:
        if not runtime.avatar.exists():
            raise HTTPException(status_code=404)
        return FileResponse(
            runtime.avatar.path,
            media_type="image/png",
            headers={"Cache-Control": "no-cache"},
        )

    @app.post("/api/avatar")
    async def upload_avatar(file: Annotated[UploadFile, File()]) -> dict[str, str]:
        data = await file.read(MAX_AVATAR_BYTES + 1)
        try:
            runtime.avatar.save(data)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        await runtime.hub.broadcast(
            {"type": "config", "payload": runtime.config.model_dump(mode="json")}
        )
        return {"revision": runtime.avatar.revision()}

    @app.delete("/api/avatar")
    async def delete_avatar() -> dict[str, object]:
        runtime.avatar.reset()
        await runtime.hub.broadcast(
            {"type": "config", "payload": runtime.config.model_dump(mode="json")}
        )
        return {"ok": True, "revision": runtime.avatar.revision()}

    @app.get("/api/background/{scene}.png", include_in_schema=False)
    async def background(scene: SceneId) -> FileResponse:
        if scene not in runtime.config.layouts:
            raise HTTPException(status_code=404, detail="未知场景")
        path = await asyncio.to_thread(runtime.renderer.render, scene, runtime.config)
        return FileResponse(path, media_type="image/png", headers={"Cache-Control": "no-store"})

    @app.get("/api/live-status")
    async def live_status() -> dict[str, Any]:
        return await runtime.bili_status.get_status(
            runtime.config.status.room_id,
            runtime.config.status.refresh_seconds,
        )

    @app.post("/api/obs/test")
    async def obs_test(payload: ObsRequest) -> dict[str, Any]:
        try:
            return await runtime.obs.test_connection(payload.password)
        except ObsError as exc:
            raise HTTPException(status_code=502, detail=str(exc)) from exc

    @app.post("/api/obs/preview/{scene}")
    async def obs_preview(scene: SceneId, payload: ObsRequest) -> dict[str, str]:
        try:
            image = await runtime.obs.capture_scene(scene, payload.password)
        except ObsError as exc:
            raise HTTPException(status_code=502, detail=str(exc)) from exc
        return {"image": image}

    @app.post("/api/obs/apply")
    async def obs_apply(payload: ObsApplyRequest) -> dict[str, Any]:
        scenes = [payload.scene] if payload.scene is not None else list(SceneId)
        applied = []
        try:
            for scene in scenes:
                background_path = await asyncio.to_thread(
                    runtime.renderer.render, scene, runtime.config
                )
                applied.append(
                    await runtime.obs.apply_scene(
                        scene,
                        background_path,
                        runtime.stage_url(scene),
                        payload.password,
                    )
                )
        except ObsError as exc:
            raise HTTPException(status_code=502, detail=str(exc)) from exc
        return {"applied": applied}

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket) -> None:
        await runtime.hub.add(websocket)
        try:
            await websocket.send_json(
                {"type": "config", "payload": runtime.config.model_dump(mode="json")}
            )
            while True:
                message = await websocket.receive_text()
                if message == "ping":
                    await websocket.send_json({"type": "pong", "time": int(time.time() * 1000)})
        except WebSocketDisconnect:
            pass
        finally:
            runtime.hub.remove(websocket)

    return app
