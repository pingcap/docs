---
title: Modify Configuration Dynamically
summary: クラスター構成を動的に変更する方法を学習します。
---

# コンフィグレーションを動的に変更する {#modify-configuration-dynamically}

このドキュメントでは、クラスター構成を動的に変更する方法について説明します。

クラスター コンポーネントを再起動せずに、SQL ステートメントを使用してコンポーネント (TiDB、TiKV、PD を含む) の構成を動的に更新できます。現在、TiDB インスタンス構成を変更する方法は、他のコンポーネント (TiKV や PD など) の構成を変更する方法とは異なります。

> **注記：**
>
> この機能は TiDB Self-Managed にのみ適用され、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)では使用できません。 TiDB Cloudの場合、設定を変更するには[TiDB Cloudサポート](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)連絡する必要があります。

## 共通操作 {#common-operations}

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

結果をフィールド別にフィルタリングできます。例:

```sql
show config where type='tidb'
show config where instance in (...)
show config where name like '%log%'
show config where type='tikv' and name='log.level'
```

### TiKV 構成を動的に変更する {#modify-tikv-configuration-dynamically}

> **注記：**
>
> -   TiKV 設定項目を動的に変更すると、TiKV 設定ファイルが自動的に更新されます。ただし、 `tiup edit-config`実行して対応する設定項目も変更する必要があります。そうしないと、 `upgrade`や`reload`などの操作によって変更が上書きされます。設定項目の変更の詳細については、 [TiUPを使用して構成を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration)を参照してください。
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

変更が成功した場合は`Query OK`が返されます。

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

バッチ変更ではアトミック性が保証されません。変更は一部のインスタンスでは成功しますが、他のインスタンスでは失敗する可能性があります。 `set tikv key=val`使用して TiKV クラスター全体の構成を変更すると、一部のインスタンスで変更が失敗する可能性があります。 `show warnings`使用して結果を確認できます。

一部の変更が失敗した場合は、対応するステートメントを再実行するか、失敗した各インスタンスを変更する必要があります。ネットワークの問題またはマシン障害のために一部の TiKV インスタンスにアクセスできない場合は、回復後にこれらのインスタンスを変更します。

