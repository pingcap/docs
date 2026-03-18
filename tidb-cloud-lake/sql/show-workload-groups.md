---
title: SHOW WORKLOAD GROUPS
summary: Returns a list of all existing workload groups along with their quotas.
---

> **Note:**
>
> Introduced or updated in v1.2.743.

Returns a list of all existing workload groups along with their quotas.

## Syntax

```sql
SHOW WORKLOAD GROUPS
```

## Examples

```sql
SHOW WORKLOAD GROUPS

┌────────────────────────────────────────────────────────────────────────────────────────────┐
│  name  │ cpu_quota │ memory_quota │ query_timeout │ max_concurrency │ query_queued_timeout │
│ String │   String  │    String    │     String    │      String     │        String        │
├────────┼───────────┼──────────────┼───────────────┼─────────────────┼──────────────────────┤
│ test   │ 30%       │              │ 15s           │                 │                      │
└────────────────────────────────────────────────────────────────────────────────────────────┘
```