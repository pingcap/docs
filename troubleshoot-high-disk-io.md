---
title: Troubleshoot High Disk I/O Usage in TiDB
summary: Learn how to locate and address the issue of high TiDB storage I/O usage.
---

# TiDB でのディスク I/O 使用率が高い場合のトラブルシューティング {#troubleshoot-high-disk-i-o-usage-in-tidb}

このドキュメントでは、TiDB でのディスク I/O 使用率が高い問題を特定して対処する方法を紹介します。

## 現在の I/O メトリックを確認する {#check-the-current-i-o-metrics}

CPU のボトルネックとトランザクションの競合によるボトルネックのトラブルシューティングを行った後、TiDB の応答が遅くなった場合は、現在のシステムのボトルネックを特定するために I/O メトリックを確認する必要があります。

### モニターから I/O の問題を特定する {#locate-i-o-issues-from-monitor}

I/O の問題を見つける最も簡単な方法は、 TiUPによってデフォルトでデプロイされる Grafana ダッシュボードなど、モニターから全体的な I/O ステータスを表示することです。 I/O に関連するダッシュボード パネルには、 **Overview** 、 <strong>Node_exporter</strong> 、および<strong>Disk-Performance</strong>が含まれます。

#### 最初のタイプの監視パネル {#the-first-type-of-monitoring-panels}

**[Overview]** &gt; <strong>[System Info]</strong> &gt; <strong>[IO Util]</strong>で、クラスター内の各マシンの I/O ステータスを確認できます。このメトリックは、Linux `iostat`モニターの`util`に似ています。パーセンテージが高いほど、ディスク I/O 使用率が高いことを表します。

-   モニターに I/O 使用率の高いマシンが 1 つしかない場合は、現在、このマシンに読み取りおよび書き込みのホットスポットがある可能性があります。
-   モニター内のほとんどのマシンの I/O 使用率が高い場合、クラスターの I/O 負荷が高くなります。

上記の最初の状況 (I/O 使用率が高い 1 台のマシンのみ) では、**ディスク パフォーマンス ダッシュボード**から`Disk Latency`や`Disk Load`などの I/O メトリックをさらに観察して、異常が存在するかどうかを判断できます。必要に応じて、fio ツールを使用してディスクをチェックします。

#### 2 番目のタイプの監視パネル {#the-second-type-of-monitoring-panels}

TiDB クラスターの主なstorageコンポーネントは TiKV です。 1 つの TiKV インスタンスには`data/raft`つのRaftインスタンスが含ま`data/db`ています。

**TiKV-Details** &gt; <strong>Raft IO</strong>では、これら 2 つのインスタンスのディスク書き込みに関連するメトリックを確認できます。

-   `Append log duration` : このメトリクスは、 Raftログを保存する RockDB への書き込みの応答時間を示します。 `.99`応答時間は 50 ミリ秒以内である必要があります。
-   `Apply log duration` : このメトリクスは、実際のデータを格納する RockDB への書き込みの応答時間を示します。 `.99`応答は 100 ミリ秒以内である必要があります。

これらの 2 つのメトリックには、書き込みホットスポットを表示するのに役立つ、**サーバーごとの**監視パネルもあります。

#### 3 番目のタイプの監視パネル {#the-third-type-of-monitoring-panels}

**TiKV-Details** &gt; <strong>Storage</strong>には、storageに関連するモニタリング メトリックがあります。

-   `Storage command total` : 受信した異なるコマンドの数を示します。
-   `Storage async write duration` : Raft I/O に関連する可能性がある`disk sync duration`などのモニタリング メトリクスが含まれます。異常な状況が発生した場合は、ログを確認して、関連するコンポーネントの動作ステータスを確認してください。

#### その他のパネル {#other-panels}

さらに、その他のパネル メトリックは、ボトルネックが I/O であるかどうかを判断するのに役立つ場合があり、いくつかのパラメーターを設定してみることができます。 TiKV gRPC 期間の prewrite/commit/raw-put (未加工のキー値クラスターのみ) を確認することで、ボトルネックが確かに遅い TiKV 書き込みであると判断できます。 TiKV 書き込みが遅い一般的な状況は次のとおりです。

-   `append log`は遅いです。 TiKV Grafana の`Raft I/O`および`append log duration`メトリックは比較的高く、これは多くの場合、ディスク書き込みが遅いことが原因です。 **RocksDB-raft**で`WAL Sync Duration max`の値を確認して、遅い`append log`の原因を特定できます。それ以外の場合は、バグを報告する必要がある場合があります。

-   `raftstore`スレッドがビジーです。 TiKV Grafana では、 `Raft Propose` / `propose wait duration`は`append log duration`よりも大幅に高くなっています。トラブルシューティングのために次の点を確認してください。

    -   `store-pool-size` of `[raftstore]`の値が小さすぎるかどうか。この値は`[1,5]`から大きすぎない範囲で設定することをお勧めします。
    -   マシンの CPU リソースが不足していませんか。

