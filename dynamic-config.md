---
title: Modify Configuration Dynamically
summary: クラスター構成を動的に変更する方法を学習します。
---

# コンフィグレーションを動的に変更する {#modify-configuration-dynamically}

このドキュメントでは、クラスター構成を動的に変更する方法について説明します。

クラスタコンポーネントを再起動することなく、SQL文を使用してコンポーネント（TiDB、TiKV、PDを含む）の構成を動的に更新できます。現在、TiDBインスタンスの構成変更方法は、他のコンポーネント（TiKVやPDなど）の構成変更方法とは異なります。

> **注記：**
>
> この機能はTiDB Self-Managedにのみ適用され、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)では利用できません。TiDB TiDB Cloudの場合は、設定を変更するには[TiDB Cloudサポート](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)お問い合わせください。

## 一般的な操作 {#common-operations}

このセクションでは、構成を動的に変更する一般的な操作について説明します。

### インスタンス構成のビュー {#view-instance-configuration}

クラスター内のすべてのインスタンスの構成を表示するには、 `show config`ステートメントを使用します。結果は次のようになります。

```sql
show config;
```

```sql
+------+-----------------+-----------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Type | Instance        | Name                                                      | Value                                                                                                                                                                                                                                                                            |
+------+-----------------+-----------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| tidb | 127.0.0.1:4001  | advertise-address                                         | 127.0.0.1                                                                                                                                                                                                                                                                        |
| tidb | 127.0.0.1:4001  | binlog.binlog-socket                                      |                                                                                                                                                                                                                                                                                  |
| tidb | 127.0.0.1:4001  | binlog.enable                                             | false                                                                                                                                                                                                                                                                            |
| tidb | 127.0.0.1:4001  | binlog.ignore-error                                       | false                                                                                                                                                                                                                                                                            |
| tidb | 127.0.0.1:4001  | binlog.strategy                                           | range                                                                                                                                                                                                                                                                            |
| tidb | 127.0.0.1:4001  | binlog.write-timeout                                      | 15s                                                                                                                                                                                                                                                                              |
| tidb | 127.0.0.1:4001  | check-mb4-value-in-utf8                                   | true                                                                                                                                                                                                                                                                             |

...
```

結果をフィールドでフィルタリングできます。例:

```sql
show config where type='tidb'
show config where instance in (...)
show config where name like '%log%'
show config where type='tikv' and name='log.level'
```

### TiKV 構成を動的に変更する {#modify-tikv-configuration-dynamically}

> **注記：**
>
> -   TiKV設定項目を動的に変更すると、TiKV設定ファイルは自動的に更新されます。ただし、 `tiup edit-config`実行して対応する設定項目も変更する必要があります。そうしないと、 `upgrade`や`reload`などの操作によって変更内容が上書きされてしまいます。設定項目の変更方法の詳細については、 [TiUPを使用して構成を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration)を参照してください。
> -   `tiup edit-config`実行した後、 `tiup reload`実行する必要はありません。

`set config`ステートメントを使用すると、インスタンス アドレスまたはコンポーネントタイプに応じて、単一のインスタンスまたはすべてのインスタンスの構成を変更できます。

-   すべての TiKV インスタンスの構成を変更します。

> **注記：**
>
> 変数名はバッククォートで囲むことをお勧めします。

```sql
set config tikv `split.qps-threshold`=1000;
```

-   単一の TiKV インスタンスの構成を変更します。

    ```sql
    set config "127.0.0.1:20180" `split.qps-threshold`=1000;
    ```

変更が成功した場合、 `Query OK`が返されます。

```sql
Query OK, 0 rows affected (0.01 sec)
```

バッチ変更中にエラーが発生した場合は、警告が返されます。

```sql
set config tikv `log-level`='warn';
```

```sql
Query OK, 0 rows affected, 1 warning (0.04 sec)
```

```sql
show warnings;
```

```sql
+---------+------+---------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                       |
+---------+------+---------------------------------------------------------------------------------------------------------------+
| Warning | 1105 | bad request to http://127.0.0.1:20180/config: fail to update, error: "config log-level can not be changed" |
+---------+------+---------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

バッチ変更はアトミック性を保証するものではありません。一部のインスタンスでは変更が成功し、他のインスタンスでは失敗する可能性があります。1 `set tikv key=val`使用して TiKV クラスター全体の設定を変更した場合、一部のインスタンスでは変更が失敗する可能性があります。3 `show warnings`使用して結果を確認できます。

変更が失敗した場合は、該当するステートメントを再実行するか、失敗したインスタンスを個別に変更する必要があります。ネットワークの問題やマシンの障害により一部のTiKVインスタンスにアクセスできない場合は、復旧後にこれらのインスタンスを変更してください。

設定項目の変更に成功した場合、その結果は設定ファイルに保存され、以降の操作に反映されます。一部の設定項目の名前は、 `limit`や`key`など、TiDBの予約語と競合する場合があります。これらの設定項目は、バッククォート`` ` ``で囲んでください。例： `` `raftstore.raft-log-gc-size-limit` `` 。

