"""Launch PyQt GUI smoke-test harness (boundary layer)."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from boundary.gui_smoke import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
