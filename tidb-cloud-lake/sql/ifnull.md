---
title: IFNULL
summary: `<expr1>` が NULL の場合は `<expr2>` を返し、それ以外の場合は `<expr1>` を返します。
---

# IFNULL

`<expr1>` が NULL の場合は `<expr2>` を返し、それ以外の場合は `<expr1>` を返します。

## 構文 {#syntax}

```sql
IFNULL(<expr1>, <expr2>)
```

## エイリアス {#aliases}

- [NVL](/tidb-cloud-lake/sql/nvl.md)

## 例 {#examples}

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