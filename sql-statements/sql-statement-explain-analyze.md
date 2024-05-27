---
title: EXPLAIN ANALYZE | TiDB SQL Statement Reference
summary: TiDB データベースのEXPLAIN ANALYZE の使用法の概要。
---

# EXPLAIN分析 {#explain-analyze}

`EXPLAIN ANALYZE`ステートメントは`EXPLAIN`と同様に機能しますが、主な違いは、実際にステートメントを実行することです。これにより、クエリ プランニングの一部として使用される推定値と、実行中に発生した実際の値を比較できます。推定値が実際の値と大幅に異なる場合は、影響を受けるテーブルで`ANALYZE TABLE`実行することを検討する必要があります。

> **注記：**
>
> `EXPLAIN ANALYZE`を使用して DML 文を実行すると、データの変更が正常に実行されます。現時点では、DML 文の実行プランはまだ表示**できません**。

## 概要 {#synopsis}

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

## EXPLAIN ANALYZE出力フォーマット {#explain-analyze-output-format}

`EXPLAIN`とは異なり、 `EXPLAIN ANALYZE`対応する SQL 文を実行し、その実行時情報を記録し、実行プランとともに情報を返します。したがって、 `EXPLAIN ANALYZE` `EXPLAIN`文の拡張と見なすことができます。 `EXPLAIN` (クエリ実行のデバッグ用) と比較すると、 `EXPLAIN ANALYZE`の戻り結果には`actRows` 、 `execution info` 、 `memory` 、 `disk`などの情報の列も含まれます。これらの列の詳細は、次のようになります。

| 属性名  | 説明                                                                                                                                                                    |
| :--- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 行為行  | 演算子によって出力される行数。                                                                                                                                                       |
| 実行情報 | 演算子の実行情報。1 `time` 、演算子に入ってから演算子を出るまでの合計`wall time`表します。これには、すべてのサブ演算子の合計実行時間が含まれます。演算子が親演算子によって何度も呼び出される場合 (ループ内)、時間は累積時間を参照します。5 `loops` 、現在の演算子が親演算子によって呼び出される回数です。 |
| メモリ  | 演算子によって占有されるメモリ領域。                                                                                                                                                    |
| ディスク | オペレータが占有するディスク領域。                                                                                                                                                     |

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

## オペレータの実行情報 {#execution-information-of-operators}

基本的な`time`と`loop`実行情報に加えて、 `execution info`はオペレータ固有の実行情報も含まれます。これには主に、オペレータが RPC 要求を送信するのに費やされた時間やその他のステップの期間が含まれます。

### ポイントゲット {#point-get}

`Point_Get`演算子からの実行情報には通常、次の情報が含まれます。

-   `Get:{num_rpc:1, total_time:697.051µs}` ：TiKVに送信された`Get`のRPC要求の数（ `num_rpc` ）とすべてのRPC要求の合計期間（ `total_time` ）。
-   `ResolveLock:{num_rpc:1, total_time:12.117495ms}` : TiDB がデータの読み取り時にロックに遭遇した場合、まずロックを解決する必要があります。これは通常、読み取り/書き込み競合のシナリオで発生します。この情報は、ロックの解決にかかる時間を示します。
-   `regionMiss_backoff:{num:11, total_time:2010 ms},tikvRPC_backoff:{num:11, total_time:10691 ms}` : RPC 要求が失敗すると、TiDB は要求を再試行する前にバックオフ時間待機します。バックオフ統計には、バックオフのタイプ ( `regionMiss`や`tikvRPC`など)、合計待機時間 ( `total_time` )、およびバックオフの合計数 ( `num` ) が含まれます。

### バッチポイント取得 {#batch-point-get}

`Batch_Point_Get`演算子の実行情報は`Point_Get`演算子と似ていますが、 `Batch_Point_Get`通常、データを読み取りするために`BatchGet` RPC 要求を TiKV に送信します。

`BatchGet:{num_rpc:2, total_time:83.13µs}` ：TiKVに送信された`BatchGet`種類のRPC要求の数（ `num_rpc` ）とすべてのRPC要求に費やされた合計時間（ `total_time` ）。

### テーブルリーダー {#tablereader}

`TableReader`演算子の実行情報は通常、次のようになります。

    cop_task: {num: 6, max: 1.07587ms, min: 844.312µs, avg: 919.601µs, p95: 1.07587ms, max_proc_keys: 16, p95_proc_keys: 16, tot_proc: 1ms, tot_wait: 1ms, rpc_num: 6, rpc_time: 5.313996 ms, copr_cache_hit_ratio: 0.00}

