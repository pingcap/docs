---
title: Explain Statements That Use Subqueries
summary: TiDB のEXPLAINステートメントによって返される実行プラン情報について学習します。
---

# サブクエリを使用するステートメントの説明 {#explain-statements-that-use-subqueries}

TiDBはサブクエリのパフォーマンスを向上させるために[いくつかの最適化](/subquery-optimization.md)実行します。このドキュメントでは、一般的なサブクエリに対するこれらの最適化のいくつかと、 `EXPLAIN`の出力の解釈方法について説明します。

このドキュメントの例は、次のサンプル データに基づいています。

```sql
CREATE TABLE t1 (id BIGINT NOT NULL PRIMARY KEY auto_increment, pad1 BLOB, pad2 BLOB, pad3 BLOB, int_col INT NOT NULL DEFAULT 0);
CREATE TABLE t2 (id BIGINT NOT NULL PRIMARY KEY auto_increment, t1_id BIGINT NOT NULL, pad1 BLOB, pad2 BLOB, pad3 BLOB, INDEX(t1_id));
CREATE TABLE t3 (
 id INT NOT NULL PRIMARY KEY auto_increment,
 t1_id INT NOT NULL,
 UNIQUE (t1_id)
);

INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM dual;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
UPDATE t1 SET int_col = 1 WHERE pad1 = (SELECT pad1 FROM t1 ORDER BY RAND() LIMIT 1);
INSERT INTO t3 SELECT NULL, id FROM t1 WHERE id < 1000;

SELECT SLEEP(1);
ANALYZE TABLE t1, t2, t3;
```

## 内部結合（一意でないサブクエリ） {#inner-join-non-unique-subquery}

次の例では、 `IN`サブクエリがテーブル`t2`からIDのリストを検索します。セマンティクスの正確性を保つため、TiDBは列`t1_id`一意であることを保証する必要があります。7 `EXPLAIN`のサブクエリを使用すると、重複を削除して`INNER JOIN`操作を実行するための実行プランを確認できます。

```sql
EXPLAIN SELECT * FROM t1 WHERE id IN (SELECT t1_id FROM t2);
```

```sql
+--------------------------------+----------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
| id                             | estRows  | task      | access object                | operator info                                                                                                             |
+--------------------------------+----------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
| IndexJoin_15                   | 21.11    | root      |                              | inner join, inner:TableReader_12, outer key:test.t2.t1_id, inner key:test.t1.id, equal cond:eq(test.t2.t1_id, test.t1.id) |
| ├─StreamAgg_44(Build)          | 21.11    | root      |                              | group by:test.t2.t1_id, funcs:firstrow(test.t2.t1_id)->test.t2.t1_id                                                      |
| │ └─IndexReader_45             | 21.11    | root      |                              | index:StreamAgg_34                                                                                                        |
| │   └─StreamAgg_34             | 21.11    | cop[tikv] |                              | group by:test.t2.t1_id,                                                                                                   |
| │     └─IndexFullScan_26       | 90000.00 | cop[tikv] | table:t2, index:t1_id(t1_id) | keep order:true                                                                                                           |
| └─TableReader_12(Probe)        | 21.11    | root      |                              | data:TableRangeScan_11                                                                                                    |
|   └─TableRangeScan_11          | 21.11    | cop[tikv] | table:t1                     | range: decided by [test.t2.t1_id], keep order:false                                                                       |
+--------------------------------+----------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
```

上記のクエリ結果から、TiDBがインデックス結合操作`IndexJoin_15`を使用してサブクエリを結合および変換していることがわかります。実行プランでは、実行プロセスは次のようになります。

1.  TiKV 側のインデックス スキャン演算子`└─IndexFullScan_26` 、 `t2.t1_id`列目の値を読み取ります。
2.  `└─StreamAgg_34`演算子の一部のタスクは、TiKV 内の`t1_id`の値を重複排除します。
3.  演算子`├─StreamAgg_44(Build)`のいくつかのタスクは、TiDB内の`t1_id`値を重複排除します。重複排除は集計関数`firstrow(test.t2.t1_id)`によって実行されます。
4.  演算結果はテーブル`t1`の主キーと結合されます。結合条件は`eq(test.t1.id, test.t2.t1_id)`です。

## 内部結合（一意のサブクエリ） {#inner-join-unique-subquery}

