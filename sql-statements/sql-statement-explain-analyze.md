---
title: EXPLAIN ANALYZE | TiDB SQL Statement Reference
summary: An overview of the usage of EXPLAIN ANALYZE for the TiDB database.
---

# EXPLAINの説明 {#explain-analyze}

`EXPLAIN ANALYZE`ステートメントは`EXPLAIN`と同様に機能しますが、主な違いはステートメントを実際に実行することです。これにより、クエリ計画の一部として使用される推定値と、実行中に発生した実際の値を比較できます。推定値が実際の値と大きく異なる場合は、影響を受けるテーブルで`ANALYZE TABLE`を実行することを検討する必要があります。

> **注記：**
>
> `EXPLAIN ANALYZE`を使用して DML ステートメントを実行すると、通常、データの変更が実行されます。現在、DML ステートメントの実行計画はまだ表示**できません**。

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

## EXPLAIN ANALYZE の出力形式 {#explain-analyze-output-format}

`EXPLAIN`とは異なり、 `EXPLAIN ANALYZE`対応する SQL ステートメントを実行し、そのランタイム情報を記録し、その情報を実行計画とともに返します。したがって、 `EXPLAIN ANALYZE` `EXPLAIN`ステートメントの拡張であると考えることができます。 `EXPLAIN` (クエリ実行のデバッグ用) と比較して、 `EXPLAIN ANALYZE`の返される結果には、 `actRows` 、 `execution info` 、 `memory` 、 `disk`などの情報列も含まれています。これらの列の詳細は次のとおりです。

| 属性名  | 説明                                                                                                                                                                                 |
| :--- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 行為行  | 演算子によって出力された行数。                                                                                                                                                                    |
| 実行情報 | オペレーターの実行情報。 `time`すべてのサブオペレーターの合計実行時間を含む、オペレーターの入力からオペレーターの退出までの合計`wall time`を表します。オペレーターが親オペレーターによって (ループ内で) 何度も呼び出される場合、時間は累積時間を指します。 `loops`は、現在のオペレーターが親オペレーターによって呼び出される回数です。 |
| メモリ  | オペレータが占有するメモリ空間。                                                                                                                                                                   |
| ディスク | オペレーターが占有するディスク容量。                                                                                                                                                                 |

## 例 {#examples}

```sql
CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
```

```sql
Query OK, 0 rows affected (0.12 sec)
```

```sql
INSERT INTO t1 (c1) VALUES (1), (2), (3);
```

```sql
Query OK, 3 rows affected (0.02 sec)
Records: 3  Duplicates: 0  Warnings: 0
```

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

基本的な`time`および`loop`実行情報に加えて、 `execution info`にはオペレーター固有の実行情報も含まれます。これには、主にオペレーターが RPC 要求を送信するのに費やされた時間やその他のステップの時間が含まれます。

### ポイントゲット {#point-get}

`Point_Get`オペレーターからの実行情報には通常、次の情報が含まれます。

-   `Get:{num_rpc:1, total_time:697.051µs}` : TiKV に送信された`Get` RPC リクエストの数 ( `num_rpc` ) と、すべての RPC リクエストの合計継続時間 ( `total_time` )。
-   `ResolveLock:{num_rpc:1, total_time:12.117495ms}` : データの読み取り時に TiDB がロックに遭遇した場合、最初にロックを解決する必要があります。これは通常、読み取りと書き込みの競合シナリオで発生します。この情報は、ロックの解決にかかる時間を示します。
-   `regionMiss_backoff:{num:11, total_time:2010 ms},tikvRPC_backoff:{num:11, total_time:10691 ms}` : RPC リクエストが失敗した場合、TiDB はリクエストを再試行する前にバックオフ時間待機します。バックオフ統計には、バックオフのタイプ ( `regionMiss`や`tikvRPC`など)、合計待機時間 ( `total_time` )、およびバックオフの合計数 ( `num` ) が含まれます。

### バッチポイント取得 {#batch-point-get}

