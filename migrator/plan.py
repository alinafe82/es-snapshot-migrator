from .models import Index, Plan


def select_indices(
    indices: list[Index],
    max_size_gb: float = 500.0,
    max_age_days: int = 365,
) -> list[Index]:
    if max_size_gb < 0:
        raise ValueError("max_size_gb must be non-negative")
    if max_age_days < 0:
        raise ValueError("max_age_days must be non-negative")

    return [i for i in indices if i.size_gb <= max_size_gb and i.created_days_ago <= max_age_days]


def build_plan(
    repo: str,
    indices: list[Index],
    snapshot: str,
    max_size_gb: float = 500.0,
    max_age_days: int = 365,
) -> Plan:
    chosen = select_indices(indices, max_size_gb=max_size_gb, max_age_days=max_age_days)
    return Plan(repository=repo, indices=chosen, snapshot_name=snapshot)
