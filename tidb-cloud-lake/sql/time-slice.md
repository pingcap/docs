---
title: TIME_SLICE
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.799"/>

TIME_SLICE is a scalar function used to map a single date/timestamp value to a fixed calendar interval (slice or bucket). 

It returns the boundary (starting or ending point) of the calendar interval containing the time point, and is often used to group, aggregate and report time series data by custom calendar periods, such as summarizing by a 2-week, 3-month or 15-minute window.

## Syntax

```sql
TIME_SLICE(<date_or_time_expr>, <slice_length>, <IntervalKind> [, <start_or_end>])
```

| Parameter             | Description                                                                                                 |
|-----------------------|-------------------------------------------------------------------------------------------------------------|
| `<date_or_time_expr>` | DATE, TIME, TIMESTAMP or other date/time expression. The return type matches the input type where possible. |
| `<slice_length>`      | INTEGER >= 1. The number of contiguous IntervalKind units in a slice (e.g., 2 for 2-week slices).           |
| `<IntervalKind>`      | One of the following (case-insensitive): YEAR, QUARTER, MONTH, WEEK, DAY, HOUR, MINUTE, SECOND.             |
| `<start_or_end>`      | String 'START' or 'END' (case-insensitive). If omitted, defaults to 'START'.                                |


## Semantics

- For a given call TIME_SLICE(value, slice_length, IntervalKind, start_or_end):
    - START returns the exact calendar boundary that begins the slice (inclusive).
    - END returns the boundary immediately after the slice (an exclusive upper bound). Depending on the input type and system precision, END can also be interpreted as the last representable instant of the slice if you convert it to an inclusive endpoint by subtracting the smallest time unit.

- Supported IntervalKind vs input type:
    - DATE inputs: YEAR, QUARTER, MONTH, WEEK, DAY.
    - TIMESTAMP / TIMESTAMPTZ inputs: YEAR, QUARTER, MONTH, WEEK, DAY, HOUR, MINUTE, SECOND (all IntervalKind values).

- Alignment rules (calendar boundaries):
    - Years start on January 1.
    - Quarters start on quarter boundaries (Jan 1, Apr 1, Jul 1, Oct 1).
    - Months start on the 1st of the month.
    - Weeks are aligned to the implementation’s week convention (Default uses Monday as the week start).
    - Days start at 00:00:00.
    - Hour/Minute/Second slices begin at the natural boundary for those units.

    
## Return Type

- DATE input → returns DATE.
- TIMESTAMP input → returns TIMESTAMP.


## Examples

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

## See Also

- [DATE_TRUNC](date-trunc.md): Provides similar functionality with a different syntax for better SQL standard compatibility.