次の TiKV 構成項目は動的に変更できます。

| コンフィグレーション項目                                              | 説明                                                                                                                                        |
| :-------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------- |
| ログレベル                                                     | ログ レベル。                                                                                                                                   |
| `raftstore.raft-max-inflight-msgs`                        | 確認するRaftログの数。この数を超えると、 Raftステートマシンはログ送信を遅くします。                                                                                            |
| `raftstore.raft-log-gc-tick-interval`                     | Raftログを削除するポーリングタスクがスケジュールされる時間間隔                                                                                                         |
| `raftstore.raft-log-gc-threshold`                         | 残存Raftログの最大許容数に関するソフト制限                                                                                                                   |
| `raftstore.raft-log-gc-count-limit`                       | 許容される残存Raftログ数のハードリミット                                                                                                                    |
| `raftstore.raft-log-gc-size-limit`                        | 残余Raftの許容サイズに関する厳密な制限                                                                                                                     |
| `raftstore.raft-max-size-per-msg`                         | 生成できる単一のメッセージパケットのサイズのソフト制限                                                                                                               |
| `raftstore.raft-entry-max-size`                           | 単一のRaftログの最大サイズに対するハード制限                                                                                                                  |
| `raftstore.raft-entry-cache-life-time`                    | メモリ内のログキャッシュに許容される最大残り時間                                                                                                                  |
| `raftstore.max-apply-unpersisted-log-limit`               | コミットされたが永続化されていないRaftログの最大数を適用できます                                                                                                        |
| `raftstore.split-region-check-tick-interval`              | リージョン分割が必要かどうかを確認する時間間隔                                                                                                                   |
| `raftstore.region-split-check-diff`                       | リージョン分割前にリージョンデータが超過できる最大値                                                                                                                |
| `raftstore.pd-heartbeat-tick-interval`                    | PDへのリージョンのハートビートがトリガーされる時間間隔                                                                                                              |
| `raftstore.pd-store-heartbeat-tick-interval`              | 店舗のPDへのハートビートがトリガーされる時間間隔                                                                                                                 |
| `raftstore.snap-mgr-gc-tick-interval`                     | 期限切れのスナップショットファイルのリサイクルがトリガーされる時間間隔                                                                                                       |
| `raftstore.snap-gc-timeout`                               | スナップショットファイルが保存される最長時間                                                                                                                    |
| `raftstore.lock-cf-compact-interval`                      | TiKVがロックカラムファミリーの手動圧縮をトリガーする時間間隔                                                                                                          |
| `raftstore.lock-cf-compact-bytes-threshold`               | TiKVがロックカラムファミリーの手動圧縮をトリガーするサイズ                                                                                                           |
| `raftstore.messages-per-tick`                             | バッチごとに処理されるメッセージの最大数                                                                                                                      |
| `raftstore.max-peer-down-duration`                        | ピアに許可される最長の非アクティブ期間                                                                                                                       |
| `raftstore.max-leader-missing-duration`                   | ピアがリーダーなしでいられる最長時間。この値を超えると、ピアはPDを使用して、自身が削除されたかどうかを確認します。                                                                                |
| `raftstore.abnormal-leader-missing-duration`              | ピアがリーダーなしで待機できる通常の期間。この値を超えると、ピアは異常とみなされ、メトリックとログにマークされます。                                                                                |
| `raftstore.peer-stale-state-check-interval`               | ピアにリーダーがいないかどうかを確認する時間間隔                                                                                                                  |
| `raftstore.consistency-check-interval`                    | 一貫性をチェックする時間間隔（TiDB のガベージコレクションと互換性がないため、推奨さ**れません**）                                                                                     |
| `raftstore.raft-store-max-leader-lease`                   | Raftリーダーの最も長い信頼期間                                                                                                                         |
| `raftstore.merge-check-tick-interval`                     | マージチェックの時間間隔                                                                                                                              |
| `raftstore.cleanup-import-sst-interval`                   | 期限切れのSSTファイルをチェックする時間間隔                                                                                                                   |
| `raftstore.local-read-batch-size`                         | 1バッチで処理される読み取り要求の最大数                                                                                                                      |
| `raftstore.apply-yield-write-size`                        | Applyスレッドが各ラウンドで1つのFSM（有限状態マシン）に書き込むことができる最大バイト数                                                                                          |
| `raftstore.hibernate-timeout`                             | 起動時に休止状態に入るまでの最短待機時間。この時間内は、TiKV は休止状態になりません（解放されません）。                                                                                    |
| `raftstore.apply-pool-size`                               | ディスクにデータをフラッシュするプール内のスレッドの数。これは適用スレッド プールのサイズです。                                                                                          |
| `raftstore.store-pool-size`                               | Raftを処理するプール内のスレッドの数。これはRaftstoreスレッドプールのサイズです。                                                                                           |
| `raftstore.apply-max-batch-size`                          | Raftステートマシンは、BatchSystemによってデータ書き込みリクエストをバッチ処理します。この設定項目は、1バッチでリクエストを実行できるRaftステートマシンの最大数を指定します。                                          |
| `raftstore.store-max-batch-size`                          | Raftステートマシンは、BatchSystemによってログをディスクにフラッシュするリクエストをバッチ処理します。この設定項目は、1回のバッチ処理でリクエストを処理できるRaftステートマシンの最大数を指定します。                              |
| `raftstore.store-io-pool-size`                            | Raft I/Oタスクを処理するスレッドの数。これはStoreWriterスレッドプールのサイズでもあります（この値を0以外の値から0に変更したり、0から0以外の値に変更し**たりしないでください**）。                                    |
| `raftstore.periodic-full-compact-start-max-cpu`           | 完全圧縮が有効な場合に TiKV が定期的に完全圧縮を実行する CPU 使用率のしきい値                                                                                              |
| `readpool.unified.max-thread-count`                       | 読み取り要求を均一に処理するスレッド プール内のスレッドの最大数。これは、UnifyReadPool スレッド プールのサイズです。                                                                        |
| `readpool.unified.max-tasks-per-worker`                   | 統合読み取りプール内の 1 つのスレッドに許可されるタスクの最大数。値を超えると`Server Is Busy`エラーが返されます。                                                                        |
| `readpool.unified.auto-adjust-pool-size`                  | UnifyReadPool スレッド プールのサイズを自動的に調整するかどうかを決定します                                                                                             |
| `resource-control.priority-ctl-strategy`                  | 低優先度タスクのフロー制御戦略を構成します。                                                                                                                    |
| `coprocessor.split-region-on-table`                       | テーブルごとにリージョンを分割できます                                                                                                                       |
| `coprocessor.batch-split-limit`                           | バッチでのリージョン分割のしきい値                                                                                                                         |
| `coprocessor.region-max-size`                             | リージョンの最大サイズ                                                                                                                               |
| `coprocessor.region-split-size`                           | 新しく分割されたリージョンのサイズ                                                                                                                         |
| `coprocessor.region-max-keys`                             | リージョンで許可されるキーの最大数                                                                                                                         |
| `coprocessor.region-split-keys`                           | 新しく分割されたリージョン内のキーの数                                                                                                                       |
| `pessimistic-txn.wait-for-lock-timeout`                   | 悲観的トランザクションがロックを待つ最長時間                                                                                                                    |
| `pessimistic-txn.wake-up-delay-duration`                  | 悲観的トランザクションが起動されるまでの期間                                                                                                                    |
| `pessimistic-txn.pipelined`                               | パイプライン化された悲観的ロック処理を有効にするかどうかを決定します                                                                                                        |
| `pessimistic-txn.in-memory`                               | メモリ内の悲観的ロックを有効にするかどうかを決定します                                                                                                               |
| `pessimistic-txn.in-memory-peer-size-limit`               | リージョン内のメモリ内悲観的ロックのメモリ使用量制限を制御します                                                                                                          |
| `pessimistic-txn.in-memory-instance-size-limit`           | TiKVインスタンス内のメモリ内悲観的ロックのメモリ使用量制限を制御します                                                                                                     |
| `quota.foreground-cpu-time`                               | TiKVフォアグラウンドが読み取りおよび書き込み要求を処理するために使用するCPUリソースのソフト制限                                                                                       |
| `quota.foreground-write-bandwidth`                        | フォアグラウンドトランザクションがデータを書き込む帯域幅のソフト制限                                                                                                        |
| `quota.foreground-read-bandwidth`                         | フォアグラウンドトランザクションとコプロセッサーがデータを読み取る帯域幅のソフト制限                                                                                                |
| `quota.background-cpu-time`                               | TiKV バックグラウンドで読み取りおよび書き込み要求を処理するために使用する CPU リソースのソフト制限                                                                                    |
| `quota.background-write-bandwidth`                        | バックグラウンドトランザクションがデータを書き込む帯域幅のソフト制限                                                                                                        |
| `quota.background-read-bandwidth`                         | バックグラウンドトランザクションとコプロセッサーがデータを読み取る帯域幅のソフト制限                                                                                                |
| `quota.enable-auto-tune`                                  | クォータの自動調整を有効にするかどうか。この設定項目を有効にすると、TiKV インスタンスの負荷に基づいて、バックグラウンドリクエストのクォータが動的に調整されます。                                                       |
| `quota.max-delay-duration`                                | 単一の読み取りまたは書き込み要求がフォアグラウンドで処理されるまでに強制的に待機される最大時間                                                                                           |
| `gc.ratio-threshold`                                      | リージョンGCがスキップされるしきい値（GCバージョン数/キー数）                                                                                                         |
| `gc.batch-keys`                                           | 1バッチで処理されるキーの数                                                                                                                            |
| `gc.max-write-bytes-per-sec`                              | RocksDBに1秒あたり書き込める最大バイト数                                                                                                                  |
| `gc.enable-compaction-filter`                             | 圧縮フィルタを有効にするかどうか                                                                                                                          |
| `gc.compaction-filter-skip-version-check`                 | 圧縮フィルタのクラスタバージョンチェックをスキップするかどうか（未リリース）                                                                                                    |
| `gc.auto-compaction.check-interval`                       | TiKVが自動（RocksDB）圧縮をトリガーするかどうかを確認する間隔                                                                                                      |
| `gc.auto-compaction.tombstone-num-threshold`              | TiKV自動（RocksDB）圧縮をトリガーするために必要なRocksDBトゥームストーンの数                                                                                           |
| `gc.auto-compaction.tombstone-percent-threshold`          | TiKV自動（RocksDB）圧縮をトリガーするために必要なRocksDBトゥームストーンの割合                                                                                          |
| `gc.auto-compaction.redundant-rows-threshold`             | TiKV自動（RocksDB）圧縮をトリガーするために必要な冗長MVCC行の数                                                                                                   |
| `gc.auto-compaction.redundant-rows-percent-threshold`     | TiKV自動（RocksDB）圧縮をトリガーするために必要な冗長MVCC行の割合                                                                                                  |
| `gc.auto-compaction.bottommost-level-force`               | RocksDB の最下層ファイルの圧縮を強制するかどうか                                                                                                              |
| `{db-name}.max-total-wal-size`                            | 合計WALの最大サイズ                                                                                                                               |
| `{db-name}.max-background-jobs`                           | RocksDBのバックグラウンドスレッドの数                                                                                                                    |
| `{db-name}.max-background-flushes`                        | RocksDBのフラッシュスレッドの最大数                                                                                                                     |
| `{db-name}.max-open-files`                                | RocksDBが開くことができるファイルの総数                                                                                                                   |
| `{db-name}.compaction-readahead-size`                     | 圧縮時のサイズ`readahead`                                                                                                                        |
| `{db-name}.bytes-per-sync`                                | ファイルが非同期的に書き込まれている間に、OSがファイルをディスクに増分的に同期する速度                                                                                              |
| `{db-name}.wal-bytes-per-sync`                            | WALファイルが書き込まれている間にOSがWALファイルをディスクに増分的に同期する速度                                                                                              |
| `{db-name}.writable-file-max-buffer-size`                 | WritableFileWriteで使用される最大バッファサイズ                                                                                                          |
| `{db-name}.{cf-name}.block-cache-size`                    | ブロックのキャッシュサイズ                                                                                                                             |
| `{db-name}.{cf-name}.write-buffer-size`                   | メンバテーブルのサイズ                                                                                                                               |
| `{db-name}.{cf-name}.max-write-buffer-number`             | メンバーテーブルの最大数                                                                                                                              |
| `{db-name}.{cf-name}.max-bytes-for-level-base`            | ベースレベル（L1）の最大バイト数                                                                                                                         |
| `{db-name}.{cf-name}.target-file-size-base`               | ベースレベルのターゲットファイルのサイズ                                                                                                                      |
| `{db-name}.{cf-name}.level0-file-num-compaction-trigger`  | 圧縮をトリガーするL0のファイルの最大数                                                                                                                      |
| `{db-name}.{cf-name}.level0-slowdown-writes-trigger`      | 書き込み停止を引き起こす L0 のファイルの最大数                                                                                                                 |
| `{db-name}.{cf-name}.level0-stop-writes-trigger`          | 書き込みを完全にブロックするL0のファイルの最大数                                                                                                                 |
| `{db-name}.{cf-name}.max-compaction-bytes`                | 圧縮ごとにディスクに書き込まれる最大バイト数                                                                                                                    |
| `{db-name}.{cf-name}.max-bytes-for-level-multiplier`      | 各レイヤーのデフォルトの増幅倍数                                                                                                                          |
| `{db-name}.{cf-name}.disable-auto-compactions`            | 自動圧縮を有効または無効にする                                                                                                                           |
| `{db-name}.{cf-name}.soft-pending-compaction-bytes-limit` | 保留中の圧縮バイトのソフト制限                                                                                                                           |
| `{db-name}.{cf-name}.hard-pending-compaction-bytes-limit` | 保留中の圧縮バイトのハード制限                                                                                                                           |
| `{db-name}.{cf-name}.titan.blob-run-mode`                 | BLOBファイルの処理モード                                                                                                                            |
| `{db-name}.{cf-name}.titan.min-blob-size`                 | Titan にデータが保存されるしきい値。このしきい値に達すると、データは Titan BLOB ファイルに保存されます。                                                                             |
| `{db-name}.{cf-name}.titan.blob-file-compression`         | Titan BLOBファイルで使用される圧縮アルゴリズム                                                                                                              |
| `{db-name}.{cf-name}.titan.discardable-ratio`             | Titanデータファイル内のGC実行時の不要データ比率のしきい値。BLOBファイル内の不要データ比率がこのしきい値を超えると、Titan GCがトリガーされます。                                                         |
| `server.grpc-memory-pool-quota`                           | gRPC で使用できるメモリサイズを制限します                                                                                                                   |
| `server.max-grpc-send-msg-len`                            | 送信できる gRPC メッセージの最大長を設定します                                                                                                                |
| `server.snap-io-max-bytes-per-sec`                        | スナップショットを処理するときに許容される最大ディスク帯域幅を設定します                                                                                                      |
| `server.concurrent-send-snap-limit`                       | 同時に送信されるスナップショットの最大数を設定します                                                                                                                |
| `server.concurrent-recv-snap-limit`                       | 同時に受信するスナップショットの最大数を設定します                                                                                                                 |
| `server.raft-msg-max-batch-size`                          | 1つのgRPCメッセージに含まれるRaftメッセージの最大数を設定します                                                                                                      |
| `server.simplify-metrics`                                 | サンプリング監視メトリックを簡素化するかどうかを制御します                                                                                                             |
| `storage.block-cache.capacity`                            | 共有ブロックキャッシュのサイズ（v4.0.3以降でサポート）                                                                                                            |
| storage.フロー制御.有効                                          | フロー制御メカニズムを有効にするかどうかを決定します                                                                                                                |
| storage.フロー制御.memtables-threshold                         | フロー制御をトリガーするkvDBメモリテーブルの最大数                                                                                                               |
| storage.フロー制御.l0-ファイルしきい値                                 | フロー制御をトリガーするkvDB L0ファイルの最大数                                                                                                               |
| storage.フロー制御.ソフト保留圧縮バイト制限                                | フロー制御メカニズムが一部の書き込み要求を拒否するトリガーとなる、kvDB 保留圧縮バイトのしきい値                                                                                        |
| storage.フロー制御.ハード保留コンパクションバイト制限                           | フロー制御メカニズムがすべての書き込み要求を拒否するトリガーとなる、kvDB 保留圧縮バイトのしきい値                                                                                       |
| `storage.scheduler-worker-pool-size`                      | スケジューラスレッドプール内のスレッド数                                                                                                                      |
| `import.num-threads`                                      | 復元またはインポート RPC 要求を処理するスレッドの数 (v8.1.2 以降では動的な変更がサポートされています)                                                                                |
| `backup.num-threads`                                      | バックアップ スレッドの数 (v4.0.3 以降でサポート)                                                                                                            |
| `split.qps-threshold`                                     | リージョンで`load-base-split`実行するしきい値。リージョンの読み取りリクエストのQPSが10秒連続で`qps-threshold`超える場合、このリージョンは分割されます。                                            |
| `split.byte-threshold`                                    | リージョンで`load-base-split`実行するためのしきい値。リージョンの読み取りリクエストのトラフィックが10秒間連続して`byte-threshold`超える場合、このリージョンは分割されます。                                   |
| `split.region-cpu-overload-threshold-ratio`               | リージョンで`load-base-split`実行するためのしきい値。リージョンの統合読み取りプールのCPU使用率が10秒連続で`region-cpu-overload-threshold-ratio`超えた場合、このリージョンは分割されます。(v6.2.0以降でサポート) |
| `split.split-balance-score`                               | `load-base-split`というパラメータは、2つの分割されたリージョンの負荷が可能な限り均等になるようにします。値が小さいほど、負荷は均等になります。ただし、値が小さすぎると分割が失敗する可能性があります。                              |
| `split.split-contained-score`                             | パラメータは`load-base-split`です。値が小さいほど、リージョン分割後の地域間訪問数が少なくなります。                                                                                |
| `cdc.min-ts-interval`                                     | 解決されたTSが転送される時間間隔                                                                                                                         |
| `cdc.old-value-cache-memory-quota`                        | TiCDC 古い値のエントリが占有するメモリの上限                                                                                                                 |
| `cdc.sink-memory-quota`                                   | TiCDCデータ変更イベントが占有するメモリの上限                                                                                                                 |
| `cdc.incremental-scan-speed-limit`                        | 履歴データの増分スキャン速度の上限                                                                                                                         |
| `cdc.incremental-scan-concurrency`                        | 履歴データの同時増分スキャンタスクの最大数                                                                                                                     |

