---
title: Modify Configuration Dynamically
summary: Learn how to dynamically modify the cluster configuration.
---

# コンフィグレーションを動的に変更する {#modify-configuration-dynamically}

このドキュメントでは、クラスター構成を動的に変更する方法について説明します。

クラスターコンポーネントを再起動せずに、SQL ステートメントを使用してコンポーネント (TiDB、TiKV、PD など) の構成を動的に更新できます。現在、TiDB インスタンスの構成を変更する方法は、他のコンポーネント (TiKV や PD など) の構成を変更する方法とは異なります。

> **注記：**
>
> この機能は TiDB セルフホスト型にのみ適用され、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)では使用できません。 TiDB Cloudの場合、構成を変更するには[TiDB Cloudのサポート](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)に連絡する必要があります。

## 共通の操作 {#common-operations}

このセクションでは、構成を動的に変更する一般的な操作について説明します。

### インスタンス構成のビュー {#view-instance-configuration}

クラスター内のすべてのインスタンスの構成を表示するには、 `show config`ステートメントを使用します。結果は次のとおりです。

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

```sql
show config where type='tidb'
show config where instance in (...)
show config where name like '%log%'
show config where type='tikv' and name='log.level'
```

### TiKV 構成を動的に変更する {#modify-tikv-configuration-dynamically}

> **注記：**
>
> -   TiKV 構成項目を動的に変更した後、TiKV 構成ファイルは自動的に更新されます。ただし、 `tiup edit-config` ; を実行して、対応する構成項目を変更する必要もあります。そうしないと、 `upgrade`や`reload`などの操作によって変更が上書きされます。設定項目の変更の詳細については、 [TiUPを使用して構成を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration)を参照してください。
> -   `tiup edit-config`を実行した後、 `tiup reload`を実行する必要はありません。

`set config`ステートメントを使用すると、インスタンス アドレスまたはコンポーネントタイプに応じて、単一インスタンスまたはすべてのインスタンスの構成を変更できます。

-   すべての TiKV インスタンスの構成を変更します。

> **注記：**
>
> 変数名をバッククォートで囲むことをお勧めします。

```sql
set config tikv `split.qps-threshold`=1000;
```

-   単一の TiKV インスタンスの構成を変更します。

    ```sql
    set config "127.0.0.1:20180" `split.qps-threshold`=1000;
    ```

変更が成功すると、 `Query OK`が返されます。

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

バッチ変更は原子性を保証しません。変更は一部のインスタンスでは成功する可能性がありますが、他のインスタンスでは失敗する可能性があります。 `set tikv key=val`を使用して TiKV クラスター全体の構成を変更すると、一部のインスタンスで変更が失敗する可能性があります。 `show warnings`使用して結果を確認できます。

一部の変更が失敗した場合は、対応するステートメントを再実行するか、失敗した各インスタンスを変更する必要があります。ネットワークの問題またはマシンの障害により一部の TiKV インスタンスにアクセスできない場合は、回復後にこれらのインスタンスを変更します。

