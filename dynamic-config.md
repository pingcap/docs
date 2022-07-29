---
title: Modify Configuration Online
summary: Learn how to change the cluster configuration online.
---

# オンラインでConfiguration / コンフィグレーションを変更する {#modify-configuration-online}

このドキュメントでは、クラスタ構成をオンラインで変更する方法について説明します。

クラスタコンポーネントを再起動せずに、SQLステートメントを使用してコンポーネント（TiDB、TiKV、およびPDを含む）の構成をオンラインで更新できます。現在、TiDBインスタンスの構成を変更する方法は、他のコンポーネント（TiKVやPDなど）の構成を変更する方法とは異なります。

## 一般的な操作 {#common-operations}

このセクションでは、構成をオンラインで変更する一般的な操作について説明します。

### インスタンス構成のビュー {#view-instance-configuration}

クラスタのすべてのインスタンスの構成を表示するには、 `show config`ステートメントを使用します。結果は次のとおりです。

{{< copyable "" >}}

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

結果をフィールドでフィルタリングできます。例えば：

{{< copyable "" >}}

```sql
show config where type='tidb'
show config where instance in (...)
show config where name like '%log%'
show config where type='tikv' and name='log.level'
```

### TiKV構成をオンラインで変更する {#modify-tikv-configuration-online}

> **ノート：**
>
> -   TiKV構成アイテムをオンラインで変更すると、TiKV構成ファイルが自動的に更新されます。ただし、 `tiup edit-config`を実行して、対応する構成アイテムも変更する必要があります。そうしないと、 `upgrade`や`reload`などの操作で変更が上書きされます。構成項目の変更の詳細については、 [TiUPを使用して構成を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration)を参照してください。
> -   `tiup edit-config`を実行した後、 `tiup reload`を実行する必要はありません。

`set config`ステートメントを使用する場合、インスタンスアドレスまたはコンポーネントタイプに応じて、単一インスタンスまたはすべてのインスタンスの構成を変更できます。

-   すべてのTiKVインスタンスの構成を変更します。

> **ノート：**
>
> 変数名をバッククォートでラップすることをお勧めします。

{{< copyable "" >}}

```sql
set config tikv `split.qps-threshold`=1000
```

-   単一のTiKVインスタンスの構成を変更します。

    {{< copyable "" >}}

    ```sql
    set config "127.0.0.1:20180" `split.qps-threshold`=1000
    ```

変更が成功すると、 `Query OK`が返されます。

```sql
Query OK, 0 rows affected (0.01 sec)
```

バッチ変更中にエラーが発生した場合、警告が返されます。

{{< copyable "" >}}

```sql
set config tikv `log-level`='warn';
```

```sql
Query OK, 0 rows affected, 1 warning (0.04 sec)
```

{{< copyable "" >}}

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

バッチ変更は原子性を保証するものではありません。変更は、一部のインスタンスでは成功し、他のインスタンスでは失敗する場合があります。 `set tikv key=val`を使用してTiKVクラスタ全体の構成を変更すると、一部のインスタンスで変更が失敗する場合があります。 `show warnings`を使用して結果を確認できます。

一部の変更が失敗した場合は、対応するステートメントを再実行するか、失敗した各インスタンスを変更する必要があります。ネットワークの問題またはマシンの障害が原因で一部のTiKVインスタンスにアクセスできない場合は、回復後にこれらのインスタンスを変更してください。

