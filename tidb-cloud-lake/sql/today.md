---
title: TODAY
summary: 現在の日付を返します。
---

# TODAY

現在の日付を返します。

## 構文 {#syntax}

```sql
TODAY()
```

## 戻り値の型 {#return-type}

`DATE`、`YYYY-MM-DD` 形式の日付を返します。

## 例 {#examples}

```sql
SELECT TODAY();

┌────────────┐
│   today()  │
├────────────┤
│ 2024-05-22 │
└────────────┘
```