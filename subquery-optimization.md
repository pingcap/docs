---
title: Subquery Related Optimizations
summary: Understand optimizations related to subqueries.
---

# サブクエリ関連の最適化 {#subquery-related-optimizations}

この記事では、主にサブクエリ関連の最適化を紹介します。

サブクエリは通常、次の状況で表示されます。

-   `NOT IN (SELECT ... FROM ...)`
-   `NOT EXISTS (SELECT ... FROM ...)`
-   `IN (SELECT ... FROM ..)`
-   `EXISTS (SELECT ... FROM ...)`
-   `... >/>=/</<=/=/!= (SELECT ... FROM ...)`

サブクエリに`select * from t where t.a in (select * from t2 where t.b=t2.b)`などの非サブクエリ列が含まれる場合があります。サブクエリの`t.b`列はサブクエリに属しておらず、サブクエリの外部から導入されています。この種のサブクエリは通常「相関サブクエリ」と呼ばれ、外部から導入された列は「相関列」と呼ばれます。相関サブクエリの最適化については、 [相関サブクエリの無相関化](/correlated-subquery-optimization.md)を参照してください。この記事では、相関列を含まないサブクエリに焦点を当てています。

デフォルトでは、サブクエリは[TiDB実行プランを理解する](/explain-overview.md)で説明した`semi join`を実行方法として使用します。一部の特別なサブクエリでは、TiDBはパフォーマンスを向上させるために論理的な書き換えを行います。

## <code>... &lt; ALL (SELECT ... FROM ...)</code>または<code>... &gt; ANY (SELECT ... FROM ...)</code> {#code-x3c-all-select-from-code-or-code-any-select-from-code}

この場合、 `ALL`と`ANY`は`MAX`と`MIN`に置き換えることができます。テーブルが空の場合、 `MAX(EXPR)`と`MIN(EXPR)`の結果はNULLになります。 `EXPR`の結果に`NULL`が含まれている場合も、同じように機能します。 `EXPR`の結果に`NULL`が含まれるかどうかは、式の最終結果に影響を与える可能性があるため、完全な書き換えは次の形式で行われます。

-   `t.id < all (select s.id from s)`は`t.id < min(s.id) and if(sum(s.id is null) != 0, null, true)`に書き換えられます
-   `t.id < any (select s.id from s)`は`t.id < max(s.id) or if(sum(s.id is null) != 0, null, false)`に書き換えられます

## <code>... != ANY (SELECT ... FROM ...)</code> {#code-any-select-from-code}

この場合、サブクエリのすべての値が異なる場合は、クエリをそれらと比較するだけで十分です。サブクエリの異なる値の数が複数ある場合は、不等式が存在する必要があります。したがって、このようなサブクエリは次のように書き直すことができます。

-   `select * from t where t.id != any (select s.id from s)`は`select t.* from t, (select s.id, count(distinct s.id) as cnt_distinct from s) where (t.id != s.id or cnt_distinct > 1)`に書き換えられます

## <code>... = ALL (SELECT ... FROM ...)</code> {#code-all-select-from-code}

この場合、サブクエリの異なる値の数が複数の場合、この式の結果はfalseである必要があります。したがって、このようなサブクエリはTiDBで次の形式に書き換えられます。

-   `select * from t where t.id = all (select s.id from s)`は`select t.* from t, (select s.id, count(distinct s.id) as cnt_distinct from s ) where (t.id = s.id and cnt_distinct <= 1)`に書き換えられます

## <code>... IN (SELECT ... FROM ...)</code> {#code-in-select-from-code}

この場合、 `IN`のサブクエリは`SELECT ... FROM ... GROUP ...`に書き直されてから、通常の形式の`JOIN`に書き直されます。

たとえば、 `select * from t1 where t1.a in (select t2.a from t2)`は`select t1.* from t1, (select distinct(a) a from t2) t2 where t1.a = t2. The form of a`に書き換えられます。 `t2.a`に`UNIQUE`属性がある場合、ここでの`DISTINCT`属性は自動的に削除できます。

{{< copyable "" >}}

```sql
explain select * from t1 where t1.a in (select t2.a from t2);
```

```sql
+------------------------------+---------+-----------+------------------------+----------------------------------------------------------------------------+
| id                           | estRows | task      | access object          | operator info                                                              |
+------------------------------+---------+-----------+------------------------+----------------------------------------------------------------------------+
| IndexJoin_12                 | 9990.00 | root      |                        | inner join, inner:TableReader_11, outer key:test.t2.a, inner key:test.t1.a |
| ├─HashAgg_21(Build)          | 7992.00 | root      |                        | group by:test.t2.a, funcs:firstrow(test.t2.a)->test.t2.a                   |
| │ └─IndexReader_28           | 9990.00 | root      |                        | index:IndexFullScan_27                                                     |
| │   └─IndexFullScan_27       | 9990.00 | cop[tikv] | table:t2, index:idx(a) | keep order:false, stats:pseudo                                             |
| └─TableReader_11(Probe)      | 1.00    | root      |                        | data:TableRangeScan_10                                                     |
|   └─TableRangeScan_10        | 1.00    | cop[tikv] | table:t1               | range: decided by [test.t2.a], keep order:false, stats:pseudo              |
+------------------------------+---------+-----------+------------------------+----------------------------------------------------------------------------+
```

この書き換えは、 `IN`のサブクエリが比較的小さく、外部クエリが比較的大きい場合にパフォーマンスが向上します。これは、書き換えがないと、駆動テーブルとしてt2を使用して`index join`を使用することができないためです。ただし、デメリットは、リライト中に集計を自動的に削除できず、 `t2`テーブルが比較的大きい場合、このリライトがクエリのパフォーマンスに影響を与えることです。現在、変数[tidb_opt_insubq_to_join_and_agg](/system-variables.md#tidb_opt_insubq_to_join_and_agg)はこの最適化を制御するために使用されています。この最適化が適切でない場合は、手動で無効にすることができます。

## <code>EXISTS</code>サブクエリおよび<code>... &gt;/&gt;=/&lt;/&lt;=/=/!= (SELECT ... FROM ...)</code> {#code-exists-code-subquery-and-code-x3c-x3c-select-from-code}

現在、このようなシナリオのサブクエリでは、サブクエリが相関サブクエリでない場合、TiDBは最適化段階で事前に評価し、結果セットに直接置き換えます。次の図に示すように、 `EXISTS`のサブクエリは事前に最適化段階で`TRUE`と評価されるため、最終的な実行結果には表示されません。

{{< copyable "" >}}

```sql
create table t1(a int);
create table t2(a int);
insert into t2 values(1);
explain select * from t where exists (select * from t2);
```

```sql
+------------------------+----------+-----------+---------------+--------------------------------+
| id                     | estRows  | task      | access object | operator info                  |
+------------------------+----------+-----------+---------------+--------------------------------+
| TableReader_12         | 10000.00 | root      |               | data:TableFullScan_11          |
| └─TableFullScan_11     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo |
+------------------------+----------+-----------+---------------+--------------------------------+
```
