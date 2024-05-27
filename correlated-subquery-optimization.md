---
title: Decorrelation of Correlated Subquery
summary: 相関サブクエリの相関を解除する方法を理解します。
---

# 相関サブクエリの非相関 {#decorrelation-of-correlated-subquery}

[サブクエリ関連の最適化](/subquery-optimization.md)では、相関列がない場合に TiDB がサブクエリを処理する方法について説明します。相関サブクエリの非相関化は複雑なため、この記事ではいくつかの簡単なシナリオと最適化ルールが適用される範囲を紹介します。

## 導入 {#introduction}

`select * from t1 where t1.a < (select sum(t2.a) from t2 where t2.b = t1.b)`例に挙げます。ここでのサブクエリ`t1.a < (select sum(t2.a) from t2 where t2.b = t1.b)` 、クエリ条件`t2.b=t1.b`の相関列を参照します。この条件は同等の条件であるため、クエリは`select t1.* from t1, (select b, sum(a) sum_a from t2 group by b) t2 where t1.b = t2.b and t1.a < t2.sum_a;`のように書き換えることができます。このようにして、相関サブクエリは`JOIN`に書き換えられます。

TiDB がこの書き換えを行う必要がある理由は、相関サブクエリがサブクエリが実行されるたびに外部クエリの結果にバインドされるためです。上記の例では、 `t1.a`に 1,000 万個の値がある場合、条件`t2.b=t1.b` `t1.a`の値によって変化するため、このサブクエリは 1,000 万回繰り返されます。何らかの理由で相関が解除されると、このサブクエリは 1 回だけ実行されます。

## 制限 {#restrictions}

この書き換えの欠点は、相関が解除されていない場合、オプティマイザが相関列のインデックスを使用できることです。つまり、このサブクエリは何度も繰り返される場合がありますが、そのたびにインデックスを使用してデータをフィルターできます。書き換えルールを使用した後、相関列の位置は通常変更されます。サブクエリは 1 回だけ実行されますが、1 回の実行時間は相関解除がない場合よりも長くなります。

