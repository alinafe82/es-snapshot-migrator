# Architecture

## Problem

Elasticsearch migrations are operationally risky when the plan is implicit. Teams need to know
which indices are moving, why they were selected, and what evidence supports the migration
before any restore job runs.

## Intended User

The intended user is a platform engineer preparing an Elasticsearch or OpenSearch snapshot
migration plan.

## Components

- `Index`: metadata used for planning.
- `Plan`: reviewable migration manifest with selected and excluded indices.
- `select_indices`: filtering logic.
- CLI: local demonstration of manifest generation.

## Data Flow

A list of indices enters the planner. The planner filters by size and age, then produces a
snapshot manifest containing the selected indices, excluded indices with reasons, repository,
and snapshot name.

## Design Choices

I kept execution out of scope because restore jobs need cluster-specific safety checks,
capacity planning, and rollback decisions. The planning logic is still useful because it is
deterministic and can be reviewed in a pull request or change ticket.

The current filters are intentionally simple. They demonstrate the shape of the planner without
pretending to cover every migration risk.

## What Is Not Built

This repo does not connect to Elasticsearch, create snapshots, restore indices, or change
cluster settings.

## Extension Points

- Add an Elasticsearch client adapter for `_cat/indices`, snapshot repositories, and ILM state.
- Include compatibility checks for target cluster version and repository access.
- Write manifests to disk so failed migrations can resume from an approved plan.

## Operational Considerations

A production tool should validate target capacity, shard counts, index templates, aliases,
security roles, and rollback behavior before execution.

## Testing Strategy

Tests cover filtering and manifest construction. The next useful layer would use recorded API
fixtures or a disposable container to test a real metadata adapter.
