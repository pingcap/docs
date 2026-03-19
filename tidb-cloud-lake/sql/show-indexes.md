---
title: SHOW INDEXES
summary: Shows the created indexes. Equivalent to SELECT * FROM system.indexes.
---

# SHOW INDEXES

> **Note:**
>
> Introduced or updated in v1.2.190.

Shows the created indexes. Equivalent to `SELECT * FROM system.indexes`.

See also: [system.indexes](/tidb-cloud-lake/sql/system-indexes.md)

## Syntax

```sql
SHOW INDEXES [LIKE '<pattern>' | WHERE <expr>] | [LIMIT <limit>]
```

## Example

```sql
CREATE TABLE t1(a int,b int);

CREATE AGGREGATING INDEX agg_idx AS SELECT avg(a), abs(sum(b)), abs(b) AS bs FROM t1 GROUP BY bs;

SHOW INDEXES;

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│   name  │     type    │                               original                               │                                     definition                                     │         created_on         │      updated_on     │
├─────────┼─────────────┼──────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────┼────────────────────────────┼─────────────────────┤
│ agg_idx │ AGGREGATING │ SELECT avg(a), abs(sum(b)), abs(b) AS bs FROM default.t1 GROUP BY bs │ SELECT abs(b) AS bs, COUNT(), COUNT(a), SUM(a), SUM(b) FROM default.t1 GROUP BY bs │ 2024-01-29 07:15:34.856234 │ NULL                │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
