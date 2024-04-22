---
title: Explain Statements in the MPP Mode
summary: TiDBはMPPモードをサポートし、TiFlashにレプリカがあるテーブルでのみ使用できます。クエリは複数のクエリフラグメントにスライスされ、ExchangeReceiverとExchangeSender演算子があります。MPPモードでは、HashPartition、ブロードキャスト、パススルーの3つの交換タイプがあります。また、EXPLAIN ANALYZEステートメントは実行時情報も出力します。新しいフィールドMPPVersionとCompressionがMPP実行プランに追加され、データ圧縮モードを示します。
---

# MPP モードでの Explain ステートメント {#explain-statements-in-the-mpp-mode}

TiDB は、 [MPPモード](/tiflash/use-tiflash-mpp-mode.md)を使用したクエリの実行をサポートしています。 MPP モードでは、TiDB オプティマイザーは MPP の実行プランを生成します。 MPP モードは、 [TiFlash](/tiflash/tiflash-overview.md)にレプリカがあるテーブルでのみ使用できることに注意してください。

このドキュメントの例は、次のサンプル データに基づいています。

```sql
CREATE TABLE t1 (id int, value int);
INSERT INTO t1 values(1,2),(2,3),(1,3);
ALTER TABLE t1 set tiflash replica 1;
ANALYZE TABLE t1;
SET tidb_allow_mpp = 1;
```

## MPP クエリ フラグメントと MPP タスク {#mpp-query-fragments-and-mpp-tasks}

MPP モードでは、クエリは論理的に複数のクエリ フラグメントにスライスされます。次のステートメントを例として取り上げます。

```sql
EXPLAIN SELECT COUNT(*) FROM t1 GROUP BY id;
```

このクエリは、MPP モードでは 2 つのフラグメントに分割されます。 1 つは第 1 段階の集計用で、もう 1 つは第 2 段階の集計用であり、最終的な集計にも使用されます。このクエリが実行されると、各クエリ フラグメントが 1 つ以上の MPP タスクにインスタンス化されます。

## 交換業者 {#exchange-operators}

`ExchangeReceiver`と`ExchangeSender` 、MPP 実行プランに固有の 2 つの交換演算子です。 `ExchangeReceiver`演算子は下流クエリ フラグメントからデータを読み取り、 `ExchangeSender`演算子は下流クエリ フラグメントから上流クエリ フラグメントにデータを送信します。 MPP モードでは、各 MPP クエリ フラグメントのルート演算子は`ExchangeSender`です。これは、クエリ フラグメントが`ExchangeSender`子で区切られることを意味します。

以下は、単純な MPP 実行プランです。

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

上記の実行プランには、次の 2 つのクエリ フラグメントが含まれています。

-   1 つ目は`[TableFullScan_25, HashAgg_9, ExchangeSender_28]`で、主に第 1 段階の集計を担当します。
-   2 番目は`[ExchangeReceiver_29, HashAgg_27, Projection_26, ExchangeSender_30]`で、主に第 2 段階の集計を担当します。

`ExchangeSender`演算子の`operator info`列は交換タイプ情報を示します。現在、交換タイプは 3 つあります。以下を参照してください。

-   HashPartition: `ExchangeSender`オペレーターはまずハッシュ値に従ってデータを分割し、次に上流 MPP タスクの`ExchangeReceiver`オペレーターにデータを分配します。この交換タイプは、ハッシュ集計およびシャッフル ハッシュ結合アルゴリズムによく使用されます。
-   ブロードキャスト: `ExchangeSender`オペレーターは、ブロードキャストを通じて上流の MPP タスクにデータを配布します。この交換タイプはブロードキャスト参加によく使用されます。
-   パススルー: `ExchangeSender`オペレーターは、ブロードキャスト タイプとは異なる唯一の上流 MPP タスクにデータを送信します。この交換タイプは、データを TiDB に返すときによく使用されます。

この実行プランの例では、オペレーター`ExchangeSender_28`の交換タイプは HashPartition であり、ハッシュ集計アルゴリズムを実行することを意味します。オペレーター`ExchangeSender_30`の交換タイプは PassThrough です。これは、データを TiDB に返すために使用されることを意味します。

MPP は結合操作にもよく適用されます。 TiDB の MPP モードは、次の 2 つの結合アルゴリズムをサポートします。

