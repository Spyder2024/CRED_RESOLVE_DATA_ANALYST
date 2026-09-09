from pathlib import Path
import runpy

# Canonical entry point is dashboard/app.py
APP_PATH = Path(__file__).resolve().parent / "dashboard" / "app.py"
runpy.run_path(str(APP_PATH), run_name="__main__")
