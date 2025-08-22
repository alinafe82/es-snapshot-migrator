# es-snapshot-migrator
> Plan and simulate Elasticsearch snapshot/restore migrations between clusters

Features:
- Repository compatibility checks (simulated)
- Index selection with size/cutoff filters
- Dry-run planning + manifest generation
- Resume-safe steps with idempotent markers

This mirrors real-world ES/Kibana migrations while remaining safe to run locally.
