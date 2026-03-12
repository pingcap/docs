---
title: Interval
sidebar_position: 7
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.677"/>

## Overview

`INTERVAL` represents a duration that can be written in natural-language text (`'1 year 2 months'`, `'3 days ago'`) or as an integer number of microseconds. Databend supports units from millennia down to microseconds and allows arithmetic on intervals, dates, and timestamps.

:::note
Fractional parts are discarded when parsing numeric intervals. `'1.6 seconds'` becomes a 1-second interval.
:::

## Examples

### Literals and Numeric Values

```sql
CREATE OR REPLACE TABLE intervals (duration INTERVAL);

INSERT INTO intervals VALUES
  ('1 year 2 months'),       -- positive natural language
  ('1 year 2 months ago'),   -- negative because of "ago"
  ('1000000'),               -- 1 second in microseconds
  ('-1000000');              -- -1 second

SELECT TO_STRING(duration) AS duration_text FROM intervals;
```

Result:
```
┌──────────────────────┐
│ duration_text        │
├──────────────────────┤
│ 1 year 2 months      │
│ -1 year -2 months    │
│ 0:00:01              │
│ -0:00:01             │
└──────────────────────┘
```

```sql
SELECT
  TO_STRING(TO_INTERVAL('1 seconds'))   AS whole,
  TO_STRING(TO_INTERVAL('1.6 seconds')) AS fractional;
```

Result:
```
┌────────┬────────────┐
│ whole  │ fractional │
├────────┼────────────┤
│ 0:00:01 │ 0:00:01   │
└────────┴────────────┘
```

### Interval Arithmetic

```sql
SELECT
  TO_STRING(TO_DAYS(3) + TO_DAYS(1)) AS add_interval,
  TO_STRING(TO_DAYS(3) - TO_DAYS(1)) AS subtract_interval;
```

Result:
```
┌──────────────┬──────────────────┐
│ add_interval │ subtract_interval │
├──────────────┼──────────────────┤
│ 4 days       │ 2 days           │
└──────────────┴──────────────────┘
```

### Apply to DATE and TIMESTAMP

```sql
SELECT
  DATE '2024-12-20' + TO_DAYS(2) AS add_days,
  DATE '2024-12-20' - TO_DAYS(2) AS subtract_days,
  TIMESTAMP '2024-12-20 10:00:00' + TO_HOURS(36) AS add_hours,
  TIMESTAMP '2024-12-20 10:00:00' - TO_HOURS(36) AS subtract_hours;
```

Result:
```
┌────────────────────┬────────────────────┬────────────────────┬────────────────────┐
│ add_days           │ subtract_days      │ add_hours          │ subtract_hours     │
├────────────────────┼────────────────────┼────────────────────┼────────────────────┤
│ 2024-12-22T00:00:00 │ 2024-12-18T00:00:00 │ 2024-12-21T22:00:00 │ 2024-12-18T22:00:00 │
└────────────────────┴────────────────────┴────────────────────┴────────────────────┘
```

Intervals are added or subtracted just like numbers, making it easy to slide windows or compute offsets with precise control down to microseconds.
