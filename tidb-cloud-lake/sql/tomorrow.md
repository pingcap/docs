---
title: TOMORROW
summary: 返回明天的日期，与 today() + 1 相同。
---

# TOMORROW

返回明天的日期，与 `today() + 1` 相同。

## 语法 {#syntax}

```sql
TOMORROW()
```

## 返回类型 {#return-type}

`DATE`，以 “YYYY-MM-DD” 格式返回日期。

## 示例 {#examples}

```sql
SELECT TOMORROW(), TODAY()+1;

┌──────────────────────────┐
│ tomorrow() │ today() + 1 │
├────────────┼─────────────┤
│ 2024-05-23 │ 2024-05-23  │
└──────────────────────────┘
```