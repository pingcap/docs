---
title: AGE
summary: age() 函数用于计算两个时间戳之间的差值，或一个时间戳与当前日期和时间之间的差值。
---

# AGE

age() 函数用于计算两个时间戳之间的差值，或一个时间戳与当前日期和时间之间的差值。

## 语法 {#syntax}

```sql
AGE(<end_timestamp>, <start_timestamp>)
```

| 参数            | 描述                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| `<end_timestamp>`   | 结束时间戳                                       |
| `<start_timestamp>` | 起始时间戳                                |

## 返回类型 {#return-type}

返回 INTERVAL 类型

## 计算逻辑 {#calculation-logic}

该函数计算以下内容：

1. 完整的年份差值（考虑闰年）
2. 剩余的月份差值（考虑每个月长度不同）
3. 剩余的天数差值（包括时间部分）

当 `<end_timestamp>` 早于 `<start_timestamp>` 时，返回负的时间间隔。

## 示例 {#examples}

### 基本 age 计算 {#basic-age-calculation}

```sql
SELECT AGE('2023-03-15'::TIMESTAMP, '2020-01-20'::TIMESTAMP);
├─────────────────────────┤
│ 3 years 1 month 26 days │
╰─────────────────────────╯
```

### 逆向时间顺序 {#reverse-chronology}

```sql
SELECT AGE('2018-12-25'::TIMESTAMP, '2022-05-10'::TIMESTAMP);
├─────────────────────────────┤
│ -3 years -4 months -16 days │
╰─────────────────────────────╯
```

### 包含时间部分 {#with-time-components}

```sql
SELECT AGE('2023-02-28 14:00:00'::TIMESTAMP, '2023-02-27 08:30:00'::TIMESTAMP);
├───────────────┤
│ 1 day 5:30:00 │
╰───────────────╯
```

### 表数据处理 {#table-data-processing}

```sql
CREATE TABLE projects (
    name String,
    start_date TIMESTAMP,
    end_date TIMESTAMP
);

INSERT INTO projects VALUES
    ('Alpha', '2020-06-01', '2023-09-30'),
    ('Beta', '2022-01-15', '2022-11-01');

SELECT
    name,
    AGE(end_date, start_date) AS duration
FROM projects;
╭─────────────────────────────────────────────╮
│       name       │         duration         │
│ Nullable(String) │    Nullable(Interval)    │
├──────────────────┼──────────────────────────┤
│ Alpha            │ 3 years 3 months 29 days │
│ Beta             │ 9 months 17 days         │
╰─────────────────────────────────────────────╯
```

## 另请参阅 {#see-also}

- [DATE_DIFF](/tidb-cloud-lake/sql/date-diff.md)：用于计算特定时间单位差值的替代函数