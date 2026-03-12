---
title: LOWER
---

Returns a string with all characters changed to lowercase.

## Syntax

```sql
LOWER(<str>)
```

## Aliases

- [LCASE](lcase.md)

## Return Type

VARCHAR

## Examples

```sql
SELECT LOWER('Hello, Databend!'), LCASE('Hello, Databend!');

┌───────────────────────────────────────────────────────┐
│ lower('hello, databend!') │ lcase('hello, databend!') │
├───────────────────────────┼───────────────────────────┤
│ hello, databend!          │ hello, databend!          │
└───────────────────────────────────────────────────────┘
```