構成アイテムが正常に変更されると、結果は構成ファイルに保持され、後続の操作で優先されます。一部の構成項目の名前は、 `limit`や`key`などの TiDB 予約語と競合する可能性があります。これらの構成項目は、バッククォート`` ` ``を使用して囲みます。たとえば、 `` `raftstore.raft-log-gc-size-limit` `` 。

次の TiKV 構成項目は動的に変更できます。

| コンフィグレーション項目                                              | 説明                                                                                                                                                  |
| :-------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------- |
| ログレベル                                                     | ログレベル。                                                                                                                                              |
| `raftstore.raft-max-inflight-msgs`                        | 確認するRaft丸太の数。この数値を超えると、 Raftステート マシンのログ送信が遅くなります。                                                                                                   |
| `raftstore.raft-log-gc-tick-interval`                     | Raftログを削除するポーリング タスクがスケジュールされる時間間隔                                                                                                                  |
| `raftstore.raft-log-gc-threshold`                         | Raft丸太の最大許容数のソフトリミット                                                                                                                                |
| `raftstore.raft-log-gc-count-limit`                       | Raftの残存丸太の許容数のハードリミット                                                                                                                               |
| `raftstore.raft-log-gc-size-limit`                        | Raftの残存丸太の許容サイズに対する厳しい制限                                                                                                                            |
| `raftstore.raft-max-size-per-msg`                         | 生成が許可される単一メッセージ パケットのサイズのソフト制限                                                                                                                      |
| `raftstore.raft-entry-max-size`                           | 単一のRaftログの最大サイズに対するハードリミット                                                                                                                          |
| `raftstore.raft-entry-cache-life-time`                    | メモリ内のログ キャッシュに許可される最大残り時間                                                                                                                           |
| `raftstore.split-region-check-tick-interval`              | リージョン分割が必要かどうかを確認する時間間隔                                                                                                                             |
| `raftstore.region-split-check-diff`                       | リージョン分割前にリージョンデータが超えることが許可される最大値                                                                                                                    |
| `raftstore.region-compact-check-interval`                 | RocksDB の圧縮を手動でトリガーする必要があるかどうかを確認する時間間隔                                                                                                             |
| `raftstore.region-compact-check-step`                     | 手動圧縮の各ラウンドで一度にチェックされるリージョンの数                                                                                                                        |
| `raftstore.region-compact-min-tombstones`                 | RocksDB の圧縮をトリガーするために必要なトゥームストーンの数                                                                                                                  |
| `raftstore.region-compact-tombstones-percent`             | RocksDB の圧縮をトリガーするために必要なトゥームストーンの割合                                                                                                                 |
| `raftstore.pd-heartbeat-tick-interval`                    | リージョンの PD へのハートビートがトリガーされる時間間隔                                                                                                                      |
| `raftstore.pd-store-heartbeat-tick-interval`              | ストアの PD へのハートビートがトリガーされる時間間隔                                                                                                                        |
| `raftstore.snap-mgr-gc-tick-interval`                     | 期限切れのスナップショット ファイルのリサイクルがトリガーされる時間間隔                                                                                                                |
| `raftstore.snap-gc-timeout`                               | スナップショット ファイルが保存される最長時間                                                                                                                             |
| `raftstore.lock-cf-compact-interval`                      | TiKV がロックカラムファミリーの手動圧縮をトリガーする時間間隔                                                                                                                   |
| `raftstore.lock-cf-compact-bytes-threshold`               | TiKV がロックカラムファミリーの手動圧縮をトリガーするサイズ                                                                                                                    |
| `raftstore.messages-per-tick`                             | バッチごとに処理されるメッセージの最大数                                                                                                                                |
| `raftstore.max-peer-down-duration`                        | ピアに許可される非アクティブ期間の最長値                                                                                                                                |
| `raftstore.max-leader-missing-duration`                   | リーダーなしでピアが存在できる最長期間。この値を超えると、ピアは PD を使用して、ピアが削除されたかどうかを確認します。                                                                                       |
| `raftstore.abnormal-leader-missing-duration`              | ピアがリーダーなしで存在できる通常の期間。この値を超えると、ピアは異常とみなされ、メトリクスとログにマークが付けられます。                                                                                       |
| `raftstore.peer-stale-state-check-interval`               | ピアにリーダーが存在しないかどうかを確認する時間間隔                                                                                                                          |
| `raftstore.consistency-check-interval`                    | 整合性をチェックする時間間隔 (TiDB のガベージコレクションと互換性がないため推奨され**ません**)                                                                                               |
| `raftstore.raft-store-max-leader-lease`                   | Raftのリーダーとして最も長く信頼されていた期間                                                                                                                           |
| `raftstore.merge-check-tick-interval`                     | マージチェックの時間間隔                                                                                                                                        |
| `raftstore.cleanup-import-sst-interval`                   | 期限切れの SST ファイルをチェックする時間間隔                                                                                                                           |
| `raftstore.local-read-batch-size`                         | 1 回のバッチで処理される読み取りリクエストの最大数                                                                                                                          |
| `raftstore.apply-yield-write-size`                        | 適用スレッドが各ラウンドで 1 つの FSM (有限状態マシン) に対して書き込むことができる最大バイト数                                                                                               |
| `raftstore.hibernate-timeout`                             | 起動時に休止状態に入るまでの最短の待機時間。この期間内では、TiKV は休止状態になりません (解放されません)。                                                                                           |
| `raftstore.apply-pool-size`                               | データをディスクにフラッシュするプール内のスレッドの数。これは、適用スレッド プールのサイズです。                                                                                                   |
| `raftstore.store-pool-size`                               | Raftを処理するプール内のスレッドの数 ( Raftstoreスレッド プールのサイズ)                                                                                                       |
| `raftstore.apply-max-batch-size`                          | Raftステート マシンは、BatchSystem によってデータ書き込みリクエストをバッチで処理します。この設定項目は、1 つのバッチでリクエストを実行できるRaftステート マシンの最大数を指定します。                                             |
| `raftstore.store-max-batch-size`                          | Raftステート マシンは、BatchSystem によってバッチでディスクにログをフラッシュするリクエストを処理します。この設定項目は、1 つのバッチでリクエストを処理できるRaftステート マシンの最大数を指定します。                                     |
| `raftstore.store-io-pool-size`                            | Raft I/O タスクを処理するスレッドの数。これは StoreWriter スレッド プールのサイズでもあります (この値をゼロ以外の値から 0 に、または 0 からゼロ以外の値に変更し**ないでください**)。                                        |
| `readpool.unified.max-thread-count`                       | 読み取りリクエストを均一に処理するスレッド プール内のスレッドの最大数。UnifyReadPool スレッド プールのサイズです。                                                                                   |
| `readpool.unified.auto-adjust-pool-size`                  | UnifyReadPool スレッド プール サイズを自動的に調整するかどうかを決定します                                                                                                       |
| `coprocessor.split-region-on-table`                       | テーブルごとにリージョンを分割できるようにします                                                                                                                            |
| `coprocessor.batch-split-limit`                           | バッチでのリージョン分割のしきい値                                                                                                                                   |
| `coprocessor.region-max-size`                             | リージョンの最大サイズ                                                                                                                                         |
| `coprocessor.region-split-size`                           | 新しく分割されたリージョンのサイズ                                                                                                                                   |
| `coprocessor.region-max-keys`                             | リージョン内で許可されるキーの最大数                                                                                                                                  |
| `coprocessor.region-split-keys`                           | 新しく分割されたリージョン内のキーの数                                                                                                                                 |
| `pessimistic-txn.wait-for-lock-timeout`                   | 悲観的トランザクションがロックを待機する最長期間                                                                                                                            |
| `pessimistic-txn.wake-up-delay-duration`                  | 悲観的トランザクションがウェイクアップされるまでの期間                                                                                                                         |
| `pessimistic-txn.pipelined`                               | パイプライン化された悲観的ロック プロセスを有効にするかどうかを決定します。                                                                                                              |
| `pessimistic-txn.in-memory`                               | メモリ内の悲観的ロックを有効にするかどうかを決定します。                                                                                                                        |
| `quota.foreground-cpu-time`                               | TiKV フォアグラウンドが読み取りおよび書き込みリクエストを処理するために使用する CPU リソースのソフト制限                                                                                           |
| `quota.foreground-write-bandwidth`                        | フォアグラウンド トランザクションがデータを書き込む帯域幅のソフト制限                                                                                                                 |
| `quota.foreground-read-bandwidth`                         | フォアグラウンド トランザクションとコプロセッサーがデータを読み取る帯域幅のソフト制限                                                                                                         |
| `quota.background-cpu-time`                               | 読み取りおよび書き込みリクエストを処理するために TiKV バックグラウンドで使用される CPU リソースのソフト制限                                                                                         |
| `quota.background-write-bandwidth`                        | バックグラウンド トランザクションがデータを書き込む帯域幅のソフト制限 (まだ有効ではありません)                                                                                                   |
| `quota.background-read-bandwidth`                         | バックグラウンド トランザクションとコプロセッサーがデータを読み取る帯域幅のソフト制限 (まだ有効ではありません)                                                                                           |
| `quota.enable-auto-tune`                                  | クォータの自動調整を有効にするかどうか。この構成項目が有効になっている場合、TiKV は TiKV インスタンスの負荷に基づいてバックグラウンド リクエストのクォータを動的に調整します。                                                       |
| `quota.max-delay-duration`                                | 単一の読み取りまたは書き込みリクエストがフォアグラウンドで処理されるまで強制的に待機する最大時間                                                                                                    |
| `gc.ratio-threshold`                                      | リージョンGC がスキップされるしきい値 (GC バージョン数 / キー数)                                                                                                              |
| `gc.batch-keys`                                           | 1 回のバッチで処理されるキーの数                                                                                                                                   |
| `gc.max-write-bytes-per-sec`                              | RocksDB に 1 秒あたりに書き込むことができる最大バイト数                                                                                                                   |
| `gc.enable-compaction-filter`                             | コンパクションフィルターを有効にするかどうか                                                                                                                              |
| `gc.compaction-filter-skip-version-check`                 | コンパクションフィルターのクラスターバージョンチェックをスキップするかどうか(未リリース)                                                                                                       |
| `{db-name}.max-total-wal-size`                            | WAL 合計の最大サイズ                                                                                                                                        |
| `{db-name}.max-background-jobs`                           | RocksDB のバックグラウンド スレッドの数                                                                                                                            |
| `{db-name}.max-background-flushes`                        | RocksDB のフラッシュ スレッドの最大数                                                                                                                             |
| `{db-name}.max-open-files`                                | RocksDB が開くことができるファイルの総数                                                                                                                            |
| `{db-name}.compaction-readahead-size`                     | 圧縮時の`readahead`のサイズ                                                                                                                                 |
| `{db-name}.bytes-per-sync`                                | ファイルが非同期で書き込まれている間に、OS がファイルをディスクに増分同期する速度。                                                                                                         |
| `{db-name}.wal-bytes-per-sync`                            | WAL ファイルの書き込み中に OS が WAL ファイルをディスクに増分同期する速度                                                                                                         |
| `{db-name}.writable-file-max-buffer-size`                 | WritableFileWrite で使用される最大バッファ サイズ                                                                                                                  |
| `{db-name}.{cf-name}.block-cache-size`                    | ブロックのキャッシュサイズ                                                                                                                                       |
| `{db-name}.{cf-name}.write-buffer-size`                   | memtableのサイズ                                                                                                                                        |
| `{db-name}.{cf-name}.max-write-buffer-number`             | memtable の最大数                                                                                                                                       |
| `{db-name}.{cf-name}.max-bytes-for-level-base`            | 基本レベル (L1) の最大バイト数                                                                                                                                  |
| `{db-name}.{cf-name}.target-file-size-base`               | 基本レベルでのターゲット ファイルのサイズ                                                                                                                               |
| `{db-name}.{cf-name}.level0-file-num-compaction-trigger`  | 圧縮をトリガーする L0 のファイルの最大数                                                                                                                              |
| `{db-name}.{cf-name}.level0-slowdown-writes-trigger`      | 書き込み停止をトリガーする L0 のファイルの最大数                                                                                                                          |
| `{db-name}.{cf-name}.level0-stop-writes-trigger`          | 書き込みを完全にブロックする L0 のファイルの最大数                                                                                                                         |
| `{db-name}.{cf-name}.max-compaction-bytes`                | 圧縮ごとにディスクに書き込まれる最大バイト数                                                                                                                              |
| `{db-name}.{cf-name}.max-bytes-for-level-multiplier`      | レイヤーのデフォルトの増幅倍数                                                                                                                                     |
| `{db-name}.{cf-name}.disable-auto-compactions`            | 自動圧縮を有効または無効にします。                                                                                                                                   |
| `{db-name}.{cf-name}.soft-pending-compaction-bytes-limit` | 保留中の圧縮バイトのソフト制限                                                                                                                                     |
| `{db-name}.{cf-name}.hard-pending-compaction-bytes-limit` | 保留中の圧縮バイトのハード制限                                                                                                                                     |
| `{db-name}.{cf-name}.titan.blob-run-mode`                 | BLOB ファイルの処理モード                                                                                                                                     |
| `server.grpc-memory-pool-quota`                           | gRPC が使用できるメモリサイズを制限します。                                                                                                                            |
| `server.max-grpc-send-msg-len`                            | 送信できる gRPC メッセージの最大長を設定します                                                                                                                          |
| `server.snap-io-max-bytes-per-sec`                        | スナップショットを処理するときに許容される最大ディスク帯域幅を設定します                                                                                                                |
| `server.concurrent-send-snap-limit`                       | 同時に送信されるスナップショットの最大数を設定します                                                                                                                          |
| `server.concurrent-recv-snap-limit`                       | 同時に受信するスナップショットの最大数を設定します                                                                                                                           |
| `server.raft-msg-max-batch-size`                          | 単一の gRPC メッセージに含まれるRaftメッセージの最大数を設定します。                                                                                                             |
| `server.simplify-metrics`                                 | サンプリング監視メトリクスを簡素化するかどうかを制御します                                                                                                                       |
| `storage.block-cache.capacity`                            | 共有ブロックキャッシュのサイズ (v4.0.3 以降サポート)                                                                                                                     |
| `storage.scheduler-worker-pool-size`                      | スケジューラのスレッド プール内のスレッドの数                                                                                                                             |
| `backup.num-threads`                                      | バックアップ スレッドの数 (v4.0.3 以降サポート)                                                                                                                       |
| `split.qps-threshold`                                     | リージョンで`load-base-split`を実行するためのしきい値。リージョンの読み取りリクエストの QPS が 10 秒連続で`qps-threshold`を超える場合、このリージョンを分割する必要があります。                                        |
| `split.byte-threshold`                                    | リージョンで`load-base-split`を実行するためのしきい値。リージョンの読み取りリクエストのトラフィックが 10 秒連続で`byte-threshold`を超える場合、このリージョンを分割する必要があります。                                      |
| `split.region-cpu-overload-threshold-ratio`               | リージョンで`load-base-split`を実行するためのしきい値。リージョンの統合読み取りプールの CPU 使用率が 10 秒連続で`region-cpu-overload-threshold-ratio`超える場合、このリージョンを分割する必要があります。 (v6.2.0以降サポート) |
| `split.split-balance-score`                               | パラメータ`load-base-split`は、2 つの分割リージョンの負荷が可能な限りバランスされるようにします。値が小さいほど、負荷のバランスが取れています。ただし、小さすぎる値を設定すると、分割エラーが発生する可能性があります。                               |
| `split.split-contained-score`                             | `load-base-split`のパラメータ。値が小さいほど、リージョン分割後のリージョン間の訪問が少なくなります。                                                                                         |
| `cdc.min-ts-interval`                                     | Resolved TSが転送される時間間隔                                                                                                                               |
| `cdc.old-value-cache-memory-quota`                        | TiCDC Old Value エントリが占有するメモリの上限                                                                                                                     |
| `cdc.sink-memory-quota`                                   | TiCDC データ変更イベントが占有するメモリの上限                                                                                                                          |
| `cdc.incremental-scan-speed-limit`                        | 履歴データの増分スキャン速度の上限                                                                                                                                   |
| `cdc.incremental-scan-concurrency`                        | 履歴データの同時増分スキャン タスクの最大数                                                                                                                              |

上の表で、接頭辞`{db-name}`または`{db-name}.{cf-name}`が付いているパラメータは、RocksDB に関連する設定です。 `db-name`のオプションの値は`rocksdb`と`raftdb`です。

-   `db-name` `writecf` `rocksdb` `raftcf`場合、 `cf-name`のオプションの値は`defaultcf` 、および`lockcf`です。
-   `db-name`が`raftdb`場合、 `cf-name`の値は`defaultcf`になる可能性があります。

パラメータの詳細な説明については、 [TiKVコンフィグレーションファイル](/tikv-configuration-file.md)を参照してください。

### PD構成を動的に変更する {#modify-pd-configuration-dynamically}

現在、PD はインスタンスごとに個別の構成をサポートしていません。すべての PD インスタンスは同じ構成を共有します。

次のステートメントを使用して PD 構成を変更できます。

```sql
set config pd `log.level`='info';
```

変更が成功すると、 `Query OK`が返されます。

```sql
Query OK, 0 rows affected (0.01 sec)
```

設定項目が正常に変更されると、結果は設定ファイルではなく etcd に保存されます。 etcd の設定が後続の操作に優先されます。一部の構成項目の名前は、TiDB の予約語と競合する可能性があります。これらの構成項目については、バッククォート`` ` ``を使用してそれらを囲みます。たとえば、 `` `schedule.leader-schedule-limit` `` 。

