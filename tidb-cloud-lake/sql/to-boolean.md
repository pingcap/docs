---
title: TO_BOOLEAN
summary: 値を BOOLEAN データ型に変換します。
---

# TO_BOOLEAN

値を BOOLEAN データ型に変換します。

## 構文 {#syntax}

```sql
TO_BOOLEAN( <expr> )
```

## 例 {#examples}

```sql
SELECT TO_BOOLEAN('true');

┌────────────────────┐
│ to_boolean('true') │
├────────────────────┤
│ true               │
└────────────────────┘
```