上記の表で、プレフィックスが`{db-name}`または`{db-name}.{cf-name}`パラメータはRocksDB関連の設定です。5のオプション値は`db-name`と`raftdb` `rocksdb` 。

-   `db-name`が`rocksdb`場合、 `cf-name`のオプションの値は`defaultcf` 、 `writecf` 、 `lockcf` 、 `raftcf`です。
-   `db-name`が`raftdb`とき、 `cf-name`の値は`defaultcf`なります。

詳細なパラメータの説明については[TiKVコンフィグレーションファイル](/tikv-configuration-file.md)を参照してください。

### PD構成を動的に変更する {#modify-pd-configuration-dynamically}

現在、PD はインスタンスごとに個別の設定をサポートしていません。すべての PD インスタンスは同じ設定を共有します。

次のステートメントを使用して PD 構成を変更できます。

```sql
set config pd `log.level`='info';
```

変更が成功した場合、 `Query OK`が返されます。

```sql
Query OK, 0 rows affected (0.01 sec)
```

設定項目が正常に変更された場合、その結果は設定ファイルではなくetcdに保存されます。以降の操作ではetcdの設定が優先されます。一部の設定項目の名前はTiDBの予約語と競合する場合があります。これらの設定項目は、バッククォート`` ` ``で囲んでください。例： `` `schedule.leader-schedule-limit` ``

次の PD 構成項目は動的に変更できます。

| コンフィグレーション項目                                         | 説明                                                         |
| :--------------------------------------------------- | :--------------------------------------------------------- |
| `log.level`                                          | ログレベル                                                      |
| `cluster-version`                                    | クラスターバージョン                                                 |
| `schedule.max-merge-region-size`                     | `Region Merge` （MiB単位）のサイズ制限を制御します                         |
| `schedule.max-merge-region-keys`                     | `Region Merge`キーの最大数を指定します                                 |
| `schedule.patrol-region-interval`                    | チェッカーがリージョンのヘルス状態を検査する頻度を決定します                             |
| `schedule.split-merge-interval`                      | 同じリージョンで分割および結合操作を実行する時間間隔を決定します                           |
| `schedule.max-snapshot-count`                        | 単一のストアが同時に送受信できるスナップショットの最大数を決定します                         |
| `schedule.max-pending-peer-count`                    | 単一ストア内の保留中のピアの最大数を決定します                                    |
| `schedule.max-store-down-time`                       | PDが切断されたストアを回復できないと判断するまでのダウンタイム                           |
| `schedule.max-store-preparing-time`                  | ストアがオンラインになるまでの最大待ち時間を制御します                                |
| `schedule.leader-schedule-policy`                    | Leaderのスケジュールポリシーを決定する                                     |
| `schedule.leader-schedule-limit`                     | 同時に実行されるLeaderスケジュールタスクの数                                  |
| `schedule.region-schedule-limit`                     | 同時に実行されるリージョンスケジュールタスクの数                                   |
| `schedule.replica-schedule-limit`                    | 同時に実行されるレプリカスケジュールタスクの数                                    |
| `schedule.merge-schedule-limit`                      | 同時に実行される`Region Merge`スケジュールタスクの数                          |
| `schedule.hot-region-schedule-limit`                 | 同時に実行されるホットリージョンスケジューリングタスクの数                              |
| `schedule.hot-region-cache-hits-threshold`           | リージョンがホットスポットとみなされる閾値を決定します                                |
| `schedule.high-space-ratio`                          | 店舗の収容能力が十分である閾値比率                                          |
| `schedule.low-space-ratio`                           | 店舗の収容能力が不足する閾値比率                                           |
| `schedule.tolerant-size-ratio`                       | `balance`バッファサイズを制御します                                     |
| `schedule.enable-remove-down-replica`                | `DownReplica`自動的に削除する機能を有効にするかどうかを決定します                    |
| `schedule.enable-replace-offline-replica`            | `OfflineReplica`移行する機能を有効にするかどうかを決定します                     |
| `schedule.enable-make-up-replica`                    | レプリカを自動的に補完する機能を有効にするかどうかを決定します                            |
| `schedule.enable-remove-extra-replica`               | 余分なレプリカを削除する機能を有効にするかどうかを決定します                             |
| `schedule.enable-location-replacement`               | 分離レベルチェックを有効にするかどうかを決定します                                  |
| `schedule.enable-cross-table-merge`                  | テーブル間の結合を有効にするかどうかを決定します                                   |
| `schedule.enable-one-way-merge`                      | 一方向のマージを有効にします。これにより、隣接する次のリージョンとのマージのみが可能になります。           |
| `schedule.region-score-formula-version`              | リージョンスコアの計算式のバージョンを制御します                                   |
| `schedule.scheduler-max-waiting-operator`            | 各スケジューラの待機オペレータの数を制御します                                    |
| `schedule.enable-debug-metrics`                      | デバッグ用のメトリクスを有効にする                                          |
| `schedule.enable-heartbeat-concurrent-runner`        | リージョンハートビートの非同期並行処理を有効にする                                  |
| `schedule.enable-heartbeat-breakdown-metrics`        | リージョンハートビートの内訳メトリックを有効にして、リージョンハートビート処理の各段階で消費された時間を測定します。 |
| `schedule.enable-joint-consensus`                    | レプリカのスケジュールにジョイントコンセンサスを使用するかどうかを制御します                     |
| `schedule.hot-regions-write-interval`                | PDがホットリージョン情報を保存する時間間隔                                     |
| `schedule.hot-regions-reserved-days`                 | ホットリージョン情報を保持する日数を指定します                                    |
| `schedule.max-movable-hot-peer-size`                 | ホットリージョンスケジューリングにスケジュールできる最大リージョンサイズを制御します。                |
| `schedule.store-limit-version`                       | [店舗制限](/configure-store-limit.md)のバージョンを制御します              |
| `schedule.patrol-region-worker-count`                | リージョンのヘルス状態を検査するときにチェッカーによって作成される同時オペレータの数を制御します           |
| `replication.max-replicas`                           | レプリカの最大数を設定する                                              |
| `replication.location-labels`                        | TiKVクラスタのトポロジ情報                                            |
| `replication.enable-placement-rules`                 | 配置ルールを有効にする                                                |
| `replication.strictly-match-label`                   | ラベルチェックを有効にする                                              |
| `replication.isolation-level`                        | TiKVクラスタの最小トポロジカル分離レベル                                     |
| `pd-server.use-region-storage`                       | 独立したリージョンstorageを有効にする                                     |
| `pd-server.max-gap-reset-ts`                         | タイムスタンプをリセットする最大間隔を設定します（BR）                               |
| `pd-server.key-type`                                 | クラスタキータイプを設定する                                             |
| `pd-server.metric-storage`                           | クラスターメトリックのstorageアドレスを設定します                               |
| `pd-server.dashboard-address`                        | ダッシュボードのアドレスを設定する                                          |
| `pd-server.flow-round-by-digit`                      | リージョンフロー情報を丸める最下位桁数を指定します                                  |
| `pd-server.min-resolved-ts-persistence-interval`     | 最小解決タイムスタンプがPDに永続的に保存される間隔を決定します。                          |
| `pd-server.server-memory-limit`                      | PDインスタンスのメモリ制限比率                                           |
| `pd-server.server-memory-limit-gc-trigger`           | PDがGCをトリガーしようとする閾値比率                                       |
| `pd-server.enable-gogc-tuner`                        | GOGCチューナーを有効にするかどうかを制御します                                  |
| `pd-server.gc-tuner-threshold`                       | GOGCのチューニングにおける最大メモリ閾値比                                    |
| `replication-mode.replication-mode`                  | バックアップモードを設定します                                            |
| `replication-mode.dr-auto-sync.label-key`            | 異なるAZを区別し、配置ルールに一致させる必要がある                                 |
| `replication-mode.dr-auto-sync.primary`              | プライマリAZ                                                    |
| `replication-mode.dr-auto-sync.dr`                   | 災害復旧（DR）AZ                                                 |
| `replication-mode.dr-auto-sync.primary-replicas`     | プライマリ AZ 内の Voter レプリカの数                                   |
| `replication-mode.dr-auto-sync.dr-replicas`          | 災害復旧（DR）AZ内の投票者レプリカの数                                      |
| `replication-mode.dr-auto-sync.wait-store-timeout`   | ネットワークの分離や障害が発生したときに非同期レプリケーションモードに切り替えるまでの待機時間            |
| `replication-mode.dr-auto-sync.wait-recover-timeout` | ネットワークが回復した後、 `sync-recover`状態に戻るまでの待機時間                   |
| `replication-mode.dr-auto-sync.pause-region-split`   | `async_wait`と`async`ステータスでリージョン分割操作を一時停止するかどうかを制御します       |

詳細なパラメータの説明については[PDコンフィグレーションファイル](/pd-configuration-file.md)を参照してください。

### TiDB 構成を動的に変更する {#modify-tidb-configuration-dynamically}

現在、TiDB構成の変更方法は、TiKVおよびPD構成の変更方法とは異なります。1 [システム変数](/system-variables.md)使用してTiDB構成を変更できます。

次の例は、 `tidb_slow_log_threshold`変数を使用して`slow-threshold`動的に変更する方法を示しています。

デフォルト値は`slow-threshold`で 300 ミリ秒です。 `tidb_slow_log_threshold`使用すると 200 ミリ秒に設定できます。

```sql
set tidb_slow_log_threshold = 200;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

