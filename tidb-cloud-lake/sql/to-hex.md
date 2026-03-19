---
title: TO_HEX
summary: For a string argument str, TO_HEX() returns a hexadecimal string representation of str where each byte of each character in str is converted to two hexadecimal digits. The inverse of this operation is performed by the UNHEX() function.
---

# TO_HEX

For a string argument str, TO_HEX() returns a hexadecimal string representation of str where each byte of each character in str is converted to two hexadecimal digits. The inverse of this operation is performed by the UNHEX() function.

For a numeric argument N, TO_HEX() returns a hexadecimal string representation of the value of N treated as a longlong (BIGINT) number.

## Syntax

```sql
TO_HEX(<expr>)
```

## Aliases

- [HEX](/tidb-cloud-lake/sql/hex.md)

## Examples

```sql
SELECT HEX('abc'), TO_HEX('abc');

┌────────────────────────────┐
│ hex('abc') │ to_hex('abc') │
├────────────┼───────────────┤
│ 616263     │ 616263        │
└────────────────────────────┘

SELECT HEX(255), TO_HEX(255);

┌────────────────────────┐
│ hex(255) │ to_hex(255) │
├──────────┼─────────────┤
│ ff       │ ff          │
└────────────────────────┘
```
