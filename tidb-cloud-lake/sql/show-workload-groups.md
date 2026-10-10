---
title: SHOW WORKLOAD GROUPS
summary: 既存のすべての workload group とその quota の一覧を返します。
---

# SHOW WORKLOAD GROUPS

既存のすべての workload group とその quota の一覧を返します。

## 構文 {#syntax}

```sql
SHOW WORKLOAD GROUPS
```

## 例 {#examples}

```sql
SHOW WORKLOAD GROUPS

┌────────────────────────────────────────────────────────────────────────────────────────────┐
│  name  │ cpu_quota │ memory_quota │ query_timeout │ max_concurrency │ query_queued_timeout │
│ String │   String  │    String    │     String    │      String     │        String        │
├────────┼───────────┼──────────────┼───────────────┼─────────────────┼──────────────────────┤
│ test   │ 30%       │              │ 15s           │                 │                      │
└────────────────────────────────────────────────────────────────────────────────────────────┘
```