-   `cop_task` : `cop`のタスクの実行情報が含まれます。例:
    -   `num` : copタスクの数。
    -   `max` `p95` cop タスクの実行に`min`れ`avg`実行時間の最大値、最小値、平均値、および P95 値。
    -   `max_proc_keys`と`p95_proc_keys` : すべての cop タスクで TiKV によってスキャンされた最大値と P95 キー値。最大値と P95 値の差が大きい場合、データ分布が不均衡になる可能性があります。
    -   `rpc_num` `rpc_time` TiKV に送信された`Cop` RPC 要求の合計数と合計消費時間。
    -   `copr_cache_hit_ratio` : `cop`タスク要求に対するコプロセッサーキャッシュのヒット率。
-   `backoff` : さまざまなタイプのバックオフとバックオフの合計待機時間が含まれます。

### 入れる {#insert}

`Insert`演算子の実行情報は通常、次のようになります。

    prepare:109.616µs, check_insert:{total_time:1.431678ms, mem_insert_time:667.878µs, prefetch:763.8µs, rpc:{BatchGet:{num_rpc:1, total_time:699.166µs},Get:{num_rpc:1, total_time:378.276µs }}}

-   `prepare` : 式、デフォルト値、自動増分値の計算など、書き込みの準備にかかる時間。
-   `check_insert` : この情報は通常、 `insert ignore`および`insert on duplicate`ステートメントで表示され、競合チェックや TiDB トランザクション キャッシュへのデータ書き込みに要した時間などが含まれます。この時間消費には、トランザクションのコミットに要した時間は含まれないことに注意してください。次の情報が含まれます。
    -   `total_time` : ステップ`check_insert`に費やされた合計時間。
    -   `mem_insert_time` : TiDB トランザクション キャッシュにデータを書き込むのにかかる時間。
    -   `prefetch` : TiKV から競合をチェックする必要があるデータを取得する期間。このステップでは、データを取得するために`Batch_Get` RPC 要求を TiKV に送信します。
    -   `rpc` : TiKV への RPC 要求の送信に費やされた合計時間。これには通常、 `BatchGet`と`Get` 2 種類の RPC 時間が含まれます。
        -   `prefetch`番目のステップで`BatchGet` RPC 要求が送信されます。
        -   `insert on duplicate`ステートメントが実行されると`duplicate update` 、 `Get` RPC 要求が送信されます。
-   `backoff` : さまざまなタイプのバックオフとバックオフの合計待機時間が含まれます。

### インデックス参加 {#indexjoin}

`IndexJoin`演算子には、同時実行用に 1 つの外部ワーカーと N 個の内部ワーカーがあります。結合結果では、外部テーブルの順序が保持されます。詳細な実行プロセスは次のとおりです。

1.  外側のワーカーは N 個の外側の行を読み取り、それをタスクにラップして、結果チャネルと内側のワーカー チャネルに送信します。
2.  内部ワーカーはタスクを受け取り、タスクからキー範囲を構築し、キー範囲に従って内部行を取得します。次に、内部行ハッシュ テーブルを構築します。
3.  メイン`IndexJoin`スレッドは結果チャネルからタスクを受信し、内部ワーカーがタスクの処理を完了するまで待機します。
4.  メイン`IndexJoin`スレッドは、内側の行のハッシュ テーブルを参照して、各外側の行を結合します。

`IndexJoin`演算子には次の実行情報が含まれます。

    inner:{total:4.297515932s, concurrency:5, task:17, construct:97.96291ms, fetch:4.164310088s, build:35.219574ms}, probe:53.574945ms

-   `Inner` : 内部ワーカーの実行情報:
    -   `total` : 内部ワーカーによって消費された合計時間。
    -   `concurrency` : 同時内部ワーカーの数。
    -   `task` : 内部ワーカーによって処理されたタスクの合計数。
    -   `construct` : 内部ワーカーがタスクに対応する内部テーブル行を読み取る前の準備時間。
    -   `fetch` : 内部ワーカーが内部テーブル行を読み取るのにかかる合計時間。
    -   `Build` : 内部ワーカーが対応する内部テーブル行のハッシュ テーブルを構築するのにかかる合計時間。
-   `probe` : メイン`IndexJoin`スレッドが外部テーブル行と内部テーブル行のハッシュ テーブルとの結合操作を実行するために費やした合計時間。

### インデックスハッシュ結合 {#indexhashjoin}

`IndexHashJoin`演算子の実行プロセスは、 `IndexJoin`演算子と似ています。5 演算`IndexHashJoin`にも 1 つの外部ワーカーと N 個の内部ワーカーがあり、並列で実行されますが、出力順序が外部テーブルと一致することは保証されません。詳細な実行プロセスは次のとおりです。

