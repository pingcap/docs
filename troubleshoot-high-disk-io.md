---
title: Troubleshoot High Disk I/O Usage in TiDB
summary: TiDBstorageのI/O 使用率が高い問題を特定して対処する方法を学びます。
---

# TiDB におけるディスク I/O 使用率の高騰のトラブルシューティング {#troubleshoot-high-disk-i-o-usage-in-tidb}

このドキュメントでは、TiDB でディスク I/O 使用率が高くなる問題を特定して解決する方法を紹介します。

## 現在のI/Oメトリックを確認する {#check-the-current-i-o-metrics}

CPU ボトルネックとトランザクション競合によるボトルネックをトラブルシューティングした後、TiDB の応答が遅くなる場合は、現在のシステム ボトルネックを特定するために I/O メトリックを確認する必要があります。

### モニターからI/Oの問題を特定する {#locate-i-o-issues-from-monitor}

I/Oの問題を特定する最も簡単な方法は、 TiUPによってデフォルトでデプロイされるGrafanaダッシュボードなどのモニターから全体的なI/Oステータスを確認することです。I/Oに関連するダッシュボードパネルには、 **Overview** 、 **Node_exporter** 、 **Disk-Performance**などがあります。

#### 最初のタイプの監視パネル {#the-first-type-of-monitoring-panels}

**「概要」** &gt; **「システム情報」** &gt; **「IO Util」**では、クラスター内の各マシンのI/Oステータスを確認できます。この指標はLinux `iostat`モニターの`util`に似ています。パーセンテージが高いほど、ディスクI/O使用率が高いことを示します。

-   モニターで I/O 使用率が高いマシンが 1 台だけの場合、現在このマシンに読み取りおよび書き込みのホットスポットがある可能性があります。
-   モニター内のほとんどのマシンの I/O 使用率が高い場合、クラスターの I/O 負荷が高くなっています。

上記の最初の状況（I/O使用率が高いマシンが1台のみ）の場合、**ディスクパフォーマンスダッシュボード**のI/Oメトリック（ `Disk Latency`や`Disk Load`など）をさらに観察し、異常の有無を確認できます。必要に応じて、fioツールを使用してディスクをチェックしてください。

#### 2番目のタイプの監視パネル {#the-second-type-of-monitoring-panels}

TiDBクラスターのメインstorageコンポーネントはTiKVです。1つのTiKVインスタンスには2つのRocksDBインスタンスが含まれます。1つはRaftログを保存するためのもので、 `data/raft`に配置されています。もう1つは実データを保存するためのもので、 `data/db`に配置されています。

**TiKV-Details** &gt; **Raft IO**では、これら 2 つのインスタンスのディスク書き込みに関連するメトリックを確認できます。

-   `Append log duration` : このメトリックは、 Raftログを保存するRockDBへの書き込みの応答時間を示します。2 `.99`応答時間は50ミリ秒以内である必要があります。
-   `Apply log duration` ：このメトリックは、実データを格納するRockDBへの書き込みの応答時間を示します。 `.99`時間は100ミリ秒以内である必要があります。

これら 2 つのメトリックには、書き込みホットスポットを表示するのに役立つ**サーバーごとの**監視パネルもあります。

#### 3番目のタイプの監視パネル {#the-third-type-of-monitoring-panels}

**TiKV-Details** &gt; **Storage**には、storageに関連する監視メトリックがあります。

-   `Storage command total` : 受信した異なるコマンドの数を示します。
-   `Storage async write duration` : `disk sync duration`などの監視メトリックが含まれます。これらはRaft I/Oに関連する可能性があります。異常な状況が発生した場合は、ログを確認して関連コンポーネントの動作状態を確認してください。

#### その他のパネル {#other-panels}

さらに、他のパネル指標もボトルネックがI/Oかどうかを判断するのに役立つ場合があります。また、パラメータの設定を試してみることもできます。TiKV gRPCのprewrite/commit/raw-put（rawキーバリュークラスターのみ）の所要時間を確認することで、ボトルネックがTiKV書き込みの遅さにあることを判断できます。TiKV書き込みが遅い場合の一般的な状況は以下のとおりです。

-   `append log`は遅いです。TiKV Grafana の`Raft I/O`と`append log duration`指標は比較的高くなっていますが、これは多くの場合、ディスク書き込みの遅延が原因です。RocksDB **-raft**で`WAL Sync Duration max`の値を確認することで、 `append log`の遅い原因を特定できます。そうでない場合は、バグを報告する必要があるかもしれません。

-   `raftstore`スレッドがビジー状態です。TiKV Grafana では、 `Raft Propose` / `propose wait duration` `append log duration`よりも大幅に高い値です。トラブルシューティングのために、以下の点を確認してください。

    -   `[raftstore]`のうち`store-pool-size`の値が小さすぎないか。この値は`[1,5]` 、大きすぎない範囲に設定することをお勧めします。
    -   マシンのCPUリソースが不足しているかどうか。