-   Shuffle Hash Join: HashPartition 交換タイプを使用して、結合操作からのデータ入力をシャッフルします。次に、上流の MPP タスクが同じパーティション内のデータを結合します。
-   ブロードキャスト結合: 結合操作で小さなテーブルのデータを各ノードにブロードキャストし、その後各ノードがデータを個別に結合します。

以下は、シャッフル ハッシュ結合の一般的な実行プランです。

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

上記の実行計画では次のようになります。

-   クエリ フラグメント`[TableFullScan_20, Selection_21, ExchangeSender_22]`テーブル b からデータを読み取り、データを上流の MPP タスクにシャッフルします。
-   クエリ フラグメント`[TableFullScan_16, Selection_17, ExchangeSender_18]`はテーブル a からデータを読み取り、データを上流の MPP タスクにシャッフルします。
-   クエリ フラグメント`[ExchangeReceiver_19, ExchangeReceiver_23, HashJoin_44, ExchangeSender_47]`はすべてのデータを結合し、TiDB に返します。

ブロードキャスト結合の一般的な実行計画は次のとおりです。

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

上記の実行計画では次のようになります。

-   クエリ フラグメント`[TableFullScan_17, Selection_18, ExchangeSender_19]`は、小さなテーブル (テーブル a) からデータを読み取り、そのデータを大きなテーブル (テーブル b) のデータを含む各ノードにブロードキャストします。
-   クエリ フラグメント`[TableFullScan_21, Selection_22, ExchangeReceiver_20, HashJoin_43, ExchangeSender_46]`はすべてのデータを結合し、TiDB に返します。

## MPP モードの<code>EXPLAIN ANALYZE</code>ステートメント {#code-explain-analyze-code-statements-in-the-mpp-mode}

`EXPLAIN ANALYZE`ステートメントは`EXPLAIN`に似ていますが、実行時情報も出力します。

以下は、単純な`EXPLAIN ANALYZE`例の出力です。

```sql
EXPLAIN ANALYZE SELECT COUNT(*) FROM t1 GROUP BY id;
```

```sql
+------------------------------------+---------+---------+-------------------+---------------+---------------------------------------------------------------------------------------------------+----------------------------------------------------------------+--------+------+
| id                                 | estRows | actRows | task              | access object | execution info                                                                                    | operator info                                                  | memory | disk |
+------------------------------------+---------+---------+-------------------+---------------+---------------------------------------------------------------------------------------------------+----------------------------------------------------------------+--------+------+
| TableReader_31                     | 4.00    | 2       | root              |               | time:44.5ms, loops:2, cop_task: {num: 1, max: 0s, proc_keys: 0, copr_cache_hit_ratio: 0.00}       | data:ExchangeSender_30                                         | N/A    | N/A  |
| └─ExchangeSender_30                | 4.00    | 2       | batchCop[tiflash] |               | tiflash_task:{time:16.5ms, loops:1, threads:1}                                                    | ExchangeType: PassThrough, tasks: [2, 3, 4]                    | N/A    | N/A  |
|   └─Projection_26                  | 4.00    | 2       | batchCop[tiflash] |               | tiflash_task:{time:16.5ms, loops:1, threads:1}                                                    | Column#4                                                       | N/A    | N/A  |
|     └─HashAgg_27                   | 4.00    | 2       | batchCop[tiflash] |               | tiflash_task:{time:16.5ms, loops:1, threads:1}                                                    | group by:test.t1.id, funcs:sum(Column#7)->Column#4             | N/A    | N/A  |
|       └─ExchangeReceiver_29        | 4.00    | 2       | batchCop[tiflash] |               | tiflash_task:{time:14.5ms, loops:1, threads:20}                                                   |                                                                | N/A    | N/A  |
|         └─ExchangeSender_28        | 4.00    | 0       | batchCop[tiflash] |               | tiflash_task:{time:9.49ms, loops:0, threads:0}                                                    | ExchangeType: HashPartition, Hash Cols: test.t1.id, tasks: [1] | N/A    | N/A  |
|           └─HashAgg_9              | 4.00    | 0       | batchCop[tiflash] |               | tiflash_task:{time:9.49ms, loops:0, threads:0}                                                    | group by:test.t1.id, funcs:count(1)->Column#7                  | N/A    | N/A  |
|             └─TableFullScan_25     | 6.00    | 0       | batchCop[tiflash] | table:t1      | tiflash_task:{time:9.49ms, loops:0, threads:0}, tiflash_scan:{dtfile:{total_scanned_packs:1,...}} | keep order:false                                               | N/A    | N/A  |
+------------------------------------+---------+---------+-------------------+---------------+---------------------------------------------------------------------------------------------------+----------------------------------------------------------------+--------+------+
```

