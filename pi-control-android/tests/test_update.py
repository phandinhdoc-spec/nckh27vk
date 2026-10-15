import hashlib
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('updater', Path(__file__).resolve().parents[1] / 'update-pi-telemetry.py')
updater = importlib.util.module_from_spec(spec)
spec.loader.exec_module(updater)


class UpdateTests(unittest.TestCase):
    def test_known_version_backup_and_unknown_version_refusal(self):
        old, new = b'x = 1\n', b'x = 2\n'
        manifest = {name: {'before': updater.checksum(old), 'after': updater.checksum(new)} for name in updater.MANIFEST}
        with tempfile.TemporaryDirectory() as directory, patch.object(updater, 'MANIFEST', manifest), patch.object(updater.urllib.request, 'urlopen', side_effect=lambda *a, **kw: io.BytesIO(new)) as fetch:
            root = Path(directory)
            for name in manifest:
                (root / name).write_bytes(old)
            updater.update(root)
            backup = next(root.glob('.pi-control-backup-*'))
            for name in manifest:
                self.assertEqual((root / name).read_bytes(), new)
                self.assertEqual((backup / name).read_bytes(), old)
            (root / 'app.py').write_text('custom code')
            fetch.reset_mock()
            with self.assertRaisesRegex(ValueError, 'khác bản'):
                updater.update(root)
            fetch.assert_not_called()
            self.assertEqual((root / 'app.py').read_text(), 'custom code')