したがって、外部値が少ない場合は、非相関化を実行しないでください。これにより、実行パフォーマンスが向上する可能性があります。この場合、 [`NO_DECORRELATE`](/optimizer-hints.md#no_decorrelate)オプティマイザ ヒントを使用するか、 [最適化ルールと式プッシュダウンのブロックリスト](/blocklist-control-plan.md)の「サブクエリの非相関化」最適化ルールを無効にすることで、この最適化を無効にすることができます。ほとんどの場合、非相関化を無効にするには、 [SQL プラン管理](/sql-plan-management.md)とともにオプティマイザ ヒントを使用することをお勧めします。

## 例 {#example}

```sql
create table t1(a int, b int);
create table t2(a int, b int, index idx(b));
explain select * from t1 where t1.a < (select sum(t2.a) from t2 where t2.b = t1.b);
```

```sql
+----------------------------------+----------+-----------+---------------+-----------------------------------------------------------------------------------------+
| id                               | estRows  | task      | access object | operator info                                                                           |
+----------------------------------+----------+-----------+---------------+-----------------------------------------------------------------------------------------+
| HashJoin_11                      | 9990.00  | root      |               | inner join, equal:[eq(test.t1.b, test.t2.b)], other cond:lt(cast(test.t1.a), Column#7)  |
| ├─HashAgg_23(Build)              | 7992.00  | root      |               | group by:test.t2.b, funcs:sum(Column#8)->Column#7, funcs:firstrow(test.t2.b)->test.t2.b |
| │ └─TableReader_24               | 7992.00  | root      |               | data:HashAgg_16                                                                         |
| │   └─HashAgg_16                 | 7992.00  | cop[tikv] |               | group by:test.t2.b, funcs:sum(test.t2.a)->Column#8                                      |
| │     └─Selection_22             | 9990.00  | cop[tikv] |               | not(isnull(test.t2.b))                                                                  |
| │       └─TableFullScan_21       | 10000.00 | cop[tikv] | table:t2      | keep order:false, stats:pseudo                                                          |
| └─TableReader_15(Probe)          | 9990.00  | root      |               | data:Selection_14                                                                       |
|   └─Selection_14                 | 9990.00  | cop[tikv] |               | not(isnull(test.t1.b))                                                                  |
|     └─TableFullScan_13           | 10000.00 | cop[tikv] | table:t1      | keep order:false, stats:pseudo                                                          |
+----------------------------------+----------+-----------+---------------+-----------------------------------------------------------------------------------------+

```

上記は最適化が効いている例です。 `HashJoin_11`は通常の`inner join`です。

次に、 `NO_DECORRELATE`オプティマイザ ヒントを使用して、サブクエリの相関解除を実行しないようにオプティマイザに指示できます。

```sql
explain select * from t1 where t1.a < (select /*+ NO_DECORRELATE() */ sum(t2.a) from t2 where t2.b = t1.b);
```

```sql
+------------------------------------------+-----------+-----------+------------------------+--------------------------------------------------------------------------------------+
| id                                       | estRows   | task      | access object          | operator info                                                                        |
+------------------------------------------+-----------+-----------+------------------------+--------------------------------------------------------------------------------------+
| Projection_10                            | 10000.00  | root      |                        | test.t1.a, test.t1.b                                                                 |
| └─Apply_12                               | 10000.00  | root      |                        | CARTESIAN inner join, other cond:lt(cast(test.t1.a, decimal(10,0) BINARY), Column#7) |
|   ├─TableReader_14(Build)                | 10000.00  | root      |                        | data:TableFullScan_13                                                                |
|   │ └─TableFullScan_13                   | 10000.00  | cop[tikv] | table:t1               | keep order:false, stats:pseudo                                                       |
|   └─MaxOneRow_15(Probe)                  | 10000.00  | root      |                        |                                                                                      |
|     └─StreamAgg_20                       | 10000.00  | root      |                        | funcs:sum(Column#14)->Column#7                                                       |
|       └─Projection_45                    | 100000.00 | root      |                        | cast(test.t2.a, decimal(10,0) BINARY)->Column#14                                     |
|         └─IndexLookUp_44                 | 100000.00 | root      |                        |                                                                                      |
|           ├─IndexRangeScan_42(Build)     | 100000.00 | cop[tikv] | table:t2, index:idx(b) | range: decided by [eq(test.t2.b, test.t1.b)], keep order:false, stats:pseudo         |
|           └─TableRowIDScan_43(Probe)     | 100000.00 | cop[tikv] | table:t2               | keep order:false, stats:pseudo                                                       |
+------------------------------------------+-----------+-----------+------------------------+--------------------------------------------------------------------------------------+
```

非相関ルールを無効にすることでも同じ効果が得られます。

```sql
insert into mysql.opt_rule_blacklist values("decorrelate");
admin reload opt_rule_blacklist;
explain select * from t1 where t1.a < (select sum(t2.a) from t2 where t2.b = t1.b);
```

```sql
+------------------------------------------+-----------+-----------+------------------------+--------------------------------------------------------------------------------------+
| id                                       | estRows   | task      | access object          | operator info                                                                        |
+------------------------------------------+-----------+-----------+------------------------+--------------------------------------------------------------------------------------+
| Projection_10                            | 10000.00  | root      |                        | test.t1.a, test.t1.b                                                                 |
| └─Apply_12                               | 10000.00  | root      |                        | CARTESIAN inner join, other cond:lt(cast(test.t1.a, decimal(10,0) BINARY), Column#7) |
|   ├─TableReader_14(Build)                | 10000.00  | root      |                        | data:TableFullScan_13                                                                |
|   │ └─TableFullScan_13                   | 10000.00  | cop[tikv] | table:t1               | keep order:false, stats:pseudo                                                       |
|   └─MaxOneRow_15(Probe)                  | 10000.00  | root      |                        |                                                                                      |
|     └─StreamAgg_20                       | 10000.00  | root      |                        | funcs:sum(Column#14)->Column#7                                                       |
|       └─Projection_45                    | 100000.00 | root      |                        | cast(test.t2.a, decimal(10,0) BINARY)->Column#14                                     |
|         └─IndexLookUp_44                 | 100000.00 | root      |                        |                                                                                      |
|           ├─IndexRangeScan_42(Build)     | 100000.00 | cop[tikv] | table:t2, index:idx(b) | range: decided by [eq(test.t2.b, test.t1.b)], keep order:false, stats:pseudo         |
|           └─TableRowIDScan_43(Probe)     | 100000.00 | cop[tikv] | table:t2               | keep order:false, stats:pseudo                                                       |
+------------------------------------------+-----------+-----------+------------------------+--------------------------------------------------------------------------------------+
```

サブクエリの非相関ルールを無効にすると、 `range: decided by [eq(test.t2.b, test.t1.b)]` in `operator info` of `IndexRangeScan_42(Build)`が表示されます。これは、相関サブクエリの非相関が実行されず、TiDB がインデックス範囲クエリを使用することを意味します。
