---
title: UPPER
---

Returns a string with all characters changed to uppercase.

## Syntax

```sql
UPPER(<str>)
```

## Aliases

- [UCASE](ucase.md)

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