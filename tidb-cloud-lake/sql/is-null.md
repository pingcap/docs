---
title: IS_NULL
summary: 値が NULL かどうかを確認します。
---

# IS_NULL

値が NULL かどうかを確認します。

## 構文 {#syntax}

```sql
IS_NULL(<expr>)
```

## 例 {#examples}

```sql
SELECT IS_NULL(1);

┌────────────┐
│ is_null(1) │
├────────────┤
│ false      │
└────────────┘
```