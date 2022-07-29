---
title: EXPLAIN ANALYZE | TiDB SQL Statement Reference
summary: An overview of the usage of EXPLAIN ANALYZE for the TiDB database.
---

# EXPLAIN分析 {#explain-analyze}

`EXPLAIN ANALYZE`ステートメントは`EXPLAIN`と同様に機能しますが、主な違いは、実際にステートメントを実行することです。これにより、クエリプランニングの一部として使用される見積もりを、実行中に検出された実際の値と比較できます。見積もりが実際の値と大幅に異なる場合は、影響を受けるテーブルで`ANALYZE TABLE`を実行することを検討する必要があります。

> **ノート：**
>
> `EXPLAIN ANALYZE`を使用してDMLステートメントを実行すると、通常、データの変更が実行されます。現在、DMLステートメントの実行プランはまだ表示**できませ**ん。

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

## EXPLAIN出力フォーマット {#explain-analyze-output-format}

`EXPLAIN`とは異なり、 `EXPLAIN ANALYZE`は対応するSQLステートメントを実行し、そのランタイム情報を記録して、実行プランと一緒に情報を返します。したがって、 `EXPLAIN ANALYZE`は`EXPLAIN`ステートメントの拡張と見なすことができます。 `EXPLAIN` （クエリ実行の`memory`用）と比較すると、 `EXPLAIN ANALYZE`の`execution info`結果には、 `actRows`などの情報の列も含まれ`disk` 。これらの列の詳細は次のとおりです。

| 属性名     | 説明                                                                                                                                                                     |
| :------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| actRows | オペレーターによって出力された行数。                                                                                                                                                     |
| 実行情報    | オペレーターの実行情報。 `time`は、すべてのサブオペレーターの合計実行時間を含む、オペレーターの入力からオペレーターの終了までの合計`wall time`を表します。演算子が親演算子によって（ループで）何度も呼び出される場合、時間は累積時間を参照します。 `loops`は、現在の演算子が親演算子によって呼び出された回数です。 |
| メモリー    | オペレーターが占有するメモリー・スペース。                                                                                                                                                  |
| ディスク    | オペレーターが占有するディスク容量。                                                                                                                                                     |

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

基本的な`time`および`loop`の実行情報に加えて、 `execution info`にはオペレーター固有の実行情報も含まれます。これには、主にオペレーターがRPC要求を送信するのにかかる時間と他のステップの期間が含まれます。

### Point_Get {#point-get}

`Point_Get`オペレーターからの実行情報には、通常、次の情報が含まれます。

-   `Get:{num_rpc:1, total_time:697.051µs}` ：TiKVに送信された`Get`のRPC要求の数（ `num_rpc` ）とすべてのRPC要求の合計期間（ `total_time` ）。
-   `ResolveLock:{num_rpc:1, total_time:12.117495ms}` ：TiDBがデータの読み取り中にロックに遭遇した場合、最初にロックを解決する必要があります。これは通常、読み取りと書き込みの競合のシナリオで発生します。この情報は、ロックを解決する期間を示します。
-   `regionMiss_backoff:{num:11, total_time:2010 ms},tikvRPC_backoff:{num:11, total_time:10691 ms}` ：RPC要求が失敗すると、TiDBは要求を再試行する前にバックオフ時間を待機します。バックオフ統計には、バックオフのタイプ（ `regionMiss`や`tikvRPC`など）、合計待機時間（ `total_time` ）、およびバックオフの合計数（ `num` ）が含まれます。

### Batch_Point_Get {#batch-point-get}

`Batch_Point_Get`オペレーターの実行情報は`Point_Get`オペレーターの実行情報と似ていますが、 `Batch_Point_Get`は通常`BatchGet`のRPC要求をTiKVに送信してデータを読み取ります。

`BatchGet:{num_rpc:2, total_time:83.13µs}` ：TiKVに送信された`BatchGet`種類のRPCリクエストの数（ `num_rpc` ）とすべてのRPCリクエストの合計消費時間（ `total_time` ）。

