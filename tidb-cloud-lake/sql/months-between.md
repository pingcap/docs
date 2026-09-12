---
title: MONTHS_BETWEEN
summary: 返回 *date1* 和 *date2* 之间的月数。
---

# MONTHS_BETWEEN

返回 *date1* 和 *date2* 之间的月数。

## 语法 {#syntax}

```sql
MONTHS_BETWEEN( <date1>, <date2> )
```

## 参数 {#arguments}

*date1* 和 *date2* 可以是 DATE 类型、TIMESTAMP 类型，或两者混合使用。

## 返回类型 {#return-type}

该函数根据以下规则返回一个 FLOAT 值：

- 如果 *date1* 早于 *date2*，则函数返回负值；否则返回正值。

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

- 如果 *date1* 和 *date2* 分别处于各自月份中的同一天，或者两者都是各自月份的最后一天，则结果为整数。否则，函数会基于 31 天的月份来计算结果的小数部分。

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

- 如果 *date1* 和 *date2* 是同一天，函数会忽略任何时间部分并返回 0。

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