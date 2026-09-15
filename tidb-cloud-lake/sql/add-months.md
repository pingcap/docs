---
title: ADD_MONTHS
summary: add_months() 函数将指定数量的月份添加到给定的日期或时间戳。
---

# ADD_MONTHS

add_months() 函数将指定数量的月份添加到给定的日期或时间戳。

如果输入日期是月末，或者超过结果月份的天数，则结果会调整为新月份的最后一天。否则，将保留原始日期中的日。

## 语法 {#syntax}

```sql
ADD_MONTHS(<date_or_timestamp>, <number_of_months>)
```

| 参数 | 描述 |
|----------------------|-----------------------------------------------------------------------------|
| `<date_or_timestamp>` | 要添加月份的起始日期或时间戳 |
| `<number_of_months>`  | 要添加的月份整数值（可以为负数，表示减去月份） |

## 返回类型 {#return-type}

返回 TIMESTAMP 或 DATE 类型

## 示例 {#examples}

### 基本月份加法 {#basic-month-addition}

```sql
SELECT ADD_MONTHS('2023-01-15'::DATE, 3);
├───────────────────────────────────┤
│ 2023-04-15                        │
╰───────────────────────────────────╯
```

### 减去月份 {#subtracting-months}

```sql
SELECT ADD_MONTHS('2023-06-20'::DATE, -4);
├─────────────────────────────────────┤
│ 2023-02-20                          │
╰─────────────────────────────────────╯
```

### 月末调整 {#month-end-adjustment}

```sql
SELECT ADD_MONTHS('2023-01-31'::DATE, 1);
├───────────────────────────────────┤
│ 2023-02-28                        │
╰───────────────────────────────────╯
```

### 保留时间戳 {#with-timestamp-preservation}

```sql
SELECT ADD_MONTHS('2023-03-15 14:30:00'::TIMESTAMP, 5);
├─────────────────────────────────────────────────┤
│ 2023-08-15 14:30:00.000000                      │
╰─────────────────────────────────────────────────╯
```

### 处理月末日期 {#with-last-day-of-month}

```sql
CREATE TABLE contracts (
    id INT,
    sign_date DATE,
    duration_months INT
);

INSERT INTO contracts VALUES
    (1, '2023-01-15', 12),
    (2, '2024-02-28', 6),
    (3, '2023-11-30', 3);

SELECT
    id,
    sign_date,
    ADD_MONTHS(sign_date, duration_months) AS end_date
FROM contracts;
├─────────────────┼────────────────┼────────────────┤
│               1 │ 2023-01-15     │ 2024-01-15     │
│               2 │ 2024-02-28     │ 2024-08-28     │
│               3 │ 2023-11-30     │ 2024-02-29     │
╰───────────────────────────────────────────────────╯

```

## 另请参阅 {#see-also}

- [DATE_ADD](/tidb-cloud-lake/sql/date-add.md)：用于添加特定时间间隔的替代函数
- [DATE_SUB](/tidb-cloud-lake/sql/date-sub.md)：用于减去时间间隔的函数