`Batch_Point_Get`オペレーターの実行情報は`Point_Get`オペレーターの実行情報と似ていますが、 `Batch_Point_Get`通常、データを読み取るために`BatchGet` RPC リクエストを TiKV に送信します。

`BatchGet:{num_rpc:2, total_time:83.13µs}` : TiKV に送信された`BatchGet`種類の RPC リクエストの数 ( `num_rpc` ) と、すべての RPC リクエストに費やされた合計時間 ( `total_time` )。

### テーブルリーダー {#tablereader}

`TableReader`オペレーターの実行情報は通常次のとおりです。

    cop_task: {num: 6, max: 1.07587ms, min: 844.312µs, avg: 919.601µs, p95: 1.07587ms, max_proc_keys: 16, p95_proc_keys: 16, tot_proc: 1ms, tot_wait: 1ms, rpc_num: 6, rpc_time: 5.313996 ms, copr_cache_hit_ratio: 0.00}

-   `cop_task` : `cop`のタスクの実行情報が含まれます。例えば：
    -   `num` : 警官タスクの数。
    -   `max` 、 `min` 、 `avg` 、 `p95` :cop タスクの実行に消費された実行時間の最大値、最小値、平均値、および P95 値。
    -   `max_proc_keys`および`p95_proc_keys` : すべての警察タスクで TiKV によってスキャンされた最大キー値と P95 キー値。最大値とP95値の差が大きい場合、データの分布が偏っている可能性があります。
    -   `rpc_num` 、 `rpc_time` : TiKV に送信された`Cop` RPC リクエストに費やされた合計数と合計時間。
    -   `copr_cache_hit_ratio` : `cop`タスク リクエストに対するコプロセッサーキャッシュのヒット率。
-   `backoff` : さまざまなタイプのバックオフとバックオフの合計待機時間が含まれます。

### 入れる {#insert}

`Insert`オペレーターの実行情報は通常次のとおりです。

    prepare:109.616µs, check_insert:{total_time:1.431678ms, mem_insert_time:667.878µs, prefetch:763.8µs, rpc:{BatchGet:{num_rpc:1, total_time:699.166µs},Get:{num_rpc:1, total_time:378.276µs }}}

-   `prepare` : 式、デフォルト値、および自動インクリメント値の計算を含む、書き込みの準備にかかる時間。
-   `check_insert` : この情報は通常、競合チェックや TiDB トランザクション キャッシュへのデータの書き込みにかかる時間を含む、 `insert ignore`および`insert on duplicate`ステートメントに表示されます。この所要時間には、トランザクションのコミットにかかる時間は含まれないことに注意してください。これには次の情報が含まれます。
    -   `total_time` : `check_insert`ステップに費やした合計時間。
    -   `mem_insert_time` : TiDB トランザクション キャッシュへのデータの書き込みにかかる時間。
    -   `prefetch` : 競合をチェックする必要があるデータを TiKV から取得する期間。このステップでは、データを取得するために`Batch_Get` RPC リクエストを TiKV に送信します。
    -   `rpc` : TiKV に RPC リクエストを送信するために消費された合計時間。これには通常、次の 2 種類の RPC 時間`BatchGet`と`Get`が含まれます。
        -   `BatchGet` RPC リクエストは`prefetch`ステップで送信されます。
        -   `Get` RPC リクエストは、 `insert on duplicate` `duplicate update`の実行時に送信されます。
-   `backoff` : さまざまなタイプのバックオフとバックオフの合計待機時間が含まれます。

### インデックス結合 {#indexjoin}

`IndexJoin`オペレーターには、同時実行のために 1 つの外部ワーカーと N つの内部ワーカーがあります。結合結果は外部テーブルの順序を保持します。詳細な実行プロセスは次のとおりです。

