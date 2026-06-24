---
title: UNHEX
summary: For a string argument str, UNHEX(str) interprets each pair of characters in the argument as a hexadecimal number and converts it to the byte represented by the number. The return value is a binary string.
---

# UNHEX

For a string argument str, UNHEX(str) interprets each pair of characters in the argument as a hexadecimal number and converts it to the byte represented by the number. The return value is a binary string.

## Syntax

```sql
UNHEX(<expr>)
```

## Aliases

- [FROM_HEX](/tidb-cloud-lake/sql/from-hex.md)

## Examples

```sql
SELECT UNHEX('646174616c616b65') as c1, typeof(c1),UNHEX('646174616c616b65')::varchar as c2, typeof(c2), FROM_HEX('646174616c616b65');

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│           c1              │     typeof(c1)         │       c2         |    typeof(c2)     |   from_hex('646174616c616b65')  |
├───────────────────────────┼────────────────────────|──────────────────┤───────────────────|─────────────────────────────────┤
│ 646174616C616B65          │      binary            │      datalake    |    varchar        |   646174616C616B65              |
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

SELECT UNHEX(HEX('string')), unhex(HEX('string'))::varchar;

┌──────────────────────────────────────────────────────┐
│ unhex(hex('string')) │ unhex(hex('string'))::varchar │
├──────────────────────┼───────────────────────────────┤
│ 737472696E67         │ string                        │
└──────────────────────────────────────────────────────┘
```
