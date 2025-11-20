---
title: Window Functions
summary: このドキュメントでは、TiDB でサポートされているウィンドウ関数について説明します。
---

# ウィンドウ関数 {#window-functions}

TiDBにおけるウィンドウ関数の使用方法は、MySQL 8.0と同様です。詳細については[MySQL ウィンドウ関数](https://dev.mysql.com/doc/refman/8.0/en/window-functions.html)参照してください。

TiDB では、次のシステム変数を使用してウィンドウ関数を制御できます。

-   [`tidb_enable_window_function`](/system-variables.md#tidb_enable_window_function) : ウィンドウ関数はパーサー内で追加の[キーワード](/keywords.md)予約するため、TiDB はこの変数を使用してウィンドウ関数を無効化します。TiDB のアップグレード後に SQL 文の解析エラーが発生する場合は、この変数を`OFF`に設定してみてください。
-   [`tidb_enable_pipelined_window_function`](/system-variables.md#tidb_enable_pipelined_window_function) : この変数を使用して、ウィンドウ関数のパイプライン実行アルゴリズムを無効にすることができます。
-   [`windowing_use_high_precision`](/system-variables.md#windowing_use_high_precision) : この変数を使用して、ウィンドウ関数の高精度モードを無効にすることができます。

ウィンドウ関数[ここに記載](/tiflash/tiflash-supported-pushdown-calculations.md) TiFlashにプッシュダウンできます。

TiDBは、 `GROUP_CONCAT()`と`APPROX_PERCENTILE()`を除く[`GROUP BY`集計関数](/functions-and-operators/aggregate-group-by-functions.md)すべてをウィンドウ関数として使用できます。さらに、TiDBは以下のウィンドウ関数もサポートしています。

| 関数名                               | 機能の説明                                                                    |
| :-------------------------------- | :----------------------------------------------------------------------- |
| [`CUME_DIST()`](#cume_dist)       | 値のグループ内の値の累積分布を返します。                                                     |
| [`DENSE_RANK()`](#dense_rank)     | パーティション内の現在の行のランクを返します。ランクにはギャップはありません。                                  |
| [`FIRST_VALUE()`](#first_value)   | 現在のウィンドウの最初の行の式の値を返します。                                                  |
| [`LAG()`](#lag)                   | パーティション内の現在の行の N 行前の行から式の値を返します。                                         |
| [`LAST_VALUE()`](#last_value)     | 現在のウィンドウの最後の行の式の値を返します。                                                  |
| [`LEAD()`](#lead)                 | パーティション内の現在の行から N 行後の行の式の値を返します。                                         |
| [`NTH_VALUE()`](#nth_value)       | 現在のウィンドウの N 行目から式の値を返します。                                                |
| [`NTILE()`](#ntile)               | パーティションを N 個のバケットに分割し、パーティション内の各行にバケット番号を割り当て、パーティション内の現在の行のバケット番号を返します。 |
| [`PERCENT_RANK()`](#percent_rank) | 現在の行の値より小さいパーティション値の割合を返します。                                             |
| [`RANK()`](#rank)                 | パーティション内の現在の行の順位を返します。順位にはギャップがある場合があります。                                |
| [`ROW_NUMBER()`](#row_number)     | パーティション内の現在の行番号を返します。                                                    |

## <code>CUME_DIST()</code> {#code-cume-dist-code}

`CUME_DIST()`値のグループ内における値の累積分布を計算します。値のグループをソートするには、 `ORDER BY`節と`CUME_DIST()`を使用する必要があります。そうしないと、この関数は期待される値を返しません。

```sql
WITH RECURSIVE cte(n) AS (
    SELECT 1
    UNION
    SELECT
        n+2
    FROM
        cte
    WHERE
        n<6
)
SELECT
    *,
    CUME_DIST() OVER(ORDER BY n)
FROM
    cte;
```

    +------+------------------------------+
    | n    | CUME_DIST() OVER(ORDER BY n) |
    +------+------------------------------+
    |    1 |                         0.25 |
    |    3 |                          0.5 |
    |    5 |                         0.75 |
    |    7 |                            1 |
    +------+------------------------------+
    4 rows in set (0.00 sec)

## <code>DENSE_RANK()</code> {#code-dense-rank-code}

`DENSE_RANK()`関数は現在行の順位を返します。3 [`RANK()`](#rank)と似ていますが、同順位（同じ値と順序条件を共有する行）の場合に空白を残しません。

```sql
SELECT
    *,
    DENSE_RANK() OVER (ORDER BY n)
FROM (
    SELECT 5 AS 'n'
    UNION ALL
    SELECT 8
    UNION ALL
    SELECT 5
    UNION ALL
    SELECT 30
    UNION ALL
    SELECT 31
    UNION ALL
    SELECT 32) a;
```

    +----+--------------------------------+
    | n  | DENSE_RANK() OVER (ORDER BY n) |
    +----+--------------------------------+
    |  5 |                              1 |
    |  5 |                              1 |
    |  8 |                              2 |
    | 30 |                              3 |
    | 31 |                              4 |
    | 32 |                              5 |
    +----+--------------------------------+
    6 rows in set (0.00 sec)

## <code>FIRST_VALUE()</code> {#code-first-value-code}

`FIRST_VALUE(expr)`ウィンドウ内の最初の値を返します。

次の例では、 2 つの異なるウィンドウ定義を使用しています。

-   `PARTITION BY n MOD 2 ORDER BY n`テーブル`a`のデータを`1, 3`と`2, 4` 2つのグループに分割します。したがって、これらのグループの最初の値である`1`または`2`返されます。
-   `PARTITION BY n <= 2 ORDER BY n`テーブル`a`のデータを`1, 2`と`3, 4` 2 つのグループに分割します。したがって、 `n`どのグループに属しているかに応じて`1`または`3`返します。

```sql
SELECT
    n,
    FIRST_VALUE(n) OVER (PARTITION BY n MOD 2 ORDER BY n),
    FIRST_VALUE(n) OVER (PARTITION BY n <= 2 ORDER BY n)
FROM (
    SELECT 1 AS 'n'
    UNION
    SELECT 2
    UNION
    SELECT 3
    UNION
    SELECT 4
) a
ORDER BY
    n;
```

    +------+-------------------------------------------------------+------------------------------------------------------+
    | n    | FIRST_VALUE(n) OVER (PARTITION BY n MOD 2 ORDER BY n) | FIRST_VALUE(n) OVER (PARTITION BY n <= 2 ORDER BY n) |
    +------+-------------------------------------------------------+------------------------------------------------------+
    |    1 |                                                     1 |                                                    1 |
    |    2 |                                                     2 |                                                    1 |
    |    3 |                                                     1 |                                                    3 |
    |    4 |                                                     2 |                                                    3 |
    +------+-------------------------------------------------------+------------------------------------------------------+
    4 rows in set (0.00 sec)

## <code>LAG()</code> {#code-lag-code}

`LAG(expr [, num [, default]])`関数は、現在行の`num`行前にある行の値`expr`を返します。そのような行が存在しない場合は、 `default`が返されます。デフォルトでは、 `num`は`1`は`default` `NULL`扱われます。

次の例では、 `num`指定されていないため、 `LAG(n)`前の行の`n`の値を返します。7が`n`の場合、前の行は存在せず、 `default`指定されていないため、 `LAG(1)`は`NULL`返します。

```sql
WITH RECURSIVE cte(n) AS (
    SELECT 1
    UNION
    SELECT
        n+1
    FROM
        cte
    WHERE
        n<10
)
SELECT
    n,
    LAG(n) OVER ()
FROM
    cte;
```

    +------+----------------+
    | n    | LAG(n) OVER () |
    +------+----------------+
    |    1 |           NULL |
    |    2 |              1 |
    |    3 |              2 |
    |    4 |              3 |
    |    5 |              4 |
    |    6 |              5 |
    |    7 |              6 |
    |    8 |              7 |
    |    9 |              8 |
    |   10 |              9 |
    +------+----------------+
    10 rows in set (0.01 sec)

## <code>LAST_VALUE()</code> {#code-last-value-code}

`LAST_VALUE()`関数はウィンドウ内の最後の値を返します。

```sql
WITH RECURSIVE cte(n) AS (
    SELECT
        1
    UNION
    SELECT
        n+1
    FROM
        cte
    WHERE
        n<10
)
SELECT
    n,
    LAST_VALUE(n) OVER (PARTITION BY n<=5)
FROM
    cte
ORDER BY
    n;
```

    +------+----------------------------------------+
    | n    | LAST_VALUE(n) OVER (PARTITION BY n<=5) |
    +------+----------------------------------------+
    |    1 |                                      5 |
    |    2 |                                      5 |
    |    3 |                                      5 |
    |    4 |                                      5 |
    |    5 |                                      5 |
    |    6 |                                     10 |
    |    7 |                                     10 |
    |    8 |                                     10 |
    |    9 |                                     10 |
    |   10 |                                     10 |
    +------+----------------------------------------+
    10 rows in set (0.00 sec)

## <code>LEAD()</code> {#code-lead-code}

`LEAD(expr [, num [,default]])`関数は、現在の行から`num`行後の行の値`expr`返します。そのような行が存在しない場合は、 `default`が返されます。デフォルトでは、 `num`指定されていない場合は`1`が、 `default`指定されていない場合は`NULL`が返されます。

次の例では、 `num`指定されていないため、 `LEAD(n)`現在行の次の行の`n`の値を返します`n`が10の場合、次の行は存在せず、 `default`指定されていないため、 `LEAD(10)` `NULL`返します。

```sql
WITH RECURSIVE cte(n) AS (
    SELECT
        1
    UNION
    SELECT
        n+1
    FROM
        cte
    WHERE
        n<10
)
SELECT
    n,
    LEAD(n) OVER ()
FROM
    cte;
```

    +------+-----------------+
    | n    | LEAD(n) OVER () |
    +------+-----------------+
    |    1 |               2 |
    |    2 |               3 |
    |    3 |               4 |
    |    4 |               5 |
    |    5 |               6 |
    |    6 |               7 |
    |    7 |               8 |
    |    8 |               9 |
    |    9 |              10 |
    |   10 |            NULL |
    +------+-----------------+
    10 rows in set (0.00 sec)

## <code>NTH_VALUE()</code> {#code-nth-value-code}

`NTH_VALUE(expr, n)`関数はウィンドウの`n`番目の値を返します。

```sql
WITH RECURSIVE cte(n) AS (
    SELECT
        1
    UNION
    SELECT
        n+1
    FROM
        cte
    WHERE
        n<10
)
SELECT
    n,
    FIRST_VALUE(n) OVER w AS 'First',
    NTH_VALUE(n, 2) OVER w AS 'Second',
    NTH_VALUE(n, 3) OVER w AS 'Third',
    LAST_VALUE(n) OVER w AS 'Last'
FROM
    cte
WINDOW
    w AS (PARTITION BY n<=5)
ORDER BY
    n;
```

    +------+-------+--------+-------+------+
    | n    | First | Second | Third | Last |
    +------+-------+--------+-------+------+
    |    1 |     1 |      2 |     3 |    5 |
    |    2 |     1 |      2 |     3 |    5 |
    |    3 |     1 |      2 |     3 |    5 |
    |    4 |     1 |      2 |     3 |    5 |
    |    5 |     1 |      2 |     3 |    5 |
    |    6 |     6 |      7 |     8 |   10 |
    |    7 |     6 |      7 |     8 |   10 |
    |    8 |     6 |      7 |     8 |   10 |
    |    9 |     6 |      7 |     8 |   10 |
    |   10 |     6 |      7 |     8 |   10 |
    +------+-------+--------+-------+------+
    10 rows in set (0.00 sec)

## <code>NTILE()</code> {#code-ntile-code}

`NTILE(n)`関数はウィンドウを`n`グループに分割し、各行のグループ番号を返します。

```sql
WITH RECURSIVE cte(n) AS (
    SELECT
        1
    UNION
    SELECT
        n+1
    FROM
        cte
    WHERE
    n<10
)
SELECT
    n,
    NTILE(5) OVER (),
    NTILE(2) OVER ()
FROM
    cte;
```

```
+------+------------------+------------------+
| n    | NTILE(5) OVER () | NTILE(2) OVER () |
+------+------------------+------------------+
|    1 |                1 |                1 |
|    2 |                1 |                1 |
|    3 |                2 |                1 |
|    4 |                2 |                1 |
|    5 |                3 |                1 |
|    6 |                3 |                2 |
|    7 |                4 |                2 |
|    8 |                4 |                2 |
|    9 |                5 |                2 |
|   10 |                5 |                2 |
+------+------------------+------------------+
10 rows in set (0.00 sec)

```

## <code>PERCENT_RANK()</code> {#code-percent-rank-code}

`PERCENT_RANK()`関数は、現在の行の値よりも小さい値を持つ行の割合を示す 0 から 1 までの数値を返します。

```sql
SELECT
    *,
    PERCENT_RANK() OVER (ORDER BY n),
    PERCENT_RANK() OVER (ORDER BY n DESC)
FROM (
    SELECT 5 AS 'n'
    UNION ALL
    SELECT 8
    UNION ALL
    SELECT 5
    UNION ALL
    SELECT 30
    UNION ALL
    SELECT 31
    UNION ALL
    SELECT 32) a;
```

    +----+----------------------------------+---------------------------------------+
    | n  | PERCENT_RANK() OVER (ORDER BY n) | PERCENT_RANK() OVER (ORDER BY n DESC) |
    +----+----------------------------------+---------------------------------------+
    |  5 |                                0 |                                   0.8 |
    |  5 |                                0 |                                   0.8 |
    |  8 |                              0.4 |                                   0.6 |
    | 30 |                              0.6 |                                   0.4 |
    | 31 |                              0.8 |                                   0.2 |
    | 32 |                                1 |                                     0 |
    +----+----------------------------------+---------------------------------------+
    6 rows in set (0.00 sec)

## <code>RANK()</code> {#code-rank-code}

`RANK()`関数は[`DENSE_RANK()`](#dense_rank)に似ていますが、同点（同じ値と順序条件を持つ行）の場合は空白を残します。つまり、絶対的な順位付けを提供します。例えば、順位が 7 の場合、それより低い順位の行が 6 行あることを意味します。

```sql
SELECT
    *,
    RANK() OVER (ORDER BY n),
    DENSE_RANK() OVER (ORDER BY n)
FROM (
    SELECT 5 AS 'n'
    UNION ALL
    SELECT 8
    UNION ALL
    SELECT 5
    UNION ALL
    SELECT 30
    UNION ALL
    SELECT 31
    UNION ALL
    SELECT 32) a;
```

    +----+--------------------------+--------------------------------+
    | n  | RANK() OVER (ORDER BY n) | DENSE_RANK() OVER (ORDER BY n) |
    +----+--------------------------+--------------------------------+
    |  5 |                        1 |                              1 |
    |  5 |                        1 |                              1 |
    |  8 |                        3 |                              2 |
    | 30 |                        4 |                              3 |
    | 31 |                        5 |                              4 |
    | 32 |                        6 |                              5 |
    +----+--------------------------+--------------------------------+
    6 rows in set (0.00 sec)

## <code>ROW_NUMBER()</code> {#code-row-number-code}

`ROW_NUMBER()`結果セット内の現在の行の行番号を返します。

```sql
WITH RECURSIVE cte(n) AS (
    SELECT
        1
    UNION
    SELECT
        n+3
    FROM
        cte
    WHERE
        n<30
)
SELECT
    n,
    ROW_NUMBER() OVER ()
FROM
    cte;
```

    +------+----------------------+
    | n    | ROW_NUMBER() OVER () |
    +------+----------------------+
    |    1 |                    1 |
    |    4 |                    2 |
    |    7 |                    3 |
    |   10 |                    4 |
    |   13 |                    5 |
    |   16 |                    6 |
    |   19 |                    7 |
    |   22 |                    8 |
    |   25 |                    9 |
    |   28 |                   10 |
    |   31 |                   11 |
    +------+----------------------+
    11 rows in set (0.00 sec)
