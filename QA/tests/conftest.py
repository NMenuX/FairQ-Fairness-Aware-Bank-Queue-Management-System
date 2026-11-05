from pathlib import Path
import sys

# Add the backend directory so QA tests can import the application package
# regardless of whether pytest is launched from the repository root or QA/.
REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
BACKEND_DIRECTORY = REPOSITORY_ROOT / "backend"
if str(BACKEND_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIRECTORY))