構成項目が正常に変更された場合、その結果は構成ファイルに保存され、後続の操作で優先されます。一部の構成項目の名前は、 `limit`や`key`など、TiDB の予約語と競合する場合があります。これらの構成項目については、バックティック`` ` ``使用して囲みます。たとえば、 `` `raftstore.raft-log-gc-size-limit` ``です。

次の TiKV 構成項目は動的に変更できます。

| コンフィグレーション項目                                              | 説明                                                                                                                                                      |
| :-------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ログレベル                                                     | ログレベル。                                                                                                                                                  |
| `raftstore.raft-max-inflight-msgs`                        | 確認するRaftログの数。この数を超えると、 Raftステート マシンはログの送信速度を低下させます。                                                                                                     |
| `raftstore.raft-log-gc-tick-interval`                     | Raftログを削除するポーリングタスクがスケジュールされる時間間隔                                                                                                                       |
| `raftstore.raft-log-gc-threshold`                         | 残存Raftの最大許容数のソフト制限                                                                                                                                      |
| `raftstore.raft-log-gc-count-limit`                       | 許容される残存Raft数のハード制限                                                                                                                                      |
| `raftstore.raft-log-gc-size-limit`                        | 残余Raftの許容サイズに関するハード制限                                                                                                                                   |
| `raftstore.raft-max-size-per-msg`                         | 生成可能な単一メッセージパケットのサイズのソフト制限                                                                                                                              |
| `raftstore.raft-entry-max-size`                           | 単一のRaftログの最大サイズに対するハード制限                                                                                                                                |
| `raftstore.raft-entry-cache-life-time`                    | メモリ内のログキャッシュに許容される最大残り時間                                                                                                                                |
| `raftstore.max-apply-unpersisted-log-limit`               | コミットされたが永続化されていないRaftログの最大数を適用できる                                                                                                                       |
| `raftstore.split-region-check-tick-interval`              | リージョン分割が必要かどうかを確認する時間間隔                                                                                                                                 |
| `raftstore.region-split-check-diff`                       | リージョン分割前にリージョンデータが超過できる最大値                                                                                                                              |
| `raftstore.region-compact-check-interval`                 | RocksDB 圧縮を手動でトリガーする必要があるかどうかを確認する時間間隔                                                                                                                  |
| `raftstore.region-compact-check-step`                     | 手動圧縮の各ラウンドで一度にチェックされる領域の数                                                                                                                               |
| `raftstore.region-compact-min-tombstones`                 | RocksDB 圧縮をトリガーするために必要なトゥームストーンの数                                                                                                                       |
| `raftstore.region-compact-tombstones-percent`             | RocksDB圧縮をトリガーするために必要な墓石の割合                                                                                                                             |
| `raftstore.pd-heartbeat-tick-interval`                    | PDへのリージョンのハートビートがトリガーされる時間間隔                                                                                                                            |
| `raftstore.pd-store-heartbeat-tick-interval`              | 店舗のPDへのハートビートがトリガーされる時間間隔                                                                                                                               |
| `raftstore.snap-mgr-gc-tick-interval`                     | 期限切れのスナップショットファイルのリサイクルがトリガーされる時間間隔                                                                                                                     |
| `raftstore.snap-gc-timeout`                               | スナップショットファイルが保存される最長時間                                                                                                                                  |
| `raftstore.lock-cf-compact-interval`                      | TiKVがロックカラムファミリの手動圧縮をトリガーする時間間隔                                                                                                                         |
| `raftstore.lock-cf-compact-bytes-threshold`               | TiKVがロックカラムファミリの手動圧縮をトリガーするサイズ                                                                                                                          |
| `raftstore.messages-per-tick`                             | バッチごとに処理されるメッセージの最大数                                                                                                                                    |
| `raftstore.max-peer-down-duration`                        | ピアに許可される最長時間の非アクティブ期間                                                                                                                                   |
| `raftstore.max-leader-missing-duration`                   | ピアがリーダーなしでいられる最長期間。この値を超えると、ピアは PD を使用して削除されたかどうかを確認します。                                                                                                |
| `raftstore.abnormal-leader-missing-duration`              | ピアがリーダーなしでいられる通常の期間。この値を超えると、ピアは異常とみなされ、メトリックとログにマークされます。                                                                                               |
| `raftstore.peer-stale-state-check-interval`               | ピアにリーダーがいないかどうかを確認する時間間隔                                                                                                                                |
| `raftstore.consistency-check-interval`                    | 一貫性をチェックする時間間隔（TiDB のガベージコレクションと互換性がないため、推奨され**ません**）                                                                                                   |
| `raftstore.raft-store-max-leader-lease`                   | Raftリーダーの最も長い信頼期間                                                                                                                                       |
| `raftstore.merge-check-tick-interval`                     | マージチェックの時間間隔                                                                                                                                            |
| `raftstore.cleanup-import-sst-interval`                   | 期限切れのSSTファイルをチェックする時間間隔                                                                                                                                 |
| `raftstore.local-read-batch-size`                         | 1バッチで処理される読み取り要求の最大数                                                                                                                                    |
| `raftstore.apply-yield-write-size`                        | 適用スレッドが各ラウンドで1つのFSM（有限状態マシン）に書き込むことができる最大バイト数                                                                                                           |
| `raftstore.hibernate-timeout`                             | 起動時に休止状態に入るまでの最短待機時間。この期間中、TiKV は休止状態になりません (解放されません)。                                                                                                  |
| `raftstore.apply-pool-size`                               | データをディスクにフラッシュするプール内のスレッドの数。これは適用スレッドプールのサイズです。                                                                                                         |
| `raftstore.store-pool-size`                               | Raftを処理するプール内のスレッド数。これはRaftstoreスレッドプールのサイズです。                                                                                                          |
| `raftstore.apply-max-batch-size`                          | Raftステート マシンは、BatchSystem によってデータ書き込み要求をバッチで処理します。この構成項目は、1 つのバッチで要求を実行できるRaftステート マシンの最大数を指定します。                                                       |
| `raftstore.store-max-batch-size`                          | Raftステート マシンは、BatchSystem によってログをディスクにフラッシュする要求をバッチで処理します。この構成項目は、1 つのバッチで要求を処理できるRaftステート マシンの最大数を指定します。                                               |
| `raftstore.store-io-pool-size`                            | Raft I/O タスクを処理するスレッドの数。これは StoreWriter スレッド プールのサイズでもあります (この値を 0 以外の値から 0 に、または 0 から 0 以外の値に変更し**ないでください**)                                           |
| `raftstore.periodic-full-compact-start-max-cpu`           | 完全圧縮が有効な場合に TiKV が定期的に完全圧縮を実行する CPU 使用率のしきい値                                                                                                            |
| `readpool.unified.max-thread-count`                       | 読み取り要求を均一に処理するスレッド プール内のスレッドの最大数。これは UnifyReadPool スレッド プールのサイズです。                                                                                      |
| `readpool.unified.max-tasks-per-worker`                   | 統合読み取りプール内の 1 つのスレッドに許可されるタスクの最大数。値を超えると`Server Is Busy`エラーが返されます。                                                                                      |
| `readpool.unified.auto-adjust-pool-size`                  | UnifyReadPool スレッド プールのサイズを自動的に調整するかどうかを決定します。                                                                                                          |
| `coprocessor.split-region-on-table`                       | テーブルごとにリージョンを分割できます                                                                                                                                     |
| `coprocessor.batch-split-limit`                           | バッチでのリージョン分割のしきい値                                                                                                                                       |
| `coprocessor.region-max-size`                             | リージョンの最大サイズ                                                                                                                                             |
| `coprocessor.region-split-size`                           | 新しく分割されたリージョンのサイズ                                                                                                                                       |
| `coprocessor.region-max-keys`                             | リージョンで許可されるキーの最大数                                                                                                                                       |
| `coprocessor.region-split-keys`                           | 新しく分割されたリージョン内のキーの数                                                                                                                                     |
| `pessimistic-txn.wait-for-lock-timeout`                   | 悲観的トランザクションがロックを待つ最長時間                                                                                                                                  |
| `pessimistic-txn.wake-up-delay-duration`                  | 悲観的トランザクションが起動されるまでの期間                                                                                                                                  |
| `pessimistic-txn.pipelined`                               | パイプライン化された悲観的ロック処理を有効にするかどうかを決定します                                                                                                                      |
| `pessimistic-txn.in-memory`                               | メモリ内の悲観的ロックを有効にするかどうかを決定します                                                                                                                             |
| `quota.foreground-cpu-time`                               | TiKVフォアグラウンドが読み取りおよび書き込み要求を処理するために使用するCPUリソースのソフト制限                                                                                                     |
| `quota.foreground-write-bandwidth`                        | フォアグラウンドトランザクションがデータを書き込む帯域幅のソフト制限                                                                                                                      |
| `quota.foreground-read-bandwidth`                         | フォアグラウンドトランザクションとコプロセッサーがデータを読み取る帯域幅のソフト制限                                                                                                              |
| `quota.background-cpu-time`                               | TiKV バックグラウンドで読み取りおよび書き込み要求を処理するために使用する CPU リソースのソフト制限                                                                                                  |
| `quota.background-write-bandwidth`                        | バックグラウンド トランザクションがデータを書き込む帯域幅のソフト制限 (まだ有効ではありません)                                                                                                       |
| `quota.background-read-bandwidth`                         | バックグラウンド トランザクションとコプロセッサーがデータを読み取る帯域幅のソフト制限 (まだ有効ではありません)                                                                                               |
| `quota.enable-auto-tune`                                  | クォータの自動調整を有効にするかどうか。この構成項目を有効にすると、TiKV は TiKV インスタンスの負荷に基づいてバックグラウンド要求のクォータを動的に調整します。                                                                   |
| `quota.max-delay-duration`                                | 単一の読み取りまたは書き込み要求がフォアグラウンドで処理されるまでに強制的に待機される最大時間                                                                                                         |
| `gc.ratio-threshold`                                      | リージョンGC がスキップされるしきい値 (GC バージョンの数 / キーの数)                                                                                                                |
| `gc.batch-keys`                                           | 1バッチで処理されるキーの数                                                                                                                                          |
| `gc.max-write-bytes-per-sec`                              | RocksDBに1秒あたり書き込める最大バイト数                                                                                                                                |
| `gc.enable-compaction-filter`                             | 圧縮フィルタを有効にするかどうか                                                                                                                                        |
| `gc.compaction-filter-skip-version-check`                 | 圧縮フィルタのクラスタバージョンチェックをスキップするかどうか（未リリース）                                                                                                                  |
| `{db-name}.max-total-wal-size`                            | 合計WALの最大サイズ                                                                                                                                             |
| `{db-name}.max-background-jobs`                           | RocksDBのバックグラウンドスレッドの数                                                                                                                                  |
| `{db-name}.max-background-flushes`                        | RocksDB のフラッシュスレッドの最大数                                                                                                                                  |
| `{db-name}.max-open-files`                                | RocksDBが開くことができるファイルの総数                                                                                                                                 |
| `{db-name}.compaction-readahead-size`                     | 圧縮時のサイズ`readahead`                                                                                                                                      |
| `{db-name}.bytes-per-sync`                                | ファイルが非同期的に書き込まれている間に、OSがファイルをディスクに段階的に同期する速度                                                                                                            |
| `{db-name}.wal-bytes-per-sync`                            | WAL ファイルが書き込まれている間に OS が WAL ファイルをディスクに増分的に同期する速度                                                                                                       |
| `{db-name}.writable-file-max-buffer-size`                 | WritableFileWriteで使用される最大バッファサイズ                                                                                                                        |
| `{db-name}.{cf-name}.block-cache-size`                    | ブロックのキャッシュサイズ                                                                                                                                           |
| `{db-name}.{cf-name}.write-buffer-size`                   | メモリテーブルのサイズ                                                                                                                                             |
| `{db-name}.{cf-name}.max-write-buffer-number`             | メンバテーブルの最大数                                                                                                                                             |
| `{db-name}.{cf-name}.max-bytes-for-level-base`            | 基本レベル（L1）での最大バイト数                                                                                                                                       |
| `{db-name}.{cf-name}.target-file-size-base`               | ベースレベルのターゲットファイルのサイズ                                                                                                                                    |
| `{db-name}.{cf-name}.level0-file-num-compaction-trigger`  | 圧縮をトリガーする L0 のファイルの最大数                                                                                                                                  |
| `{db-name}.{cf-name}.level0-slowdown-writes-trigger`      | 書き込み停止を引き起こす L0 のファイルの最大数                                                                                                                               |
| `{db-name}.{cf-name}.level0-stop-writes-trigger`          | 書き込みを完全にブロックするL0のファイルの最大数                                                                                                                               |
| `{db-name}.{cf-name}.max-compaction-bytes`                | 圧縮ごとにディスクに書き込まれる最大バイト数                                                                                                                                  |
| `{db-name}.{cf-name}.max-bytes-for-level-multiplier`      | 各レイヤーのデフォルトの増幅倍数                                                                                                                                        |
| `{db-name}.{cf-name}.disable-auto-compactions`            | 自動圧縮を有効または無効にする                                                                                                                                         |
| `{db-name}.{cf-name}.soft-pending-compaction-bytes-limit` | 保留中の圧縮バイトのソフト制限                                                                                                                                         |
| `{db-name}.{cf-name}.hard-pending-compaction-bytes-limit` | 保留中の圧縮バイトのハード制限                                                                                                                                         |
| `{db-name}.{cf-name}.titan.blob-run-mode`                 | BLOBファイルの処理モード                                                                                                                                          |
| `{db-name}.{cf-name}.titan.min-blob-size`                 | Titan にデータを保存するしきい値。データの値がこのしきい値に達すると、データは Titan BLOB ファイルに保存されます。                                                                                      |
| `{db-name}.{cf-name}.titan.blob-file-compression`         | Titan BLOBファイルで使用される圧縮アルゴリズム                                                                                                                            |
| `{db-name}.{cf-name}.titan.discardable-ratio`             | GC の Titan データ ファイル内のゴミデータ比率のしきい値。BLOB ファイル内の無駄なデータの比率がしきい値を超えると、Titan GC がトリガーされます。                                                                    |
| `server.grpc-memory-pool-quota`                           | gRPCで使用できるメモリサイズを制限します                                                                                                                                  |
| `server.max-grpc-send-msg-len`                            | 送信できるgRPCメッセージの最大長を設定します                                                                                                                                |
| `server.snap-io-max-bytes-per-sec`                        | スナップショットを処理するときに許容される最大ディスク帯域幅を設定します                                                                                                                    |
| `server.concurrent-send-snap-limit`                       | 同時に送信されるスナップショットの最大数を設定します                                                                                                                              |
| `server.concurrent-recv-snap-limit`                       | 同時に受信するスナップショットの最大数を設定します                                                                                                                               |
| `server.raft-msg-max-batch-size`                          | 1 つの gRPC メッセージに含まれるRaftメッセージの最大数を設定します。                                                                                                                |
| `server.simplify-metrics`                                 | サンプリング監視メトリックを簡素化するかどうかを制御します                                                                                                                           |
| `storage.block-cache.capacity`                            | 共有ブロックキャッシュのサイズ (v4.0.3 以降でサポート)                                                                                                                        |
| `storage.scheduler-worker-pool-size`                      | スケジューラスレッドプール内のスレッド数                                                                                                                                    |
| `import.num-threads`                                      | 復元またはインポート RPC 要求を処理するスレッドの数 (動的変更は v8.1.2 以降でサポートされます)                                                                                                 |
| `backup.num-threads`                                      | バックアップ スレッドの数 (v4.0.3 以降でサポート)                                                                                                                          |
| `split.qps-threshold`                                     | リージョンで`load-base-split`実行するしきい値。リージョンの読み取り要求の QPS が 10 秒連続で`qps-threshold`超える場合、このリージョンは分割される必要があります。                                                   |
| `split.byte-threshold`                                    | リージョンで`load-base-split`実行するしきい値。リージョンの読み取り要求のトラフィックが 10 秒連続で`byte-threshold`超える場合、このリージョンは分割される必要があります。                                                 |
| `split.region-cpu-overload-threshold-ratio`               | リージョンで`load-base-split`実行するしきい値。リージョンの統合読み取りプールの CPU 使用率が 10 秒連続で`region-cpu-overload-threshold-ratio`超える場合、このリージョンは分割される必要があります。(v6.2.0 以降でサポートされています) |
| `split.split-balance-score`                               | `load-base-split`のパラメータは、2 つの分割されたリージョンの負荷が可能な限り均等になるようにします。値が小さいほど、負荷は均等になります。ただし、設定が小さすぎると、分割が失敗する可能性があります。                                           |
| `split.split-contained-score`                             | パラメータは`load-base-split`です。値が小さいほど、リージョン分割後の地域間訪問が少なくなります。                                                                                               |
| `cdc.min-ts-interval`                                     | 解決されたTSが転送される時間間隔                                                                                                                                       |
| `cdc.old-value-cache-memory-quota`                        | TiCDC 古い値エントリが占有するメモリの上限                                                                                                                                |
| `cdc.sink-memory-quota`                                   | TiCDCデータ変更イベントが占有するメモリの上限                                                                                                                               |
| `cdc.incremental-scan-speed-limit`                        | 履歴データの増分スキャンの速度の上限                                                                                                                                      |
| `cdc.incremental-scan-concurrency`                        | 履歴データの同時増分スキャンタスクの最大数                                                                                                                                   |

上記の表で、プレフィックスが`{db-name}`または`{db-name}.{cf-name}`パラメータは、RocksDB に関連する設定です。 `db-name`のオプションの値は`rocksdb`と`raftdb`です。

-   `db-name`が`rocksdb`場合、 `cf-name`のオプションの値は`defaultcf` 、 `writecf` 、 `lockcf` 、および`raftcf`です。
-   `db-name`が`raftdb`場合、 `cf-name`の値は`defaultcf`になります。

詳細なパラメータの説明については[TiKVコンフィグレーションファイル](/tikv-configuration-file.md)を参照してください。

### PD構成を動的に変更する {#modify-pd-configuration-dynamically}

現在、PD はインスタンスごとに個別の構成をサポートしていません。すべての PD インスタンスは同じ構成を共有します。

次のステートメントを使用して PD 構成を変更できます。

```sql
set config pd `log.level`='info';
```

変更が成功した場合は`Query OK`が返されます。

```sql
Query OK, 0 rows affected (0.01 sec)
```

構成項目が正常に変更された場合、その結果は構成ファイルではなく etcd に保存されます。後続の操作では、etcd の構成が優先されます。一部の構成項目の名前は、TiDB の予約語と競合する場合があります。これらの構成項目については、バックティック`` ` ``使用して囲みます。たとえば、 `` `schedule.leader-schedule-limit` ``です。

