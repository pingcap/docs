---
title: TO_TIMESTAMP
summary: 式を時刻付きの日付に変換します。
---

# TO_TIMESTAMP

式を時刻付きの日付に変換します。

関連項目: [TO_DATE](/tidb-cloud-lake/sql/to-date.md)

## 構文 {#syntax}

この関数は複数のオーバーロードをサポートしており、次のユースケースに対応しています。

```sql
-- Convert a string or integer to a timestamp
TO_TIMESTAMP(<expr>)
```

[ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) 形式の日付文字列が指定された場合、この関数は文字列から日付を抽出します。整数が指定された場合、この関数はその整数を、Unix エポック（1970 年 1 月 1 日 00:00:00）より前（負の数の場合）または後（正の数の場合）の秒数、ミリ秒数、またはマイクロ秒数として解釈します。どの単位として解釈するかは、`x` の絶対値によって決まります。

| 範囲                                        | 単位                 |
|---------------------------------------------|----------------------|
| \|x\| < 31,536,000,000                      | 秒                   |
| 31,536,000,000 ≤ \|x\| < 31,536,000,000,000 | ミリ秒               |
| \|x\| ≥ 31,536,000,000,000                  | マイクロ秒           |

```sql
-- Convert a string to a timestamp using the given pattern
TO_TIMESTAMP(<expr>, <pattern>)
```

