"""Executed on the Pi using SSH; JSON request on stdin. No persistent agent."""
import base64
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import tempfile

LIMIT = 512 * 1024
UPLOAD_LIMIT = 16 * 1024 * 1024


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read_regular(path):
    fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW)
    with os.fdopen(fd, 'rb') as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode):
            raise ValueError('Chỉ mở file thông thường, không mở thiết bị/FIFO/socket')
        raw = stream.read(LIMIT + 1)
    if len(raw) > LIMIT:
        raise ValueError('File vượt giới hạn 512 KiB')
    if b'\0' in raw:
        raise ValueError('File nhị phân không hỗ trợ chỉnh sửa')
    raw.decode('utf-8')
    return raw, info


def upload_state(path):
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW)
    except FileNotFoundError:
        if path.is_symlink():
            raise ValueError('Không ghi đè symlink; nhập đường dẫn file đích thực')
        return None, None
    info = os.fstat(fd)
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        os.close(fd)
        raise ValueError('Chỉ ghi đè file thường có một hard link')
    with os.fdopen(fd, 'rb') as stream:
        raw = stream.read(UPLOAD_LIMIT + 1)
    if len(raw) > UPLOAD_LIMIT:
        raise ValueError('File đích vượt giới hạn ghi đè 16 MiB')
    return raw, info


