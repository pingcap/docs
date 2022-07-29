---
title: Decorrelation of Correlated Subquery
summary: Understand how to decorrelate correlated subqueries.
---

# 相関サブクエリの無相関化 {#decorrelation-of-correlated-subquery}

[サブクエリ関連の最適化](/subquery-optimization.md)は、相関する列がない場合にTiDBがサブクエリを処理する方法を示します。相関サブクエリの無相関化は複雑であるため、この記事では、いくつかの簡単なシナリオと、最適化ルールが適用される範囲を紹介します。

## 序章 {#introduction}

例として`select * from t1 where t1.a < (select sum(t2.a) from t2 where t2.b = t1.b)`を取り上げます。ここでのサブクエリ`t1.a < (select sum(t2.a) from t2 where t2.b = t1.b)`は、クエリ条件`t2.b=t1.b`の相関列を参照します。この条件はたまたま同等の条件であるため、クエリを`select t1.* from t1, (select b, sum(a) sum_a from t2 group by b) t2 where t1.b = t2.b and t1.a < t2.sum_a;`として書き換えることができます。このようにして、相関サブクエリは`JOIN`に書き換えられます。

TiDBがこの書き換えを行う必要がある理由は、サブクエリが実行されるたびに、相関サブクエリがその外部クエリ結果にバインドされるためです。上記の例では、 `t1.a`に1,000万の値がある場合、条件`t2.b=t1.b`は`t1.a`の値によって変化するため、このサブクエリは1,000万回繰り返されます。相関関係が何らかの理由で解除されると、このサブクエリは1回だけ実行されます。

## 制限 {#restrictions}

この書き換えの欠点は、相関が解除されていない場合、オプティマイザが相関列のインデックスを使用できることです。つまり、このサブクエリは何度も繰り返される可能性がありますが、インデックスを使用して毎回データをフィルタリングできます。書き換えルールを使用すると、通常、相関列の位置が変わります。サブクエリは1回だけ実行されますが、1回の実行時間は、無相関化がない場合よりも長くなります。

したがって、外部値が少ない場合は、実行パフォーマンスが向上する可能性があるため、無相関化を実行しないでください。現在、この最適化は[最適化ルールと式のプッシュダウンのブロックリスト](/blocklist-control-plan.md)に`subquery decorrelation`の最適化ルールを設定することで無効にできます。

## 例 {#example}

{{< copyable "" >}}

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

上記は、最適化が有効になる例です。 `HashJoin_11`は通常の`inner join`です。

次に、サブクエリの非相関ルールをオフにします。

{{< copyable "" >}}

```sql
insert into mysql.opt_rule_blacklist values("decorrelate");
admin reload opt_rule_blacklist;
explain select * from t1 where t1.a < (select sum(t2.a) from t2 where t2.b = t1.b);
```

```sql
+----------------------------------------+----------+-----------+------------------------+------------------------------------------------------------------------------+
| id                                     | estRows  | task      | access object          | operator info                                                                |
+----------------------------------------+----------+-----------+------------------------+------------------------------------------------------------------------------+
| Projection_10                          | 10000.00 | root      |                        | test.t1.a, test.t1.b                                                         |
| └─Apply_12                             | 10000.00 | root      |                        | CARTESIAN inner join, other cond:lt(cast(test.t1.a), Column#7)               |
|   ├─TableReader_14(Build)              | 10000.00 | root      |                        | data:TableFullScan_13                                                        |
|   │ └─TableFullScan_13                 | 10000.00 | cop[tikv] | table:t1               | keep order:false, stats:pseudo                                               |
|   └─MaxOneRow_15(Probe)                | 1.00     | root      |                        |                                                                              |
|     └─HashAgg_27                       | 1.00     | root      |                        | funcs:sum(Column#10)->Column#7                                               |
|       └─IndexLookUp_28                 | 1.00     | root      |                        |                                                                              |
|         ├─IndexRangeScan_25(Build)     | 10.00    | cop[tikv] | table:t2, index:idx(b) | range: decided by [eq(test.t2.b, test.t1.b)], keep order:false, stats:pseudo |
|         └─HashAgg_17(Probe)            | 1.00     | cop[tikv] |                        | funcs:sum(test.t2.a)->Column#10                                              |
|           └─TableRowIDScan_26          | 10.00    | cop[tikv] | table:t2               | keep order:false, stats:pseudo                                               |
+----------------------------------------+----------+-----------+------------------------+------------------------------------------------------------------------------+
```

サブクエリの非相関ルールを無効にすると、 `IndexRangeScan_25(Build)` `operator info` `range: decided by [eq(test.t2.b, test.t1.b)]`表示されます。これは、相関サブクエリの非相関化が実行されず、TiDBがインデックス範囲クエリを使用することを意味します。
