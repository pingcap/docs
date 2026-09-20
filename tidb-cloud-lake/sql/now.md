---
title: NOW
summary: Returns the current date and time.
---

# NOW

Returns the current date and time.

## Syntax

```sql
NOW()
```

## Return Type

TIMESTAMP

## Aliases

- [CURRENT_TIMESTAMP](/tidb-cloud-lake/sql/current-timestamp.md)

## Examples

This example returns the current date and time:

```sql
SELECT CURRENT_TIMESTAMP(), NOW();

┌─────────────────────────────────────────────────────────┐
│     current_timestamp()    │            now()           │
├────────────────────────────┼────────────────────────────┤
│ 2024-01-29 04:38:12.584359 │ 2024-01-29 04:38:12.584417 │
└─────────────────────────────────────────────────────────┘
```