この関数は、2 番目の文字列で指定されたパターンに基づいて、最初の文字列を timestamp に変換します。パターンを指定するには、specifier を使用します。specifier を使うことで、日付および時刻の値に対して希望する形式を定義できます。サポートされている specifier の一覧については、[日付と時刻の書式設定](/tidb-cloud-lake/sql/date-time.md#formatting-date-and-time) を参照してください。

```sql
-- Convert an integer to a timestamp based on the specified scale
TO_TIMESTAMP(<int>, <scale>)
```

この関数は整数値を timestamp に変換し、その整数を Unix エポック（1970 年 1 月 1 日 00:00:00）からの秒数（または、指定された scale に基づく小数秒を含む値）として解釈します。scale は小数秒の精度を定義し、0 から 6 までの値をサポートします。例:

- `scale = 0`: 整数を秒として解釈します。
- `scale = 1`: 整数を 10 分の 1 秒として解釈します。
- `scale = 6`: 整数をマイクロ秒として解釈します。

## 戻り値の型 {#return-type}

`YYYY-MM-DD hh:mm:ss.ffffff` 形式の timestamp を返します。

- 返される timestamp は常に {{{ .lake }}} のタイムゾーンを反映します。
    - 指定された文字列にタイムゾーン情報が含まれている場合、timestamp は {{{ .lake }}} で設定されたタイムゾーンに対応する時刻へ変換されます。つまり、timestamp は {{{ .lake }}} に設定されたタイムゾーンを反映するように調整されます。

    ```sql
    -- Set timezone to 'America/Toronto' (UTC-5:00, Eastern Standard Time)
    SET timezone = 'America/Toronto';

    SELECT TO_TIMESTAMP('2022-01-02T01:12:00-07:00'), TO_TIMESTAMP('2022/01/02T01:12:00-07:00', '%Y/%m/%dT%H:%M:%S%::z');

    ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
    │ to_timestamp('2022-01-02t01:12:00-07:00') │ to_timestamp('2022/01/02t01:12:00-07:00', '%y/%m/%dt%h:%m:%s%::z') │
    ├───────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┤
    │ 2022-01-02 03:12:00                       │ 2022-01-02 03:12:00                                                │
    └────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
    ```

    - 指定された文字列にタイムゾーン情報がない場合、その timestamp は現在のセッションで設定されているタイムゾーンに属するものとして扱われます。

    ```sql
    -- Set timezone to 'America/Toronto' (UTC-5:00, Eastern Standard Time)
    SET timezone = 'America/Toronto';

    SELECT TO_TIMESTAMP('2022-01-02T01:12:00'), TO_TIMESTAMP('2022/01/02T01:12:00', '%Y/%m/%dT%H:%M:%S');

    ┌────────────────────────────────────────────────────────────────────────────────────────────────┐
    │ to_timestamp('2022-01-02t01:12:00') │ to_timestamp('2022/01/02t01:12:00', '%y/%m/%dt%h:%m:%s') │
    ├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
    │ 2022-01-02 01:12:00                 │ 2022-01-02 01:12:00                                      │
    └────────────────────────────────────────────────────────────────────────────────────────────────┘
    ```

- 指定された文字列がこの形式に一致していても時刻部分を含まない場合は、自動的にこのパターンへ拡張されます。埋められる値は 0 です。
- 変換に失敗した場合はエラーが返されます。このようなエラーを回避するには、[TRY_TO_TIMESTAMP](/tidb-cloud-lake/sql/try-to-timestamp.md) 関数を使用できます。

    ```sql
    root@localhost:8000/default> SELECT TO_TIMESTAMP('20220102');
    error: APIError: ResponseError with 1006: cannot parse to type `TIMESTAMP` while evaluating function `to_timestamp('20220102')`

    root@localhost:8000/default> SELECT TRY_TO_TIMESTAMP('20220102');

    SELECT
    try_to_timestamp('20220102')

    ┌──────────────────────────────┐
    │ try_to_timestamp('20220102') │
    ├──────────────────────────────┤
    │ NULL                         │
    └──────────────────────────────┘
    ```

## エイリアス {#aliases}

- [TO_DATETIME](/tidb-cloud-lake/sql/datetime.md)
- [STR_TO_TIMESTAMP](/tidb-cloud-lake/sql/str-to-timestamp.md)

## 例 {#examples}

### 例 1: 文字列を Timestamp に変換する {#example-1-converting-string-to-timestamp}

```sql
SELECT TO_TIMESTAMP('2022-01-02 02:00:11');

┌─────────────────────────────────────┐
│ to_timestamp('2022-01-02 02:00:11') │
├─────────────────────────────────────┤
│ 2022-01-02 02:00:11                 │
└─────────────────────────────────────┘

SELECT TO_TIMESTAMP('2022-01-02T01');

┌───────────────────────────────┐
│ to_timestamp('2022-01-02t01') │
├───────────────────────────────┤
│ 2022-01-02 01:00:00           │
└───────────────────────────────┘

-- Set timezone to 'America/Toronto' (UTC-5:00, Eastern Standard Time)
SET timezone = 'America/Toronto';
-- Convert provided string to current timezone ('America/Toronto')
SELECT TO_TIMESTAMP('2022-01-02T01:12:00-07:00');

┌───────────────────────────────────────────┐
│ to_timestamp('2022-01-02t01:12:00-07:00') │
├───────────────────────────────────────────┤
│ 2022-01-02 03:12:00                       │
└───────────────────────────────────────────┘
```

### 例 2: 整数を Timestamp に変換する {#example-2-converting-integer-to-timestamp}

```sql
SELECT TO_TIMESTAMP(1), TO_TIMESTAMP(-1);

┌───────────────────────────────────────────┐
│   to_timestamp(1)   │  to_timestamp(- 1)  │
├─────────────────────┼─────────────────────┤
│ 1969-12-31 19:00:01 │ 1969-12-31 18:59:59 │
└───────────────────────────────────────────┘
```

整数の文字列を timestamp に変換することもできます。

```sql
SELECT TO_TIMESTAMP(TO_INT64('994518299'));

┌─────────────────────────────────────┐
│ to_timestamp(to_int64('994518299')) │
├─────────────────────────────────────┤
│ 2001-07-07 15:04:59                 │
└─────────────────────────────────────┘
```

- 変換には `SELECT TO_TIMESTAMP('994518299', '%s')` も使用できますが、推奨されません。このような変換では、より良いパフォーマンスのために、{{{ .lake }}} は上記の例の方法を使用することを推奨します。

- Timestamp 値の範囲は 1000-01-01 00:00:00.000000 から 9999-12-31 23:59:59.999999 です。次のステートメントを実行すると、{{{ .lake }}} はエラーを返します。

```bash
root@localhost:8000/default> SELECT TO_TIMESTAMP(9999999999999999999);
error: APIError: ResponseError with 1006: number overflowed while evaluating function `to_int64(9999999999999999999)`
```

### 例 3: パターンを使用して文字列を変換する {#example-3-converting-string-with-pattern}

```sql
-- Set timezone to 'America/Toronto' (UTC-5:00, Eastern Standard Time)
SET timezone = 'America/Toronto';

-- Convert provided string to current timezone ('America/Toronto')
SELECT TO_TIMESTAMP('2022/01/02T01:12:00-07:00', '%Y/%m/%dT%H:%M:%S%::z');

┌────────────────────────────────────────────────────────────────────┐
│ to_timestamp('2022/01/02t01:12:00-07:00', '%y/%m/%dt%h:%m:%s%::z') │
├────────────────────────────────────────────────────────────────────┤
│ 2022-01-02 03:12:00                                                │
└────────────────────────────────────────────────────────────────────┘

-- If no timezone is specified, the session's time zone applies.
SELECT TO_TIMESTAMP('2022/01/02T01:12:00', '%Y/%m/%dT%H:%M:%S');

┌──────────────────────────────────────────────────────────┐
│ to_timestamp('2022/01/02t01:12:00', '%y/%m/%dt%h:%m:%s') │
├──────────────────────────────────────────────────────────┤
│ 2022-01-02 01:12:00                                      │
└──────────────────────────────────────────────────────────┘
```

### 例 4: スケール付き整数の変換 {#example-4-converting-integer-with-scale}

```sql
-- Interpret an integer with seconds precision (scale = 0)
SELECT TO_TIMESTAMP(1638473645, 0), TO_TIMESTAMP(-1638473645, 0);

┌─────────────────────────────────────────────────────────────┐
│ to_timestamp(1638473645, 0) │ to_timestamp(- 1638473645, 0) │
├─────────────────────────────┼───────────────────────────────┤
│ 2021-12-02 19:34:05         │ 1918-01-30 04:25:55           │
└─────────────────────────────────────────────────────────────┘

-- Interpret an integer with milliseconds precision (scale = 3)
SELECT TO_TIMESTAMP(1638473645123, 3);

┌────────────────────────────────┐
│ to_timestamp(1638473645123, 3) │
├────────────────────────────────┤
│ 2021-12-02 19:34:05.123        │
└────────────────────────────────┘
```