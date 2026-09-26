import logging, subprocess
from typing import Optional
from pathlib import Path
from config import AppConfig

class CameraError(RuntimeError): pass

def capture_jpeg(config: AppConfig) -> Path:
    path = config.capture_path
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([config.capture_command, "-o", str(path), "--nopreview"], check=True, timeout=20, capture_output=True)
        if not path.is_file() or path.stat().st_size == 0: raise CameraError("JPEG rỗng hoặc không tồn tại")
        return path
    except (OSError, subprocess.SubprocessError) as exc:
        raise CameraError("Không chụp được ảnh") from exc

def delete_file_if_exists(path: Optional[Path]) -> None:
    if path is not None:
        try: path.unlink(missing_ok=True)
        except OSError: logging.getLogger(__name__).warning("Không xóa được ảnh tạm: %s", path)
