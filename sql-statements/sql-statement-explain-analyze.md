---
title: EXPLAIN ANALYZE | TiDB SQL Statement Reference
summary: An overview of the usage of EXPLAIN ANALYZE for the TiDB database.
---

# EXPLAIN分析する {#explain-analyze}

`EXPLAIN ANALYZE`ステートメントは`EXPLAIN`と同様に機能しますが、主な違いはステートメントを実際に実行することです。これにより、クエリ計画の一部として使用される見積もりを、実行中に発生した実際の値と比較できます。見積もりが実際の値と大幅に異なる場合は、影響を受けるテーブルで`ANALYZE TABLE`を実行することを検討する必要があります。

> **ノート：**
>
> `EXPLAIN ANALYZE`を使用して DML ステートメントを実行すると、通常はデータの変更が実行されます。現在、DML ステートメントの実行計画はまだ表示**できません**。

## あらすじ {#synopsis}

```ebnf+diagram
ExplainSym ::=
    'EXPLAIN'
|   'DESCRIBE'
|    'DESC'

ExplainStmt ::=
    ExplainSym ( TableName ColumnName? | 'ANALYZE'? ExplainableStmt | 'FOR' 'CONNECTION' NUM | 'FORMAT' '=' ( stringLit | ExplainFormatType ) ( 'FOR' 'CONNECTION' NUM | ExplainableStmt ) )

ExplainableStmt ::=
    SelectStmt
|   DeleteFromStmt
|   UpdateStmt
|   InsertIntoStmt
|   ReplaceIntoStmt
|   UnionStmt
```

## EXPLAIN ANALYZE 出力形式 {#explain-analyze-output-format}

`EXPLAIN`とは異なり、 `EXPLAIN ANALYZE`対応する SQL ステートメントを実行し、そのランタイム情報を記録し、実行計画と共に情報を返します。したがって、 `EXPLAIN ANALYZE` `EXPLAIN`ステートメントの拡張と見なすことができます。 `EXPLAIN` (クエリ実行のデバッグ用) と比較すると、 `EXPLAIN ANALYZE`の戻り結果には、 `actRows` 、 `execution info` 、 `memory` 、および`disk`などの情報の列も含まれます。これらの列の詳細は次のとおりです。

| 属性名     | 説明                                                                                                                                                                                    |
| :------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| actRows | オペレーターによって出力された行数。                                                                                                                                                                    |
| 実行情報    | オペレーターの実行情報。 `time`すべてのサブオペレーターの合計実行時間を含めて、オペレーターに入ってからオペレーターを離れるまでの合計`wall time`を表します。オペレーターが親オペレーターによって (ループで) 何度も呼び出された場合、時間は累積時間を参照します。 `loops`は、現在のオペレーターが親オペレーターによって呼び出された回数です。 |
| メモリ     | オペレータが占有するメモリ空間。                                                                                                                                                                      |
| ディスク    | オペレーターが占有するディスク容量。                                                                                                                                                                    |

## 例 {#examples}

{{< copyable "" >}}

```sql
CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
```

```sql
Query OK, 0 rows affected (0.12 sec)
```

{{< copyable "" >}}

```sql
INSERT INTO t1 (c1) VALUES (1), (2), (3);
```

```sql
Query OK, 3 rows affected (0.02 sec)
Records: 3  Duplicates: 0  Warnings: 0
```

{{< copyable "" >}}

```sql
EXPLAIN ANALYZE SELECT * FROM t1 WHERE id = 1;
```

```sql
+-------------+---------+---------+------+---------------+----------------------------------------------------------------+---------------+--------+------+
| id          | estRows | actRows | task | access object | execution info                                                 | operator info | memory | disk |
+-------------+---------+---------+------+---------------+----------------------------------------------------------------+---------------+--------+------+
| Point_Get_1 | 1.00    | 1       | root | table:t1      | time:757.205µs, loops:2, Get:{num_rpc:1, total_time:697.051µs} | handle:1      | N/A    | N/A  |
+-------------+---------+---------+------+---------------+----------------------------------------------------------------+---------------+--------+------+
1 row in set (0.01 sec)
```

{{< copyable "" >}}

