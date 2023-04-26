---
title: Troubleshoot Increased Read and Write Latency
summary: Learn how to troubleshoot the issue of increased read and write latency.
---

# 増加した読み取りおよび書き込み遅延のトラブルシューティング {#troubleshoot-increased-read-and-write-latency}

このドキュメントでは、読み取りと書き込みのレイテンシーとジッターの考えられる原因と、これらの問題のトラブルシューティング方法を紹介します。

## 一般的な原因 {#common-causes}

### TiDB 実行計画が正しくない {#incorrect-tidb-execution-plan}

クエリの実行計画は不安定であり、不適切なインデックスを選択する可能性があり、これによりレイテンシーが高くなります。

#### 現象 {#phenomenon}

-   クエリ実行プランがスローログに出力されている場合は、プランを直接表示できます。 `select tidb_decode_plan('xxx...')`ステートメントを実行して、詳細な実行計画を解析します。
-   モニター内のスキャンされたキーの数が異常に増加します。スローログでは`Scan Keys`の数が多い。
-   TiDB での SQL 実行時間は、MySQL などの他のデータベースとは大きく異なります。他のデータベースの実行計画を比較できます (たとえば、 `Join Order`が異なるかどうか)。

#### 考えられる理由 {#possible-reason}

統計は不正確です。

#### トラブルシューティング方法 {#troubleshooting-methods}

-   統計情報の更新
    -   `analyze table`手動で実行し、 `analyze` `crontab`コマンドで定期的に実行して、統計を正確に保ちます。
    -   `auto analyze`を自動的に実行します。 `analyze ratio`のしきい値を下げ、情報収集の頻度を増やし、実行の開始時刻と終了時刻を設定します。次の例を参照してください。
        -   `set global tidb_auto_analyze_ratio=0.2;`
        -   `set global tidb_auto_analyze_start_time='00:00 +0800';`
        -   `set global tidb_auto_analyze_end_time='06:00 +0800';`
-   実行計画をバインドする
    -   アプリケーション SQL ステートメントを変更し、 `use index`を実行して、列のインデックスを一貫して使用します。
    -   バージョン 3.0 では、アプリケーション SQL ステートメントを変更する必要はありません。 `create global binding`を使用して、 `force index`のバインディング SQL ステートメントを作成します。
    -   バージョン 4.0 では、不安定な実行計画によるパフォーマンスの低下を回避する[SQL計画管理](/sql-plan-management.md)がサポートされています。

### PD異常 {#pd-anomalies}

#### 現象 {#phenomenon}

PD TSO の`wait duration`メトリックの異常な増加があります。このメトリクスは、PD がリクエストを返すまでの待機時間を表します。

#### 考えられる理由 {#possible-reasons}

-   ディスクの問題。 PD ノードが配置されているディスクの I/O 負荷が最大になっています。 I/O 要求が高く、ディスクの状態が良好な他のコンポーネントと共に PD が展開されているかどうかを調査します。 **Grafana** -&gt; <strong>disk performance</strong> -&gt; <strong>レイテンシー</strong> / <strong>load</strong>でモニター メトリックを表示することで、原因を確認できます。必要に応じて、FIO ツールを使用してディスクのチェックを実行することもできます。

-   PD ピア間のネットワークの問題。 PD ログには`lost the TCP streaming connection`が表示されます。 PD ノード間のネットワークに問題があるかどうかを確認し、モニター**Grafana** -&gt; <strong>PD</strong> -&gt; <strong>etcd</strong>で`round trip`表示して原因を確認する必要があります。

-   サーバーの負荷が高い。ログには`server is likely overloaded`表示されます。

