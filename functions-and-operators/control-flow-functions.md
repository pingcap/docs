---
title: Control Flow Functions
summary: 制御フロー関数について学習します。
---

# 制御フロー関数 {#control-flow-functions}

TiDB は、MySQL 8.0 で利用可能な[制御フロー関数](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html)のすべてをサポートします。

| 名前                    | 説明                        |
| :-------------------- | :------------------------ |
| [`CASE`](#case)       | ケース演算子                    |
| [`IF()`](#if)         | If/else構文                 |
| [`IFNULL()`](#ifnull) | null if/else 構文           |
| [`NULLIF()`](#nullif) | expr1 = expr2の場合は`NULL`返す |

## 場合 {#case}

[`CASE`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#operator_case)演算子を使用すると、条件付きロジックを実行し、指定された条件に基づいてクエリ結果をカスタマイズできます。

構文：

```sql
CASE
    WHEN condition1 THEN result1
    WHEN condition2 THEN result2
    ...
    ELSE default_result
END
```

例：

```sql
WITH RECURSIVE d AS (SELECT 1 AS n UNION ALL SELECT n+1 FROM d WHERE n<10)
SELECT n, CASE WHEN n MOD 2 THEN "odd" ELSE "even" END FROM d;
```

    +----+----------------------------------------------+
    | n  | CASE WHEN n MOD 2 THEN "odd" ELSE "even" END |
    +----+----------------------------------------------+
    |  1 | odd                                          |
    |  2 | even                                         |
    |  3 | odd                                          |
    |  4 | even                                         |
    |  5 | odd                                          |
    |  6 | even                                         |
    |  7 | odd                                          |
    |  8 | even                                         |
    |  9 | odd                                          |
    | 10 | even                                         |
    +----+----------------------------------------------+
    10 rows in set (0.00 sec)

## もし（） {#if}

[`IF()`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_if)関数を使用すると、値または式が真であるかどうかに基づいてさまざまなアクションを実行できます。

構文：

```sql
IF(condition, value_if_true, value_if_false)
```

例：

```sql
WITH RECURSIVE d AS (SELECT 1 AS n UNION ALL SELECT n+1 FROM d WHERE n<10)
SELECT n, IF(n MOD 2, "odd", "even") FROM d;
```

    +----+----------------------------+
    | n  | IF(n MOD 2, "odd", "even") |
    +----+----------------------------+
    |  1 | odd                        |
    |  2 | even                       |
    |  3 | odd                        |
    |  4 | even                       |
    |  5 | odd                        |
    |  6 | even                       |
    |  7 | odd                        |
    |  8 | even                       |
    |  9 | odd                        |
    | 10 | even                       |
    +----+----------------------------+
    10 rows in set (0.00 sec)

## IFNULL() {#ifnull}

[`IFNULL(expr1,expr2)`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_ifnull)関数は、クエリ内の NULL 値を処理するために使用されます。 `expr1`が`NULL`でない場合は`expr1`返し、それ以外の場合は`expr2`返します。

例：

```sql
WITH data AS (SELECT NULL AS x UNION ALL SELECT 1 )
SELECT x, IFNULL(x,'x has no value') FROM data;
```

    +------+----------------------------+
    | x    | IFNULL(x,'x has no value') |
    +------+----------------------------+
    | NULL | x has no value             |
    |    1 | 1                          |
    +------+----------------------------+
    2 rows in set (0.0006 sec)

## NULLIF() {#nullif}

[`NULLIF(expr1,expr2)`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_nullif)関数は、両方の引数が同じか、最初の引数が`NULL`の場合に`NULL`返します。それ以外の場合は、最初の引数を返します。

例：

```sql
WITH RECURSIVE d AS (SELECT 1 AS n UNION ALL SELECT n+1 FROM d WHERE n<10)
SELECT n, NULLIF(n+n, n+2) FROM d;
```

    +----+------------------+
    | n  | NULLIF(n+n, n+2) |
    +----+------------------+
    |  1 |                2 |
    |  2 |             NULL |
    |  3 |                6 |
    |  4 |                8 |
    |  5 |               10 |
    |  6 |               12 |
    |  7 |               14 |
    |  8 |               16 |
    |  9 |               18 |
    | 10 |               20 |
    +----+------------------+
    10 rows in set (0.00 sec)

この例では、 `n` `2`に等しい場合、 `n+n`と`n+2`両方とも`4`に等しくなり、両方の引数が同じになり、関数は`NULL`返します。