### TableReader {#tablereader}

`TableReader`オペレーターの実行情報は、通常、次のとおりです。

```
cop_task: {num: 6, max: 1.07587ms, min: 844.312µs, avg: 919.601µs, p95: 1.07587ms, max_proc_keys: 16, p95_proc_keys: 16, tot_proc: 1ms, tot_wait: 1ms, rpc_num: 6, rpc_time: 5.313996 ms, copr_cache_hit_ratio: 0.00}
```

-   `cop_task` ： `cop`のタスクの実行情報が含まれます。例えば：
    -   `num` ：警官タスクの数。
    -   `max` ： `min`タスクの実行に`avg`れた実行時間の最大値、最小値、平均値、および`p95`値。
    -   `max_proc_keys`および`p95_proc_keys` ：すべての警官タスクでTiKVによってスキャンされた最大およびP95キー値。最大値とP95値の差が大きい場合、データ分布が不均衡になる可能性があります。
    -   `rpc_num` ：TiKVに送信された`rpc_time` `Cop`のRPC要求に費やされた合計数と合計時間。
    -   `copr_cache_hit_ratio` ： `cop`のタスク要求に対するコプロセッサーキャッシュのヒット率。
-   `backoff` ：さまざまなタイプのバックオフとバックオフの合計待機時間が含まれます。

### 入れる {#insert}

`Insert`オペレーターの実行情報は、通常、次のとおりです。

```
prepare:109.616µs, check_insert:{total_time:1.431678ms, mem_insert_time:667.878µs, prefetch:763.8µs, rpc:{BatchGet:{num_rpc:1, total_time:699.166µs},Get:{num_rpc:1, total_time:378.276µs }}}
```

-   `prepare` ：式、デフォルト値、自動インクリメント値の計算など、書き込みの準備に費やされた時間。
-   `check_insert` ：この情報は通常、競合チェックやTiDBトランザクションキャッシュへのデータの書き込みにかかる時間を含め、 `insert ignore`および`insert on duplicate`のステートメントに表示されます。この時間の消費には、トランザクションのコミットに費やされた時間は含まれないことに注意してください。次の情報が含まれています。
    -   `total_time` ： `check_insert`ステップに費やされた合計時間。
    -   `mem_insert_time` ：TiDBトランザクションキャッシュへのデータの書き込みに費やされた時間。
    -   `prefetch` ：TiKVから競合をチェックする必要があるデータを取得する期間。このステップでは、データを取得するために2RPC要求を`Batch_Get`に送信します。
    -   `rpc` ：RPC要求をTiKVに送信するために消費された合計時間。これには、通常、 `BatchGet`と`Get`の2種類のRPC時間が含まれます。
        -   `BatchGet`要求は`prefetch`ステップで送信されます。
        -   `Get` `insert on duplicate`ステートメントが`duplicate update`を実行すると、RPC要求が送信されます。
-   `backoff` ：さまざまなタイプのバックオフとバックオフの合計待機時間が含まれます。

### IndexJoin {#indexjoin}

`IndexJoin`人のオペレーターには、同時実行のために1人の外部ワーカーとN人の内部ワーカーがいます。結合結果は、外部テーブルの順序を保持します。詳細な実行プロセスは次のとおりです。

1.  外部ワーカーはN個の外部行を読み取り、それをタスクにラップして、結果チャネルと内部ワーカーチャネルに送信します。
2.  内部ワーカーはタスクを受け取り、タスクからキー範囲を構築し、キー範囲に従って内部行をフェッチします。次に、内側の行のハッシュテーブルを作成します。
3.  メイン`IndexJoin`スレッドは、結果チャネルからタスクを受け取り、内部ワーカーがタスクの処理を終了するのを待ちます。
4.  メインの`IndexJoin`スレッドは、内側の行のハッシュテーブルを参照して、外側の各行を結合します。

`IndexJoin`演算子には、次の実行情報が含まれています。

