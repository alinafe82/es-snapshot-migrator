# es-snapshot-migrator

A migration-plan builder for Elasticsearch (or OpenSearch) snapshots. Given a list of indices and a target snapshot repository, it produces a JSON manifest that names every index going into the snapshot and every index being left out, with the reason for each exclusion.

The repo does the planning step on purpose. Restore execution stays out of scope; the part that benefits from being reviewable in a PR is the index selection, not the restore.

## Why planning is the safe public part

A migration plan is cheap to be wrong about and expensive to skip reviewing. The actual `restore` call is short, but it depends on a lot of preconditions: target version compatibility, ILM policy alignment, repository registration, shard count assumptions, and the index list itself. The selection step is where most mistakes happen ("we forgot to exclude the system indices", "we included a closed index", "we exceeded our target size budget"). That is the part the repo turns into a JSON artefact that a reviewer can look at and either approve or reject.

The restore itself is left for the operator's own runbook. The plan in this repo is the input to that runbook.

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -q
python -m migrator.cli --repo cold-repo --snapshot logs-2026-01
```

With `uv`:

```bash
uv run --extra dev pytest
uv run --extra dev ruff check .
```

## How the manifest is built

- `migrator.models.Index` carries the per-index metadata that goes into the filter: name, size in GB, created-days-ago. The model rejects empty names and negative numbers, so a bad input fails before the planner sees it.
- `migrator.plan.exclusion_reasons` is the only place that knows what makes an index ineligible. Today that is size (`max_size_gb`) and age (`max_age_days`). Each exclusion carries every reason it failed, not just the first one.
- `migrator.plan.build_plan` walks the indices once, splits them into chosen and excluded, and returns a `Plan`. The manifest is deterministic for a given input.
- `migrator.cli` emits the manifest as JSON. Nothing else.

Design notes: [docs/architecture.md](docs/architecture.md).

## What the tests prove

- size filter excludes indices above `max_size_gb`.
- age filter excludes indices above `max_age_days`.
- custom thresholds override defaults.
- negative thresholds are rejected.
- empty names and negative metadata fail at model construction.
- multi-failure indices list every reason, not just the first.
- the CLI JSON manifest includes `repository`, `snapshot_name`, and `excluded_indices`.

## Adapter checks I would add before a real cluster

Today the filter is two-dimensional (size, age). Before pointing this at a real `_snapshot/...` repository I would add:

- shard count per index; large shard counts inflate snapshot duration and restore cost.
- ILM phase; an index in `delete` phase should not be migrated forward.
- index pattern matching against the target cluster's mappings, so a mapping conflict is caught at plan time.
- repository compatibility: confirm the target repo type (S3, GCS, FS) is registered on the destination cluster.

Those are listed as adapter responsibilities, not core planner logic, so the planner stays simple.

## Operational notes

- [docs/runbook.md](docs/runbook.md)
- [docs/security-notes.md](docs/security-notes.md)
- [docs/production-readiness.md](docs/production-readiness.md)
- [docs/interview-notes.md](docs/interview-notes.md)
