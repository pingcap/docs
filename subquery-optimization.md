---
title: Subquery Related Optimizations
summary: Understand optimizations related to subqueries.
---

# サブクエリ関連の最適化 {#subquery-related-optimizations}

この記事では、主にサブクエリ関連の最適化について紹介します。

サブクエリは通常、次の状況で表示されます。

-   `NOT IN (SELECT ... FROM ...)`
-   `NOT EXISTS (SELECT ... FROM ...)`
-   `IN (SELECT ... FROM ..)`
-   `EXISTS (SELECT ... FROM ...)`
-   `... >/>=/</<=/=/!= (SELECT ... FROM ...)`

サブクエリには、 `select * from t where t.a in (select * from t2 where t.b=t2.b)`などのサブクエリ以外の列が含まれる場合があります。サブクエリの`t.b`列目はサブクエリに属さず、サブクエリの外部から導入されます。このようなサブクエリは通常「相関サブクエリ」と呼ばれ、外部から導入された列は「相関列」と呼ばれます。相関サブクエリに関する最適化については、 [相関サブクエリの非相関](/correlated-subquery-optimization.md)を参照してください。この記事では、相関列を含まないサブクエリに焦点を当てています。

デフォルトでは、サブクエリは[TiDB 実行計画について](/explain-overview.md)の`semi join`実行方法として使用します。一部の特別なサブクエリでは、TiDB はパフォーマンスを向上させるために論理的な書き直しを行います。

## <code>... &lt; ALL (SELECT ... FROM ...)</code>または<code>... &gt; ANY (SELECT ... FROM ...)</code> {#code-x3c-all-select-from-code-or-code-any-select-from-code}

この場合、 `ALL`と`ANY` `MAX`と`MIN`に置き換えることができます。テーブルが空の場合、 `MAX(EXPR)`と`MIN(EXPR)`の結果は NULL です。 `EXPR`の結果に`NULL`含まれる場合も同様です。 `EXPR`の結果に`NULL`が含まれるかどうかは、式の最終結果に影響を与える可能性があるため、完全な書き直しは次の形式で与えられます。

-   `t.id < all (select s.id from s)`は`t.id < min(s.id) and if(sum(s.id is null) != 0, null, true)`に書き換えられます
-   `t.id < any (select s.id from s)`は`t.id < max(s.id) or if(sum(s.id is null) != 0, null, false)`に書き換えられます

## <code>... != ANY (SELECT ... FROM ...)</code> {#code-any-select-from-code}

この場合、サブクエリからのすべての値が異なる場合、クエリをそれらと比較するだけで十分です。サブクエリ内の異なる値の数が複数の場合、不等式が存在する必要があります。したがって、このようなサブクエリは次のように書き直すことができます。

-   `select * from t where t.id != any (select s.id from s)`は`select t.* from t, (select s.id, count(distinct s.id) as cnt_distinct from s) where (t.id != s.id or cnt_distinct > 1)`に書き換えられます

## <code>... = ALL (SELECT ... FROM ...)</code> {#code-all-select-from-code}

この場合、サブクエリ内の異なる値の数が複数ある場合、この式の結果は false になる必要があります。したがって、そのようなサブクエリは、TiDB では次の形式に書き換えられます。

-   `select * from t where t.id = all (select s.id from s)`は`select t.* from t, (select s.id, count(distinct s.id) as cnt_distinct from s ) where (t.id = s.id and cnt_distinct <= 1)`に書き換えられます

## <code>... IN (SELECT ... FROM ...)</code> {#code-in-select-from-code}

この場合、 `IN`のサブクエリは`SELECT ... FROM ... GROUP ...`に書き換えられ、その後通常の形式の`JOIN`に書き換えられます。

たとえば、 `select * from t1 where t1.a in (select t2.a from t2)`は`select t1.* from t1, (select distinct(a) a from t2) t2 where t1.a = t2. The form of a`に書き換えられます。ここの`DISTINCT`属性は、 `t2.a`が`UNIQUE`属性を持つ場合、自動的に削除できます。

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
| └─TableReader_11(Probe)      | 7992.00 | root      |                        | data:TableRangeScan_10                                                     |
|   └─TableRangeScan_10        | 7992.00 | cop[tikv] | table:t1               | range: decided by [test.t2.a], keep order:false, stats:pseudo              |
+------------------------------+---------+-----------+------------------------+----------------------------------------------------------------------------+
```

`IN`サブクエリが比較的小さく、外部クエリが比較的大きい場合、この書き換えによりパフォーマンスが向上します。これは、書き換えなしでは、駆動テーブルとして t2 で`index join`使用することが不可能であるためです。ただし、不利な点は、再書き込み中に集計を自動的に削除できず、 `t2`が比較的大きい場合、この再書き込みがクエリのパフォーマンスに影響を与えることです。現在、この最適化を制御するために変数[tidb_opt_insubq_to_join_and_agg](/system-variables.md#tidb_opt_insubq_to_join_and_agg)が使用されています。この最適化が適切でない場合は、手動で無効にすることができます。

## <code>EXISTS</code>サブクエリと<code>... &gt;/&gt;=/&lt;/&lt;=/=/!= (SELECT ... FROM ...)</code> {#code-exists-code-subquery-and-code-x3c-x3c-select-from-code}

現在、このようなシナリオのサブクエリでは、サブクエリが相関サブクエリでない場合、TiDB は最適化段階で事前に評価し、直接結果セットに置き換えます。下図のように、サブクエリ`EXISTS`は事前に最適化段階で`TRUE`と評価されるため、最終的な実行結果には反映されません。

{{< copyable "" >}}

```sql
create table t1(a int);
create table t2(a int);
insert into t2 values(1);
explain select * from t1 where exists (select * from t2);
```

```sql
+------------------------+----------+-----------+---------------+--------------------------------+
| id                     | estRows  | task      | access object | operator info                  |
+------------------------+----------+-----------+---------------+--------------------------------+
| TableReader_12         | 10000.00 | root      |               | data:TableFullScan_11          |
| └─TableFullScan_11     | 10000.00 | cop[tikv] | table:t1      | keep order:false, stats:pseudo |
+------------------------+----------+-----------+---------------+--------------------------------+
```

前述の最適化では、オプティマイザは文の実行を自動的に最適化します。さらに、ステートメントをさらに書き直すために[`SEMI_JOIN_REWRITE`](/optimizer-hints.md#semi_join_rewrite)ヒントを追加することもできます。

このヒントを使用してクエリを書き直さない場合、実行プランでハッシュ結合が選択されている場合、セミ結合クエリはサブクエリを使用してハッシュ テーブルを構築することしかできません。この場合、サブクエリの結果が外側のクエリの結果よりも大きい場合、実行速度が予想よりも遅くなる可能性があります。

同様に、実行計画でインデックス結合が選択されている場合、セミ結合クエリは外部クエリのみを駆動テーブルとして使用できます。この場合、サブクエリの結果が外側のクエリの結果よりも小さい場合、実行速度が予想よりも遅くなる可能性があります。

`SEMI_JOIN_REWRITE()`を使用してクエリを書き換えると、オプティマイザーは選択範囲を拡張して、より適切な実行プランを選択できます。
