# Runbook

## Run Locally

```bash
uv run python -m migrator.cli --repo cold-repo --snapshot logs-2026-01
uv run python -m migrator.cli --repo cold-repo --snapshot logs-2026-01 --max-size-gb 150 --max-age-days 90
```

## Test

```bash
uv run --extra dev pytest
uv run --extra dev ruff check .
```

## Common Failure Modes

- Negative `--max-size-gb` or `--max-age-days`: use non-negative thresholds.
- Empty repo or snapshot names: provide explicit names.
- Missing `click`: install dependencies from `requirements.txt` or use `uv run --extra dev`.

## Troubleshooting

- Use the JSON manifest output to verify selected indices.
- Lower `--max-size-gb` or `--max-age-days` to test filter behavior.
- Keep real cluster data out of public fixtures.

## Safe Cleanup

The local demo does not create snapshots or files. Remove `.venv`, `.pytest_cache`, or
`__pycache__` if needed.

## Known Limitations

The tool does not connect to Elasticsearch or OpenSearch. It models the planning step only.
