---
title: TO_SECONDS
summary: Converts a specified number of seconds into an Interval type.
---

> **Note:**
>
> Introduced or updated in v1.2.677.

Converts a specified number of seconds into an Interval type.

- Accepts positive integers, zero, and negative integers as input.

## Syntax

```sql
TO_SECONDS(<seconds>)
```

## Aliases

- [EPOCH](/tidb-cloud-lake/sql/epoch.md)

## Return Type

Interval (in the format `hh:mm:ss`).

## Examples

```sql
SELECT TO_SECONDS(2), TO_SECONDS(0), TO_SECONDS((- 2));

┌─────────────────────────────────────────────────┐
│ to_seconds(2) │ to_seconds(0) │ to_seconds(- 2) │
├───────────────┼───────────────┼─────────────────┤
│ 0:00:02       │ 00:00:00      │ -0:00:02        │
└─────────────────────────────────────────────────┘
```