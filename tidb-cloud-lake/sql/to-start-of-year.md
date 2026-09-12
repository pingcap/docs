---
title: TO_START_OF_YEAR
summary: 返回日期或带时间的日期（timestamp/datetime）所在年份的第一天。
---

# TO_START_OF_YEAR

返回日期或带时间的日期（timestamp/datetime）所在年份的第一天。

## 语法 {#syntax}

```sql
TO_START_OF_YEAR(<expr>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|----------------|
| `<expr>`  | 日期/时间戳 |

## 返回类型 {#return-type}

`DATE`，以 “YYYY-MM-DD” 格式返回日期。

## 示例 {#examples}

```sql
SELECT
  to_start_of_year('2023-11-12 09:38:18.165575');

┌────────────────────────────────────────────────┐
│ to_start_of_year('2023-11-12 09:38:18.165575') │
│                      Date                      │
├────────────────────────────────────────────────┤
│ 2023-01-01                                     │
└────────────────────────────────────────────────┘
```