```sql
EXPLAIN ANALYZE SELECT * FROM t1;
```

```sql
+-------------------+----------+---------+-----------+---------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------+-----------+------+
| id                | estRows  | actRows | task      | access object | execution info                                                                                                                                                                                                                            | operator info                  | memory    | disk |
+-------------------+----------+---------+-----------+---------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------+-----------+------+
| TableReader_5     | 10000.00 | 3       | root      |               | time:278.2µs, loops:2, cop_task: {num: 1, max: 437.6µs, proc_keys: 3, rpc_num: 1, rpc_time: 423.9µs, copr_cache_hit_ratio: 0.00}                                                                                                          | data:TableFullScan_4           | 251 Bytes | N/A  |
| └─TableFullScan_4 | 10000.00 | 3       | cop[tikv] | table:t1      | tikv_task:{time:0s, loops:1}, scan_detail: {total_process_keys: 3, total_process_keys_size: 111, total_keys: 4, rocksdb: {delete_skipped_count: 0, key_skipped_count: 3, block: {cache_hit_count: 0, read_count: 0, read_byte: 0 Bytes}}} | keep order:false, stats:pseudo | N/A       | N/A  |
+-------------------+----------+---------+-----------+---------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------+-----------+------+
2 rows in set (0.00 sec)
```

## オペレーターの実行情報 {#execution-information-of-operators}

基本的な`time`と`loop`実行情報に加えて、 `execution info`にはオペレーター固有の実行情報も含まれます。これには、主に、オペレーターが RPC 要求を送信するのにかかった時間と、他のステップの所要時間が含まれます。

### Point_Get {#point-get}

`Point_Get`オペレーターからの実行情報には、通常、次の情報が含まれます。

-   `Get:{num_rpc:1, total_time:697.051µs}` : TiKV に送信された`Get` RPC 要求 ( `num_rpc` ) の数と、すべての RPC 要求の合計期間 ( `total_time` )。
-   `ResolveLock:{num_rpc:1, total_time:12.117495ms}` : TiDB がデータの読み取り中にロックに遭遇した場合、最初にロックを解決する必要があります。これは通常、読み取りと書き込みの競合のシナリオで発生します。この情報は、ロックを解決する期間を示します。
-   `regionMiss_backoff:{num:11, total_time:2010 ms},tikvRPC_backoff:{num:11, total_time:10691 ms}` : RPC リクエストが失敗した場合、TiDB はリクエストを再試行する前にバックオフ時間待機します。バックオフ統計には、バックオフのタイプ ( `regionMiss`や`tikvRPC`など)、合計待機時間 ( `total_time` )、およびバックオフの合計数 ( `num` ) が含まれます。

### Batch_Point_Get {#batch-point-get}

`Batch_Point_Get`オペレーターの実行情報は`Point_Get`オペレーターの実行情報と似ていますが、 `Batch_Point_Get`一般的に`BatchGet` RPC 要求を TiKV に送信してデータを読み取ります。

`BatchGet:{num_rpc:2, total_time:83.13µs}` : TiKV に送信された`BatchGet`タイプの RPC 要求の数 ( `num_rpc` ) と、すべての RPC 要求にかかった合計時間 ( `total_time` )。

### テーブルリーダー {#tablereader}

通常、 `TableReader`演算子の実行情報は次のとおりです。

```
cop_task: {num: 6, max: 1.07587ms, min: 844.312µs, avg: 919.601µs, p95: 1.07587ms, max_proc_keys: 16, p95_proc_keys: 16, tot_proc: 1ms, tot_wait: 1ms, rpc_num: 6, rpc_time: 5.313996 ms, copr_cache_hit_ratio: 0.00}
```

-   `cop_task` : `cop`のタスクの実行情報が含まれます。例えば：
    -   `num` : cop タスクの数。
    -   `max` 、 `min` 、 `avg` 、 `p95` : cop タスクの実行にかかった実行時間の最大値、最小値、平均値、および P95 値。
    -   `max_proc_keys`および`p95_proc_keys` : すべての警官タスクで TiKV によってスキャンされた最大および P95 キー値。最大値と P95 値の差が大きい場合、データ分布が偏っている可能性があります。
    -   `rpc_num` , `rpc_time` : TiKV に送信された`Cop` RPC リクエストの合計数と合計時間。
    -   `copr_cache_hit_ratio` : `cop`タスク要求に対するコプロセッサーキャッシュのヒット率。
