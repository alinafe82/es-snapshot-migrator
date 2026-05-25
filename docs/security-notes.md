# Security Notes

## Threat Assumptions

- The local workflow uses static demo metadata and does not connect to Elasticsearch.
- Any future cluster credentials must come from the environment or a secret manager, not the
  repository.
- The tool is intended to plan migrations, not execute them.

## What It Protects Against

- Invalid basic index metadata through Pydantic validation.
- Accidental mutation by not implementing snapshot creation or restore execution.
- Unsafe filter settings by rejecting negative thresholds.
- Secret commits through CI secret scanning and local pre-commit guidance.

## What It Does Not Protect Against

- Leaked Elasticsearch credentials in a future adapter.
- Incorrect capacity planning or restore compatibility.
- Snapshot repository misconfiguration.
- Sensitive index names or customer data being copied into public examples.

## Safe Local Usage

```bash
uv run python -m migrator.cli --repo cold-repo --snapshot logs-2026-01
```

Use synthetic index names in examples and tests. Do not commit private cluster endpoints,
credentials, customer names, or production index names.

## Known Limitations

The repo produces a manifest only. A production migration tool would need least-privilege
credentials, dry-run output, approval gates, rollback steps, and target-cluster checks.
