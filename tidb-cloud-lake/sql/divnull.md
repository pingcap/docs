---
title: DIVNULL
summary: 1 番目の数値を 2 番目の数値で割った商を返します。2 番目の数値が 0 または NULL の場合は NULL を返します。
---

# DIVNULL

1 番目の数値を 2 番目の数値で割った商を返します。2 番目の数値が 0 または NULL の場合は NULL を返します。

関連情報:

- [DIV](/tidb-cloud-lake/sql/div.md)
- [DIV0](/tidb-cloud-lake/sql/div0.md)

## 構文 {#syntax}

```sql
DIVNULL(<number1>, <number2>)
```

## 例 {#examples}

```sql
SELECT
  DIVNULL(20, 6),
  DIVNULL(20, 0),
  DIVNULL(20, NULL);

┌─────────────────────────────────────────────────────────┐
│   divnull(20, 6)   │ divnull(20, 0) │ divnull(20, null) │
├────────────────────┼────────────────┼───────────────────┤
│ 3.3333333333333335 │ NULL           │ NULL              │
└─────────────────────────────────────────────────────────┘
```