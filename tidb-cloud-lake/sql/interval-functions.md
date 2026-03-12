---
title: Interval Functions
---

This section provides reference information for the interval functions in Databend. Interval functions allow you to create interval values of various time units for use in date and time calculations.

## Time Unit Conversion Functions

### Day-based Intervals

| Function | Description | Example |
|----------|-------------|--------|
| [TO_DAYS](interval-functions/to-days) | Converts a number to an interval of days | `TO_DAYS(2)` → `2 days` |
| [TO_WEEKS](interval-functions/to-weeks) | Converts a number to an interval of weeks | `TO_WEEKS(3)` → `21 days` |
| [TO_MONTHS](interval-functions/to-months) | Converts a number to an interval of months | `TO_MONTHS(2)` → `2 months` |
| [TO_YEARS](interval-functions/to-years) | Converts a number to an interval of years | `TO_YEARS(1)` → `1 year` |

### Hour-based Intervals

| Function | Description | Example |
|----------|-------------|--------|
| [TO_HOURS](interval-functions/to-hours) | Converts a number to an interval of hours | `TO_HOURS(5)` → `5:00:00` |
| [TO_MINUTES](interval-functions/to-minutes) | Converts a number to an interval of minutes | `TO_MINUTES(90)` → `1:30:00` |
| [TO_SECONDS](interval-functions/to-seconds) | Converts a number to an interval of seconds | `TO_SECONDS(3600)` → `1:00:00` |
| [EPOCH](interval-functions/epoch) | Alias for TO_SECONDS | `EPOCH(60)` → `00:01:00` |

### Smaller Time Units

| Function | Description | Example |
|----------|-------------|--------|
| [TO_MILLISECONDS](interval-functions/to-milliseconds) | Converts a number to an interval of milliseconds | `TO_MILLISECONDS(2000)` → `00:00:02` |
| [TO_MICROSECONDS](interval-functions/to-microseconds) | Converts a number to an interval of microseconds | `TO_MICROSECONDS(2000000)` → `00:00:02` |

### Larger Time Units

| Function | Description | Example |
|----------|-------------|--------|
| [TO_DECADES](interval-functions/to-decades) | Converts a number to an interval of decades | `TO_DECADES(2)` → `20 years` |
| [TO_CENTRIES](interval-functions/to-centries) | Converts a number to an interval of centuries | `TO_CENTRIES(1)` → `100 years` |
| [TO_MILLENNIA](interval-functions/to-millennia) | Converts a number to an interval of millennia | `TO_MILLENNIA(1)` → `1000 years` |