---
title: H3_IS_PENTAGON
---

Checks if the given [H3](https://eng.uber.com/h3/) index represents a pentagonal cell. 

## Syntax

```sql
H3_IS_PENTAGON(h3)
```

## Examples

```sql
SELECT H3_IS_PENTAGON(599119489002373119);

┌────────────────────────────────────┐
│ h3_is_pentagon(599119489002373119) │
├────────────────────────────────────┤
│ true                               │
└────────────────────────────────────┘
```