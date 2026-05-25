import pytest
from click.testing import CliRunner
from pydantic import ValidationError

from migrator.cli import main
from migrator.models import Index
from migrator.plan import build_plan, exclusion_reasons, select_indices


def test_select_indices_filters():
    data = [
        Index(name="a", size_gb=100, created_days_ago=10),
        Index(name="b", size_gb=700, created_days_ago=10),
        Index(name="c", size_gb=100, created_days_ago=800),
    ]
    chosen = select_indices(data, max_size_gb=500, max_age_days=365)
    assert [x.name for x in chosen] == ["a"]


def test_build_plan_keeps_manifest_fields():
    data = [
        Index(name="logs-2026.01.01", size_gb=10, created_days_ago=2),
    ]

    plan = build_plan("repo-a", data, "snap-001")

    assert plan.repository == "repo-a"
    assert plan.snapshot_name == "snap-001"
    assert [index.name for index in plan.indices] == ["logs-2026.01.01"]
    assert plan.excluded_indices == []


def test_build_plan_uses_custom_filter_thresholds():
    data = [
        Index(name="small-new", size_gb=100, created_days_ago=10),
        Index(name="medium-new", size_gb=300, created_days_ago=10),
    ]

    plan = build_plan("repo-a", data, "snap-001", max_size_gb=150, max_age_days=30)

    assert [index.name for index in plan.indices] == ["small-new"]
    assert [entry.index.name for entry in plan.excluded_indices] == ["medium-new"]
    assert "size_gb 300.0 exceeds max_size_gb 150" in plan.excluded_indices[0].reasons


def test_select_indices_rejects_negative_thresholds():
    with pytest.raises(ValueError, match="max_size_gb"):
        select_indices([], max_size_gb=-1)

    with pytest.raises(ValueError, match="max_age_days"):
        select_indices([], max_age_days=-1)


def test_index_validation_rejects_invalid_metadata():
    with pytest.raises(ValidationError):
        Index(name="", size_gb=-1, created_days_ago=-1)


def test_exclusion_reasons_explains_all_failed_filters():
    index = Index(name="old-large", size_gb=600, created_days_ago=500)

    reasons = exclusion_reasons(index, max_size_gb=500, max_age_days=365)

    assert reasons == [
        "size_gb 600.0 exceeds max_size_gb 500",
        "created_days_ago 500 exceeds max_age_days 365",
    ]


def test_cli_emits_manifest_json():
    runner = CliRunner()

    result = runner.invoke(main, ["--repo", "cold-repo", "--snapshot", "snap-001"])

    assert result.exit_code == 0
    assert '"repository": "cold-repo"' in result.output
    assert '"snapshot_name": "snap-001"' in result.output
    assert '"excluded_indices"' in result.output
