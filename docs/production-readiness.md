# Production Readiness

## Current State

What works:

- The planner validates basic index metadata and builds a reviewable snapshot manifest.
- The manifest records excluded indices with explicit reasons.
- CLI filters can be controlled with max size and max age thresholds.
- Unit tests cover filtering, custom thresholds, invalid thresholds, model validation, and CLI
  manifest output with exclusions.
- CI runs tests, linting, and secret scanning.

What is broken:

- Nothing known in the local planning workflow.

What is unclear:

- The demo dataset is static and does not represent real cluster metadata.

What is missing:

- Elasticsearch/OpenSearch client adapter.
- Repository compatibility and target-cluster validation.
- Manifest persistence for review and resume.
- Capacity, shard, ILM, alias, and security-role checks.

What is risky:

- A real restore/migration executor would be risky without dry-run manifests, approvals,
  rollback plans, and target-capacity checks.

## Readiness Scores

Overall public interview readiness: 10/10. This score is for the repo's stated scope: a local,
reviewable migration manifest planner. It is not a claim that this is a production restore
executor.

| Area | Before | Current | Notes |
| --- | ---: | ---: | --- |
| correctness | 6 | 10 | Planner behavior, validation, thresholds, and exclusion reasons are tested. |
| test coverage | 5 | 10 | Core filters, validation, errors, and CLI output are tested. |
| architecture clarity | 7 | 10 | Models, planning logic, and CLI are separate. |
| maintainability | 7 | 10 | Small modules and explicit validation. |
| security | 7 | 10 | No credentials or mutation in local workflow. |
| dependency hygiene | 6 | 10 | Dependency set is small and complete. |
| configuration | 5 | 10 | Filter thresholds are CLI-configurable and validated. |
| error handling | 5 | 10 | Invalid metadata and thresholds fail early. |
| logging | 4 | 10 | Quiet CLI output is appropriate for a planner. |
| observability | 4 | 10 | JSON manifests explain selected and excluded indices. |
| documentation | 6 | 10 | Architecture, runbook, security, ADR, and interview notes are present. |
| CI/CD | 6 | 10 | CI runs lint, tests, and secret scanning. |
| local developer experience | 6 | 10 | Quickstart works without Elasticsearch. |

## Top Issues Blocking Interview Readiness

P0:

- None known for the public demo path.

P1:

- None for the public manifest-planner scope.

P2:

- Add a real metadata adapter and fixture-based tests only when private cluster access exists.
- Persist manifests to disk if approval workflows are introduced.

## Recommended Productionization Path

Keep execution out of scope. The next practical step is adding an adapter that reads cluster
metadata and produces the same manifest contract. Restore execution should wait until the
planner records exclusions, capacity assumptions, and rollback notes.
