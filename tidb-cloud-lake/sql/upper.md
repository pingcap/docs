---
title: UPPER
summary: Returns a string with all characters changed to uppercase.
---
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
SELECT UPPER('Hello, Databend!'), UCASE('Hello, Databend!');

┌───────────────────────────────────────────────────────┐
│ upper('hello, databend!') │ ucase('hello, databend!') │
├───────────────────────────┼───────────────────────────┤
│ HELLO, DATABEND!          │ HELLO, DATABEND!          │
└───────────────────────────────────────────────────────┘
```