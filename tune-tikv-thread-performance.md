---
title: Tune TiKV Thread Pool Performance
summary: 最適なパフォーマンスを得るために TiKV スレッド プールを調整する方法を学習します。
---

# TiKV スレッド プールのパフォーマンスを調整する {#tune-tikv-thread-pool-performance}

このドキュメントでは、TiKV 内部スレッド プールとそのパフォーマンスを調整する方法について説明します。

## スレッドプールの紹介 {#thread-pool-introduction}

TiKV スレッド プールは、主に gRPC、Scheduler、UnifyReadPool、 Raftstore、StoreWriter、Apply、RocksDB、および CPU をあまり消費しないいくつかのスケジュールされたタスクと検出コンポーネントで構成されています。このドキュメントでは、主に読み取りおよび書き込み要求のパフォーマンスに影響を与える CPU を集中的に使用するスレッド プールをいくつか紹介します。

-   gRPC スレッド プール: すべてのネットワーク リクエストを処理し、さまざまなタスク タイプのリクエストをさまざまなスレッド プールに転送します。

-   スケジューラ スレッド プール: 書き込みトランザクションの競合を検出し、2 フェーズ コミット、悲観的ロック、トランザクション ロールバックなどの要求をキーと値のペアの配列に変換し、 RaftログのレプリケーションのためにRaftstoreスレッドに送信します。

