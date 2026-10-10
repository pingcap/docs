---
title: TOMORROW
summary: 明日の日付を返します。`today() + 1` と同じです。
---

# TOMORROW

明日の日付を返します。`today() + 1` と同じです。

## 構文 {#syntax}

```sql
TOMORROW()
```

## 戻り値の型 {#return-type}

`DATE`。`YYYY-MM-DD` 形式の日付を返します。

## 例 {#examples}

```sql
SELECT TOMORROW(), TODAY()+1;

┌──────────────────────────┐
│ tomorrow() │ today() + 1 │
├────────────┼─────────────┤
│ 2024-05-23 │ 2024-05-23  │
└──────────────────────────┘
```