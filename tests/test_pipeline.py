from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).parents[1]


def test_demo_pipeline_outputs_golden_metrics():
    subprocess.run([sys.executable, "scripts/generate_demo_data.py"], cwd=ROOT, check=True, capture_output=True, text=True)
    subprocess.run([sys.executable, "-m", "src.pipeline"], cwd=ROOT, check=True, capture_output=True, text=True)
    quality = json.loads((ROOT / "data/golden/quality_report.json").read_text(encoding="utf-8"))
    assert quality["targeting_raw_rows"] == 3000
    assert quality["duplicate_payment_rows_removed"] == 6
    assert (ROOT / "data/golden/monthly_metrics.csv").exists()
