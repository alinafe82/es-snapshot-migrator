from .models import Index, IndexExclusion, Plan


def validate_thresholds(max_size_gb: float, max_age_days: int) -> None:
    if max_size_gb < 0:
        raise ValueError("max_size_gb must be non-negative")
    if max_age_days < 0:
        raise ValueError("max_age_days must be non-negative")


def exclusion_reasons(
    index: Index,
    max_size_gb: float = 500.0,
    max_age_days: int = 365,
) -> list[str]:
    reasons = []
    if index.size_gb > max_size_gb:
        reasons.append(f"size_gb {index.size_gb} exceeds max_size_gb {max_size_gb}")
    if index.created_days_ago > max_age_days:
        reasons.append(
            f"created_days_ago {index.created_days_ago} exceeds max_age_days {max_age_days}"
        )
    return reasons


def select_indices(
    indices: list[Index],
    max_size_gb: float = 500.0,
    max_age_days: int = 365,
) -> list[Index]:
    validate_thresholds(max_size_gb, max_age_days)

    return [i for i in indices if not exclusion_reasons(i, max_size_gb, max_age_days)]


def build_plan(
    repo: str,
    indices: list[Index],
    snapshot: str,
    max_size_gb: float = 500.0,
    max_age_days: int = 365,
) -> Plan:
    validate_thresholds(max_size_gb, max_age_days)

    seen_names: set[str] = set()
    duplicate_names: set[str] = set()
    for index in indices:
        if index.name in seen_names:
            duplicate_names.add(index.name)
        seen_names.add(index.name)
    if duplicate_names:
        names = ", ".join(sorted(duplicate_names))
        raise ValueError(f"duplicate index names: {names}")

    chosen = []
    excluded = []
    for index in indices:
        reasons = exclusion_reasons(index, max_size_gb=max_size_gb, max_age_days=max_age_days)
        if reasons:
            excluded.append(IndexExclusion(index=index, reasons=reasons))
        else:
            chosen.append(index)

    return Plan(
        repository=repo,
        indices=chosen,
        excluded_indices=excluded,
        snapshot_name=snapshot,
    )
