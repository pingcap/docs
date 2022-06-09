---
title: Troubleshoot High Disk I/O Usage in TiDB
summary: Learn how to locate and address the issue of high TiDB storage I/O usage.
---

# TiDBでの高ディスクI/O使用量のトラブルシューティング {#troubleshoot-high-disk-i-o-usage-in-tidb}

このドキュメントでは、TiDBでのディスクI/Oの使用率が高い問題を特定して対処する方法を紹介します。

## 現在のI/Oメトリックを確認します {#check-the-current-i-o-metrics}

CPUのボトルネックとトランザクションの競合によって引き起こされたボトルネックをトラブルシューティングした後、TiDBの応答が遅くなる場合は、現在のシステムのボトルネックを特定するためにI/Oメトリックを確認する必要があります。

### モニターからI/Oの問題を特定する {#locate-i-o-issues-from-monitor}

I / Oの問題を見つける最も簡単な方法は、TiUPによってデフォルトで展開されるGrafanaダッシュボードなど、モニターから全体的なI/Oステータスを表示することです。 I / Oに関連するダッシュボードパネルには、 **Overview** 、 <strong>Node_exporter</strong> 、および<strong>Disk-Performance</strong>が含まれます。

#### 最初のタイプの監視パネル {#the-first-type-of-monitoring-panels}

[**概要**]&gt;[<strong>システム情報</strong>]&gt;[ <strong>IOUtil]</strong>で、クラスタの各マシンのI/Oステータスを確認できます。このメトリックは、 `iostat`モニターの`util`に似ています。パーセンテージが高いほど、ディスクI/Oの使用率が高くなります。

-   モニターにI/O使用率の高いマシンが1つしかない場合、現在、このマシンに読み取りおよび書き込みのホットスポットがある可能性があります。
-   モニター内のほとんどのマシンのI/O使用率が高い場合、クラスタのI/O負荷は高くなります。

上記の最初の状況（I / O使用率が高い1台のマシンのみ）の場合、 `Disk Latency`や`Disk Load`などの**ディスクパフォーマンスダッシュボード**からI / Oメトリックをさらに観察して、異常が存在するかどうかを判断できます。必要に応じて、fioツールを使用してディスクをチェックします。

#### 2番目のタイプの監視パネル {#the-second-type-of-monitoring-panels}

TiDBクラスタの主なストレージコンポーネントはTiKVです。 1つのTiKVインスタンスには2つのRocksDBインスタンスが含まれています。1つは`data/raft`にあるRaftログを保存するためのもので、もう1つは`data/db`にある実際のデータを保存するためのものです。

**TiKV-Details** &gt; <strong>Raft IO</strong>で、次の2つのインスタンスのディスク書き込みに関連するメトリックを確認できます。

-   `Append log duration` ：このメトリックは、Raftログを格納するRockDBへの書き込みの応答時間を示します。 `.99`の応答時間は50ミリ秒以内である必要があります。
-   `Apply log duration` ：このメトリックは、実際のデータを格納するRockDBへの書き込みの応答時間を示します。 `.99`の応答は100ミリ秒以内である必要があります。

これらの2つのメトリックには、書き込みホットスポットを表示するのに役立つ**サーバーごと**の監視パネルもあります。

#### 3番目のタイプの監視パネル {#the-third-type-of-monitoring-panels}

**TiKV-詳細**&gt;<strong>ストレージ</strong>には、ストレージに関連する監視メトリックがあります。

-   `Storage command total` ：受信したさまざまなコマンドの数を示します。
-   `Storage async write duration` ：Raft I/Oに関連する可能性のある`disk sync duration`などの監視メトリックが含まれます。異常が発生した場合は、ログを確認して関連部品の動作状態を確認してください。

#### その他のパネル {#other-panels}

さらに、他のいくつかのパネルメトリックは、ボトルネックがI / Oであるかどうかを判断するのに役立つ場合があり、いくつかのパラメーターを設定してみることができます。 TiKVgRPC期間のprewrite/commit / raw-put（rawキー値クラスターの場合のみ）を確認することで、ボトルネックが実際に遅いTiKV書き込みであると判断できます。 TiKVの書き込みが遅い一般的な状況は次のとおりです。

-   `append log`は遅いです。 TiKV Grafanaの`Raft I/O`および`append log duration`メトリックは比較的高く、これは多くの場合、ディスク書き込みが遅いことが原因です。 **RocksDB-raft**で`WAL Sync Duration max`の値を確認して、 `append log`が遅い原因を特定できます。そうしないと、バグを報告する必要があるかもしれません。

-   `raftstore`のスレッドがビジーです。 TiKV Grafanaでは、 `Raft Propose` / `propose wait duration`は`append log duration`よりも大幅に高くなっています。トラブルシューティングについては、次の側面を確認してください。

    -   `[raftstore]`の`store-pool-size`の値が小さすぎるかどうか。この値は`[1,5]`から大きすぎないように設定することをお勧めします。
    -   マシンのCPUリソースが不足していないか。