```sql
select @@tidb_slow_log_threshold;
```

```sql
+---------------------------+
| @@tidb_slow_log_threshold |
+---------------------------+
| 200                       |
+---------------------------+
1 row in set (0.00 sec)
```

次の TiDB 構成項目は動的に変更できます。

| コンフィグレーション項目                                            | SQL変数                                        | 説明                                                                                    |
| ------------------------------------------------------- | -------------------------------------------- | ------------------------------------------------------------------------------------- |
| `instance.tidb_enable_slow_log`                         | `tidb_enable_slow_log`                       | スローログを有効にするかどうかを制御します                                                                 |
| `instance.tidb_slow_log_threshold`                      | `tidb_slow_log_threshold`                    | スローログのしきい値を指定します                                                                      |
| `instance.tidb_expensive_query_time_threshold`          | `tidb_expensive_query_time_threshold`        | 高価なクエリのしきい値を指定します                                                                     |
| `instance.tidb_enable_collect_execution_info`           | `tidb_enable_collect_execution_info`         | オペレータの実行情報を記録するかどうかを制御します                                                             |
| `instance.tidb_record_plan_in_slow_log`                 | `tidb_record_plan_in_slow_log`               | 実行計画をスローログに記録するかどうかを制御します                                                             |
| `instance.tidb_force_priority`                          | `tidb_force_priority`                        | この TiDB インスタンスから送信されるステートメントの優先順位を指定します                                               |
| `instance.max_connections`                              | `max_connections`                            | この TiDB インスタンスに許可される同時接続の最大数を指定します                                                    |
| `instance.tidb_enable_ddl`                              | `tidb_enable_ddl`                            | この TiDB インスタンスが DDL 所有者になれるかどうかを制御します                                                 |
| `pessimistic-txn.constraint-check-in-place-pessimistic` | `tidb_constraint_check_in_place_pessimistic` | ユニークインデックスのユニーク制約チェックを、このインデックスが次にロックを必要とするときまで延期するか、トランザクションがコミットされるときまで延期するかを制御します。 |

### TiFlash構成を動的に変更する {#modify-tiflash-configuration-dynamically}

現在、システム変数[`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610)を使用してTiFlash構成`max_threads`変更できます。この変数は、 TiFlash が要求を実行するための最大同時実行性を指​​定します。

デフォルト値は`tidb_max_tiflash_threads` `-1` 、このシステム変数は無効であり、 TiFlash設定ファイルの設定に依存することを示します。 `tidb_max_tiflash_threads`使用すると、 `max_threads`から 10 に設定できます。

```sql
set tidb_max_tiflash_threads = 10;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

```sql
select @@tidb_max_tiflash_threads;
```

```sql
+----------------------------+
| @@tidb_max_tiflash_threads |
+----------------------------+
| 10                         |
+----------------------------+
1 row in set (0.00 sec)
```
