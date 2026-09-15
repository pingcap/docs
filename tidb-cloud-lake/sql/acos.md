---
title: ACOS
summary: 返回 `x` 的反余弦，即余弦值为 `x` 的值。如果 `x` 不在 -1 到 1 的范围内，则返回 NULL。
---

# ACOS

返回 `x` 的反余弦，即余弦值为 `x` 的值。如果 `x` 不在 -1 到 1 的范围内，则返回 NULL。

## 语法 {#syntax}

```sql
ACOS( <x> )
```

## 示例 {#examples}

```sql
SELECT ACOS(1);

┌─────────┐
│ acos(1) │
├─────────┤
│       0 │
└─────────┘
```