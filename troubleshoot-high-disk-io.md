---
title: Troubleshoot High Disk I/O Usage in TiDB
summary: Learn how to locate and address the issue of high TiDB storage I/O usage.
---

# TiDB でのディスク I/O 使用率の高さのトラブルシューティング {#troubleshoot-high-disk-i-o-usage-in-tidb}

このドキュメントでは、TiDB でのディスク I/O 使用率の高さの問題を特定して対処する方法を紹介します。

## 現在の I/O メトリクスを確認する {#check-the-current-i-o-metrics}

CPU ボトルネックとトランザクションの競合によって引き起こされるボトルネックのトラブルシューティングを行った後に TiDB の応答が遅くなった場合は、現在のシステム ボトルネックを特定するために I/O メトリックを確認する必要があります。

### モニターから I/O の問題を特定する {#locate-i-o-issues-from-monitor}

I/O の問題を見つける最も簡単な方法は、 TiUPによってデフォルトでデプロイされる Grafana ダッシュボードなどのモニターから全体的な I/O ステータスを表示することです。 I/O に関連するダッシュボード パネルには、**概要**、 **Node_exporter** 、および**Disk-Performance**が含まれます。

#### 最初のタイプの監視パネル {#the-first-type-of-monitoring-panels}

**[概要]** &gt; **[システム情報]** &gt; **[IO 使用率]**で、クラスター内の各マシンの I/O ステータスを確認できます。このメトリックは、Linux `iostat`モニターの`util`に似ています。パーセンテージが高いほど、ディスク I/O 使用率が高くなります。

-   モニター内に I/O 使用率の高いマシンが 1 台だけある場合は、現在、このマシンに読み取りおよび書き込みのホットスポットが存在する可能性があります。
-   モニター内のほとんどのマシンの I/O 使用率が高い場合、クラスターの I/O 負荷は高くなります。

上記の最初の状況 (I/O 使用率が高いマシンが 1 台のみ) の場合は、**ディスク パフォーマンス ダッシュボード**から I/O メトリクス ( `Disk Latency`や`Disk Load`など) をさらに観察して、異常が存在するかどうかを判断できます。必要に応じて、fio ツールを使用してディスクをチェックします。

#### 2 番目のタイプの監視パネル {#the-second-type-of-monitoring-panels}

TiDB クラスターの主なstorageコンポーネントは TiKV です。 1 つの TiKV インスタンスには 2 つの RocksDB インスタンスが含まれています。1 つはRaftログの保存用であり、 `data/raft`にあり、もう 1 つは実際のデータの保存用で、 `data/db`にあります。

**[TiKV-Details]** &gt; **[Raft IO]**で、これら 2 つのインスタンスのディスク書き込みに関連するメトリクスを確認できます。

-   `Append log duration` : このメトリクスは、 Raftログを保存する RockDB への書き込みの応答時間を示します。 `.99`応答時間は 50 ミリ秒以内である必要があります。
-   `Apply log duration` : このメトリクスは、実際のデータを保存する RockDB への書き込みの応答時間を示します。 `.99`応答は 100 ミリ秒以内である必要があります。

これら 2 つのメトリクスには、書き込みホットスポットの表示に役立つ**..サーバーごとの**監視パネルもあります。

#### 3番目のタイプの監視パネル {#the-third-type-of-monitoring-panels}

**[TiKV-Details]** &gt; **[Storage]**には、storageに関連するモニタリング メトリックがあります。

-   `Storage command total` : 受信した異なるコマンドの数を示します。
-   `Storage async write duration` : Raft I/O に関連する可能性がある`disk sync duration`などのモニタリング メトリクスが含まれます。異常が発生した場合は、ログを確認して関連コンポーネントの動作状況を確認してください。

#### その他のパネル {#other-panels}

さらに、他のパネル メトリクスは、ボトルネックが I/O であるかどうかを判断するのに役立つ場合があり、いくつかのパラメータの設定を試みることができます。 TiKV gRPC 継続時間の prewrite/commit/raw-put (生のキーと値のクラスターのみ) をチェックすることで、ボトルネックが実際に TiKV 書き込みの遅さであることを判断できます。 TiKV 書き込みが遅い一般的な状況は次のとおりです。

-   `append log`は遅いです。 TiKV Grafana の`Raft I/O`および`append log duration`メトリックは比較的高く、これは多くの場合、ディスク書き込みが遅いことが原因です。 **RocksDB-raft**の`WAL Sync Duration max`の値を確認して、 `append log`が遅い原因を特定できます。それ以外の場合は、バグを報告する必要がある場合があります。

-   `raftstore`スレッドはビジー状態です。 TiKV Grafana では、 `Raft Propose` / `propose wait duration`は`append log duration`よりも大幅に高くなります。トラブルシューティングのために次の点を確認してください。

    -   `[raftstore]`のうち`store-pool-size`の値が小さすぎるかどうか。この値は`[1,5]`から大きすぎない範囲に設定することをお勧めします。
    -   マシンのCPUリソースが不足していないか。