1.  外側のワーカーは N 個の外側の行を読み取り、それをタスクにラップし、結果チャネルと内側のワーカー チャネルに送信します。
2.  内部ワーカーはタスクを受け取り、タスクからキー範囲を構築し、キー範囲に従って内部行をフェッチします。次に、内部行のハッシュ テーブルを構築します。
3.  メイン`IndexJoin`スレッドは結果チャネルからタスクを受け取り、内部ワーカーがタスクの処理を完了するまで待機します。
4.  メイン`IndexJoin`スレッドは、内側の行のハッシュ テーブルを参照して、外側の各行を結合します。

`IndexJoin`演算子には次の実行情報が含まれます。

    inner:{total:4.297515932s, concurrency:5, task:17, construct:97.96291ms, fetch:4.164310088s, build:35.219574ms}, probe:53.574945ms

-   `Inner` : 内部ワーカーの実行情報:
    -   `total` : 内部ワーカーによって消費された合計時間。
    -   `concurrency` : 同時内部ワーカーの数。
    -   `task` : 内部ワーカーによって処理されたタスクの総数。
    -   `construct` : 内部ワーカーがタスクに対応する内部テーブル行を読み取る前の準備時間。
    -   `fetch` : 内部ワーカーが内部テーブルの行を読み取るのにかかる合計時間。
    -   `Build` : 内部ワーカーが対応する内部テーブル行のハッシュ テーブルを構築するのにかかる合計時間。
-   `probe` : メイン`IndexJoin`スレッドが外部テーブルの行と内部テーブルの行のハッシュ テーブルとの結合操作を実行するために費やした合計時間。

### インデックスハッシュ結合 {#indexhashjoin}

`IndexHashJoin`オペレーターの実行プロセスは`IndexJoin`オペレーターの実行プロセスと同様です。 `IndexHashJoin`演算子には、並列実行する 1 つの外部ワーカーと N つの内部ワーカーもありますが、出力順序が外部テーブルの順序と一致することは保証されません。詳細な実行プロセスは次のとおりです。

1.  外側のワーカーは外側の N 行を読み取り、タスクを構築し、それを内側のワーカー チャネルに送信します。
2.  内部ワーカーは内部ワーカー チャネルからタスクを受け取り、すべてのタスクに対して次の 3 つの操作を順番に実行します。 b. 外側の行からハッシュ テーブルを構築します。 c. 外側の行からキー範囲を構築し、内側の行をフェッチします。ハッシュ テーブルを調査し、結合結果を結果チャネルに送信します。注: ステップ a とステップ b は同時に実行されます。
3.  `IndexHashJoin`のメイン スレッドは、結果チャネルから結合結果を受け取ります。

`IndexHashJoin`演算子には次の実行情報が含まれます。

```sql
inner:{total:4.429220003s, concurrency:5, task:17, construct:96.207725ms, fetch:4.239324006s, build:24.567801ms, join:93.607362ms}
```

-   `Inner` : 内部ワーカーの実行情報:
    -   `total` : 内部ワーカーによって消費された合計時間。
    -   `concurrency` : 内部ワーカーの数。
    -   `task` : 内部ワーカーによって処理されたタスクの総数。
    -   `construct` : 内部ワーカーが内部テーブルの行を読み取る前の準備時間。
    -   `fetch` : 内部ワーカーが内部テーブルの行を読み取るために費やした合計時間。
    -   `Build` : 内部ワーカーが外部テーブル行のハッシュ テーブルを構築するために費やした合計時間。
    -   `join` : 内部ワーカーが内部テーブルの行と外部テーブルの行のハッシュ テーブルとの結合に費やした合計時間。

### ハッシュ結合 {#hashjoin}

`HashJoin`のオペレーターには、内部ワーカー、外部ワーカー、および N 個の結合ワーカーがあります。詳細な実行プロセスは次のとおりです。

1.  内部ワーカーは内部テーブルの行を読み取り、ハッシュ テーブルを構築します。
2.  外部ワーカーは外部テーブルの行を読み取り、それをタスクにラップして結合ワーカーに送信します。
3.  結合ワーカーは、ステップ 1 のハッシュ テーブルの構築が完了するまで待機します。
4.  結合ワーカーは、タスク内の外部テーブルの行とハッシュ テーブルを使用して結合操作を実行し、結合結果を結果チャネルに送信します。
5.  `HashJoin`のメインスレッドは結果チャネルから結合結果を受け取ります。

