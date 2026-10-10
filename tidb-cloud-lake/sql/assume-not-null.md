---
title: ASSUME_NOT_NULL
summary: Nullable 型に対して、等価な非 Nullable 値を返します。元の値が NULL の場合、結果は不定です。
---

# ASSUME_NOT_NULL

Nullable 型に対して、等価な非 `Nullable` 値を返します。元の値が `NULL` の場合、結果は不定です。

## 構文 {#syntax}

```sql
ASSUME_NOT_NULL(<x>)
```

## エイリアス {#aliases}

- [REMOVE_NULLABLE](/tidb-cloud-lake/sql/remove-nullable.md)

## 戻り値の型 {#return-type}

非 `Nullable` 型に対しては元のデータ型を返します。`Nullable` 型に対しては、内部に埋め込まれた非 `Nullable` データ型を返します。

## 例 {#examples}

```sql
CREATE TABLE default.t_null ( x int,  y int null);

INSERT INTO default.t_null values (1, null), (2, 3);

SELECT ASSUME_NOT_NULL(y), REMOVE_NULLABLE(y) FROM t_null;

┌─────────────────────────────────────────┐
│ assume_not_null(y) │ remove_nullable(y) │
├────────────────────┼────────────────────┤
│                  0 │                  0 │
│                  3 │                  3 │
└─────────────────────────────────────────┘
```