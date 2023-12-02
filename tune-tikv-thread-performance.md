---
title: Tune TiKV Thread Pool Performance
summary: Learn how to tune TiKV thread pools for optimal performance.
---

# TiKV スレッド プールのパフォーマンスを調整する {#tune-tikv-thread-pool-performance}

このドキュメントでは、TiKV 内部スレッド プールとそのパフォーマンスを調整する方法を紹介します。

## スレッドプールの紹介 {#thread-pool-introduction}

TiKV スレッド プールは主に、gRPC、Scheduler、UnifyReadPool、 Raftstore、StoreWriter、Apply、RocksDB、および CPU をあまり消費しないいくつかのスケジュールされたタスクと検出コンポーネントで構成されます。このドキュメントでは主に、読み取りおよび書き込みリクエストのパフォーマンスに影響を与える、CPU 集中型のスレッド プールをいくつか紹介します。

-   gRPC スレッド プール: すべてのネットワーク リクエストを処理し、さまざまなタスク タイプのリクエストをさまざまなスレッド プールに転送します。

-   スケジューラ スレッド プール: 書き込みトランザクションの競合を検出し、2 フェーズ コミット、悲観的ロック、トランザクション ロールバックなどのリクエストをキーと値のペアの配列に変換し、 Raftログ レプリケーションのためにRaftstoreスレッドに送信します。

