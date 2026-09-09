from pathlib import Path

import duckdb

from src.pipeline import OUTPUT, SOURCE, build_golden


def test_uploaded_extract_builds_dashboard_contract():
    assert SOURCE.exists()
    output = build_golden()
    assert output == OUTPUT
    connection = duckdb.connect(str(output), read_only=True)
    try:
        summary = connection.execute("SELECT * FROM mart_kpi_summary").df().iloc[0]
        assert summary["data_asof_date"].strftime("%Y-%m-%d") == "2026-08-08"
        assert connection.execute("SELECT count(*) FROM mart_monthly_trend").fetchone()[0] == 8
        assert connection.execute("SELECT count(*) FROM mart_metric_truth").fetchone()[0] == 9
        assert connection.execute("SELECT count(*) FROM mart_investment WHERE is_recommended").fetchone()[0] == 1
    finally:
        connection.close()