-   `backoff` : さまざまなタイプのバックオフとバックオフの合計待機時間が含まれます。

### 入れる {#insert}

通常、 `Insert`演算子の実行情報は次のとおりです。

```
prepare:109.616µs, check_insert:{total_time:1.431678ms, mem_insert_time:667.878µs, prefetch:763.8µs, rpc:{BatchGet:{num_rpc:1, total_time:699.166µs},Get:{num_rpc:1, total_time:378.276µs }}}
```

-   `prepare` : 式、デフォルト値、および自動インクリメント値の計算を含む、書き込みの準備にかかった時間。
-   `check_insert` : この情報は通常、競合チェックや TiDB トランザクション キャッシュへのデータの書き込みにかかった時間を含め、 `insert ignore`と`insert on duplicate`ステートメントで表示されます。この消費時間には、トランザクションのコミットに費やされた時間が含まれていないことに注意してください。次の情報が含まれています。
    -   `total_time` : `check_insert`ステップに費やされた合計時間。
    -   `mem_insert_time` : TiDB トランザクション キャッシュへのデータの書き込みにかかった時間。
    -   `prefetch` : TiKV から競合をチェックする必要があるデータを取得する期間。このステップでは、 `Batch_Get` RPC リクエストを TiKV に送信してデータを取得します。
    -   `rpc` : RPC リクエストを TiKV に送信するために費やされた合計時間。これには、一般に`BatchGet`と`Get`の 2 種類の RPC 時間が含まれます。
        -   `BatchGet` RPC リクエストは`prefetch`ステップで送信されます。
        -   `Get` `insert on duplicate` `duplicate update`の実行時に RPC 要求が送信されます。
-   `backoff` : さまざまなタイプのバックオフとバックオフの合計待機時間が含まれます。

### 索引結合 {#indexjoin}

`IndexJoin`オペレーターには、同時実行用に 1 つの外部ワーカーと N 個の内部ワーカーがあります。結合結果は、外部テーブルの順序を保持します。詳細な実行プロセスは次のとおりです。

1.  外側のワーカーは外側の N 行を読み取り、それをタスクにラップして、結果チャネルと内側のワーカー チャネルに送信します。
2.  内部ワーカーはタスクを受け取り、タスクからキー範囲を構築し、キー範囲に従って内部行をフェッチします。次に、内側の行のハッシュ テーブルを作成します。
3.  メイン`IndexJoin`スレッドは結果チャネルからタスクを受け取り、内部ワーカーがタスクの処理を完了するのを待ちます。
4.  メイン`IndexJoin`スレッドは、内側の行のハッシュ テーブルを参照して、外側の各行を結合します。

`IndexJoin`演算子には、次の実行情報が含まれます。

```
inner:{total:4.297515932s, concurrency:5, task:17, construct:97.96291ms, fetch:4.164310088s, build:35.219574ms}, probe:53.574945ms
```

-   `Inner` : 内部ワーカーの実行情報:
    -   `total` : 内部ワーカーが消費した合計時間。
    -   `concurrency` : 同時内部ワーカーの数。
    -   `task` : 内部ワーカーによって処理されたタスクの総数。
    -   `construct` : 内部ワーカーがタスクに対応する内部テーブル行を読み取る前の準備時間。
    -   `fetch` : 内部ワーカーが内部テーブル行を読み取るのにかかる合計時間。
    -   `Build` : 内部ワーカーが対応する内部テーブル行のハッシュ テーブルを構築するのにかかる合計時間。
-   `probe` : メイン`IndexJoin`スレッドが外表行と内表行のハッシュ テーブルを結合操作するのにかかった合計時間。

### インデックスハッシュジョイン {#indexhashjoin}

`IndexHashJoin`オペレーターの実行プロセスは、 `IndexJoin`オペレーターの実行プロセスと似ています。 `IndexHashJoin`演算子には、並列に実行する 1 つの外部ワーカーと N 個の内部ワーカーもありますが、出力順序が外部テーブルの順序と一致することは保証されません。詳細な実行プロセスは次のとおりです。

