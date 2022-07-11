---
title: Explain Statements in the MPP Mode
summary: Learn about the execution plan information returned by the EXPLAIN statement in TiDB.
---

# MPPモードでのステートメントの説明 {#explain-statements-in-the-mpp-mode}

TiDBは、 [MPPモード](/tiflash/use-tiflash-mpp-mode.md)を使用したクエリの実行をサポートしています。 MPPモードでは、TiDBオプティマイザがMPPの実行プランを生成します。 MPPモードは、 [TiFlash](/tiflash/tiflash-overview.md)にレプリカがあるテーブルでのみ使用できることに注意してください。

このドキュメントの例は、次のサンプルデータに基づいています。

{{< copyable "" >}}

```sql
CREATE TABLE t1 (id int, value int);
INSERT INTO t1 values(1,2),(2,3),(1,3);
ALTER TABLE t1 set tiflash replica 1;
ANALYZE TABLE t1;
SET tidb_allow_mpp = 1;
```

## MPPクエリフラグメントとMPPタスク {#mpp-query-fragments-and-mpp-tasks}

MPPモードでは、クエリは論理的に複数のクエリフラグメントにスライスされます。例として、次のステートメントを取り上げます。

{{< copyable "" >}}

```sql
EXPLAIN SELECT COUNT(*) FROM t1 GROUP BY id;
```

このクエリは、MPPモードで2つのフラグメントに分割されます。 1つは第1段階の集約用で、もう1つは第2段階の集約用であり、これも最終的な集約です。このクエリが実行されると、各クエリフラグメントが1つ以上のMPPタスクにインスタンス化されます。

## 交換事業者 {#exchange-operators}

`ExchangeReceiver`と`ExchangeSender`は、MPP実行プランに固有の2つの交換演算子です。 `ExchangeReceiver`オペレーターは、ダウンストリームクエリフラグメントからデータを読み取り、 `ExchangeSender`オペレーターは、ダウンストリームクエリフラグメントからアップストリームクエリフラグメントにデータを送信します。 MPPモードでは、各MPPクエリフラグメントのルート演算子は`ExchangeSender`です。これは、クエリフラグメントが`ExchangeSender`演算子で区切られていることを意味します。

以下は、単純なMPP実行プランです。

{{< copyable "" >}}

```sql
EXPLAIN SELECT COUNT(*) FROM t1 GROUP BY id;
```

```sql
+------------------------------------+---------+-------------------+---------------+----------------------------------------------------+
| id                                 | estRows | task              | access object | operator info                                      |
+------------------------------------+---------+-------------------+---------------+----------------------------------------------------+
| TableReader_31                     | 2.00    | root              |               | data:ExchangeSender_30                             |
| └─ExchangeSender_30                | 2.00    | batchCop[tiflash] |               | ExchangeType: PassThrough                          |
|   └─Projection_26                  | 2.00    | batchCop[tiflash] |               | Column#4                                           |
|     └─HashAgg_27                   | 2.00    | batchCop[tiflash] |               | group by:test.t1.id, funcs:sum(Column#7)->Column#4 |
|       └─ExchangeReceiver_29        | 2.00    | batchCop[tiflash] |               |                                                    |
|         └─ExchangeSender_28        | 2.00    | batchCop[tiflash] |               | ExchangeType: HashPartition, Hash Cols: test.t1.id |
|           └─HashAgg_9              | 2.00    | batchCop[tiflash] |               | group by:test.t1.id, funcs:count(1)->Column#7      |
|             └─TableFullScan_25     | 3.00    | batchCop[tiflash] | table:t1      | keep order:false                                   |
+------------------------------------+---------+-------------------+---------------+----------------------------------------------------+
```

上記の実行プランには、2つのクエリフラグメントが含まれています。

-   1つ目は`[TableFullScan_25, HashAgg_9, ExchangeSender_28]`で、これは主に第1段階の集約を担当します。
-   2番目は`[ExchangeReceiver_29, HashAgg_27, Projection_26, ExchangeSender_30]`で、これは主に第2段階の集約を担当します。

`ExchangeSender`演算子の`operator info`列には、交換タイプ情報が表示されます。現在、交換には3つのタイプがあります。以下を参照してください。

-   HashPartition： `ExchangeSender`オペレーターは、最初にハッシュ値に従ってデータを分割し、次にアップストリームMPPタスクの`ExchangeReceiver`オペレーターにデータを配布します。この交換タイプは、ハッシュ集計およびシャッフルハッシュ結合アルゴリズムでよく使用されます。
-   ブロードキャスト： `ExchangeSender`オペレーターは、ブロードキャストを介してデータをアップストリームMPPタスクに配信します。この交換タイプは、ブロードキャスト参加によく使用されます。
-   PassThrough： `ExchangeSender`オペレーターは、ブロードキャストタイプとは異なる唯一のアップストリームMPPタスクにデータを送信します。この交換タイプは、データをTiDBに返すときによく使用されます。