-   `append log`は遅いです。 TiKV Grafana の`Raft I/O`および`append log duration`メトリックは比較的高く、通常は比較的高い`Raft Propose` / `apply wait duration`とともに発生する可能性があります。考えられる原因は次のとおりです。

    -   `apply-pool-size` `[raftstore]`値は小さすぎます。この値は`[1, 5]`から大きすぎない範囲で設定することをお勧めします。 `Thread CPU`の値`apply cpu`比較的高いです。
    -   マシンの CPU リソースが不足しています。
    -   単一リージョンのホットスポットの問題を書きます (現在、この問題の解決策はまだ開発中です)。単一の`apply`スレッドの CPU 使用率が高くなっています (これは、Grafana 式を変更して`by (instance, name)`を追加することで確認できます)。
    -   RocksDB への書き込みが遅く、 `RocksDB kv` / `max write duration`が高い。単一のRaftログには、複数のキーと値のペア (kv) が含まれる場合があります。 128 kv がバッチで RocksDB に書き込まれるため、1 つの`apply`ログに複数の RocksDB 書き込みが含まれる場合があります。
    -   その他の原因については、バグとして報告してください。

-   `raft commit log`は遅いです。 TiKV Grafana では、 `Raft I/O`および`commit log duration` (Grafana 4.x でのみ使用可能) メトリックが比較的高くなります。各リージョンは、独立したRaftグループに対応します。 Raft には、TCP のスライディング ウィンドウ メカニズムに似たフロー制御メカニズムがあります。スライディング ウィンドウのサイズを制御するには、 `[raftstore] raft-max-inflight-msgs`パラメータを調整します。書き込みホットスポットがあり、 `commit log duration`が高い場合は、このパラメーターを`1024`などのより大きな値に適切に設定できます。

### ログから I/O の問題を特定する {#locate-i-o-issues-from-log}

-   クライアントが`server is busy`や特に`raftstore is busy`などのエラーを報告する場合、エラーは I/O の問題に関連している可能性があります。

    監視パネル ( **Grafana** -&gt; <strong>TiKV</strong> -&gt;<strong>エラー</strong>) をチェックして、 `busy`エラーの具体的な原因を確認できます。 `server is busy`は TiKV のフロー制御メカニズムです。このようにして、TiKV は`tidb/ti-client` 、TiKV の現在の圧力が高すぎることを通知し、クライアントは後で試す必要があります。

-   `Write stall` TiKV RocksDB ログに表示されます。

    レベル 0 の SST ファイルが多すぎると、書き込みが停止する可能性があります。この問題に対処するには、 `[rocksdb] max-sub-compactions = 2 (or 3)`パラメーターを追加して、レベル 0 の SST ファイルの圧縮を高速化します。このパラメーターは、レベル 0 からレベル 1 の圧縮タスクを`max-sub-compactions`サブタスクに分割してマルチスレッド同時実行できることを意味します。

    ディスクの I/O 機能が書き込みに追いつかない場合は、ディスクをスケールアップすることをお勧めします。ディスクのスループットが上限に達し (たとえば、SATA SSD のスループットが NVMe SSD のスループットよりもはるかに低い)、書き込みストールが発生するが、CPU リソースが比較的十分である場合は、圧縮を試すことができます。より高い圧縮率のアルゴリズムを使用して、ディスクの負荷を軽減します。つまり、CPU リソースを使用してディスク リソースを補います。

    たとえば、 `default cf compaction`の圧力が比較的高い場合は、パラメータ`[rocksdb.defaultcf] compression-per-level = ["no", "no", "lz4", "lz4", "lz4", "zstd" , "zstd"]`を`compression-per-level = ["no", "no", "zstd", "zstd", "zstd", "zstd", "zstd"]`に変更できます。

### アラートで見つかった I/O の問題 {#i-o-issues-found-in-alerts}

クラスター デプロイ ツール (TiUP) は、既定で、組み込みのアラート アイテムとしきい値を持つアラート コンポーネントを使用してクラスターをデプロイします。以下のアラート項目は、I/O に関連しています。

-   TiKV_write_stall
-   TiKV_raft_log_lag
-   TiKV_async_request_snapshot_duration_seconds
-   TiKV_async_request_write_duration_seconds
-   TiKV_raft_append_log_duration_secs
-   TiKV_raft_apply_log_duration_secs

## I/O の問題を処理する {#handle-i-o-issues}

-   I/O ホットスポットの問題が発生することが確認されたら、TiDB ホットスポットの問題の処理を参照して、I/O ホットスポットを排除する必要があります。
-   全体のI/O性能がボトルネックになっていることが確認でき、アプリケーション側でI/O性能が低下し続けると判断できれば、分散データベースのスケーリング能力を活かしてパフォーマンスを向上させることができます。全体的な I/O スループットを向上させる TiKV ノードの数。
-   上記のようにパラメータの一部を調整し、コンピューティング/メモリリソースを使用してディスクstorageリソースを補います。
