---
title: Distinct Optimization
summary: TiDB クエリ オプティマイザーに distinct` 最適化を導入します。
---

# クエリの最適化 {#distinct-optimization}

このドキュメントでは、集計関数の`SELECT DISTINCT`と`DISTINCT`を含む、TiDB クエリ オプティマイザーの`distinct`最適化について説明します。

## <code>SELECT</code>ステートメントの<code>DISTINCT</code>修飾子 {#code-distinct-code-modifier-in-code-select-code-statements}

`DISTINCT`修飾子は、結果セットから重複行を削除することを指定します。 `SELECT DISTINCT`は`GROUP BY`に変換されます。例:

```sql
mysql> explain SELECT DISTINCT a from t;
+--------------------------+---------+-----------+---------------+-------------------------------------------------------+
| id                       | estRows | task      | access object | operator info                                         |
+--------------------------+---------+-----------+---------------+-------------------------------------------------------+
| HashAgg_6                | 2.40    | root      |               | group by:test.t.a, funcs:firstrow(test.t.a)->test.t.a |
| └─TableReader_11         | 3.00    | root      |               | data:TableFullScan_10                                 |
|   └─TableFullScan_10     | 3.00    | cop[tikv] | table:t       | keep order:false, stats:pseudo                        |
+--------------------------+---------+-----------+---------------+-------------------------------------------------------+
3 rows in set (0.00 sec)
```

## 集計関数の<code>DISTINCT</code>オプション {#code-distinct-code-option-in-aggregate-functions}

通常、オプション`DISTINCT`を指定した集計関数は、シングルスレッド実行モデルの TiDBレイヤーで実行されます。

<CustomContent platform="tidb">

TiDB の[`tidb_opt_distinct_agg_push_down`](/system-variables.md#tidb_opt_distinct_agg_push_down)のシステム変数または[`distinct-agg-push-down`](/tidb-configuration-file.md#distinct-agg-push-down)構成項目は、個別の集計クエリを書き換えて TiKV またはTiFlashコプロセッサーにプッシュするかどうかを制御します。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB の[`tidb_opt_distinct_agg_push_down`](/system-variables.md#tidb_opt_distinct_agg_push_down)システム変数は、個別の集計クエリを書き換えて TiKV またはTiFlashコプロセッサーにプッシュするかどうかを制御します。

</CustomContent>

この最適化の例として、次のクエリを見てみましょう。 `tidb_opt_distinct_agg_push_down`はデフォルトで無効になっており、集計関数は TiDBレイヤーで実行されます。値を`1`に設定してこの最適化を有効にすると、 `count(distinct a)`の`distinct a`部分が TiKV またはTiFlashコプロセッサーにプッシュされます。TiKVコプロセッサーの列 a の重複値を削除する HashAgg_5 があります。これにより、 TiDBレイヤーの`HashAgg_8`の計算オーバーヘッドが削減される可能性があります。

```sql
mysql> desc select count(distinct a) from test.t;
+-------------------------+----------+-----------+---------------+------------------------------------------+
| id                      | estRows  | task      | access object | operator info                            |
+-------------------------+----------+-----------+---------------+------------------------------------------+
| StreamAgg_6             | 1.00     | root      |               | funcs:count(distinct test.t.a)->Column#4 |
| └─TableReader_10        | 10000.00 | root      |               | data:TableFullScan_9                     |
|   └─TableFullScan_9     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo           |
+-------------------------+----------+-----------+---------------+------------------------------------------+
3 rows in set (0.01 sec)

mysql> set session tidb_opt_distinct_agg_push_down = 1;
Query OK, 0 rows affected (0.00 sec)

mysql> desc select count(distinct a) from test.t;
+---------------------------+----------+-----------+---------------+------------------------------------------+
| id                        | estRows  | task      | access object | operator info                            |
+---------------------------+----------+-----------+---------------+------------------------------------------+
| HashAgg_8                 | 1.00     | root      |               | funcs:count(distinct test.t.a)->Column#3 |
| └─TableReader_9           | 1.00     | root      |               | data:HashAgg_5                           |
|   └─HashAgg_5             | 1.00     | cop[tikv] |               | group by:test.t.a,                       |
|     └─TableFullScan_7     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo           |
+---------------------------+----------+-----------+---------------+------------------------------------------+
4 rows in set (0.00 sec)
```