1.  外側のワーカーは N 個の外側の行を読み取り、タスクを構築して、それを内側のワーカー チャネルに送信します。
2.  内部ワーカーは、内部ワーカー チャネルからタスクを受信し、すべてのタスクに対して次の 3 つの操作を順番に実行します。a. 外部行からハッシュ テーブルを構築します。b. 外部行からキー範囲を構築し、内部行を取得します。c. ハッシュ テーブルをプローブし、結合結果を結果チャネルに送信します。注: ステップ a とステップ b は同時に実行されます。
3.  `IndexHashJoin`のメイン スレッドは、結果チャネルから結合結果を受信します。

`IndexHashJoin`演算子には次の実行情報が含まれます。

```sql
inner:{total:4.429220003s, concurrency:5, task:17, construct:96.207725ms, fetch:4.239324006s, build:24.567801ms, join:93.607362ms}
```

-   `Inner` : 内部ワーカーの実行情報:
    -   `total` : 内部ワーカーによって消費された合計時間。
    -   `concurrency` : 内部ワーカーの数。
    -   `task` : 内部ワーカーによって処理されたタスクの合計数。
    -   `construct` : 内部ワーカーが内部テーブル行を読み取る前の準備時間。
    -   `fetch` : 内部ワーカーが内部テーブル行を読み取るのに費やされた合計時間。
    -   `Build` : 内部ワーカーが外部テーブル行のハッシュ テーブルを構築するのに費やされた合計時間。
    -   `join` : 内部ワーカーが内部テーブル行と外部テーブル行のハッシュ テーブルを結合するのにかかる合計時間。

### ハッシュ結合 {#hashjoin}

`HashJoin`演算子には、内部ワーカー、外部ワーカー、および N 結合ワーカーがあります。詳細な実行プロセスは次のとおりです。

1.  内部ワーカーは内部テーブルの行を読み取り、ハッシュ テーブルを構築します。
2.  外部ワーカーは外部テーブルの行を読み取り、それをタスクにラップして結合ワーカーに送信します。
3.  結合ワーカーは、ステップ 1 のハッシュ テーブルの構築が完了するまで待機します。
4.  結合ワーカーは、タスク内の外部テーブル行とハッシュ テーブルを使用して結合操作を実行し、結合結果を結果チャネルに送信します。
5.  `HashJoin`のメイン スレッドは結果チャネルから結合結果を受信します。

`HashJoin`演算子には次の実行情報が含まれます。

    build_hash_table:{total:146.071334ms, fetch:110.338509ms, build:35.732825ms}, probe:{concurrency:5, total:857.162518ms, max:171.48271ms, probe:125.341665ms, fetch:731.820853ms}

-   `build_hash_table` : 内部テーブルのデータを読み取り、ハッシュテーブルの実行情報を構築します。
    -   `total` : 合計消費時間。
    -   `fetch` : 内部テーブルデータの読み取りに費やされた合計時間。
    -   `build` : ハッシュ テーブルの構築に費やされた合計時間。
-   `probe` : 結合ワーカーの実行情報:
    -   `concurrency` : 結合ワーカーの数。
    -   `total` : すべての結合ワーカーによって消費された合計時間。
    -   `max` : 単一の結合ワーカーが実行される最長時間。
    -   `probe` : 外部テーブル行とハッシュ テーブルとの結合に費やされた合計時間。
    -   `fetch` : 結合ワーカーが外部テーブル行データを読み取るために待機する合計時間。

### テーブルフルスキャン (TiFlash) {#tablefullscan-tiflash}

TiFlashノードで実行される`TableFullScan`演算子には、次の実行情報が含まれます。

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

-   `dtfile` : テーブルスキャン中の DTFile (DeltaTree ファイル) 関連情報。TiFlash Stableレイヤーのデータスキャンステータスを反映します。
    -   `total_scanned_packs` : DTFile でスキャンされたパックの合計数。パックとは、 TiFlash DTFile で読み取ることができる最小単位です。デフォルトでは、8192 行ごとに 1 つのパックが構成されます。
    -   `total_skipped_packs` : DTFile 内のスキャンによってスキップされたパックの合計数`WHERE`句がラフ セット インデックスにヒットするか、主キーの範囲フィルタリングに一致すると、無関係なパックはスキップされます。
    -   `total_scanned_rows` : DTFile でスキャンされた行の合計数。MVCC が原因で更新または削除のバージョンが複数ある場合、各バージョンは個別にカウントされます。
    -   `total_skipped_rows` : DTFile 内のスキャンによってスキップされる行の合計数。
    -   `total_rs_index_load_time` : DTFile ラフ セット インデックスの読み取りにかかった合計時間。
    -   `total_read_time` : DTFile データの読み取りに費やされた合計時間。
-   `total_create_snapshot_time` : テーブルスキャン中にスナップショットを作成するために使用された合計時間。

### lock_keys 実行情報 {#lock-keys-execution-information}

