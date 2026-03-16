---
title: NEXT_DAY
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.655"/>

Returns the date of the upcoming specified day of the week after the given date or timestamp.

## Syntax

```sql
NEXT_DAY(<date_expression>, <target_day>)
```

| Parameter           | Description                                                                                                                                                              |
|---------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `<date_expression>` | A `DATE` or `TIMESTAMP` value to calculate the next occurrence of the specified day.                                                                                 |
| `<target_day>`      | The target day of the week to find the next occurrence of. Accepted values include `monday`, `tuesday`, `wednesday`, `thursday`, `friday`, `saturday`, and `sunday`. |

## Return Type

Date.

## Examples

To find the next Monday after a specific date, such as 2024-11-13:

```sql
SELECT NEXT_DAY(to_date('2024-11-13'), monday) AS next_monday;

┌─────────────┐
│ next_monday │
├─────────────┤
│ 2024-11-18  │
└─────────────┘
```