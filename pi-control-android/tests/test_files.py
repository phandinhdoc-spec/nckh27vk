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


if __name__ == '__main__':
    unittest.main()