次の PD 構成項目は動的に変更できます。

| コンフィグレーション項目                               | 説明                                              |
| :----------------------------------------- | :---------------------------------------------- |
| `log.level`                                | ログレベル                                           |
| `cluster-version`                          | クラスターのバージョン                                     |
| `schedule.max-merge-region-size`           | サイズ制限を`Region Merge` (MiB 単位) に制御します。           |
| `schedule.max-merge-region-keys`           | `Region Merge`キーの最大数を指定します                      |
| `schedule.patrol-region-interval`          | `replicaChecker`の健全性状態をチェックする頻度を決定します。          |
| `schedule.split-merge-interval`            | 同じリージョンで分割およびマージ操作を実行する時間間隔を決定します。              |
| `schedule.max-snapshot-count`              | 単一ストアが同時に送信または受信できるスナップショットの最大数を決定します。          |
| `schedule.max-pending-peer-count`          | 単一ストア内の保留中のピアの最大数を決定します。                        |
| `schedule.max-store-down-time`             | 切断されたストアを回復できないとPDが判断するまでのダウンタイム                |
| `schedule.leader-schedule-policy`          | Leaderのスケジューリングのポリシーを決定します                      |
| `schedule.leader-schedule-limit`           | 同時に実行されるLeaderのスケジュール設定タスクの数                    |
| `schedule.region-schedule-limit`           | 同時に実行されるリージョンスケジュール タスクの数                       |
| `schedule.replica-schedule-limit`          | 同時に実行されるレプリカのスケジューリング タスクの数                     |
| `schedule.merge-schedule-limit`            | 同時に実行される`Region Merge`スケジューリング タスクの数            |
| `schedule.hot-region-schedule-limit`       | 同時に実行されるホットリージョンスケジューリング タスクの数                  |
| `schedule.hot-region-cache-hits-threshold` | リージョンがホットスポットとみなされるしきい値を決定します。                  |
| `schedule.high-space-ratio`                | ストアのキャパシティがそれ以下であれば十分であるというしきい値比率               |
| `schedule.low-space-ratio`                 | ストアの容量が不足するしきい値比率                               |
| `schedule.tolerant-size-ratio`             | `balance`バッファ サイズを制御します                         |
| `schedule.enable-remove-down-replica`      | `DownReplica`を自動的に削除する機能を有効にするかどうかを決定します。       |
| `schedule.enable-replace-offline-replica`  | 移行する機能を有効にするかどうかを決定します`OfflineReplica`          |
| `schedule.enable-make-up-replica`          | レプリカを自動的に補完する機能を有効にするかどうかを決定します。                |
| `schedule.enable-remove-extra-replica`     | 余分なレプリカを削除する機能を有効にするかどうかを決定します。                 |
| `schedule.enable-location-replacement`     | 分離レベルチェックを有効にするかどうかを決定します                       |
| `schedule.enable-cross-table-merge`        | テーブル間のマージを有効にするかどうかを決定します                       |
| `schedule.enable-one-way-merge`            | 一方向のマージを有効にします。これにより、次に隣接するリージョンとのマージのみが許可されます。 |
| `replication.max-replicas`                 | レプリカの最大数を設定します                                  |
| `replication.location-labels`              | TiKVクラスターのトポロジー情報                               |
| `replication.enable-placement-rules`       | 配置ルールを有効にする                                     |
| `replication.strictly-match-label`         | ラベルチェックを有効にします                                  |
| `pd-server.use-region-storage`             | 独立したリージョンstorageを有効にする                          |
| `pd-server.max-gap-reset-ts`               | タイムスタンプ (BR) をリセットする最大間隔を設定します。                 |
| `pd-server.key-type`                       | クラスターキーのタイプを設定します                               |
| `pd-server.metric-storage`                 | クラスターメトリックのstorageアドレスを設定します                    |
| `pd-server.dashboard-address`              | ダッシュボードのアドレスを設定します                              |
| `replication-mode.replication-mode`        | バックアップモードを設定します                                 |