```
inner:{total:4.297515932s, concurrency:5, task:17, construct:97.96291ms, fetch:4.164310088s, build:35.219574ms}, probe:53.574945ms
```

-   `Inner` ：内部ワーカーの実行情報：
    -   `total` ：内部ワーカーが消費した合計時間。
    -   `concurrency` ：同時内部ワーカーの数。
    -   `task` ：内部ワーカーによって処理されたタスクの総数。
    -   `construct` ：内部ワーカーがタスクに対応する内部テーブルの行を読み取る前の準備時間。
    -   `fetch` ：内部ワーカーが内部テーブルの行を読み取るのにかかる合計時間。
    -   `Build` ：内部ワーカーが対応する内部テーブル行のハッシュテーブルを構築するのにかかる合計時間。
-   `probe` ：メイン`IndexJoin`スレッドが外部テーブル行と内部テーブル行のハッシュテーブルとの結合操作を実行するために消費した合計時間。

### IndexHashJoin {#indexhashjoin}

`IndexHashJoin`演算子の実行プロセスは、 `IndexJoin`演算子の実行プロセスと同様です。 `IndexHashJoin`演算子には、1つの外部ワーカーとNの内部ワーカーが並行して実行されますが、出力順序が外部テーブルの順序と一致することは保証されていません。詳細な実行プロセスは次のとおりです。

1.  外部ワーカーはN個の外部行を読み取り、タスクを作成して、それを内部ワーカーチャネルに送信します。
2.  内部ワーカーは、内部ワーカー チャネルからタスクを受け取り、タスクごとに次の 3 つの操作を順番に実行します。 a. 外側の行からハッシュ テーブルを作成します。外側の行からキー範囲を構築し、内側の行をフェッチします c.ハッシュ テーブルをプローブし、結合結果を結果チャネルに送信します。注: ステップ a とステップ b は同時に実行されています。
3.  `IndexHashJoin`のメインスレッドは、結果チャネルから結合結果を受け取ります。

`IndexHashJoin`演算子には、次の実行情報が含まれています。

```sql
inner:{total:4.429220003s, concurrency:5, task:17, construct:96.207725ms, fetch:4.239324006s, build:24.567801ms, join:93.607362ms}
```

-   `Inner` ：内部ワーカーの実行情報：
    -   `total` ：内部ワーカーが消費した合計時間。
    -   `concurrency` ：内部ワーカーの数。
    -   `task` ：内部ワーカーによって処理されたタスクの総数。
    -   `construct` ：内部ワーカーが内部テーブルの行を読み取る前の準備時間。
    -   `fetch` ：内部ワーカーが内部テーブルの行を読み取るのに費やした合計時間。
    -   `Build` ：内部ワーカーが外部テーブル行のハッシュテーブルを構築するために費やした合計時間。
    -   `join` ：内部ワーカーが内部テーブル行および外部テーブル行のハッシュテーブルと結合するために消費された合計時間。

### HashJoin {#hashjoin}

`HashJoin`人のオペレーターには、内部ワーカー、外部ワーカー、およびN人の参加ワーカーがいます。詳細な実行プロセスは次のとおりです。

1.  内部ワーカーは内部テーブルの行を読み取り、ハッシュテーブルを作成します。
2.  外部ワーカーは外部テーブルの行を読み取り、それをタスクにラップして、結合ワーカーに送信します。
3.  結合ワーカーは、ステップ1のハッシュテーブルの構築が完了するのを待ちます。
4.  結合ワーカーは、タスク内の外部テーブル行とハッシュテーブルを使用して結合操作を実行し、結合結果を結果チャネルに送信します。
5.  `HashJoin`のメインスレッドは、結果チャネルから結合結果を受け取ります。

`HashJoin`演算子には、次の実行情報が含まれています。

```
build_hash_table:{total:146.071334ms, fetch:110.338509ms, build:35.732825ms}, probe:{concurrency:5, total:857.162518ms, max:171.48271ms, probe:125.341665ms, fetch:731.820853ms}
```

