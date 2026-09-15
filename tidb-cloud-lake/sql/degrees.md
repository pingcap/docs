---
title: DEGREES
summary: 返回参数 `x` 从弧度转换为角度后的值，其中 `x` 以弧度给出。
---

# DEGREES

返回参数 `x` 从弧度转换为角度后的值，其中 `x` 以弧度给出。

## 语法 {#syntax}

```sql
DEGREES( <x> )
```

## 示例 {#examples}

```sql
SELECT DEGREES(PI());

┌───────────────┐
│ degrees(pi()) │
├───────────────┤
│           180 │
└───────────────┘
```