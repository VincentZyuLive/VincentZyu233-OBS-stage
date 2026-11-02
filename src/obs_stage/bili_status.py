from __future__ import annotations

import asyncio
import time
from datetime import datetime
from typing import Any

import httpx

LIVE_API = "https://api.live.bilibili.com/room/v1/Room/get_info"


class BilibiliStatusError(RuntimeError):
    pass


class BilibiliStatusService:
    def __init__(self, client: httpx.AsyncClient | None = None) -> None:
        self._client = client or httpx.AsyncClient(timeout=4.0)
        self._owns_client = client is None
        self._cache: dict[str, Any] | None = None
        self._cache_at = 0.0
        self._cache_room_id = ""
        self._lock = asyncio.Lock()

    async def close(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    async def get_status(self, room_id: str, refresh_seconds: int) -> dict[str, Any]:
        normalized_room = room_id.strip()
        if not normalized_room:
            return self._unavailable("", "直播间号未配置")

        now = time.monotonic()
        if self._has_fresh_cache(normalized_room, refresh_seconds, now):
            return dict(self._cache or {})

        async with self._lock:
            now = time.monotonic()
            if self._has_fresh_cache(normalized_room, refresh_seconds, now):
                return dict(self._cache or {})
            try:
                result = await self._fetch(normalized_room, refresh_seconds)
            except Exception as exc:
                if self._cache is not None and self._cache_room_id == normalized_room:
                    stale = dict(self._cache)
                    stale.update(
                        {
                            "stale": True,
                            "error": str(exc),
                            "refresh_seconds": refresh_seconds,
                        }
                    )
                    return stale
                return self._unavailable(normalized_room, str(exc), refresh_seconds)
            self._cache = result
            self._cache_at = time.monotonic()
            self._cache_room_id = normalized_room
            return dict(result)

    def _has_fresh_cache(self, room_id: str, refresh_seconds: int, now: float) -> bool:
        return bool(
            self._cache is not None
            and self._cache_room_id == room_id
            and now - self._cache_at < max(1, refresh_seconds)
        )

    async def _fetch(self, room_id: str, refresh_seconds: int) -> dict[str, Any]:
        response = await self._client.get(
            LIVE_API,
            params={"room_id": room_id},
            headers={
                "User-Agent": "Mozilla/5.0 VincentZyu-OBS-Stage",
                "Referer": f"https://live.bilibili.com/{room_id}",
            },
        )
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, dict) or payload.get("code") != 0:
            message = payload.get("message") or payload.get("msg") or "B站接口返回错误"
            raise BilibiliStatusError(str(message))
        data = payload.get("data")
        if not isinstance(data, dict):
            raise BilibiliStatusError("B站接口缺少 room data")

        live_status = self._int_value(data.get("live_status"))
        parent_area = str(data.get("parent_area_name") or "").strip()
        area = str(data.get("area_name") or "").strip()
        area_name = " · ".join(part for part in (parent_area, area) if part)
        return {
            "available": True,
            "stale": False,
            "room_id": str(data.get("room_id") or room_id),
            "uid": self._int_value(data.get("uid")),
            "live_status": live_status,
            "status_text": {0: "未开播", 1: "直播中", 2: "轮播中"}.get(
                live_status, "未知状态"
            ),
            "title": str(data.get("title") or "").strip(),
            "area_name": area_name,
            "online": self._int_value(data.get("online")),
            "followers": self._int_value(data.get("attention")),
            "live_time": str(data.get("live_time") or "").strip(),
            "fetched_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "refresh_seconds": refresh_seconds,
            "error": None,
        }

    @staticmethod
    def _int_value(value: object) -> int:
        try:
            if isinstance(value, (int, float, str, bytes, bytearray)):
                return int(value)
            return int(str(value)) if value is not None else 0
        except (TypeError, ValueError):
            return 0

    @staticmethod
    def _unavailable(
        room_id: str, error: str, refresh_seconds: int = 10
    ) -> dict[str, Any]:
        return {
            "available": False,
            "stale": True,
            "room_id": room_id,
            "uid": 0,
            "live_status": -1,
            "status_text": "数据不可用",
            "title": "",
            "area_name": "",
            "online": 0,
            "followers": 0,
            "live_time": "",
            "fetched_at": None,
            "refresh_seconds": refresh_seconds,
            "error": error,
        }
