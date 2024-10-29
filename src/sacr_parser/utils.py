import inspect
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SRC_DIR = BASE_DIR / "src"


def relative_path(path):
    """Return an absolute path relative to the current file."""
    # use inspect.stack()[1] to get the caller's filename
    module_path = inspect.stack()[1].filename
    return Path(module_path).resolve().parent / path

