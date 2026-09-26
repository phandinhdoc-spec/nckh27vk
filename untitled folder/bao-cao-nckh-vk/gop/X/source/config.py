"""Immutable application configuration."""
from dataclasses import dataclass
import os
from pathlib import Path

BUTTON_GPIO_BCM = 25
BUTTON_PHYSICAL_PIN = 22
GROUND_PHYSICAL_PIN = 20
GEMINI_MODEL = "gemini-2.5-flash-lite"
CAPTURE_PATH = Path("/dev/shm/green-eye-capture.jpg")

@dataclass(frozen=True)
class AppConfig:
    api_key: str
    mp3_dir: Path
    capture_path: Path = CAPTURE_PATH
    capture_command: str = "rpicam-jpeg"
    audio_player: str = "mpg123"
    http_timeout: float = 20.0
    retry_count: int = 1
    debounce_seconds: float = 0.1
    audio_timeout: float = 30.0

def load_config() -> AppConfig:
    base = Path(__file__).resolve().parent
    mp3_dir = Path(os.getenv("MP3_DIR", str(base.parent / "mp3"))).resolve()
    cfg = AppConfig(api_key=os.getenv("GEMINI_API_KEY", ""), mp3_dir=mp3_dir,
                    capture_path=Path(os.getenv("CAPTURE_PATH", str(CAPTURE_PATH))))
    validate_config(cfg)
    return cfg

def validate_config(config: AppConfig) -> None:
    if not config.api_key.strip():
        raise ValueError("GEMINI_API_KEY chưa được cấu hình")
    if GEMINI_MODEL != "gemini-2.5-flash-lite":
        raise ValueError("Sai model Gemini")
    if BUTTON_GPIO_BCM != 25 or BUTTON_PHYSICAL_PIN != 22 or GROUND_PHYSICAL_PIN != 20:
        raise ValueError("Sai sơ đồ GPIO")
    if not 0.05 <= config.debounce_seconds <= 0.15 or config.http_timeout <= 0:
        raise ValueError("Cấu hình timeout/debounce không hợp lệ")

def build_gemini_endpoint(config: AppConfig) -> str:
    from urllib.parse import urlencode
    return f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?{urlencode({'key': config.api_key})}"
