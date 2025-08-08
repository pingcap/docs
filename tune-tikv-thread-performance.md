---
title: Tune TiKV Thread Pool Performance
summary: 最適なパフォーマンスを得るために TiKV スレッド プールを調整する方法を学習します。
---

# TiKV スレッドプールのパフォーマンスを調整する {#tune-tikv-thread-pool-performance}

このドキュメントでは、TiKV 内部スレッド プールとそのパフォーマンスを調整する方法について説明します。

## スレッドプールの導入 {#thread-pool-introduction}

TiKVスレッドプールは、主にgRPC、Scheduler、UnifyReadPool、 Raftstore、StoreWriter、Apply、RocksDB、そしてCPUをあまり消費しないいくつかのスケジュールタスクと検出コンポーネントで構成されています。このドキュメントでは、主に読み取りおよび書き込みリクエストのパフォーマンスに影響を与える、CPUを大量に消費するスレッドプールをいくつか紹介します。

-   gRPC スレッド プール: すべてのネットワーク リクエストを処理し、さまざまなタスク タイプのリクエストをさまざまなスレッド プールに転送します。

-   スケジューラ スレッド プール: 書き込みトランザクションの競合を検出し、2 フェーズ コミット、悲観的ロック、トランザクション ロールバックなどの要求をキーと値のペアの配列に変換し、 RaftログのレプリケーションのためにRaftstoreスレッドに送信します。

