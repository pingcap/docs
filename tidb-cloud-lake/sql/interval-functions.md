---
title: Interval Functions
summary: This section provides reference information for the interval functions in Databend. Interval functions allow you to create interval values of various time units for use in date and time calculations.
---
This section provides reference information for the interval functions in Databend. Interval functions allow you to create interval values of various time units for use in date and time calculations.

## Time Unit Conversion Functions

### Day-based Intervals

| Function | Description | Example |
|----------|-------------|--------|
| [TO_DAYS](/tidb-cloud-lake/sql/days.md) | Converts a number to an interval of days | `TO_DAYS(2)` → `2 days` |
| [TO_WEEKS](/tidb-cloud-lake/sql/weeks.md) | Converts a number to an interval of weeks | `TO_WEEKS(3)` → `21 days` |
| [TO_MONTHS](/tidb-cloud-lake/sql/months.md) | Converts a number to an interval of months | `TO_MONTHS(2)` → `2 months` |
| [TO_YEARS](/tidb-cloud-lake/sql/years.md) | Converts a number to an interval of years | `TO_YEARS(1)` → `1 year` |

### Hour-based Intervals

| Function | Description | Example |
|----------|-------------|--------|
| [TO_HOURS](/tidb-cloud-lake/sql/hours.md) | Converts a number to an interval of hours | `TO_HOURS(5)` → `5:00:00` |
| [TO_MINUTES](/tidb-cloud-lake/sql/minutes.md) | Converts a number to an interval of minutes | `TO_MINUTES(90)` → `1:30:00` |
| [TO_SECONDS](/tidb-cloud-lake/sql/seconds.md) | Converts a number to an interval of seconds | `TO_SECONDS(3600)` → `1:00:00` |
| [EPOCH](/tidb-cloud-lake/sql/epoch.md) | Alias for TO_SECONDS | `EPOCH(60)` → `00:01:00` |

### Smaller Time Units

| Function | Description | Example |
|----------|-------------|--------|
| [TO_MILLISECONDS](/tidb-cloud-lake/sql/milliseconds.md) | Converts a number to an interval of milliseconds | `TO_MILLISECONDS(2000)` → `00:00:02` |
| [TO_MICROSECONDS](/tidb-cloud-lake/sql/microseconds.md) | Converts a number to an interval of microseconds | `TO_MICROSECONDS(2000000)` → `00:00:02` |

### Larger Time Units

| Function | Description | Example |
|----------|-------------|--------|
| [TO_DECADES](/tidb-cloud-lake/sql/decades.md) | Converts a number to an interval of decades | `TO_DECADES(2)` → `20 years` |
| [TO_CENTRIES](/tidb-cloud-lake/sql/to-centuries.md) | Converts a number to an interval of centuries | `TO_CENTRIES(1)` → `100 years` |
| [TO_MILLENNIA](/tidb-cloud-lake/sql/millennia.md) | Converts a number to an interval of millennia | `TO_MILLENNIA(1)` → `1000 years` |