---
title: TIME_SLICE
summary: TIME_SLICE 是一个标量函数，用于将单个日期/时间戳值映射到固定的日历间隔（slice 或 bucket）。
---

# TIME_SLICE

TIME_SLICE 是一个标量函数，用于将单个日期/时间戳值映射到固定的日历间隔（slice 或 bucket）。

它返回包含该时间点的日历区间的边界（起点或终点），通常用于按自定义日历周期对时间序列数据进行分组、聚合和报表，例如按 2 周、3 个月或 15 分钟窗口进行汇总。

## 语法 {#syntax}

```sql
TIME_SLICE(<date_or_time_expr>, <slice_length>, <IntervalKind> [, <start_or_end>])
```

| 参数                  | 描述                                                                 |
|-----------------------|-------------------------------------------------------------------------------------------------------------|
| `<date_or_time_expr>` | DATE、TIME、TIMESTAMP 或其他日期/时间表达式。在可能的情况下，返回类型与输入类型一致。 |
| `<slice_length>`      | INTEGER >= 1。一个 slice 中连续的 IntervalKind 单位数量（例如，2 表示 2 周 slice）。           |
| `<IntervalKind>`      | 以下值之一（不区分大小写）：YEAR、QUARTER、MONTH、WEEK、DAY、HOUR、MINUTE、SECOND。             |
| `<start_or_end>`      | 字符串 'START' 或 'END'（不区分大小写）。如果省略，默认为 'START'。                                |

## 语义 {#semantics}

- 对于给定调用 TIME_SLICE(value, slice_length, IntervalKind, start_or_end)：
    - START 返回该 slice 的精确日历边界起点（包含）。
    - END 返回紧接在该 slice 之后的边界（排他的上界）。根据输入类型和系统精度，如果通过减去最小时间单位将其转换为包含式终点，END 也可以解释为该 slice 中最后一个可表示的时刻。

- 支持的 IntervalKind 与输入类型：
    - DATE 输入：YEAR、QUARTER、MONTH、WEEK、DAY。
    - TIMESTAMP / TIMESTAMPTZ 输入：YEAR、QUARTER、MONTH、WEEK、DAY、HOUR、MINUTE、SECOND（所有 IntervalKind 值）。

- 对齐规则（日历边界）：
    - 年从 1 月 1 日开始。
    - 季度从季度边界开始（1 月 1 日、4 月 1 日、7 月 1 日、10 月 1 日）。
    - 月从每月 1 日开始。
    - 周按照该实现的周规则对齐（默认使用周一作为一周的开始）。
    - 天从 00:00:00 开始。
    - Hour/Minute/Second slice 从这些单位的自然边界开始。

## 返回类型 {#return-type}

- DATE 输入 → 返回 DATE。
- TIMESTAMP 输入 → 返回 TIMESTAMP。

## 示例 {#examples}

```sql
SELECT
    '2019-02-28'::DATE AS "DATE",
        TIME_SLICE("DATE", 4, 'MONTH', 'START') AS "start",
    TIME_SLICE("DATE", 4, 'MONTH', 'END') AS "end";

╭──────────────────────────────────────╮
│    DATE    │    start   │     end    │
├────────────┼────────────┼────────────┤
│ 2019-02-28 │ 2019-01-01 │ 2019-05-01 │
╰──────────────────────────────────────╯

```

```sql
CREATE OR REPLACE TABLE accounts (
  id INT,
  billing_date DATE,
  balance_due DECIMAL(11, 2)
)

INSERT INTO
  accounts (id, billing_date, balance_due)
VALUES
  (1, '2018-07-31', 100.00),
  (2, '2018-08-01', 200.00),
  (3, '2018-08-25', 400.00);

-- Group by 2-week slices:
SELECT
    TIME_SLICE(billing_date, 2, 'WEEK', 'START') AS slice_start,
    TIME_SLICE(billing_date, 2, 'WEEK', 'END') AS slice_end,
    COUNT(*) AS num_late_bills,
    SUM(balance_due) AS total_due
FROM
    accounts
WHERE
    balance_due > 0
GROUP BY 1, 2
ORDER BY
    total_due;

╭─────────────────────────────────────────────────────────────────────────────╮
│   slice_start  │    slice_end   │ num_late_bills │         total_due        │
├────────────────┼────────────────┼────────────────┼──────────────────────────┤
│ 2018-07-23     │ 2018-08-06     │              2 │                   300.00 │
│ 2018-08-20     │ 2018-09-03     │              1 │                   400.00 │
╰─────────────────────────────────────────────────────────────────────────────╯

```

## 另请参阅 {#see-also}

- [DATE_TRUNC](/tidb-cloud-lake/sql/date-trunc.md)：提供类似功能，但使用不同的语法，以获得更好的 SQL 标准兼容性。