構成アイテムが正常に変更されると、結果は構成ファイルに保持され、後続の操作で優先されます。一部の構成アイテムの名前は、 `limit`や`key`などのTiDB予約語と競合する可能性があります。これらの構成アイテムについては、バッククォート`` ` ``を使用して囲みます。たとえば、 `` `raftstore.raft-log-gc-size-limit` `` 。

次のTiKV構成アイテムはオンラインで変更できます。

| Configuration / コンフィグレーション項目                              | 説明                                                                                                              |
| :-------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------- |
| `raftstore.raft-max-inflight-msgs`                        | 確認するRaftの数。この数を超えると、 Raftステートマシンはログの送信を遅くします。                                                                   |
| `raftstore.raft-log-gc-tick-interval`                     | Raftログを削除するポーリングタスクがスケジュールされる時間間隔                                                                               |
| `raftstore.raft-log-gc-threshold`                         | 残りのRaftログの最大許容数のソフト制限                                                                                           |
| `raftstore.raft-log-gc-count-limit`                       | 残りのRaftログの許容数の厳しい制限                                                                                             |
| `raftstore.raft-log-gc-size-limit`                        | 残りのRaftの許容サイズの厳しい制限                                                                                             |
| `raftstore.raft-max-size-per-msg`                         | 生成が許可される単一のメッセージパケットのサイズのソフト制限                                                                                  |
| `raftstore.raft-entry-max-size`                           | 単一のRaftログの最大サイズの厳しい制限                                                                                           |
| `raftstore.raft-entry-cache-life-time`                    | メモリ内のログキャッシュに許可される最大残り時間                                                                                        |
| `raftstore.split-region-check-tick-interval`              | リージョン分割が必要かどうかを確認する時間間隔                                                                                         |
| `raftstore.region-split-check-diff`                       | リージョン分割前にリージョンデータが超過できる最大値                                                                                      |
| `raftstore.region-compact-check-interval`                 | RocksDB圧縮を手動でトリガーする必要があるかどうかを確認する時間間隔                                                                           |
| `raftstore.region-compact-check-step`                     | 手動圧縮の各ラウンドで一度にチェックされるリージョンの数                                                                                    |
| `raftstore.region-compact-min-tombstones`                 | RocksDBの圧縮をトリガーするために必要なトゥームストーンの数                                                                               |
| `raftstore.region-compact-tombstones-percent`             | RocksDBの圧縮をトリガーするために必要なトゥームストーンの割合                                                                              |
| `raftstore.pd-heartbeat-tick-interval`                    | リージョンのPDへのハートビートがトリガーされる時間間隔                                                                                    |
| `raftstore.pd-store-heartbeat-tick-interval`              | 店舗のPDへのハートビートがトリガーされる時間間隔                                                                                       |
| `raftstore.snap-mgr-gc-tick-interval`                     | 期限切れのスナップショットファイルのリサイクルがトリガーされる時間間隔                                                                             |
| `raftstore.snap-gc-timeout`                               | スナップショットファイルが保存される最長時間                                                                                          |
| `raftstore.lock-cf-compact-interval`                      | TiKVがロックカラムファミリの手動圧縮をトリガーする時間間隔                                                                                 |
| `raftstore.lock-cf-compact-bytes-threshold`               | TiKVがロックカラムファミリの手動圧縮をトリガーするサイズ                                                                                  |
| `raftstore.messages-per-tick`                             | バッチごとに処理されるメッセージの最大数                                                                                            |
| `raftstore.max-peer-down-duration`                        | ピアに許可されている最長の非アクティブ期間                                                                                           |
| `raftstore.max-leader-missing-duration`                   | ピアがリーダーなしでいることができる最長の期間。この値を超えると、ピアはPDで値が削除されたかどうかを確認します。                                                       |
| `raftstore.abnormal-leader-missing-duration`              | 通常の期間では、ピアにリーダーがいなくてもかまいません。この値を超えると、ピアは異常と見なされ、メトリックとログにマークされます。                                               |
| `raftstore.peer-stale-state-check-interval`               | ピアにリーダーがいないかどうかを確認する時間間隔                                                                                        |
| `raftstore.consistency-check-interval`                    | 整合性をチェックする時間間隔（TiDBのガベージコレクションと互換性がないため、お勧めし**ません**）                                                            |
| `raftstore.raft-store-max-leader-lease`                   | Raftリーダーの最長の信頼できる期間                                                                                             |
| `raftstore.merge-check-tick-interval`                     | マージチェックの時間間隔                                                                                                    |
| `raftstore.cleanup-import-sst-interval`                   | 期限切れのSSTファイルをチェックする時間間隔                                                                                         |
| `raftstore.local-read-batch-size`                         | 1つのバッチで処理される読み取り要求の最大数                                                                                          |
| `raftstore.hibernate-timeout`                             | 開始時に休止状態に入るまでの最短待機時間。この期間内、TiKVは休止状態になりません（解放されません）。                                                            |
| `raftstore.apply-pool-size`                               | データをディスクにフラッシュするプール内のスレッドの数。これは、アプライスレッドプールのサイズです。                                                              |
| `raftstore.store-pool-size`                               | Raftを処理するプール内のスレッドの数。これはRaftstoreスレッドプールのサイズです。                                                                 |
| `raftstore.apply-max-batch-size`                          | Raftステートマシンは、BatchSystemによってデータ書き込み要求をバッチで処理します。この構成項目は、1つのバッチで要求を実行できるRaftステートマシンの最大数を指定します。                   |
| `raftstore.store-max-batch-size`                          | Raftステートマシンは、BatchSystemによってログをディスクにフラッシュする要求をバッチで処理します。この構成項目は、1つのバッチで要求を処理できるRaftステートマシンの最大数を指定します。           |
| `readpool.unified.max-thread-count`                       | 読み取り要求を均一に処理するスレッドプール内のスレッドの最大数。これは、UnifyReadPoolスレッドプールのサイズです。                                                 |
| `coprocessor.split-region-on-table`                       | テーブルごとにリージョンを分割できるようにします                                                                                        |
| `coprocessor.batch-split-limit`                           | バッチで分割されたリージョンのしきい値                                                                                             |
| `coprocessor.region-max-size`                             | リージョンの最大サイズ                                                                                                     |
| `coprocessor.region-split-size`                           | 新しく分割されたリージョンのサイズ                                                                                               |
| `coprocessor.region-max-keys`                             | リージョンで許可されるキーの最大数                                                                                               |
| `coprocessor.region-split-keys`                           | 新しく分割されたリージョンのキーの数                                                                                              |
| `pessimistic-txn.wait-for-lock-timeout`                   | ペシミスティックトランザクションがロックを待機する最長の期間                                                                                  |
| `pessimistic-txn.wake-up-delay-duration`                  | 悲観的なトランザクションが起こされるまでの期間                                                                                         |
| `pessimistic-txn.pipelined`                               | パイプライン化された悲観的ロックプロセスを有効にするかどうかを決定します                                                                            |
| `pessimistic-txn.in-memory`                               | インメモリペシミスティックロックを有効にするかどうかを決定します                                                                                |
| `quota.foreground-cpu-time`                               | 読み取りおよび書き込み要求を処理するためにTiKVフォアグラウンドによって使用されるCPUリソースのソフト制限                                                         |
| `quota.foreground-write-bandwidth`                        | トランザクションがデータを書き込む帯域幅のソフト制限                                                                                      |
| `quota.foreground-read-bandwidth`                         | トランザクションとコプロセッサーがデータを読み取る帯域幅のソフト制限                                                                              |
| `quota.max-delay-duration`                                | 単一の読み取りまたは書き込み要求がフォアグラウンドで処理される前に強制的に待機される最大時間                                                                  |
| `gc.ratio-threshold`                                      | リージョンGCがスキップされるしきい値（GCバージョンの数/キーの数）                                                                             |
| `gc.batch-keys`                                           | 1つのバッチで処理されるキーの数                                                                                                |
| `gc.max-write-bytes-per-sec`                              | RocksDBに1秒あたりに書き込むことができる最大バイト数                                                                                  |
| `gc.enable-compaction-filter`                             | 圧縮フィルターを有効にするかどうか                                                                                               |
| `gc.compaction-filter-skip-version-check`                 | 圧縮フィルターのクラスタバージョンチェックをスキップするかどうか（リリースされていません）                                                                   |
| `{db-name}.max-total-wal-size`                            | 合計WALの最大サイズ                                                                                                     |
| `{db-name}.max-background-jobs`                           | RocksDBのバックグラウンドスレッドの数                                                                                          |
| `{db-name}.max-background-flushes`                        | RocksDBのフラッシュスレッドの最大数                                                                                           |
| `{db-name}.max-open-files`                                | RocksDBが開くことができるファイルの総数                                                                                         |
| `{db-name}.compaction-readahead-size`                     | 圧縮時のサイズは`readahead`                                                                                             |
| `{db-name}.bytes-per-sync`                                | これらのファイルが非同期に書き込まれている間に、OSがファイルをディスクに段階的に同期する速度                                                                 |
| `{db-name}.wal-bytes-per-sync`                            | WALファイルの書き込み中にOSがWALファイルをディスクに段階的に同期する速度                                                                        |
| `{db-name}.writable-file-max-buffer-size`                 | WritableFileWriteで使用される最大バッファサイズ                                                                                |
| `{db-name}.{cf-name}.block-cache-size`                    | ブロックのキャッシュサイズ                                                                                                   |
| `{db-name}.{cf-name}.write-buffer-size`                   | memtableのサイズ                                                                                                    |
| `{db-name}.{cf-name}.max-write-buffer-number`             | memtableの最大数                                                                                                    |
| `{db-name}.{cf-name}.max-bytes-for-level-base`            | 基本レベル（L1）での最大バイト数                                                                                               |
| `{db-name}.{cf-name}.target-file-size-base`               | 基本レベルでのターゲットファイルのサイズ                                                                                            |
| `{db-name}.{cf-name}.level0-file-num-compaction-trigger`  | 圧縮をトリガーするL0でのファイルの最大数                                                                                           |
| `{db-name}.{cf-name}.level0-slowdown-writes-trigger`      | 書き込みストールをトリガーするL0でのファイルの最大数                                                                                     |
| `{db-name}.{cf-name}.level0-stop-writes-trigger`          | 書き込みを完全にブロックするL0でのファイルの最大数                                                                                      |
| `{db-name}.{cf-name}.max-compaction-bytes`                | 圧縮ごとにディスクに書き込まれる最大バイト数                                                                                          |
| `{db-name}.{cf-name}.max-bytes-for-level-multiplier`      | 各層のデフォルトの増幅倍数                                                                                                   |
| `{db-name}.{cf-name}.disable-auto-compactions`            | 自動圧縮を有効または無効にします                                                                                                |
| `{db-name}.{cf-name}.soft-pending-compaction-bytes-limit` | 保留中の圧縮バイトのソフト制限                                                                                                 |
| `{db-name}.{cf-name}.hard-pending-compaction-bytes-limit` | 保留中の圧縮バイトのハード制限                                                                                                 |
| `{db-name}.{cf-name}.titan.blob-run-mode`                 | BLOBファイルを処理するモード                                                                                                |
| `server.grpc-memory-pool-quota`                           | gRPCで使用できるメモリサイズを制限します                                                                                          |
| `server.max-grpc-send-msg-len`                            | 送信できるgRPCメッセージの最大長を設定します                                                                                        |
| `server.raft-msg-max-batch-size`                          | 1つのgRPCメッセージに含まれるRaftメッセージの最大数を設定します                                                                            |
| `storage.block-cache.capacity`                            | 共有ブロックキャッシュのサイズ（v4.0.3以降でサポート）                                                                                  |
| `storage.scheduler-worker-pool-size`                      | スケジューラスレッドプール内のスレッド数                                                                                            |
| `backup.num-threads`                                      | バックアップスレッドの数（v4.0.3以降でサポート）                                                                                     |
| `split.qps-threshold`                                     | リージョンで`load-base-split`を実行するためのしきい値。リージョンの読み取り要求のQPSが連続して`qps-threshold`を超える場合、このリージョンを分割する必要があります。             |
| `split.byte-threshold`                                    | リージョンで`load-base-split`を実行するためのしきい値。リージョンの読み取り要求のトラフィックが連続して`byte-threshold`を超える場合、このリージョンを分割する必要があります。         |
| `split.split-balance-score`                               | 2つの分割領域の負荷が可能な限りバランスが取れていることを保証する`load-base-split`のパラメーター。値が小さいほど、負荷のバランスが取れています。ただし、設定が小さすぎると、分割が失敗する可能性があります。 |
| `split.split-contained-score`                             | `load-base-split`のパラメータ。値が小さいほど、リージョン分割後のリージョン間の訪問は少なくなります。                                                     |
| `cdc.min-ts-interval`                                     | 解決済みTSが転送される時間間隔                                                                                                |
| `cdc.old-value-cache-memory-quota`                        | TiCDCOldValueエントリが占有するメモリの上限                                                                                    |
| `cdc.sink-memory-quota`                                   | TiCDCデータ変更イベントが占めるメモリの上限                                                                                        |
| `cdc.incremental-scan-speed-limit`                        | 履歴データのインクリメンタルスキャンの速度の上限                                                                                        |
| `cdc.incremental-scan-concurrency`                        | 履歴データの同時増分スキャンタスクの最大数                                                                                           |

上記の表で、プレフィックスが`{db-name}`または`{db-name}.{cf-name}`のパラメーターは、RocksDBに関連する構成です。 `db-name`のオプション値は`rocksdb`と`raftdb`です。

-   `db-name`が`rocksdb`の場合、 `cf-name`のオプション値は`defaultcf` 、 `writecf` `lockcf` `raftcf` 。
-   `db-name`が`raftdb`の場合、 `cf-name`の値は`defaultcf`になります。

パラメータの詳細な説明については、 [TiKVConfiguration / コンフィグレーションファイル](/tikv-configuration-file.md)を参照してください。

### PD構成をオンラインで変更する {#modify-pd-configuration-online}

現在、PDはインスタンスごとに個別の構成をサポートしていません。すべてのPDインスタンスは同じ構成を共有します。

次のステートメントを使用して、PD構成を変更できます。

{{< copyable "" >}}

```sql
set config pd `log.level`='info'
```

変更が成功すると、 `Query OK`が返されます。

```sql
Query OK, 0 rows affected (0.01 sec)
```

構成アイテムが正常に変更された場合、結果は構成ファイルではなくetcdに保持されます。 etcdの構成は、後続の操作で優先されます。一部の構成アイテムの名前は、TiDBの予約語と競合する可能性があります。これらの構成項目については、バッククォート`` ` ``を使用して囲みます。たとえば、 `` `schedule.leader-schedule-limit` `` 。

