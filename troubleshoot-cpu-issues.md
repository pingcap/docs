---
title: Troubleshoot Increased Read and Write Latency
summary: Learn how to troubleshoot the issue of increased read and write latency.
---

# 読み取りと書き込みの待ち時間の増加のトラブルシューティング {#troubleshoot-increased-read-and-write-latency}

このドキュメントでは、読み取りと書き込みの遅延とジッターの考えられる原因と、これらの問題のトラブルシューティング方法を紹介します。

## 一般的な原因 {#common-causes}

### 不正なTiDB実行プラン {#incorrect-tidb-execution-plan}

クエリの実行プランは不安定であり、誤ったインデックスを選択する可能性があります。これにより、待ち時間が長くなります。

#### 現象 {#phenomenon}

-   クエリ実行プランがスローログに出力されている場合は、プランを直接表示できます。 `select tidb_decode_plan('xxx...')`ステートメントを実行して、詳細な実行プランを解析します。
-   モニターでスキャンされたキーの数が異常に増加します。遅いログでは、 `Scan Keys`の数が多いです。
-   TiDBのSQL実行時間は、MySQLなどの他のデータベースの実行時間とは大きく異なります。他のデータベースの実行プランを比較できます（たとえば、 `Join Order`が異なるかどうか）。

#### 考えられる理由 {#possible-reason}

統計は不正確です。

#### トラブルシューティング方法 {#troubleshooting-methods}

-   統計情報を更新する
    -   統計を正確に保つために、 `analyze table`を手動で実行し、 `crontab`コマンドを使用して`analyze`を定期的に実行します。
    -   `auto analyze`を自動的に実行します。しきい値を`analyze ratio`に下げ、情報収集の頻度を増やし、実行の開始時刻と終了時刻を設定します。次の例を参照してください。
        -   `set global tidb_auto_analyze_ratio=0.2;`
        -   `set global tidb_auto_analyze_start_time='00:00 +0800';`
        -   `set global tidb_auto_analyze_end_time='06:00 +0800';`
-   実行プランをバインドする
    -   アプリケーションのSQLステートメントを変更し、 `use index`を実行して、列のインデックスを一貫して使用します。
    -   3.0バージョンでは、アプリケーションのSQLステートメントを変更する必要はありません。 `create global binding`を使用して、 `force index`のバインディングSQLステートメントを作成します。
    -   4.0バージョンでは、 [SQL計画管理](/sql-plan-management.md)がサポートされており、不安定な実行計画によって引き起こされるパフォーマンスの低下を回避します。

### PDの異常 {#pd-anomalies}

#### 現象 {#phenomenon}

PDTSOの`wait duration`メトリックの異常な増加があります。このメトリックは、PDが要求を返すのを待機する時間を表します。

#### 考えられる理由 {#possible-reasons}

-   ディスクの問題。 PDノードが配置されているディスクには、完全なI/O負荷があります。 PDが、I/Oの需要が高くディスクの状態が高い他のコンポーネントとともに展開されているかどうかを調査します。 **Grafana-** &gt;<strong>ディスクパフォーマンス</strong>-&gt;<strong>レイテンシ</strong>/<strong>ロード</strong>でモニターメトリックを表示することで、原因を確認できます。必要に応じて、FIOツールを使用してディスクのチェックを実行することもできます。

-   PDピア間のネットワークの問題。 PDログには`lost the TCP streaming connection`が表示されます。 PDノード間のネットワークに問題があるかどうかを確認し、モニター**Grafana-** &gt; <strong>PD-</strong> &gt; <strong>etcd</strong>で`round trip`を表示して、原因を確認する必要があります。

-   サーバーの負荷が高い。ログには`server is likely overloaded`が表示されます。

