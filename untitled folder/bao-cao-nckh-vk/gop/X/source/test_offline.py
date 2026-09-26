import tempfile, unittest
from pathlib import Path
from messages import *
from camera import delete_file_if_exists
from gemini_client import build_payload, build_prompt
from config import AppConfig

class CatalogTests(unittest.TestCase):
 def test_catalog(self):
  self.assertEqual(len(VALID_MESSAGES), 36); self.assertEqual(len(set(MESSAGE_TO_MP3.values())), 36)
  self.assertEqual(normalize_and_validate(" không hợp lệ "), FALLBACK_MESSAGE)
  self.assertEqual(mp3_filename_for(VALID_MESSAGES[0]), "01-ay-la-to-nam-tram-ong.mp3")
 def test_payload_and_prompt(self):
  c=AppConfig("x", Path("/tmp")); p=build_payload(build_prompt(), "abc", c)
  self.assertEqual(p["generationConfig"]["temperature"], 0); self.assertIn(FALLBACK_MESSAGE, build_prompt())
 def test_cleanup(self):
  with tempfile.TemporaryDirectory() as d:
   f=Path(d)/"x.jpg"; f.write_bytes(b"x"); delete_file_if_exists(f); self.assertFalse(f.exists())
if __name__ == "__main__": unittest.main()
