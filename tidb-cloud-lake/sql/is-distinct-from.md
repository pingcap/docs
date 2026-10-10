---
title: IS [ NOT ] DISTINCT FROM
summary: 2 つの式が等しいか（または等しくないか）を、NULL 可能性を考慮して比較します。つまり、等価比較の際に NULL を既知の値として扱います。
---

# IS [ NOT ] DISTINCT FROM

2 つの式が等しいか（または等しくないか）を、NULL 可能性を考慮して比較します。つまり、等価比較の際に NULL を既知の値として扱います。

## 構文 {#syntax}

```sql
<expr1> IS [ NOT ] DISTINCT FROM <expr2>
```

## 例 {#examples}

```sql
SELECT NULL IS DISTINCT FROM NULL;

┌────────────────────────────┐
│ null is distinct from null │
├────────────────────────────┤
│ false                      │
└────────────────────────────┘
```