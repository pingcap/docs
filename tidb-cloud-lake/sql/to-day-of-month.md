---
title: TO_DAY_OF_MONTH
summary: 将日期或带时间的日期（timestamp/datetime）转换为一个 UInt8 数字，表示该日期是当月的第几天（1-31）。
---

# TO_DAY_OF_MONTH

将日期或带时间的日期（timestamp/datetime）转换为一个 UInt8 数字，表示该日期是当月的第几天（1-31）。

## 语法 {#syntax}

```sql
TO_DAY_OF_MONTH(<expr>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|----------------|
| `<expr>`  | 日期/时间戳 |

## 别名 {#aliases}

- [DAY](/tidb-cloud-lake/sql/day.md)

## 返回类型 {#return-type}

`TINYINT`

## 示例 {#examples}

```sql
SELECT NOW(), TO_DAY_OF_MONTH(NOW()), DAY(NOW());

┌──────────────────────────────────────────────────────────────────┐
│            now()           │ to_day_of_month(now()) │ day(now()) │
├────────────────────────────┼────────────────────────┼────────────┤
│ 2024-03-14 23:35:41.947962 │                     14 │         14 │
└──────────────────────────────────────────────────────────────────┘
```