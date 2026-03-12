---
title: MONTHS_BETWEEN
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.307"/>

Returns the number of months between *date1* and *date2*.

## Syntax

```sql
MONTHS_BETWEEN( <date1>, <date2> )
```

## Arguments

*date1* and *date2* can be of DATE type, TIMESTAMP type, or a mix of both.

## Return Type

The function returns a FLOAT value based on the following rules:

- If *date1* is earlier than *date2*, the function returns a negative value; otherwise, it returns a positive value.

    ```sql title='Example:'
    SELECT
        MONTHS_BETWEEN('2024-03-15'::DATE,
                    '2024-02-15'::DATE),
        MONTHS_BETWEEN('2024-02-15'::DATE,
                    '2024-03-15'::DATE);

    -[ RECORD 1 ]-----------------------------------
    months_between('2024-03-15'::date, '2024-02-15'::date): 1
    months_between('2024-02-15'::date, '2024-03-15'::date): -1
    ```

- If *date1* and *date2* fall on the same day of their respective months or both are the last day of their respective months, the result is an integer. Otherwise, the function calculates the fractional portion of the result based on a 31-day month.

    ```sql title='Example:'
    SELECT
        MONTHS_BETWEEN('2024-02-29'::DATE,
                    '2024-01-29'::DATE),
        MONTHS_BETWEEN('2024-02-29'::DATE,
                    '2024-01-31'::DATE);

    -[ RECORD 1 ]-----------------------------------
    months_between('2024-02-29'::date, '2024-01-29'::date): 1
    months_between('2024-02-29'::date, '2024-01-31'::date): 1

    SELECT
        MONTHS_BETWEEN('2024-08-05'::DATE,
                    '2024-01-01'::DATE);

    -[ RECORD 1 ]-----------------------------------
    months_between('2024-08-05'::date, '2024-01-01'::date): 7.129032258064516
    ```

- If *date1* and *date2* are the same date, the function ignores any time components and returns 0.

    ```sql title='Example:'
    SELECT
        MONTHS_BETWEEN('2024-08-05'::DATE,
                    '2024-08-05'::DATE),
        MONTHS_BETWEEN('2024-08-05 02:00:00'::TIMESTAMP,
                    '2024-08-05 01:00:00'::TIMESTAMP);

    -[ RECORD 1 ]-----------------------------------
                                months_between('2024-08-05'::date, '2024-08-05'::date): 0
    months_between('2024-08-05 02:00:00'::timestamp, '2024-08-05 01:00:00'::timestamp): 0
    ```