-   `build_hash_table` ：内部テーブルのデータを読み取り、ハッシュテーブルの実行情報を作成します。
    -   `total` ：合計時間消費。
    -   `fetch` ：内部テーブルデータの読み取りに費やされた合計時間。
    -   `build` ：ハッシュテーブルの作成に費やされた合計時間。
-   `probe` ：参加ワーカーの実行情報：
    -   `concurrency` ：参加ワーカーの数。
    -   `total` ：すべての参加ワーカーが消費した合計時間。
    -   `max` ：単一の結合ワーカーが実行する最長時間。
    -   `probe` ：外部テーブルの行とハッシュテーブルとの結合に費やされた合計時間。
    -   `fetch` ：結合ワーカーが外部テーブルの行データの読み取りを待機する合計時間。

### lock_keys実行情報 {#lock-keys-execution-information}

悲観的なトランザクションでDMLステートメントが実行される場合、オペレーターの実行情報には`lock_keys`の実行情報も含まれる場合があります。例えば：

```
lock_keys: {time:94.096168ms, region:6, keys:8, lock_rpc:274.503214ms, rpc_count:6}
```

-   `time` ： `lock_keys`の操作を実行する合計時間。
-   `region` ： `lock_keys`操作の実行に関係するリージョンの数。
-   `keys` ： `Lock`を必要とする`Key`の数。
-   `lock_rpc` ： `Lock`タイプのRPC要求をTiKVに送信するために費やされた合計時間。複数のRPC要求を並行して送信できるため、RPCの合計時間消費量は、 `lock_keys`の操作の合計時間消費量よりも大きくなる可能性があります。
-   `rpc_count` ：TiKVに送信された`Lock`タイプのRPCリクエストの総数。

### commit_txn実行情報 {#commit-txn-execution-information}

書き込みタイプのDMLステートメントが`autocommit=1`のトランザクションで実行される場合、書き込み演算子の実行情報には、トランザクションコミットの期間情報も含まれます。例えば：

```
commit_txn: {prewrite:48.564544ms, wait_prewrite_binlog:47.821579, get_commit_ts:4.277455ms, commit:50.431774ms, region_num:7, write_keys:16, write_byte:536}
```

-   `prewrite` ：トランザクションの2PCコミットの`prewrite`フェーズに費やされた時間。
-   `wait_prewrite_binlog:` ：Binlogの書き込みを待機するために費やされた時間。
-   `get_commit_ts` ：トランザクションコミットタイムスタンプの取得に費やされた時間。
-   `commit` ：トランザクションの2PCコミット中に`commit`フェーズに費やされた時間。
-   `write_keys` ：トランザクションに書き込まれた合計`keys` 。
-   `write_byte` ：トランザクションに書き込まれた`key-value`の合計バイト数で、単位はバイトです。

### その他の一般的な実行情報 {#other-common-execution-information}

コプロセッサー演算子には通常、実行時間情報の2つの部分（ `cop_task`と`tikv_task` ）が含まれています。 `cop_task`はTiDBによって記録された時間であり、要求がサーバーに送信された瞬間から応答が受信された瞬間までです。 `tikv_task`は、TiKVコプロセッサー自体によって記録された時間です。 2つの間に大きな違いがある場合は、応答の待機に費やされた時間が長すぎるか、gRPCまたはネットワークに費やされた時間が長すぎることを示している可能性があります。

## MySQLの互換性 {#mysql-compatibility}

`EXPLAIN ANALYZE`はMySQL8.0の機能ですが、TiDBの出力形式と潜在的な実行プランはどちらもMySQLとは大幅に異なります。

## も参照してください {#see-also}

-   [クエリ実行プランを理解する](/explain-overview.md)
-   [EXPLAIN](/sql-statements/sql-statement-explain.md)
-   [テーブルの分析](/sql-statements/sql-statement-analyze-table.md)
-   [痕跡](/sql-statements/sql-statement-trace.md)
