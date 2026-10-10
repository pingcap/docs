---
title: ARRAY_APPROX_COUNT_DISTINCT
summary: 配列内の重複しない要素数のおおよその値を返します。`NULL` 値は無視されます。これは、`APPROX_COUNT_DISTINCT` と同じ HyperLogLog ベースの推定器を使用します。
---

# ARRAY_APPROX_COUNT_DISTINCT

配列内の重複しない要素数のおおよその値を返します。`NULL` 値は無視されます。これは、[`APPROX_COUNT_DISTINCT`](/tidb-cloud-lake/sql/approx-count-distinct.md) と同じ HyperLogLog ベースの推定器を使用します。

## 構文 {#syntax}

```sql
ARRAY_APPROX_COUNT_DISTINCT(<array>)
```

## 戻り値の型 {#return-type}

`BIGINT`

## 例 {#examples}

```sql
SELECT ARRAY_APPROX_COUNT_DISTINCT([1, 1, 2, 3, 3, 3]) AS approx_cnt;

┌────────────┐
│ approx_cnt │
├────────────┤
│          3 │
└────────────┘
```

```sql
SELECT ARRAY_APPROX_COUNT_DISTINCT([NULL, 'a', 'a', 'b']) AS approx_cnt_text;

┌──────────────────┐
│ approx_cnt_text  │
├──────────────────┤
│                2 │
└──────────────────┘
```