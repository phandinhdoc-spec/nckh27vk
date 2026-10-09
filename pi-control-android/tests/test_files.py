import importlib.util
import json
import os
from pathlib import Path
import stat
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('remote_files', ROOT / 'remote_files.py')
files = importlib.util.module_from_spec(spec)
spec.loader.exec_module(files)


class FileTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.path = self.root / "file ' $(literal).env"
        self.path.write_bytes('TOKEN=abc\r\nTên=Pi\r\n'.encode())
        self.path.chmod(0o640)

    def tearDown(self):
        self.temp.cleanup()

    def read(self):
        return files.operate({'action': 'read', 'path': str(self.path)})

    def test_save_backup_unicode_newlines_permissions(self):
        before = self.path.read_bytes()
        read = self.read()
        result = files.operate({'action': 'write', 'path': str(self.path), 'revision': read['revision'], 'content': 'Chào Pi\n'})
        self.assertEqual(self.path.read_text(), 'Chào Pi\n')
        self.assertEqual(Path(result['backup']).read_bytes(), before)
        self.assertEqual(stat.S_IMODE(self.path.stat().st_mode), 0o640)
        self.assertEqual(stat.S_IMODE(Path(result['backup']).stat().st_mode), 0o600)

    def test_conflict_keeps_remote_changes(self):
        read = self.read()
        self.path.write_text('changed by another process')
        with self.assertRaisesRegex(ValueError, 'thay đổi'):
            files.operate({'action': 'write', 'path': str(self.path), 'revision': read['revision'], 'content': 'overwrite'})
        self.assertEqual(self.path.read_text(), 'changed by another process')

    def test_binary_large_fifo_rejected(self):
        for raw in (b'\0binary', b'x'*(files.LIMIT+1)):
            self.path.write_bytes(raw)
            with self.assertRaises(ValueError):
                self.read()
        fifo = self.root / 'fifo'
        os.mkfifo(fifo)
        with self.assertRaises(ValueError):
            files.operate({'action': 'read', 'path': str(fifo)})

    def test_symlink_resolves_without_replacing_link(self):
        link = self.root / 'alias'
        link.symlink_to(self.path)
        read = files.operate({'action': 'read', 'path': str(link)})
        self.assertEqual(read['path'], str(self.path))
        files.operate({'action': 'write', 'path': read['path'], 'revision': read['revision'], 'content': 'updated'})
        self.assertTrue(link.is_symlink())
        self.assertEqual(link.read_text(), 'updated')

    def test_list_hidden_and_json_stdin_protocol(self):
        (self.root / '.env').write_text('')
        request = {'action': 'list', 'path': str(self.root)}
        result = subprocess.run(['python3', str(ROOT / 'remote_files.py')], input=json.dumps(request), text=True, capture_output=True, check=True)
        names = [e['name'] for e in json.loads(result.stdout)['entries']
        ]
        self.assertIn('.env', names)
        self.assertIn(self.path.name, names)



class UploadTests(unittest.TestCase):
    def setUp(self):
        import base64
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.path = self.root / "new ' $(literal).bin"
        self.raw = bytes(range(256)) * 3000
        self.encoded = base64.b64encode(self.raw).decode()

    def tearDown(self):
        self.temp.cleanup()

    def check(self):
        return files.operate({'action': 'upload_check', 'path': str(self.path)})

    def upload(self, revision=None, **overrides):
        return files.operate({'action': 'upload', 'path': str(self.path),
                              'revision': revision, 'base64': self.encoded, **overrides})

    def test_new_binary_file_preserved_byte_for_byte(self):
        self.assertFalse(self.check()['exists'])
        result = self.upload()
        self.assertEqual(self.path.read_bytes(), self.raw)
        self.assertEqual(result['revision'], files.digest(self.raw))
        self.assertIsNone(result['backup'])
        self.assertEqual(stat.S_IMODE(self.path.stat().st_mode), 0o600)

    def test_overwrite_binary_backup_and_executable_mode(self):
        self.path.write_bytes(b'old\0data')
        self.path.chmod(0o750)
        checked = self.check()
        result = self.upload(checked['revision'])
        self.assertEqual(Path(result['backup']).read_bytes(), b'old\0data')
        self.assertEqual(self.path.read_bytes(), self.raw)
        self.assertEqual(stat.S_IMODE(self.path.stat().st_mode), 0o750)

    def test_existing_requires_matching_revision(self):
        self.path.write_bytes(b'original')
        checked = self.check()
        self.path.write_bytes(b'changed')
        for revision in (None, checked['revision']):
            with self.assertRaisesRegex(ValueError, 'thay đổi'):
                self.upload(revision)
        self.assertEqual(self.path.read_bytes(), b'changed')

    def test_create_race_does_not_overwrite(self):
        from unittest.mock import patch
        link = os.link
        def racing_link(src, dst):
            self.path.write_bytes(b'created elsewhere')
            return link(src, dst)
        with patch.object(files.os, 'link', side_effect=racing_link):
            with self.assertRaises(FileExistsError):
                self.upload()
        self.assertEqual(self.path.read_bytes(), b'created elsewhere')
        self.assertFalse(list(self.root.glob('.pi-control-upload-*')))

    def test_empty_file_invalid_base64_size_and_symlink(self):
        from unittest.mock import patch
        self.upload(base64='')
        self.assertEqual(self.path.read_bytes(), b'')
        revision = self.check()['revision']
        with self.assertRaises(ValueError):
            self.upload(revision, base64='bad!')
        with patch.object(files, 'UPLOAD_LIMIT', 10):
            with self.assertRaisesRegex(ValueError, '16 MiB'):
                self.upload(revision)
        link = self.root / 'alias'
        link.symlink_to(self.path)
        with self.assertRaises(OSError):
            self.upload(path=str(link))
        self.assertEqual(self.path.read_bytes(), b'')

    def test_directory_and_missing_parent_rejected(self):
        with self.assertRaises(ValueError):
            self.upload(path=str(self.root))
        with self.assertRaises(FileNotFoundError):
            self.upload(path=str(self.root / 'missing' / 'file'))

if __name__ == '__main__':
    unittest.main()
