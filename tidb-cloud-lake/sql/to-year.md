---
title: TO_YEAR
summary: 日付または日時（timestamp/datetime）を、西暦の年を含む UInt16 数値に変換します。
---

# TO_YEAR

日付または日時（timestamp/datetime）を、西暦の年を含む UInt16 数値に変換します。

## 構文 {#syntax}

```sql
TO_YEAR(<expr>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|----------------|
| `<expr>`  | 日付/タイムスタンプ |

## エイリアス {#aliases}

- [YEAR](/tidb-cloud-lake/sql/year.md)

## 戻り値の型 {#return-type}

 `SMALLINT`

## 例 {#examples}

```sql
SELECT NOW(), TO_YEAR(NOW()), YEAR(NOW());

┌───────────────────────────────────────────────────────────┐
│            now()           │ to_year(now()) │ year(now()) │
├────────────────────────────┼────────────────┼─────────────┤
│ 2024-03-14 23:37:03.895166 │           2024 │        2024 │
└───────────────────────────────────────────────────────────┘
```