パラメータの詳細な説明については、 [PDコンフィグレーションファイル](/pd-configuration-file.md)を参照してください。

### TiDB 構成を動的に変更する {#modify-tidb-configuration-dynamically}

現在、TiDB 構成を変更する方法は、TiKV および PD 構成を変更する方法とは異なります。 [システム変数](/system-variables.md)を使用して TiDB 構成を変更できます。

次の例は、変数`tidb_slow_log_threshold`を使用して`slow-threshold`動的に変更する方法を示しています。

デフォルト値の`slow-threshold`は 300 ミリ秒です。 `tidb_slow_log_threshold`を使用すると、200 ミリ秒に設定できます。

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

|コンフィグレーション項目 | SQL 変数 |説明 | | :--- | :--- | | `instance.tidb_enable_slow_log` | `tidb_enable_slow_log` |スローログを有効にするかどうか | | `instance.tidb_slow_log_threshold` | `tidb_slow_log_threshold` |スローログのしきい値 | | `instance.tidb_expensive_query_time_threshold` | `tidb_expensive_query_time_threshold` |高価なクエリのしきい値 |

### TiFlash構成を動的に変更する {#modify-tiflash-configuration-dynamically}

現在、システム変数[`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610)を使用してTiFlash構成`max_threads`を変更できます。これは、 TiFlash がリクエストを実行するための最大同時実行数を指定します。

デフォルト値`tidb_max_tiflash_threads`は`-1`で、このシステム変数が無効であり、 TiFlash構成ファイルの設定に依存することを示します。 `tidb_max_tiflash_threads`を使用して`max_threads` ～ 10 を設定できます。

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