`HashJoin`演算子には次の実行情報が含まれます。

    build_hash_table:{total:146.071334ms, fetch:110.338509ms, build:35.732825ms}, probe:{concurrency:5, total:857.162518ms, max:171.48271ms, probe:125.341665ms, fetch:731.820853ms}

-   `build_hash_table` : 内部テーブルのデータを読み取り、ハッシュ テーブルの実行情報を構築します。
    -   `total` : 合計の消費時間。
    -   `fetch` : 内部テーブルのデータの読み取りに費やされた合計時間。
    -   `build` : ハッシュ テーブルの構築に費やされた合計時間。
-   `probe` : 結合ワーカーの実行情報:
    -   `concurrency` : 結合ワーカーの数。
    -   `total` : すべての結合ワーカーによって消費された合計時間。
    -   `max` : 単一の結合ワーカーの実行にかかる最長時間。
    -   `probe` : 外部テーブルの行とハッシュ テーブルとの結合に費やされる合計時間。
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

-   `dtfile` : テーブル スキャン中の DTFile (DeltaTree File) 関連情報。これは、 TiFlash Stableレイヤーのデータ スキャン ステータスを反映します。
    -   `total_scanned_packs` : DTFile でスキャンされたパックの総数。パックとは、 TiFlash DTFile で読み込める最小単位です。デフォルトでは、8192 行ごとにパックが構成されます。
    -   `total_skipped_packs` : DTFile 内のスキャンによってスキップされたパックの総数。 `WHERE`句が大まかなセットのインデックスにヒットするか、主キーの範囲フィルタリングに一致する場合、無関係なパックはスキップされます。
    -   `total_scanned_rows` : DTFile 内でスキャンされた行の総数。 MVCC が原因で複数のバージョンの更新または削除がある場合、各バージョンは個別にカウントされます。
    -   `total_skipped_rows` : DTFile 内のスキャンによってスキップされた行の総数。
    -   `total_rs_index_load_time` : DTFile のラフ セット インデックスの読み取りに使用された合計時間。
    -   `total_read_time` : DTFile データの読み取りに費やされた合計時間。
-   `total_create_snapshot_time` : テーブル スキャン中にスナップショットの作成に費やされた合計時間。

### lock_keys 実行情報 {#lock-keys-execution-information}

DML ステートメントが悲観的トランザクションで実行される場合、演算子の実行情報には`lock_keys`の実行情報も含まれる場合があります。例えば：

    lock_keys: {time:94.096168ms, region:6, keys:8, lock_rpc:274.503214ms, rpc_count:6}

-   `time` : `lock_keys`操作を実行する合計時間。
-   `region` : `lock_keys`操作の実行に関係するリージョンの数。
-   `keys` : `Lock`が必要な`Key`の数。
-   `lock_rpc` : `Lock`種類の RPC リクエストを TiKV に送信するのに費やした合計時間。複数の RPC 要求を並行して送信できるため、RPC の合計消費時間は`lock_keys`操作の合計消費時間よりも長くなる可能性があります。
-   `rpc_count` : TiKV に送信された`Lock`種類の RPC リクエストの合計数。

### commit_txnの実行情報 {#commit-txn-execution-information}

`autocommit=1`のトランザクションで書き込み型の DML ステートメントが実行される場合、書き込み演算子の実行情報には、トランザクション コミットの期間情報も含まれます。例えば：

    commit_txn: {prewrite:48.564544ms, wait_prewrite_binlog:47.821579, get_commit_ts:4.277455ms, commit:50.431774ms, region_num:7, write_keys:16, write_byte:536}

