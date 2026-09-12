---
title: RADIANS
summary: 返回参数 `x` 从角度转换为弧度后的值。
---

# RADIANS

返回参数 `x` 从角度转换为弧度后的值。

## 语法 {#syntax}

```sql
RADIANS( <x> )
```

## 示例 {#examples}

```sql
SELECT RADIANS(90);

┌────────────────────┐
│     radians(90)    │
├────────────────────┤
│ 1.5707963267948966 │
└────────────────────┘
```