-   Raftstoreスレッド プール:

    -   すべてのRaftメッセージと新しいログを追加する提案を処理します。
    -   Raftログをディスクに書き込みます。 [`store-io-pool-size`](/tikv-configuration-file.md#store-io-pool-size-new-in-v530)の値が`0`の場合、 Raftstoreスレッドはログをディスクに書き込みます。値が`0`でない場合、 Raftstoreスレッドはログを StoreWriter スレッドに送信します。
    -   大多数のレプリカのRaftログが整合している場合、 Raftstoreスレッドはログを適用スレッドに送信します。

-   StoreWriter スレッド プール: すべてのRaftログをディスクに書き込み、結果をRaftstoreスレッドに返します。

-   Apply スレッド プール: Raftstoreスレッド プールから送信された送信ログを受信し、それをキー値要求として解析し、RocksDB に書き込み、コールバック関数を呼び出して書き込み要求が完了したことを gRPC スレッド プールに通知し、結果をクライアントに返します。

-   RocksDB スレッド プール: RocksDB がタスクを圧縮およびフラッシュするためのスレッド プールです。RocksDB のアーキテクチャと`Compact`操作については、 [RocksDB: フラッシュおよび RAM ストレージ用の永続的なキー値ストア](https://github.com/facebook/rocksdb)を参照してください。

-   UnifyReadPool スレッド プール:コプロセッサースレッド プールとストレージ読み取りプールの組み合わせです。kv get、kv batch get、raw kv get、コプロセッサなどのすべての読み取り要求は、このスレッド プールで実行されます。

## TiKV 読み取り専用リクエスト {#tikv-read-only-requests}

TiKV の読み取り要求は次のタイプに分類されます。

-   ストレージ読み取りプールで実行される、特定の行または複数の行を指定する単純なクエリ。
-   コプロセッサー読み取りプールで実行される複雑な集計計算と範囲クエリ。

TiKV v5.0 以降では、すべての読み取り要求はデフォルトでクエリに統合スレッド プールを使用します。TiKV クラスターが TiKV v4.0 からアップグレードされ、アップグレード前に`use-unified-pool`構成の`readpool.storage`が`false`に設定されていた場合、すべての読み取り要求はアップグレード後も引き続き異なるスレッド プールを使用します。このシナリオでは、すべての読み取り要求がクエリに統合スレッド プールを使用するようにするには、 `readpool.storage.use-unified-pool`の値を`true`に設定できます。

## TiKV スレッド プールのパフォーマンス チューニング {#performance-tuning-for-tikv-thread-pools}

-   gRPC スレッド プール。

    gRPC スレッド プールのデフォルト サイズ ( `server.grpc-concurrency`に設定) は`5`です。このスレッド プールにはコンピューティング オーバーヘッドがほとんどなく、主にネットワーク I/O とデシリアライゼーション要求を担当するため、通常はデフォルト構成を調整する必要はありません。

    -   TiKV を使用してデプロイされたマシンの CPU コア数が少ない (8 個以下) 場合は、 `server.grpc-concurrency`構成項目を`2`に設定することを検討してください。
    -   TiKV がデプロイされたマシンの構成が非常に高く、TiKV が大量の読み取りおよび書き込み要求を実行し、Grafana でスレッド CPU を監視する値`gRPC poll CPU`が`server.grpc-concurrency`の 80% を超える場合は、スレッド プールの使用率を 80% 未満 (つまり、Grafana のメトリックが`80% * server.grpc-concurrency`未満) に保つために`server.grpc-concurrency`の値を増やすことを検討してください。

-   スケジューラ スレッド プール。

    TiKV がマシンの CPU コアの数が 16 以上であることを検出すると、スケジューラ スレッド プールのデフォルト サイズ ( `storage.scheduler-worker-pool-size`に設定) は`8`なります。TiKV がマシンの CPU コアの数が 16 未満であることを検出すると、デフォルト サイズは`4`なります。

    このスレッド プールは主に、複雑なトランザクション要求を単純なキー値の読み取りおよび書き込み要求に変換するために使用されます。ただし、**スケジューラ スレッド プール自体は書き込み操作を実行しません**。

    -   トランザクションの競合が検出されると、このスレッド プールは競合の結果を事前にクライアントに返します。
    -   競合が検出されない場合、このスレッド プールは書き込み操作を実行するキー値要求をRaftログにマージし、 RaftログのレプリケーションのためにRaftstoreスレッドに送信します。

    一般的に、過度のスレッド切り替えを回避するには、スケジューラ スレッド プールの使用率が 50% から 75% の間になるようにするのが最適です。スレッド プールのサイズが`8`の場合、Grafana では`TiKV-Details.Thread CPU.scheduler worker CPU` 400% から 600% の間に保つことをお勧めします。

-   Raftstoreスレッド プール。

    Raftstoreスレッド プールは、TiKV で最も複雑なスレッド プールです。このスレッド プールのデフォルト サイズ ( `raftstore.store-pool-size`で構成) は`2`です。StoreWriter スレッド プールの場合、デフォルト サイズ ( `raftstore.store-io-pool-size`で構成) は`1`です。

    -   StoreWriter スレッド プールのサイズが 0 の場合、すべての書き込み要求はRaftstoreスレッドによって`fsync`として RocksDB に書き込まれます。この場合、次のようにパフォーマンスをチューニングすることをお勧めします。

        -   Raftstoreスレッドの全体的な CPU 使用率を 60% 未満に保ちます。Raftstore スレッドの数が 2 の場合、Grafana 上の**TiKV-Details** 、 **Thread CPU** 、 **Raft store CPU を**120% 未満に保ちます。I / O 要求により、理論上はRaftstoreスレッドの CPU 使用率は常に 100% 未満になります。
        -   書き込みパフォーマンスを向上させるために、 Raftstoreスレッド プールのサイズを慎重に検討せずに増やさないでください。ディスクの負荷が増加し、パフォーマンスが低下する可能性があります。

    -   StoreWriter スレッド プールのサイズが 0 でない場合、すべての書き込み要求は StoreWriter スレッドによって`fsync`として RocksDB に書き込まれます。この場合、次のようにパフォーマンスをチューニングすることをお勧めします。

        -   全体的な CPU リソースが十分な場合にのみ、StoreWriter スレッド プールを有効にしてください。StoreWriter スレッド プールを有効にすると、StoreWriter スレッドとRaftstoreスレッドの CPU 使用率が 80% 未満に保たれます。

        書き込み要求がRaftstoreスレッドで処理される場合と比較すると、理論上は、書き込み要求が StoreWriter スレッドで処理される場合、書き込みレイテンシーとデータ読み取りのテールレイテンシーが大幅に短縮されます。ただし、書き込み速度が速くなると、それに応じてRaftログの数が増えます。これにより、 Raftstoreスレッド、Apply スレッド、gRPC スレッドの CPU オーバーヘッドが増加する可能性があります。この場合、CPU リソースが不足するとチューニング効果が相殺され、結果として書き込み速度が以前よりも遅くなる可能性があります。したがって、CPU リソースが十分でない場合は、StoreWriter スレッドを有効にすることは推奨されません。Raftstore スレッドはほとんどの I/O 要求を StoreWriter スレッドに送信するため、 Raftstoreスレッドの CPU 使用率を 80% 未満に抑える必要があります。

    -   ほとんどの場合、StoreWriter スレッド プールのサイズは 1 または 2 に設定します。これは、StoreWriter スレッド プールのサイズがRaftログの数に影響するため、スレッド プール サイズの値が大きすぎないようにするためです。CPU 使用率が 80% を超える場合は、スレッド プール サイズを増やすことを検討してください。

    -   Raftログの増加が他のスレッド プールの CPU オーバーヘッドに与える影響に注意してください。必要に応じて、 Raftstoreスレッド、Apply スレッド、gRPC スレッドの数を増やす必要があります。

-   UnifyReadPool スレッド プール。

    UnifyReadPool は、すべての読み取り要求の処理を担当します。デフォルトのサイズ ( `readpool.unified.max-thread-count`に設定) は、マシンの CPU コア数の 80% です。たとえば、マシンの CPU に 16 個のコアがある場合、デフォルトのスレッド プール サイズは 12 です。アプリケーションのワークロードに応じて CPU 使用率を調整し、スレッド プール サイズの 60% ～ 90% に保つことをお勧めします。

    Grafana の`TiKV-Details.Thread CPU.Unified read pool CPU`のピーク値が 800% を超えない場合は、 `readpool.unified.max-thread-count` 〜 `10`に設定することをお勧めします。スレッドが多すぎると、スレッドの切り替えが頻繁に発生し、他のスレッド プールのリソースが消費される可能性があります。

    v6.3.0 以降、TiKV は現在の CPU 使用率に基づいて UnifyReadPool スレッド プール サイズを自動的に調整することをサポートしています。この機能を有効にするには、 [`readpool.unified.auto-adjust-pool-size = true`](/tikv-configuration-file.md#auto-adjust-pool-size-new-in-v630)を設定します。再読み取りされ、最大 CPU 使用率が 80% を超えるクラスターのスレッド プール サイズを自動的に調整することをお勧めします。

-   RocksDB スレッド プール。

    RocksDB スレッド プールは、RocksDB がタスクを圧縮およびフラッシュするためのスレッド プールです。通常は、これを構成する必要はありません。

    -   マシンの CPU コア数が少ない場合は、 `rocksdb.max-background-jobs`と`raftdb.max-background-jobs`両方を`4`に設定します。
    -   書き込みストールが発生した場合は、Grafana の**RocksDB-kv**の Write Stall Reason に移動し、 `0`以外のメトリックを確認します。

        -   保留中の圧縮バイトに関連する理由によって発生した場合は、 `rocksdb.max-sub-compactions` ～ `2`または`3`設定します。この構成項目は、単一の圧縮ジョブに許可されるサブスレッドの数を示します。デフォルト値は、TiKV 4.0 では`3` 、TiKV 3.0 では`1`です。
        -   理由が memtable の数に関連している場合は、すべての列の`max-write-buffer-number` (デフォルトでは`5` ) を増やすことをお勧めします。
        -   理由がレベル 0 のファイル制限に関連している場合は、次のパラメータの値を`64`以上に増やすことをお勧めします。

                rocksdb.defaultcf.level0-slowdown-writes-trigger
                rocksdb.writecf.level0-slowdown-writes-trigger
                rocksdb.lockcf.level0-slowdown-writes-trigger
                rocksdb.defaultcf.level0-stop-writes-trigger
                rocksdb.writecf.level0-stop-writes-trigger
                rocksdb.lockcf.level0-stop-writes-trigger