-   PD がLeaderを選出できない: PD ログは`lease is not expired`を示します。 v3.0.x と v2.1.19 で[この問題](https://github.com/etcd-io/etcd/issues/10355)が修正されました。

-   リーダーの選挙は遅いです。リージョンの読み込み時間が長い。 PD ログで`grep "regions cost"`を実行すると、この問題を確認できます。結果が`load 460927 regions cost 11.77099s`などの秒単位の場合、リージョンの読み込みが遅いことを意味します。 `use-region-storage`を`true`に設定することで v3.0 の`region storage`機能を有効にできます。これにより、リージョンの読み込み時間が大幅に短縮されます。

-   TiDB と PD 間のネットワークの問題。モニター**Grafana** -&gt; <strong>blackbox_exporter</strong> -&gt; <strong>ping レイテンシー</strong>にアクセスして、TiDB から PDLeaderへのネットワークが正常に動作しているかどうかを確認します。

-   PD は`FATAL`エラーを報告し、ログには`range failed to find revision pair`が表示されます。この問題は v3.0.8 ( [#2040](https://github.com/pingcap/pd/pull/2040) ) で修正されています。

-   `/api/v1/regions`インターフェイスを使用する場合、リージョンが多すぎると PD OOM が発生する可能性があります。この問題は v3.0.8 で修正されています ( [#1986](https://github.com/pingcap/pd/pull/1986) )。

-   ローリング アップグレード中の PD OOM。 gRPC メッセージのサイズは制限されておらず、モニターは`TCP InSegs`が比較的大きいことを示しています。この問題は v3.0.6 で修正されています ( [#1952](https://github.com/pingcap/pd/pull/1952) )。

-   PDパニック。 [バグを報告](https://github.com/tikv/pd/issues/new?labels=kind/bug&#x26;template=bug-report.md) .

-   その他の原因。 `curl http://127.0.0.1:2379/debug/pprof/goroutine?debug=2`と[バグを報告](https://github.com/pingcap/pd/issues/new?labels=kind%2Fbug&#x26;template=bug-report.md)を実行してゴルーチンを取得します。

### TiKVの異常 {#tikv-anomalies}

#### 現象 {#phenomenon}

モニターの`KV Cmd Duration`メトリックが異常に増加します。このメトリクスは、TiDB が TiKV にリクエストを送信してから TiDB がレスポンスを受信するまでの時間を表します。

#### 考えられる理由 {#possible-reasons}

-   `gRPC duration`メトリックを確認します。このメトリクスは、TiKV での gRPC リクエストの合計時間を表します。 TiKV の`gRPC duration` TiDB の`KV duration`を比較することで、潜在的なネットワークの問題を見つけることができます。たとえば、gRPC 期間は短いが、TiDB の KV 期間が長い場合、TiDB と TiKV の間のネットワークレイテンシーが高い可能性があるか、TiDB と TiKV の間の NIC 帯域幅が完全に占有されている可能性があることを示しています。

-   TiKV再始動のため再選。
    -   TiKV がパニックした後、 `systemd`でプルアップされ、正常に実行されます。panicが発生したかどうかは、TiKV ログを表示することで確認できます。この問題は予期しないものであるため、発生した場合は[バグを報告](https://github.com/tikv/tikv/issues/new?template=bug-report.md) 。
    -   TiKV は第三者によって停止または強制終了され、その後`systemd`によって引き上げられました。 `dmesg`と TiKV ログを参照して原因を確認してください。
    -   TiKV は OOM であり、再起動を引き起こします。
    -   `THP` (Transparent Hugepage) を動的に調整するため、TiKV がハングします。

-   チェック モニター: TiKV RocksDB で書き込みストールが発生し、再選択されます。モニター**Grafana** -&gt; <strong>TiKV-details</strong> -&gt; <strong>errors が</strong>`server is busy`示しているかどうかを確認できます。

-   ネットワーク分離による再選。

-   `block-cache`構成が大きすぎると、TiKV OOM が発生する可能性があります。問題の原因を確認するには、モニター**Grafana** -&gt; <strong>TiKV-details</strong>で該当するインスタンスを選択して、RocksDB の`block cache size`を確認します。その間、パラメータ`[storage.block-cache] capacity = # "1GB"`が正しく設定されているかどうかを確認します。デフォルトでは、TiKV の`block-cache`マシンの合計メモリの`45%`に設定されています。 TiKV はコンテナーのメモリ制限を超える可能性がある物理マシンのメモリを取得するため、コンテナーに TiKV をデプロイするときに、このパラメーターを明示的に指定する必要があります。

-   コプロセッサー は多数の大きなクエリを受け取り、大量のデータを返します。 gRPC は、コプロセッサがデータを返すのと同じ速さでデータを送信できず、OOM が発生します。原因を確認するには、モニター**Grafana** -&gt; <strong>TiKV-details</strong> -&gt; <strong>coprocessor overview</strong>を表示して、 `response size` `network outbound`トラフィックを超えているかどうかを確認できます。

### シングル TiKV スレッドのボトルネック {#bottleneck-of-a-single-tikv-thread}

TiKV には、ボトルネックになる可能性のあるシングル スレッドがいくつかあります。

-   TiKV インスタンス内のリージョンが多すぎると、単一の gRPC スレッドがボトルネックになります ( **Grafana** -&gt; <strong>TiKV-details</strong> -&gt; <strong>Thread CPU/gRPC CPU Per Thread</strong>メトリックを確認してください)。 v3.x 以降のバージョンでは、 `Hibernate Region`有効にして問題を解決できます。
-   v3.0 より前のバージョンでは、raftstore スレッドまたは適用スレッドがボトルネックになる場合 ( **Grafana** -&gt; <strong>TiKV-details</strong> -&gt; <strong>Thread CPU/raft store CPU</strong>および<strong>Async apply CPU</strong>メトリクスが`80%`を超える)、TiKV (v2 .x) インスタンスまたはマルチスレッドで v3.x にアップグレードします。

### CPU 負荷が増加する {#cpu-load-increases}

#### 現象 {#phenomenon}

CPU リソースの使用量がボトルネックになります。

#### 考えられる理由 {#possible-reasons}

-   ホットスポットの問題
-   全体的な負荷が高い。 TiDB の遅いクエリと高価なクエリを確認します。インデックスを追加するか、バッチでクエリを実行することにより、実行中のクエリを最適化します。もう 1 つの解決策は、クラスターをスケールアウトすることです。

## その他の原因 {#other-causes}

### クラスタのメンテナンス {#cluster-maintenance}

各オンライン クラスタのほとんどには、3 つまたは 5 つのノードがあります。保守対象のマシンに PDコンポーネントがある場合、ノードがリーダーかフォロワーかを判断する必要があります。フォロワーを無効にしても、クラスターの操作には影響しません。リーダーを無効にする前に、リーダーを切り替える必要があります。リーダー交代中は、約3秒のパフォーマンスの揺れが発生します。

### 少数のレプリカがオフライン {#minority-of-replicas-are-offline}

デフォルトでは、各 TiDB クラスターには 3 つのレプリカがあるため、各リージョンにはクラスター内に 3 つのレプリカがあります。これらのリージョンはリーダーを選出し、 Raftプロトコルを介してデータをレプリケートします。 Raftプロトコルは、ノード (レプリカの半分未満) が故障したり分離されたりした場合でも、TiDB がデータ損失なしでサービスを提供できることを保証します。 3 つのレプリカを持つクラスターの場合、1 つのノードの障害によってパフォーマンスのジッターが発生する可能性がありますが、理論上の使いやすさと正確性には影響しません。

### 新しいインデックス {#new-indexes}

インデックスを作成すると、TiDB がテーブルをスキャンしてインデックスをバックフィルするときに、大量のリソースが消費されます。インデックスの作成は、頻繁に更新されるフィールドと競合することさえあり、アプリケーションに影響を与えます。大規模なテーブルでのインデックスの作成には時間がかかることが多いため、インデックスの作成時間とクラスターのパフォーマンスのバランスを取るようにする必要があります (たとえば、オフピーク時にインデックスを作成するなど)。

**パラメータ調整:**

現在、 `tidb_ddl_reorg_worker_cnt`と`tidb_ddl_reorg_batch_size`を使用して、インデックス作成の速度を動的に調整できます。通常、値が小さいほど、システムへの影響は小さくなりますが、実行時間は長くなります。

一般的なケースでは、最初にデフォルト値 ( `4`および`256` ) を維持し、クラスターのリソース使用率と応答速度を観察してから、値`tidb_ddl_reorg_worker_cnt`を増やして同時実行性を高めることができます。モニターに明らかなジッターが見られない場合は、値`tidb_ddl_reorg_batch_size`を増やします。インデックスの作成に関係する列が頻繁に更新される場合、多くの競合が発生するため、インデックスの作成が失敗し、再試行されます。

さらに、 `tidb_ddl_reorg_priority` ～ `PRIORITY_HIGH`の値を設定して、インデックスの作成を優先し、プロセスを高速化することもできます。ただし、一般的な OLTP システムでは、デフォルト値を維持することをお勧めします。

### 高 GC 圧力 {#high-gc-pressure}

TiDB のトランザクションは、Multi-Version Concurrency Control (MVCC) メカニズムを採用しています。新しく書き込まれたデータが古いデータを上書きする場合、古いデータは置き換えられず、両方のバージョンのデータが保存されます。タイムスタンプは、異なるバージョンをマークするために使用されます。 GC のタスクは、古いデータを消去することです。

-   Resolve Locks のフェーズでは、大量の`scan_lock`リクエストが TiKV で作成されます。これは gRPC 関連のメトリックで確認できます。これら`scan_lock`リクエストは、すべてのリージョンを呼び出します。
-   範囲の削除のフェーズでは、いくつかの (またはまったくない) `unsafe_destroy_range`リクエストが TiKV に送信されます。これは、gRPC 関連のメトリックと**GC タスク**パネルで確認できます。
-   Do GC のフェーズでは、デフォルトで各 TiKV がマシン上のリーダー リージョンをスキャンし、各リーダーに対して GC を実行します。これは**GC タスク**パネルで確認できます。
