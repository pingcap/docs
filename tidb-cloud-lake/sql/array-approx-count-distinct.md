---
title: ARRAY_APPROX_COUNT_DISTINCT
---

Returns an approximate count of distinct elements in an array, ignoring `NULL` values. This uses the same HyperLogLog-based estimator as [`APPROX_COUNT_DISTINCT`](../../07-aggregate-functions/aggregate-approx-count-distinct.md).

## Syntax

```sql
ARRAY_APPROX_COUNT_DISTINCT(<array>)
```

## Return Type

`BIGINT`

## Examples

```sql
SELECT ARRAY_APPROX_COUNT_DISTINCT([1, 1, 2, 3, 3, 3]) AS approx_cnt;

┌────────────┐
│ approx_cnt │
├────────────┤
│          3 │
└────────────┘
```

```sql
SELECT ARRAY_APPROX_COUNT_DISTINCT([NULL, 'a', 'a', 'b']) AS approx_cnt_text;

┌──────────────────┐
│ approx_cnt_text  │
├──────────────────┤
│                2 │
└──────────────────┘
```
