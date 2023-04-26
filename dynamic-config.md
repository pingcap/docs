---
title: Modify Configuration Dynamically
summary: Learn how to dynamically modify the cluster configuration.
---

# コンフィグレーションを動的に変更する {#modify-configuration-dynamically}

このドキュメントでは、クラスター構成を動的に変更する方法について説明します。

クラスター コンポーネントを再起動せずに、SQL ステートメントを使用して、コンポーネント (TiDB、TiKV、および PD を含む) の構成を動的に更新できます。現在、TiDB インスタンスの構成を変更する方法は、他のコンポーネント (TiKV や PD など) の構成を変更する方法とは異なります。

## 共通操作 {#common-operations}

このセクションでは、構成を動的に変更する一般的な操作について説明します。

### インスタンス構成のビュー {#view-instance-configuration}

クラスター内のすべてのインスタンスの構成を表示するには、 `show config`ステートメントを使用します。結果は次のとおりです。

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

フィールドで結果をフィルタリングできます。例えば：

{{< copyable "" >}}

```sql
show config where type='tidb'
show config where instance in (...)
show config where name like '%log%'
show config where type='tikv' and name='log.level'
```

### TiKV 構成を動的に変更する {#modify-tikv-configuration-dynamically}

> **ノート：**
>
> -   TiKV 構成項目を動的に変更した後、TiKV 構成ファイルは自動的に更新されます。ただし、 `tiup edit-config`を実行して、対応する構成項目を変更する必要もあります。そうしないと、 `upgrade`や`reload`などの操作によって変更が上書きされます。設定項目の変更については[TiUPを使用して構成を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration)を参照してください。
> -   `tiup edit-config`を実行した後、 `tiup reload`を実行する必要はありません。

`set config`ステートメントを使用すると、インスタンス アドレスまたはコンポーネントタイプに従って、単一インスタンスまたはすべてのインスタンスの構成を変更できます。

-   すべての TiKV インスタンスの構成を変更します。

> **ノート：**
>
> 変数名をバッククォートで囲むことをお勧めします。

{{< copyable "" >}}

```sql
set config tikv `split.qps-threshold`=1000;
```

-   単一の TiKV インスタンスの構成を変更します。

    {{< copyable "" >}}

    ```sql
    set config "127.0.0.1:20180" `split.qps-threshold`=1000;
    ```

変更が成功すると、 `Query OK`が返されます。

```sql
Query OK, 0 rows affected (0.01 sec)
```

バッチ変更中にエラーが発生した場合は、警告が返されます。

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

バッチ変更は原子性を保証しません。変更は、一部のインスタンスでは成功する可能性がありますが、他のインスタンスでは失敗する可能性があります。 `set tikv key=val`を使用して TiKV クラスター全体の構成を変更すると、一部のインスタンスで変更が失敗する可能性があります。 `show warnings`使用して結果を確認できます。

一部の変更が失敗した場合は、対応するステートメントを再実行するか、失敗した各インスタンスを変更する必要があります。ネットワークの問題やマシンの障害が原因で一部の TiKV インスタンスにアクセスできない場合は、それらのインスタンスが回復した後にこれらのインスタンスを変更します。

