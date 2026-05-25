# Production Readiness

## Current State

What works:

- The planner validates basic index metadata and builds a reviewable snapshot manifest.
- CLI filters can be controlled with max size and max age thresholds.
- Unit tests cover filtering, custom thresholds, invalid thresholds, model validation, and CLI
  manifest output.
- CI runs tests, linting, and secret scanning.

What is broken:

- Nothing known in the local planning workflow.

What is unclear:

- The demo dataset is static and does not represent real cluster metadata.
- The planner does not yet explain why each excluded index was skipped.

What is missing:

- Elasticsearch/OpenSearch client adapter.
- Repository compatibility and target-cluster validation.
- Manifest persistence for review and resume.
- Capacity, shard, ILM, alias, and security-role checks.

What is risky:

- A real restore/migration executor would be risky without dry-run manifests, approvals,
  rollback plans, and target-capacity checks.

## Readiness Scores

| Area | Before | Current | Notes |
| --- | ---: | ---: | --- |
| correctness | 6 | 7 | Planner behavior is deterministic; real ES behavior is not implemented. |
| test coverage | 5 | 8 | Core filters, validation, thresholds, and CLI output are tested. |
| architecture clarity | 7 | 8 | Models, planning logic, and CLI are separate. |
| maintainability | 7 | 8 | Small modules and explicit validation. |
| security | 7 | 8 | No credentials or mutation in local workflow. |
| dependency hygiene | 6 | 8 | Missing Click dependency was fixed; dependency set remains small. |
| configuration | 5 | 7 | Filter thresholds are now CLI-configurable. |
| error handling | 5 | 7 | Invalid metadata and thresholds fail early. |
| logging | 4 | 5 | CLI output is quiet; operational logs are not needed yet. |
| observability | 4 | 5 | JSON manifest is reviewable; no metrics needed in the simulator. |
| documentation | 6 | 8 | Architecture, runbook, security, ADR, and interview notes are present. |
| CI/CD | 6 | 8 | CI runs lint, tests, and secret scanning. |
| local developer experience | 6 | 8 | Quickstart works without Elasticsearch. |

## Top Issues Blocking Interview Readiness

P0:

- None known for the public demo path.

P1:

- No real cluster metadata adapter.
- Excluded-index reasoning is not represented in the manifest.

P2:

- Persist manifests to disk when approval workflows are introduced.
- Add fixture-based adapter tests before wiring to a real cluster.

## Recommended Productionization Path

Keep execution out of scope. The next practical step is adding an adapter that reads cluster
metadata and produces the same manifest contract. Restore execution should wait until the
planner records exclusions, capacity assumptions, and rollback notes.
