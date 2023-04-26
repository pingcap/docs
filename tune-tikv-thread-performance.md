---
title: Tune TiKV Thread Pool Performance
summary: Learn how to tune TiKV thread pools for optimal performance.
---

# TiKV スレッド プールのパフォーマンスを調整する {#tune-tikv-thread-pool-performance}

このドキュメントでは、TiKV の内部スレッド プールとそのパフォーマンスを調整する方法を紹介します。

## スレッドプールの紹介 {#thread-pool-introduction}

TiKV スレッド プールは、主に gRPC、Scheduler、UnifyReadPool、 Raftstore、StoreWriter、Apply、RocksDB、および CPU をあまり消費しないいくつかのスケジュールされたタスクと検出コンポーネントで構成されています。このドキュメントでは、読み取りおよび書き込み要求のパフォーマンスに影響を与える、CPU を集中的に使用するいくつかのスレッド プールを主に紹介します。

-   gRPC スレッド プール: すべてのネットワーク リクエストを処理し、さまざまなタスク タイプのリクエストをさまざまなスレッド プールに転送します。

-   スケジューラ スレッド プール: 書き込みトランザクションの競合を検出し、2 フェーズ コミット、悲観的ロック、トランザクション ロールバックなどの要求をキーと値のペアの配列に変換し、 Raftログ レプリケーションのためにRaftstoreスレッドに送信します。

