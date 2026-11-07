import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from mentor_lab.schemas import format_failure_rate  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
format_failure_rate(1000)