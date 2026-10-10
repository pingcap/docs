---
title: YESTERDAY
summary: 昨日の日付を返します。`today() - 1` と同じです。
---

# YESTERDAY

昨日の日付を返します。`today() - 1` と同じです。

## 構文 {#syntax}

```sql
YESTERDAY()
```

## 戻り値の型 {#return-type}

`DATE`。`YYYY-MM-DD` 形式の日付を返します。

## 例 {#examples}

```sql
SELECT YESTERDAY(), TODAY()-1;

┌───────────────────────────┐
│ yesterday() │ today() - 1 │
├─────────────┼─────────────┤
│ 2024-05-21  │ 2024-05-21  │
└───────────────────────────┘
```