構成アイテムが正常に変更された場合、結果は構成ファイルに保持され、後続の操作で優先されます。一部の構成項目の名前は、 `limit`や`key`などの TiDB 予約語と競合する場合があります。これらの構成アイテムについては、バッククォート`` ` ``を使用して囲みます。たとえば、 `` `raftstore.raft-log-gc-size-limit` ``です。

次の TiKV 構成アイテムは、動的に変更できます。

| コンフィグレーション項目                                              | 説明                                                                                                                                                      |
| :-------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ログレベル                                                     | ログレベル。                                                                                                                                                  |
| `raftstore.raft-max-inflight-msgs`                        | 確認するRaftログの数。この数を超えると、 Raftステート マシンはログの送信を遅くします。                                                                                                        |
| `raftstore.raft-log-gc-tick-interval`                     | Raftログを削除するポーリング タスクがスケジュールされている時間間隔                                                                                                                    |
| `raftstore.raft-log-gc-threshold`                         | 残りのRaftログの最大許容数のソフト リミット                                                                                                                                |
| `raftstore.raft-log-gc-count-limit`                       | 残りのRaftログの許容数のハード リミット                                                                                                                                  |
| `raftstore.raft-log-gc-size-limit`                        | 残りのRaftログの許容サイズのハード リミット                                                                                                                                |
| `raftstore.raft-max-size-per-msg`                         | 生成できる単一メッセージ パケットのサイズのソフト リミット                                                                                                                          |
| `raftstore.raft-entry-max-size`                           | 1 つのRaftログの最大サイズのハード リミット                                                                                                                               |
| `raftstore.raft-entry-cache-life-time`                    | メモリ内のログ キャッシュに許可される最大残り時間                                                                                                                               |
| `raftstore.split-region-check-tick-interval`              | リージョン分割が必要かどうかを確認する時間間隔                                                                                                                                 |
| `raftstore.region-split-check-diff`                       | リージョン分割前にリージョンデータが超えることのできる最大値                                                                                                                          |
| `raftstore.region-compact-check-interval`                 | RocksDB 圧縮を手動でトリガーする必要があるかどうかを確認する時間間隔                                                                                                                  |
| `raftstore.region-compact-check-step`                     | 手動圧縮の各ラウンドで一度にチェックされるリージョンの数                                                                                                                            |
| `raftstore.region-compact-min-tombstones`                 | RocksDB 圧縮をトリガーするために必要なトゥームストーンの数                                                                                                                       |
| `raftstore.region-compact-tombstones-percent`             | RocksDB 圧縮をトリガーするために必要なトゥームストーンの割合                                                                                                                      |
| `raftstore.pd-heartbeat-tick-interval`                    | PD へのリージョンのハートビートがトリガーされる時間間隔                                                                                                                           |
| `raftstore.pd-store-heartbeat-tick-interval`              | PD へのストアのハートビートがトリガーされる時間間隔                                                                                                                             |
| `raftstore.snap-mgr-gc-tick-interval`                     | 期限切れのスナップショット ファイルのリサイクルがトリガーされる時間間隔                                                                                                                    |
| `raftstore.snap-gc-timeout`                               | スナップショット ファイルが保存される最長時間                                                                                                                                 |
| `raftstore.lock-cf-compact-interval`                      | TiKV が Lock カラム Family の手動圧縮をトリガーする時間間隔                                                                                                                 |
| `raftstore.lock-cf-compact-bytes-threshold`               | TiKV が Lock カラム Family の手動圧縮をトリガーするサイズ                                                                                                                  |
| `raftstore.messages-per-tick`                             | バッチごとに処理されるメッセージの最大数                                                                                                                                    |
| `raftstore.max-peer-down-duration`                        | ピアに許可される最長の非アクティブ期間                                                                                                                                     |
| `raftstore.max-leader-missing-duration`                   | リーダーなしでピアに許可される最長期間。この値を超えると、ピアは削除されたかどうかを PD で確認します。                                                                                                   |
| `raftstore.abnormal-leader-missing-duration`              | ピアがリーダーなしで存在できる通常の期間。この値を超えると、ピアは異常と見なされ、メトリックとログでマークされます。                                                                                              |
| `raftstore.peer-stale-state-check-interval`               | ピアにリーダーがいないかどうかを確認する時間間隔                                                                                                                                |
| `raftstore.consistency-check-interval`                    | 一貫性をチェックする時間間隔 (TiDB のガベージコレクションと互換性がないため、推奨され**ません**)                                                                                                  |
| `raftstore.raft-store-max-leader-lease`                   | Raftリーダーの最長信頼期間                                                                                                                                         |
| `raftstore.merge-check-tick-interval`                     | 合流チェックの時間間隔                                                                                                                                             |
| `raftstore.cleanup-import-sst-interval`                   | 期限切れの SST ファイルをチェックする時間間隔                                                                                                                               |
| `raftstore.local-read-batch-size`                         | 1 回のバッチで処理される読み取り要求の最大数                                                                                                                                 |
| `raftstore.apply-yield-write-size`                        | 適用スレッドが各ラウンドで 1 つの FSM (有限状態マシン) に書き込むことができる最大バイト数                                                                                                      |
| `raftstore.hibernate-timeout`                             | 起動時に休止状態に入るまでの最短待機時間。この期間中、TiKV は休止状態になりません (解放されません)。                                                                                                  |
| `raftstore.apply-pool-size`                               | データをディスクにフラッシュするプール内のスレッドの数。これは、適用スレッド プールのサイズです。                                                                                                       |
| `raftstore.store-pool-size`                               | Raftを処理するプール内のスレッド数 ( Raftstoreスレッド プールのサイズ)                                                                                                            |
| `raftstore.apply-max-batch-size`                          | Raftステート マシンは、BatchSystem によってバッチでデータ書き込み要求を処理します。この設定項目は、1 つのバッチでリクエストを実行できるRaftステート マシンの最大数を指定します。                                                    |
| `raftstore.store-max-batch-size`                          | Raftステート マシンは、BatchSystem によってバッチでログをディスクにフラッシュするための要求を処理します。この設定項目は、1 つのバッチでリクエストを処理できるRaftステート マシンの最大数を指定します。                                         |
| `readpool.unified.max-thread-count`                       | UnifyReadPool スレッド プールのサイズである、読み取り要求を均一に処理するスレッド プール内のスレッドの最大数                                                                                          |
| `readpool.unified.auto-adjust-pool-size`                  | UnifyReadPool スレッド プール サイズを自動的に調整するかどうかを決定します                                                                                                           |
| `coprocessor.split-region-on-table`                       | テーブルごとにリージョンを分割できます                                                                                                                                     |
| `coprocessor.batch-split-limit`                           | 一括でのリージョン分割の閾値                                                                                                                                          |
| `coprocessor.region-max-size`                             | リージョンの最大サイズ                                                                                                                                             |
| `coprocessor.region-split-size`                           | 新しく分割されたリージョンのサイズ                                                                                                                                       |
| `coprocessor.region-max-keys`                             | リージョンで許可されるキーの最大数                                                                                                                                       |
| `coprocessor.region-split-keys`                           | 新しく分割されたリージョンのキーの数                                                                                                                                      |
| `pessimistic-txn.wait-for-lock-timeout`                   | 悲観的トランザクションがロックを待機する最長期間                                                                                                                                |
| `pessimistic-txn.wake-up-delay-duration`                  | 悲観的トランザクションが起動されるまでの期間                                                                                                                                  |
| `pessimistic-txn.pipelined`                               | パイプライン化された悲観的ロック プロセスを有効にするかどうかを決定します。                                                                                                                  |
| `pessimistic-txn.in-memory`                               | インメモリ悲観的ロックを有効にするかどうかを決定します                                                                                                                             |
| `quota.foreground-cpu-time`                               | TiKV フォアグラウンドが読み取りおよび書き込み要求を処理するために使用する CPU リソースのソフト制限                                                                                                  |
| `quota.foreground-write-bandwidth`                        | フォアグラウンド トランザクションがデータを書き込む帯域幅のソフト リミット                                                                                                                  |
| `quota.foreground-read-bandwidth`                         | フォアグラウンド トランザクションとコプロセッサーがデータを読み取る帯域幅のソフト リミット                                                                                                          |
| `quota.background-cpu-time`                               | TiKV バックグラウンドが読み取りおよび書き込み要求を処理するために使用する CPU リソースのソフト制限                                                                                                  |
| `quota.background-write-bandwidth`                        | バックグラウンド トランザクションがデータを書き込む帯域幅のソフト リミット (まだ有効ではありません)                                                                                                    |
| `quota.background-read-bandwidth`                         | バックグラウンド トランザクションとコプロセッサーがデータを読み取る帯域幅のソフト リミット (まだ有効ではありません)                                                                                            |
| `quota.enable-auto-tune`                                  | クォータの自動調整を有効にするかどうか。この構成項目が有効になっている場合、TiKV は、TiKV インスタンスの負荷に基づいて、バックグラウンド リクエストのクォータを動的に調整します。                                                          |
| `quota.max-delay-duration`                                | 単一の読み取りまたは書き込み要求がフォアグラウンドで処理されるまで強制的に待機される最大時間                                                                                                          |
| `gc.ratio-threshold`                                      | リージョンGC がスキップされるしきい値 (GC バージョンの数/キーの数)                                                                                                                  |
| `gc.batch-keys`                                           | 1 回のバッチで処理されるキーの数                                                                                                                                       |
| `gc.max-write-bytes-per-sec`                              | 1 秒あたりに RocksDB に書き込むことができる最大バイト数                                                                                                                       |
| `gc.enable-compaction-filter`                             | 圧縮フィルターを有効にするかどうか                                                                                                                                       |
| `gc.compaction-filter-skip-version-check`                 | コンパクション フィルタのクラスタ バージョン チェックをスキップするかどうか (未公開)                                                                                                           |
| `{db-name}.max-total-wal-size`                            | 合計 WAL の最大サイズ                                                                                                                                           |
| `{db-name}.max-background-jobs`                           | RocksDB のバックグラウンド スレッドの数                                                                                                                                |
| `{db-name}.max-background-flushes`                        | RocksDB のフラッシュ スレッドの最大数                                                                                                                                 |
| `{db-name}.max-open-files`                                | RocksDB が開くことができるファイルの総数                                                                                                                                |
| `{db-name}.compaction-readahead-size`                     | 圧縮時のサイズ`readahead`                                                                                                                                      |
| `{db-name}.bytes-per-sync`                                | これらのファイルが非同期的に書き込まれている間に、OS がファイルをディスクに増分的に同期する速度                                                                                                       |
| `{db-name}.wal-bytes-per-sync`                            | WALファイルの書き込み中に、OSがWALファイルをディスクに段階的に同期する速度                                                                                                               |
| `{db-name}.writable-file-max-buffer-size`                 | WritableFileWrite で使用される最大バッファ サイズ                                                                                                                      |
| `{db-name}.{cf-name}.block-cache-size`                    | ブロックのキャッシュサイズ                                                                                                                                           |
| `{db-name}.{cf-name}.write-buffer-size`                   | memtable のサイズ                                                                                                                                           |
| `{db-name}.{cf-name}.max-write-buffer-number`             | memtable の最大数                                                                                                                                           |
| `{db-name}.{cf-name}.max-bytes-for-level-base`            | ベースレベル (L1) の最大バイト数                                                                                                                                     |
| `{db-name}.{cf-name}.target-file-size-base`               | ベース レベルでのターゲット ファイルのサイズ                                                                                                                                 |
| `{db-name}.{cf-name}.level0-file-num-compaction-trigger`  | 圧縮をトリガーする L0 のファイルの最大数                                                                                                                                  |
| `{db-name}.{cf-name}.level0-slowdown-writes-trigger`      | 書き込みストールをトリガーする L0 のファイルの最大数                                                                                                                            |
| `{db-name}.{cf-name}.level0-stop-writes-trigger`          | 書き込みを完全にブロックする L0 のファイルの最大数                                                                                                                             |
| `{db-name}.{cf-name}.max-compaction-bytes`                | 圧縮ごとにディスクに書き込まれる最大バイト数                                                                                                                                  |
| `{db-name}.{cf-name}.max-bytes-for-level-multiplier`      | 各レイヤーのデフォルトの増幅倍数                                                                                                                                        |
| `{db-name}.{cf-name}.disable-auto-compactions`            | 自動圧縮を有効または無効にします                                                                                                                                        |
| `{db-name}.{cf-name}.soft-pending-compaction-bytes-limit` | 保留中の圧縮バイトのソフト制限                                                                                                                                         |
| `{db-name}.{cf-name}.hard-pending-compaction-bytes-limit` | 保留中の圧縮バイトのハード制限                                                                                                                                         |
| `{db-name}.{cf-name}.titan.blob-run-mode`                 | BLOB ファイルの処理モード                                                                                                                                         |
| `server.grpc-memory-pool-quota`                           | gRPC で使用できるメモリサイズを制限します                                                                                                                                 |
| `server.max-grpc-send-msg-len`                            | 送信できる gRPC メッセージの最大長を設定します                                                                                                                              |
| `server.snap-max-write-bytes-per-sec`                     | スナップショットの処理時に許容される最大ディスク帯域幅を設定します                                                                                                                       |
| `server.concurrent-send-snap-limit`                       | 同時に送信されるスナップショットの最大数を設定します                                                                                                                              |
| `server.concurrent-recv-snap-limit`                       | 同時に受信するスナップショットの最大数を設定します                                                                                                                               |
| `server.raft-msg-max-batch-size`                          | 単一の gRPC メッセージに含まれるRaftメッセージの最大数を設定します                                                                                                                  |
| `server.simplify-metrics`                                 | サンプリング モニタリング メトリックを単純化するかどうかを制御します                                                                                                                     |
| `storage.block-cache.capacity`                            | 共有ブロックキャッシュのサイズ (v4.0.3 以降でサポート)                                                                                                                        |
| `storage.scheduler-worker-pool-size`                      | スケジューラ スレッド プール内のスレッド数                                                                                                                                  |
| `backup.num-threads`                                      | バックアップ スレッドの数 (v4.0.3 以降でサポート)                                                                                                                          |
| `split.qps-threshold`                                     | リージョンで`load-base-split`を実行するためのしきい値。リージョンの読み取りリクエストの QPS が 10 秒間連続して`qps-threshold`超える場合、このリージョンは分割する必要があります。                                           |
| `split.byte-threshold`                                    | リージョンで`load-base-split`を実行するためのしきい値。リージョンの読み取りリクエストのトラフィックが 10 秒間連続して`byte-threshold`超えた場合、このリージョンを分割する必要があります。                                         |
| `split.region-cpu-overload-threshold-ratio`               | リージョンで`load-base-split`を実行するためのしきい値。リージョンの統合読み取りプールの CPU 使用率が 10 秒間連続して`region-cpu-overload-threshold-ratio`超えた場合、このリージョンを分割する必要があります。 (v6.2.0 以降でサポート) |
| `split.split-balance-score`                               | 2 つの分割されたリージョンの負荷が可能な限りバランスが取れていることを保証する`load-base-split`のパラメーター。値が小さいほど負荷が分散されます。ただし、小さすぎると分割に失敗する場合があります。                                             |
| `split.split-contained-score`                             | `load-base-split`のパラメーター。値が小さいほど、リージョン分割後のリージョン間の訪問が少なくなります。                                                                                            |
| `cdc.min-ts-interval`                                     | 解決済み TS が転送される時間間隔                                                                                                                                      |
| `cdc.old-value-cache-memory-quota`                        | TiCDC Old Value エントリが占有するメモリの上限                                                                                                                         |
| `cdc.sink-memory-quota`                                   | TiCDC データ変更イベントが占有するメモリの上限                                                                                                                              |
| `cdc.incremental-scan-speed-limit`                        | 履歴データのインクリメンタル スキャンの速度の上限                                                                                                                               |
| `cdc.incremental-scan-concurrency`                        | 履歴データの同時増分スキャン タスクの最大数                                                                                                                                  |

上記の表で、 `{db-name}`または`{db-name}.{cf-name}`プレフィックスが付いたパラメーターは、RocksDB に関連する構成です。 `db-name`のオプション値は`rocksdb`と`raftdb`です。

-   `db-name` `writecf` `rocksdb` `raftcf`場合、オプションの`cf-name`の値は`defaultcf` 、および`lockcf`です。
-   `db-name`が`raftdb`の場合、 `cf-name`の値は`defaultcf`になります。

詳細なパラメーターの説明については、 [TiKVコンフィグレーションファイル](/tikv-configuration-file.md)を参照してください。

### PD 構成を動的に変更する {#modify-pd-configuration-dynamically}

現在、PD はインスタンスごとに個別の構成をサポートしていません。すべての PD インスタンスは同じ構成を共有します。

次のステートメントを使用して、PD 構成を変更できます。

{{< copyable "" >}}

```sql
set config pd `log.level`='info';
```

変更が成功すると、 `Query OK`が返されます。

```sql
Query OK, 0 rows affected (0.01 sec)
```

構成アイテムが正常に変更された場合、結果は構成ファイルではなく etcd に保持されます。以降の操作では、etcd の構成が優先されます。一部の構成項目の名前は、TiDB の予約語と競合する場合があります。これらの構成アイテムについては、バッククォート`` ` ``を使用して囲みます。たとえば、 `` `schedule.leader-schedule-limit` ``です。