実行プランの例では、演算子`ExchangeSender_28`の交換タイプはHashPartitionです。これは、 集計アルゴリズムを実行することを意味します。演算子`ExchangeSender_30`の交換タイプはPassThroughです。これは、データをTiDBに返すために使用されることを意味します。

MPPは、結合操作にもよく適用されます。 TiDBのMPPモードは、次の2つの結合アルゴリズムをサポートしています。

-   ハッシュ結合のシャッフル：HashPartition交換タイプを使用して、結合操作から入力されたデータをシャッフルします。次に、アップストリームMPPタスクが同じパーティション内のデータを結合します。
-   ブロードキャスト結合：結合操作中の小さなテーブルのデータを各ノードにブロードキャストします。その後、各ノードはデータを個別に結合します。

以下は、シャッフルハッシュ結合の一般的な実行プランです。

{{< copyable "" >}}

```sql
SET tidb_broadcast_join_threshold_count=0;
SET tidb_broadcast_join_threshold_size=0;
EXPLAIN SELECT COUNT(*) FROM t1 a JOIN t1 b ON a.id = b.id;
```

```sql
+----------------------------------------+---------+--------------+---------------+----------------------------------------------------+
| id                                     | estRows | task         | access object | operator info                                      |
+----------------------------------------+---------+--------------+---------------+----------------------------------------------------+
| StreamAgg_14                           | 1.00    | root         |               | funcs:count(1)->Column#7                           |
| └─TableReader_48                       | 9.00    | root         |               | data:ExchangeSender_47                             |
|   └─ExchangeSender_47                  | 9.00    | cop[tiflash] |               | ExchangeType: PassThrough                          |
|     └─HashJoin_44                      | 9.00    | cop[tiflash] |               | inner join, equal:[eq(test.t1.id, test.t1.id)]     |
|       ├─ExchangeReceiver_19(Build)     | 6.00    | cop[tiflash] |               |                                                    |
|       │ └─ExchangeSender_18            | 6.00    | cop[tiflash] |               | ExchangeType: HashPartition, Hash Cols: test.t1.id |
|       │   └─Selection_17               | 6.00    | cop[tiflash] |               | not(isnull(test.t1.id))                            |
|       │     └─TableFullScan_16         | 6.00    | cop[tiflash] | table:a       | keep order:false                                   |
|       └─ExchangeReceiver_23(Probe)     | 6.00    | cop[tiflash] |               |                                                    |
|         └─ExchangeSender_22            | 6.00    | cop[tiflash] |               | ExchangeType: HashPartition, Hash Cols: test.t1.id |
|           └─Selection_21               | 6.00    | cop[tiflash] |               | not(isnull(test.t1.id))                            |
|             └─TableFullScan_20         | 6.00    | cop[tiflash] | table:b       | keep order:false                                   |
+----------------------------------------+---------+--------------+---------------+----------------------------------------------------+
12 rows in set (0.00 sec)
```

上記の実行計画では：

-   クエリフラグメント`[TableFullScan_20, Selection_21, ExchangeSender_22]`は、テーブルbからデータを読み取り、データをアップストリームMPPタスクにシャッフルします。
-   クエリフラグメント`[TableFullScan_16, Selection_17, ExchangeSender_18]`は、テーブルaからデータを読み取り、データをアップストリームMPPタスクにシャッフルします。
-   クエリフラグメント`[ExchangeReceiver_19, ExchangeReceiver_23, HashJoin_44, ExchangeSender_47]`はすべてのデータを結合し、それをTiDBに返します。

BroadcastJoinの一般的な実行プランは次のとおりです。

{{< copyable "" >}}

```sql
EXPLAIN SELECT COUNT(*) FROM t1 a JOIN t1 b ON a.id = b.id;
```

```sql
+----------------------------------------+---------+--------------+---------------+------------------------------------------------+
| id                                     | estRows | task         | access object | operator info                                  |
+----------------------------------------+---------+--------------+---------------+------------------------------------------------+
| StreamAgg_15                           | 1.00    | root         |               | funcs:count(1)->Column#7                       |
| └─TableReader_47                       | 9.00    | root         |               | data:ExchangeSender_46                         |
|   └─ExchangeSender_46                  | 9.00    | cop[tiflash] |               | ExchangeType: PassThrough                      |
|     └─HashJoin_43                      | 9.00    | cop[tiflash] |               | inner join, equal:[eq(test.t1.id, test.t1.id)] |
|       ├─ExchangeReceiver_20(Build)     | 6.00    | cop[tiflash] |               |                                                |
|       │ └─ExchangeSender_19            | 6.00    | cop[tiflash] |               | ExchangeType: Broadcast                        |
|       │   └─Selection_18               | 6.00    | cop[tiflash] |               | not(isnull(test.t1.id))                        |
|       │     └─TableFullScan_17         | 6.00    | cop[tiflash] | table:a       | keep order:false                               |
|       └─Selection_22(Probe)            | 6.00    | cop[tiflash] |               | not(isnull(test.t1.id))                        |
|         └─TableFullScan_21             | 6.00    | cop[tiflash] | table:b       | keep order:false                               |
+----------------------------------------+---------+--------------+---------------+------------------------------------------------+
```

