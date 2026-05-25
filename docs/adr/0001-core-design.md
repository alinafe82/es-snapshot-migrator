# ADR 0001: Plan Snapshot Migrations Before Execution

## Context

Elasticsearch migrations fail when teams start with execution instead of a reviewed plan. The
public repo should show deterministic manifest generation without requiring a private cluster.

## Decision

Implement the project as a local manifest planner with validated models, explicit filters, and
CLI output.

## Alternatives Considered

- Build a real snapshot/restore executor.
- Add a full Elasticsearch client immediately.
- Keep the repo as documentation only.

## Why This Design Was Selected

I chose this design because the plan is the safest public part of the workflow. It is
deterministic, testable, and easy to discuss without exposing private infrastructure.

## Tradeoffs

The tradeoff is that the repo does not prove cluster compatibility or restore safety. Those
checks belong in the next adapter layer.

## Consequences

- The demo works without credentials.
- Tests can exercise planning rules directly.
- Execution remains intentionally out of scope.

## What Would Change At Larger Scale

At larger scale, I would add a metadata adapter, per-index exclusion reasons, manifest
persistence, repository compatibility checks, target-capacity validation, and rollback
documentation before allowing any restore command.
