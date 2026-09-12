---
title: IF
summary: 如果 `<cond1>` 为 TRUE，则返回 `<expr1>`。否则，如果 `<cond2>` 为 TRUE，则返回 `<expr2>`，依此类推。
---

# IF

如果 `<cond1>` 为 TRUE，则返回 `<expr1>`。否则，如果 `<cond2>` 为 TRUE，则返回 `<expr2>`，依此类推。

## 语法 {#syntax}

```sql
IF(<cond1>, <expr1>, [<cond2>, <expr2> ...], <expr_else>)
```

## 别名 {#aliases}

- [IFF](/tidb-cloud-lake/sql/iff.md)

## 示例 {#examples}

```sql
SELECT IF(1 > 2, 3, 4 < 5, 6, 7);

┌───────────────────────────────┐
│ if((1 > 2), 3, (4 < 5), 6, 7) │
├───────────────────────────────┤
│                             6 │
└───────────────────────────────┘
```