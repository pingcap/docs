---
title: UNHEX
---

For a string argument str, UNHEX(str) interprets each pair of characters in the argument as a hexadecimal number and converts it to the byte represented by the number. The return value is a binary string.

## Syntax

```sql
UNHEX(<expr>)
```

## Aliases

- [FROM_HEX](from-hex.md)

## Examples

```sql
SELECT UNHEX('6461746162656e64') as c1, typeof(c1),UNHEX('6461746162656e64')::varchar as c2, typeof(c2), FROM_HEX('6461746162656e64');

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│           c1              │     typeof(c1)         │       c2         |    typeof(c2)     |   from_hex('6461746162656e64')  |
├───────────────────────────┼────────────────────────|──────────────────┤───────────────────|─────────────────────────────────┤
│ 6461746162656E64          │      binary            │      databend    |    varchar        |   6461746162656E64              |
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

SELECT UNHEX(HEX('string')), unhex(HEX('string'))::varchar;

┌──────────────────────────────────────────────────────┐
│ unhex(hex('string')) │ unhex(hex('string'))::varchar │
├──────────────────────┼───────────────────────────────┤
│ 737472696E67         │ string                        │
└──────────────────────────────────────────────────────┘
```
