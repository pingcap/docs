---
title: Numeric
summary: 基本的な数値データ型。
---

# Numeric

## 整数データ型 {#integer-data-types}

| 名前     | エイリアス | サイズ    | 最小値               | 最大値              |
|----------|-------|---------|----------------------|---------------------|
| TINYINT  | INT8  | 1 byte  | -128                 | 127                 |
| SMALLINT | INT16 | 2 bytes | -32768               | 32767               |
| INT      | INT32 | 4 bytes | -2147483648          | 2147483647          |
| BIGINT   | INT64 | 8 bytes | -9223372036854775808 | 9223372036854775807 |

> **Tip:**
>
> 符号なし整数を使用する場合は、`UNSIGNED` 制約を使用してください。これは MySQL と互換性があります。例:
>
> ```sql
> CREATE TABLE test_numeric(tiny TINYINT, tiny_unsigned TINYINT UNSIGNED)
> ```

## 浮動小数点データ型 {#floating-point-data-types}

| 名前   | サイズ    | 最小値                | 最大値               |
|--------|---------|--------------------------|-------------------------|
| FLOAT  | 4 bytes | -3.40282347e+38          | 3.40282347e+38          |
| DOUBLE | 8 bytes | -1.7976931348623157E+308 | 1.7976931348623157E+308 |

## 関数 {#functions}

[数値関数](/tidb-cloud-lake/sql/numeric-functions.md) を参照してください。

## 例 {#examples}

```sql
CREATE TABLE test_numeric
(
    tiny              TINYINT,
    tiny_unsigned     TINYINT UNSIGNED,
    smallint          SMALLINT,
    smallint_unsigned SMALLINT UNSIGNED,
    int               INT,
    int_unsigned      INT UNSIGNED,
    bigint            BIGINT,
    bigint_unsigned   BIGINT UNSIGNED,
    float             FLOAT,
    double            DOUBLE
);
```

```sql
DESC test_numeric;
```

結果:

```
┌───────────────────────────────────────────────────────────────────┐
│       Field       │        Type       │  Null  │ Default │  Extra │
├───────────────────┼───────────────────┼────────┼─────────┼────────┤
│ tiny              │ TINYINT           │ YES    │ NULL    │        │
│ tiny_unsigned     │ TINYINT UNSIGNED  │ YES    │ NULL    │        │
│ smallint          │ SMALLINT          │ YES    │ NULL    │        │
│ smallint_unsigned │ SMALLINT UNSIGNED │ YES    │ NULL    │        │
│ int               │ INT               │ YES    │ NULL    │        │
│ int_unsigned      │ INT UNSIGNED      │ YES    │ NULL    │        │
│ bigint            │ BIGINT            │ YES    │ NULL    │        │
│ bigint_unsigned   │ BIGINT UNSIGNED   │ YES    │ NULL    │        │
│ float             │ FLOAT             │ YES    │ NULL    │        │
│ double            │ DOUBLE            │ YES    │ NULL    │        │
└───────────────────────────────────────────────────────────────────┘
```