-   `apply log`は遅いです。TiKV Grafana の`Raft I/O`と`apply log duration`指標は比較的高く、これは通常、 `Raft Propose` / `apply wait duration`指標も比較的高い場合に発生します。考えられる原因は次のとおりです。

    -   `[raftstore]`のうち`apply-pool-size`は小さすぎます。この値は`[1, 5]`から大きすぎない範囲に設定することをお勧めします。7と`Thread CPU` `apply cpu`比較的高い値です。
    -   マシンの CPU リソースが不足しています。
    -   単一リージョンの書き込みホットスポットの問題（現在、この問題の解決は進行中です）。単一スレッド`apply`のCPU使用率が高くなっています（Grafana式に`by (instance, name)`追加することで確認できます）。
    -   RocksDBへの書き込み速度が遅く、 `RocksDB kv` / `max write duration`高い値です。1つのRaftログには複数のキーと値のペア（kv）が含まれる場合があります。128 kvが一括でRocksDBに書き込まれるため、 `apply`ログ1つにつきRocksDBへの書き込みが複数回発生する可能性があります。
    -   その他の原因の場合は、バグとして報告してください。

-   `raft commit log`は遅いです。TiKV Grafanaでは、 `Raft I/O`と`commit log duration` （Grafana 4.xのみで利用可能）のメトリックは比較的高いです。各リージョンは独立したRaftグループに対応しています。Raftは、TCPのスライディングウィンドウ機構に似たフロー制御機構を備えています。スライディングウィンドウのサイズを制御するには、 `[raftstore] raft-max-inflight-msgs`パラメータを調整します。書き込みホットスポットがあり、 `commit log duration`が大きい場合は、このパラメータを`1024`などのより大きな値に設定することで適切に対処できます。

### ログからI/Oの問題を特定する {#locate-i-o-issues-from-log}

-   クライアントが`server is busy`や特に`raftstore is busy`などのエラーを報告する場合、エラーは I/O の問題に関連している可能性があります。

    `busy`エラーの具体的な原因を確認するには、監視パネル（ **Grafana** -&gt; **TiKV** -&gt; **errors** ）を確認してください。9 `server is busy` TiKVのフロー制御メカニズムです。これにより、TiKVは`tidb/ti-client` 、現在のTiKVの負荷が高すぎるため、クライアントは後で再試行する必要があることを通知します。

-   TiKV RocksDB ログに`Write stall`表示されます。

    レベル0のSSTファイルが多すぎると書き込みストールが発生している可能性があります。この問題に対処するには、パラメータ`[rocksdb] max-sub-compactions = 2 (or 3)`を追加してレベル0のSSTファイルの圧縮を高速化できます。このパラメータは、レベル0からレベル1への圧縮タスクを`max-sub-compactions`サブタスクに分割し、マルチスレッドで同時実行できるようにすることを意味します。

    ディスクのI/O性能が書き込みに追いつかない場合は、ディスクのスケールアップをお勧めします。ディスクのスループットが上限に達し（例えば、SATA SSDのスループットがNVMe SSDよりも大幅に低い場合）、書き込みが停止する可能性があるものの、CPUリソースが比較的十分な場合は、より高い圧縮率の圧縮アルゴリズムを使用してディスクの負荷を軽減し、CPUリソースでディスクリソースを補う方法を検討してください。

    たとえば、 `default cf compaction`の圧力が比較的高い場合は、パラメータ`[rocksdb.defaultcf] compression-per-level = ["no", "no", "lz4", "lz4", "lz4", "zstd", "zstd"]`を`compression-per-level = ["no", "no", "zstd", "zstd", "zstd", "zstd", "zstd"]`に変更できます。

### アラートで見つかったI/Oの問題 {#i-o-issues-found-in-alerts}

クラスターデプロイメントツール（TiUP）は、デフォルトでアラート項目としきい値が組み込まれたアラートコンポーネントを使用してクラスターをデプロイします。以下のアラート項目はI/Oに関連しています。

-   TiKV_write_stall
-   TiKV_raft_log_lag
-   TiKV_async_request_snapshot_duration_seconds
-   TiKV_async_request_write_duration_seconds
-   TiKV_raft_append_log_duration_secs
-   TiKV_raft_apply_log_duration_secs

## I/Oの問題を処理する {#handle-i-o-issues}

-   I/O ホットスポットの問題が発生していることが確認された場合は、「TiDB ホットスポットの問題の処理」を参照して I/O ホットスポットを排除する必要があります。
-   全体的な I/O パフォーマンスがボトルネックになっていることが確認され、アプリケーション側で I/O パフォーマンスが低下し続けると判断できる場合は、分散データベースのスケーリング機能を活用し、TiKV ノードの数を増やして全体的な I/O スループットを向上させることができます。
-   上記のようにいくつかのパラメータを調整し、コンピューティング/メモリリソースを使用してディスクstorageリソースを補います。
