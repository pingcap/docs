---
title: PREVIOUS_DAY
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.655"/>

Returns the date of the most recent specified day of the week before the given date or timestamp.

## Syntax

```sql
PREVIOUS_DAY(<date_expression>, <target_day>)
```

| Parameter           | Description                                                                                                                                                              |
|---------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `<date_expression>` | A `DATE` or `TIMESTAMP` value to calculate the previous occurrence of the specified day.                                                                                 |
| `<target_day>`      | The target day of the week to find the previous occurrence of. Accepted values include `monday`, `tuesday`, `wednesday`, `thursday`, `friday`, `saturday`, and `sunday`. |

## Return Type

Date.

## Examples

If you need to find the previous Friday before a given date, such as 2024-11-13:

```sql
SELECT PREVIOUS_DAY(to_date('2024-11-13'), friday) AS last_friday;

┌─────────────┐
│ last_friday │
├─────────────┤
│ 2024-11-08  │
└─────────────┘
```