次の PD 構成アイテムは、動的に変更できます。

| コンフィグレーション項目                               | 説明                                       |
| :----------------------------------------- | :--------------------------------------- |
| `log.level`                                | ログレベル                                    |
| `cluster-version`                          | クラスターのバージョン                              |
| `schedule.max-merge-region-size`           | `Region Merge`のサイズ制限を制御します (MiB 単位)      |
| `schedule.max-merge-region-keys`           | `Region Merge`キーの最大数を指定します               |
| `schedule.patrol-region-interval`          | リージョンのヘルス状態を`replicaChecker`する頻度を決定します   |
| `schedule.split-merge-interval`            | 同じリージョンで分割およびマージ操作を実行する時間間隔を決定します        |
| `schedule.max-snapshot-count`              | 1 つのストアが同時に送受信できるスナップショットの最大数を決定します      |
| `schedule.max-pending-peer-count`          | 1 つのストア内の保留中のピアの最大数を決定します                |
| `schedule.max-store-down-time`             | 切断されたストアを復旧できないと PD が判断するまでのダウンタイム       |
| `schedule.leader-schedule-policy`          | Leaderのスケジューリングのポリシーを決定します               |
| `schedule.leader-schedule-limit`           | 同時に実行されるLeaderスケジューリング タスクの数             |
| `schedule.region-schedule-limit`           | 同時に実行されるリージョンスケジューリング タスクの数              |
| `schedule.replica-schedule-limit`          | 同時に実行されるレプリカ スケジューリング タスクの数              |
| `schedule.merge-schedule-limit`            | 同時に実行される`Region Merge`スケジューリング タスクの数     |
| `schedule.hot-region-schedule-limit`       | 同時に実行されるホットリージョンスケジューリング タスクの数           |
| `schedule.hot-region-cache-hits-threshold` | リージョンがホット スポットと見なされるしきい値を決定します           |
| `schedule.high-space-ratio`                | 店舗のキャパシティが十分である閾値比率                      |
| `schedule.low-space-ratio`                 | それを超えると店舗のキャパシティが不足するしきい値比率              |
| `schedule.tolerant-size-ratio`             | `balance`バッファ サイズを制御します                  |
| `schedule.enable-remove-down-replica`      | `DownReplica`を自動的に削除する機能を有効にするかどうかを決定します |
| `schedule.enable-replace-offline-replica`  | 移行する機能を有効にするかどうかを決定します`OfflineReplica`   |
| `schedule.enable-make-up-replica`          | レプリカを自動的に補完する機能を有効にするかどうかを決定します          |
| `schedule.enable-remove-extra-replica`     | 余分なレプリカを削除する機能を有効にするかどうかを決定します           |
| `schedule.enable-location-replacement`     | 分離レベルのチェックを有効にするかどうかを決定します               |
| `schedule.enable-cross-table-merge`        | クロステーブル マージを有効にするかどうかを決定します              |
| `schedule.enable-one-way-merge`            | 次の隣接するリージョンとのマージのみを許可する、一方向のマージを有効にします   |
| `replication.max-replicas`                 | レプリカの最大数を設定します                           |
| `replication.location-labels`              | TiKV クラスターのトポロジー情報                       |
| `replication.enable-placement-rules`       | 配置ルールを有効にします                             |
| `replication.strictly-match-label`         | ラベル チェックを有効にします                          |
| `pd-server.use-region-storage`             | 独立したリージョンstorageを有効にします                  |
| `pd-server.max-gap-reset-ts`               | タイムスタンプをリセットする最大間隔を設定します (BR)            |
| `pd-server.key-type`                       | クラスタ キーのタイプを設定します                        |
| `pd-server.metric-storage`                 | クラスタ メトリックのstorageアドレスを設定します             |
| `pd-server.dashboard-address`              | ダッシュボードのアドレスを設定します                       |
| `replication-mode.replication-mode`        | バックアップモードを設定します                          |

