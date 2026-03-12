---
title: SHA
---

Calculates an SHA-1 160-bit checksum for the string, as described in RFC 3174 (Secure Hash Algorithm). The value is returned as a string of 40 hexadecimal digits or NULL if the argument was NULL.

## Syntax

```sql
SHA(<expr>)
```

## Aliases

- [SHA1](sha1.md)

## Examples

```sql
SELECT SHA('1234567890'), SHA1('1234567890');

┌─────────────────────────────────────────────────────────────────────────────────────┐
│             sha('1234567890')            │            sha1('1234567890')            │
├──────────────────────────────────────────┼──────────────────────────────────────────┤
│ 01b307acba4f54f55aafc33bb06bbbf6ca803e9a │ 01b307acba4f54f55aafc33bb06bbbf6ca803e9a │
└─────────────────────────────────────────────────────────────────────────────────────┘
```