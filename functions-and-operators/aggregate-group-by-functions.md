---
title: Aggregate (GROUP BY) Functions
summary: Learn about the supported aggregate functions in TiDB.
---

# 集計 (GROUP BY) 関数 {#aggregate-group-by-functions}

このドキュメントでは、TiDB でサポートされている集計関数について詳しく説明します。

## サポートされている集計関数 {#supported-aggregate-functions}

このセクションでは、TiDB でサポートされている MySQL `GROUP BY`集計関数について説明します。

| 名前                                                                                                                       | 説明                                      |
| :----------------------------------------------------------------------------------------------------------------------- | :-------------------------------------- |
| [`COUNT()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_count)                             | 返された行数を返します。                            |
| [`COUNT(DISTINCT)`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_count-distinct)            | さまざまな値の数を返します。                          |
| [`SUM()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_sum)                                 | 合計を返します                                 |
| [`AVG()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_avg)                                 | 引数の平均値を返します                             |
| [`MAX()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_max)                                 | 最大値を返す                                  |
| [`MIN()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_min)                                 | 最小値を返す                                  |
| [`GROUP_CONCAT()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_group-concat)               | 連結された文字列を返す                             |
| [`VARIANCE()` 、 `VAR_POP()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_var-pop)          | 母集団の標準分散を返します                           |
| [`STD()` 、 `STDDEV()` 、 `STDDEV_POP`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_std)     | 母集団の標準偏差を返します                           |
| [`VAR_SAMP()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_var-samp)                       | 標本分散を返す                                 |
| [`STDDEV_SAMP()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_stddev-samp)                 | サンプルの標準偏差を返します                          |
| [`JSON_OBJECTAGG(key, value)`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_json-objectagg) | 結果セットをキーと値のペアを含む単一の JSON オブジェクトとして返します。 |

-   特に明記されていない限り、グループ関数は`NULL`値を無視します。
-   `GROUP BY`句を含まないステートメントでグループ関数を使用すると、すべての行をグループ化することと同じになります。

さらに、TiDB は次の集計関数も提供します。

-   `APPROX_PERCENTILE(expr, constant_integer_expr)`

    この関数は`expr`のパーセンタイルを返します。 `constant_integer_expr`引数は、 `[1,100]`の範囲の定数整数であるパー​​センテージ値を示します。パーセンタイル P <sub>k</sub> ( `k`パーセンテージを表す) は、データ セット内に P <sub>k</sub>以下の値が少なくとも`k%`あることを示します。

    この関数は、 `expr`の戻り値の型として[数値型](/data-type-numeric.md)と[日付と時刻のタイプ](/data-type-date-and-time.md)のみをサポートします。他の返される型の場合、 `APPROX_PERCENTILE` `NULL`のみを返します。

    次の例は、 `INT`列の 50 パーセンタイルを計算する方法を示しています。

    ```sql
    drop table if exists t;
    create table t(a int);
    insert into t values(1), (2), (3);
    ```

    ```sql
    select approx_percentile(a, 50) from t;
    ```

    ```sql
    +--------------------------+
    | approx_percentile(a, 50) |
    +--------------------------+
    |                        2 |
    +--------------------------+
    1 row in set (0.00 sec)
    ```

`GROUP_CONCAT()`と`APPROX_PERCENTILE()`関数を除き、前述のすべての関数が[ウィンドウ関数](/functions-and-operators/window-functions.md)として機能します。

## GROUP BY 修飾子 {#group-by-modifiers}

v7.4.0 以降、TiDB の`GROUP BY`句は`WITH ROLLUP`修飾子をサポートします。詳細については、 [GROUP BY 修飾子](/functions-and-operators/group-by-modifier.md)を参照してください。

## SQLモードのサポート {#sql-mode-support}

TiDB は SQL モード`ONLY_FULL_GROUP_BY`をサポートしており、有効にすると、TiDB はあいまいな非集計列を含むクエリを拒否します。たとえば、リスト`SELECT`の非集計列 &quot;b&quot; が`GROUP BY`ステートメントに現れないため、このクエリは`ONLY_FULL_GROUP_BY`有効になっていると不正になります。

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

`ONLY_FULL_GROUP_BY`の現在の実装は、 MySQL 5.7の実装よりも厳密ではありません。たとえば、結果が「c」順に並べられることを期待して次のクエリを実行するとします。

```sql
drop table if exists t;
create table t(a bigint, b bigint, c bigint);
insert into t values(1, 2, 1), (1, 2, 2), (1, 3, 1), (1, 3, 2);
select distinct a, b from t order by c;
```

結果を順序付けするには、最初に重複を削除する必要があります。しかし、そのためにはどの行を保持すればよいでしょうか?この選択は「c」の保持値に影響を与え、その結果、順序付けに影響を与え、任意になります。

MySQL では、 `ORDER BY`の式が次の条件の少なくとも 1 つを満たさない場合、 `DISTINCT`と`ORDER BY`を含むクエリは無効として拒否されます。

-   式はリスト`SELECT`の 1 に等しい
-   式によって参照され、クエリの選択されたテーブルに属するすべての列は、 `SELECT`リストの要素です。

ただし、TiDB では、上記のクエリは有効です。詳細については、 [#4254](https://github.com/pingcap/tidb/issues/4254)を参照してください。

標準 SQL への別の TiDB 拡張機能では、 `HAVING`節で`SELECT`リストのエイリアス化された式への参照が許可されます。たとえば、次のクエリは、テーブル &quot;orders&quot; に 1 回だけ出現する &quot;name&quot; 値を返します。

```sql
select name, count(name) from orders
group by name
having count(name) = 1;
```

TiDB 拡張機能では、集計列の`HAVING`句でエイリアスの使用が許可されています。

```sql
select name, count(name) as c from orders
group by name
having c = 1;
```

標準 SQL では`GROUP BY`句内の列式のみが許可されるため、「FLOOR(value/100)」は非列式であるため、次のようなステートメントは無効です。

```sql
select id, floor(value/100)
from tbl_name
group by id, floor(value/100);
```

TiDB は標準 SQL を拡張して、 `GROUP BY`節で非列式を許可し、前述のステートメントが有効であるとみなします。

標準 SQL では、 `GROUP BY`句でのエイリアスも許可されません。 TiDB は標準 SQL を拡張してエイリアスを許可するため、クエリを記述する別の方法は次のようになります。

```sql
select id, floor(value/100) as val
from tbl_name
group by id, val;
```

## 関連するシステム変数 {#related-system-variables}

`group_concat_max_len`変数は、 `GROUP_CONCAT()`関数の最大項目数を設定します。
