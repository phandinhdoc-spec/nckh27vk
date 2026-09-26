#!/usr/bin/env python3
import json
import os
import subprocess
import tempfile
import time
import urllib.request
from pathlib import Path

SERVER_URL = os.getenv("SERVER_URL", "http://127.0.0.1:8765").rstrip("/")
BUTTON_PIN = int(os.getenv("BUTTON_PIN", "17"))
MP3_DIR = Path(os.getenv("MP3_DIR", Path(__file__).with_name("audio")))
CODES = {"RHC", "RVC", "RNH", "RKH", "RK"}


def capture(path: str) -> None:
    subprocess.run(
        ["rpicam-jpeg", "-n", "-t", "1", "--width", "640", "--height", "480", "-o", path],
        check=True,
        timeout=15,
    )


def classify(path: str) -> str:
    data = Path(path).read_bytes()
    request = urllib.request.Request(
        f"{SERVER_URL}/classify", data=data, method="POST", headers={"Content-Type": "image/jpeg"}
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        code = json.loads(response.read())["code"]
    return code if code in CODES else "RK"


def play(code: str) -> None:
    subprocess.run(["mpg123", "-q", str(MP3_DIR / f"{code}.mp3")], check=True, timeout=15)


def handle_press() -> None:
    path = ""
    try:
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False, dir="/dev/shm") as image:
            path = image.name
        capture(path)
        play(classify(path))
    except Exception as error:
        print(f"Green Eye error: {error}", flush=True)
    finally:
        if path:
            Path(path).unlink(missing_ok=True)


def self_test() -> None:
    assert CODES == {"RHC", "RVC", "RNH", "RKH", "RK"}
    assert all((MP3_DIR / f"{code}.mp3").is_file() for code in CODES)
    print("self-test: ok")


def main() -> None:
    from gpiozero import Button

    button = Button(BUTTON_PIN, pull_up=True, bounce_time=0.15)
    print(f"Green Eye ready: GPIO {BUTTON_PIN} -> {SERVER_URL}", flush=True)
    while True:
        button.wait_for_press()
        handle_press()
        button.wait_for_release()
        time.sleep(0.1)


if __name__ == "__main__":
    if "--self-test" in os.sys.argv:
        self_test()
    else:
        main()
