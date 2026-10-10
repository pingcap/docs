---
title: IF
summary: "`<cond1>` が TRUE の場合は `<expr1>` を返します。そうでない場合、`<cond2>` が TRUE なら `<expr2>` を返し、以降も同様です。"
---

# IF

`<cond1>` が TRUE の場合は `<expr1>` を返します。そうでない場合、`<cond2>` が TRUE なら `<expr2>` を返し、以降も同様です。

## 構文 {#syntax}

```sql
IF(<cond1>, <expr1>, [<cond2>, <expr2> ...], <expr_else>)
```

## エイリアス {#aliases}

- [IFF](/tidb-cloud-lake/sql/iff.md)

## 例 {#examples}

```sql
SELECT IF(1 > 2, 3, 4 < 5, 6, 7);

┌───────────────────────────────┐
│ if((1 > 2), 3, (4 < 5), 6, 7) │
├───────────────────────────────┤
│                             6 │
└───────────────────────────────┘
```