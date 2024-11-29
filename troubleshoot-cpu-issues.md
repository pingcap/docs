---
title: Troubleshoot Increased Read and Write Latency
summary: 読み取りおよび書き込みのレイテンシーが長くなる問題のトラブルシューティング方法を学びます。
---

# 読み取りおよび書き込み遅延の増加のトラブルシューティング {#troubleshoot-increased-read-and-write-latency}

このドキュメントでは、読み取りおよび書き込みのレイテンシーとジッターの考えられる原因と、これらの問題のトラブルシューティング方法について説明します。

## 一般的な原因 {#common-causes}

### TiDB 実行プランが正しくありません {#incorrect-tidb-execution-plan}

クエリの実行プランが不安定になり、間違ったインデックスが選択され、レイテンシーが増加する可能性があります。

#### 現象 {#phenomenon}

-   スローログにクエリ実行プランが出力されている場合は、プランを直接参照できます。 `select tidb_decode_plan('xxx...')`ステートメントを実行して、詳細な実行プランを解析します。
-   モニター内のスキャンされたキーの数が異常に増加し、スローログでは`Scan Keys`の数が多くなります。
-   TiDB における SQL 実行時間は、MySQL などの他のデータベースと比較して大きく異なります。他のデータベースの実行プランと比較することができます (たとえば、 `Join Order`が異なるかどうか)。

#### 考えられる理由 {#possible-reason}

統計は不正確です。

#### トラブルシューティング方法 {#troubleshooting-methods}

-   統計情報を更新する
    -   統計を正確に保つために、 `analyze table`手動で実行し、 `crontab`コマンドを使用して`analyze`定期的に実行します。
    -   `auto analyze`自動的に実行します。 `analyze ratio`のしきい値を下げ、情報収集の頻度を増やし、実行の開始時間と終了時間を設定します。次の例を参照してください。
        -   `set global tidb_auto_analyze_ratio=0.2;`
        -   `set global tidb_auto_analyze_start_time='00:00 +0800';`
        -   `set global tidb_auto_analyze_end_time='06:00 +0800';`
-   実行計画をバインドする
    -   アプリケーションの SQL ステートメントを変更し、 `use index`実行して、列のインデックスを一貫して使用します。
    -   3.0 バージョンでは、アプリケーション SQL ステートメントを変更する必要はありません。 `create global binding`使用して、 `force index`のバインディング SQL ステートメントを作成します。
    -   4.0 バージョンでは[SQL プラン管理](/sql-plan-management.md)がサポートされており、不安定な実行プランによるパフォーマンスの低下を回避します。

### PD異常 {#pd-anomalies}

#### 現象 {#phenomenon}

PD TSO の`wait duration`メトリックが異常に増加しています。このメトリックは、PD がリクエストを返すのを待機する期間を表します。

#### 考えられる理由 {#possible-reasons}