-   PDはリーダーを選出できません：PDログには`lease is not expired`が表示されます。 [この問題](https://github.com/etcd-io/etcd/issues/10355)はv3.0.xおよびv2.1.19で修正されています。

-   リーダー選挙は遅いです。リージョンの読み込み時間が長いです。この問題は、PDログで`grep "regions cost"`を実行することで確認できます。結果が`load 460927 regions cost 11.77099s`秒などの秒単位の場合は、リージョンの読み込みが遅いことを意味します。 `use-region-storage`を`true`に設定すると、v3.0で`region storage`機能を有効にできます。これにより、リージョンの読み込み時間が大幅に短縮されます。

-   TiDBとPD間のネットワークの問題。モニター**Grafana-** &gt; <strong>blackbox_exporter-</strong> &gt; <strong>pingレイテンシー</strong>にアクセスして、TiDBからPDリーダーへのネットワークが正常に実行されているかどうかを確認します。

-   PDは`FATAL`のエラーを報告し、ログには`range failed to find revision pair`が表示されます。この問題はv3.0.8（ [＃2040](https://github.com/pingcap/pd/pull/2040) ）で修正されています。

-   `/api/v1/regions`のインターフェイスを使用する場合、リージョンが多すぎるとPDOOMが発生する可能性があります。この問題はv3.0.8（ [＃1986](https://github.com/pingcap/pd/pull/1986) ）で修正されています。

-   ローリングアップグレード中のPDOOM。 gRPCメッセージのサイズは制限されておらず、モニターは`TCP InSegs`が比較的大きいことを示しています。この問題はv3.0.6（ [＃1952](https://github.com/pingcap/pd/pull/1952) ）で修正されています。

-   PDはパニックになります。 [バグを報告](https://github.com/tikv/pd/issues/new?labels=kind/bug&#x26;template=bug-report.md) 。

-   その他の原因。 `curl http://127.0.0.1:2379/debug/pprof/goroutine?debug=2`と[バグを報告](https://github.com/pingcap/pd/issues/new?labels=kind%2Fbug&#x26;template=bug-report.md)を実行してゴルーチンを取得します。

### TiKVの異常 {#tikv-anomalies}

#### 現象 {#phenomenon}

モニターの`KV Cmd Duration`メトリックが異常に増加します。このメトリックは、TiDBがTiKVに要求を送信してからTiDBが応答を受信するまでの時間を表します。

#### 考えられる理由 {#possible-reasons}

-   `gRPC duration`のメトリックを確認してください。このメトリックは、TiKVでのgRPCリクエストの合計期間を表します。 `gRPC duration`のTiKVと`KV duration`つのTiDBを比較することで、潜在的なネットワークの問題を見つけることができます。たとえば、gRPC期間は短いが、TiDBのKV期間は長いため、TiDBとTiKVの間のネットワーク遅延が高いか、TiDBとTiKVの間のNIC帯域幅が完全に占有されている可能性があります。

-   TiKVが再開されたため、再選。
    -   TiKVがパニックになった後、 `systemd`だけ引き上げられ、正常に動作します。 TiKVログを表示することで、パニックが発生したかどうかを確認できます。この問題は予期しないものであるため、発生した場合は[バグを報告](https://github.com/tikv/tikv/issues/new?template=bug-report.md)です。
    -   TiKVは、サードパーティによって停止または強制終了された後、 `systemd`によってプルアップされます。 `dmesg`とTiKVログを表示して原因を確認してください。
    -   TiKVはOOMであり、再起動します。
    -   `THP` （Transparent Hugepage）を動的に調整するため、TiKVがハングします。

-   モニターを確認してください：TiKV RocksDBで書き込みストールが発生したため、再選されました。モニターの**Grafana-** &gt; <strong>TiKV-details-</strong> &gt;<strong>エラー</strong>が`server is busy`を示しているかどうかを確認できます。

-   ネットワークの分離による再選。

-   `block-cache`の構成が大きすぎると、TiKVOOMが発生する可能性があります。問題の原因を確認するには、モニター**Grafana-** &gt; <strong>TiKV-details</strong>で対応するインスタンスを選択して、RocksDBの`block cache size`を確認します。その間、 `[storage.block-cache] capacity = # "1GB"`パラメータが正しく設定されているか確認してください。デフォルトでは、TiKVの`block-cache`はマシンの合計メモリの`45%`に設定されています。 TiKVは物理マシンのメモリを取得するため、コンテナにTiKVをデプロイするときに、このパラメータを明示的に指定する必要があります。これは、コンテナのメモリ制限を超える可能性があります。

-   コプロセッサーは多くの大きなクエリを受け取り、大量のデータを返します。 gRPCは、コプロセッサーがデータを返すのと同じ速さでデータを送信できず、その結果、OOMになります。原因を確認するには、モニターの**Grafana-** &gt; <strong>TiKV-details-</strong> &gt;<strong>コプロセッサーの概要</strong>を表示して、 `response size`が`network outbound`トラフィックを超えているかどうかを確認できます。

### 単一のTiKVスレッドのボトルネック {#bottleneck-of-a-single-tikv-thread}

TiKVには、ボトルネックになる可能性のあるシングルスレッドがいくつかあります。

-   TiKVインスタンスのリージョンが多すぎると、単一のgRPCスレッドがボトルネックになります（Grafana-&gt; **TiKV** <strong>-details-</strong> &gt; <strong>Thread CPU / gRPC CPU Per Thread</strong>メトリックを確認してください）。 v3.x以降のバージョンでは、 `Hibernate Region`を有効にして問題を解決できます。
-   v3.0より前のバージョンでは、raftstoreスレッドまたはapplyスレッドがボトルネックになった場合（ **Grafana-** &gt; <strong>TiKV-details-</strong> &gt; <strong>Thread CPU / raft</strong> storeCPUおよび<strong>AsyncapplyCPU</strong>メトリックが`80%`を超える場合）、TiKV（v2 .x）インスタンスまたはマルチスレッドを使用したv3.xへのアップグレード。

### CPU負荷が増加します {#cpu-load-increases}

#### 現象 {#phenomenon}

CPUリソースの使用がボトルネックになります。

#### 考えられる理由 {#possible-reasons}

-   ホットスポットの問題
-   全体的な負荷が高い。 TiDBの遅いクエリと高価なクエリを確認してください。インデックスを追加するか、クエリをバッチで実行することにより、実行中のクエリを最適化します。別の解決策は、クラスタをスケールアウトすることです。

## その他の原因 {#other-causes}

### クラスターのメンテナンス {#cluster-maintenance}

各オンラインクラスタのほとんどには、3つまたは5つのノードがあります。保守対象のマシンにPDコンポーネントがある場合は、ノードがリーダーであるかフォロワーであるかを判別する必要があります。フォロワーを無効にしても、クラスタの動作には影響しません。リーダーを無効にする前に、リーダーシップを切り替える必要があります。リーダーシップの変更中に、約3秒のパフォーマンスジッターが発生します。

### 少数のレプリカがオフラインです {#minority-of-replicas-are-offline}

デフォルトでは、各TiDBクラスタには3つのレプリカがあるため、各リージョンにはクラスタに3つのレプリカがあります。これらのリージョンはリーダーを選出し、Raftプロトコルを介してデータを複製します。 Raftプロトコルは、ノード（レプリカの半分未満）に障害が発生したり、分離されたりした場合でも、TiDBがデータを失うことなくサービスを提供できることを保証します。 3つのレプリカを持つクラスタの場合、1つのノードに障害が発生するとパフォーマンスのジッターが発生する可能性がありますが、理論上の使いやすさと正確性には影響しません。

### 新しいインデックス {#new-indexes}

TiDBがテーブルをスキャンしてインデックスを埋め戻す場合、インデックスの作成は大量のリソースを消費します。インデックスの作成は、頻繁に更新されるフィールドと競合することもあり、アプリケーションに影響します。大きなテーブルでのインデックスの作成には時間がかかることが多いため、インデックスの作成時間とクラスタのパフォーマンスのバランスをとる必要があります（たとえば、オフピーク時にインデックスを作成する）。

**パラメータ調整：**

現在、 `tidb_ddl_reorg_worker_cnt`と`tidb_ddl_reorg_batch_size`を使用して、インデックス作成の速度を動的に調整できます。通常、値が小さいほど、システムへの影響は小さくなりますが、実行時間は長くなります。

通常、最初にデフォルト値（ `4`と`256` ）を維持し、クラスタのリソース使用量と応答速度を観察してから、値`tidb_ddl_reorg_worker_cnt`を増やして同時実行性を高めることができます。モニターに明らかなジッターが見られない場合は、 `tidb_ddl_reorg_batch_size`の値を増やします。インデックスの作成に関係する列が頻繁に更新される場合、結果として生じる多くの競合により、インデックスの作成が失敗し、再試行されます。

さらに、 `tidb_ddl_reorg_priority`の`PRIORITY_HIGH`を設定して、インデックスの作成に優先順位を付け、プロセスを高速化することもできます。ただし、一般的なOLTPシステムでは、デフォルト値を維持することをお勧めします。

### 高いGC圧力 {#high-gc-pressure}

TiDBのトランザクションは、マルチバージョン同時実行制御（MVCC）メカニズムを採用しています。新しく書き込まれたデータが古いデータを上書きする場合、古いデータは置き換えられず、両方のバージョンのデータが保存されます。タイムスタンプは、さまざまなバージョンをマークするために使用されます。 GCのタスクは、廃止されたデータをクリアすることです。

-   ロックの解決のフェーズでは、TiKVで大量の`scan_lock`リクエストが作成されます。これは、gRPC関連のメトリックで確認できます。これらの`scan_lock`のリクエストは、すべてのリージョンを呼び出します。
-   範囲の削除のフェーズでは、いくつかの（またはまったく） `unsafe_destroy_range`のリクエストがTiKVに送信されます。これは、gRPC関連のメトリックと**GCタスク**パネルで確認できます。
-   Do GCのフェーズでは、各TiKVはデフォルトでマシン上のリーダー領域をスキャンし、各リーダーに対してGCを実行します。これは、 **GCタスク**パネルで確認できます。