次のPD構成アイテムはオンラインで変更できます。

| Configuration / コンフィグレーション項目               | 説明                                               |
| :----------------------------------------- | :----------------------------------------------- |
| `log.level`                                | ログレベル                                            |
| `cluster-version`                          | クラスタバージョン                                        |
| `schedule.max-merge-region-size`           | `Region Merge`のサイズ制限を制御します（MiB単位）                |
| `schedule.max-merge-region-keys`           | `Region Merge`のキーの最大数を指定します                      |
| `schedule.patrol-region-interval`          | `replicaChecker`がリージョンのヘルス状態をチェックする頻度を決定します      |
| `schedule.split-merge-interval`            | 同じリージョンで分割操作とマージ操作を実行する時間間隔を決定します                |
| `schedule.max-snapshot-count`              | 1つのストアが同時に送信または受信できるスナップショットの最大数を決定します           |
| `schedule.max-pending-peer-count`          | 1つのストアで保留中のピアの最大数を決定します                          |
| `schedule.max-store-down-time`             | 切断されたストアを回復できないとPDが判断した後のダウンタイム                  |
| `schedule.leader-schedule-policy`          | リーダースケジューリングのポリシーを決定します                          |
| `schedule.leader-schedule-limit`           | 同時に実行されたリーダースケジューリングタスクの数                        |
| `schedule.region-schedule-limit`           | 同時に実行されたリージョンスケジューリングタスクの数                       |
| `schedule.replica-schedule-limit`          | 同時に実行されたレプリカスケジューリングタスクの数                        |
| `schedule.merge-schedule-limit`            | 同時に実行された`Region Merge`のスケジューリングタスクの数             |
| `schedule.hot-region-schedule-limit`       | 同時に実行されたホットリージョンスケジューリングタスクの数                    |
| `schedule.hot-region-cache-hits-threshold` | リージョンがホットスポットと見なされるしきい値を決定します                    |
| `schedule.high-space-ratio`                | それを下回るとストアの容量が十分になるしきい値比率                        |
| `schedule.low-space-ratio`                 | それを超えると店舗の容量が不足するしきい値比率                          |
| `schedule.tolerant-size-ratio`             | `balance`のバッファサイズを制御します                          |
| `schedule.enable-remove-down-replica`      | `DownReplica`を自動的に削除する機能を有効にするかどうかを決定します         |
| `schedule.enable-replace-offline-replica`  | 移行する機能を有効にするかどうかを決定します`OfflineReplica`           |
| `schedule.enable-make-up-replica`          | レプリカを自動的に補足する機能を有効にするかどうかを決定します                  |
| `schedule.enable-remove-extra-replica`     | 余分なレプリカを削除する機能を有効にするかどうかを決定します                   |
| `schedule.enable-location-replacement`     | 分離レベルチェックを有効にするかどうかを決定します                        |
| `schedule.enable-cross-table-merge`        | クロステーブルマージを有効にするかどうかを決定します                       |
| `schedule.enable-one-way-merge`            | 一方向のマージを有効にします。これにより、次の隣接するリージョンとのマージのみが可能になります。 |
| `replication.max-replicas`                 | レプリカの最大数を設定します                                   |
| `replication.location-labels`              | TiKVクラスタのトポロジー情報                                 |
| `replication.enable-placement-rules`       | 配置ルールを有効にします                                     |
| `replication.strictly-match-label`         | ラベルチェックを有効にします                                   |
| `pd-server.use-region-storage`             | 独立したリージョンストレージを有効にします                            |
| `pd-server.max-gap-reset-ts`               | タイムスタンプ（BR）をリセットする最大間隔を設定します                     |
| `pd-server.key-type`                       | クラスタキータイプを設定します                                  |
| `pd-server.metric-storage`                 | クラスタメトリックのストレージアドレスを設定します                        |
| `pd-server.dashboard-address`              | ダッシュボードアドレスを設定します                                |
| `replication-mode.replication-mode`        | バックアップモードを設定します                                  |

