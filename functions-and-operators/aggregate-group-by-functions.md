---
title: Aggregate (GROUP BY) Functions
summary: Learn about the supported aggregate functions in TiDB.
---

# 集約（GROUP BY）関数 {#aggregate-group-by-functions}

このドキュメントでは、TiDBでサポートされている集計関数について詳しく説明します。

## サポートされている集計関数 {#supported-aggregate-functions}

このセクションでは、TiDBでサポートされている`GROUP BY`集計関数について説明します。

| 名前                                                                                                                                         | 説明                                   |
| :----------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------- |
| [`COUNT()`](https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_count)                                               | 返された行数のカウントを返します                     |
| [`COUNT(DISTINCT)`](https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_count-distinct)                              | いくつかの異なる値のカウントを返します                  |
| [`SUM()`](https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_sum)                                                   | 合計を返す                                |
| [`AVG()`](https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_avg)                                                   | 引数の平均値を返します                          |
| [`MAX()`](https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_max)                                                   | 最大値を返す                               |
| [`MIN()`](https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_min)                                                   | 最小値を返す                               |
| [`GROUP_CONCAT()`](https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_group-concat)                                 | 連結された文字列を返します                        |
| [`VARIANCE()` 、 <code>VAR_POP()</code>](https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_var-pop)                 | 母分散を返します                             |
| [`STD()` 、 <code>STDDEV()</code> 、 <code>STDDEV_POP</code>](https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_std) | 母標準偏差を返します                           |
| [`VAR_SAMP()`](https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_var-samp)                                         | サンプル分散を返す                            |
| [`STDDEV_SAMP()`](https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_stddev-samp)                                   | サンプルの標準偏差を返します                       |
| [`JSON_OBJECTAGG(key, value)`](https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_json-objectagg)                   | キーと値のペアを含む単一のJSONオブジェクトとして結果セットを返します |

-   特に明記されていない限り、グループ関数は`NULL`の値を無視します。
-   `GROUP BY`句を含まないステートメントでグループ関数を使用する場合、それはすべての行でグループ化することと同じです。

さらに、TiDBは次の集約関数も提供します。

-   `APPROX_PERCENTILE(expr, constant_integer_expr)`

    この関数は、 `expr`のパーセンタイルを返します。 `constant_integer_expr`引数は、 `[1,100]`の範囲の定数整数であるパーセンテージ値を示します。パーセンタイル<sub>Pk</sub> （ `k`はパーセンテージを表す）は、データセットに<sub>Pk</sub>以下の値が少なくとも`k%`あることを示します。

    この関数は、返される`expr`の型として[数値型](/data-type-numeric.md)と[日付と時刻のタイプ](/data-type-date-and-time.md)のみをサポートします。他の返されるタイプの場合、 `APPROX_PERCENTILE`は`NULL`のみを返します。

    次の例は、 `INT`列の50パーセンタイルを計算する方法を示しています。

    {{< copyable "" >}}

    ```sql
    drop table if exists t;
    create table t(a int);
    insert into t values(1), (2), (3);
    ```

    {{< copyable "" >}}

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

## GROUPBY修飾子 {#group-by-modifiers}

TiDBは現在、 `WITH ROLLUP`などの`GROUP BY`の修飾子をサポートしていません。将来的にはサポートを追加する予定です。 [TiDB＃4250](https://github.com/pingcap/tidb/issues/4250)を参照してください。

## SQLモードのサポート {#sql-mode-support}

TiDBはSQLモード`ONLY_FULL_GROUP_BY`をサポートしており、有効にすると、TiDBはあいまいな非集計列を含むクエリを拒否します。たとえば、 `SELECT`リストの非集計列「b」が`GROUP BY`ステートメントに表示されないため、 `ONLY_FULL_GROUP_BY`が有効になっている場合、このクエリは無効です。

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

TiDBは現在、デフォルトで[`ONLY_FULL_GROUP_BY`](/mysql-compatibility.md#default-differences)モードを有効にしています。

### MySQLとの違い {#differences-from-mysql}

`ONLY_FULL_GROUP_BY`の現在の実装は、MySQL5.7の実装よりも厳密ではありません。たとえば、結果が「c」で並べ替えられることを期待して、次のクエリを実行するとします。

```sql
drop table if exists t;
create table t(a bigint, b bigint, c bigint);
insert into t values(1, 2, 1), (1, 2, 2), (1, 3, 1), (1, 3, 2);
select distinct a, b from t order by c;
```

結果を注文するには、最初に重複を排除する必要があります。しかし、そうするために、どの行を保持する必要がありますか？この選択は、「c」の保持値に影響を与えます。これにより、順序が影響を受け、任意になります。

MySQLでは、 `ORDER BY`の式のいずれかが次の条件の少なくとも1つを満たさない場合、 `DISTINCT`と`ORDER BY`を持つクエリは無効として拒否されます。

-   式は1つのリストの`SELECT`つに等しい
-   式によって参照され、クエリで選択されたテーブルに属するすべての列は、 `SELECT`リストの要素です。

ただし、TiDBでは、上記のクエリは有効です。詳細については、 [＃4254](https://github.com/pingcap/tidb/issues/4254)を参照してください。

標準SQLに対する別のTiDB拡張では、 `HAVING`句で`SELECT`リストのエイリアス式を参照できます。たとえば、次のクエリは、テーブル「orders」で1回だけ発生する「name」値を返します。

```sql
select name, count(name) from orders
group by name
having count(name) = 1;
```

TiDB拡張機能では、集約列の`HAVING`句でエイリアスを使用できます。

```sql
select name, count(name) as c from orders
group by name
having c = 1;
```

標準SQLでは`GROUP BY`句の列式のみが許可されているため、「FLOOR（value / 100）」は非列式であるため、このようなステートメントは無効です。

```sql
select id, floor(value/100)
from tbl_name
group by id, floor(value/100);
```

TiDBは、標準SQLを拡張して、 `GROUP BY`節で非列式を許可し、前のステートメントを有効と見なします。

標準SQLでは、 `GROUP BY`句のエイリアスも許可されていません。 TiDBは標準SQLを拡張してエイリアスを許可するため、クエリを作成する別の方法は次のとおりです。

```sql
select id, floor(value/100) as val
from tbl_name
group by id, val;
```

## サポートされていない集計関数 {#unsupported-aggregate-functions}

次の集計関数は、現在TiDBではサポートされていません。あなたは[TiDB＃7623](https://github.com/pingcap/tidb/issues/7623)で私たちの進歩を追跡することができます：

-   `JSON_ARRAYAGG`

## 関連するシステム変数 {#related-system-variables}

`group_concat_max_len`変数は、 `GROUP_CONCAT()`関数のアイテムの最大数を設定します。
