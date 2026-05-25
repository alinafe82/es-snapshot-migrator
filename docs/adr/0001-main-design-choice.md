# ADR 0001: Separate Planning From Migration Execution

## Status

Accepted

## Context

Snapshot migration execution is environment-specific and risky. A public portfolio repo should
not pretend to run production migrations without real cluster context.

## Decision

The repo focuses on manifest planning and leaves snapshot creation and restore execution out of
scope.

## Consequences

The code is safe to run locally and easy to test. The tradeoff is that production use requires
a real adapter, capacity checks, and execution orchestration.
