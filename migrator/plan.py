from .models import Index, Plan


def select_indices(
    indices: list[Index],
    max_size_gb: float = 500.0,
    max_age_days: int = 365,
) -> list[Index]:
    return [i for i in indices if i.size_gb <= max_size_gb and i.created_days_ago <= max_age_days]


def build_plan(repo: str, indices: list[Index], snapshot: str) -> Plan:
    chosen = select_indices(indices)
    return Plan(repository=repo, indices=chosen, snapshot_name=snapshot)
