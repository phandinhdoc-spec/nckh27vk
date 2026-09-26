from __future__ import annotations

import os
import sys
import threading
import time
import uuid
from collections import deque
from datetime import datetime, timezone
from pathlib import Path


_KEEP_SECONDS = 7 * 24 * 60 * 60
_CHECK_INTERVAL_SECONDS = 2
_CPU_SAMPLE_SECONDS = 0.25


class History:
    def __init__(
        self,
        root: Path,
        *,
        cpu_idle_percent: int,
        ram_available_percent: int,
    ) -> None:
        self.root = root
        self.cpu_idle_percent = cpu_idle_percent
        self.ram_available_percent = ram_available_percent
        self._items: deque[tuple[str, bytes, float]] = deque()
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, name="history-writer", daemon=True)
        self._thread.start()

    def add_image(self, data: bytes, transmitted_at: float) -> None:
        self._add("image", data, transmitted_at)

    def add_sound(self, data: bytes, played_at: float) -> None:
        self._add("sound", data, played_at)

    def close(self) -> None:
        self._stop.set()
        self._thread.join(timeout=1)

    def _add(self, kind: str, data: bytes, event_time: float) -> None:
        if not data:
            return
        with self._lock:
            self._items.append((kind, data, event_time))

    def _run(self) -> None:
        while not self._stop.wait(_CHECK_INTERVAL_SECONDS):
            if self._memory_is_low() or self._cpu_is_idle():
                self._flush()
                self._prune()

    def _flush(self) -> None:
        while True:
            with self._lock:
                if not self._items:
                    return
                item = self._items[0]
            try:
                self._write(*item)
            except OSError as error:
                print(f"Không thể lưu history: {error}", file=sys.stderr)
                return
            with self._lock:
                self._items.popleft()

    def _write(self, kind: str, data: bytes, event_time: float) -> None:
        directory = self.root / kind
        directory.mkdir(parents=True, exist_ok=True)
        stamp = datetime.fromtimestamp(event_time, timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
        extension = ".jpg" if kind == "image" else ".mp3"
        destination = directory / f"{stamp}-{uuid.uuid4().hex[:8]}{extension}"
        temporary = destination.with_suffix(destination.suffix + ".tmp")
        try:
            temporary.write_bytes(data)
            os.replace(temporary, destination)
            os.utime(destination, (event_time, event_time))
        finally:
            temporary.unlink(missing_ok=True)

    def _prune(self) -> None:
        cutoff = time.time() - _KEEP_SECONDS
        for kind in ("image", "sound"):
            directory = self.root / kind
            if not directory.exists():
                continue
            for path in directory.iterdir():
                try:
                    if path.is_file() and path.stat().st_mtime < cutoff:
                        path.unlink()
                except OSError as error:
                    print(f"Không thể xóa history cũ {path}: {error}", file=sys.stderr)

    def _memory_is_low(self) -> bool:
        values: dict[str, int] = {}
        try:
            for line in Path("/proc/meminfo").read_text(encoding="ascii").splitlines():
                key, separator, rest = line.partition(":")
                if separator and key in {"MemTotal", "MemAvailable"}:
                    values[key] = int(rest.split()[0])
        except (OSError, ValueError, IndexError):
            return False
        total = values.get("MemTotal", 0)
        available = values.get("MemAvailable", 0)
        return total > 0 and available * 100 / total <= self.ram_available_percent

    def _cpu_is_idle(self) -> bool:
        first = _cpu_times()
        if first is None or self._stop.wait(_CPU_SAMPLE_SECONDS):
            return False
        second = _cpu_times()
        if second is None:
            return False
        idle_delta = second[0] - first[0]
        total_delta = second[1] - first[1]
        return total_delta > 0 and idle_delta * 100 / total_delta >= self.cpu_idle_percent


def _cpu_times() -> tuple[int, int] | None:
    try:
        fields = Path("/proc/stat").read_text(encoding="ascii").splitlines()[0].split()[1:]
        values = [int(value) for value in fields]
    except (OSError, ValueError, IndexError):
        return None
    idle = values[3] + (values[4] if len(values) > 4 else 0)
    return idle, sum(values)