1.  外側のワーカーは、N 個の外側の行を読み取り、タスクを構築して、内側のワーカー チャネルに送信します。
2.  内部ワーカーは、内部ワーカー チャネルからタスクを受け取り、タスクごとに次の 3 つの操作を順番に実行します。 a. 外側の行からハッシュ テーブルを作成します。外側の行からキー範囲を構築し、内側の行をフェッチします c.ハッシュ テーブルをプローブし、結合結果を結果チャネルに送信します。注: ステップ a とステップ b は同時に実行されています。
3.  `IndexHashJoin`のメイン スレッドは、結果チャネルから結合結果を受け取ります。

`IndexHashJoin`演算子には、次の実行情報が含まれます。

```sql
inner:{total:4.429220003s, concurrency:5, task:17, construct:96.207725ms, fetch:4.239324006s, build:24.567801ms, join:93.607362ms}
```

-   `Inner` : 内部ワーカーの実行情報:
    -   `total` : 内部ワーカーが消費した合計時間。
    -   `concurrency` : 内部ワーカーの数。
    -   `task` : 内部ワーカーによって処理されたタスクの総数。
    -   `construct` : 内部ワーカーが内部テーブルの行を読み取る前の準備時間。
    -   `fetch` : 内部ワーカーが内部テーブル行を読み取るのにかかった合計時間。
    -   `Build` : 内部ワーカーが外部テーブル行のハッシュ テーブルを構築するのにかかった合計時間。
    -   `join` : 内部ワーカーが内部表の行と外部表の行のハッシュ表を結合するのにかかった合計時間。

### ハッシュジョイン {#hashjoin}

`HashJoin`オペレーターには、内部ワーカー、外部ワーカー、および N 個の結合ワーカーがあります。詳細な実行プロセスは次のとおりです。

1.  内部ワーカーは、内部テーブルの行を読み取り、ハッシュ テーブルを構築します。
2.  外側のワーカーは外側のテーブルの行を読み取り、それをタスクにラップして結合ワーカーに送信します。
3.  結合ワーカーは、手順 1 のハッシュ テーブルの構築が完了するまで待機します。
4.  結合ワーカーは、タスク内の外部テーブルの行とハッシュ テーブルを使用して結合操作を実行し、結合結果を結果チャネルに送信します。
5.  `HashJoin`のメイン スレッドは、結果チャネルから結合結果を受け取ります。

`HashJoin`演算子には、次の実行情報が含まれます。

```
build_hash_table:{total:146.071334ms, fetch:110.338509ms, build:35.732825ms}, probe:{concurrency:5, total:857.162518ms, max:171.48271ms, probe:125.341665ms, fetch:731.820853ms}
```

-   `build_hash_table` : 内部テーブルのデータを読み取り、ハッシュ テーブルの実行情報を構築します。
    -   `total` : 総消費時間。
    -   `fetch` : 内部テーブル データの読み取りに費やされた合計時間。
    -   `build` : ハッシュ テーブルの構築に費やされた合計時間。
-   `probe` : 結合ワーカーの実行情報:
    -   `concurrency` : 結合ワーカーの数。
    -   `total` : すべての結合ワーカーが消費した合計時間。
    -   `max` : 単一の結合ワーカーの実行にかかる最長時間。
    -   `probe` : 外部表の行とハッシュ表の結合にかかった合計時間。
    -   `fetch` : 結合ワーカーが外部テーブルの行データを読み取るために待機する合計時間。

### テーブルフルスキャン (TiFlash) {#tablefullscan-tiflash}

TiFlashノードで実行される`TableFullScan`オペレーターには、次の実行情報が含まれます。

```sql
tiflash_scan: {
  dtfile: {
    total_scanned_packs: 2, 
    total_skipped_packs: 1, 
    total_scanned_rows: 16000, 
    total_skipped_rows: 8192, 
    total_rough_set_index_load_time: 2ms, 
    total_read_time: 20ms
  }, 
  total_create_snapshot_time: 1ms
}
```

