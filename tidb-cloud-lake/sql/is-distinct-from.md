---
title: IS [ NOT ] DISTINCT FROM
summary: 在考虑可空性的情况下比较两个表达式是否相等（或不相等），这意味着它将 NULL 视为已知值来进行相等性比较。
---

# IS [ NOT ] DISTINCT FROM

在考虑可空性的情况下比较两个表达式是否相等（或不相等），这意味着它将 NULL 视为已知值来进行相等性比较。

## 语法 {#syntax}

```sql
<expr1> IS [ NOT ] DISTINCT FROM <expr2>
```

## 示例 {#examples}

```sql
SELECT NULL IS DISTINCT FROM NULL;

┌────────────────────────────┐
│ null is distinct from null │
├────────────────────────────┤
│ false                      │
└────────────────────────────┘
```