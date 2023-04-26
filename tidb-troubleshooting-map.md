---
title: TiDB Troubleshooting Map
summary: Learn how to troubleshoot common errors in TiDB.
---

# TiDB トラブルシューティング マップ {#tidb-troubleshooting-map}

このドキュメントでは、TiDB およびその他のコンポーネントの一般的な問題をまとめています。このマップを使用して、関連する問題が発生したときに問題を診断して解決できます。

## 1. サービス利用不可 {#1-service-unavailable}

### 1.1 クライアントが<code>Region is Unavailable</code>エラーを報告する {#1-1-the-client-reports-code-region-is-unavailable-code-error}

-   1.1.1 通常、 `Region is Unavailable`エラーは、リージョンが一定期間利用できないために発生します。 `TiKV server is busy`発生するか、 `not leader`または`epoch not match`が原因で TiKV へのリクエストが失敗するか、TiKV へのリクエストがタイムアウトする可能性があります。このような場合、TiDB は`backoff`の再試行メカニズムを実行します。 `backoff`しきい値 (デフォルトでは 20 秒) を超えると、クライアントにエラーが送信されます。 `backoff`しきい値内では、このエラーはクライアントには表示されません。

-   1.1.2 複数の TiKV インスタンスが同時に OOM であるため、OOM 期間中にLeaderが発生しません。中国語で[ケース-991](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case991.md)を参照してください。