DML ステートメントが悲観的トランザクションで実行されると、演算子の実行情報に`lock_keys`の実行情報も含まれる場合があります。例:

    lock_keys: {time:94.096168ms, region:6, keys:8, lock_rpc:274.503214ms, rpc_count:6}

-   `time` : `lock_keys`操作を実行する合計時間。
-   `region` : `lock_keys`番目の操作の実行に関係する領域の数。
-   `keys` : `Lock`必要な`Key`の数。
-   `lock_rpc` : `Lock`タイプの RPC 要求を TiKV に送信するのに費やされた合計時間。複数の RPC 要求を並行して送信できるため、合計 RPC 時間消費は`lock_keys`操作の合計時間消費よりも長くなる可能性があります。
-   `rpc_count` : TiKV に送信された`Lock`タイプの RPC 要求の合計数。

### commit_txn 実行情報 {#commit-txn-execution-information}

`autocommit=1`のトランザクションで書き込み型 DML ステートメントが実行されると、書き込み演算子の実行情報にはトランザクションコミットの期間情報も含まれます。例:

    commit_txn: {prewrite:48.564544ms, wait_prewrite_binlog:47.821579, get_commit_ts:4.277455ms, commit:50.431774ms, region_num:7, write_keys:16, write_byte:536}

-   `prewrite` : トランザクションの 2PC コミットの`prewrite`フェーズに費やされた時間。
-   `wait_prewrite_binlog:` : 事前書き込みBinlog の書き込みを待機するのにかかる時間。
-   `get_commit_ts` : トランザクションコミットタイムスタンプを取得するのに費やされた時間。
-   `commit` : トランザクションの 2PC コミット中に`commit`フェーズで消費された時間。
-   `write_keys` : トランザクションに書き込まれた合計`keys` 。
-   `write_byte` : トランザクションで書き込まれた合計バイト数`key-value`単位はバイトです。

### RU（リクエストユニット）消費量 {#ru-request-unit-consumption}

[リクエストユニット (RU)](/tidb-resource-control.md#what-is-request-unit-ru)は、TiDB リソース制御で定義されているシステム リソースの統一された抽象化単位です。最上位レベルの演算子の`execution info` 、この特定の SQL ステートメントの全体的な RU 消費量を示します。

    RU:273.842670

> **注記：**
>
> この値は、この実行で実際に消費された RU を示します。キャッシュの影響により、同じ SQL ステートメントでも、実行されるたびに消費される RU の量が異なる場合があります (たとえば、 [コプロセッサキャッシュ](/coprocessor-cache.md) )。

RU は、 `EXPLAIN ANALYZE`の他の値、具体的には`execution info`列から計算できます。例:

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

基本コストは[`tikv/pd`ソースコード](https://github.com/tikv/pd/blob/aeb259335644d65a97285d7e62b38e7e43c6ddca/client/resource_group/controller/config.go#L58C19-L67)ファイルで定義され、計算は[`model.go`](https://github.com/tikv/pd/blob/54219d649fb4c8834cd94362a63988f3c074d33e/client/resource_group/controller/model.go#L107)ファイルで実行されます。

TiDB v7.1 を使用している場合、計算は`pd/pd-client/model.go`の`BeforeKVRequest()`と`AfterKVRequest()`の合計になります。つまり、次のようになります。

    before key/value request is processed:
          consumption.RRU += float64(kc.ReadBaseCost) -> kv.ReadBaseCost * rpc_nums

    after key/value request is processed:
          consumption.RRU += float64(kc.ReadBytesCost) * readBytes -> kc.ReadBytesCost * total_process_keys_size
          consumption.RRU += float64(kc.CPUMsCost) * kvCPUMs -> kc.CPUMsCost * total_process_time

書き込みとバッチ取得の場合、計算は基本コストが異なりますが、同様です。

### その他の一般的な実行情報 {#other-common-execution-information}

コプロセッサーオペレータには通常、 `cop_task`と`tikv_task` 2 つの実行時間情報の部分が含まれます。 `cop_task` TiDB によって記録された時間で、リクエストがサーバーに送信されてから応答が受信されるまでの時間です。 `tikv_task`は TiKVコプロセッサー自体によって記録された時間です。 2 つの間に大きな差がある場合は、応答を待つ時間が長すぎるか、gRPC またはネットワークに費やされた時間が長すぎることを示している可能性があります。

## MySQL 互換性 {#mysql-compatibility}

`EXPLAIN ANALYZE`は MySQL 8.0 の機能ですが、TiDB の出力形式と潜在的な実行プランはどちらも MySQL とは大幅に異なります。

## 参照 {#see-also}

-   [クエリ実行プランを理解する](/explain-overview.md)
-   [EXPLAIN](/sql-statements/sql-statement-explain.md)
-   [テーブルを分析](/sql-statements/sql-statement-analyze-table.md)
-   [痕跡](/sql-statements/sql-statement-trace.md)
