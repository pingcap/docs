---
title: "IS [ NOT ] DISTINCT FROM"
---

Compares whether two expressions are equal (or not equal) with awareness of nullability, meaning it treats NULLs as known values for comparing equality.

## Syntax

```sql
<expr1> IS [ NOT ] DISTINCT FROM <expr2>
```

## Examples

```sql
SELECT NULL IS DISTINCT FROM NULL;

┌────────────────────────────┐
│ null is distinct from null │
├────────────────────────────┤
│ false                      │
└────────────────────────────┘
```