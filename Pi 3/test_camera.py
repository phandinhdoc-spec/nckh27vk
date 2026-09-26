#!/usr/bin/env python3
"""Kiểm tra rpicam-jpeg độc lập, không chạy ứng dụng chính."""

from __future__ import annotations

import shutil
import signal
import subprocess
import sys
import time

from devices import _CAMERA_HEIGHT, _CAMERA_RAM_DIR, _CAMERA_TIMEOUT_MS, _CAMERA_WIDTH


OUTPUT = _CAMERA_RAM_DIR / "thiennhan-camera-test.jpg"
TESTS = (
    ("timeout như capture_jpeg", ["--timeout", str(_CAMERA_TIMEOUT_MS)]),
    ("timeout 2 giây", ["--timeout", "2000"]),
    ("chụp ngay", ["--immediate"]),
)


def print_command(name: str, command: list[str]) -> None:
    print(f"\n--- {name} ---", flush=True)
    try:
        result = subprocess.run(command, capture_output=True, timeout=8, check=False)
        output = (result.stdout + result.stderr).decode("utf-8", errors="replace").strip()
        print(output or f"Không có output, mã thoát {result.returncode}", flush=True)
    except (OSError, subprocess.TimeoutExpired) as error:
        print(f"Không chạy được: {error}", flush=True)


def print_system_info(camera: str) -> None:
    print_command("Hệ điều hành", ["uname", "-a"])
    print_command("Phiên bản rpicam", [camera, "--version"])
    print_command(
        "Gói camera",
        [
            "dpkg-query",
            "-W",
            "-f=${binary:Package}\t${Version}\t${Architecture}\n",
            "rpicam*",
            "libcamera*",
        ],
    )
    print_command("Thư viện đang liên kết", ["ldd", camera])
    hello = shutil.which("rpicam-hello")
    if hello:
        print_command("Danh sách camera", [hello, "--list-cameras"])


def run_test(camera: str, name: str, mode: list[str]) -> bool:
    OUTPUT.unlink(missing_ok=True)
    command = [
        camera,
        "--output",
        str(OUTPUT),
        "--width",
        str(_CAMERA_WIDTH),
        "--height",
        str(_CAMERA_HEIGHT),
        *mode,
        "--nopreview",
    ]
    print(f"\n=== {name} ===", flush=True)
    print("Lệnh:", " ".join(command), flush=True)
    started = time.monotonic()
    try:
        result = subprocess.run(command, capture_output=True, timeout=12, check=False)
    except subprocess.TimeoutExpired:
        OUTPUT.unlink(missing_ok=True)
        print("KẾT QUẢ: LỖI - tiến trình quá 12 giây", flush=True)
        return False

    stderr = result.stderr.decode("utf-8", errors="replace").strip()
    data = OUTPUT.read_bytes() if OUTPUT.exists() else b""
    is_jpeg = data.startswith(b"\xff\xd8")
    valid = result.returncode == 0 and is_jpeg
    print(f"Mã thoát: {result.returncode}", flush=True)
    if result.returncode < 0:
        print(f"Tín hiệu: {signal.Signals(-result.returncode).name}", flush=True)
    print(f"Thời gian: {time.monotonic() - started:.2f} giây", flush=True)
    print(f"Kích thước: {len(data)} byte", flush=True)
    print(f"JPEG hợp lệ: {'có' if is_jpeg else 'không'}", flush=True)
    if stderr:
        print("stderr:\n" + stderr, flush=True)
    print(f"KẾT QUẢ: {'OK' if valid else 'LỖI'}", flush=True)
    OUTPUT.unlink(missing_ok=True)
    return valid


def main() -> int:
    camera = shutil.which("rpicam-jpeg")
    if camera is None:
        print("LỖI: Không tìm thấy lệnh rpicam-jpeg.", file=sys.stderr)
        return 2
    if not OUTPUT.parent.is_dir():
        print("LỖI: Không có /dev/shm để lưu ảnh trong RAM.", file=sys.stderr)
        return 2

    print(f"Camera command: {camera}", flush=True)
    print_system_info(camera)
    passed = [name for name, mode in TESTS if run_test(camera, name, mode)]
    print("\n=== TỔNG KẾT ===", flush=True)
    print("Thành công: " + (", ".join(passed) if passed else "không có"), flush=True)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