-   Raftstoreスレッド プール:

    -   すべてのRaftメッセージと提案を処理して、新しいログを追加します。
    -   Raftログをディスクに書き込みます。 [`store-io-pool-size`](/tikv-configuration-file.md#store-io-pool-size-new-in-v530)の値が`0`の場合、 Raftstoreスレッドはログをディスクに書き込みます。値が`0`でない場合、 Raftstoreスレッドはログを StoreWriter スレッドに送信します。
    -   大多数のレプリカのRaftログが一貫している場合、 Raftstoreスレッドはログを Apply スレッドに送信します。

-   StoreWriter スレッド プール: すべてのRaftログをディスクに書き込み、結果をRaftstoreスレッドに返します。

-   Apply スレッド プール: Raftstoreスレッド プールから送信された送信済みログを受け取り、それをキー値リクエストとして解析し、それを RocksDB に書き込み、コールバック関数を呼び出して書き込みリクエストが完了したことを gRPC スレッド プールに通知します。結果をクライアントに返します。

-   RocksDB スレッド プール: RocksDB がタスクを圧縮およびフラッシュするためのスレッド プールです。 RocksDB のアーキテクチャと`Compact`操作については、 [RocksDB: フラッシュおよび RAM ストレージ用の永続的な Key-Value ストア](https://github.com/facebook/rocksdb)を参照してください。

-   UnifyReadPool スレッド プール:コプロセッサースレッド プールとストレージ読み取りプールの組み合わせです。 kv get、kv batch get、raw kv get、コプロセッサーなどのすべての読み取り要求は、このスレッド プールで実行されます。

## TiKV 読み取り専用リクエスト {#tikv-read-only-requests}

TiKV の読み取りリクエストは、次のタイプに分類されます。

-   ストレージ読み取りプールで実行される、特定の行または複数の行を指定する単純なクエリ。
-   コプロセッサー読み取りプールで実行される複雑な集計計算および範囲照会。

TiKV v5.0 以降、すべての読み取りリクエストはデフォルトでクエリに統合スレッド プールを使用します。 TiKV クラスターが TiKV v4.0 からアップグレードされ、アップグレード前に`readpool.storage`の`use-unified-pool`構成が`false`に設定されていた場合、すべての読み取り要求は、アップグレード後も異なるスレッド プールを使用して続行されます。このシナリオでは、すべての読み取り要求がクエリに統合スレッド プールを使用するようにするには、値を`readpool.storage.use-unified-pool`から`true`に設定します。

## TiKV スレッド プールのパフォーマンス チューニング {#performance-tuning-for-tikv-thread-pools}

-   gRPC スレッド プール。

    gRPC スレッド プールのデフォルト サイズ ( `server.grpc-concurrency`で構成) は`5`です。このスレッド プールにはコンピューティング オーバーヘッドがほとんどなく、主にネットワーク I/O と逆シリアル化の要求を担当するため、通常、デフォルトの構成を調整する必要はありません。

    -   TiKV でデプロイされたマシンの CPU コア数が少ない (8 以下) 場合は、 `server.grpc-concurrency`構成項目を`2`に設定することを検討してください。
    -   TiKV でデプロイされたマシンの構成が非常に高く、TiKV が多数の読み取りおよび書き込み要求を処理し、Grafana でスレッド CPU を監視する`gRPC poll CPU`の値が`server.grpc-concurrency`の 80% を超える場合は、値`server.grpc-concurrency`を増やしてスレッドを維持することを検討してください。プールの使用率が 80% 未満 (つまり、Grafana のメトリックが`80% * server.grpc-concurrency`未満)。

-   スケジューラのスレッド プール。

    マシンの CPU コア数が 16 以上であることを TiKV が検出すると、スケジューラ スレッド プールのデフォルト サイズ ( `storage.scheduler-worker-pool-size`で設定) は`8`です。マシンの CPU コアの数が 16 より小さいことを TiKV が検出した場合、デフォルトのサイズは`4`です。

    このスレッド プールは主に、複雑なトランザクション リクエストを単純なキー値の読み取りおよび書き込みリクエストに変換するために使用されます。ただし、 **Scheduler スレッド プール自体は書き込み操作を実行しません**。

    -   トランザクションの競合が検出された場合、このスレッド プールは事前に競合の結果をクライアントに返します。
    -   競合が検出されない場合、このスレッド プールは、書き込み操作を実行するキー値リクエストをRaftログにマージし、それをRaftログ レプリケーションのためにRaftstoreスレッドに送信します。

    一般的に言えば、過剰なスレッドの切り替えを避けるために、スケジューラ スレッド プールの使用率を 50% から 75% の間に確保することをお勧めします。スレッド プール サイズが`8`の場合、Grafana では`TiKV-Details.Thread CPU.scheduler worker CPU` 400% から 600% の間で維持することをお勧めします。

-   Raftstoreスレッド プール。

    Raftstoreスレッド プールは、TiKV で最も複雑なスレッド プールです。このスレッド プールのデフォルト サイズ ( `raftstore.store-pool-size`で構成) は`2`です。 StoreWriter スレッド プールの場合、既定のサイズ ( `raftstore.store-io-pool-size`で構成) は`0`です。

    -   StoreWriter スレッド プールのサイズが 0 の場合、すべての書き込み要求はRaftstoreスレッドによって`fsync`の方法で RocksDB に書き込まれます。この場合、次のようにパフォーマンスを調整することをお勧めします。

        -   Raftstoreスレッドの全体的な CPU 使用率を 60% 未満に保ちます。 Raftstoreスレッドの数が 2 の場合、 **TiKV-Details** 、 <strong>Thread CPU</strong> 、Grafana の<strong>Raft store CPU を</strong>120% 未満に保ちます。 I/O リクエストにより、理論上のRaftstoreスレッドの CPU 使用率は常に 100% より低くなります。
        -   ディスクの負荷が増大し、パフォーマンスが低下する可能性があるため、書き込みパフォーマンスを改善するためにRaftstoreスレッド プールのサイズを大きくしないでください。

    -   StoreWriter スレッド プールのサイズが 0 でない場合、すべての書き込み要求は、StoreWriter スレッドによって`fsync`の方法で RocksDB に書き込まれます。この場合、次のようにパフォーマンスを調整することをお勧めします。

        -   全体的な CPU リソースが十分な場合にのみ、StoreWriter スレッド プールを有効にします。 StoreWriter スレッド プールが有効になっている場合は、StoreWriter スレッドとRaftstoreスレッドの CPU 使用率を 80% 未満に保ちます。

        書き込み要求がRaftstoreスレッドによって処理される場合と比較して、書き込み要求が StoreWriter スレッドによって処理される場合、理論的には、書き込みレイテンシーとデータ読み取りの末尾レイテンシーが大幅に削減されます。ただし、書き込み速度が速くなるにつれて、それに応じてRaftログの数が増加します。これにより、 Raftstoreスレッド、Apply スレッド、および gRPC スレッドの CPU オーバーヘッドが増加する可能性があります。この場合、CPUリソースが不足するとチューニングの効果が相殺され、その結果、書き込み速度が以前より遅くなる可能性があります。したがって、CPU リソースが十分でない場合は、StoreWriter スレッドを有効にすることはお勧めしません。 Raftstoreスレッドはほとんどの I/O 要求を StoreWriter スレッドに送信するため、 Raftstoreスレッドの CPU 使用率を 80% 未満に保つ必要があります。

    -   ほとんどの場合、StoreWriter スレッド プールのサイズを 1 または 2 に設定します。これは、StoreWriter スレッド プールのサイズがRaftログの数に影響するため、スレッド プール サイズの値が大きすぎてはならないためです。 CPU 使用率が 80% を超える場合は、スレッド プール サイズを増やすことを検討してください。

    -   他のスレッド プールの CPU オーバーヘッドに対するRaftログの増加の影響に注意してください。必要に応じて、それに応じてRaftstoreスレッド、Apply スレッド、および gRPC スレッドの数を増やす必要があります。

-   UnifyReadPool スレッド プール。

    UnifyReadPool は、すべての読み取り要求の処理を担当します。デフォルトのサイズ ( `readpool.unified.max-thread-count`で構成) は、マシンの CPU コア数の 80% です。たとえば、マシンの CPU に 16 コアがある場合、デフォルトのスレッド プール サイズは 12 です。アプリケーションのワークロードに応じて CPU 使用率を調整し、スレッド プール サイズの 60% から 90% の間に維持することをお勧めします。

    Grafana の`TiKV-Details.Thread CPU.Unified read pool CPU`のピーク値が 800% を超えない場合は、 `readpool.unified.max-thread-count`から`10`に設定することをお勧めします。スレッドが多すぎると、スレッドの切り替えが頻繁になり、他のスレッド プールのリソースを占有する可能性があります。

    v6.3.0 以降、TiKV は現在の CPU 使用率に基づいた UnifyReadPool スレッド プール サイズの自動調整をサポートしています。この機能を有効にするには、 [`readpool.unified.auto-adjust-pool-size = true`](/tikv-configuration-file.md#auto-adjust-pool-size-new-in-v630)を設定します。再読み込みされ、最大 CPU 使用率が 80% を超えるクラスターのスレッド プール サイズを自動的に調整することをお勧めします。

-   RocksDB スレッド プール。

    RocksDB スレッド プールは、RocksDB がタスクを圧縮およびフラッシュするためのスレッド プールです。通常、設定する必要はありません。

    -   マシンの CPU コア数が少ない場合は、 `rocksdb.max-background-jobs`と`raftdb.max-background-jobs`の両方を`4`に設定します。
    -   書き込みストールが発生した場合は、Grafana の**RocksDB-kv**の Write Stall Reason に移動し、 `0`以外のメトリックを確認します。

        -   保留中の圧縮バイトに関連する理由が原因である場合は、 `rocksdb.max-sub-compactions`を`2`または`3`に設定します。この構成項目は、1 つの圧縮ジョブで許可されるサブスレッドの数を示します。デフォルト値は、TiKV 4.0 では`3` 、TiKV 3.0 では`1`です。
        -   理由が memtable 数に関連している場合は、すべての列の`max-write-buffer-number`を増やすことをお勧めします (デフォルトでは`5` )。
        -   理由が level0 ファイル制限に関連している場合は、次のパラメーターの値を`64`以上に増やすことをお勧めします。

            ```
            rocksdb.defaultcf.level0-slowdown-writes-trigger
            rocksdb.writecf.level0-slowdown-writes-trigger
            rocksdb.lockcf.level0-slowdown-writes-trigger
            rocksdb.defaultcf.level0-stop-writes-trigger
            rocksdb.writecf.level0-stop-writes-trigger
            rocksdb.lockcf.level0-stop-writes-trigger
            ```