-   Raftstoreスレッド プール:

    -   すべてのRaftメッセージと新しいログを追加する提案を処理します。
    -   Raftログをディスクに書き込みます。1の値が[`store-io-pool-size`](/tikv-configuration-file.md#store-io-pool-size-new-in-v530) `0`場合、 Raftstoreスレッドはログをディスクに書き込みます。値が`0`でない場合、 RaftstoreスレッドはログをStoreWriterスレッドに送信します。
    -   大部分のレプリカのRaftログが整合している場合、 Raftstoreスレッドはログを適用スレッドに送信します。

-   StoreWriter スレッド プール: すべてのRaftログをディスクに書き込み、結果をRaftstoreスレッドに返します。

-   Apply スレッド プール: Raftstoreスレッド プールから送信された送信ログを受信し、それをキー値要求として解析し、RocksDB に書き込み、コールバック関数を呼び出して gRPC スレッド プールに書き込み要求が完了したことを通知し、結果をクライアントに返します。

-   RocksDBスレッドプール：RocksDBがタスクを圧縮およびフラッシュするためのスレッドプールです。RocksDBのアーキテクチャと`Compact`操作については、 [RocksDB: フラッシュと RAM ストレージ用の永続的なキーバリューストア](https://github.com/facebook/rocksdb)を参照してください。

-   UnifyReadPool スレッドプール：コプロセッサースレッドプールとストレージ読み取りプールを組み合わせたものです。kv get、kv batch get、raw kv get、コプロセッサなどのすべての読み取り要求はこのスレッドプールで実行されます。

## TiKV読み取り専用リクエスト {#tikv-read-only-requests}

TiKV の読み取り要求は次の種類に分類されます。

-   ストレージ読み取りプールで実行される、特定の行または複数の行を指定する単純なクエリ。
-   コプロセッサー読み取りプールで実行される複雑な集計計算と範囲クエリ。

TiKV v5.0以降、すべての読み取りリクエストはデフォルトでクエリ用の統合スレッドプールを使用します。TiKVクラスターをTiKV v4.0からアップグレードし、アップグレード前に`use-unified-pool`構成の`readpool.storage` `false`に設定していた場合、アップグレード後もすべての読み取りリクエストは引き続き異なるスレッドプールを使用します。このシナリオでは、すべての読み取りリクエストがクエリ用の統合スレッドプールを使用するようにするには、 `readpool.storage.use-unified-pool`を`true`に設定します。

## TiKV スレッドプールのパフォーマンスチューニング {#performance-tuning-for-tikv-thread-pools}

-   gRPC スレッド プール。

    gRPC スレッドプールのデフォルトサイズ（ `server.grpc-concurrency`に設定）は`5`です。このスレッドプールにはコンピューティングオーバーヘッドはほとんどなく、主にネットワーク I/O とデシリアライズリクエストを処理するため、通常はデフォルト設定を調整する必要はありません。

    -   TiKV がデプロイされたマシンの CPU コア数が少ない (8 個以下) 場合は、 `server.grpc-concurrency`構成項目を`2`に設定することを検討してください。
    -   TiKV を導入したマシンの構成が非常に高く、TiKV が大量の読み取りおよび書き込み要求を処理し、Grafana でスレッド CPU を監視する値`gRPC poll CPU`が`server.grpc-concurrency`の 80% を超える場合は、スレッド プールの使用率を 80% 未満 (つまり、Grafana のメトリックが`80% * server.grpc-concurrency`未満) に保つために値`server.grpc-concurrency`を増やすことを検討してください。

-   スケジューラ スレッド プール。

    TiKV がマシンの CPU コアの数が 16 以上であることを検出すると、スケジューラ スレッド プールのデフォルト サイズ ( `storage.scheduler-worker-pool-size`に設定) は`8`なります。TiKV がマシンの CPU コアの数が 16 未満であることを検出すると、デフォルト サイズは`4`なります。

    このスレッドプールは主に、複雑なトランザクションリクエストを単純なキー値の読み取り/書き込みリクエストに変換するために使用されます。ただし、**スケジューラスレッドプール自体は書き込み操作を実行しません**。

    -   トランザクションの競合が検出されると、このスレッド プールは競合の結果を事前にクライアントに返します。
    -   競合が検出されない場合、このスレッド プールは書き込み操作を実行するキー値要求をRaftログにマージし、 RaftログのレプリケーションのためにRaftstoreスレッドに送信します。

    一般的に、過度のスレッド切り替えを避けるには、スケジューラのスレッドプールの使用率を50%～75%に保つことが最善です。スレッドプールのサイズが`8`場合、Grafanaでは400%～600%の範囲で`TiKV-Details.Thread CPU.scheduler worker CPU`維持することをお勧めします。

-   Raftstoreスレッド プール。

    Raftstoreスレッドプールは、TiKV で最も複雑なスレッドプールです。このスレッドプールのデフォルトサイズ（ `raftstore.store-pool-size`で設定）は`2` 。StoreWriter スレッドプールのデフォルトサイズ（ `raftstore.store-io-pool-size`で設定）は`1`です。

    -   StoreWriterスレッドプールのサイズが0の場合、すべての書き込みリクエストはRaftstoreスレッドによって`fsync`としてRocksDBに書き込まれます。この場合、以下の方法でパフォーマンスをチューニングすることをお勧めします。

        -   Raftstoreスレッド全体のCPU使用率を60%未満に保ちます。Raftstoreスレッド数が2の場合、 **TiKV-Details** 、 **Thread CPU** 、Grafanaの**Raft store CPUを**120 %未満に保ちます。I/Oリクエストにより、 RaftstoreスレッドのCPU使用率は理論上は常に100%未満になります。
        -   書き込みパフォーマンスを向上させるために、 Raftstoreスレッド プールのサイズを慎重に検討せずに増やさないでください。そうすると、ディスクの負担が増加し、パフォーマンスが低下する可能性があります。

    -   StoreWriterスレッドプールのサイズが0でない場合、すべての書き込みリクエストはStoreWriterスレッドによって`fsync`としてRocksDBに書き込まれます。この場合、以下の方法でパフォーマンスをチューニングすることをお勧めします。

        -   StoreWriterスレッドプールは、CPUリソース全体が十分である場合にのみ有効にしてください。StoreWriterスレッドプールを有効にする際は、StoreWriterスレッドとRaftstoreスレッドのCPU使用率を80%未満に抑えてください。

        書き込み要求がRaftstoreスレッドで処理される場合と比較して、理論上は、書き込み要求が StoreWriter スレッドで処理される場合、書き込みレイテンシーとデータ読み取りのテールレイテンシーが大幅に削減されます。ただし、書き込み速度が高速化すると、それに応じてRaftログの数が増加します。これにより、 Raftstoreスレッド、Apply スレッド、および gRPC スレッドの CPU オーバーヘッドが増加する可能性があります。この場合、CPU リソースが不足するとチューニング効果が打ち消され、結果として書き込み速度が以前よりも遅くなる可能性があります。したがって、CPU リソースが十分でない場合は、StoreWriter スレッドを有効にすることは推奨されません。Raftstore スレッドはほとんどの I/O 要求をRaftstoreスレッドに送信するため、 Raftstoreスレッドの CPU 使用率を 80% 未満に維持する必要があります。

    -   ほとんどの場合、StoreWriter スレッドプールのサイズは 1 または 2 に設定してください。これは、StoreWriter スレッドプールのサイズがRaftログの数に影響するため、スレッドプールのサイズを大きくしすぎないようにするためです。CPU 使用率が 80% を超える場合は、スレッドプールのサイズを増やすことを検討してください。

    -   Raftログの増加が他のスレッドプールのCPUオーバーヘッドに与える影響に注意してください。必要に応じて、 Raftstoreスレッド、Applyスレッド、gRPCスレッドの数を増やす必要があります。

-   UnifyReadPool スレッド プール。

    UnifyReadPool はすべての読み取りリクエストの処理を担当します。デフォルトのサイズ（ `readpool.unified.max-thread-count`に設定）は、マシンの CPU コア数の 80% です。例えば、マシンの CPU コア数が 16 の場合、デフォルトのスレッドプールサイズは 12 です。アプリケーションのワークロードに応じて CPU 使用率を調整し、スレッドプールサイズの 60% から 90% の範囲に維持することをお勧めします。

    Grafanaの`TiKV-Details.Thread CPU.Unified read pool CPU`のピーク値が800%を超えない場合は、 `readpool.unified.max-thread-count` ～ `10`に設定することをお勧めします。スレッド数が多すぎると、スレッドの切り替えが頻繁に発生し、他のスレッドプールのリソースを消費する可能性があります。

    v6.3.0以降、TiKVは現在のCPU使用率に基づいてUnifyReadPoolスレッドプールサイズを自動調整する機能をサポートしています。この機能を有効にするには、 [`readpool.unified.auto-adjust-pool-size = true`](/tikv-configuration-file.md#auto-adjust-pool-size-new-in-v630)設定します。再読み取りが行われ、最大CPU使用率が80%を超えるクラスターについては、スレッドプールサイズを自動調整することをお勧めします。

-   RocksDB スレッド プール。

    RocksDBスレッドプールは、RocksDBがタスクを圧縮およびフラッシュするためのスレッドプールです。通常は設定する必要はありません。

    -   マシンの CPU コア数が少ない場合は、 `rocksdb.max-background-jobs`と`raftdb.max-background-jobs`両方を`4`に設定します。
    -   書き込みストールが発生した場合は、Grafana の**RocksDB-kv**の Write Stall Reason に移動し、 `0`以外のメトリックを確認します。

        -   保留中の圧縮バイトに関連する理由によって発生した場合は、 `rocksdb.max-sub-compactions`を`2`または`3`に設定してください。この設定項目は、単一の圧縮ジョブで許可されるサブスレッドの数を示します。デフォルト値は、TiKV 4.0 では`3` 、TiKV 3.0 では`1`です。
        -   理由が memtable 数に関連している場合は、すべての列の`max-write-buffer-number` (デフォルトでは`5` ) を増やすことをお勧めします。
        -   理由がレベル 0 のファイル制限に関連している場合は、次のパラメータの値を`64`以上に増やすことをお勧めします。

                rocksdb.defaultcf.level0-slowdown-writes-trigger
                rocksdb.writecf.level0-slowdown-writes-trigger
                rocksdb.lockcf.level0-slowdown-writes-trigger
                rocksdb.defaultcf.level0-stop-writes-trigger
                rocksdb.writecf.level0-stop-writes-trigger
                rocksdb.lockcf.level0-stop-writes-trigger