次の PD 構成項目は動的に変更できます。

| コンフィグレーション項目                               | 説明                                               |
| :----------------------------------------- | :----------------------------------------------- |
| `log.level`                                | ログレベル                                            |
| `cluster-version`                          | クラスターバージョン                                       |
| `schedule.max-merge-region-size`           | `Region Merge` （MiB）のサイズ制限を制御します                 |
| `schedule.max-merge-region-keys`           | `Region Merge`キーの最大数を指定します                       |
| `schedule.patrol-region-interval`          | リージョンのヘルス状態をチェックする`replicaChecker`を決定します         |
| `schedule.split-merge-interval`            | 同じリージョンで分割および結合操作を実行する時間間隔を決定します                 |
| `schedule.max-snapshot-count`              | 1 つのストアが同時に送信または受信できるスナップショットの最大数を決定します。         |
| `schedule.max-pending-peer-count`          | 単一ストア内の保留中のピアの最大数を決定します                          |
| `schedule.max-store-down-time`             | PDが切断されたストアを回復できないと判断するまでのダウンタイム                 |
| `schedule.leader-schedule-policy`          | Leaderのスケジュールのポリシーを決定します                         |
| `schedule.leader-schedule-limit`           | 同時に実行されるLeaderスケジュールタスクの数                        |
| `schedule.region-schedule-limit`           | 同時に実行されるリージョンスケジュールタスクの数                         |
| `schedule.replica-schedule-limit`          | 同時に実行されるレプリカ スケジューリング タスクの数                      |
| `schedule.merge-schedule-limit`            | 同時に実行される`Region Merge`のスケジュールタスクの数               |
| `schedule.hot-region-schedule-limit`       | 同時に実行されるホットリージョンスケジューリングタスクの数                    |
| `schedule.hot-region-cache-hits-threshold` | リージョンがホットスポットとみなされる閾値を決定します                      |
| `schedule.high-space-ratio`                | 店舗の収容能力が十分である閾値比率                                |
| `schedule.low-space-ratio`                 | 店舗の収容能力が不足する閾値比率                                 |
| `schedule.tolerant-size-ratio`             | `balance`バッファサイズを制御します                           |
| `schedule.enable-remove-down-replica`      | `DownReplica`自動的に削除する機能を有効にするかどうかを決定します          |
| `schedule.enable-replace-offline-replica`  | `OfflineReplica`移行する機能を有効にするかどうかを決定します           |
| `schedule.enable-make-up-replica`          | レプリカを自動的に補完する機能を有効にするかどうかを決定します                  |
| `schedule.enable-remove-extra-replica`     | 余分なレプリカを削除する機能を有効にするかどうかを決定します                   |
| `schedule.enable-location-replacement`     | 分離レベルチェックを有効にするかどうかを決定します                        |
| `schedule.enable-cross-table-merge`        | テーブル間の結合を有効にするかどうかを決定します                         |
| `schedule.enable-one-way-merge`            | 一方向のマージを有効にします。これにより、隣接する次のリージョンとのマージのみが可能になります。 |
| `replication.max-replicas`                 | レプリカの最大数を設定します                                   |
| `replication.location-labels`              | TiKVクラスタのトポロジ情報                                  |
| `replication.enable-placement-rules`       | 配置ルールを有効にする                                      |
| `replication.strictly-match-label`         | ラベルチェックを有効にする                                    |
| `pd-server.use-region-storage`             | 独立したリージョンstorageを有効にする                           |
| `pd-server.max-gap-reset-ts`               | タイムスタンプをリセットする最大間隔を設定します（BR）                     |
| `pd-server.key-type`                       | クラスタキータイプを設定します                                  |
| `pd-server.metric-storage`                 | クラスターメトリックのstorageアドレスを設定します                     |
| `pd-server.dashboard-address`              | ダッシュボードのアドレスを設定します                               |
| `replication-mode.replication-mode`        | バックアップモードを設定します                                  |

