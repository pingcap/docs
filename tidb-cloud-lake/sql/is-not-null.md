---
title: IS_NOT_NULL
summary: 値が NULL ではないかどうかを確認します。
---

# IS_NOT_NULL

値が NULL ではないかどうかを確認します。

## 構文 {#syntax}

```sql
IS_NOT_NULL(<expr>)
```

## 例 {#examples}

```sql
SELECT IS_NOT_NULL(1);

┌────────────────┐
│ is_not_null(1) │
├────────────────┤
│ true           │
└────────────────┘
```