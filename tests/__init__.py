import sys
from pathlib import Path

# Ensure the src/ directory is on the path for tests
SRC_PATH = Path(__file__).resolve().parents[1] / "src"
if SRC_PATH.exists() and str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

# Import src so that it registers the 'mod' alias
import src  # noqa: E402
