---
title: H3_TO_STRING
---

Converts the representation of the given [H3](https://eng.uber.com/h3/) index to the string representation. 

## Syntax

```sql
H3_TO_STRING(h3)
```

## Examples

```sql
SELECT H3_TO_STRING(635318325446452991);

┌──────────────────────────────────┐
│ h3_to_string(635318325446452991) │
├──────────────────────────────────┤
│ 8d11aa6a38826ff                  │
└──────────────────────────────────┘
```