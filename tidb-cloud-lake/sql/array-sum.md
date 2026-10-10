---
title: ARRAY_SUM
summary: 配列内の数値要素を合計します。`NULL` 項目はスキップされ、数値以外の値はエラーになります。
---

# ARRAY_SUM

配列内の数値要素を合計します。`NULL` 項目はスキップされ、数値以外の値はエラーになります。

## 構文 {#syntax}

```sql
ARRAY_SUM(<array>)
```

## 戻り値の型 {#return-type}

数値型（配列内で最も広い数値型に一致します）。

## 例 {#examples}

```sql
SELECT ARRAY_SUM([1, 2, 3, 4]) AS total;

┌───────┐
│ total │
├───────┤
│    10 │
└───────┘
```

```sql
SELECT ARRAY_SUM([1.5, 2.25, 3.0]) AS total;

┌────────┐
│ total  │
├────────┤
│   6.75 │
└────────┘
```

```sql
SELECT ARRAY_SUM([10, NULL, -3]) AS total;

┌───────┐
│ total │
├───────┤
│     7 │
└───────┘
```

## 関連 {#related}

- [ARRAY_AGGREGATE](/tidb-cloud-lake/sql/array-aggregate.md)