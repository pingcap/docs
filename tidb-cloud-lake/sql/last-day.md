---
title: LAST_DAY
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.655"/>

Returns the last day of the specified interval (week, month, quarter, or year) based on the provided date or timestamp.

## Syntax

```sql
LAST_DAY(<date_expression>, <date_part>)
```

| Parameter           | Description                                                                                                   |
|---------------------|---------------------------------------------------------------------------------------------------------------|
| `<date_expression>` | A DATE or TIMESTAMP value to calculate the last day of the specified interval.                                |
| `<date_part>`       | The date_part for which to find the last day. Accepted values are `week`, `month`, `quarter`, and `year`.     |

## Return Type

Date.

## Examples

Let's say you want to determine the billing date, which is always the last day of the month, based on an arbitrary date of a transaction (e.g., 2024-11-13):

```sql
SELECT LAST_DAY(to_date('2024-11-13'), month) AS billing_date;

┌──────────────┐
│ billing_date │
├──────────────┤
│ 2024-11-30   │
└──────────────┘
```