-   `dtfile` : テーブル スキャンTiFlashの DTFile (DeltaTree ファイル) 関連情報。TiFlash Stableレイヤーのデータ スキャン ステータスを反映します。
    -   `total_scanned_packs` : DTFile でスキャンされたパックの総数。パックは、 TiFlash DTFile で読み取ることができる最小単位です。デフォルトでは、8192 行ごとに 1 つのパックが構成されます。
    -   `total_skipped_packs` : DTFile でスキャンによってスキップされたパックの総数。 `WHERE`句がラフ セット インデックスにヒットするか、主キーの範囲フィルタリングに一致する場合、無関係なパックはスキップされます。
    -   `total_scanned_rows` : DTFile でスキャンされた行の総数。 MVCC のために複数のバージョンの更新または削除がある場合、各バージョンは個別にカウントされます。
    -   `total_skipped_rows` : DTFile でスキャンによってスキップされた行の総数。
    -   `total_rs_index_load_time` : DTFile ラフ セット インデックスの読み取りに使用された合計時間。
    -   `total_read_time` : DTFile データの読み取りに使用された合計時間。
-   `total_create_snapshot_time` : テーブル スキャン中にスナップショットの作成に使用された合計時間。

### lock_keys 実行情報 {#lock-keys-execution-information}

悲観的トランザクションで DML ステートメントが実行されると、オペレーターの実行情報にも`lock_keys`の実行情報が含まれる場合があります。例えば：

```
lock_keys: {time:94.096168ms, region:6, keys:8, lock_rpc:274.503214ms, rpc_count:6}
```

-   `time` : `lock_keys`操作の合計実行時間。
-   `region` : `lock_keys`操作の実行に関与するリージョンの数。
-   `keys` : `Lock`を必要とする`Key`の数。
-   `lock_rpc` : `Lock`タイプの RPC リクエストを TiKV に送信するのに費やされた合計時間。複数の RPC 要求を並行して送信できるため、RPC の合計消費時間は、 `lock_keys`操作の合計消費時間よりも長くなる可能性があります。
-   `rpc_count` : TiKV に送信された`Lock`タイプの RPC リクエストの総数。

### commit_txn 実行情報 {#commit-txn-execution-information}

`autocommit=1`のトランザクションで write 型の DML 文を実行した場合、write 演算子の実行情報には、トランザクション commit の期間情報も含まれます。例えば：

```
commit_txn: {prewrite:48.564544ms, wait_prewrite_binlog:47.821579, get_commit_ts:4.277455ms, commit:50.431774ms, region_num:7, write_keys:16, write_byte:536}
```

-   `prewrite` : トランザクションの 2PC コミットの`prewrite`フェーズにかかった時間。
-   `wait_prewrite_binlog:` : 書き込み前のBinlogの書き込みを待機するのにかかった時間。
-   `get_commit_ts` : トランザクション コミット タイムスタンプを取得するためにかかった時間。
-   `commit` : トランザクションの 2PC コミット中に`commit`フェーズに費やされた時間。
-   `write_keys` : トランザクションで書き込まれた合計`keys` 。
-   `write_byte` : トランザクションで書き込まれた`key-value`の合計バイト数で、単位はバイトです。

### その他共通実行情報 {#other-common-execution-information}

通常、 コプロセッサーオペレーターには、実行時間情報の 2 つの部分 ( `cop_task`と`tikv_task`が含まれています。 `cop_task`は TiDB によって記録された時間であり、リクエストがサーバーに送信された瞬間から応答が受信される瞬間までです。 `tikv_task`は TiKV コプロセッサー自体によって記録された時間です。この 2 つに大きな違いがある場合は、応答の待機に費やされた時間が長すぎるか、gRPC またはネットワークに費やされた時間が長すぎることを示している可能性があります。

## MySQL の互換性 {#mysql-compatibility}

`EXPLAIN ANALYZE`は MySQL 8.0 の機能ですが、出力形式と TiDB の潜在的な実行計画の両方が MySQL とは大幅に異なります。

## こちらもご覧ください {#see-also}

-   [クエリ実行プランについて](/explain-overview.md)
-   [EXPLAIN](/sql-statements/sql-statement-explain.md)
-   [テーブルを分析](/sql-statements/sql-statement-analyze-table.md)
-   [痕跡](/sql-statements/sql-statement-trace.md)
