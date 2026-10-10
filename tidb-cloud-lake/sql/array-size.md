---
title: ARRAY_SIZE
summary: NULL 要素を含めて、配列の長さを返します。
---

# ARRAY_SIZE

`NULL` 要素を含めて、配列の長さを返します。

エイリアス: `ARRAY_LENGTH`

## 構文 {#syntax}

```sql
ARRAY_SIZE(<array>)
```

## 戻り値の型 {#return-type}

`BIGINT`

## 例 {#examples}

```sql
SELECT ARRAY_SIZE([1, 2, 3]) AS size_plain;

┌──────────┐
│ size_plain │
├──────────┤
│        3 │
└──────────┘
```

```sql
SELECT ARRAY_SIZE([1, NULL, 3]) AS size_with_null;

┌──────────────┐
│ size_with_null│
├──────────────┤
│            3 │
└──────────────┘
```