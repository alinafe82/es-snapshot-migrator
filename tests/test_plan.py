from migrator.models import Index
from migrator.plan import select_indices

def test_select_indices_filters():
    data = [
        Index(name="a", size_gb=100, created_days_ago=10),
        Index(name="b", size_gb=700, created_days_ago=10),
        Index(name="c", size_gb=100, created_days_ago=800),
    ]
    chosen = select_indices(data, max_size_gb=500, max_age_days=365)
    assert [x.name for x in chosen] == ["a"]
