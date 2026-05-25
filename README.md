# es-snapshot-migrator
Plan Elasticsearch snapshot migration manifests.

This repo models the planning step of an Elasticsearch migration. It filters candidate
indices, builds a snapshot manifest, and prints a reviewable plan without connecting to a real
cluster.

The project is intentionally small. It focuses on the part that is easiest to test and safest
to show publicly: deciding what should move before any restore job is executed.

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

## Architecture Overview

- `migrator.models` defines index and plan data contracts.
- `migrator.plan` selects indices and builds the manifest.
- `migrator.cli` provides a local demo entry point.

See [docs/architecture.md](docs/architecture.md) for design details.

## Limitations

- Elasticsearch APIs are simulated.
- Restore execution is intentionally out of scope.
- The current filters only consider size and age.

## Future Improvements

- Add a real Elasticsearch client adapter.
- Include shard count, ILM state, and repository compatibility checks.
- Persist plan manifests for approval and resumption.

## Interview Notes

See [docs/interview-notes.md](docs/interview-notes.md).
