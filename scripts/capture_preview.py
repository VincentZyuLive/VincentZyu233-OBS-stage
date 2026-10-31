#!/usr/bin/env python3
"""Capture an OBS scene through the running OBS Stage WebUI."""

from __future__ import annotations

import argparse
import base64
import json
import os
import urllib.request
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("scene", choices=["no-screen", "half-screen", "full-screen"])
    parser.add_argument("--base-url", default="http://127.0.0.1:6162")
    parser.add_argument("--password", default=os.environ.get("OBS_WEBSOCKET_PASSWORD", ""))
    parser.add_argument("--output", type=Path, default=Path("preview.png"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    request = urllib.request.Request(
        f"{args.base_url.rstrip('/')}/api/obs/preview/{args.scene}",
        data=json.dumps({"password": args.password}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.load(response)
    image = data.get("image")
    if not isinstance(image, str) or "," not in image:
        raise RuntimeError("WebUI did not return an image data URL")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(base64.b64decode(image.split(",", 1)[1]))
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