-   ディスクの問題。PD ノードが配置されているディスクには、完全な I/O 負荷があります。PD が、I/O 需要の高い他のコンポーネントと一緒にデプロイされているかどうか、およびディスクの状態を調査します。原因は、 **Grafana** -&gt;**ディスク パフォーマンス**-&gt;**レイテンシー**/**負荷**のモニター メトリックを表示することで確認できます。必要に応じて、FIO ツールを使用してディスクのチェックを実行することもできます。

-   PD ピア間のネットワークの問題。PD ログには`lost the TCP streaming connection`表示されます。PD ノード間のネットワークに問題があるかどうかを確認し、モニター**Grafana** -&gt; **PD** -&gt; **etcd**で`round trip`表示して原因を確認する必要があります。

-   サーバーの負荷が高いです。ログには`server is likely overloaded`表示されています。

-   PD がLeaderを選出できない: PD ログには`lease is not expired`と表示されます。3 [この号](https://github.com/etcd-io/etcd/issues/10355) v3.0.x および v2.1.19 で修正されました。

-   リーダー選出が遅い。リージョンの読み込み時間が長い。この問題は、PD ログで`grep "regions cost"`実行することで確認できます。結果が`load 460927 regions cost 11.77099s`などの秒単位の場合は、リージョンの読み込みが遅いことを意味します。v3.0 で`use-region-storage`を`true`に設定することで`region storage`機能を有効にでき、リージョンの読み込み時間が大幅に短縮されます。

-   TiDB と PD 間のネットワークの問題。モニター**Grafana** -&gt; **blackbox_exporter** -&gt; **pingレイテンシー**にアクセスして、TiDB から PDLeaderへのネットワークが正常に動作しているかどうかを確認します。

-   PDは`FATAL`エラーを報告し、ログには`range failed to find revision pair`表示されます。この問題はv3.0.8（ [＃2040](https://github.com/pingcap/pd/pull/2040) ）で修正されました。

-   `/api/v1/regions`インターフェースを使用すると、リージョンが多すぎると PD OOM が発生する可能性があります。この問題は v3.0.8 ( [＃1986](https://github.com/pingcap/pd/pull/1986) ) で修正されました。

-   ローリングアップグレード中のPD OOM。gRPCメッセージのサイズは制限されておらず、モニターでは`TCP InSegs`が比較的大きいことが示されています。この問題はv3.0.6（ [＃1952](https://github.com/pingcap/pd/pull/1952) ）で修正されました。

-   PDはパニックに陥る[バグを報告する](https://github.com/tikv/pd/issues/new?labels=kind/bug&#x26;template=bug-report.md) .

-   その他の原因。1 と[バグを報告する](https://github.com/pingcap/pd/issues/new?labels=kind%2Fbug&#x26;template=bug-report.md) `curl http://127.0.0.1:2379/debug/pprof/goroutine?debug=2`して goroutine を取得します。

### TiKVの異常 {#tikv-anomalies}

#### 現象 {#phenomenon}

モニターの`KV Cmd Duration`メトリックが異常に増加しています。このメトリックは、TiDB が TiKV に要求を送信してから TiDB が応答を受信するまでの期間を表します。

#### 考えられる理由 {#possible-reasons}

-   `gRPC duration`メトリックを確認します。このメトリックは、TiKV での gRPC 要求の合計期間を表します。TiKV の`gRPC duration`と TiDB の`KV duration`比較することで、潜在的なネットワークの問題を見つけることができます。たとえば、gRPC 期間は短いですが、TiDB の KV 期間は長い場合、TiDB と TiKV 間のネットワークレイテンシーが高いか、TiDB と TiKV 間の NIC 帯域幅が完全に占有されている可能性があります。

-   TiKVが再開されたため再選。
    -   TiKV がパニックした後、 `systemd`に引き上げられ、正常に動作します。panicが発生したかどうかは、TiKV ログを表示することで確認できます。この問題は予期しないものなので、発生する場合は[バグを報告する](https://github.com/tikv/tikv/issues/new?template=bug-report.md) 。
    -   TiKV は第三者によって停止または強制終了され、その後`systemd`によってプルアップされます。3 と TiKV ログ`dmesg`表示して原因を確認します。
    -   TiKV は OOM であり、再起動を引き起こします。
    -   `THP` (Transparent Hugepage) を動的に調整するため、TiKV がハングします。

-   モニターを確認してください: TiKV RocksDB は書き込み停止に遭遇し、その結果再選出が行われます。モニター**Grafana** -&gt; **TiKV-details** -&gt; **errors**に`server is busy`表示されているかどうかを確認できます。

-   ネットワーク分離のため再選。

-   `block-cache`設定が大きすぎると、TiKV OOM が発生する可能性があります。問題の原因を確認するには、モニター**Grafana** -&gt; **TiKV-details**で対応するインスタンスを選択して、RocksDB の`block cache size`確認します。同時に、 `[storage.block-cache] capacity = # "1GB"`パラメータが適切に設定されているかどうかを確認します。デフォルトでは、TiKV の`block-cache`マシンの合計メモリの`45%`に設定されています。コンテナに TiKV をデプロイするときにこのパラメータを明示的に指定する必要があります。TiKV は物理マシンのメモリを取得するため、コンテナのメモリ制限を超える可能性があるためです。

-   コプロセッサーは大量の大きなクエリを受信し、大量のデータを返します。コプロセッサがデータを返すのと同じ速さで gRPC がデータを送信できず、OOM が発生します。原因を確認するには、モニター**Grafana** -&gt; **TiKV-details** -&gt; **coprocessor summary**を表示して、 `response size` `network outbound`トラフィックを超えているかどうかを確認できます。

### 単一の TiKV スレッドのボトルネック {#bottleneck-of-a-single-tikv-thread}

TiKV にはボトルネックになる可能性のある単一スレッドがいくつかあります。

-   TiKV インスタンス内のリージョンが多すぎると、単一の gRPC スレッドがボトルネックになります ( **Grafana** -&gt; **TiKV 詳細**-&gt;**スレッド CPU/gRPC CPU スレッドあたりの**メトリックを確認してください)。v3.x 以降のバージョンでは、 `Hibernate Region`有効にするとこの問題を解決できます。
-   v3.0 より前のバージョンでは、raftstore スレッドまたは適用スレッドがボトルネックになった場合 ( **Grafana** -&gt; **TiKV-details** -&gt; **Thread CPU/raft store CPU**および**Async apply CPU**メトリックが`80%`を超える)、TiKV (v2.x) インスタンスをスケールアウトするか、マルチスレッドで v3.x にアップグレードできます。

### CPU負荷が増加する {#cpu-load-increases}

#### 現象 {#phenomenon}

CPU リソースの使用がボトルネックになります。

#### 考えられる理由 {#possible-reasons}

-   ホットスポットの問題
-   全体的な負荷が高い。TiDB の遅いクエリと高価なクエリを確認します。インデックスを追加するか、クエリをバッチで実行して、実行中のクエリを最適化します。別の解決策は、クラスターをスケールアウトすることです。

## その他の原因 {#other-causes}

### クラスタのメンテナンス {#cluster-maintenance}

各オンライン クラスターのほとんどは、3 つまたは 5 つのノードで構成されています。メンテナンス対象のマシンに PDコンポーネントがある場合は、ノードがリーダーかフォロワーかを判断する必要があります。フォロワーを無効にしても、クラスターの動作には影響しません。リーダーを無効にする前に、リーダーシップを切り替える必要があります。リーダーシップの変更中は、約 3 秒のパフォーマンス ジッターが発生します。

### レプリカの少数はオフラインです {#minority-of-replicas-are-offline}

デフォルトでは、各 TiDB クラスターには 3 つのレプリカがあるため、各リージョンにはクラスター内に 3 つのレプリカがあります。これらのリージョンはリーダーを選出し、 Raftプロトコルを介してデータを複製します。Raft プロトコルにより、ノード (レプリカの半分未満) に障害が発生したり、孤立したりした場合でも、TiDB はデータ損失なしでサービスを提供できます。3 つのレプリカを持つクラスターの場合、1 つのノードに障害が発生するとパフォーマンスのジッターが発生する可能性がありますが、理論上の使いやすさと正確性には影響しません。

### 新しいインデックス {#new-indexes}

インデックスを作成すると、TiDB がテーブルをスキャンしてインデックスをバックフィルするときに大量のリソースが消費されます。インデックスの作成は、頻繁に更新されるフィールドと競合する可能性があり、アプリケーションに影響を及ぼします。大きなテーブルにインデックスを作成すると時間がかかることが多いため、インデックスの作成時間とクラスターのパフォーマンスのバランスを取る必要があります (たとえば、オフピーク時にインデックスを作成します)。

**パラメータ調整:**

現在、 `tidb_ddl_reorg_worker_cnt`と`tidb_ddl_reorg_batch_size`使用して、インデックス作成の速度を動的に調整できます。通常、値が小さいほど、システムへの影響は小さくなりますが、実行時間は長くなります。

一般的には、まずデフォルト値 ( `4`と`256` ) をそのままにして、クラスターのリソース使用量と応答速度を観察し、次に`tidb_ddl_reorg_worker_cnt`の値を増やして同時実行性を高めます。モニターで明らかなジッターが見られない場合は、 `tidb_ddl_reorg_batch_size`の値を増やします。インデックス作成に関係する列が頻繁に更新される場合、結果として生じる多くの競合により、インデックス作成が失敗し、再試行されることになります。

また、インデックス作成を優先し、処理を高速化するために、 `tidb_ddl_reorg_priority` ～ `PRIORITY_HIGH`の値を設定することもできます。ただし、一般的な OLTP システムでは、デフォルト値を維持することをお勧めします。

### 高いGC圧力 {#high-gc-pressure}

TiDB のトランザクションは、マルチバージョン同時実行制御 (MVCC) メカニズムを採用しています。新しく書き込まれたデータが古いデータを上書きする場合、古いデータは置き換えられず、両方のバージョンのデータが保存されます。タイムスタンプは、異なるバージョンをマークするために使用されます。GC のタスクは、古いデータをクリアすることです。

-   ロック解決のフェーズでは、TiKV に大量の`scan_lock`リクエストが作成され、gRPC 関連のメトリックで確認できます。これらの`scan_lock`リクエストは、すべてのリージョンを呼び出します。
-   範囲削除のフェーズでは、TiKV に少数の (またはまったくない`unsafe_destroy_range`リクエストが送信され、gRPC 関連のメトリックと**GC タスク**パネルで確認できます。
-   Do GC フェーズでは、各 TiKV はデフォルトでマシン上のリーダー領域をスキャンし、各リーダーに対して GC を実行します。これは、 **GC タスク**パネルで確認できます。
