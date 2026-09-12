---
title: TO_START_OF_ISO_YEAR
summary: 返回某个日期或带时间的日期（timestamp/datetime）所在 ISO 年的第一天。
---

# TO_START_OF_ISO_YEAR

返回某个日期或带时间的日期（timestamp/datetime）所在 ISO 年的第一天。

## 语法 {#syntax}

```sql
TO_START_OF_ISO_YEAR(<expr>)
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
  to_start_of_iso_year('2023-11-12 09:38:18.165575');

┌────────────────────────────────────────────────────┐
│ to_start_of_iso_year('2023-11-12 09:38:18.165575') │
├────────────────────────────────────────────────────┤
│ 2023-01-02                                         │
└────────────────────────────────────────────────────┘
```