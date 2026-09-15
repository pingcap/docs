---
title: TODAY
summary: 返回当前日期。
---

# TODAY

返回当前日期。

## 语法 {#syntax}

```sql
TODAY()
```

## 返回类型 {#return-type}

`DATE`，返回 “YYYY-MM-DD” 格式的日期。

## 示例 {#examples}

```sql
SELECT TODAY();

┌────────────┐
│   today()  │
├────────────┤
│ 2024-05-22 │
└────────────┘
```