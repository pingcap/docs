---
title: TO_BITMAP
summary: 将一个值转换为 BITMAP 数据类型。
---

# TO_BITMAP

将一个值转换为 BITMAP 数据类型。

## 语法 {#syntax}

```sql
TO_BITMAP( <expr> )
```

## 示例 {#examples}

```sql
SELECT TO_BITMAP('1101');

┌───────────────────┐
│ to_bitmap('1101') │
├───────────────────┤
│ <bitmap binary>   │
└───────────────────┘
```