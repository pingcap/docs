---
title: Tune TiKV Thread Pool Performance
summary: Learn how to tune TiKV thread pools for optimal performance.
---

# TiKVスレッドプールのパフォーマンスを調整する {#tune-tikv-thread-pool-performance}

このドキュメントでは、TiKV内部スレッドプールとそのパフォーマンスを調整する方法を紹介します。

## スレッドプールの紹介 {#thread-pool-introduction}

TiKVスレッドプールは、主にgRPC、Scheduler、UnifyReadPool、Raftstore、StoreWriter、Apply、RocksDB、およびCPUをあまり消費しないいくつかのスケジュールされたタスクと検出コンポーネントで構成されています。このドキュメントでは、主に、読み取りおよび書き込み要求のパフォーマンスに影響を与えるCPUを集中的に使用するスレッドプールをいくつか紹介します。

-   gRPCスレッドプール：すべてのネットワークリクエストを処理し、さまざまなタスクタイプのリクエストをさまざまなスレッドプールに転送します。

-   スケジューラスレッドプール：書き込みトランザクションの競合を検出し、2フェーズコミット、ペシミスティックロック、トランザクションロールバックなどの要求をキーと値のペアの配列に変換してから、RaftログレプリケーションのためにRaftstoreスレッドに送信します。