前の例では、テーブル`t1`に結合する前に、 `t1_id`の値が一意であることを確認するために集計が必要でした。しかし、次の例では、 `UNIQUE`制約により、 `t3.t1_id`既に一意であることが保証されています。

```sql
EXPLAIN SELECT * FROM t1 WHERE id IN (SELECT t1_id FROM t3);
```

```sql
+-----------------------------+---------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
| id                          | estRows | task      | access object                | operator info                                                                                                             |
+-----------------------------+---------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
| IndexJoin_18                | 999.00  | root      |                              | inner join, inner:TableReader_15, outer key:test.t3.t1_id, inner key:test.t1.id, equal cond:eq(test.t3.t1_id, test.t1.id) |
| ├─IndexReader_41(Build)     | 999.00  | root      |                              | index:IndexFullScan_40                                                                                                    |
| │ └─IndexFullScan_40        | 999.00  | cop[tikv] | table:t3, index:t1_id(t1_id) | keep order:false                                                                                                          |
| └─TableReader_15(Probe)     | 999.00  | root      |                              | data:TableRangeScan_14                                                                                                    |
|   └─TableRangeScan_14       | 999.00  | cop[tikv] | table:t1                     | range: decided by [test.t3.t1_id], keep order:false                                                                       |
+-----------------------------+---------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
```

意味的には`t3.t1_id`一意であることが保証されているため、 `INNER JOIN`として直接実行できます。

## セミ結合（相関サブクエリ） {#semi-join-correlated-subquery}

前の2つの例では、TiDBはサブクエリ内のデータが（ `StreamAgg`によって）一意にされた後、または一意であることが保証された後に、 `INNER JOIN`操作を実行できます。どちらの結合もインデックス結合を使用して実行されます。

この例では、TiDB は異なる実行プランを選択します。

```sql
EXPLAIN SELECT * FROM t1 WHERE id IN (SELECT t1_id FROM t2 WHERE t1_id != t1.int_col);
```

```sql
+-----------------------------+----------+-----------+------------------------------+--------------------------------------------------------------------------------------------------------+
| id                          | estRows  | task      | access object                | operator info                                                                                          |
+-----------------------------+----------+-----------+------------------------------+--------------------------------------------------------------------------------------------------------+
| MergeJoin_9                 | 45446.40 | root      |                              | semi join, left key:test.t1.id, right key:test.t2.t1_id, other cond:ne(test.t2.t1_id, test.t1.int_col) |
| ├─IndexReader_24(Build)     | 90000.00 | root      |                              | index:IndexFullScan_23                                                                                 |
| │ └─IndexFullScan_23        | 90000.00 | cop[tikv] | table:t2, index:t1_id(t1_id) | keep order:true                                                                                        |
| └─TableReader_22(Probe)     | 56808.00 | root      |                              | data:Selection_21                                                                                      |
|   └─Selection_21            | 56808.00 | cop[tikv] |                              | ne(test.t1.id, test.t1.int_col)                                                                        |
|     └─TableFullScan_20      | 71010.00 | cop[tikv] | table:t1                     | keep order:true                                                                                        |
+-----------------------------+----------+-----------+------------------------------+--------------------------------------------------------------------------------------------------------+
```

上記の結果から、TiDBが`Semi Join`アルゴリズムを使用していることがわかります。セミ結合は内部結合とは異なり、右側のキーの最初の値（ `t2.t1_id` ）のみを許可します。つまり、重複は結合演算子のタスクの一環として除去されます。結合アルゴリズムもマージ結合であり、演算子が左側と右側の両方からソート順にデータを読み取るため、効率的なジッパー結合に似ています。

元の文は*相関サブクエリ*とみなされます。これは、サブクエリがサブクエリの外部に存在する列 ( `t1.int_col` ) を参照しているためです。ただし、 `EXPLAIN`の出力は、 [サブクエリの相関除去最適化](/correlated-subquery-optimization.md)適用した後の実行プランを示しています。条件`t1_id != t1.int_col`は`t1.id != t1.int_col`に書き換えられます。TiDB はテーブル`t1`からデータを読み取る際に`└─Selection_21`でこれを実行できるため、この相関関係の除去と書き換えによって実行効率が大幅に向上します。

## アンチセミジョイン（サブクエリ<code>NOT IN</code> ） {#anti-semi-join-code-not-in-code-subquery}

