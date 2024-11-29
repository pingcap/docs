---
title: Troubleshoot High Disk I/O Usage in TiDB
summary: TiDBstorageI/O 使用率が高い問題を特定して対処する方法を学びます。
---

# TiDB でのディスク I/O 使用率が高い場合のトラブルシューティング {#troubleshoot-high-disk-i-o-usage-in-tidb}

このドキュメントでは、TiDB でのディスク I/O 使用率が高い問題を特定して対処する方法について説明します。

## 現在のI/Oメトリックを確認する {#check-the-current-i-o-metrics}

CPU ボトルネックとトランザクション競合によるボトルネックをトラブルシューティングした後、TiDB の応答が遅くなる場合は、現在のシステム ボトルネックを特定するために I/O メトリックを確認する必要があります。

### モニターからI/Oの問題を特定する {#locate-i-o-issues-from-monitor}

I/O の問題を見つける最も簡単な方法は、 TiUPによってデフォルトでデプロイされる Grafana ダッシュボードなどのモニターから全体的な I/O ステータスを表示することです。I/O に関連するダッシュボード パネルには、 **Overview** 、 **Node_exporter** 、および**Disk-Performance**があります。

#### 最初のタイプの監視パネル {#the-first-type-of-monitoring-panels}

**「概要」** &gt; **「システム情報」** &gt; **「IO 使用率」**では、クラスター内の各マシンの I/O ステータスを確認できます。このメトリックは、Linux `iostat`モニターの`util`に似ています。パーセンテージが高いほど、ディスク I/O の使用率が高いことを示します。

-   モニターで I/O 使用率が高いマシンが 1 台だけの場合、現在このマシンに読み取りおよび書き込みのホットスポットがある可能性があります。
-   モニター内のほとんどのマシンの I/O 使用率が高い場合、クラスターの I/O 負荷が高くなります。

上記の最初の状況 (I/O 使用率が高いマシンが 1 台のみ) の場合、**ディスク パフォーマンス ダッシュボード**の I/O メトリック ( `Disk Latency`や`Disk Load`など) をさらに観察して、異常が存在するかどうかを判断できます。必要に応じて、fio ツールを使用してディスクをチェックします。

#### 2番目のタイプの監視パネル {#the-second-type-of-monitoring-panels}

TiDB クラスターの主なstorageコンポーネントは TiKV です。1 つの TiKV インスタンスには 2 つの RocksDB インスタンスが含まれます。1 つは`data/raft`にあるRaftログを保存するためのもので、もう 1 つは`data/db`にある実際のデータを保存するものです。

**TiKV-Details** &gt; **Raft IO**では、次の 2 つのインスタンスのディスク書き込みに関連するメトリックを確認できます。

-   `Append log duration` : このメトリックは、 Raftログ`.99`保存する RockDB への書き込みの応答時間を示します。2 応答時間は 50 ミリ秒以内である必要があります。
-   `Apply log duration` : このメトリックは、実際のデータを保存する RockDB への書き込みの応答時間を示します。 `.99`応答は 100 ミリ秒以内である必要があります。

これら 2 つのメトリックには**、書き込みホットスポットを表示するのに役立つサーバーごとの**監視パネルもあります。

#### 3番目のタイプの監視パネル {#the-third-type-of-monitoring-panels}

**TiKV-Details** &gt; **Storage**には、storageに関連する監視メトリックがあります。

-   `Storage command total` : 受信した異なるコマンドの数を示します。
-   `Storage async write duration` : `disk sync duration`などのRaft I/O に関連する可能性のある監視メトリックが含まれます。異常な状況が発生した場合は、ログを確認して関連コンポーネントの動作状態を確認してください。

#### その他のパネル {#other-panels}

さらに、他のパネル メトリックは、ボトルネックが I/O であるかどうかを判断するのに役立つ場合があり、いくつかのパラメータを設定することもできます。TiKV gRPC 期間の prewrite/commit/raw-put (raw キー値クラスターのみ) を確認することで、ボトルネックが確かに遅い TiKV 書き込みであることを判断できます。遅い TiKV 書き込みの一般的な状況は次のとおりです。

-   `append log`は遅いです。TiKV Grafana の`Raft I/O`と`append log duration`メトリックは比較的高く、これは多くの場合、ディスク書き込みが遅いことが原因です。RocksDB **-raft**で`WAL Sync Duration max`の値をチェックして、遅い`append log`の原因を特定できます。それ以外の場合は、バグを報告する必要があるかもしれません。

-   `raftstore`スレッドはビジーです。TiKV Grafana では、 `Raft Propose` / `propose wait duration` `append log duration`よりも大幅に高くなっています。トラブルシューティングのために次の点を確認してください。

    -   `[raftstore]`のうち`store-pool-size`の値が小さすぎるかどうか。この値は`[1,5]`から大きすぎない範囲に設定することをお勧めします。
    -   マシンのCPUリソースが不足しているかどうか。