-   Raftstoreスレッドプール：

    -   すべてのRaftメッセージと、新しいログを追加するための提案を処理します。
    -   Raftログをディスクに書き込みます。 [`store-io-pool-size`](/tikv-configuration-file.md#store-io-pool-size-new-in-v530)の値が`0`の場合、Raftstoreスレッドはログをディスクに書き込みます。値が`0`でない場合、RaftstoreスレッドはログをStoreWriterスレッドに送信します。
    -   大部分のレプリカのRaftログに一貫性がある場合、RaftstoreスレッドはログをApplyスレッドに送信します。

-   StoreWriterスレッドプール：すべてのRaftログをディスクに書き込み、結果をRaftstoreスレッドに返します。

-   スレッドプールの適用：Raftstoreスレッドプールから送信された送信済みログを受信し、それをキー値要求として解析してからRocksDBに書き込み、コールバック関数を呼び出して書き込み要求が完了したことをgRPCスレッドプールに通知します。結果をクライアントに返します。

-   RocksDBスレッドプール：これは、RocksDBがタスクを圧縮およびフラッシュするためのスレッドプールです。 RocksDBのアーキテクチャと`Compact`の操作については、 [RocksDB：フラッシュおよびRAMストレージ用の永続的なKey-Valueストア](https://github.com/facebook/rocksdb)を参照してください。

-   UnifyReadPoolスレッドプール：コプロセッサースレッドプールとストレージ読み取りプールの組み合わせです。 kv get、kv batch get、raw kv get、コプロセッサーなどのすべての読み取り要求は、このスレッドプールで実行されます。

## TiKV読み取り専用リクエスト {#tikv-read-only-requests}

TiKVの読み取り要求は、次のタイプに分けられます。

-   ストレージ読み取りプールで実行される、特定の行または複数の行を指定する単純なクエリ。
-   コプロセッサー読み取りプールで実行される、複雑な集計計算と範囲クエリ。

TiKV v5.0以降、すべての読み取り要求は、デフォルトでクエリに統合スレッドプールを使用します。 TiKVクラスタがTiKVv4.0からアップグレードされ、アップグレード前に`readpool.storage`の`use-unified-pool`構成が`false`に設定されていた場合、すべての読み取り要求は、アップグレード後も異なるスレッドプールを使用し続けます。このシナリオでは、すべての読み取り要求でクエリに統合スレッドプールを使用するように、 `readpool.storage.use-unified-pool`の値を設定でき`true` 。

## TiKVスレッドプールのパフォーマンスチューニング {#performance-tuning-for-tikv-thread-pools}

-   gRPCスレッドプール。

    gRPCスレッドプールのデフォルトサイズ（ `server.grpc-concurrency`で構成）は`5`です。このスレッドプールにはコンピューティングのオーバーヘッドがほとんどなく、主にネットワークI / Oと逆シリアル化の要求を担当するため、通常、デフォルトの構成を調整する必要はありません。

    -   TiKVを使用してデプロイされたマシンのCPUコアの数が少ない（8以下）場合は、 `server.grpc-concurrency`構成項目を`2`に設定することを検討してください。
    -   TiKVでデプロイされたマシンの構成が非常に高い場合、TiKVは多数の読み取りおよび書き込み要求を実行し、GrafanaでスレッドCPUを監視する`gRPC poll CPU`の値が`server.grpc-concurrency`の80％を超える場合は、 `server.grpc-concurrency`の値を増やしてスレッドを維持することを検討してください。プールの使用率が80％未満（つまり、Grafanaのメトリックが`80% * server.grpc-concurrency`未満）。

-   スケジューラスレッドプール。

    TiKVがマシンのCPUコアの数が16以上であることを検出すると、スケジューラスレッドプールのデフォルトサイズ（ `storage.scheduler-worker-pool-size`で構成）は`8`になります。 TiKVがマシンのCPUコアの数が16未満であることを検出すると、デフォルトのサイズは`4`になります。

    このスレッドプールは主に、複雑なトランザクション要求を単純なKey-Value読み取りおよび書き込み要求に変換するために使用されます。ただし、**スケジューラスレッドプール自体は書き込み操作を実行しません**。

    -   トランザクションの競合が検出された場合、このスレッドプールは競合の結果を事前にクライアントに返します。
    -   競合が検出されない場合、このスレッドプールは、書き込み操作を実行するKey-ValueリクエストをRaftログにマージし、RaftログレプリケーションのためにRaftstoreスレッドに送信します。

    一般的に、過度のスレッドスイッチングを回避するには、スケジューラスレッドプールの使用率が50％から75％の間であることを確認するのが最善です。スレッドプールのサイズが`8`の場合、Grafanaで`TiKV-Details.Thread CPU.scheduler worker CPU`を400％から600％の間に保つことをお勧めします。

-   Raftstoreスレッドプール。

    Raftstoreスレッドプールは、TiKVで最も複雑なスレッドプールです。このスレッドプールのデフォルトサイズ（ `raftstore.store-pool-size`で構成）は`2`です。 StoreWriterスレッドプールの場合、デフォルトのサイズ（ `raftstore.store-io-pool-size`で構成）は`0`です。

    -   StoreWriterスレッドプールのサイズが0の場合、すべての書き込み要求はRaftstoreスレッドによって`fsync`の方法でRocksDBに書き込まれます。この場合、次のようにパフォーマンスを調整することをお勧めします。

        -   Raftstoreスレッドの全体的なCPU使用率を60％未満に保ちます。 Raftstoreスレッドの数が2の場合、 **TiKV-Details** 、 <strong>Thread CPU</strong> 、 <strong>Raft store CPU</strong>をGrafanaで120％未満に保ちます。 I / O要求により、理論上、RaftstoreスレッドのCPU使用率は常に100％未満です。
        -   慎重に検討せずに書き込みパフォーマンスを向上させるためにRaftstoreスレッドプールのサイズを大きくしないでください。ディスクの負荷が増加し、パフォーマンスが低下する可能性があります。

    -   StoreWriterスレッドプールのサイズが0でない場合、すべての書き込み要求は、StoreWriterスレッドによって`fsync`の方法でRocksDBに書き込まれます。この場合、次のようにパフォーマンスを調整することをお勧めします。

        -   全体的なCPUリソースが十分な場合にのみ、StoreWriterスレッドプールを有効にします。 StoreWriterスレッドプールが有効になっている場合は、StoreWriterスレッドとRaftstoreスレッドのCPU使用率を80％未満に保ちます。

        書き込み要求がRaftstoreスレッドによって処理される場合と比較して、理論的には、書き込み要求がStoreWriterスレッドによって処理される場合、書き込みレイテンシとデータ読み取りのテールレイテンシが大幅に短縮されます。ただし、書き込み速度が速くなると、それに応じてRaftログの数が増えます。これにより、Raftstoreスレッド、Applyスレッド、およびgRPCスレッドのCPUオーバーヘッドが増加する可能性があります。この場合、CPUリソースが不足するとチューニング効果が相殺され、書き込み速度が以前より遅くなる可能性があります。したがって、CPUリソースが十分でない場合は、StoreWriterスレッドを有効にすることはお勧めしません。 RaftstoreスレッドはほとんどのI/O要求をStoreWriterスレッドに送信するため、RaftstoreスレッドのCPU使用率を80％未満に保つ必要があります。

    -   ほとんどの場合、StoreWriterスレッドプールのサイズを1または2に設定します。これは、StoreWriterスレッドプールのサイズがRaftログの数に影響するため、スレッドプールサイズの値が大きすぎないようにする必要があるためです。 CPU使用率が80％を超える場合は、スレッドプールサイズを増やすことを検討してください。

    -   Raftログの増加が他のスレッドプールのCPUオーバーヘッドに与える影響に注意してください。必要に応じて、Raftstoreスレッド、Applyスレッド、およびgRPCスレッドの数を増やす必要があります。

-   UnifyReadPoolスレッドプール。

    UnifyReadPoolは、すべての読み取り要求を処理する責任があります。デフォルトのサイズ（ `readpool.unified.max-thread-count`で構成）は、マシンのCPUコアの数の80％です。たとえば、マシンのCPUに16コアがある場合、デフォルトのスレッドプールサイズは12です。アプリケーションのワークロードに応じてCPU使用率を調整し、スレッドプールサイズの60％から90％の間に保つことをお勧めします。

    Grafanaの`TiKV-Details.Thread CPU.Unified read pool CPU`のピーク値が800％を超えない場合は、 `readpool.unified.max-thread-count`から`10`に設定することをお勧めします。スレッドが多すぎると、スレッドの切り替えが頻繁になり、他のスレッドプールのリソースを消費する可能性があります。

-   RocksDBスレッドプール。

    RocksDBスレッドプールは、RocksDBがタスクを圧縮およびフラッシュするためのスレッドプールです。通常、設定する必要はありません。

    -   マシンのCPUコアの数が少ない場合は、 `rocksdb.max-background-jobs`と`raftdb.max-background-jobs`の両方を`4`に設定します。
    -   書き込みストールが発生した場合は、 **GrafanaのRocksDB-kvの**書き込みストール理由に移動し、 `0`以外のメトリックを確認してください。

        -   保留中の圧縮バイトに関連する理由が原因である場合は、 `rocksdb.max-sub-compactions`を`2`または`3`に設定します。この構成項目は、単一の圧縮ジョブで許可されるサブスレッドの数を示します。デフォルト値は、TiKV 4.0では`3` 、TiKV3.0では`1`です。
        -   理由がmemtablecountに関連している場合は、すべての列の`max-write-buffer-number`を増やすことをお勧めします（デフォルトでは`5` ）。
        -   理由がレベル0のファイル制限に関連している場合は、次のパラメーターの値を`64`以上に増やすことをお勧めします。

            ```
            rocksdb.defaultcf.level0-slowdown-writes-trigger
            rocksdb.writecf.level0-slowdown-writes-trigger
            rocksdb.lockcf.level0-slowdown-writes-trigger
            rocksdb.defaultcf.level0-stop-writes-trigger
            rocksdb.writecf.level0-stop-writes-trigger
            rocksdb.lockcf.level0-stop-writes-trigger
            ```
