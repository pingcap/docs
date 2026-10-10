---
title: MONTHS_BETWEEN
summary: "*date1* と *date2* の間の月数を返します。"
---

# MONTHS_BETWEEN

*date1* と *date2* の間の月数を返します。

## 構文 {#syntax}

```sql
MONTHS_BETWEEN( <date1>, <date2> )
```

## 引数 {#arguments}

*date1* と *date2* には、DATE 型、TIMESTAMP 型、またはその両方を組み合わせて指定できます。

## 戻り値の型 {#return-type}

この関数は、次のルールに基づいて FLOAT 値を返します。

- *date1* が *date2* より前の日付である場合、この関数は負の値を返します。それ以外の場合は、正の値を返します。

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

- *date1* と *date2* がそれぞれの月の同じ日である場合、または両方がそれぞれの月の末日である場合、結果は整数になります。それ以外の場合、この関数は 31 日の月を基準にして結果の小数部分を計算します。

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

- *date1* と *date2* が同じ日付である場合、この関数は時刻コンポーネントを無視して 0 を返します。

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