-   `append log`は遅いです。 TiKV Grafana の`Raft I/O`および`append log duration`メトリクスは比較的高く、通常は比較的高い`Raft Propose` / `apply wait duration`とともに発生する可能性があります。考えられる原因は次のとおりです。

    -   `[raftstore]`の`apply-pool-size`の値が小さすぎます。この値は`[1, 5]`から大きすぎない範囲に設定することをお勧めします。 `Thread CPU` / `apply cpu`という値も比較的高いです。
    -   マシン上の CPU リソースが不十分です。
    -   単一リージョンの書き込みホットスポットの問題 (現在、この問題の解決はまだ途中です)。単一の`apply`スレッドの CPU 使用率が高くなります (これは、 Grafana 式を変更して`by (instance, name)`を追加することで確認できます)。
    -   RocksDB への書き込みが遅く、 `RocksDB kv` / `max write duration`は高いです。単一のRaftログには複数のキーと値のペア (kv) が含まれる場合があります。 128 kv がバッチで RocksDB に書き込まれるため、1 つの`apply`ログに複数の RocksDB 書き込みが含まれる可能性があります。
    -   他の原因については、バグとして報告してください。

-   `raft commit log`は遅いです。 TiKV Grafana では、 `Raft I/O`と`commit log duration` (Grafana 4.x でのみ利用可能) メトリクスは比較的高くなります。各リージョンは独立したRaftグループに対応します。 Raft には、TCP のスライディング ウィンドウ メカニズムと同様のフロー制御メカニズムがあります。スライディング ウィンドウのサイズを制御するには、 `[raftstore] raft-max-inflight-msgs`パラメータを調整します。書き込みホットスポットがあり、 `commit log duration`が高い場合は、このパラメータを`1024`などのより大きな値に適切に設定できます。

### ログから I/O 問題を特定する {#locate-i-o-issues-from-log}

-   クライアントが`server is busy` 、特に`raftstore is busy`などのエラーを報告する場合、そのエラーは I/O の問題に関連している可能性があります。

    監視パネル ( **[Grafana** ] -&gt; **[TiKV]** -&gt; [**エラー**]) をチェックして、 `busy`エラーの具体的な原因を確認できます。 `server is busy`は TiKV のフロー制御メカニズムです。このようにして、TiKV は、TiKV の現在の圧力が高すぎるため、クライアントは後で試行する必要があることを`tidb/ti-client`通知します。

-   TiKV RocksDB ログに`Write stall`が表示されます。

    レベル 0 の SST ファイルが多すぎると書き込み停止が発生する可能性があります。この問題に対処するには、 `[rocksdb] max-sub-compactions = 2 (or 3)`パラメータを追加して、レベル 0 SST ファイルの圧縮を高速化します。このパラメーターは、レベル 0 からレベル 1 までの圧縮タスクをマルチスレッド同時実行のために`max-sub-compactions`サブタスクに分割できることを意味します。

    ディスクの I/O 能力が書き込みに追いつかない場合は、ディスクをスケールアップすることをお勧めします。ディスクのスループットが上限に達し (たとえば、SATA SSD のスループットが NVMe SSD のスループットよりもはるかに低い)、その結果書き込みが停止するが、CPU リソースが比較的十分である場合は、圧縮を使用してみることができます。より高い圧縮率のアルゴリズムを使用してディスクへの圧力を軽減します。つまり、CPU リソースを使用してディスク リソースを補います。

    たとえば、 `default cf compaction`の圧力が比較的高い場合、パラメータ`[rocksdb.defaultcf] compression-per-level = ["no", "no", "lz4", "lz4", "lz4", "zstd" , "zstd"]`を`compression-per-level = ["no", "no", "zstd", "zstd", "zstd", "zstd", "zstd"]`に変更できます。

### アラートで見つかった I/O 問題 {#i-o-issues-found-in-alerts}

クラスター デプロイメント ツール (TiUP) は、デフォルトで、組み込みのアラート項目としきい値を持つアラート コンポーネントを使用してクラスターをデプロイします。次のアラート項目は I/O に関連しています。

-   TiKV_write_stall
-   TiKV_raft_log_lag
-   TiKV_async_request_snapshot_duration_秒
-   TiKV_async_request_write_duration_秒
-   TiKV_raft_append_log_duration_secs
-   TiKV_raft_apply_log_duration_secs

## I/Oの問題を処理する {#handle-i-o-issues}

-   I/O ホットスポットの問題の発生が確認された場合は、「TiDB ホットスポットの問題の処理」を参照して I/O ホットスポットを排除する必要があります。
-   全体的な I/O パフォーマンスがボトルネックになっていることが確認され、アプリケーション側で I/O パフォーマンスが遅れ続けると判断できる場合は、分散データベースのスケーリング機能を活用して、I/O パフォーマンスを向上させることができます。 TiKV ノードの数を増やすと、全体的な I/O スループットが向上します。
-   上記のようにパラメータの一部を調整し、コンピューティング/メモリリソースを使用してディスクstorageリソースを補います。
