---
title: Troubleshoot Increased Read and Write Latency
summary: Learn how to troubleshoot the issue of increased read and write latency.
---

# 読み取りおよび書き込み遅延の増加のトラブルシューティング {#troubleshoot-increased-read-and-write-latency}

このドキュメントでは、読み取りおよび書き込みのレイテンシーとジッターの考えられる原因と、これらの問題のトラブルシューティング方法を紹介します。

## よくある原因 {#common-causes}

### 正しくない TiDB 実行計画 {#incorrect-tidb-execution-plan}

クエリの実行プランは不安定で、間違ったインデックスが選択される可能性があり、これによりレイテンシーが長くなります。

#### 現象 {#phenomenon}

-   クエリ実行プランがスローログに出力されている場合は、プランを直接確認できます。 `select tidb_decode_plan('xxx...')`ステートメントを実行して、詳細な実行計画を解析します。
-   モニター内でスキャンされたキーの数が異常に増加します。遅いログでは`Scan Keys`の数が多くなります。
-   TiDB での SQL 実行時間は、MySQL などの他のデータベースとは大きく異なります。他のデータベースの実行計画を比較できます (たとえば、 `Join Order`が異なるかどうかなど)。

#### 考えられる理由 {#possible-reason}

統計は不正確です。

#### トラブルシューティング方法 {#troubleshooting-methods}

-   統計情報を更新する
    -   統計を正確に保つために、 `analyze table`手動で実行し、 `crontab`コマンドを使用して`analyze`定期的に実行します。
    -   `auto analyze`を自動で実行します。しきい値`analyze ratio`を下げ、情報収集の頻度を上げ、実行の開始時刻と終了時刻を設定します。次の例を参照してください。
        -   `set global tidb_auto_analyze_ratio=0.2;`
        -   `set global tidb_auto_analyze_start_time='00:00 +0800';`
        -   `set global tidb_auto_analyze_end_time='06:00 +0800';`
-   実行計画をバインドする
    -   アプリケーション SQL ステートメントを変更し、 `use index`実行して列のインデックスを一貫して使用します。
    -   3.0 バージョンでは、アプリケーション SQL ステートメントを変更する必要はありません。 `create global binding`を使用して`force index`のバインディング SQL ステートメントを作成します。
    -   4.0 バージョンでは[SQL計画管理](/sql-plan-management.md)がサポートされており、不安定な実行プランによって引き起こされるパフォーマンスの低下を回避します。

### PD異常 {#pd-anomalies}

#### 現象 {#phenomenon}

PD TSO の`wait duration`メトリックが異常に増加しています。このメトリクスは、PD がリクエストを返すまでの待機時間を表します。

#### 考えられる理由 {#possible-reasons}

