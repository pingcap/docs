---
title: TO_TIMESTAMP_TZ
---

Converts a value to [`TIMESTAMP_TZ`](../../00-sql-reference/10-data-types/datetime.md#timestamp_tz), keeping both the UTC moment and the timezone offset. Use `TRY_TO_TIMESTAMP_TZ` if you prefer `NULL` instead of an error.

## Syntax

```sql
TO_TIMESTAMP_TZ(<expr>)
```

`<expr>` can be a string in ISO-8601 style (`YYYY-MM-DD`, `YYYY-MM-DDTHH:MM:SS[.fraction][±offset]`), a `TIMESTAMP`, or a `DATE`.

## Return Type

`TIMESTAMP_TZ`

## Examples

### Parse a string with an explicit offset

```sql
SELECT TO_TIMESTAMP_TZ('2021-12-20 17:01:01.000000 +0000')::STRING AS utc_example;

┌──────────────────────────────────────────┐
│ utc_example                              │
├──────────────────────────────────────────┤
│ 2021-12-20 17:01:01.000000 +0000         │
└──────────────────────────────────────────┘
```

### Promote a TIMESTAMP

```sql
SELECT TO_TIMESTAMP_TZ(TO_TIMESTAMP('2021-12-20 17:01:01.000000'))::STRING AS from_timestamp;

┌──────────────────────────────────────────┐
│ from_timestamp                           │
├──────────────────────────────────────────┤
│ 2021-12-20 17:01:01.000000 +0000         │
└──────────────────────────────────────────┘
```

### Convert back to TIMESTAMP

```sql
SELECT TO_TIMESTAMP(TO_TIMESTAMP_TZ('2021-12-20 17:01:01.000000 +0800')) AS back_to_timestamp;

┌────────────────────────┐
│ back_to_timestamp      │
├────────────────────────┤
│ 2021-12-20T09:01:01    │
└────────────────────────┘
```
