---
title: Materialized Views
summary: Learn what materialized views are in TiDB, when to use them, and where the creation, refresh, limitation, and compatibility details belong.
---

# Materialized Views

TiDB materialized views store the result of a query in a reusable object so you can avoid recomputing the same result repeatedly. This page collects the core concept, usage flow, and limitations for the feature.

## Usage scenarios

Materialized views are intended for workloads that repeatedly read the same query result.

- Reuse expensive analytical query results.
- Reduce repeated computation for read-heavy workloads.
- Provide a stable result set for downstream consumers that do not need to rerun the base query each time.

## Prerequisites

- <!-- TODO: confirm the minimum TiDB version and any feature gates. -->
- <!-- TODO: confirm whether the feature depends on specific storage engines or cluster settings. -->

## How it works

TiDB materialized views are backed by stored data derived from a query. The final design will define how TiDB creates, refreshes, and invalidates that data.

## Create and manage materialized views

### Create a materialized view

This section will describe the supported creation flow, required clauses, and examples. <!-- TODO: fill in from the spec. -->

### Refresh a materialized view

This section will describe refresh behavior, supported refresh modes, and operational guidance. <!-- TODO: fill in from the spec. -->

### Query a materialized view

This section will describe how queries resolve to the stored result and any optimizer behavior. <!-- TODO: fill in from the spec. -->

### Drop a materialized view

This section will describe cleanup behavior and any related objects. <!-- TODO: fill in from the spec. -->

## Limitations

- <!-- TODO: list unsupported DDL, DML, replication, or optimizer cases from the spec. -->
- <!-- TODO: add size, freshness, or compatibility limits if they exist. -->

## Compatibility

- <!-- TODO: describe MySQL compatibility gaps or version-specific behavior. -->
- <!-- TODO: describe behavior differences across TiDB versions or storage layouts. -->

## See also

- [Views](/views.md)