パラメータの詳細な説明については、 [PDConfiguration / コンフィグレーションファイル](/pd-configuration-file.md)を参照してください。

### TiDB構成をオンラインで変更する {#modify-tidb-configuration-online}

現在、TiDB構成を変更する方法は、TiKVおよびPD構成を変更する方法とは異なります。 [システム変数](/system-variables.md)を使用してTiDB構成を変更できます。

次の例は、 `tidb_slow_log_threshold`変数を使用して`slow-threshold`をオンラインで変更する方法を示しています。

デフォルト値の`slow-threshold`は300ミリ秒です。 `tidb_slow_log_threshold`を使用して200ミリ秒に設定できます。

{{< copyable "" >}}

```sql
set tidb_slow_log_threshold = 200;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

{{< copyable "" >}}

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

次のTiDB構成アイテムはオンラインで変更できます。

|Configuration / コンフィグレーション項目| SQL変数|説明| | ：--- | ：--- | | `log.enable-slow-log` | `tidb_enable_slow_log` |スローログを有効にするかどうか| | `log.slow-threshold` | `tidb_slow_log_threshold` |遅いログのしきい値| | `log.expensive-threshold` | `tidb_expensive_query_time_threshold` |高価なクエリのしきい値|

### TiFlash構成をオンラインで変更する {#modify-tiflash-configuration-online}

現在、TiFlashがリクエストを実行するための最大同時実行性を指定するシステム変数[`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610)を使用して、TiFlash構成`max_threads`を変更できます。

デフォルト値の`tidb_max_tiflash_threads`は`-1`です。これは、このシステム変数が無効であり、TiFlash構成ファイルの設定に依存することを示します。 `tidb_max_tiflash_threads`を使用して`max_threads`から10に設定できます：

{{< copyable "" >}}

```sql
set tidb_max_tiflash_threads = 10;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

{{< copyable "" >}}

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
