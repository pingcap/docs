---
title: TO_START_OF_QUARTER
summary: 日付または日時（timestamp/datetime）を、その四半期の初日まで切り下げます。四半期の初日は、1 January、1 April、1 July、または 1 October のいずれかです。日付を返します。
---

# TO_START_OF_QUARTER

日付または日時（timestamp/datetime）を、その四半期の初日まで切り下げます。四半期の初日は、1 January、1 April、1 July、または 1 October のいずれかです。日付を返します。

## 構文 {#syntax}

```sql
TO_START_OF_QUARTER(<expr>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|----------------|
| `<expr>`   | 日付/タイムスタンプ |

## 戻り値の型 {#return-type}

`DATE`。`YYYY-MM-DD` 形式の日付を返します。

## 例 {#examples}

```sql
SELECT
  to_start_of_quarter('2023-11-12 09:38:18.165575');

┌───────────────────────────────────────────────────┐
│ to_start_of_quarter('2023-11-12 09:38:18.165575') │
├───────────────────────────────────────────────────┤
│ 2023-10-01                                        │
└───────────────────────────────────────────────────┘
```