-   `append log`は遅いです。 TiKV Grafanaの`Raft I/O`および`append log duration`メトリックは比較的高く、通常は比較的高い`Raft Propose`とともに発生する可能性があり`apply wait duration` 。考えられる原因は次のとおりです。

    -   `[raftstore]`の`apply-pool-size`の値が小さすぎます。この値は`[1, 5]`から大きすぎないように設定することをお勧めします。 `Thread CPU`の`apply cpu`も比較的高いです。
    -   マシンのCPUリソースが不足しています。
    -   単一のリージョンのホットスポットの問題を記述します（現在、この問題の解決策はまだ進行中です）。単一の`apply`スレッドのCPU使用率は高くなります（これは、 `by (instance, name)`を追加したGrafana式を変更することで表示できます）。
    -   RocksDBへの書き込みが遅く、 `RocksDB kv` / `max write duration`が高い。単一のRaftログには、複数のキーと値のペア（kv）が含まれる場合があります。 128 kvがバッチでRocksDBに書き込まれるため、1つの`apply`ログに複数のRocksDB書き込みが含まれる場合があります。
    -   その他の原因については、バグとして報告してください。

-   `raft commit log`は遅いです。 TiKV Grafanaでは、 `Raft I/O`と`commit log duration` （Grafana 4.xでのみ使用可能）のメトリックが比較的高くなっています。各リージョンは、独立したRaftグループに対応しています。 Raftには、TCPのスライディングウィンドウメカニズムと同様のフロー制御メカニズムがあります。スライディングウィンドウのサイズを制御するには、 `[raftstore] raft-max-inflight-msgs`パラメータを調整します。書き込みホットスポットがあり、 `commit log duration`が高い場合は、このパラメーターを`1024`などのより大きな値に適切に設定できます。

### ログからI/Oの問題を特定する {#locate-i-o-issues-from-log}

-   クライアントが`server is busy`または特に`raftstore is busy`などのエラーを報告した場合、エラーはI/Oの問題に関連している可能性があります。

    監視パネル（ **Grafana-** &gt; <strong>TiKV-</strong> &gt;<strong>エラー</strong>）をチェックして、 `busy`エラーの具体的な原因を確認できます。 `server is busy`はTiKVのフロー制御メカニズムです。このようにして、TiKVは`tidb/ti-client`の現在の圧力が高すぎることを通知し、クライアントは後で試す必要があります。

-   `Write stall`はTiKVRocksDBログに表示されます。

    レベル0のSSTファイルが多すぎると、書き込みストールが発生する可能性があります。この問題に対処するために、 `[rocksdb] max-sub-compactions = 2 (or 3)`パラメーターを追加して、レベル0のSSTファイルの圧縮を高速化できます。このパラメーターは、レベル0からレベル1の圧縮タスクを、マルチスレッドの同時実行のために`max-sub-compactions`のサブタスクに分割できることを意味します。

    ディスクのI/O機能が書き込みに追いつかない場合は、ディスクをスケールアップすることをお勧めします。ディスクのスループットが上限に達した場合（たとえば、SATASSDのスループットがNVMeSSDのスループットよりもはるかに低い場合）、書き込みストールが発生しますが、CPUリソースが比較的十分である場合は、圧縮を使用してみてください。ディスクへの圧力を軽減するためのより高い圧縮率のアルゴリズム。つまり、CPUリソースを使用してディスクリソースを補います。

    たとえば、 `default cf compaction`の圧力が比較的高い場合は、パラメータ`[rocksdb.defaultcf] compression-per-level = ["no", "no", "lz4", "lz4", "lz4", "zstd" , "zstd"]`を`compression-per-level = ["no", "no", "zstd", "zstd", "zstd", "zstd", "zstd"]`に変更できます。

### アラートで見つかったI/Oの問題 {#i-o-issues-found-in-alerts}

クラスタ展開ツール（TiUP）は、アラート項目としきい値が組み込まれているアラートコンポーネントをデフォルトで使用してクラスタを展開します。次のアラート項目はI/Oに関連しています。

-   TiKV_write_stall
-   TiKV_raft_log_lag
-   TiKV_async_request_snapshot_duration_seconds
-   TiKV_async_request_write_duration_seconds
-   TiKV_raft_append_log_duration_secs
-   TiKV_raft_apply_log_duration_secs

## I/Oの問題を処理する {#handle-i-o-issues}

-   I / Oホットスポットの問題が発生していることが確認されたら、「TiDBホットスポットの問題の処理」を参照してI/Oホットスポットを排除する必要があります。
-   全体的なI/Oパフォーマンスがボトルネックになっていることが確認され、I / Oパフォーマンスがアプリケーション側で遅れ続けると判断できる場合は、分散データベースのスケーリング機能を利用して、全体的なI/Oスループットを向上させるTiKVノードの数。
-   上記のようにいくつかのパラメータを調整し、コンピューティング/メモリリソースを使用してディスクストレージリソースを補います。
