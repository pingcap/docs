---
title: YESTERDAY
summary: 返回昨天的日期，与 today() - 1 相同。
---

# YESTERDAY

返回昨天的日期，与 `today() - 1` 相同。

## 语法 {#syntax}

```sql
YESTERDAY()
```

## 返回类型 {#return-type}

`DATE`，以 “YYYY-MM-DD” 格式返回日期。

## 示例 {#examples}

```sql
SELECT YESTERDAY(), TODAY()-1;

┌───────────────────────────┐
│ yesterday() │ today() - 1 │
├─────────────┼─────────────┤
│ 2024-05-21  │ 2024-05-21  │
└───────────────────────────┘
```