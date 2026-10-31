from __future__ import annotations

import argparse
import threading
import webbrowser
from pathlib import Path

import uvicorn

from . import __version__
from .app import Runtime, create_app
from .config import ConfigStore


def parse_args() -> argparse.Namespace:
    return build_parser().parse_args()


def _open_browser(port: int) -> None:
    timer = threading.Timer(1.2, lambda: webbrowser.open(f"http://127.0.0.1:{port}/admin"))
    timer.daemon = True
    timer.start()


def main(argv: list[str] | None = None) -> int:
    args = parse_args() if argv is None else build_parser().parse_args(argv)
    if not 1 <= args.port <= 65535:
        raise SystemExit("--port must be between 1 and 65535")
    store = ConfigStore(args.data_dir)
    runtime = Runtime(store, args.port)
    app = create_app(runtime)
    if not args.no_browser:
        _open_browser(args.port)
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=args.port,
        log_level="info" if args.verbose else "warning",
        access_log=args.verbose,
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="obs-stage",
        description="Editable watercolor stage overlays for OBS Browser Source.",
    )
    parser.add_argument("--data-dir", type=Path, help="Override the application data directory.")
    parser.add_argument("--port", type=int, default=6162, help="Local WebUI port. Default: 6162")
    parser.add_argument("--no-browser", action="store_true", help="Do not open the admin page.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose server logs.")
    parser.add_argument("--version", action="version", version=__version__)
    return parser