詳細なパラメータの説明については[PDコンフィグレーションファイル](/pd-configuration-file.md)を参照してください。

### TiDB構成を動的に変更する {#modify-tidb-configuration-dynamically}

現在、TiDB 構成の変更方法は、TiKV および PD 構成の変更方法とは異なります。 [システム変数](/system-variables.md)使用して TiDB 構成を変更できます。

次の例は、 `tidb_slow_log_threshold`変数を使用して`slow-threshold`動的に変更する方法を示しています。

デフォルト値`slow-threshold`は 300 ミリ秒です。 `tidb_slow_log_threshold`使用すると 200 ミリ秒に設定できます。

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
| `instance.tidb_force_priority`                          | `tidb_force_priority`                        | このTiDBインスタンスから送信されるステートメントの優先順位を指定します                                                 |
| `instance.max_connections`                              | `max_connections`                            | このTiDBインスタンスに許可される同時接続の最大数を指定します                                                      |
| `instance.tidb_enable_ddl`                              | `tidb_enable_ddl`                            | このTiDBインスタンスがDDL所有者になれるかどうかを制御します                                                     |
| `pessimistic-txn.constraint-check-in-place-pessimistic` | `tidb_constraint_check_in_place_pessimistic` | ユニークインデックスのユニーク制約チェックを、このインデックスがロックを必要とする次の時点まで延期するか、トランザクションがコミットされる時点まで延期するかを制御します。 |

### TiFlash構成を動的に変更する {#modify-tiflash-configuration-dynamically}

現在、システム変数[`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610)使用してTiFlash構成`max_threads`を変更できます。この変数は、 TiFlash が要求を実行するための最大同時実行性を指​​定します。

`tidb_max_tiflash_threads`のデフォルト値は`-1`で、このシステム変数は無効であり、 TiFlash構成ファイルの設定に依存することを示します。 `tidb_max_tiflash_threads`使用して`max_threads`から 10 に設定できます。

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
