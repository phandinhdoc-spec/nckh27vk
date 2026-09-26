import subprocess
from pathlib import Path
from config import AppConfig
from messages import FALLBACK_MESSAGE, mp3_filename_for

class AudioError(RuntimeError): pass
def resolve_mp3_path(mp3_dir: Path, filename: str) -> Path:
    root, path = mp3_dir.resolve(), (mp3_dir / filename).resolve()
    if path.parent != root or not path.is_file(): raise AudioError(f"MP3 không hợp lệ: {filename}")
    return path
def play_mp3(path: Path, config: AppConfig) -> None:
    try: subprocess.run([config.audio_player, str(path)], check=True, timeout=config.audio_timeout)
    except (OSError, subprocess.SubprocessError) as exc: raise AudioError("Phát MP3 thất bại") from exc
def play_fallback(config: AppConfig) -> None: play_mp3(resolve_mp3_path(config.mp3_dir, mp3_filename_for(FALLBACK_MESSAGE)), config)
