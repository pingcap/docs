---
title: LOWER
summary: Returns a string with all characters changed to lowercase.
---

# LOWER

Returns a string with all characters changed to lowercase.

## Syntax

```sql
LOWER(<str>)
```

## Aliases

- [LCASE](/tidb-cloud-lake/sql/lcase.md)

## Return Type

VARCHAR

## Examples

```sql
SELECT LOWER('Hello, DataLake!'), LCASE('Hello, DataLake!');

┌───────────────────────────────────────────────────────┐
│ lower('hello, datalake!') │ lcase('hello, datalake!') │
├───────────────────────────┼───────────────────────────┤
│ hello, datalake!          │ hello, datalake!          │
└───────────────────────────────────────────────────────┘
```