-   Raftstoreスレッド プール:

    -   すべてのRaftメッセージと新しいログを追加する提案を処理します。
    -   Raftログをディスクに書き込みます。 [`store-io-pool-size`](/tikv-configuration-file.md#store-io-pool-size-new-in-v530)の値が`0`の場合、 Raftstoreスレッドはログをディスクに書き込みます。値が`0`でない場合、 Raftstoreスレッドはログを StoreWriter スレッドに送信します。
    -   大部分のレプリカのRaftログに一貫性がある場合、 Raftstoreスレッドはログを適用スレッドに送信します。

-   StoreWriter スレッド プール: すべてのRaftログをディスクに書き込み、結果をRaftstoreスレッドに返します。

-   アプライ スレッド プール: Raftstoreスレッド プールから送信された送信済みログを受信し、それをキーと値のリクエストとして解析して RocksDB に書き込み、コールバック関数を呼び出して gRPC スレッド プールに書き込みリクエストが完了したことを通知します。結果をクライアントに返します。

-   RocksDB スレッド プール: タスクを圧縮してフラッシュするための RocksDB のスレッド プールです。 RocksDB のアーキテクチャと`Compact`操作については、 [RocksDB: フラッシュおよび RAM ストレージ用の永続的なキーと値のストア](https://github.com/facebook/rocksdb)を参照してください。

-   UnifyReadPool スレッド プール:コプロセッサースレッド プールとストレージ読み取りプールを組み合わせたものです。 kv get、kvバッチget、raw kv get、コプロセッサなどのすべての読み取りリクエストは、このスレッドプールで実行されます。

## TiKV 読み取り専用リクエスト {#tikv-read-only-requests}

TiKV の読み取りリクエストは次のタイプに分類されます。

-   ストレージ読み取りプールで実行される、特定の行または複数の行を指定する単純なクエリ。
-   複雑な集計計算と範囲クエリは、コプロセッサー読み取りプールで実行されます。

TiKV v5.0 以降、すべての読み取りリクエストはデフォルトでクエリに統合スレッド プールを使用します。 TiKV クラスターが TiKV v4.0 からアップグレードされ、アップグレード前に`readpool.storage`の`use-unified-pool`構成が`false`に設定されていた場合、すべての読み取りリクエストはアップグレード後も引き続き異なるスレッド プールを使用します。このシナリオでは、すべての読み取りリクエストがクエリに統合スレッド プールを使用するようにするには、値`readpool.storage.use-unified-pool`から`true`を設定します。

## TiKV スレッド プールのパフォーマンス チューニング {#performance-tuning-for-tikv-thread-pools}

-   gRPC スレッド プール。

    gRPC スレッド プールのデフォルトのサイズ ( `server.grpc-concurrency`で構成) は`5`です。このスレッド プールにはコンピューティング オーバーヘッドがほとんどなく、主にネットワーク I/O と逆シリアル化リクエストを担当するため、通常はデフォルト構成を調整する必要はありません。

    -   TiKV を使用してデプロイされたマシンの CPU コア数が少ない (8 以下) 場合は、 `server.grpc-concurrency`構成項目を`2`に設定することを検討してください。
    -   TiKV でデプロイされたマシンの構成が非常に高く、TiKV が大量の読み取りおよび書き込みリクエストを処理し、Grafana のスレッド CPU を監視する`gRPC poll CPU`の値が`server.grpc-concurrency`の 80% を超えている場合は、スレッドを維持するために`server.grpc-concurrency`の値を増やすことを検討してください。プール使用率が 80% 未満 (つまり、Grafana のメトリクスが`80% * server.grpc-concurrency`未満)。

-   スケジューラのスレッド プール。

    TiKV がマシンの CPU コアの数が 16 以上であることを検出した場合、スケジューラ スレッド プールのデフォルト サイズ ( `storage.scheduler-worker-pool-size`で構成) は`8`です。 TiKV がマシンの CPU コアの数が 16 未満であることを検出した場合、デフォルトのサイズは`4`です。

    このスレッド プールは主に、複雑なトランザクション リクエストを単純なキーと値の読み取りおよび書き込みリクエストに変換するために使用されます。ただし、**スケジューラ スレッド プール自体は書き込み操作を実行しません**。

    -   トランザクションの競合を検出した場合、このスレッド プールは競合の結果をクライアントに事前に返します。
    -   競合が検出されない場合、このスレッド プールは、書き込み操作を実行するキーと値のリクエストをRaftログにマージし、それをRaftログ レプリケーションのためにRaftstoreスレッドに送信します。

    一般に、過度のスレッド切り替えを回避するには、スケジューラ スレッド プールの使用率を 50% ～ 75% にするのが最善です。スレッド プール サイズが`8`の場合、Grafana では`TiKV-Details.Thread CPU.scheduler worker CPU` 400% から 600% の間で維持することをお勧めします。

-   Raftstoreスレッド プール。

    Raftstoreスレッド プールは、TiKV で最も複雑なスレッド プールです。このスレッド プールのデフォルト サイズ ( `raftstore.store-pool-size`で構成) は`2`です。 StoreWriter スレッド プールの場合、デフォルトのサイズ ( `raftstore.store-io-pool-size`で構成) は`0`です。

    -   StoreWriter スレッド プールのサイズが 0 の場合、すべての書き込みリクエストはRaftstoreスレッドによって`fsync`の方法で RocksDB に書き込まれます。この場合、次のようにパフォーマンスを調整することをお勧めします。

        -   Raftstoreスレッドの全体的な CPU 使用率を 60% 未満に保ちます。 Raftstoreスレッドの数が 2 の場合、Grafana 上の**TiKV-Details** 、 **Thread CPU** 、 **Raftストア CPU を**120% 未満に保ちます。 I/O リクエストにより、理論上、 Raftstoreスレッドの CPU 使用率は常に 100% 未満になります。
        -   書き込みパフォーマンスを向上させるために、慎重に考慮せずにRaftstoreスレッド プールのサイズを大きくしないでください。ディスクの負担が増大し、パフォーマンスが低下する可能性があります。

    -   StoreWriter スレッド プールのサイズが 0 ではない場合、すべての書き込みリクエストは StoreWriter スレッドによって`fsync`の方法で RocksDB に書き込まれます。この場合、次のようにパフォーマンスを調整することをお勧めします。

        -   全体的な CPU リソースが十分である場合にのみ、StoreWriter スレッド プールを有効にします。 StoreWriter スレッド プールが有効になっている場合は、StoreWriter スレッドとRaftstoreスレッドの CPU 使用率を 80% 未満に維持してください。

        書き込みリクエストがRaftstoreスレッドによって処理される場合と比較して、書き込みリクエストが StoreWriter スレッドによって処理される場合、理論上、書き込みレイテンシーとデータ読み取りのテールレイテンシーが大幅に短縮されます。ただし、書き込み速度が速くなると、それに応じてRaftログの数も増加します。これにより、 Raftstoreスレッド、Apply スレッド、および gRPC スレッドの CPU オーバーヘッドが増加する可能性があります。この場合、CPU リソースが不足するとチューニング効果が相殺され、その結果、書き込み速度が以前より遅くなる可能性があります。したがって、CPU リソースが十分でない場合は、StoreWriter スレッドを有効にすることはお勧めできません。 Raftstoreスレッドはほとんどの I/O リクエストを StoreWriter スレッドに送信するため、 Raftstoreスレッドの CPU 使用率を 80% 未満に保つ必要があります。

    -   ほとんどの場合、StoreWriter スレッド プールのサイズは 1 または 2 に設定します。これは、StoreWriter スレッド プールのサイズがRaftログの数に影響するため、スレッド プール サイズの値が大きすぎないようにする必要があります。 CPU 使用率が 80% を超えている場合は、スレッド プール サイズを増やすことを検討してください。

    -   Raftログの増加が他のスレッド プールの CPU オーバーヘッドに及ぼす影響に注意してください。必要に応じて、 Raftstoreスレッド、Apply スレッド、および gRPC スレッドの数をそれに応じて増やす必要があります。

-   UnifyReadPool スレッド プール。

    UnifyReadPool は、すべての読み取りリクエストの処理を担当します。デフォルトのサイズ ( `readpool.unified.max-thread-count`で構成) は、マシンの CPU コア数の 80% です。たとえば、マシンの CPU に 16 コアがある場合、デフォルトのスレッド プール サイズは 12 です。アプリケーションのワークロードに応じて CPU 使用率を調整し、スレッド プール サイズの 60% ～ 90% の間に維持することをお勧めします。

    Grafana の`TiKV-Details.Thread CPU.Unified read pool CPU`のピーク値が 800% を超えない場合は、 `readpool.unified.max-thread-count` ～ `10`に設定することをお勧めします。スレッドが多すぎると、スレッドの切り替えが頻繁に発生し、他のスレッド プールのリソースが占有される可能性があります。

    v6.3.0 以降、TiKV は、現在の CPU 使用率に基づいて UnifyReadPool スレッド プール サイズの自動調整をサポートします。この機能を有効にするには、 [`readpool.unified.auto-adjust-pool-size = true`](/tikv-configuration-file.md#auto-adjust-pool-size-new-in-v630)を設定します。再読み取りされ、最大 CPU 使用率が 80% を超えるクラスターのスレッド プール サイズを自動的に調整することをお勧めします。

-   RocksDB スレッド プール。

    RocksDB スレッド プールは、タスクを圧縮してフラッシュするための RocksDB のスレッド プールです。通常、設定する必要はありません。

    -   マシンの CPU コアの数が少ない場合は、 `rocksdb.max-background-jobs`と`raftdb.max-background-jobs`の両方を`4`に設定します。
    -   書き込みストールが発生した場合は、Grafana 上の**RocksDB-kv**の「書き込みストールの理由」に移動し、 `0`はないメトリクスを確認してください。

        -   保留中の圧縮バイトに関連した理由が原因である場合は、 `rocksdb.max-sub-compactions`を`2`または`3`に設定します。この構成項目は、単一の圧縮ジョブに許可されるサブスレッドの数を示します。デフォルト値は、TiKV 4.0 では`3` 、TiKV 3.0 では`1`です。
        -   理由が memtable 数に関連している場合は、すべての列の`max-write-buffer-number`を増やすことをお勧めします (デフォルトでは`5` )。
        -   理由がレベル 0 ファイル制限に関連している場合は、次のパラメータの値を`64`以上に増やすことをお勧めします。

                rocksdb.defaultcf.level0-slowdown-writes-trigger
                rocksdb.writecf.level0-slowdown-writes-trigger
                rocksdb.lockcf.level0-slowdown-writes-trigger
                rocksdb.defaultcf.level0-stop-writes-trigger
                rocksdb.writecf.level0-stop-writes-trigger
                rocksdb.lockcf.level0-stop-writes-trigger
