import contextlib
import io
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from ai_teacher.main import main


class TestMain(unittest.TestCase):
    def test_main_outputs_greeting(self) -> None:
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            main()
        self.assertIn("Hello from ai-teacher.", buffer.getvalue())


if __name__ == "__main__":
    unittest.main()
