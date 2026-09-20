---
title: UPPER
summary: Returns a string with all characters changed to uppercase.
---

# UPPER

Returns a string with all characters changed to uppercase.

## Syntax

```sql
UPPER(<str>)
```

## Aliases

- [UCASE](/tidb-cloud-lake/sql/ucase.md)

## Return Type

VARCHAR

## Examples

```sql
SELECT UPPER('Hello, Datalake!'), UCASE('Hello, Datalake!');

┌───────────────────────────────────────────────────────┐
│ upper('hello, datalake!') │ ucase('hello, datalake!') │
├───────────────────────────┼───────────────────────────┤
│ HELLO, DATALAKE!          │ HELLO, DATALAKE!          │
└───────────────────────────────────────────────────────┘
```
