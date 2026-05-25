from migrator.models import Index
from migrator.plan import build_plan, select_indices


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
