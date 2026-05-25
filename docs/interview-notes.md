# Interview Notes

## 60-Second Explanation

This is a Python CLI that models the planning stage of an Elasticsearch snapshot migration. It
filters indices by size and age, builds a manifest, and prints a plan for review. It does not
touch a real cluster.

## Decisions I Can Defend

- Planning is separated from execution because restore operations are risky and environment
  specific.
- The plan is a typed object so it can later be persisted or passed to another workflow.
- The CLI is thin; filtering logic is tested directly.

## Tradeoffs

The repo is intentionally narrow. It does not prove full migration automation, but it does show
how I isolate deterministic planning from operational execution.

## Fixes Made During Portfolio Hardening

- Added local test and lint tooling.
- Added GitHub Actions CI.
- Added a license, architecture notes, ADR, and interview notes.
- Added a manifest construction test.

## Likely Questions

**Why only size and age filters?**
They are easy to explain and test. In production I would add shard count, ILM state, aliases,
security roles, and target capacity.

**Why not execute the restore?**
Execution needs real cluster context and rollback design. I would keep execution behind an
adapter and require an approved manifest first.

**What does this show for Engineering Productivity?**
It shows how I turn a manual operational checklist into typed, testable planning logic.
