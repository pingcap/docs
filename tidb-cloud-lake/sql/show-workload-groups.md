---
title: SHOW WORKLOAD GROUPS
summary: 返回所有现有 workload group 及其配额的列表。
---

# SHOW WORKLOAD GROUPS

返回所有现有 workload group 及其配额的列表。

## 语法 {#syntax}

```sql
SHOW WORKLOAD GROUPS
```

## 示例 {#examples}

```sql
SHOW WORKLOAD GROUPS

┌────────────────────────────────────────────────────────────────────────────────────────────┐
│  name  │ cpu_quota │ memory_quota │ query_timeout │ max_concurrency │ query_queued_timeout │
│ String │   String  │    String    │     String    │      String     │        String        │
├────────┼───────────┼──────────────┼───────────────┼─────────────────┼──────────────────────┤
│ test   │ 30%       │              │ 15s           │                 │                      │
└────────────────────────────────────────────────────────────────────────────────────────────┘
```