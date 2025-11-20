---
title: Aggregate (GROUP BY) Functions
summary: TiDB でサポートされている集計関数について学習します。
---

# 集計（GROUP BY）関数 {#aggregate-group-by-functions}

このドキュメントでは、TiDB でサポートされている集計関数の詳細について説明します。

## サポートされている集計関数 {#supported-aggregate-functions}

このセクションでは、TiDB でサポートされている MySQL `GROUP BY`集計関数について説明します。

| 名前                                                                                                                   | 説明                                    |
| :------------------------------------------------------------------------------------------------------------------- | :------------------------------------ |
| [`COUNT()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_count)                         | 返された行の数を返す                            |
| [`COUNT(DISTINCT)`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_count-distinct)        | 異なる値の数を返す                             |
| [`SUM()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_sum)                             | 合計を返す                                 |
| [`AVG()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_avg)                             | 引数の平均値を返す                             |
| [`MAX()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_max)                             | 最大値を返す                                |
| [`MIN()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_min)                             | 最小値を返す                                |
| [`GROUP_CONCAT()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_group-concat)           | 連結された文字列を返す                           |
| [`VARIANCE()` 、 `VAR_POP()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_var-pop)      | 母集団標準分散を返す                            |
| [`STD()` 、 `STDDEV()` 、 `STDDEV_POP`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_std) | 母標準偏差を返す                              |
| [`VAR_SAMP()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_var-samp)                   | 標本分散を返す                               |
| [`STDDEV_SAMP()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_stddev-samp)             | 標本標準偏差を返す                             |
| [`JSON_ARRAYAGG()`](/functions-and-operators/json-functions/json-functions-aggregate.md#json_arrayagg)               | 結果セットを単一のJSON配列として返します                |
| [`JSON_OBJECTAGG()`](/functions-and-operators/json-functions/json-functions-aggregate.md#json_objectagg)             | 結果セットをキーと値のペアを含む単一のJSONオブジェクトとして返します。 |

-   特に明記しない限り、グループ関数は`NULL`値を無視します。
-   `GROUP BY`句を含まないステートメントでグループ関数を使用すると、すべての行をグループ化するのと同じになります。

さらに、TiDB は次の集計関数も提供します。

-   `APPROX_PERCENTILE(expr, constant_integer_expr)`

    この関数は`expr`のパーセンタイルを返します。引数`constant_integer_expr`は、 5 から`[1,100]`の範囲の定数整数であるパーセンタイル値を示します。パーセンタイル P <sub>k</sub> （ `k`はパーセンタイルを表します）は、データセット内に P <sub>k</sub>以下の値が少なくとも`k%`あることを示します。

    この関数は、 `expr`の戻り値の型として[数値型](/data-type-numeric.md)と[日付と時刻の種類](/data-type-date-and-time.md)をサポートします。その他の戻り値の型については、 `APPROX_PERCENTILE` `NULL`を返します。

    次の例は、 `INT`列の 50 パーセンタイルを計算する方法を示しています。

    ```sql
    DROP TABLE IF EXISTS t;
    CREATE TABLE t(a INT);
    INSERT INTO t VALUES(1), (2), (3);
    ```

    ```sql
    SELECT APPROX_PERCENTILE(a, 50) FROM t;
    ```

    ```sql
    +--------------------------+
    | APPROX_PERCENTILE(a, 50) |
    +--------------------------+
    |                        2 |
    +--------------------------+
    1 row in set (0.00 sec)
    ```

-   `APPROX_COUNT_DISTINCT(expr, [expr...])`

    この関数は、異なる値の数を数える点では`COUNT(DISTINCT)`に似ていますが、近似値を返します。3 `BJKST`アルゴリズムを使用することで、べき乗分布を持つ大規模なデータセットを処理する際のメモリ消費量を大幅に削減します。さらに、低カーディナリティデータの場合、この関数はCPU使用率を効率的に維持しながら高い精度を実現します。

    次の例は、この関数の使用方法を示しています。

    ```sql
    DROP TABLE IF EXISTS t;
    CREATE TABLE t(a INT, b INT, c INT);
    INSERT INTO t VALUES(1, 1, 1), (2, 1, 1), (2, 2, 1), (3, 1, 1), (5, 1, 2), (5, 1, 2), (6, 1, 2), (7, 1, 2);
    ```

    ```sql
    SELECT APPROX_COUNT_DISTINCT(a, b) FROM t GROUP BY c;
    ```

        +-----------------------------+
        | approx_count_distinct(a, b) |
        +-----------------------------+
        |                           3 |
        |                           4 |
        +-----------------------------+
        2 rows in set (0.00 sec)

`GROUP_CONCAT()` 、 `APPROX_PERCENTILE()` 、 `APPROX_COUNT_DISTINCT`関数を除き、前述の関数はすべて[ウィンドウ関数](/functions-and-operators/window-functions.md)として機能します。

## GROUP BY修飾子 {#group-by-modifiers}

TiDB v7.4.0以降、 `GROUP BY`句は`WITH ROLLUP`修飾子をサポートします。詳細については、 [GROUP BY修飾子](/functions-and-operators/group-by-modifier.md)参照してください。

## SQLモードのサポート {#sql-mode-support}

TiDBはSQLモード`ONLY_FULL_GROUP_BY`をサポートしており、有効にすると、曖昧な非集計列を含むクエリを拒否します。例えば、次のクエリは`ONLY_FULL_GROUP_BY`が有効になっていると無効になります。5 `SELECT`のリストにある非集計列「b」が`GROUP BY`ステートメントに含まれていないためです。

```sql
drop table if exists t;
create table t(a bigint, b bigint, c bigint);
insert into t values(1, 2, 3), (2, 2, 3), (3, 2, 3);

mysql> select a, b, sum(c) from t group by a;
+------+------+--------+
| a    | b    | sum(c) |
+------+------+--------+
|    1 |    2 |      3 |
|    2 |    2 |      3 |
|    3 |    2 |      3 |
+------+------+--------+
3 rows in set (0.01 sec)

mysql> set sql_mode = 'ONLY_FULL_GROUP_BY';
Query OK, 0 rows affected (0.00 sec)

mysql> select a, b, sum(c) from t group by a;
ERROR 1055 (42000): Expression #2 of SELECT list is not in GROUP BY clause and contains nonaggregated column 'b' which is not functionally dependent on columns in GROUP BY clause; this is incompatible with sql_mode=only_full_group_by
```

TiDB は現在、デフォルトで[`ONLY_FULL_GROUP_BY`](/mysql-compatibility.md#default-differences)モードを有効にしています。

### MySQLとの違い {#differences-from-mysql}

`ONLY_FULL_GROUP_BY`の現在の実装は、 MySQL 5.7の実装よりも厳密ではありません。例えば、結果が「c」で順序付けられることを期待して、次のクエリを実行するとします。

```sql
drop table if exists t;
create table t(a bigint, b bigint, c bigint);
insert into t values(1, 2, 1), (1, 2, 2), (1, 3, 1), (1, 3, 2);
select distinct a, b from t order by c;
```

結果を順序付けるには、まず重複を排除する必要があります。しかし、そのためにはどの行を保持すべきでしょうか？ この選択は「c」の保持値に影響し、さらに順序付けにも影響を与え、結果的に順序付けを恣意的なものにしてしまいます。

MySQL では、 `DISTINCT`と`ORDER BY`含むクエリは、 `ORDER BY`式のいずれかが以下の条件の少なくとも 1 つを満たしていない場合、無効として拒否されます。

-   式は`SELECT`リストの1に等しい
-   式によって参照され、クエリの選択されたテーブルに属するすべての列は、 `SELECT`リストの要素です。

しかし、TiDB では上記のクエリは有効です。詳細については、 [＃4254](https://github.com/pingcap/tidb/issues/4254)参照してください。

標準SQLに対するTiDBのもう一つの拡張機能は、 `HAVING`句で`SELECT`番目のリスト内のエイリアス式を参照することを許可します。例えば、次のクエリはテーブル「orders」に一度だけ出現する「name」の値を返します。

```sql
select name, count(name) from orders
group by name
having count(name) = 1;
```

TiDB 拡張機能では、集計列の`HAVING`句でエイリアスの使用が許可されます。

```sql
select name, count(name) as c from orders
group by name
having c = 1;
```

標準 SQL では、 `GROUP BY`句で列式のみが許可されるため、次のようなステートメントは、「FLOOR(value/100)」が非列式であるため無効です。

```sql
select id, floor(value/100)
from tbl_name
group by id, floor(value/100);
```

TiDB は標準 SQL を拡張して`GROUP BY`句で非列式を許可し、前述のステートメントを有効と見なします。

標準SQLでは、 `GROUP BY`節でのエイリアスの使用は許可されていません。TiDBは標準SQLを拡張してエイリアスの使用を許可しているため、クエリの別の記述方法は次のようになります。

```sql
select id, floor(value/100) as val
from tbl_name
group by id, val;
```

## 関連するシステム変数 {#related-system-variables}

[`group_concat_max_len`](/system-variables.md#group_concat_max_len)変数は、 `GROUP_CONCAT()`関数の項目の最大数を設定します。
