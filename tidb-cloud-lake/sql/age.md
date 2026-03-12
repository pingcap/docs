---
title: AGE
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.756"/>

The age() function calculates the difference between two timestamps or the difference between a timestamp and the current date and time.

## Syntax

```sql
AGE(<end_timestamp>, <start_timestamp>)
```

| Parameter            | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| `<end_timestamp>`   | The ending timestamp                                       |
| `<start_timestamp>` | The starting timestamp                                |

## Return Type

Returns an INTERVAL type

## Calculation Logic

The function calculates:
1. Full year differences (accounting for leap years)
2. Remaining month differences (considering varying month lengths)
3. Remaining day differences (including time components)

Negative intervals are returned when `<end_timestamp>` is earlier than `<start_timestamp>`.

## Examples

### Basic Age Calculation
```sql
SELECT AGE('2023-03-15'::TIMESTAMP, '2020-01-20'::TIMESTAMP);
├─────────────────────────┤
│ 3 years 1 month 26 days │
╰─────────────────────────╯
```

### Reverse Chronology
```sql
SELECT AGE('2018-12-25'::TIMESTAMP, '2022-05-10'::TIMESTAMP);
├─────────────────────────────┤
│ -3 years -4 months -16 days │
╰─────────────────────────────╯
```

### With Time Components
```sql
SELECT AGE('2023-02-28 14:00:00'::TIMESTAMP, '2023-02-27 08:30:00'::TIMESTAMP);
├───────────────┤
│ 1 day 5:30:00 │
╰───────────────╯
```

### Table Data Processing
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


## See Also

- [DATE_DIFF](date-diff.md): Alternative function for calculating specific time unit differences

