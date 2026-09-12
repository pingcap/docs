---
title: MODULO
summary: 返回 `x` 除以 `y` 的余数。如果 `y` 为 0，则返回错误。
---

# MODULO

返回 `x` 除以 `y` 的余数。如果 `y` 为 0，则返回错误。

## 语法 {#syntax}

```sql
MODULO( <x>, <y> )
```

## 别名 {#aliases}

- [MOD](/tidb-cloud-lake/sql/mod.md)

## 示例 {#examples}

```sql
SELECT MOD(9, 2), MODULO(9, 2);

┌──────────────────────────┐
│ mod(9, 2) │ modulo(9, 2) │
├───────────┼──────────────┤
│         1 │            1 │
└──────────────────────────┘
```