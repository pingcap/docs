---
title: TO_VARIANT
summary: 将一个值转换为 VARIANT 数据类型。
---

# TO_VARIANT

将一个值转换为 VARIANT 数据类型。

## 语法 {#syntax}

```sql
TO_VARIANT( <expr> )
```

## 示例 {#examples}

```sql
SELECT TO_VARIANT(TO_BITMAP('100,200,300'));

┌──────────────────────────────────────┐
│ to_variant(to_bitmap('100,200,300')) │
├──────────────────────────────────────┤
│ [100,200,300]                        │
└──────────────────────────────────────┘
```