-   `prewrite` : トランザクションの 2PC コミットの`prewrite`フェーズに費やされた時間。
-   `wait_prewrite_binlog:` : 事前書き込みBinlogの書き込みを待機するために費やされる時間。
-   `get_commit_ts` : トランザクションコミットタイムスタンプの取得にかかる時間。
-   `commit` : トランザクションの 2PC コミット中の`commit`フェーズに費やされた時間。
-   `write_keys` : トランザクションに書き込まれた合計`keys` 。
-   `write_byte` : トランザクションで書き込まれた`key-value`の合計バイト数。単位はバイトです。

### RU（リクエストユニット）の消費量 {#ru-request-unit-consumption}

[リクエストユニット(RU)](/tidb-resource-control.md#what-is-request-unit-ru)は、TiDB リソース制御で定義されるシステム リソースの統一抽象化単位です。最上位演算子の`execution info`この特定の SQL ステートメントの全体的な RU 消費量を示します。

    RU:273.842670

> **注記：**
>
> この値は、この実行によって消費された実際の RU を示します。同じ SQL ステートメントは、キャッシュの影響により、実行されるたびに異なる量の RU を消費する可能性があります (たとえば、 [コプロセッサキャッシュ](/coprocessor-cache.md) )。

`EXPLAIN ANALYZE`の他の値、特に`execution info`列から RU を計算できます。例えば：

```json
'executeInfo':
   time:2.55ms, 
   loops:2, 
   RU:0.329460, 
   Get:{
       num_rpc:1,
       total_time:2.13ms
   }, 
   total_process_time: 231.5µs,
   total_wait_time: 732.9µs, 
   tikv_wall_time: 995.8µs,
   scan_detail: {
      total_process_keys: 1, 
      total_process_keys_size: 150, 
      total_keys: 1, 
      get_snapshot_time: 691.7µs,
      rocksdb: {
          block: {
              cache_hit_count: 2,
              read_count: 1,
              read_byte: 8.19 KB,
              read_time: 10.3µs
          }
      }
  },
```

基本コストは[`tikv/pd`ソースコード](https://github.com/tikv/pd/blob/aeb259335644d65a97285d7e62b38e7e43c6ddca/client/resource_group/controller/config.go#L58C19-L67)で定義され、計算は[`model.go`](https://github.com/tikv/pd/blob/54219d649fb4c8834cd94362a63988f3c074d33e/client/resource_group/controller/model.go#L107)ファイルで実行されます。

TiDB v7.1 を使用している場合、計算は`pd/pd-client/model.go`の`BeforeKVRequest()`と`AfterKVRequest()`の合計です。つまり、次のようになります。

    before key/value request is processed:
          consumption.RRU += float64(kc.ReadBaseCost) -> kv.ReadBaseCost * rpc_nums

    after key/value request is processed:
          consumption.RRU += float64(kc.ReadBytesCost) * readBytes -> kc.ReadBytesCost * total_process_keys_size
          consumption.RRU += float64(kc.CPUMsCost) * kvCPUMs -> kc.CPUMsCost * total_process_time

書き込みとバッチ取得の場合、計算は同様ですが、基本コストは異なります。

### その他の一般的な実行情報 {#other-common-execution-information}

コプロセッサーオペレータには通常、実行時間情報の 2 つの部分 ( `cop_task`と`tikv_task`が含まれています。 `cop_task`は TiDB によって記録された時間で、リクエストがサーバーに送信された瞬間からレスポンスが受信されるまでの時間です。 `tikv_task`は、TiKVコプロセッサー自体によって記録された時間です。 2 つの間に大きな違いがある場合は、応答の待機時間が長すぎるか、gRPC またはネットワークに費やした時間が長すぎることを示している可能性があります。

## MySQLの互換性 {#mysql-compatibility}

`EXPLAIN ANALYZE`は MySQL 8.0 の機能ですが、TiDB の出力形式と潜在的な実行プランの両方が MySQL とは大きく異なります。

## こちらも参照 {#see-also}

-   [クエリ実行プランを理解する](/explain-overview.md)
-   [EXPLAIN](/sql-statements/sql-statement-explain.md)
-   [分析テーブル](/sql-statements/sql-statement-analyze-table.md)
-   [痕跡](/sql-statements/sql-statement-trace.md)
