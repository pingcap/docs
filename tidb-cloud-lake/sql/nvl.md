---
title: NVL
summary: "`<expr1>` が NULL の場合は `<expr2>` を返し、それ以外の場合は `<expr1>` を返します。"
---

# NVL

`<expr1>` が NULL の場合は `<expr2>` を返し、それ以外の場合は `<expr1>` を返します。

## 構文 {#syntax}

```sql
NVL(<expr1>, <expr2>)
```

## エイリアス {#aliases}

- [IFNULL](/tidb-cloud-lake/sql/ifnull.md)

## 例 {#examples}

```sql
SELECT NVL(NULL, 'b'), NVL('a', 'b');

┌────────────────────────────────┐
│ nvl(null, 'b') │ nvl('a', 'b') │
├────────────────┼───────────────┤
│ b              │ a             │
└────────────────────────────────┘

SELECT NVL(NULL, 2), NVL(1, 2);

┌──────────────────────────┐
│ nvl(null, 2) │ nvl(1, 2) │
├──────────────┼───────────┤
│            2 │         1 │
└──────────────────────────┘
```