上記の実行計画では：

-   クエリフラグメント`[TableFullScan_17, Selection_18, ExchangeSender_19]`は、小さなテーブル（テーブルa）からデータを読み取り、大きなテーブル（テーブルb）からのデータを含む各ノードにデータをブロードキャストします。
-   クエリフラグメント`[TableFullScan_21, Selection_22, ExchangeReceiver_20, HashJoin_43, ExchangeSender_46]`はすべてのデータを結合し、それをTiDBに返します。

## MPPモードでの<code>EXPLAIN ANALYZE</code>ステートメント {#code-explain-analyze-code-statements-in-the-mpp-mode}

`EXPLAIN ANALYZE`ステートメントは`EXPLAIN`に似ていますが、実行時情報も出力します。

以下は、単純な`EXPLAIN ANALYZE`の例の出力です。

{{< copyable "" >}}

```sql
EXPLAIN ANALYZE SELECT COUNT(*) FROM t1 GROUP BY id;
```

```sql
+------------------------------------+---------+---------+-------------------+---------------+---------------------------------------------------------------------------------------------+----------------------------------------------------------------+--------+------+
| id                                 | estRows | actRows | task              | access object | execution info                                                                              | operator info                                                  | memory | disk |
+------------------------------------+---------+---------+-------------------+---------------+---------------------------------------------------------------------------------------------+----------------------------------------------------------------+--------+------+
| TableReader_31                     | 4.00    | 2       | root              |               | time:44.5ms, loops:2, cop_task: {num: 1, max: 0s, proc_keys: 0, copr_cache_hit_ratio: 0.00} | data:ExchangeSender_30                                         | N/A    | N/A  |
| └─ExchangeSender_30                | 4.00    | 2       | batchCop[tiflash] |               | tiflash_task:{time:16.5ms, loops:1, threads:1}                                              | ExchangeType: PassThrough, tasks: [2, 3, 4]                    | N/A    | N/A  |
|   └─Projection_26                  | 4.00    | 2       | batchCop[tiflash] |               | tiflash_task:{time:16.5ms, loops:1, threads:1}                                              | Column#4                                                       | N/A    | N/A  |
|     └─HashAgg_27                   | 4.00    | 2       | batchCop[tiflash] |               | tiflash_task:{time:16.5ms, loops:1, threads:1}                                              | group by:test.t1.id, funcs:sum(Column#7)->Column#4             | N/A    | N/A  |
|       └─ExchangeReceiver_29        | 4.00    | 2       | batchCop[tiflash] |               | tiflash_task:{time:14.5ms, loops:1, threads:20}                                             |                                                                | N/A    | N/A  |
|         └─ExchangeSender_28        | 4.00    | 0       | batchCop[tiflash] |               | tiflash_task:{time:9.49ms, loops:0, threads:0}                                              | ExchangeType: HashPartition, Hash Cols: test.t1.id, tasks: [1] | N/A    | N/A  |
|           └─HashAgg_9              | 4.00    | 0       | batchCop[tiflash] |               | tiflash_task:{time:9.49ms, loops:0, threads:0}                                              | group by:test.t1.id, funcs:count(1)->Column#7                  | N/A    | N/A  |
|             └─TableFullScan_25     | 6.00    | 0       | batchCop[tiflash] | table:t1      | tiflash_task:{time:9.49ms, loops:0, threads:0}                                              | keep order:false                                               | N/A    | N/A  |
+------------------------------------+---------+---------+-------------------+---------------+---------------------------------------------------------------------------------------------+----------------------------------------------------------------+--------+------+
```

`EXPLAIN`の出力と比較して、演算子`ExchangeSender`の`operator info`列には`tasks`も表示されます。これは、クエリフラグメントがインスタンス化されるMPPタスクのIDを記録します。さらに、各MPPオペレーターには`execution info`列に`threads`フィールドがあり、TiDBがこのオペレーターを実行するときの操作の同時実行性を記録します。クラスタが複数のノードで構成されている場合、この同時実行性は、すべてのノードの同時実行性を合計した結果です。
