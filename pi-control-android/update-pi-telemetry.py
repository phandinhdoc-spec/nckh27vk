#!/usr/bin/env python3
"""Update only known Pi 3 sources, backing up first; never edits .env or restarts services."""
import argparse
import hashlib
import os
from pathlib import Path
import shutil
import tempfile
import urllib.request

MANIFEST = {'app.py': {'before': 'c11698d7a0df342d0fff0e43ef6150cde3583b8d456fa35450d8f5403e2848b2', 'after': '52d19816f855cfd27d37e57d67283b1fffa0d9a29be7d272b0472eff428a5aa0'}, 'config.py': {'before': '614f3d545d9616e699d2739e96df75cb31ab791dab316894bebe2abe56bfde12', 'after': 'd062d364138c8aa2c27df322eea1dc5f26f062eadb2fa11e27da96720f89fad1'}, 'sensors.py': {'before': '25f3f778558c2ca4b054e575adbb1f35ffe418f5ebc0dc2fcb584bdc82af3564', 'after': 'ab8b1bb355b0ccd2d759724b4486276a9ce776df685ef4ef653e9454ccf16d6f'}}
BASE = 'https://raw.githubusercontent.com/phandinhdoc-spec/nckh27vk/main/Pi%203/'


def checksum(raw):
    return hashlib.sha256(raw).hexdigest()


def update(directory):
    directory = Path(directory).expanduser().resolve(strict=True)
    originals = {}
    for name, hashes in MANIFEST.items():
        path = directory / name
        if path.is_symlink():
            raise ValueError(f'{name} là symlink; cần kiểm tra thủ công')
        raw = path.read_bytes()
        if checksum(raw) not in hashes.values():
            raise ValueError(f'{name} khác bản Pi 3 đã kiểm tra. Chưa sửa file nào. Cần đối chiếu trước khi cập nhật.')
        originals[name] = raw
    # Download and validate every candidate before touching existing files.
    replacements = {}
    for name, hashes in MANIFEST.items():
        with urllib.request.urlopen(BASE + name, timeout=30) as response:
            raw = response.read(1024 * 1024)
        if checksum(raw) != hashes['after']:
            raise ValueError('Nguồn GitHub đã đổi. Tải lại update-pi-telemetry.py mới nhất rồi thử lại.')
        compile(raw, name, 'exec')
        replacements[name] = raw
    backup = Path(tempfile.mkdtemp(prefix='.pi-control-backup-', dir=directory))
    for name in originals:
        shutil.copy2(directory / name, backup / name)
    changed = []
    try:
        for name, raw in replacements.items():
            path = directory / name
            if path.read_bytes() != originals[name]:
                raise ValueError(f'{name} vừa thay đổi; dừng cập nhật')
            fd, temporary = tempfile.mkstemp(prefix='.pi-control-update-', dir=directory)
            try:
                with os.fdopen(fd, 'wb') as stream:
                    stream.write(raw)
                    stream.flush()
                    os.fsync(stream.fileno())
                info = path.stat()
                os.chown(temporary, info.st_uid, info.st_gid)
                shutil.copystat(path, temporary)
                os.replace(temporary, path)
                changed.append(name)
            finally:
                if os.path.exists(temporary):
                    os.unlink(temporary)
    except Exception:
        for name in changed:
            shutil.copy2(backup / name, directory / name)
        raise
    print('Đã cập nhật 3 file. Bản sao:', backup)
    print('Trong .env thêm: PI_CONTROL_TELEMETRY_PATH=' + str(directory / 'telemetry.json'))
    print('Sau đó restart service ứng dụng Pi đang dùng. Chưa thay .env, chưa restart service.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', nargs='?', default='/root/pi')
    args = parser.parse_args()
    try:
        update(args.directory)
    except Exception as exc:
        parser.exit(1, str(exc) + '\n')