-   `apply log`は遅いです。TiKV Grafana の`Raft I/O`と`apply log duration`メトリックは比較的高く、通常は比較的高い`Raft Propose` / `apply wait duration`とともに発生する可能性があります。考えられる原因は次のとおりです。

    -   `apply-pool-size`の値は小さすぎます。この値は`[1, 5]`から大きすぎない範囲`[raftstore]`設定することをお勧めします`Thread CPU` / `apply cpu`の値も比較的高いです。
    -   マシンの CPU リソースが不足しています。
    -   単一リージョンの書き込みホットスポットの問題 (現在、この問題の解決はまだ進行中です)。単一`apply`スレッドの CPU 使用率が高くなっています (これは、Grafana 式を変更して`by (instance, name)`を追加することで確認できます)。
    -   RocksDB への書き込みが遅く、 `RocksDB kv` / `max write duration`高いです。1 つのRaftログに複数のキーと値のペア (kv) が含まれる場合があります。128 の kv が一括で RocksDB に書き込まれるため、1 つの`apply`ログに複数の RocksDB 書き込みが含まれる可能性があります。
    -   その他の原因の場合は、バグとして報告してください。

-   `raft commit log`は遅いです。TiKV Grafana では、 `Raft I/O`と`commit log duration` (Grafana 4.x でのみ使用可能) のメトリックは比較的高くなっています。各リージョンは独立したRaftグループに対応しています。Raftには、TCP のスライディング ウィンドウ メカニズムに似たフロー制御メカニズムがあります。スライディング ウィンドウのサイズを制御するには、 `[raftstore] raft-max-inflight-msgs`パラメータを調整します。書き込みホットスポットがあり、 `commit log duration`が高い場合は、このパラメータを`1024`などのより大きな値に設定できます。

### ログからI/Oの問題を特定する {#locate-i-o-issues-from-log}

-   クライアントが`server is busy`や特に`raftstore is busy`などのエラーを報告する場合、エラーは I/O の問題に関連している可能性があります。

    監視パネル ( **Grafana** -&gt; **TiKV** -&gt;**エラー**) をチェックして、 `busy`エラーの具体的な原因を確認できます`server is busy`は TiKV のフロー制御メカニズムです。このようにして、TiKV は`tidb/ti-client` 、TiKV の現在の圧力が高すぎるため、クライアントは後で再試行する必要があることを通知します。

-   TiKV RocksDB ログに`Write stall`表示されます。

    レベル 0 SST ファイルが多すぎると、書き込みが停止する可能性があります。この問題に対処するには、 `[rocksdb] max-sub-compactions = 2 (or 3)`パラメータを追加して、レベル 0 SST ファイルの圧縮を高速化できます。このパラメータは、レベル 0 からレベル 1 への圧縮タスクを`max-sub-compactions`サブタスクに分割して、マルチスレッドの同時実行ができることを意味します。

    ディスクの I/O 能力が書き込みに追いつかない場合は、ディスクをスケールアップすることをお勧めします。ディスクのスループットが上限に達し (たとえば、SATA SSD のスループットが NVMe SSD のスループットよりはるかに低い)、書き込みが停止するが、CPU リソースが比較的十分な場合は、より高い圧縮率の圧縮アルゴリズムを使用してディスクの負荷を軽減し、CPU リソースを使用してディスク リソースを補うことができます。

    例えば、 `default cf compaction`の圧力が比較的高い場合は、パラメータ`[rocksdb.defaultcf] compression-per-level = ["no", "no", "lz4", "lz4", "lz4", "zstd", "zstd"]` `compression-per-level = ["no", "no", "zstd", "zstd", "zstd", "zstd", "zstd"]`に変更できます。

### アラートでI/Oの問題が見つかりました {#i-o-issues-found-in-alerts}

クラスター デプロイメント ツール (TiUP) は、アラート項目としきい値が組み込まれたアラート コンポーネントをデフォルトで使用してクラスターをデプロイします。次のアラート項目は I/O に関連しています。

-   TiKV_書き込みストール
-   TiKV_ラフトログラグ
-   TiKV_async_request_スナップショット継続時間秒
-   TiKV_async_request_write_duration_seconds
-   TiKV_raft_append_log_duration_secs
-   TiKV_raft_apply_log_duration_secs

## I/Oの問題を処理する {#handle-i-o-issues}

-   I/O ホットスポットの問題が発生したことが確認された場合は、「TiDB ホットスポットの問題の処理」を参照して I/O ホットスポットを排除する必要があります。
-   全体的な I/O パフォーマンスがボトルネックになっていることが確認され、アプリケーション側で I/O パフォーマンスが低下し続けると判断できる場合は、分散データベースのスケーリング機能を活用し、TiKV ノードの数を増やして全体的な I/O スループットを向上させることができます。
-   上記のようにいくつかのパラメータを調整し、コンピューティング/メモリリソースを使用してディスクstorageリソースを補います。