-   ディスクの問題。 PD ノードが配置されているディスクには、完全な I/O 負荷がかかっています。 PD が、I/O 要求の高い他のコンポーネントおよびディスクの健全性とともにデプロイされているかどうかを調査します。 **Grafana** -&gt;**ディスクパフォ​​ーマンス**-&gt;**レイテンシー**/**負荷**でモニターメトリクスを表示することで、原因を確認できます。必要に応じて、FIO ツールを使用してディスクのチェックを実行することもできます。

-   PD ピア間のネットワークの問題。 PD ログには`lost the TCP streaming connection`が表示されます。 PD ノード間のネットワークに問題があるかどうかを確認し、モニターの**Grafana** -&gt; **PD** -&gt; **etcd**の`round trip`表示して原因を検証する必要があります。

-   サーバー負荷が高い。ログには`server is likely overloaded`表示されます。

-   PD はLeaderを選出できません: PD ログには`lease is not expired`表示されます。 [この問題](https://github.com/etcd-io/etcd/issues/10355) v3.0.x および v2.1.19 で修正されました。

-   リーダー選出は遅々として進まない。リージョンのロード時間が長い。 PD ログで`grep "regions cost"`を実行すると、この問題を確認できます。結果が`load 460927 regions cost 11.77099s`などの秒単位の場合は、リージョンの読み込みが遅いことを意味します。 v3.0 では`use-region-storage`を`true`に設定することで`region storage`機能を有効にすることができ、これによりリージョンの読み込み時間が大幅に短縮されます。

-   TiDB と PD の間のネットワークの問題。 **Grafana** -&gt; **blackbox_exporter** -&gt; **ping レイテンシー**モニターにアクセスして、TiDB から PD Leaderまでのネットワークが正常に動作しているかどうかを確認します。

-   PD は`FATAL`エラーを報告し、ログには`range failed to find revision pair`が表示されます。この問題は v3.0.8 ( [#2040](https://github.com/pingcap/pd/pull/2040) ) で修正されました。

-   `/api/v1/regions`インターフェイスが使用される場合、リージョンが多すぎると PD OOM が発生する可能性があります。この問題は v3.0.8 ( [#1986](https://github.com/pingcap/pd/pull/1986) ) で修正されました。

-   ローリング アップグレード中の PD OOM。 gRPC メッセージのサイズには制限がなく、モニターには`TCP InSegs`が比較的大きいことが示されます。この問題は v3.0.6 ( [#1952](https://github.com/pingcap/pd/pull/1952) ) で修正されました。

-   PDはパニックに陥ります。 [バグを報告](https://github.com/tikv/pd/issues/new?labels=kind/bug&#x26;template=bug-report.md) .

-   その他の原因。 `curl http://127.0.0.1:2379/debug/pprof/goroutine?debug=2`と[バグを報告](https://github.com/pingcap/pd/issues/new?labels=kind%2Fbug&#x26;template=bug-report.md)を実行して goroutine を取得します。

### TiKV の異常 {#tikv-anomalies}

#### 現象 {#phenomenon}

モニターの`KV Cmd Duration`メトリックが異常に増加します。このメトリックは、TiDB が TiKV にリクエストを送信してから TiDB が応答を受信するまでの時間を表します。

#### 考えられる理由 {#possible-reasons}

-   `gRPC duration`メトリックを確認します。このメトリクスは、TiKV での gRPC リクエストの合計時間を表します。 TiKV の`gRPC duration` TiDB の`KV duration`を比較することで、潜在的なネットワークの問題を見つけることができます。たとえば、gRPC の期間は短いですが、TiDB の KV の期間は長く、これは、TiDB と TiKV の間のネットワークレイテンシーが高い可能性があるか、TiDB と TiKV の間の NIC 帯域幅が完全に占有されている可能性があることを示しています。

-   TiKV再始動のため再選。
    -   TiKV がパニックになった後は、 `systemd`にプルアップされ、正常に動作します。panicが発生したかどうかは、TiKV ログを表示することで確認できます。この問題は予期せぬものであるため、発生した場合は[バグを報告](https://github.com/tikv/tikv/issues/new?template=bug-report.md) 。
    -   TiKV は第三者によって停止または強制終了され、 `systemd`つ引き上げられます。 `dmesg`とTiKVログを参照して原因を確認してください。
    -   TiKV は OOM であるため、再起動が発生します。
    -   TiKV は、 `THP` (透明な巨大ページ) を動的に調整するためにハングします。

-   モニターのチェック: TiKV RocksDB で書き込み停止が発生したため、再選択が発生します。モニター**Grafana** -&gt; **TiKV-details** -&gt;**エラー**に`server is busy`表示されるかどうかを確認できます。

-   ネットワーク孤立のため再選。

-   `block-cache`構成が大きすぎる場合、TiKV OOM が発生する可能性があります。問題の原因を確認するには、モニター**Grafana** -&gt; **TiKV-details**で対応するインスタンスを選択して、RocksDB の`block cache size`を確認します。その間、 `[storage.block-cache] capacity = # "1GB"`パラメータが正しく設定されているかどうかを確認してください。デフォルトでは、TiKV の`block-cache`マシンの合計メモリの`45%`に設定されています。 TiKV は物理マシンのメモリを取得するため、コンテナに TiKV をデプロイするときにこのパラメータを明示的に指定する必要があります。これは、コンテナのメモリ制限を超える可能性があります。

-   コプロセッサーは多くの大規模なクエリを受信し、大量のデータを返します。 gRPC は、コプロセッサがデータを返すのと同じくらい早くデータを送信できないため、OOM が発生します。原因を確認するには、モニター**Grafana** -&gt; **TiKV 詳細**-&gt;**コプロセッサー概要**を表示して、 `response size` `network outbound`トラフィックを超えているかどうかを確認できます。

### 単一 TiKV スレッドのボトルネック {#bottleneck-of-a-single-tikv-thread}

TiKV にはボトルネックとなる可能性のある単一スレッドがいくつかあります。

-   TiKV インスタンス内のリージョンが多すぎると、単一の gRPC スレッドがボトルネックになります ( **Grafana** -&gt; **TiKV の詳細**-&gt;**スレッド CPU/スレッドあたりの gRPC CPU**メトリックを確認してください)。 v3.x 以降のバージョンでは、 `Hibernate Region`有効にすることで問題を解決できます。
-   v3.0 より前のバージョンでは、raftstore スレッドまたは適用スレッドがボトルネックになる場合 ( **Grafana** -&gt; **TiKV-details** -&gt;**スレッド CPU/raft ストア CPU**および**非同期適用 CPU**メトリックが`80%`を超える)、TiKV (v2) をスケールアウトできます。 .x) インスタンスを使用するか、マルチスレッドを使用して v3.x にアップグレードします。

### CPU負荷が増加する {#cpu-load-increases}

#### 現象 {#phenomenon}

CPU リソースの使用量がボトルネックになります。

#### 考えられる理由 {#possible-reasons}

-   ホットスポットの問題
-   全体的な負荷が高い。 TiDB の遅いクエリと高価なクエリを確認してください。インデックスを追加するか、クエリをバッチで実行することで、実行中のクエリを最適化します。別の解決策は、クラスターをスケールアウトすることです。

## その他の原因 {#other-causes}

### クラスタのメンテナンス {#cluster-maintenance}

各オンライン クラスターのほとんどには 3 つまたは 5 つのノードがあります。保守対象のマシンに PDコンポーネントがある場合、そのノードがリーダーであるかフォロワーであるかを判断する必要があります。フォロワーを無効にしても、クラスターの動作には影響しません。リーダーを無効にする前に、リーダーを切り替える必要があります。リーダーの変更中に、約 3 秒のパフォーマンスのジッターが発生します。

### 少数のレプリカがオフラインです {#minority-of-replicas-are-offline}

デフォルトでは、各 TiDB クラスターには 3 つのレプリカがあるため、各リージョンにはクラスター内に 3 つのレプリカがあります。これらのリージョンはリーダーを選出し、 Raftプロトコルを通じてデータを複製します。 Raftプロトコルを使用すると、ノード (レプリカの半分未満) に障害が発生したり孤立したりした場合でも、TiDB がデータを損失することなくサービスを提供できることが保証されます。 3 つのレプリカを持つクラスターの場合、1 つのノードの障害がパフォーマンスのジッターを引き起こす可能性がありますが、理論上は使いやすさと正確さには影響しません。

### 新しいインデックス {#new-indexes}

インデックスの作成では、TiDB がテーブルをスキャンしてインデックスをバックフィルするときに大量のリソースが消費されます。インデックスの作成は、頻繁に更新されるフィールドと競合する可能性もあり、アプリケーションに影響を与えます。大きなテーブルでのインデックスの作成には長い時間がかかることが多いため、インデックスの作成時間とクラスターのパフォーマンスのバランスを取るように努める必要があります (たとえば、オフピーク時にインデックスを作成するなど)。

**パラメータ調整：**

現在、 `tidb_ddl_reorg_worker_cnt`と`tidb_ddl_reorg_batch_size`を使用してインデックス作成の速度を動的に調整できます。通常、値が小さいほどシステムへの影響は小さくなりますが、実行時間は長くなります。

一般に、まずデフォルト値 ( `4`および`256` ) を保持し、クラスターのリソース使用量と応答速度を観察してから、値`tidb_ddl_reorg_worker_cnt`を増やして同時実行性を高めます。モニターに明らかなジッターが観察されない場合は、 `tidb_ddl_reorg_batch_size`の値を増やします。インデックスの作成に関係する列が頻繁に更新される場合、多くの競合が発生してインデックスの作成が失敗し、再試行されます。

さらに、値`tidb_ddl_reorg_priority` ～ `PRIORITY_HIGH`を設定して、インデックスの作成を優先し、プロセスを高速化することもできます。ただし、一般的な OLTP システムでは、デフォルト値を使用することをお勧めします。

### 高い GC 圧力 {#high-gc-pressure}

TiDB のトランザクションは、Multi-Version Concurrency Control (MVCC) メカニズムを採用しています。新しく書き込まれたデータが古いデータを上書きする場合、古いデータは置き換えられず、両方のバージョンのデータが保存されます。タイムスタンプは、異なるバージョンをマークするために使用されます。 GC のタスクは、古いデータを消去することです。

-   ロックの解決フェーズでは、TiKV で大量の`scan_lock`リクエストが作成されます。これは、gRPC 関連のメトリクスで確認できます。これら`scan_lock`リクエストはすべてのリージョンを呼び出します。
-   範囲の削除フェーズでは、いくつかの (またはまったく) `unsafe_destroy_range`リクエストが TiKV に送信されます。これは、gRPC 関連のメトリクスと**GC タスク**パネルで確認できます。
-   Do GC フェーズでは、各 TiKV はデフォルトでマシン上のリーダー リージョンをスキャンし、各リーダーに対して GC を実行します。これは**GC タスク**パネルで確認できます。