-   1.1.3 TiKV は`TiKV server is busy`報告し、 `backoff`時間を超えます。詳細については、 [4.3](#43-the-client-reports-the-server-is-busy-error)を参照してください。 `TiKV server is busy`は内部フロー制御メカニズムの結果であり、 `backoff`時間にカウントされるべきではありません。この問題は修正される予定です。

-   1.1.4 複数の TiKV インスタンスの開始に失敗したため、リージョンにLeaderがありません。複数の TiKV インスタンスが物理マシンにデプロイされている場合、ラベルが適切に構成されていないと、物理マシンの障害によってリージョンにLeaderが存在しなくなる可能性があります。中国語で[ケース-228](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case228.md)を参照してください。

-   1.1.5Followerの適用が前のエポックで遅れている場合、FollowerがLeaderになった後、 `epoch not match`でリクエストを拒否します。中国語の[ケース-958](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case958.md)参照してください (TiKV はそのメカニズムを最適化する必要があります)。

### 1.2 PD エラーによりサービスが利用できなくなる {#1-2-pd-errors-cause-service-unavailable}

[5 PDの問題](#5-pd-issues)を参照してください。

## 2. レイテンシが大幅に増加 {#2-latency-increases-significantly}

### 2.1 一時的な増加 {#2-1-transient-increase}

-   2.1.1 間違った TiDB 実行計画により、レイテンシーが増加します。 [3.3](#33-wrong-execution-plan)を参照してください。
-   2.1.2 PDLeader選挙の問題または OOM。 [5.2](#52-pd-election)と[5.3](#53-pd-oom)を参照してください。
-   2.1.3 一部の TiKV インスタンスで多数のLeaderドロップが発生する。 [4.4](#44-some-tikv-nodes-drop-leader-frequently)を参照してください。
-   2.1.4 その他の原因については、 [増加した読み取りおよび書き込み遅延のトラブルシューティング](/troubleshoot-cpu-issues.md)を参照してください。

### 2.2 持続的かつ大幅な増加 {#2-2-persistent-and-significant-increase}

-   2.2.1 TiKV シングルスレッドのボトルネック

    -   TiKV インスタンス内のリージョンが多すぎると、単一の gRPC スレッドがボトルネックになります ( **Grafana** -&gt; <strong>TiKV-details</strong> -&gt; <strong>Thread CPU/gRPC CPU Per Thread</strong>メトリックを確認してください)。 v3.x 以降のバージョンでは、 `Hibernate Region`有効にして問題を解決できます。中国語で[ケース-612](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case612.md)参照してください。

    -   v3.0 より前のバージョンでは、raftstore スレッドまたは適用スレッドがボトルネックになる場合 ( **Grafana** -&gt; <strong>TiKV-details</strong> -&gt; <strong>Thread CPU/raft store CPU</strong>および<strong>Async apply CPU</strong>メトリクスが`80%`を超える)、TiKV (v2 .x) インスタンスまたはマルチスレッドで v3.x にアップグレードします。 <!-- See [case-517](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case517.md) in Chinese. -->

-   2.2.2 CPU 負荷が増加します。

-   2.2.3 TiKV 書き込みが遅い。 [4.5](#45-tikv-write-is-slow)を参照してください。

-   2.2.4 TiDB の間違った実行計画。 [3.3](#33-wrong-execution-plan)を参照してください。

-   2.2.5 その他の原因については、 [増加した読み取りおよび書き込み遅延のトラブルシューティング](/troubleshoot-cpu-issues.md)を参照してください。

## 3. TiDB の問題 {#3-tidb-issues}

### 3.1 DDL {#3-1-ddl}

-   3.1.1 `decimal`フィールドの長さを変更すると、エラー`ERROR 1105 (HY000): unsupported modify decimal column precision`が報告されます。 <!--See [case-1004](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case517.md) in Chinese.--> TiDB は`decimal`フィールドの長さの変更をサポートしていません。

-   3.1.2 TiDB DDL ジョブがハングするか実行が遅い ( `admin show ddl jobs`を使用して DDL の進行状況を確認する)

    -   原因 1: 他のコンポーネント (PD/TiKV) とのネットワークの問題。

    -   原因 2: TiDB の初期バージョン (v3.0.8 より前) は、同時実行性が高いゴルーチンが多いため、内部負荷が高くなっています。

    -   原因 3: 初期のバージョン (v2.1.15 &amp; バージョン &lt; v3.0.0-rc1) では、PD インスタンスが TiDB キーの削除に失敗し、DDL のすべての変更が 2 つのリースを待機する原因になります。

    -   その他の不明な原因については、 [バグを報告](https://github.com/pingcap/tidb/issues/new?labels=type%2Fbug&#x26;template=bug-report.md) .

    -   解決：

        -   原因 1 については、TiDB と TiKV/PD 間のネットワーク接続を確認してください。
        -   原因 2 と 3 については、問題は新しいバージョンで既に修正されています。 TiDB を新しいバージョンにアップグレードできます。
        -   その他の原因については、DDL 所有者を移行する次の解決策を使用できます。

    -   DDL 所有者の移行:

        -   TiDBサーバーに接続できる場合は、所有者選出コマンドを`curl -X POST http://{TiDBIP}:10080/ddl/owner/resign`実行します。
        -   TiDBサーバーに接続できない場合は、 `tidb-ctl`を使用して PD クラスターの etcd から DDL 所有者を削除し、再選択をトリガーします: `tidb-ctl etcd delowner [LeaseID] [flags] + ownerKey`

-   3.1.3 TiDB がログに`information schema is changed`エラーを報告する

    -   詳細な原因と解決策については、 [`Information schema is changed`理由エラーが報告される](/faq/sql-faq.md#what-triggers-the-information-schema-is-changed-error)を参照してください。

    -   背景: 増加した`schema version`の数は、各 DDL 変更操作の`schema state`の数と一致しています。たとえば、 `create table`操作には 1 つのバージョン変更があり、 `add column`操作には 4 つのバージョン変更があります。したがって、列の変更操作が多すぎると、 `schema version`が急速に増加する可能性があります。詳細は[オンラインスキーマ変更](https://static.googleusercontent.com/media/research.google.com/zh-CN//pubs/archive/41376.pdf)を参照してください。

-   3.1.4 TiDB がログに`information schema is out of date`報告する

    -   原因 1: DML ステートメントを実行している TiDBサーバーが`graceful kill`で停止され、終了の準備をしています。 DML ステートメントを含むトランザクションの実行時間が 1 DDL リースを超えています。トランザクションがコミットされると、エラーが報告されます。

    -   原因 2: DML ステートメントの実行中に、TiDBサーバーがPD または TiKV に接続できません。その結果、TiDBサーバーは1 つの DDL リース (デフォルトでは`45s` ) 内で新しいスキーマをロードしなかったか、TiDBサーバーは`keep alive`設定で PD から切断されました。

    -   原因 3: TiKV の負荷が高いか、ネットワークがタイムアウトになっています。 **Grafana** -&gt; <strong>TiDB</strong>および<strong>TiKV</strong>でノードの負荷を確認します。

    -   解決：

        -   原因 1 の場合は、TiDB の開始時に DML 操作を再試行してください。
        -   原因 2 については、TiDBサーバーと PD/TiKV 間のネットワークを確認してください。
        -   原因 3 については、TiKV がビジーである理由を調査します。 [4 TiKVの問題](#4-tikv-issues)を参照してください。

### 3.2 OOM の問題 {#3-2-oom-issues}

-   3.2.1 症状

    -   クライアント: クライアントはエラー`ERROR 2013 (HY000): Lost connection to MySQL server during query`を報告します。

    -   ログを確認する

        -   `dmesg -T | grep tidb-server`を実行します。結果には、エラーが発生した時点の OOM-killer ログが表示されます。

        -   エラーが発生した前後の時点 (つまり、tidb-server が再起動した時点) で、「TiDB へようこそ」ログ`tidb.log` grep します。

        -   `fatal error: runtime: out of memory`または`cannot allocate memory` in `tidb_stderr.log`を grep します。

        -   v2.1.8 以前のバージョンでは、 `tidb_stderr.log`の`fatal error: stack overflow`を grep できます。

    -   監視: tidb-server インスタンスのメモリ使用量が短期間で急激に増加します。

-   3.2.2 OOM の原因となっている SQL ステートメントを見つけます。 (現在、TiDB のすべてのバージョンで SQL を正確に特定することはできません。OOM が SQL ステートメントを特定した後に原因であるかどうかを分析する必要があります。)

    -   バージョン &gt;= v3.0.0 の場合、 grep &quot;expensive_query&quot; in `tidb.log` .このログ メッセージには、タイムアウトしたかメモリクォータを超えた SQL クエリが記録されます。

    -   v3.0.0 より前のバージョンの場合、 `tidb.log`で grep &quot;メモリ exceeded quota&quot; を実行して、メモリクォータを超えている SQL クエリを見つけます。

    > **ノート：**
    >
    > 単一の SQLメモリ使用量のデフォルトのしきい値は`1GB`です。このパラメータは、システム変数[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)を構成することで設定できます。

-   3.2.3 OOM の問題を軽減する

    -   `SWAP`を有効にすることで、大規模なクエリによるメモリの過剰使用によって引き起こされる OOM の問題を軽減できます。メモリが不足している場合、この方法は I/O オーバーヘッドのために大規模なクエリのパフォーマンスに影響を与える可能性があります。パフォーマンスへの影響の程度は、残りのメモリ容量とディスク I/O 速度によって異なります。

-   3.2.4 OOM の典型的な理由

    -   SQL クエリには`join`があります。 `explain`使用して SQL ステートメントを表示すると、 `join`操作で`HashJoin`アルゴリズムが選択され、 `inner`テーブルが大きいことがわかります。

    -   単一の`UPDATE/DELETE`クエリのデータ量が大きすぎます。中国語で[ケース-882](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case882.md)参照してください。

    -   SQL には、 `Union`で接続された複数のサブクエリが含まれています。中国語で[ケース-1828](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case1828.md)参照してください。

OOM のトラブルシューティングの詳細については、 [TiDB OOM の問題のトラブルシューティング](/troubleshoot-tidb-oom.md)を参照してください。

### 3.3 間違った実行計画 {#3-3-wrong-execution-plan}

-   3.3.1 症状

    -   SQL クエリの実行時間が以前の実行に比べて大幅に長くなった、または実行計画が突然変更された。実行計画がスロー ログに記録されている場合は、実行計画を直接比較できます。

    -   SQL クエリの実行時間は、MySQL などの他のデータベースに比べてはるかに長くなります。実行計画を他のデータベースと比較して、 `Join Order`などの違いを確認します。

    -   スローログでは、SQL実行回数`Scan Keys`が多い。

-   3.3.2 実行計画の調査

    -   `explain analyze {SQL}` .実行時間が許容できる場合は、 `explain analyze`の結果の`count`と`execution info`の`row`の数を比較します。 `TableScan/IndexScan`行目に大きな差が見られる場合は、統計が正しくない可能性があります。他の行で大きな違いが見つかった場合、問題は統計にない可能性があります。

    -   `select count(*)` .実行計画に`join`操作が含まれている場合、 `explain analyze`は時間がかかる場合があります。統計に問題があるかどうかは、 `TableScan/IndexScan`の条件に対して`select count(*)`実行し、 `explain`結果の`row count`情報を比較することで確認できます。

-   3.3.3 緩和

    -   v3.0 以降のバージョンでは、 `SQL Bind`機能を使用して実行プランをバインドします。

    -   統計を更新します。問題の原因が統計にあるとほぼ確信している場合は、 [統計をダンプする](/statistics.md#export-statistics) .原因が、 `show stats_meta`分の`modify count/row count`特定の値 (0.3 など) より大きいなどの古い統計である場合、またはテーブルに時間列のインデックスがある場合は、 `analyze table`使用して回復を試みることができます。 `auto analyze`が設定されている場合は、システム変数`tidb_auto_analyze_ratio`が大きすぎるかどうか (たとえば、0.3 より大きいかどうか)、および現在の時刻が`tidb_auto_analyze_start_time`から`tidb_auto_analyze_end_time`の間にあるかどうかを確認します。

    -   その他の状況については、 [バグを報告](https://github.com/pingcap/tidb/issues/new?labels=type%2Fbug&#x26;template=bug-report.md) .

### 3.4 SQL実行エラー {#3-4-sql-execution-error}

-   3.4.1 クライアントは`ERROR 1265(01000) Data Truncated`エラーを報告します。これは、TiDB が`Decimal`型の精度を内部で計算する方法が MySQL の精度と互換性がないためです。この問題は v3.0.10 で修正されています ( [#14438](https://github.com/pingcap/tidb/pull/14438) )。

    -   原因：

        MySQL では、2 つの大きな精度の`Decimal`が除算され、結果が 10 進数の最大精度 ( `30` ) を超える場合、 `30`桁のみが予約され、エラーは報告されません。

        TiDB では、計算結果は MySQL と同じですが、 `Decimal`を表すデータ構造内で、10 進精度のフィールドは実際の精度を保持しています。

        例として`(0.1^30) / 10`を取り上げます。 TiDB と MySQL の結果はどちらも`0`です。これは、精度が最大で`30`であるためです。ただし、TiDB では、10 進精度のフィールドは依然として`31`です。

        複数の`Decimal`除算の後、結果が正しい場合でも、この精度フィールドがどんどん大きくなり、最終的に TiDB のしきい値を超える可能性があり ( `72` )、 `Data Truncated`エラーが報告されます。

        `Decimal`の乗算では、範囲外がバイパスされ、精度が最大精度制限に設定されるため、この問題は発生しません。

    -   解決策: `Cast(xx as decimal(a, b))`手動で追加することにより、この問題を回避できます。ここで、 `a`と`b`はターゲット精度です。

### 3.5 遅いクエリの問題 {#3-5-slow-query-issues}

遅いクエリを特定するには、 [遅いクエリを特定する](/identify-slow-queries.md)を参照してください。遅いクエリを分析して処理するには、 [遅いクエリを分析する](/analyze-slow-queries.md)参照してください。

### 3.6 ホットスポットの問題 {#3-6-hotspot-issues}

分散型データベースとして、TiDB には負荷分散メカニズムがあり、アプリケーションの負荷を異なるコンピューティング ノードまたはstorageノードにできるだけ均等に分散して、サーバーリソースをより有効に活用します。ただし、特定のシナリオでは、一部のアプリケーションの負荷を適切に分散できず、パフォーマンスに影響を与え、ホットスポットとも呼ばれる単一の高負荷ポイントを形成する可能性があります。

TiDB は、ホットスポットのトラブルシューティング、解決、または回避のための完全なソリューションを提供します。負荷のホットスポットのバランスを取ることで、QPS の向上やレイテンシーなど、全体的なパフォーマンスを向上させることができます。詳細な解決策については、 [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)を参照してください。

### 3.7 高いディスク I/O 使用率 {#3-7-high-disk-i-o-usage}

CPU のボトルネックとトランザクションの競合によるボトルネックのトラブルシューティングを行った後、TiDB の応答が遅くなった場合は、現在のシステムのボトルネックを特定するために I/O メトリックを確認する必要があります。 TiDB で I/O 使用率が高い問題を特定して処理する方法については、 [高いディスク I/O 使用率のトラブルシューティング](/troubleshoot-high-disk-io.md)を参照してください。

### 3.8 ロックの衝突 {#3-8-lock-conflicts}

TiDB は完全な分散トランザクションをサポートしています。 v3.0 以降、TiDB は楽観的トランザクション モードと悲観的トランザクション モードを提供します。ロック関連の問題をトラブルシューティングする方法、および楽観的および悲観的ロックの競合を処理する方法については、 [ロック競合のトラブルシューティング](/troubleshoot-lock-conflicts.md)を参照してください。

### 3.9 データと索引の不一致 {#3-9-inconsistency-between-data-and-indexes}

TiDB は、トランザクションまたは[`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md)ステートメントを実行するときに、データとインデックスの間の整合性をチェックします。チェックにより、レコードのキー値と対応するインデックスのキー値が矛盾していることが判明した場合、つまり、行データを格納するキーと値のペアとそのインデックスを格納する対応するキーと値のペアが矛盾している場合 (たとえば、より多くのインデックスまたはインデックスが見つからない)、TiDB はデータの不整合エラーを報告し、関連するエラーをエラー ログに出力。

不整合エラーとチェックをバイパスする方法の詳細については、 [データとインデックス間の不一致のトラブルシューティング](/troubleshoot-data-inconsistency-errors.md)を参照してください。

## 4.TiKVの問題 {#4-tikv-issues}

### 4.1 TiKV がパニックになり、起動に失敗する {#4-1-tikv-panics-and-fails-to-start}

-   4.1.1 `sync-log = false` .マシンの電源をオフにした後、 `unexpected raft log index: last_index X < applied_index Y`エラーが返されます。

    この問題は予期されたものです。 `tikv-ctl`を使用してリージョンを復元できます。

-   4.1.2 TiKV が仮想マシンにデプロイされている場合、仮想マシンが強制終了されるか物理マシンの電源がオフになると、 `entries[X, Y] is unavailable from storage`エラーが報告されます。

    この問題は予期されたものです。仮想マシンの`fsync`信頼できないため、 `tikv-ctl`使用してリージョンを復元する必要があります。

-   4.1.3 その他の予期せぬ原因については、 [バグを報告](https://github.com/tikv/tikv/issues/new?template=bug-report.md) .

### 4.2 TiKV OOM {#4-2-tikv-oom}

-   4.2.1 `block-cache`構成が大きすぎると、OOM が発生する可能性があります。

    問題の原因を確認するには、モニター**Grafana** -&gt; <strong>TiKV-details</strong>で対応するインスタンスを選択して、RocksDB の`block cache size`を確認します。

    一方、 `[storage.block-cache] capacity = # "1GB"`パラメータが正しく設定されているかどうかを確認します。デフォルトでは、TiKV の`block-cache`マシンの合計メモリの`45%`に設定されています。 TiKV はコンテナーのメモリ制限を超える可能性がある物理マシンのメモリを取得するため、コンテナーに TiKV をデプロイするときに、このパラメーターを明示的に指定する必要があります。

-   4.2.2コプロセッサーが大量のクエリを受け取り、大量のデータを返します。 gRPC は、コプロセッサがデータを返すのと同じ速さでデータを送信できず、OOM が発生します。

    原因を確認するには、モニター**Grafana** -&gt; <strong>TiKV-details</strong> -&gt; <strong>coprocessor overview</strong>を表示して、 `response size` `network outbound`トラフィックを超えているかどうかを確認できます。

-   4.2.3 他のコンポーネントがメモリを占有しすぎている。

    この問題は予想外です。 [バグを報告](https://github.com/tikv/tikv/issues/new?template=bug-report.md) .

### 4.3 クライアントが<code>server is busy</code>エラーを報告する {#4-3-the-client-reports-the-code-server-is-busy-code-error}

モニタ**Grafana** -&gt; <strong>TiKV</strong> -&gt; <strong>errors</strong>を表示して、ビジーの特定の原因を確認します。 `server is busy`は、TiKV のフロー制御メカニズムが原因であり、TiKV が現在過大な圧力を受けており、後で再試行することを`tidb/ti-client`に通知します。

-   4.3.1 TiKV RocksDB は`write stall`に遭遇します。

    TiKV インスタンスには 2 つの RocksDB インスタンスがあり、 `data/raft`つはRaftログを保存するためのもので、もう`data/db`は実際のデータを保存するためのものです。ログで`grep "Stalling" RocksDB`を実行すると、ストールの具体的な原因を確認できます。 RocksDB ログは`LOG`で始まるファイルで、 `LOG`が現在のログです。

    -   `level0 sst`が多すぎると失速します。 `[rocksdb] max-sub-compactions = 2` (または 3) パラメータを追加して、 `level0 sst`圧縮を高速化できます。 level0 から level1 までの圧縮タスクは、複数のサブタスク (サブタスクの最大数は`max-sub-compactions`の値) に分割され、同時に実行されます。中国語で[ケース-815](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case815.md)参照してください。

    -   `pending compaction bytes`が多すぎると失速します。ディスク I/O は、ビジネス ピーク時の書き込み操作についていけません。この問題は、対応する CF の`soft-pending-compaction-bytes-limit`と`hard-pending-compaction-bytes-limit`を増やすことで軽減できます。

        -   `[rocksdb.defaultcf] soft-pending-compaction-bytes-limit`のデフォルト値は`64GB`です。保留中の圧縮バイトがしきい値に達すると、RocksDB は書き込み速度を遅くします。 `[rocksdb.defaultcf] soft-pending-compaction-bytes-limit` ～ `128GB`まで設定できます。

        -   `hard-pending-compaction-bytes-limit`のデフォルト値は`256GB`です。保留中のコンパクション バイト数がしきい値に達すると (保留中のコンパクション バイト数が`soft-pending-compaction-bytes-limit`に達すると、RocksDB は書き込みを遅くするため、これが発生する可能性はほとんどありません)、RocksDB は書き込み操作を停止します。 `hard-pending-compaction-bytes-limit` ～ `512GB`まで設定できます。 <!-- See [case-275](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case275.md) in Chinese.-->

        -   ディスク I/O キャパシティが書き込みに長時間対応できない場合は、ディスクをスケールアップすることをお勧めします。ディスクのスループットが上限に達し、書き込みストールが発生する場合 (たとえば、SATA SSD は NVME SSD よりもはるかに低い)、CPU リソースが十分にある場合は、より高い圧縮率の圧縮アルゴリズムを適用できます。このようにして、CPU リソースがディスク リソースと交換され、ディスクへのプレッシャーが緩和されます。

        -   デフォルトの CF 圧縮で圧力が高い場合は、 `[rocksdb.defaultcf] compression-per-level`パラメータを`["no", "no", "lz4", "lz4", "lz4", "zstd", "zstd"]`から`["no", "no", "zstd", "zstd", "zstd", "zstd", "zstd"]`に変更します。

    -   memtable が多すぎるとストールが発生します。これは通常、インスタント書き込みの量が多く、memtables がディスクにゆっくりとフラッシュされる場合に発生します。ディスクの書き込み速度を向上させることができず、この問題がビジネスのピーク時にのみ発生する場合は、対応する CF の`max-write-buffer-number`を増やすことで軽減できます。

        -   たとえば、 `[rocksdb.defaultcf] max-write-buffer-number` ～ `8` (デフォルトでは`5` ) を設定します。これにより、メモリ内のメモリが増える可能性があるため、ピーク時のメモリ使用量が増える可能性があることに注意してください。

-   4.3.2 `scheduler too busy`

    -   深刻な書き込み競合。 `latch wait duration`が高い。モニター**Grafana** -&gt; <strong>TiKV-details</strong> -&gt; <strong>scheduler prewrite</strong> / <strong>scheduler commit</strong>で`latch wait duration`表示できます。スケジューラーに書き込みタスクが溜まると、保留中の書き込みタスクが`[storage] scheduler-pending-write-threshold`で設定されたしきい値 (100MB) を超えます。 `MVCC_CONFLICT_COUNTER`に対応するメトリクスを表示することで、原因を確認できます。

    -   書き込みが遅いと、書き込みタスクが山積みになります。 TiKV に書き込まれているデータが、 `[storage] scheduler-pending-write-threshold`で設定されたしきい値 (100MB) を超えています。 [4.5](#45-tikv-write-is-slow)を参照してください。

-   4.3.3 `raftstore is busy` .メッセージの処理は、メッセージの受信よりも遅くなります。短期的な`channel full`状態はサービスに影響はありませんが、エラーが長時間続く場合は、Leaderの切り替えが発生する可能性があります。

    -   `append log`遭遇失速。 [4.3.1](#43-the-client-reports-the-server-is-busy-error)を参照してください。
    -   `append log duration`は高く、メッセージの処理が遅くなります。 [4.5](#45-tikv-write-is-slow)を参照して、 `append log duration`が高い理由を分析できます。
    -   raftstore は瞬時に大量のメッセージを受信し (TiKV Raftメッセージ ダッシュボードで確認してください)、それらの処理に失敗します。通常、短期`channel full`ステータスはサービスに影響しません。

-   4.3.4 TiKV コプロセッサーがキューに入っています。積み上げられたタスクの数が`coprocessor threads * readpool.coprocessor.max-tasks-per-worker-[normal|low|high]`を超えています。大規模なクエリが多すぎると、コプロセッサでタスクが積み重なってしまいます。実行計画の変更によって多数のテーブル スキャン操作が発生するかどうかを確認する必要があります。 [3.3](#33-wrong-execution-plan)を参照してください。

### 4.4 一部の TiKV ノードはLeaderを頻繁にドロップします {#4-4-some-tikv-nodes-drop-leader-frequently}

-   4.4.1 TiKV再始動による再選

    -   TiKV がパニックに陥った後、systemd によってプルアップされ、正常に実行されます。panicが発生したかどうかは、TiKV ログを表示することで確認できます。この問題は想定外であるため、発生した場合は[バグを報告](https://github.com/tikv/tikv/issues/new?template=bug-report.md) 。

    -   TiKV はサードパーティによって停止または強制終了され、systemd によってプルアップされます。 `dmesg`と TiKV ログを参照して原因を確認してください。

    -   TiKV は OOM であり、再起動を引き起こします。 [4.2](#42-tikv-oom)を参照してください。

    -   `THP` (Transparent Hugepage) を動的に調整するため、TiKV がハングします。中国語のケース[ケース-500](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case500.md)を参照してください。

-   4.4.2 TiKV RocksDB で書き込みストールが発生し、再選択されます。モニター**Grafana** -&gt; <strong>TiKV-details</strong> -&gt; <strong>errors が</strong>`server is busy`示しているかどうかを確認できます。 [4.3.1](#43-the-client-reports-the-server-is-busy-error)を参照してください。

-   4.4.3 ネットワーク分離による再選。

### 4.5 TiKV 書き込みが遅い {#4-5-tikv-write-is-slow}

-   4.5.1 TiKV gRPC の`prewrite/commit/raw-put`期間を表示して、TiKV 書き込みが少ないかどうかを確認します (RawKV クラスターの場合のみ)。一般に、 [パフォーマンス マップ](https://github.com/pingcap/tidb-map/blob/master/maps/performance-map.png)に従って遅い段階を見つけることができます。一般的な状況を次に示します。

-   4.5.2 スケジューラ CPU がビジーです (トランザクション kv のみ)。

    prewrite/commit の`scheduler command duration` `scheduler latch wait duration`と`storage async write duration`の合計よりも長くなっています。スケジューラ ワーカーの CPU 需要が高い ( `scheduler-worker-pool-size` * 100% の 80% を超えるなど) か、マシン全体の CPU リソースが比較的制限されています。書き込みワークロードが大きい場合は、 `[storage] scheduler-worker-pool-size`の設定が小さすぎないかどうかを確認してください。

    その他の状況については、 [バグを報告](https://github.com/tikv/tikv/issues/new?template=bug-report.md) .

-   4.5.3 ログの追加が遅い。

    TiKV Grafana の**Raft IO** / `append log duration`が高いのは、通常、ディスクの書き込み操作が遅いためです。 RocksDB - raft の`WAL Sync Duration max`値を確認することで原因を確認できます。

    その他の状況については、 [バグを報告](https://github.com/tikv/tikv/issues/new?template=bug-report.md) .

-   4.5.4 raftstore スレッドがビジーです。

    **Raft Propose** / `propose wait duration`は、TiKV Grafana の追加ログ期間よりも大幅に長くなります。次の方法を取ります。

    -   `[raftstore] store-pool-size`構成値が小さすぎるかどうかを確認します。値は`1` ～ `5`の間で、大きすぎない値に設定することをお勧めします。
    -   マシンのCPUリソースが不足していないか確認してください。

-   4.5.5 適用が遅い。

    TiKV Grafana の**Raft IO** / `apply log duration`は高く、通常は<strong>Raft Propose</strong> / `apply wait duration`が高くなります。考えられる原因は次のとおりです。

    -   `[raftstore] apply-pool-size`は小さすぎます (値は`1`から`5`の間で、大きすぎない値を設定することをお勧めします)、**スレッド CPU** / `apply CPU`は大きくなります。

    -   マシンの CPU リソースが不足しています。

    -   リージョン書き込みホット スポット。 1 つの適用スレッドの CPU 使用率が高くなります。現在、改善中の単一のリージョンでのホット スポットの問題に適切に対処できません。各スレッドの CPU 使用率を表示するには、Grafana 式を変更して`by (instance, name)`を追加します。

    -   RocksDB の書き込みが遅い。 **RocksDB kv** / `max write duration`は高いです。 1 つのRaftログに複数の KV が含まれる場合があります。 RocksDB に書き込む場合、128 KV が書き込みバッチで RocksDB に書き込まれます。したがって、適用ログは RocksDB の複数の書き込みに関連付けられる場合があります。

    -   その他の状況については、 [バグを報告](https://github.com/tikv/tikv/issues/new?template=bug-report.md) .

-   4.5.6 Raftコミット ログが遅い。

    TiKV Grafana の**Raft IO** / `commit log duration`が高い (このメトリックは、v4.x 以降の Grafana でのみサポートされています)。すべてのリージョンは、独立したRaftグループに対応します。 Raft には、TCP のスライディング ウィンドウ メカニズムに似たフロー制御メカニズムがあります。 `[raftstore] raft-max-inflight-msgs = 256`パラメータを設定することで、スライディング ウィンドウのサイズを制御できます。書き込みホット スポットがあり、 `commit log duration`が高い場合は、 `1024`に増やすなど、パラメーターを調整できます。

-   4.5.7 その他の場合は、 [パフォーマンス マップ](https://github.com/pingcap/tidb-map/blob/master/maps/performance-map.png)の書き込みパスを参照し、原因を分析してください。

## 5.PDの問題 {#5-pd-issues}

### 5.1 PD スケジューリング {#5-1-pd-scheduling}

-   5.1.1 マージ

    -   テーブル間の空のリージョンはマージできません。 v4.x ではデフォルトで`false`に設定されている TiKV の`[coprocessor] split-region-on-table`パラメータを変更する必要があります。中国語で[ケース-896](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case896.md)参照してください。

    -   リージョンのマージが遅い。マージされたオペレーターが生成されているかどうかは、 **Grafana** -&gt; <strong>PD</strong> -&gt; <strong>operator</strong>でモニター ダッシュボードにアクセスして確認できます。マージを加速するには、 `merge-schedule-limit`の値を増やします。

-   5.1.2 レプリカの追加またはレプリカのオンライン/オフライン化

    -   TiKV ディスクは容量の 80% を使用し、PD はレプリカを追加しません。この状況では、ミスピアの数が増えるため、TiKV をスケールアウトする必要があります。中国語で[ケース-801](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case801.md)を参照してください。

    -   TiKV ノードがオフラインになると、一部のリージョンを他のノードに移行できなくなります。この問題は v3.0.4 で修正されています ( [#5526](https://github.com/tikv/tikv/pull/5526) )。中国語で[ケース-870](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case870.md)参照してください。

-   5.1.3 バランス

    -   Leader/リージョンの数は均等に分散されていません。中国語の[ケース-394](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case394.md)と[ケース-759](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case759.md)を参照してください。主な原因は、 Balance がリージョン/ Leaderのサイズに基づいてスケジューリングを行うため、カウントの偏りが生じる可能性があることです。 TiDB 4.0 では、 `[leader-schedule-policy]`パラメーターが導入されました。これにより、Leaderのスケジューリング ポリシーを`count`ベースまたは`size`ベースに設定できます。

### 5.2 PD の選出 {#5-2-pd-election}

-   5.2.1 PD スイッチLeader。

    -   原因 1: ディスク。 PD ノードが配置されているディスクの I/O 負荷が最大になっています。 I/O 要求が高く、ディスクの状態が良好な他のコンポーネントと共に PD が展開されているかどうかを調査します。 **Grafana** -&gt; <strong>disk performance</strong> -&gt; <strong>レイテンシー</strong> / <strong>load</strong>でモニター メトリックを表示することで、原因を確認できます。必要に応じて、FIO ツールを使用してディスクのチェックを実行することもできます。中国語で[ケース-292](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case292.md)参照してください。

    -   原因 2: ネットワーク。 PD ログには`lost the TCP streaming connection`が表示されます。 PD ノード間のネットワークに問題があるかどうかを確認し、モニター**Grafana** -&gt; <strong>PD</strong> -&gt; <strong>etcd</strong>で`round trip`表示して原因を確認する必要があります。中国語で[ケース-177](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case177.md)参照してください。

    -   原因 3: システム負荷が高い。ログには`server is likely overloaded`表示されます。中国語で[ケース-214](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case214.md)参照してください。

-   5.2.2 PD がLeaderを選出できない、または選出が遅い。

    -   PD がLeaderを選出できない: PD ログは`lease is not expired`を示します。 v3.0.x と v2.1.19 で[この問題](https://github.com/etcd-io/etcd/issues/10355)が修正されました。中国語で[ケース-875](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case875.md)参照してください。

    -   選挙が遅い:リージョンの読み込み時間が長い。 PD ログで`grep "regions cost"`を実行すると、この問題を確認できます。結果が`load 460927 regions cost 11.77099s`などの秒単位の場合、リージョンの読み込みが遅いことを意味します。 `use-region-storage`を`true`に設定することで v3.0 の`region storage`機能を有効にできます。これにより、リージョンの読み込み時間が大幅に短縮されます。中国語で[ケース-429](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case429.md)参照してください。

-   5.2.3 TiDB が SQL ステートメントを実行すると PD がタイムアウトする。

    -   PD にはLeaderがないか、 Leader が切り替えられます。 [5.2.1](#52-pd-election)と[5.2.2](#52-pd-election)を参照してください。

    -   ネットワークの問題。モニター**Grafana** -&gt; <strong>blackbox_exporter</strong> -&gt; <strong>ping レイテンシー</strong>にアクセスして、TiDB から PDLeaderへのネットワークが正常に動作しているかどうかを確認します。

    -   PDパニック。 [バグを報告](https://github.com/pingcap/pd/issues/new?labels=kind%2Fbug&#x26;template=bug-report.md) .

    -   PD は OOM です。 [5.3](#53-pd-oom)を参照してください。

    -   問題に他の原因がある場合は、 `curl http://127.0.0.1:2379/debug/pprof/goroutine?debug=2`と[バグを報告](https://github.com/pingcap/pd/issues/new?labels=kind%2Fbug&#x26;template=bug-report.md)を実行して goroutine を取得します。

-   5.2.4 その他の問題

    -   PD は`FATAL`エラーを報告し、ログには`range failed to find revision pair`が表示されます。この問題は v3.0.8 ( [#2040](https://github.com/pingcap/pd/pull/2040) ) で修正されています。詳細については、中国語の[ケース-947](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case947.md)を参照してください。

    -   その他の状況については、 [バグを報告](https://github.com/pingcap/pd/issues/new?labels=kind%2Fbug&#x26;template=bug-report.md) .

### 5.3 PD OOM {#5-3-pd-oom}

-   5.3.1 `/api/v1/regions`インターフェースを使用する場合、リージョンが多すぎると PD OOM が発生する可能性があります。この問題は v3.0.8 で修正されています ( [#1986](https://github.com/pingcap/pd/pull/1986) )。

-   5.3.2 ローリング アップグレード中の PD OOM。 gRPC メッセージのサイズは制限されておらず、モニターは TCP InSeg が比較的大きいことを示しています。この問題は v3.0.6 で修正されています ( [#1952](https://github.com/pingcap/pd/pull/1952) )。 <!--For details, see [case-852](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case852.md).-->

### 5.4 グラファナ表示 {#5-4-grafana-display}

-   5.4.1 **Grafana**のモニター -&gt; <strong>PD</strong> -&gt;<strong>クラスター</strong>-&gt;<strong>ロール</strong>はフォロワーを表示します。 Grafana 式の問題は v3.0.8 で修正されました。

## 6. 生態系ツール {#6-ecosystem-tools}

### 6.1 TiDBBinlog {#6-1-tidb-binlog}

-   6.1.1 TiDB Binlog は、 TiDB から変更を収集し、ダウンストリームの TiDB または MySQL プラットフォームにバックアップとレプリケーションを提供するツールです。詳細については、 [GitHub の TiDB Binlog](https://github.com/pingcap/tidb-binlog)を参照してください。

-   6.1.2 Pump/ Drainer Status の`Update Time`正常に更新され、ログに異常は表示されませんが、下流にデータが書き込まれません。

    -   Binlog はTiDB 構成で有効になっていません。 TiDB の`[binlog]`構成を変更します。

-   6.1.3 Drainerの`sarama` `EOF`エラーを報告します。

    -   Drainerの Kafka クライアントのバージョンは、Kafka のバージョンと矛盾しています。 `[syncer.to] kafka-version`構成を変更する必要があります。

-   6.1.4 Drainer がKafka への書き込みに失敗してパニックになり、Kafka が`Message was too large`エラーを報告します。

    -   binlogデータが大きすぎるため、Kafka に書き込まれる 1 つのメッセージが大きすぎます。次の Kafka の構成を変更する必要があります。

        ```conf
        message.max.bytes=1073741824
        replica.fetch.max.bytes=1073741824
        fetch.message.max.bytes=1073741824
        ```

        詳細については、中国語の[ケース-789](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case789.md)を参照してください。

-   6.1.5 アップストリームとダウンストリームのデータの不整合

    -   一部の TiDB ノードはbinlog を有効にしません。 v3.0.6 以降のバージョンでは、 [http://127.0.0.1:10080/info/all](http://127.0.0.1:10080/info/all)インターフェースにアクセスすることで、すべてのノードのbinlogステータスを確認できます。 v3.0.6 より前のバージョンでは、構成ファイルを表示してbinlog の状態を確認できます。

    -   一部の TiDB ノードは`ignore binlog`ステータスになります。 v3.0.6 以降のバージョンでは、 [http://127.0.0.1:10080/info/all](http://127.0.0.1:10080/info/all)インターフェイスにアクセスすることで、すべてのノードのbinlogステータスを確認できます。 v3.0.6 より前のバージョンの場合は、TiDB ログをチェックして、 `ignore binlog`キーワードが含まれているかどうかを確認してください。

    -   アップストリームとダウンストリームでタイムスタンプ列の値が一致しません。

        -   これは、異なるタイム ゾーンが原因です。 Drainer が上流および下流のデータベースと同じタイム ゾーンにあることを確認する必要があります。 Drainer は`/etc/localtime`からタイム ゾーンを取得し、 `TZ`環境変数をサポートしません。中国語で[ケース-826](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case826.md)参照してください。

        -   TiDB では、timestamp のデフォルト値は`null`ですが、 MySQL 5.7 (MySQL 8 を除く) の同じデフォルト値は現在の時刻です。したがって、上流の TiDB のタイムスタンプが`null`で下流がMySQL 5.7の場合、タイムスタンプ列のデータは矛盾しています。 binlogを有効にする前に、アップストリームで`set @@global.explicit_defaults_for_timestamp=on;`を実行する必要があります。

    -   その他の状況については、 [バグを報告](https://github.com/pingcap/tidb-binlog/issues/new?labels=bug&#x26;template=bug-report.md) .

-   6.1.6 遅い複製

    -   ダウンストリームは TiDB/MySQL であり、アップストリームは頻繁な DDL 操作を実行します。中国語で[ケース-1023](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case1023.md)を参照してください。

    -   ダウンストリームは TiDB/MySQL であり、レプリケートされるテーブルには主キーと一意のインデックスがないため、 binlogでのパフォーマンスが低下します。主キーまたは一意のインデックスを追加することをお勧めします。

    -   ダウンストリームがファイルに出力する場合は、出力ディスクまたはネットワーク ディスクが遅いかどうかを確認します。

    -   その他の状況については、 [バグを報告](https://github.com/pingcap/tidb-binlog/issues/new?labels=bug&#x26;template=bug-report.md) .

-   6.1.7Pumpがbinlogを書き込めず、 `no space left on device`エラーが報告されます。

    -   Pump がbinlogデータを正常に書き込むには、ローカル ディスク容量が不足しています。ディスク領域をクリーンアップしてから、 Pumpを再起動する必要があります。

-   6.1.8Pumpは起動時に`fail to notify all living drainer`エラーを報告します。

    -   原因: Pumpが開始されると、状態が`online`のすべてのDrainerノードに通知されます。 Drainerへの通知に失敗した場合、このエラー ログが出力されます。

    -   解決策: binlogctl ツールを使用して、各Drainerノードが正常かどうかを確認します。これは、 `online`状態のすべてのDrainerノードが正常に動作していることを確認するためです。 Drainerノードの状態が実際の動作状態と一致しない場合は、binlogctl ツールを使用して状態を変更し、 Pumpを再起動します。ケース[通知に失敗したすべての生きているドレーナー](/tidb-binlog/handle-tidb-binlog-errors.md#fail-to-notify-all-living-drainer-is-returned-when-pump-is-started)を参照してください。

-   6.1.9 Drainer が`gen update sqls failed: table xxx: row data is corruption []`エラーを報告します。

    -   トリガー: アップストリームは、 `DROP COLUMN` DDL を実行しながら、このテーブルで DML 操作を実行します。この問題は v3.0.6 で修正されています。中国語で[ケース-820](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case820.md)参照してください。

-   6.1.10 Drainer の複製がハングします。プロセスはアクティブなままですが、チェックポイントは更新されません。

    -   この問題は v3.0.4 で修正されています。中国語で[ケース-741](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case741.md)を参照してください。

-   6.1.11コンポーネントのパニック。

    -   [バグを報告](https://github.com/pingcap/tidb-binlog/issues/new?labels=bug&#x26;template=bug-report.md) .

### 6.2 データ移行 {#6-2-data-migration}

-   6.2.1 TiDB Data Migration (DM) は、MySQL/MariaDB から TiDB へのデータ移行をサポートする移行ツールです。詳細については、 [GitHub の DM](https://github.com/pingcap/dm/)を参照してください。

-   6.2.2 `Access denied for user 'root'@'172.31.43.27' (using password: YES)` 、 `query status`実行するか、ログを確認すると表示されます。

    -   すべての DM 構成ファイル内のデータベース関連のパスワードは`dmctl`で暗号化する必要があります。データベースのパスワードが空の場合、パスワードを暗号化する必要はありません。 v1.0.6以降、クリアテキストのパスワードを使用できます。
    -   DM の操作中、アップストリーム データベースとダウンストリーム データベースのユーザーは、対応する読み取りおよび書き込み権限を持っている必要があります。データ複製タスクの開始中に、データ移行も自動的に[対応する権限を事前チェックします](/dm/dm-precheck.md)なります。
    -   DM クラスターに異なるバージョンの DM-worker/DM-master/dmctl をデプロイするには、中国語の[AskTUGのケーススタディ](https://asktug.com/t/dm1-0-0-ga-access-denied-for-user/1049/5)を参照してください。

-   6.2.3 `driver: bad connection`のエラーが返されてレプリケーション タスクが中断されます。

    -   `driver: bad connection`エラーは、DM と下流の TiDB データベースとの間の接続に異常 (ネットワーク障害や TiDB の再起動など) が発生し、現在の要求のデータがまだ TiDB に送信されていないことを示します。

        -   DM 1.0.0 GA より前のバージョンの場合、 `stop-task`を実行してタスクを停止し、 `start-task`を実行してタスクを再開します。
        -   DM 1.0.0 GA 以降のバージョンでは、このタイプのエラーに対する自動再試行メカニズムが追加されています。 [#265](https://github.com/pingcap/dm/pull/265)を参照してください。

-   6.2.4 レプリケーション タスクが`invalid connection`エラーで中断されます。

    -   `invalid connection`エラーは、DM と下流の TiDB データベース間の接続に異常 (ネットワーク障害、TiDB 再起動、TiKV ビジーなど) が発生し、現在の要求のデータの一部が TiDB に送信されたことを示します。 DM には、レプリケーション タスクでデータを下流に同時にレプリケートする機能があるため、タスクが中断されると、いくつかのエラーが発生する可能性があります。これらのエラーは、 `query-status`または`query-error`を実行して確認できます。

        -   増分レプリケーション プロセス中にエラーが`invalid connection`だけ発生した場合、DM はタスクを自動的に再試行します。
        -   DM が再試行しないか、バージョンの問題が原因で自動再試行に失敗した場合 (自動再試行は v1.0.0-rc.1 で導入されました)、 `stop-task`を使用してタスクを停止し、 `start-task`使用してタスクを再開します。

-   6.2.5 リレー ユニットがエラー`event from * in * diff from passed-in event *`を報告するか、binlogの取得または解析に失敗するエラーでレプリケーション タスクが中断されます`get binlog error ERROR 1236 (HY000) and binlog checksum mismatch, data may be corrupted returned`

    -   DM がリレー ログまたは増分レプリケーションをプルするプロセス中に、上流のbinlogファイルのサイズが 4 GB を超えると、この 2 つのエラーが発生する可能性があります。

    -   原因: リレー ログを書き込むとき、DM はbinlog の位置とbinlogファイルのサイズに基づいてイベント検証を実行し、レプリケートされたbinlog の位置をチェックポイントとして保存する必要があります。ただし、公式の MySQL は uint32 を使用してbinlog位置を保存します。つまり、4 GB を超えるbinlogファイルのbinlog位置がオーバーフローし、上記のエラーが発生します。

    -   解決：

        -   中継処理ユニットの場合、 [レプリケーションを手動で回復する](https://pingcap.com/docs/tidb-data-migration/dev/error-handling/#the-relay-unit-throws-error-event-from--in--diff-from-passed-in-event--or-a-replication-task-is-interrupted-with-failing-to-get-or-parse-binlog-errors-like-get-binlog-error-error-1236-hy000-and-binlog-checksum-mismatch-data-may-be-corrupted-returned) ．
        -   binlogレプリケーション処理ユニットの場合、 [レプリケーションを手動で回復する](https://pingcap.com/docs/tidb-data-migration/dev/error-handling/#the-relay-unit-throws-error-event-from--in--diff-from-passed-in-event--or-a-replication-task-is-interrupted-with-failing-to-get-or-parse-binlog-errors-like-get-binlog-error-error-1236-hy000-and-binlog-checksum-mismatch-data-may-be-corrupted-returned) .

-   6.2.6 DM レプリケーションが中断され、ログが`ERROR 1236 (HY000) The slave is connecting using CHANGE MASTER TO MASTER_AUTO_POSITION = 1, but the master has purged binary logs containing GTIDs that the slave requires.`を返す

    -   マスターbinlog がパージされているかどうかを確認します。
    -   `relay.meta`で記録した位置情報を確認します。

        -   `relay.meta`には空の GTID 情報が記録されています。 DM-worker は、終了時または 30 秒ごとに GTID 情報をメモリに`relay.meta`に保存します。 DM-worker が上流の GTID 情報を取得できない場合、空の GTID 情報を`relay.meta`に保存します。中国語で[ケース-772](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case772.md)参照してください。

        -   `relay.meta`で記録されたbinlogイベントは、不完全な回復プロセスをトリガーし、間違った GTID 情報を記録します。この問題は v1.0.2 で修正されており、以前のバージョンでは発生する可能性があります。 <!--See [case-764](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case764.md).-->

-   6.2.7 DM 複製プロセスがエラー`Error 1366: incorrect utf8 value eda0bdedb29d(\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd)`を返します。

    -   この値は、MySQL 8.0 または TiDB に正常に書き込むことはできませんが、 MySQL 5.7には書き込むことができます。 `tidb_skip_utf8_check`パラメータを有効にすると、データ形式のチェックをスキップできます。

### 6.3 TiDB Lightning {#6-3-tidb-lightning}

-   6.3.1 TiDB Lightning は、大量のデータを TiDB クラスターに高速に完全にインポートするためのツールです。 [GitHub のTiDB Lightning](https://github.com/pingcap/tidb/tree/master/br/pkg/lightning)を参照してください。

-   6.3.2 インポート速度が遅すぎる。

    -   `region-concurrency`の設定が高すぎると、スレッドの競合が発生し、パフォーマンスが低下します。トラブルシューティングの 3 つの方法:

        -   設定は、ログの先頭から`region-concurrency`を検索して見つけることができます。
        -   TiDB Lightningがサーバーを他のサービス (インポーターなど) と共有する場合、そのサーバーの CPU コアの総数の`region-concurrency` ～ 75% を手動で設定する必要があります。
        -   CPU にクォータがある場合 (たとえば、Kubernetes の設定によって制限されている場合)、 TiDB Lightning はこれを読み取れない可能性があります。この場合、 `region-concurrency`も手動で減らす必要があります。

    -   インデックスを追加するたびに、行ごとに新しい KV ペアが導入されます。 N 個のインデックスがある場合、インポートされる実際のサイズは、 [マイダンパー](https://docs.pingcap.com/tidb/v4.0/mydumper-overview)の出力のサイズの約 (N+1) 倍になります。インデックスが無視できる場合は、最初にそれらをスキーマから削除し、インポートが完了した後に`CREATE INDEX`を介してそれらを再度追加することができます。

    -   TiDB Lightningのバージョンが古い。インポート速度が向上する可能性がある最新バージョンを試してください。

-   6.3.3 `checksum failed: checksum mismatched remote vs local` .

    -   原因 1: テーブルに既にデータがある可能性があります。これらの古いデータは、最終的なチェックサムに影響を与える可能性があります。

    -   原因 2: ターゲット データベースのチェックサムが 0 の場合、つまり何もインポートされていない場合、クラスターが過熱してデータの取り込みに失敗している可能性があります。

    -   原因 3: データ ソースがマシンによって生成され、 [マイダンパー](https://docs.pingcap.com/tidb/v4.0/mydumper-overview)によってバックアップされていない場合は、テーブルの制約に従っていることを確認してください。例えば：

        -   `AUTO_INCREMENT`列は正である必要があり、値「0」が含まれていません。
        -   UNIQUE および PRIMARY KEY に重複するエントリがあってはなりません。

    -   解決策: [トラブルシューティングの解決策](/tidb-lightning/troubleshoot-tidb-lightning.md#checksum-failed-checksum-mismatched-remote-vs-local)を参照してください。

-   6.3.4 `Checkpoint for … has invalid status:(error code)`

    -   原因: チェックポイントが有効になっていて、Lightning/Importer が以前に異常終了しました。偶発的なデータ破損を防ぐために、 TiDB Lightning はエラーが解決されるまで起動しません。エラー コードは 25 未満の整数で、可能な値は`0, 3, 6, 9, 12, 14, 15, 17, 18, 20 and 21`です。整数は、インポート プロセスで予期しない終了が発生したステップを示します。整数が大きいほど、終了が遅くなります。

    -   解決策: [トラブルシューティングの解決策](/tidb-lightning/troubleshoot-tidb-lightning.md#checkpoint-for--has-invalid-status-error-code)を参照してください。

-   6.3.5 `ResourceTemporarilyUnavailable("Too many open engines …: 8")`

    -   原因: 同時エンジン ファイルの数が、tikv-importer で指定された制限を超えています。これは、設定ミスが原因である可能性があります。また、設定が正しい場合でも、以前に tidb-lightning が異常終了したことがあると、エンジン ファイルがダングリング オープン状態のままになる可能性があり、これも同様のエラーを引き起こす可能性があります。
    -   解決策: [トラブルシューティングの解決策](/tidb-lightning/troubleshoot-tidb-lightning.md#resourcetemporarilyunavailabletoo-many-open-engines--)を参照してください。

-   6.3.6 `cannot guess encoding for input file, please convert to UTF-8 manually`

    -   原因: TiDB Lightning は、 UTF-8 および GB-18030 エンコーディングのみをサポートしています。このエラーは、ファイルがこれらのエンコーディングのいずれでもないことを意味します。過去の ALTER TABLE の実行により、UTF-8 の文字列と GB-18030 の別の文字列が含まれているなど、ファイルにエンコーディングが混在している可能性もあります。

    -   解決策: [トラブルシューティングの解決策](/tidb-lightning/troubleshoot-tidb-lightning.md#cannot-guess-encoding-for-input-file-please-convert-to-utf-8-manually)を参照してください。

-   6.3.7 `[sql2kv] sql encode error = [types:1292]invalid time format: '{1970 1 1 0 45 0 0}'`

    -   原因: タイムスタンプ タイプのエントリに、存在しない時間値があります。これは、DST の変更が原因であるか、時間の値がサポートされている範囲 (1970 年 1 月 1 日から 2038 年 1 月 19 日まで) を超えたためです。

    -   解決策: [トラブルシューティングの解決策](/tidb-lightning/troubleshoot-tidb-lightning.md#sql2kv-sql-encode-error--types1292invalid-time-format-1970-1-1-)を参照してください。

## 7. 共通ログ分析 {#7-common-log-analysis}

### 7.1 TiDB {#7-1-tidb}

-   7.1.1 `GC life time is shorter than transaction duration` .

    トランザクション期間が GC の有効期間 (既定では 10 分) を超えています。

    [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)システム変数を変更することで、GC の寿命を延ばすことができます。通常、このパラメーターを変更することはお勧めしません。これを変更すると、このトランザクションに`UPDATE`と`DELETE`ステートメントが多数含まれている場合、多くの古いバージョンが蓄積される可能性があるためです。

-   7.1.2 `txn takes too much time` .

    このエラーは、長時間 (590 秒以上) コミットされていないトランザクションをコミットすると返されます。

    アプリケーションがこのような長時間のトランザクションを実行する必要がある場合は、 `[tikv-client] max-txn-time-use = 590`パラメータと GC の有効期間を増やして、この問題を回避できます。アプリケーションがそのような長いトランザクション時間を必要とするかどうかを確認することをお勧めします。

-   7.1.3 `coprocessor.go`レポート`request outdated` 。

    このエラーは、TiKV に送信されたコプロセッサー要求が TiKV のキューで 60 秒以上待機している場合に返されます。

    TiKV コプロセッサーが長いキューに入っている理由を調査する必要があります。

-   7.1.4 `region_cache.go`多数の`switch region peer to next due to send request fail`を報告し、エラー メッセージは`context deadline exceeded`です。

    TiKV のリクエストがタイムアウトになり、リージョン キャッシュがトリガーされて、リクエストが他のノードに切り替えられます。ログの`addr`フィールドで`grep "<addr> cancelled`コマンドを引き続き実行し、 `grep`結果に従って次の手順を実行できます。

    -   `send request is cancelled` : 送信フェーズ中にリクエストがタイムアウトしました。 **Grafana** -&gt; <strong>TiDB</strong> -&gt; <strong>Batch Client</strong> / `Pending Request Count by TiKV`の監視を調査し、保留中の要求数が 128 より大きいかどうかを確認できます。

        -   128を超えると送信がKVの処理能力を超えてしまうため、送信が重なってしまいます。
        -   値が 128 以下の場合は、ログをチェックして、レポートが対応する KV の運用および保守の変更によって引き起こされているかどうかを確認します。それ以外の場合、このエラーは予期しないものであり、 [バグを報告](https://github.com/pingcap/tidb/issues/new?labels=type%2Fbug&#x26;template=bug-report.md)する必要があります。

    -   `wait response is cancelled` : リクエストが TiKV に送信された後にタイムアウトになりました。対応する TiKV アドレスの応答時間を確認する必要があり、その時点でリージョンがPD と KV にログインします。

-   7.1.5 `distsql.go`レポート`inconsistent index` 。

    データ インデックスに一貫性がないようです。報告されたインデックスがあるテーブルで`admin check table <TableName>`コマンドを実行します。チェックが失敗した場合は、次のコマンドを実行してガベージコレクションを無効にし、 [バグを報告](https://github.com/pingcap/tidb/issues/new?labels=type%2Fbug&#x26;template=bug-report.md) :

    ```sql
    SET GLOBAL tidb_gc_enable = 0;
    ```

### 7.2 TiKV {#7-2-tikv}

-   7.2.1 `key is locked` .

    読み取りと書き込みが競合しています。読み取り要求は、コミットされていないデータに遭遇し、データがコミットされるまで待機する必要があります。

    このエラーの数が少ない場合はビジネスに影響はありませんが、このエラーの数が多い場合は、ビジネスで読み取りと書き込みの競合が深刻であることを示しています。

-   7.2.2 `write conflict` .

    これは、楽観的トランザクションにおける書き込みと書き込みの競合です。複数のトランザクションが同じキーを変更した場合、1 つのトランザクションのみが成功し、他のトランザクションは自動的にタイムスタンプを再度取得して操作を再試行します。ビジネスに影響はありません。

    競合が深刻な場合、複数回の再試行後にトランザクションが失敗する可能性があります。この場合、悲観的ロックを使用することをお勧めします。エラーと解決策の詳細については、 [オプティミスティック トランザクションでの書き込み競合のトラブルシューティング](/troubleshoot-write-conflicts.md)を参照してください。

-   7.2.3 `TxnLockNotFound` .

    このトランザクション コミットは遅すぎるため、Time To Live (TTL) 後に他のトランザクションによってロールバックされます。このトランザクションは自動的に再試行されるため、通常、ビジネスは影響を受けません。サイズが 0.25 MB 以下のトランザクションの場合、デフォルトの TTL は 3 秒です。詳細については、 [`LockNotFound`エラー](/troubleshoot-lock-conflicts.md#locknotfound-error)を参照してください。

-   7.2.4 `PessimisticLockNotFound` .

    `TxnLockNotFound`に似ています。悲観的トランザクション コミットは遅すぎるため、他のトランザクションによってロールバックされます。

-   7.2.5 `stale_epoch` .

    リクエストのエポックが古いため、TiDB はルーティングを更新した後にリクエストを再送信します。ビジネスに影響はありません。リージョンに分割/マージ操作があるか、レプリカが移行されると、エポックが変更されます。

-   7.2.6 `peer is not leader` .

    リクエストは、 Leaderではないレプリカに送信されます。エラー応答がどのレプリカが最新のLeaderであるかを示している場合、TiDB はエラーに従ってローカル ルーティングを更新し、新しい要求を最新のLeaderに送信します。通常、ビジネスは影響を受けません。

    v3.0 以降のバージョンでは、以前のLeaderへのリクエストが失敗した場合、TiDB は他のピアを試行し、TiKV ログで頻繁に`peer is not leader`になる可能性があります。 TiDB で対応するリージョンの`switch region peer to next due to send request fail`ログを確認して、送信エラーの根本原因を特定できます。詳細は[7.1.4](#71-tidb)を参照してください。

    このエラーは、他の理由でリージョンにLeaderがない場合にも返されることがあります。詳細については、 [4.4](#44-some-tikv-nodes-drop-leader-frequently)を参照してください。