次の例では、サブクエリに`t3.t1_id`が含まれてい*ない限り、*クエリは意味的にテーブル`t3`のすべての行を返します。

```sql
EXPLAIN SELECT * FROM t3 WHERE t1_id NOT IN (SELECT id FROM t1 WHERE int_col < 100);
```

```sql
+-----------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------------------------------------------------+
| id                          | estRows | task      | access object | operator info                                                                                                                 |
+-----------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------------------------------------------------+
| IndexJoin_16                | 799.20  | root      |               | anti semi join, inner:TableReader_12, outer key:test.t3.t1_id, inner key:test.t1.id, equal cond:eq(test.t3.t1_id, test.t1.id) |
| ├─TableReader_28(Build)     | 999.00  | root      |               | data:TableFullScan_27                                                                                                         |
| │ └─TableFullScan_27        | 999.00  | cop[tikv] | table:t3      | keep order:false                                                                                                              |
| └─TableReader_12(Probe)     | 999.00  | root      |               | data:Selection_11                                                                                                             |
|   └─Selection_11            | 999.00  | cop[tikv] |               | lt(test.t1.int_col, 100)                                                                                                      |
|     └─TableRangeScan_10     | 999.00  | cop[tikv] | table:t1      | range: decided by [test.t3.t1_id], keep order:false                                                                           |
+-----------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------------------------------------------------+
```

このクエリは、まずテーブル`t3`読み取り、次にテーブル`t1` `PRIMARY KEY`に基づいてプローブを実行します。結合タイプは*アンチセミ結合*です。この例は値 ( `NOT IN` ) が存在しないことを想定しているためアンチ結合、結合を拒否するには最初の行のみが一致する必要があるためセミ結合です。

## Null 対応セミ結合 ( <code>IN</code>および<code>= ANY</code>サブクエリ) {#null-aware-semi-join-code-in-code-and-code-any-code-subqueries}

`IN`または`= ANY`集合演算子の値は3つの値（ `true` 、 `false` 、 `NULL` ）です。2つの演算子のいずれかから変換された結合型の場合、TiDBは結合キーの両側にある`NULL`を認識し、特別な方法で処理する必要があります。