`EXPLAIN`の出力と比較して、演算子`ExchangeSender`の`operator info`列には`tasks`表示されます。これは、クエリ フラグメントがインスタンス化される MPP タスクの ID を記録します。さらに、各 MPP オペレーターには`execution info`列に`threads`フィールドがあり、TiDB がこのオペレーターを実行するときの操作の同時実行性が記録されます。クラスターが複数のノードで構成されている場合、この同時実行数は、すべてのノードの同時実行数を合計した結果になります。

## MPP バージョンと交換データ圧縮 {#mpp-version-and-exchange-data-compression}

v6.6.0 以降、新しいフィールド`MPPVersion`と`Compression`が MPP 実行プランに追加されます。

-   `MppVersion` : MPP 実行プランのバージョン番号。システム変数[`mpp_version`](/system-variables.md#mpp_version-new-in-v660)を通じて設定できます。
-   `Compression` : `Exchange`演算子のデータ圧縮モード。システム変数[`mpp_exchange_compression_mode`](/system-variables.md#mpp_exchange_compression_mode-new-in-v660)を通じて設定できます。データ圧縮が有効になっていない場合、このフィールドは実行計画に表示されません。

次の例を参照してください。

```sql
mysql > EXPLAIN SELECT COUNT(*) AS count_order FROM lineitem GROUP BY l_returnflag, l_linestatus ORDER BY l_returnflag, l_linestatus;

+----------------------------------------+--------------+--------------+----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id                                     | estRows      | task         | access object  | operator info                                                                                                                                                                                                                                                                        |
+----------------------------------------+--------------+--------------+----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Projection_6                           | 3.00         | root         |                | Column#18                                                                                                                                                                                                                                                                            |
| └─Sort_8                               | 3.00         | root         |                | tpch100.lineitem.l_returnflag, tpch100.lineitem.l_linestatus                                                                                                                                                                                                                         |
|   └─TableReader_36                     | 3.00         | root         |                | MppVersion: 1, data:ExchangeSender_35                                                                                                                                                                                                                                                |
|     └─ExchangeSender_35                | 3.00         | mpp[tiflash] |                | ExchangeType: PassThrough                                                                                                                                                                                                                                                            |
|       └─Projection_31                  | 3.00         | mpp[tiflash] |                | Column#18, tpch100.lineitem.l_returnflag, tpch100.lineitem.l_linestatus                                                                                                                                                                                                              |
|         └─HashAgg_32                   | 3.00         | mpp[tiflash] |                | group by:tpch100.lineitem.l_linestatus, tpch100.lineitem.l_returnflag, funcs:sum(Column#23)->Column#18, funcs:firstrow(tpch100.lineitem.l_returnflag)->tpch100.lineitem.l_returnflag, funcs:firstrow(tpch100.lineitem.l_linestatus)->tpch100.lineitem.l_linestatus, stream_count: 20 |
|           └─ExchangeReceiver_34        | 3.00         | mpp[tiflash] |                | stream_count: 20                                                                                                                                                                                                                                                                     |
|             └─ExchangeSender_33        | 3.00         | mpp[tiflash] |                | ExchangeType: HashPartition, Compression: FAST, Hash Cols: [name: tpch100.lineitem.l_returnflag, collate: utf8mb4_bin], [name: tpch100.lineitem.l_linestatus, collate: utf8mb4_bin], stream_count: 20                                                                                |
|               └─HashAgg_14             | 3.00         | mpp[tiflash] |                | group by:tpch100.lineitem.l_linestatus, tpch100.lineitem.l_returnflag, funcs:count(1)->Column#23                                                                                                                                                                                     |
|                 └─TableFullScan_30     | 600037902.00 | mpp[tiflash] | table:lineitem | keep order:false                                                                                                                                                                                                                                                                     |
+----------------------------------------+--------------+--------------+----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

前述の実行計画の結果では、TiDB はバージョン`1`の MPP 実行計画を使用して`TableReader`をビルドします。 `HashPartition`タイプの`ExchangeSender`演算子は、 `FAST`データ圧縮モードを使用します。 `PassThrough`タイプの`ExchangeSender`オペレータでは、データ圧縮は有効になっていません。
