---
title: ADD_MONTHS
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.760"/>

The add_months() function adds a specified number of months to a given date or timestamp.

If the input date is month-end or exceeds the resulting month’s days, the result is adjusted to the last day of the new month. Otherwise, the original day is preserved.

## Syntax

```sql
ADD_MONTHS(<date_or_timestamp>, <number_of_months>)
```

| Parameter            | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| `<date_or_timestamp>` | The starting date or timestamp to which months will be added               |
| `<number_of_months>`  | The integer number of months to add (can be negative to subtract months)   |

## Return Type

Returns a TIMESTAMP or DATE type

## Examples

### Basic Month Addition
```sql
SELECT ADD_MONTHS('2023-01-15'::DATE, 3);
├───────────────────────────────────┤
│ 2023-04-15                        │
╰───────────────────────────────────╯
```

### Subtracting Months
```sql
SELECT ADD_MONTHS('2023-06-20'::DATE, -4);
├─────────────────────────────────────┤
│ 2023-02-20                          │
╰─────────────────────────────────────╯
```

### Month-End Adjustment
```sql
SELECT ADD_MONTHS('2023-01-31'::DATE, 1);
├───────────────────────────────────┤
│ 2023-02-28                        │
╰───────────────────────────────────╯
```

### With Timestamp Preservation
```sql
SELECT ADD_MONTHS('2023-03-15 14:30:00'::TIMESTAMP, 5);
├─────────────────────────────────────────────────┤
│ 2023-08-15 14:30:00.000000                      │
╰─────────────────────────────────────────────────╯
```

### With last day of month
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

## See Also

- [DATE_ADD](date-add.md): Alternative function for adding specific time intervals
- [DATE_SUB](date-sub.md): Function for subtracting time intervals
