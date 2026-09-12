---
title: IFNULL
summary: 如果 `<expr1>` 为 NULL，则返回 `<expr2>`；否则返回 `<expr1>`。
---

# IFNULL

如果 `<expr1>` 为 NULL，则返回 `<expr2>`；否则返回 `<expr1>`。

## 语法 {#syntax}

```sql
IFNULL(<expr1>, <expr2>)
```

## 别名 {#aliases}

- [NVL](/tidb-cloud-lake/sql/nvl.md)

## 示例 {#examples}

```sql
SELECT IFNULL(NULL, 'b'), IFNULL('a', 'b');

┌──────────────────────────────────────┐
│ ifnull(null, 'b') │ ifnull('a', 'b') │
├───────────────────┼──────────────────┤
│ b                 │ a                │
└──────────────────────────────────────┘

SELECT IFNULL(NULL, 2), IFNULL(1, 2);

┌────────────────────────────────┐
│ ifnull(null, 2) │ ifnull(1, 2) │
├─────────────────┼──────────────┤
│               2 │            1 │
└────────────────────────────────┘
```