演算子が`IN`つと`= ANY`含まれるサブクエリは、それぞれセミ結合と左外部セミ結合に変換されます。前述の例[セミジョイン](#semi-join-correlated-subquery)では、結合キーの両側の列`test.t1.id`と`test.t2.t1_id` `not NULL`であるため、セミ結合をnull対応と見なす必要はありません（ `NULL`特別な処理は行われません）。TiDBは、特別な最適化を行わずに、カルテシアン積とフィルターに基づいてnull対応セミ結合を処理します。以下は例です。

```sql
CREATE TABLE t(a INT, b INT);
CREATE TABLE s(a INT, b INT);
EXPLAIN SELECT (a,b) IN (SELECT * FROM s) FROM t;
EXPLAIN SELECT * FROM t WHERE (a,b) IN (SELECT * FROM s);
```

```sql
tidb> EXPLAIN SELECT (a,b) IN (SELECT * FROM s) FROM t;
+-----------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------------+
| id                          | estRows | task      | access object | operator info                                                                             |
+-----------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------------+
| HashJoin_8                  | 1.00    | root      |               | CARTESIAN left outer semi join, other cond:eq(test.t.a, test.s.a), eq(test.t.b, test.s.b) |
| ├─TableReader_12(Build)     | 1.00    | root      |               | data:TableFullScan_11                                                                     |
| │ └─TableFullScan_11        | 1.00    | cop[tikv] | table:s       | keep order:false, stats:pseudo                                                            |
| └─TableReader_10(Probe)     | 1.00    | root      |               | data:TableFullScan_9                                                                      |
|   └─TableFullScan_9         | 1.00    | cop[tikv] | table:t       | keep order:false, stats:pseudo                                                            |
+-----------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------------+
5 rows in set (0.00 sec)

tidb> EXPLAIN SELECT * FROM t WHERE (a,b) IN (SELECT * FROM s);
+------------------------------+---------+-----------+---------------+-----------------------------------------------------------------------------------------------------+
| id                           | estRows | task      | access object | operator info                                                                                       |
+------------------------------+---------+-----------+---------------+-----------------------------------------------------------------------------------------------------+
| HashJoin_11                  | 1.00    | root      |               | inner join, equal:[eq(test.t.a, test.s.a) eq(test.t.b, test.s.b)]                                   |
| ├─TableReader_14(Build)      | 1.00    | root      |               | data:Selection_13                                                                                   |
| │ └─Selection_13             | 1.00    | cop[tikv] |               | not(isnull(test.t.a)), not(isnull(test.t.b))                                                        |
| │   └─TableFullScan_12       | 1.00    | cop[tikv] | table:t       | keep order:false, stats:pseudo                                                                      |
| └─HashAgg_17(Probe)          | 1.00    | root      |               | group by:test.s.a, test.s.b, funcs:firstrow(test.s.a)->test.s.a, funcs:firstrow(test.s.b)->test.s.b |
|   └─TableReader_24           | 1.00    | root      |               | data:Selection_23                                                                                   |
|     └─Selection_23           | 1.00    | cop[tikv] |               | not(isnull(test.s.a)), not(isnull(test.s.b))                                                        |
|       └─TableFullScan_22     | 1.00    | cop[tikv] | table:s       | keep order:false, stats:pseudo                                                                      |
+------------------------------+---------+-----------+---------------+-----------------------------------------------------------------------------------------------------+
8 rows in set (0.01 sec)
```

最初のクエリ文`EXPLAIN SELECT (a,b) IN (SELECT * FROM s) FROM t;`では、テーブル`t`と`s`列`a`と`b` NULL 値可能（NULLABLE）であるため、サブクエリ`IN`によって変換された左外部セミ結合は NULL 値に対応します。具体的には、まずカルテシアン積を計算し、次に列`IN`または`= ANY`で連結された列を、フィルタリングのための通常の等価性クエリとして他の条件に組み込みます。

2番目のクエリ文`EXPLAIN SELECT * FROM t WHERE (a,b) IN (SELECT * FROM s);`では、テーブル`t`と`s`列`a`と`b`が NULL 可能であるため、 `IN`サブクエリは NULL 対応のセミ結合に変換される必要があります。しかし、TiDB はセミ結合を内部結合と集計に変換することで最適化します。これは、非スカラー出力の`IN`のサブクエリでは、 `NULL`と`false`等価であるためです。プッシュダウンフィルタの`NULL`行は、 `WHERE`句の否定的なセマンティクスになります。したがって、これらの行は事前に無視できます。

> **注記：**
>
> `Exists`演算子もセミ結合に変換されますが、null を認識しません。

## Null 対応アンチセミ結合 ( <code>NOT IN</code>かつ<code>!= ALL</code>サブクエリ) {#null-aware-anti-semi-join-code-not-in-code-and-code-all-code-subqueries}

`NOT IN`または`!= ALL`集合演算子の値は3つの値（ `true` 、 `false` 、 `NULL` ）です。2つの演算子のいずれかから変換された結合型の場合、TiDBは結合キーの両側にある`NULL`を認識し、特別な方法で処理する必要があります。

演算子が`NOT IN`つと`! = ALL`含まれるサブクエリは、それぞれanti semi join とanti left outer semi join に変換されます。前述の例[アンチセミジョイン](#anti-semi-join-not-in-subquery)では、結合キーの両側の列`test.t3.t1_id`と`test.t1.id` `not NULL`であるため、anti semi join をnull対応として扱う必要はありません（ `NULL`特別な処理は行われません）。

TiDB v6.3.0 は、null 認識アンチ結合 (NAAJ) を次のように最適化します。

-   null 対応等価条件 (NA-EQ) を使用してハッシュ結合を構築する

    集合演算子は等価条件を導入します。この条件では、条件の両側の演算子の`NULL`値に対して特別な処理が必要です。null対応を必要とする等価条件はNA-EQと呼ばれます。以前のバージョンとは異なり、TiDB v6.3.0ではNA-EQを以前のように処理せず、結合後の他の条件にNA-EQを配置し、直積を照合した後に結果セットの正当性を判定します。

    TiDB v6.3.0以降、ハッシュ結合の構築には、弱められた等価条件であるNA-EQが引き続き使用されます。これにより、走査が必要なマッチングデータ量が削減され、マッチング処理が高速化されます。構築テーブルにおける`DISTINCT()`値の合計割合がほぼ100%の場合、加速効果はさらに顕著になります。

-   `NULL`の特別なプロパティを使用して、一致する結果を返す速度を向上します。

    反準結合は連言正規形（CNF）であるため、結合のどちらかの側に`NULL`があれば、結果は確定的になります。この特性を利用することで、マッチング処理全体の戻り値を高速化できます。

次に例を示します。

```sql
CREATE TABLE t(a INT, b INT);
CREATE TABLE s(a INT, b INT);
EXPLAIN SELECT (a, b) NOT IN (SELECT * FROM s) FROM t;
EXPLAIN SELECT * FROM t WHERE (a, b) NOT IN (SELECT * FROM s);
```

```sql
tidb> EXPLAIN SELECT (a, b) NOT IN (SELECT * FROM s) FROM t;
+-----------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------+
| id                          | estRows  | task      | access object | operator info                                                                               |
+-----------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------+
| HashJoin_8                  | 10000.00 | root      |               | Null-aware anti left outer semi join, equal:[eq(test.t.b, test.s.b) eq(test.t.a, test.s.a)] |
| ├─TableReader_12(Build)     | 10000.00 | root      |               | data:TableFullScan_11                                                                       |
| │ └─TableFullScan_11        | 10000.00 | cop[tikv] | table:s       | keep order:false, stats:pseudo                                                              |
| └─TableReader_10(Probe)     | 10000.00 | root      |               | data:TableFullScan_9                                                                        |
|   └─TableFullScan_9         | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo                                                              |
+-----------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------+
5 rows in set (0.00 sec)

tidb> EXPLAIN SELECT * FROM t WHERE (a, b) NOT IN (SELECT * FROM s);
+-----------------------------+----------+-----------+---------------+----------------------------------------------------------------------------------+
| id                          | estRows  | task      | access object | operator info                                                                    |
+-----------------------------+----------+-----------+---------------+----------------------------------------------------------------------------------+
| HashJoin_8                  | 8000.00  | root      |               | Null-aware anti semi join, equal:[eq(test.t.b, test.s.b) eq(test.t.a, test.s.a)] |
| ├─TableReader_12(Build)     | 10000.00 | root      |               | data:TableFullScan_11                                                            |
| │ └─TableFullScan_11        | 10000.00 | cop[tikv] | table:s       | keep order:false, stats:pseudo                                                   |
| └─TableReader_10(Probe)     | 10000.00 | root      |               | data:TableFullScan_9                                                             |
|   └─TableFullScan_9         | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo                                                   |
+-----------------------------+----------+-----------+---------------+----------------------------------------------------------------------------------+
5 rows in set (0.00 sec)
```

最初のクエリ文`EXPLAIN SELECT (a, b) NOT IN (SELECT * FROM s) FROM t;`では、表`t`と`s`の列`a`と`b` NULL 可能であるため、サブクエリ`NOT IN`によって変換された左外部セミ結合は NULL 対応となります。違いは、NAAJ 最適化ではハッシュ結合の条件として NA-EQ も使用されるため、結合計算が大幅に高速化される点です。

2番目のクエリ文`EXPLAIN SELECT * FROM t WHERE (a, b) NOT IN (SELECT * FROM s);`では、表`t`と表`s`の列`a`と列`b`がNULL値可能であるため、 `NOT IN`のサブクエリによって変換されたアンチセミ結合はNULL値に対応します。違いは、NAAJ最適化ではハッシュ結合条件としてNA-EQも使用されるため、結合計算が大幅に高速化されることです。

現在、TiDBはアンチセミ結合とアンチ左外部セミ結合のNULL値のみに対応しています。ハッシュ結合タイプのみがサポートされており、その構築テーブルは右側のテーブルに固定する必要があります。

> **注記：**
>
> `Not Exists`演算子もアンチセミ結合に変換されますが、null を認識しません。

## 他の種類のサブクエリを使用してステートメントを説明する {#explain-statements-using-other-types-of-subqueries}

-   [MPPモードでステートメントを説明する](/explain-mpp.md)
-   [インデックスを使用するステートメントを説明する](/explain-indexes.md)
-   [テーブル結合を使用する文を説明する](/explain-joins.md)
-   [集計を使用するステートメントを説明する](/explain-aggregation.md)
-   [ビューを使用してステートメントを説明する](/explain-views.md)
-   [パーティションを使用したステートメントの説明](/explain-partitions.md)
-   [インデックスマージを使用したステートメントの説明](/explain-index-merge.md)