詳細なパラメーターの説明については、 [PDコンフィグレーションファイル](/pd-configuration-file.md)を参照してください。

### TiDB 構成を動的に変更する {#modify-tidb-configuration-dynamically}

現在、TiDB 構成を変更する方法は、TiKV および PD 構成を変更する方法とは異なります。 [システム変数](/system-variables.md)を使用して TiDB 構成を変更できます。

次の例は、 `tidb_slow_log_threshold`変数を使用して`slow-threshold`動的に変更する方法を示しています。

デフォルト値の`slow-threshold`は 300 ミリ秒です。 `tidb_slow_log_threshold`を使用して 200 ms に設定できます。

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

次の TiDB 構成項目は動的に変更できます。

| |コンフィグレーション項目 | SQL 変数 |説明 | | | :--- | :--- | | | `log.enable-slow-log` | `tidb_enable_slow_log` |スローログを有効にするかどうか | | | `log.slow-threshold` | `tidb_slow_log_threshold` |遅いログのしきい値 | | | `log.expensive-threshold` | `tidb_expensive_query_time_threshold` |高価なクエリのしきい値 |

### TiFlash構成を動的に変更する {#modify-tiflash-configuration-dynamically}

現在、システム変数[`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610)を使用してTiFlash構成`max_threads`を変更できます。この変数は、 TiFlashがリクエストを実行する最大同時実行数を指定します。

デフォルト値の`tidb_max_tiflash_threads`は`-1`で、このシステム変数が無効であり、 TiFlash構成ファイルの設定に依存することを示します。 `tidb_max_tiflash_threads`使用して`max_threads`から 10 を設定できます。

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
