---
title: STRING_TO_H3
---

Converts the string representation to [H3](https://eng.uber.com/h3/) (uint64) representation.

## Syntax

```sql
STRING_TO_H3(h3)
```

## Examples

```sql
SELECT STRING_TO_H3('8d11aa6a38826ff');

┌─────────────────────────────────┐
│ string_to_h3('8d11aa6a38826ff') │
├─────────────────────────────────┤
│              635318325446452991 │
└─────────────────────────────────┘
```