def upload(data, requested):
    # Resolve parent only; never silently follow a final symlink on overwrite.
    path = requested.parent.resolve(strict=True) / requested.name
    raw, info = upload_state(path)
    revision = digest(raw) if raw is not None else None
    if data['action'] == 'upload_check':
        return {'path': str(path), 'exists': raw is not None, 'revision': revision,
                'bytes': len(raw) if raw is not None else 0}
    if 'revision' not in data or data['revision'] != revision:
        raise ValueError('File đích đã thay đổi. Chọn Tải lên lần nữa để kiểm tra lại.')
    encoded = data.get('base64')
    if not isinstance(encoded, str) or len(encoded) > ((UPLOAD_LIMIT + 2) // 3) * 4:
        raise ValueError('File tải lên vượt 16 MiB hoặc nội dung không hợp lệ')
    try:
        content = base64.b64decode(encoded, validate=True)
    except (ValueError, TypeError):
        raise ValueError('Dữ liệu file không hợp lệ') from None
    if len(content) > UPLOAD_LIMIT:
        raise ValueError('File tải lên vượt 16 MiB')
    temporary = None
    backup = None
    try:
        fd, temporary = tempfile.mkstemp(prefix='.pi-control-upload-', dir=path.parent)
        with os.fdopen(fd, 'wb') as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        if info is not None:
            os.chown(temporary, info.st_uid, info.st_gid)
            shutil.copystat(path, temporary)
            for name in os.listxattr(path):
                os.setxattr(temporary, name, os.getxattr(path, name))
            os.utime(temporary, None)
            fd, backup = tempfile.mkstemp(prefix=path.name + '.pi-control-backup-', dir=path.parent)
            with os.fdopen(fd, 'wb') as stream:
                stream.write(raw)
                stream.flush()
                os.fsync(stream.fileno())
            current, current_info = upload_state(path)
            if (current is None or digest(current) != revision
                    or current_info.st_ino != info.st_ino
                    or current_info.st_mtime_ns != info.st_mtime_ns):
                raise ValueError('File vừa thay đổi trên Pi; chưa ghi đè. Hãy tải lại.')
            os.replace(temporary, path)
            temporary = None
        else:
            # Atomic create-if-absent: never replace a concurrently created file.
            os.link(temporary, path)
        return {'path': str(path), 'bytes': len(content), 'revision': digest(content),
                'backup': backup, 'message': 'Đã ghi đè file' if info is not None else 'Đã tạo file mới'}
    finally:
        if temporary:
            os.unlink(temporary)


def operate(data):
    value = data.get('path', '')
    if not isinstance(value, str) or not value or len(value) > 4096 or '\0' in value:
        raise ValueError('Đường dẫn không hợp lệ')
    path = Path(value).expanduser()
    if not path.is_absolute():
        raise ValueError('Nhập đường dẫn tuyệt đối hoặc ~/')
    action = data.get('action')
    if action in {'upload_check', 'upload'}:
        return upload(data, path)
    path = path.resolve(strict=True)
    if action == 'list':
        entries = []
        with os.scandir(path) as iterator:
            for entry in iterator:
                if len(entries) >= 1000:
                    raise ValueError('Thư mục có hơn 1000 mục; nhập đường dẫn thư mục con hoặc file')
                try:
                    info = entry.stat(follow_symlinks=False)
                    kind = 'link' if entry.is_symlink() else 'directory' if stat.S_ISDIR(info.st_mode) else 'file' if stat.S_ISREG(info.st_mode) else 'special'
                    entries.append({'name': entry.name, 'path': str(path / entry.name), 'kind': kind, 'bytes': info.st_size})
                except OSError:
                    entries.append({'name': entry.name, 'path': str(path / entry.name), 'kind': 'unavailable'})
        return {'path': str(path), 'parent': str(path.parent), 'entries': sorted(entries, key=lambda e: (e['kind'] != 'directory', e['name'].lower()))}
    raw, info = read_regular(path)
    if action == 'read':
        return {'path': str(path), 'content': raw.decode('utf-8'), 'revision': digest(raw),
                'mode': oct(stat.S_IMODE(info.st_mode)), 'uid': info.st_uid, 'gid': info.st_gid, 'bytes': len(raw)}
    if action != 'write':
        raise ValueError('Thao tác file không hợp lệ')
    content = data.get('content')
    if not isinstance(content, str):
        raise ValueError('Nội dung phải là văn bản UTF-8')
    updated = content.encode('utf-8')
    if len(updated) > LIMIT or '\0' in content:
        raise ValueError('Chỉ lưu văn bản UTF-8 tối đa 512 KiB')
    if data.get('revision') != digest(raw):
        raise ValueError('File đã thay đổi trên Pi. Sao chép phần đang sửa rồi mở lại file trước khi lưu.')
    if info.st_nlink != 1:
        raise ValueError('File có hard link; dùng công cụ chuyên dụng để giữ liên kết')
    if updated == raw:
        return {'path': str(path), 'revision': digest(raw), 'message': 'Nội dung không thay đổi', 'backup': None}
    temporary = None
    backup = None
    try:
        fd, temporary = tempfile.mkstemp(prefix='.pi-control-edit-', dir=path.parent)
        with os.fdopen(fd, 'wb') as stream:
            stream.write(updated)
            stream.flush()
            os.fsync(stream.fileno())
        # Preserve owner/mode and extended attributes (including ACLs).
        os.chown(temporary, info.st_uid, info.st_gid)
        shutil.copystat(path, temporary)
        for name in os.listxattr(path):
            os.setxattr(temporary, name, os.getxattr(path, name))
        os.utime(temporary, None)
        fd, backup = tempfile.mkstemp(prefix=path.name + '.pi-control-backup-', dir=path.parent)
        with os.fdopen(fd, 'wb') as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        # Backup remains private (0600), even if original file is public.
        current, current_info = read_regular(path)
        if (digest(current) != digest(raw) or current_info.st_ino != info.st_ino
                or current_info.st_mtime_ns != info.st_mtime_ns):
            raise ValueError('File vừa thay đổi trên Pi; chưa ghi đè. Mở lại để đối chiếu.')
        os.replace(temporary, path)
        temporary = None
        return {'path': str(path), 'revision': digest(updated), 'backup': backup, 'message': 'Đã lưu file'}
    finally:
        if temporary:
            os.unlink(temporary)


if __name__ == '__main__':
    try:
        print(json.dumps(operate(json.load(sys.stdin)), ensure_ascii=False))
    except Exception as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False))
