---
title: COS
summary: 返回 `x` 的余弦值，其中 `x` 以弧度为单位给出。
---

# COS

返回 `x` 的余弦值，其中 `x` 以弧度为单位给出。

## 语法 {#syntax}

```sql
COS( <x> )
```

## 示例 {#examples}

```sql
SELECT COS(PI());

┌───────────┐
│ cos(pi()) │
├───────────┤
│        -1 │
└───────────┘
```