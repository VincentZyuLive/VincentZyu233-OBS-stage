from __future__ import annotations

import httpx

import obs_stage.bili_status as status_module
from obs_stage.bili_status import BilibiliStatusService


def payload() -> dict:
    return {
        "code": 0,
        "message": "ok",
        "data": {
            "uid": 34318934,
            "room_id": 5861873,
            "attention": 698,
            "online": 19,
            "live_status": 1,
            "parent_area_name": "知识",
            "area_name": "自习室",
            "title": "进行严肃的vibe捏",
            "live_time": "2026-11-02 08:03:29",
        },
    }


async def test_bilibili_status_parses_and_caches() -> None:
    calls = 0

    async def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        assert request.url.params["room_id"] == "5861873"
        return httpx.Response(200, json=payload())

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    service = BilibiliStatusService(client)
    first = await service.get_status("5861873", 10)
    second = await service.get_status("5861873", 10)
    await client.aclose()

    assert calls == 1
    assert first["available"] is True
    assert first["live_status"] == 1
    assert first["status_text"] == "直播中"
    assert first["area_name"] == "知识 · 自习室"
    assert first["online"] == 19
    assert first["followers"] == 698
    assert second["stale"] is False


async def test_bilibili_status_uses_stale_cache_after_failure(monkeypatch) -> None:
    clock = [0.0]
    monkeypatch.setattr(status_module.time, "monotonic", lambda: clock[0])
    fail = [False]

    async def handler(request: httpx.Request) -> httpx.Response:
        if fail[0]:
            raise httpx.ConnectError("offline", request=request)
        return httpx.Response(200, json=payload())

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    service = BilibiliStatusService(client)
    fresh = await service.get_status("5861873", 10)
    fail[0] = True
    clock[0] = 20.0
    stale = await service.get_status("5861873", 10)
    await client.aclose()

    assert fresh["title"] == "进行严肃的vibe捏"
    assert stale["stale"] is True
    assert stale["available"] is True
    assert stale["title"] == fresh["title"]
    assert "offline" in stale["error"]


async def test_bilibili_status_unavailable_without_cache() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, request=request)

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    service = BilibiliStatusService(client)
    result = await service.get_status("5861873", 10)
    await client.aclose()

    assert result["available"] is False
    assert result["stale"] is True
    assert result["status_text"] == "数据不可用"
    assert result["fetched_at"] is None
