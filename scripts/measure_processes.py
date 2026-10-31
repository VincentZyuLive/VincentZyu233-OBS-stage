#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["psutil>=6.0"]
# ///
"""Sample RSS, USS and CPU usage for processes by name or PID."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import psutil


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Cross-platform process sampler.")
    parser.add_argument("--name", action="append", default=[], help="Process name; repeatable.")
    parser.add_argument("--pid", action="append", type=int, default=[], help="PID; repeatable.")
    parser.add_argument("--include-children", action="store_true")
    parser.add_argument("--seconds", type=float, default=10.0)
    parser.add_argument("--interval", type=float, default=1.0)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if not args.name and not args.pid:
        args.name = ["obs-browser-page"]
    if args.seconds <= 0 or args.interval <= 0:
        parser.error("--seconds and --interval must be greater than zero")
    return args


def candidates(process: psutil.Process) -> set[str]:
    values: set[str] = set()
    try:
        values.add(process.name())
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass
    for getter in (process.exe, lambda: process.cmdline()[0]):
        try:
            value = getter()
        except (psutil.NoSuchProcess, psutil.AccessDenied, IndexError):
            continue
        if value:
            values.add(Path(value).name)
    return {Path(value).stem.casefold() for value in values if value}


def find_processes(
    names: list[str], pids: list[int], include_children: bool
) -> list[psutil.Process]:
    wanted = {Path(name).stem.casefold() for name in names}
    found: dict[int, psutil.Process] = {}
    if wanted:
        for process in psutil.process_iter():
            if candidates(process) & wanted:
                found[process.pid] = process
    for pid in pids:
        try:
            process = psutil.Process(pid)
        except psutil.NoSuchProcess:
            continue
        found[process.pid] = process
        if include_children:
            try:
                for child in process.children(recursive=True):
                    found[child.pid] = child
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
    return list(found.values())


def cpu_seconds(process: psutil.Process) -> float:
    times = process.cpu_times()
    return float(times.user + times.system)


def memory_mb(process: psutil.Process) -> tuple[float, float]:
    info = process.memory_full_info()
    rss = float(info.rss) / 1024 / 1024
    uss = float(getattr(info, "uss", getattr(info, "private", info.rss))) / 1024 / 1024
    return rss, uss


def sample(args: argparse.Namespace) -> dict[str, Any]:
    processes = find_processes(args.name, args.pid, args.include_children)
    if not processes:
        raise RuntimeError("No matching processes")
    initial_cpu = {}
    for process in processes:
        try:
            initial_cpu[process.pid] = cpu_seconds(process)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    rss_samples: list[float] = []
    uss_samples: list[float] = []
    started = time.monotonic()
    while True:
        rss_total = 0.0
        uss_total = 0.0
        for process in processes:
            try:
                rss, uss = memory_mb(process)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
            rss_total += rss
            uss_total += uss
        if rss_total:
            rss_samples.append(rss_total)
            uss_samples.append(uss_total)
        elapsed = time.monotonic() - started
        if elapsed >= args.seconds:
            break
        time.sleep(min(args.interval, args.seconds - elapsed))

    elapsed = time.monotonic() - started
    per_process = []
    cpu_delta_total = 0.0
    for process in processes:
        try:
            final_cpu = cpu_seconds(process)
            rss, uss = memory_mb(process)
            name = process.name()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
        delta = max(0.0, final_cpu - initial_cpu.get(process.pid, final_cpu))
        cpu_delta_total += delta
        per_process.append(
            {
                "pid": process.pid,
                "name": name,
                "rss_mb": round(rss, 1),
                "uss_mb": round(uss, 1),
                "cpu_single_core_pct": round(delta / elapsed * 100, 2),
            }
        )

    logical_cpus = psutil.cpu_count(logical=True) or os.cpu_count() or 1
    single_core_pct = cpu_delta_total / elapsed * 100
    return {
        "started_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(elapsed, 2),
        "matched_processes": len(per_process),
        "rss_average_mb": round(sum(rss_samples) / len(rss_samples), 1),
        "rss_peak_mb": round(max(rss_samples), 1),
        "uss_average_mb": round(sum(uss_samples) / len(uss_samples), 1),
        "uss_peak_mb": round(max(uss_samples), 1),
        "cpu_single_core_pct": round(single_core_pct, 2),
        "cpu_all_cores_pct": round(single_core_pct / logical_cpus, 2),
        "logical_cpus": logical_cpus,
        "processes": per_process,
    }


def print_table(result: dict[str, Any]) -> None:
    print(f"Duration: {result['duration_seconds']} s")
    print(f"Logical CPUs: {result['logical_cpus']}")
    print(
        f"Memory: RSS avg {result['rss_average_mb']} MB / peak {result['rss_peak_mb']} MB; "
        f"USS avg {result['uss_average_mb']} MB / peak {result['uss_peak_mb']} MB"
    )
    print(
        f"CPU: {result['cpu_single_core_pct']}% of one core, "
        f"{result['cpu_all_cores_pct']}% of all cores"
    )
    print(f"\n{'PID':>8}  {'NAME':<24} {'RSS MB':>9} {'USS MB':>9} {'CPU %':>8}")
    for process in result["processes"]:
        print(
            f"{process['pid']:>8}  {process['name']:<24} "
            f"{process['rss_mb']:>9.1f} {process['uss_mb']:>9.1f} "
            f"{process['cpu_single_core_pct']:>8.2f}"
        )


def main() -> int:
    args = parse_args()
    try:
        result = sample(args)
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_table(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
