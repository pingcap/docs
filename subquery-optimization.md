---
title: Subquery Related Optimizations
summary: Understand optimizations related to subqueries.
---

# サブクエリ関連の最適化 {#subquery-related-optimizations}

この記事では主にサブクエリ関連の最適化について紹介します。

サブクエリは通常、次の状況で使用されます。

-   `NOT IN (SELECT ... FROM ...)`
-   `NOT EXISTS (SELECT ... FROM ...)`
-   `IN (SELECT ... FROM ..)`
-   `EXISTS (SELECT ... FROM ...)`
-   `... >/>=/</<=/=/!= (SELECT ... FROM ...)`

サブクエリには、 `select * from t where t.a in (select * from t2 where t.b=t2.b)`などの非サブクエリ列が含まれる場合があります。サブクエリの`t.b`列はサブクエリに属さず、サブクエリの外部から導入されます。この種のサブクエリは通常「相関サブクエリ」と呼ばれ、外部から導入された列は「相関列」と呼ばれます。相関サブクエリの最適化については、 [相関サブクエリの相関解除](/correlated-subquery-optimization.md)を参照してください。この記事では、相関列を含まないサブクエリに焦点を当てます。

デフォルトでは、サブクエリは実行方法として[TiDB 実行計画を理解する](/explain-overview.md)で説明した`semi join`を使用します。一部の特殊なサブクエリでは、TiDB はパフォーマンスを向上させるために論理的な書き換えを行います。

## <code>... &lt; ALL (SELECT ... FROM ...)</code>または<code>... &gt; ANY (SELECT ... FROM ...)</code> {#code-x3c-all-select-from-code-or-code-any-select-from-code}

この場合、 `ALL`と`ANY` `MAX`と`MIN`に置き換えることができます。テーブルが空の場合、 `MAX(EXPR)`と`MIN(EXPR)`の結果は NULL になります。 `EXPR`の結果に`NULL`含まれる場合も同様に機能します。 `EXPR`の結果に`NULL`が含まれるかどうかは、式の最終結果に影響を与える可能性があるため、完全な書き換えは次の形式で行われます。

-   `t.id < all (select s.id from s)`は`t.id < min(s.id) and if(sum(s.id is null) != 0, null, true)`に書き換えられます
-   `t.id < any (select s.id from s)`は`t.id < max(s.id) or if(sum(s.id is null) != 0, null, false)`に書き換えられます

## <code>... != ANY (SELECT ... FROM ...)</code> {#code-any-select-from-code}

この場合、サブクエリの値がすべて異なる場合、クエリとそれらの値を比較するだけで十分です。サブクエリ内の異なる値の数が複数ある場合は、不等号が存在する必要があります。したがって、そのようなサブクエリは次のように書き換えることができます。

-   `select * from t where t.id != any (select s.id from s)`は`select t.* from t, (select s.id, count(distinct s.id) as cnt_distinct from s) where (t.id != s.id or cnt_distinct > 1)`に書き換えられます

## <code>... = ALL (SELECT ... FROM ...)</code> {#code-all-select-from-code}

この場合、サブクエリ内の異なる値の数が複数である場合、この式の結果は false でなければなりません。したがって、このようなサブクエリは TiDB で次の形式に書き換えられます。

-   `select * from t where t.id = all (select s.id from s)`は`select t.* from t, (select s.id, count(distinct s.id) as cnt_distinct from s ) where (t.id = s.id and cnt_distinct <= 1)`に書き換えられます

## <code>... IN (SELECT ... FROM ...)</code> {#code-in-select-from-code}

この場合、サブクエリ`IN`は`SELECT ... FROM ... GROUP ...`に書き換えられ、さらに通常の形式の`JOIN`に書き換えられます。

たとえば、 `select * from t1 where t1.a in (select t2.a from t2)`は`select t1.* from t1, (select distinct(a) a from t2) t2 where t1.a = t2. The form of a`に書き換えられます。ここでの`DISTINCT`属性は、 `t2.a`に`UNIQUE`属性があれば自動的に削除できます。

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

この書き換えは、サブクエリ`IN`が比較的小さく、外部クエリが比較的大きい場合にパフォーマンスが向上します。これは、書き換えなしでは、駆動テーブルとして`index join`と t2 を使用することが不可能であるためです。ただし、リライト中に集計を自動的に削除できず、 `t2`が比較的大きい場合、このリライトがクエリのパフォーマンスに影響を与えるという欠点があります。現在、変数[tidb_opt_insubq_to_join_and_agg](/system-variables.md#tidb_opt_insubq_to_join_and_agg)はこの最適化を制御するために使用されます。この最適化が適切でない場合は、手動で無効にすることができます。

## <code>EXISTS</code>サブクエリと<code>... &gt;/&gt;=/&lt;/&lt;=/=/!= (SELECT ... FROM ...)</code> {#code-exists-code-subquery-and-code-x3c-x3c-select-from-code}

現時点では、このようなシナリオのサブクエリの場合、サブクエリが相関サブクエリでない場合、TiDB は最適化段階で事前にサブクエリを評価し、結果セットに直接置き換えます。下図のように、 `EXISTS`サブクエリはあらかじめ最適化段階で`TRUE`と評価されているため、最終的な実行結果には反映されません。

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

前述の最適化では、オプティマイザーはステートメントの実行を自動的に最適化します。さらに、 [`SEMI_JOIN_REWRITE`](/optimizer-hints.md#semi_join_rewrite)ヒントを追加してステートメントをさらに書き直すこともできます。

このヒントを使用してクエリを書き換えない場合、実行プランでハッシュ結合が選択されている場合、セミ結合クエリはサブクエリを使用してハッシュ テーブルを構築することしかできません。この場合、サブクエリの結果が外側のクエリの結果よりも大きい場合、実行速度が予想より遅くなる可能性があります。

同様に、実行プランでインデックス結合が選択されている場合、準結合クエリは駆動テーブルとして外部クエリのみを使用できます。この場合、サブクエリの結果が外側のクエリの結果よりも小さい場合、実行速度が予想より遅くなる可能性があります。

`SEMI_JOIN_REWRITE()`を使用してクエリを書き換えると、オプティマイザは選択範囲を拡張して、より適切な実行プランを選択できます。
