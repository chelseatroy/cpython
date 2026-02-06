import sys
from pathlib import Path

# Add the scripts directory to sys.path so we can import the modules under test.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
