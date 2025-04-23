---
title: TiDB Troubleshooting Map
summary: TiDB の一般的なエラーをトラブルシューティングする方法を学びます。
---

# TiDB トラブルシューティング マップ {#tidb-troubleshooting-map}

このドキュメントでは、TiDB およびその他のコンポーネントにおける一般的な問題をまとめています。関連する問題が発生した場合、このマップを使用して診断と解決を行うことができます。

## 1. サービスは利用できません {#1-service-unavailable}

### 1.1 クライアントが<code>Region is Unavailable</code>エラーを報告する {#1-1-the-client-reports-code-region-is-unavailable-code-error}

-   1.1.1 `Region is Unavailable`エラーは通常、リージョンが一定期間利用できないために発生します。3 `TiKV server is busy`発生する場合や、 `not leader`または`epoch not match`原因で TiKV へのリクエストが失敗する、あるいは TiKV へのリクエストがタイムアウトする場合もあります。このような場合、TiDB は`backoff`の再試行メカニズムを実行します。11 `backoff`しきい値（デフォルトでは 20 秒）を超えると、エラーがクライアントに送信されます。13 `backoff`しきい値を超えると、このエラーはクライアントには表示されません。

-   1.1.2 複数のTiKVインスタンスが同時にOOM状態になり、OOM期間中にLeaderが存在しない状態になります。中国語版の[ケース991](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case991.md)ご覧ください。

-   1.1.3 TiKVは`TiKV server is busy`報告し、 `backoff`回を超えています。詳細は[4.3](#43-the-client-reports-the-server-is-busy-error)を参照してください。7 `TiKV server is busy`内部フロー制御メカニズムの結果であり、 `backoff`回にカウントされるべきではありません。この問題は修正される予定です。

-   1.1.4 複数の TiKV インスタンスの起動に失敗し、リージョンにLeaderが存在しない状態になります。物理マシンに複数の TiKV インスタンスがデプロイされている場合、ラベルが適切に設定されていないと、物理マシンの障害によってリージョンにLeaderが存在しない状態になる可能性があります。中国語版の[ケース228](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case228.md)参照してください。

-   1.1.5Followerの適用が前のエポックで遅れている場合、FollowerがLeaderになった後、 `epoch not match`でリクエストを拒否します。中国語では[ケース958](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case958.md)参照してください（TiKVはメカニズムを最適化する必要があります）。

### 1.2 PDエラーによりサービスが利用できなくなる {#1-2-pd-errors-cause-service-unavailable}

[5 PDの問題](#5-pd-issues)を参照してください。

## 2. レイテンシーが大幅に増加する {#2-latency-increases-significantly}

### 2.1 一時的な増加 {#2-1-transient-increase}

-   2.1.1 TiDB実行プランが間違っているとレイテンシーが増加します。1を参照してください[3.3](#33-wrong-execution-plan)
-   2.1.2 PDLeader選挙問題またはOOM。1と[5.2](#52-pd-election) [5.3](#53-pd-oom)参照してください。
-   2.1.3 一部のTiKVインスタンスでLeaderの離脱が多数発生しています[4.4](#44-some-tikv-nodes-drop-leader-frequently)を参照してください。
-   2.1.4 その他の原因については、 [読み取りおよび書き込みレイテンシの増加のトラブルシューティング](/troubleshoot-cpu-issues.md)参照してください。

### 2.2 持続的かつ顕著な増加 {#2-2-persistent-and-significant-increase}

-   2.2.1 TiKVシングルスレッドボトルネック

    -   TiKVインスタンス内のリージョンが多すぎると、単一のgRPCスレッドがボトルネックになります（ **Grafana** -&gt; **TiKV詳細**-&gt;**スレッドCPU/gRPC CPU Per Thread**メトリックを確認してください）。v3.x以降のバージョンでは、 `Hibernate Region`有効にするとこの問題を解決できます。中国語版は[ケース612](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case612.md)ご覧ください。

    -   v3.0 より前のバージョンでは、raftstore スレッドまたは apply スレッドがボトルネックになる場合 ( **Grafana** -&gt; **TiKV-details** -&gt; **Thread CPU/raft store CPU**および**Async apply CPU**メトリックが`80%`超える)、TiKV (v2.x) インスタンスをスケールアウトするか、マルチスレッド対応の v3.x にアップグレードできます。 <!-- See [case-517](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case517.md) in Chinese. -->

-   2.2.2 CPU負荷が増加します。

-   2.2.3 TiKVの低速書き込み[4.5](#45-tikv-write-is-slow)を参照してください。

-   2.2.4 TiDBの実行プランが間違っています。1を参照してください[3.3](#33-wrong-execution-plan)

-   2.2.5 その他の原因については、 [読み取りおよび書き込みレイテンシの増加のトラブルシューティング](/troubleshoot-cpu-issues.md)参照してください。

## 3. TiDBの問題 {#3-tidb-issues}

### 3.1 DDL {#3-1-ddl}

-   3.1.1 `decimal`フィールドの長さを変更すると、エラー`ERROR 1105 (HY000): unsupported modify decimal column precision`が報告されます。 <!--See [case-1004](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case517.md) in Chinese.--> TiDB は`decimal`フィールドの長さの変更をサポートしていません。

-   3.1.2 TiDB DDLジョブがハングしたり実行速度が遅くなる（DDLの進行状況を確認するには`admin show ddl jobs`使用）

    -   原因1: TiDBはバージョン6.3.0で[メタデータロック](/metadata-lock.md)を導入し、バージョン6.5.0以降ではデフォルトで有効になっています。DDL操作に関係するテーブルが、コミットされていないトランザクションに関係するテーブルと交差している場合、トランザクションがコミットまたはロールバックされるまでDDL操作はブロックされます。

    -   原因 2: 他のコンポーネント (PD/TiKV) とのネットワークの問題。

    -   原因 3: TiDB の初期バージョン (v3.0.8 より前) では、高同時実行での goroutine が多数あるため、内部負荷が高くなります。

    -   原因 4: 以前のバージョン (v2.1.15 およびバージョン &lt; v3.0.0-rc1) では、PD インスタンスが TiDB キーの削除に失敗し、すべての DDL 変更が 2 つのリースを待機することになります。

    -   その他の原因不明の場合、 [バグを報告する](https://github.com/pingcap/tidb/issues/new?labels=type%2Fbug&#x26;template=bug-report.md) 。

    -   解決：

        -   原因 1 の場合、TiDB と TiKV/PD 間のネットワーク接続を確認してください。
        -   原因2と3については、問題は以降のバージョンで既に修正されています。TiDBを以降のバージョンにアップグレードできます。
        -   その他の原因の場合は、DDL 所有者を移行する次の解決策を使用できます。

    -   DDL 所有者の移行:

        -   TiDBサーバーに接続できる場合は、所有者選出コマンドを再度実行します`curl -X POST http://{TiDBIP}:10080/ddl/owner/resign`
        -   TiDBサーバーに接続できない場合は、 `tidb-ctl`使用してPDクラスターのetcdからDDL所有者を削除し、再選挙をトリガーします`tidb-ctl etcd delowner [LeaseID] [flags] + ownerKey`

-   3.1.3 TiDBがログに`information schema is changed`エラーを報告する

    -   詳しい原因と解決策については[`Information schema is changed`エラーが報告される理由](/faq/sql-faq.md#what-triggers-the-information-schema-is-changed-error)参照してください。

    -   背景：増加した`schema version`の数は、各DDL変更操作の`schema state`の数と一致しています。例えば、 `create table`操作ではバージョン変更が1つ、 `add column`操作ではバージョン変更が4つあります。そのため、列変更操作が多すぎると、 `schema version`急速に増加する可能性があります。詳細は[オンラインスキーマ変更](https://static.googleusercontent.com/media/research.google.com/zh-CN//pubs/archive/41376.pdf)を参照してください。

-   3.1.4 TiDBがログに`information schema is out of date`報告

    -   原因1: DML文を実行中のTiDBサーバーが`graceful kill`によって停止され、終了準備中です。DML文を含むトランザクションの実行時間が1DDLリースを超えています。トランザクションがコミットされるとエラーが報告されます。

    -   原因2: TiDBサーバーがDML文の実行中にPDまたはTiKVに接続できません。その結果、TiDBサーバーは1つのDDLリース（デフォルトは`45s` ）内に新しいスキーマをロードしなかったか、 `keep alive`に設定されてPDから切断されサーバーた。

    -   原因3: TiKVの負荷が高いか、ネットワークがタイムアウトしています。Grafana -&gt; **TiDB**と**TiKV**でノード**の**負荷を確認してください。

    -   解決：

        -   原因 1 の場合、TiDB の起動時に DML 操作を再試行します。
        -   原因 2 の場合、TiDBサーバーと PD/TiKV 間のネットワークを確認してください。
        -   原因3については、TiKVがビジー状態になっている理由を調べてください。1を参照してください[4 TiKVの問題](#4-tikv-issues)

### 3.2 OOMの問題 {#3-2-oom-issues}

-   3.2.1 症状

    -   クライアント: クライアントがエラー`ERROR 2013 (HY000): Lost connection to MySQL server during query`を報告します。

    -   ログを確認する

        -   `dmesg -T | grep tidb-server`実行します。結果として、エラーが発生した時点周辺の OOM-killer ログが表示されます。

        -   エラーが発生した後の時点（つまり、tidb-server が再起動した時点）の「Welcome to TiDB」ログ`tidb.log`を grep します。

        -   `tidb_stderr.log`の`fatal error: runtime: out of memory`または`cannot allocate memory` grep します。

        -   v2.1.8 以前のバージョンでは、 `tidb_stderr.log`の`fatal error: stack overflow` grep できます。

    -   モニター: tidb-server インスタンスのメモリ使用量が短期間で急増します。

-   3.2.2 OOM の原因となっている SQL 文を特定します。(現在、TiDB のすべてのバージョンでは SQL 文を正確に特定できません。SQL 文を特定した後でも、OOM の原因がその SQL 文にあるかどうかを分析する必要があります。)

    -   バージョンが v3.0.0 以上の場合には、 `tidb.log`で &quot;expensive_query&quot; を grep してください。このログメッセージには、タイムアウトした、またはメモリクォータを超えた SQL クエリが記録されます。

    -   バージョン &lt; v3.0.0 の場合、 `tidb.log`で grep &quot;メモリ exceeds quota&quot; を実行して、メモリクォータを超える SQL クエリを見つけます。

    > **注記：**
    >
    > 単一のSQLメモリ使用量のデフォルトのしきい値は`1GB`です。このパラメータは、システム変数[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)設定することで設定できます。

-   3.2.3 OOMの問題を軽減する

    -   `SWAP`有効にすると、大規模クエリによるメモリの過剰使用によって引き起こされる OOM 問題を軽減できます。メモリが不足している場合、この方法は I/O オーバーヘッドにより大規模クエリのパフォーマンスに影響を与える可能性があります。パフォーマンスへの影響の程度は、残りのメモリ容量とディスク I/O 速度によって異なります。

-   3.2.4 OOMの典型的な理由

    -   SQLクエリには`join`あります。3 `explain`使用してSQL文を表示すると、 `join`操作で`HashJoin`アルゴリズムが選択され、 `inner`テーブルが大きいことがわかります。

    -   `UPDATE/DELETE`クエリのデータ量が大きすぎます。中国語では[ケース882](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case882.md)参照してください。

    -   SQLには`Union`で接続された複数のサブクエリが含まれています。中国語では[ケース-1828](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case1828.md)参照してください。

OOM のトラブルシューティングの詳細については、 [TiDB OOM の問題のトラブルシューティング](/troubleshoot-tidb-oom.md)参照してください。

### 3.3 間違った実行計画 {#3-3-wrong-execution-plan}

-   3.3.1 症状

    -   SQLクエリの実行時間が前回の実行と比べて大幅に長くなったり、実行プランが突然変更されたりすることがあります。実行プランがスローログに記録されている場合は、実行プランを直接比較できます。

    -   SQLクエリの実行時間は、MySQLなどの他のデータベースと比べてかなり長くなります。他のデータベースとの実行プランを比較すると、 `Join Order`ような違いが分かります。

    -   スローログではSQL実行時間`Scan Keys`の数値が大きいです。

-   3.3.2 実行計画の調査

    -   `explain analyze {SQL}` 。実行時間が許容範囲内であれば、 `explain analyze`結果の`count`と`execution info`の`row`を比較してください`TableScan/IndexScan`行目に大きな差がある場合は、統計情報に誤りがある可能性があります。他の行にも大きな差がある場合は、統計情報に問題があるわけではない可能性があります。

    -   `select count(*)` 。実行プランに`join`操作が含まれている場合、 `explain analyze`長い時間がかかる可能性があります`TableScan/IndexScan`の条件で`select count(*)`実行し、 `explain`結果の`row count`情報と比較することで、統計情報に問題があるかどうかを確認できます。

-   3.3.3 緩和策

    -   v3.0 以降のバージョンでは、 `SQL Bind`機能を使用して実行プランをバインドします。

    -   統計を更新してください。問題の原因が統計[統計をダンプする](/statistics.md#export-statistics)にあるとほぼ確信できる場合は、統計情報の更新を行ってください。統計情報が古い場合（例えば、 `show stats_meta`の`modify count/row count`が特定の値（例えば0.3）より大きい場合や、テーブルに時間列のインデックスがある場合など）は、 `analyze table`を使用して復旧を試みることができます`auto analyze`設定されている場合は、システム変数`tidb_auto_analyze_ratio`大きすぎないか（例えば0.3より大きい場合）、および現在の時刻が`tidb_auto_analyze_start_time`から`tidb_auto_analyze_end_time`間であるかどうかを確認してください。

    -   その他の状況では、 [バグを報告する](https://github.com/pingcap/tidb/issues/new?labels=type%2Fbug&#x26;template=bug-report.md) 。

### 3.4 SQL実行エラー {#3-4-sql-execution-error}

-   3.4.1 クライアントが`ERROR 1265(01000) Data Truncated`エラーを報告します。これは、TiDBが`Decimal`型の精度を内部的に計算する方法がMySQLと互換性がないためです。この問題はv3.0.10 ( [＃14438](https://github.com/pingcap/tidb/pull/14438) )で修正されました。

    -   原因：

        MySQLでは、2つの大きな精度の`Decimal`除算し、結果が最大小数点精度（ `30` ）を超える場合、 `30`桁のみが予約され、エラーは報告されません。

        TiDB では計算結果は MySQL と同じですが、 `Decimal`表すデータ構造内では、小数精度のフィールドが実際の精度を保持します。

        `(0.1^30) / 10`例に挙げましょう。TiDB と MySQL ではどちらも`0`なります。これは、精度が最大`30`であるためです。しかし、TiDB では小数点精度のフィールドは依然として`31`です。

        `Decimal`除算を複数回実行すると、結果が正しいにもかかわらず、この精度フィールドがどんどん大きくなり、最終的にTiDB（ `72` ）のしきい値を超え、 `Data Truncated`エラーが報告されます。

        `Decimal`の乗算では、範囲外が回避され、精度が最大精度制限に設定されるため、この問題は発生しません。

    -   解決策: `a`と`b`ターゲット精度である場合に、手動で`Cast(xx as decimal(a, b))`追加することでこの問題を回避できます。

### 3.5 クエリの遅延の問題 {#3-5-slow-query-issues}

遅いクエリを特定するには[遅いクエリを特定する](/identify-slow-queries.md)参照してください。遅いクエリを分析して処理するには[遅いクエリを分析する](/analyze-slow-queries.md)参照してください。

### 3.6 ホットスポットの問題 {#3-6-hotspot-issues}

分散データベースであるTiDBは、アプリケーションの負荷を異なるコンピューティングノードまたはstorageノードに可能な限り均等に分散し、サーバーリソースをより有効に活用する負荷分散メカニズムを備えています。しかし、特定のシナリオでは、一部のアプリケーションの負荷が適切に分散されず、パフォーマンスに影響を与え、ホットスポットと呼ばれる高負荷の単一ポイントが形成される可能性があります。

TiDBは、ホットスポットのトラブルシューティング、解決、または回避のための包括的なソリューションを提供します。負荷ホットスポットを分散することで、QPSの向上やレイテンシーの削減など、全体的なパフォーマンスを向上させることができます。詳細なソリューションについては、 [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)ご覧ください。

### 3.7 ディスクI/O使用率が高い {#3-7-high-disk-i-o-usage}

CPUボトルネックとトランザクション競合によるボトルネックのトラブルシューティング後もTiDBの応答速度が低下した場合は、I/Oメトリックをチェックして、現在のシステムボトルネックを特定する必要があります。TiDBにおけるI/O使用率の上昇の問題を特定し、対処する方法については、 [ディスクI/O使用率が高い場合のトラブルシューティング](/troubleshoot-high-disk-io.md)参照してください。

### 3.8 ロックの競合 {#3-8-lock-conflicts}

TiDBは完全な分散トランザクションをサポートします。v3.0以降、TiDBは楽観的トランザクションモードと悲観的トランザクションモードを提供します。ロック関連の問題のトラブルシューティング方法、および楽観的と悲観的ロックの競合の処理方法については、 [ロックの競合のトラブルシューティング](/troubleshoot-lock-conflicts.md)参照してください。

### 3.9 データとインデックスの不整合 {#3-9-inconsistency-between-data-and-indexes}

TiDBは、トランザクションまたは[`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md)ステートメントを実行する際に、データとインデックス間の整合性をチェックします。チェックの結果、レコードのキー値と対応するインデックスのキー値に不整合がある場合、つまり、行データを格納するキー値ペアとそのインデックスを格納するキー値ペアに不整合がある場合（たとえば、インデックスが多すぎる、またはインデックスが欠落している）、TiDBはデータ不整合エラーを報告し、関連するエラーをエラーログに出力。

不整合エラーの詳細とチェックをバイパスする方法については、 [データとインデックス間の不整合のトラブルシューティング](/troubleshoot-data-inconsistency-errors.md)参照してください。

## 4. TiKVの問題 {#4-tikv-issues}

### 4.1 TiKVがパニックを起こし起動に失敗する {#4-1-tikv-panics-and-fails-to-start}

-   4.1.1 `sync-log = false` . マシンの電源を切った後に`unexpected raft log index: last_index X < applied_index Y`エラーが返されます。

    この問題は想定内です。1 `tikv-ctl`使用してリージョンを復元できます。

-   4.1.2 TiKV が仮想マシンに展開されている場合、仮想マシンが強制終了されるか物理マシンの電源がオフになると、エラー`entries[X, Y] is unavailable from storage`が報告されます。

    この問題は想定内です。仮想マシン`fsync`は信頼できないため、 `tikv-ctl`を使用してリージョンを復元する必要があります。

-   4.1.3 その他の予期せぬ原因の場合、 [バグを報告する](https://github.com/tikv/tikv/issues/new?template=bug-report.md) .

### 4.2 TiKV OOM {#4-2-tikv-oom}

-   4.2.1 `block-cache`構成が大きすぎると、OOM が発生する可能性があります。

    問題の原因を確認するには、モニター**Grafana** -&gt; **TiKV-details**で対応するインスタンスを選択して、RocksDB の`block cache size`確認します。

    同時に、パラメータ`[storage.block-cache] capacity = # "1GB"`が正しく設定されているかどうかを確認してください。デフォルトでは、TiKVの`block-cache`マシンの総メモリの`45%`に設定されています。コンテナにTiKVをデプロイする際には、このパラメータを明示的に指定する必要があります。TiKVは物理マシンのメモリを取得するため、コンテナのメモリ制限を超える可能性があります。

-   4.2.2コプロセッサーは多数の大きなクエリを受信し、大量のデータを返します。gRPC はコプロセッサがデータを返すのと同じ速さでデータを送信できず、OOM が発生します。

    原因を確認するには、モニター**Grafana** -&gt; **TiKV-details** -&gt; **coprocessor overview**を表示して、 `response size` `network outbound`トラフィックを超えているかどうかを確認できます。

-   4.2.3 他のコンポーネントが大量のメモリを占有します。

    この問題は予期せぬものです。1 [バグを報告する](https://github.com/tikv/tikv/issues/new?template=bug-report.md)実行できます。

### 4.3 クライアントが<code>server is busy</code>というエラーを報告する {#4-3-the-client-reports-the-code-server-is-busy-code-error}

モニター**Grafana** -&gt; **TiKV** -&gt; **errors**を表示して、ビジー状態の具体的な原因を確認します。7 `server is busy` 、TiKV のフロー制御メカニズムによって発生し、TiKV の負荷が現在高すぎるため後で再試行することを`tidb/ti-client`通知します。

-   4.3.1 TiKV RocksDB の遭遇`write stall` 。

    TiKV インスタンスには 2 つの RocksDB インスタンスがあり、1 つはRaftログを保存するために`data/raft`に、もう 1 つは実際のデータを保存するために`data/db`にあります。ログで`grep "Stalling" RocksDB`実行すると、ストールの具体的な原因を確認できます。RocksDB ログは`LOG`で始まるファイルで、 `LOG`現在のログです。 `write stall` RocksDB にネイティブに組み込まれているパフォーマンス低下メカニズムです。RocksDB で`write stall`発生すると、システム パフォーマンスが大幅に低下します。v5.2.0 より前のバージョンでは、TiDB は`write stall`に遭遇すると`ServerIsBusy`エラーを直接クライアントに返すことで、すべての書き込み要求をブロックしようとしていましたが、これにより QPS パフォーマンスが急激に低下する可能性がありました。v5.2.0 以降、TiKV は、 `write stall`が発生したときに`server is busy`クライアントに返す以前のメカニズムに代わる、スケジューリングレイヤーで書き込み要求を動的に遅らせることで書き込みを抑制する新しいフロー制御メカニズムを導入しています。新しいフロー制御メカニズムはデフォルトで有効になっており、TiKVは`KvDB`と`RaftDB` （memtableを除く）に対して`write stall`メカニズムを自動的に無効にします。ただし、保留中のリクエスト数が一定のしきい値を超えると、フロー制御メカニズムは引き続き有効になり、一部またはすべての書き込みリクエストを拒否し、クライアントに`server is busy`エラーを返します。詳細な説明としきい値については、 [フロー制御設定](/tikv-configuration-file.md#storageflow-control)参照してください。

    -   保留中の圧縮バイトが多すぎるために`server is busy`エラーが発生した場合は、 [`soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit)および[`hard-pending-compaction-bytes-limit`](/tikv-configuration-file.md#hard-pending-compaction-bytes-limit)パラメータの値を増やすことでこの問題を軽減できます。

        -   保留中の圧縮バイト数がパラメータ`soft-pending-compaction-bytes-limit` （デフォルトでは`192GiB` ）に達すると、フロー制御メカニズムは一部の書き込み要求を拒否し始めます（クライアントに`ServerIsBusy`返します）。この場合、このパラメータの値を`[storage.flow-control] soft-pending-compaction-bytes-limit = "384GiB"`など、増やすことができます。

        -   保留中の圧縮バイト数がパラメータ`hard-pending-compaction-bytes-limit` （デフォルトは`1024GiB` ）に達すると、フロー制御メカニズムはすべての書き込み要求を拒否し始めます（クライアントに`ServerIsBusy`返します）。このシナリオは、しきい値`soft-pending-compaction-bytes-limit`に達するとフロー制御メカニズムが介入して書き込み速度を低下させるため、発生する可能性は低くなります。このようなシナリオが発生した場合は、このパラメータの値を`[storage.flow-control] hard-pending-compaction-bytes-limit = "2048GiB"`に増やすことができます。

        -   ディスクI/O容量が長時間書き込みに追いつかない場合は、ディスクのスケールアップをお勧めします。ディスクスループットが上限に達し書き込みが停止する場合（例えば、SATA SSDがNVME SSDよりも大幅に低い場合）、CPUリソースが十分であれば、より高い圧縮率の圧縮アルゴリズムを適用できます。これにより、CPUリソースがディスクリソースに引き継がれ、ディスクへの負荷が軽減されます。

        -   デフォルトの CF 圧縮で高圧が発生する場合は、 `[rocksdb.defaultcf] compression-per-level`パラメータを`["no", "no", "lz4", "lz4", "lz4", "zstd", "zstd"]`から`["no", "no", "zstd", "zstd", "zstd", "zstd", "zstd"]`に変更します。

    -   メモリテーブルが多すぎるとストールが発生します。これは通常、インスタントライトの量が多く、メモリテーブルのディスクへのフラッシュが遅い場合に発生します。ディスク書き込み速度を改善できず、この問題がビジネスピーク時にのみ発生する場合は、対応するCFの`max-write-buffer-number`増やすことで軽減できます。

        -   例えば、 `[rocksdb.defaultcf] max-write-buffer-number`を`8` （デフォルトは`5` ）に設定します。この場合、メモリ内のメモリテーブルが増えるため、ピーク時のメモリ使用量が増加する可能性があることに注意してください。

-   4.3.2 `scheduler too busy`

    -   深刻な書き込み競合が発生しています。1 `latch wait duration`高い値です。モニター**「Grafana」** → **「TiKV詳細」** → **「scheduler prewrite** / **Scheduler commit」**で`latch wait duration`確認できます。スケジューラに書き込みタスクが蓄積されると、保留中の書き込みタスクが`[storage] scheduler-pending-write-threshold`で設定した閾値（100MB）を超えます`MVCC_CONFLICT_COUNTER`に対応するメトリックを確認することで、原因を確認できます。

    -   書き込み速度が遅いため、書き込みタスクが山積みになります。TiKVに書き込まれているデータが、 `[storage] scheduler-pending-write-threshold`で設定されたしきい値（100MB）を超えています。3 [4.5](#45-tikv-write-is-slow)参照してください。

-   4.3.3 `raftstore is busy` . メッセージの処理速度が受信速度よりも遅い。短期的なステータス`channel full`はサービスに影響しませんが、エラーが長時間続くと、Leaderの切り替えが発生する可能性があります。

    -   エンカウンター数`append log` [4.3.1](#43-the-client-reports-the-server-is-busy-error)参照。
    -   `append log duration`が高いため、メッセージの処理が遅くなります。4 `append log duration`高い理由を分析するには、 [4.5](#45-tikv-write-is-slow)を参照してください。
    -   raftstore は大量のメッセージを瞬時に受信し（TiKV Raftメッセージダッシュボードで確認できます）、処理に失敗します。通常、短期的なステータス`channel full`サービスに影響を与えません。

-   4.3.4 TiKVコプロセッサがキューに入っています。蓄積されているタスク数が`coprocessor threads * readpool.coprocessor.max-tasks-per-worker-[normal|low|high]`超えてい[3.3](#33-wrong-execution-plan) 。大規模なクエリが多すぎると、コプロセッサにタスクが蓄積されます。実行プランの変更によって大量のテーブルスキャン操作が発生していないか確認する必要があります。3を参照してください。

### 4.4 一部のTiKVノードが頻繁にLeaderをドロップする {#4-4-some-tikv-nodes-drop-leader-frequently}

-   4.4.1 TiKVの再開による再選挙

    -   TiKVがパニック状態になった後、systemdによって引き上げられ、正常に動作します。panicが発生したかどうかは、TiKVのログを確認することで確認できます。この問題は予期せぬものであるため、発生した場合は[バグを報告する](https://github.com/tikv/tikv/issues/new?template=bug-report.md) 。

    -   TiKV がサードパーティによって停止または強制終了され、その後 systemd によってプルアップされました。1 `dmesg` TiKV ログを確認して原因を確認してください。

    -   TiKVはOOMであり、再起動が発生します[4.2](#42-tikv-oom)を参照してください。

    -   TiKVは、動的調整`THP` （Transparent Hugepage）が原因でハングアップしています。中国語のケース[ケース500](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case500.md)ご覧ください。

-   4.4.2 TiKV RocksDB が書き込みストールに遭遇し、再選出が行われます。モニター**Grafana** -&gt; **TiKV-details** -&gt; **errors**に`server is busy`表示されているか確認してください[4.3.1](#43-the-client-reports-the-server-is-busy-error)を参照してください。

-   4.4.3 ネットワーク分離による再選。

### 4.5 TiKVの書き込みが遅い {#4-5-tikv-write-is-slow}

-   4.5.1 TiKV gRPCの`prewrite/commit/raw-put`期間を表示して、TiKV書き込みが遅いかどうかを確認します（RawKVクラスターのみ）。一般的に、 [パフォーマンスマップ](https://github.com/pingcap/tidb-map/blob/master/maps/performance-map.png)に基づいて遅いフェーズを特定できます。よくある状況を以下に示します。

-   4.5.2 スケジューラ CPU がビジー状態です (トランザクション kv の場合のみ)。

    プレライト/コミットの`scheduler command duration`が`scheduler latch wait duration`と`storage async write duration`の合計よりも長いです。スケジューラワーカーのCPU需要が高い（例えば`scheduler-worker-pool-size` * 100% の 80% を超える）か、マシン全体のCPUリソースが比較的限られている可能性があります。書き込みワークロードが大きい場合は、 `[storage] scheduler-worker-pool-size`設定が小さすぎないか確認してください。

    その他の状況では、 [バグを報告する](https://github.com/tikv/tikv/issues/new?template=bug-report.md) 。

-   4.5.3 ログの追加が遅い。

    TiKV Grafanaの**Raft IO** / `append log duration`値が高い場合、通常はディスク書き込み操作が遅いことが原因です。RocksDB - raftの`WAL Sync Duration max`値を確認することで原因を確認できます。

    その他の状況では、 [バグを報告する](https://github.com/tikv/tikv/issues/new?template=bug-report.md) 。

-   4.5.4 raftstore スレッドがビジー状態です。

    **Raft Propose** / `propose wait duration`は、TiKV Grafana のログ追加期間よりも大幅に長くなります。以下の方法を試してください。

    -   設定値`[raftstore] store-pool-size`が小さすぎないか確認してください。3～ `1` `5`間で、大きすぎない値を設定することを推奨します。
    -   マシン上の CPU リソースが不足していないかどうかを確認します。

-   4.5.5 適用が遅い。

    TiKV Grafana の**Raft IO** / `apply log duration`値が高くなっています。これは通常、 **Raft Propose** / `apply wait duration`値も高いことを意味します。考えられる原因は以下のとおりです。

    -   `[raftstore] apply-pool-size`は小さすぎます ( `1`から`5`間で大きすぎない値を設定することを推奨します)、また、 **Thread CPU** / `apply CPU`は大きすぎます。

    -   マシン上の CPU リソースが不足しています。

    -   リージョン書き込みのホットスポット。単一の適用スレッドのCPU使用率が高くなります。現在、単一のリージョンにおけるホットスポット問題を適切に解決できていませんが、改善に向けて取り組んでいます。各スレッドのCPU使用率を確認するには、Grafana式に`by (instance, name)`追加してください。

    -   RocksDBへの書き込みが遅いです。RocksDB**のkv** / `max write duration`が高くなっています。1つのRaftログに複数のKVが含まれる場合があります。RocksDBへの書き込みでは、128個のKVが1回の書き込みバッチでRocksDBに書き込まれます。そのため、適用ログがRocksDBへの複数の書き込みに関連付けられている可能性があります。

    -   その他の状況では、 [バグを報告する](https://github.com/tikv/tikv/issues/new?template=bug-report.md) 。

-   4.5.6 Raftコミット ログが遅い。

    TiKV Grafanaの**Raft IO** / `commit log duration`は高い値です（この指標はGrafana v4.x以降でのみサポートされています）。各リージョンは独立したRaftグループに対応しています。Raftには、TCPのスライディングウィンドウ機構に似たフロー制御機構があります。スライディングウィンドウのサイズは、パラメータ`[raftstore] raft-max-inflight-msgs = 256`設定することで制御できます。書き込みホットスポットがあり、パラメータ`commit log duration`値が高い場合は、パラメータを`1024`に増やすなど調整できます。

-   4.5.7 その他の状況については、 [パフォーマンスマップ](https://github.com/pingcap/tidb-map/blob/master/maps/performance-map.png)の書き込みパスを参照して原因を分析します。

## 5. PDの問題 {#5-pd-issues}

### 5.1 PDスケジュール {#5-1-pd-scheduling}

-   5.1.1 マージ

    -   テーブル間の空領域は結合できません。TiKVの`[coprocessor] split-region-on-table`パラメータを変更する必要があります。v4.xではデフォルトで`false`に設定されています。中国語版は[ケース896](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case896.md)参照してください。

    -   リージョンのマージが遅いです。Grafana -&gt; **PD** -&gt;**オペレーター**の**モニター**ダッシュボードにアクセスして、マージされたオペレーターが生成されているかどうかを確認できます。マージを高速化するには、値を`merge-schedule-limit`に増やしてください。

-   5.1.2 レプリカを追加する、またはレプリカをオンライン/オフラインにする

    -   TiKVディスクが容量の80%を使用しており、PDはレプリカを追加していません。この状況では、ミスピアの数が増加するため、TiKVをスケールアウトする必要があります。中国語の[ケース801](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case801.md)参照してください。

    -   TiKVノードがオフラインになると、一部のリージョンを他のノードに移行できなくなります。この問題はv3.0.4（ [＃5526](https://github.com/tikv/tikv/pull/5526) ）で修正されました。中国語版は[ケース870](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case870.md)ご覧ください。

-   5.1.3 バランス

    -   Leader/ リージョン の数が均等に配分されていません。中国語版では[ケース394](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case394.md)と[ケース759](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case759.md)参照してください。主な原因は、Balance がリージョン/ Leaderのサイズに基づいてスケジューリングを実行するため、数が均等に配分されない可能性があることです。TiDB 4.0 では、 `[leader-schedule-policy]`パラメータが導入され、 Leaderのスケジューリングポリシーを`count`ベースまたは`size`ベースに設定できるようになりました。

### 5.2 PD選挙 {#5-2-pd-election}

-   5.2.1 PD はLeaderを切り替えます。

    -   原因1：ディスク。PDノードが配置されているディスクのI/O負荷が最大になっています。PDノードが、I/O需要の高い他のコンポーネントと同時にデプロイされているかどうか、またディスクの健全性を確認してください。Grafanaのモニターメトリクス（**ディスクパフォ​​ーマンス**、**レイテンシー**/**負荷**）を確認することで原因を確認できます。必要に応じて、FIOツールを使用してディスクのチェック**を**実行することもできます。中国語版は[ケース292](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case292.md)ご覧ください。

    -   原因2：ネットワーク。PDログに`lost the TCP streaming connection`表示されています。PDノード間のネットワークに問題がないか確認し、 **Grafana** -&gt; **PD** -&gt; **etcd**モニターの`round trip`確認して原因を特定する必要があります。中国語版は[ケース177](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case177.md)ご覧ください。

    -   原因3：システム負荷が高い。ログには`server is likely overloaded`表示されています。中国語では[ケース214](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case214.md)参照してください。

-   5.2.2 PD がLeaderを選出できない、または選出が遅い。

    -   PDがLeaderを選出できません：PDログには`lease is not expired`表示されています。3 [この号](https://github.com/etcd-io/etcd/issues/10355) v3.0.xおよびv2.1.19で修正されました。中国語版は[ケース875](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case875.md)ご覧ください。

    -   選挙が遅い：リージョンの読み込み時間が長いです。この問題は、PDログで`grep "regions cost"`実行することで確認できます。結果が`load 460927 regions cost 11.77099s`秒など秒単位の場合、リージョンの読み込みが遅いことを意味します。v3.0では、 `use-region-storage`を`true`に設定することで`region storage`機能を有効にでき、リージョンの読み込み時間を大幅に短縮できます。中国語版は[ケース429](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case429.md)ご覧ください。

-   5.2.3 TiDB が SQL ステートメントを実行すると PD がタイムアウトします。

    -   PDにLeaderがいない、またはLeaderが切り替わりました。1と[5.2.1](#52-pd-election) [5.2.2](#52-pd-election)参照してください。

    -   ネットワークの問題です。モニター**Grafana** -&gt; **blackbox_exporter** -&gt; **レイテンシー**にアクセスして、TiDBからPDLeaderへのネットワークが正常に動作しているかどうかを確認してください。

    -   PDはパニックになる[バグを報告する](https://github.com/pingcap/pd/issues/new?labels=kind%2Fbug&#x26;template=bug-report.md) 。

    -   PDは[5.3](#53-pd-oom)です。1を参照してください。

    -   問題に他の原因がある場合は、 `curl http://127.0.0.1:2379/debug/pprof/goroutine?debug=2`と[バグを報告する](https://github.com/pingcap/pd/issues/new?labels=kind%2Fbug&#x26;template=bug-report.md)実行して goroutine を取得します。

-   5.2.4 その他の問題

    -   PDは`FATAL`エラーを報告していますが、ログには`range failed to find revision pair`表示されています。この問題はv3.0.8（ [＃2040](https://github.com/pingcap/pd/pull/2040) ）で修正されました。詳細は中国語版[ケース947](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case947.md)ご覧ください。

    -   その他の状況では、 [バグを報告する](https://github.com/pingcap/pd/issues/new?labels=kind%2Fbug&#x26;template=bug-report.md) 。

### 5.3 PD OOM {#5-3-pd-oom}

-   5.3.1 `/api/v1/regions`インターフェースを使用する場合、リージョンが多すぎるとPD OOMが発生する可能性があります。この問題はv3.0.8 ( [＃1986](https://github.com/pingcap/pd/pull/1986) ) で修正されました。

-   5.3.2 ローリングアップグレード中のPD OOM。gRPCメッセージのサイズに制限がなく、モニターではTCP InSegsが比較的大きいことが示されています。この問題はv3.0.6（ [＃1952](https://github.com/pingcap/pd/pull/1952) ）で修正されました。 <!--For details, see [case-852](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case852.md).-->

### 5.4 Grafana ディスプレイ {#5-4-grafana-display}

-   5.4.1 **Grafana** -&gt; **PD** -&gt;**クラスター**-&gt;**ロール**のモニターにフォロワーが表示されます。Grafana 式の問題は v3.0.8 で修正されました。

## 6. エコシステムツール {#6-ecosystem-tools}

### 6.1 TiDBBinlog {#6-1-tidb-binlog}

-   6.1.1 TiDB Binlogは、TiDBからの変更を収集し、下流のTiDBまたはMySQLプラットフォームへのバックアップとレプリケーションを提供するツールです。詳細については、 [GitHub 上の TiDBBinlog](https://github.com/pingcap/tidb-binlog)参照してください。

-   6.1.2Pump/Drainerステータスの`Update Time`正常に更新され、ログに異常は表示されませんが、下流にデータが書き込まれません。

    -   TiDB設定でBinlogが有効になっていません。TiDBの`[binlog]`設定を変更してください。

-   6.1.3 Drainerの`sarama` `EOF`エラーを報告します。

    -   Drainerの Kafka クライアントのバージョンが Kafka のバージョンと一致していません。1 `[syncer.to] kafka-version`設定を変更する必要があります。

-   6.1.4 Drainer がKafka への書き込みに失敗してパニックになり、Kafka が`Message was too large`エラーを報告します。

    -   binlogデータが大きすぎるため、Kafka に書き込まれる単一のメッセージが大きすぎます。Kafka の以下の設定を変更する必要があります。

        ```properties
        message.max.bytes=1073741824
        replica.fetch.max.bytes=1073741824
        fetch.message.max.bytes=1073741824
        ```

        詳細は中国語版[ケース789](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case789.md)ご覧ください。

-   6.1.5 上流と下流のデータの不一致

    -   一部のTiDBノードではbinlogが有効になっていません。v3.0.6以降のバージョンでは、 [http://127.0.0.1:10080/info/all](http://127.0.0.1:10080/info/all)インターフェースにアクセスすることで全ノードのbinlogステータスを確認できます。v3.0.6より前のバージョンでは、設定ファイルを表示することでbinlogステータスを確認できます。

    -   一部のTiDBノードは`ignore binlog`ステータスになります。v3.0.6以降のバージョンでは、 [http://127.0.0.1:10080/info/all](http://127.0.0.1:10080/info/all)インターフェースにアクセスすることで、すべてのノードのbinlogステータスを確認できます。v3.0.6より前のバージョンでは、TiDBログにキーワード`ignore binlog`が含まれているかどうかを確認してください。

    -   タイムスタンプ列の値がアップストリームとダウンストリームで一致していません。

        -   これはタイムゾーンの違いが原因です。Drainerが上流および下流のデータベースと同じタイムゾーンにあることを確認する必要があります。Drainerはタイムゾーンを`/etc/localtime`から取得し、環境変数`TZ`サポートしていません。中国語版の[ケース826](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case826.md)参照してください。

        -   TiDBではtimestampのデフォルト値は`null`ですが、 MySQL 5.7 （MySQL 8を除く）では同じデフォルト値が現在時刻です。そのため、上流のTiDBのtimestampが`null`で、下流がMySQL 5.7の場合、timestamp列のデータが不整合になります。binlogを有効にする前に、上流で`set @@global.explicit_defaults_for_timestamp=on;`実行する必要があります。

    -   その他の状況では、 [バグを報告する](https://github.com/pingcap/tidb-binlog/issues/new?labels=bug&#x26;template=bug-report.md) 。

-   6.1.6 遅いレプリケーション

    -   ダウンストリームはTiDB/MySQLで、アップストリームは頻繁にDDL操作を実行します。中国語版は[ケース1023](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case1023.md)ご覧ください。

    -   下流はTiDB/MySQLであり、レプリケート対象のテーブルには主キーとユニークインデックスが設定されていないため、 binlogのパフォーマンスが低下します。主キーまたはユニークインデックスを追加することをお勧めします。

    -   ダウンストリームがファイルに出力する場合は、出力ディスクまたはネットワーク ディスクが遅いかどうかを確認します。

    -   その他の状況では、 [バグを報告する](https://github.com/pingcap/tidb-binlog/issues/new?labels=bug&#x26;template=bug-report.md) 。

-   6.1.7Pumpはbinlogを書き込むことができず、エラー`no space left on device`を報告します。

    -   Pumpがbinlogデータを正常に書き込むには、ローカルディスクの空き容量が不足しています。ディスク容量をクリーンアップしてから、 Pumpを再起動する必要があります。

-   6.1.8Pumpは起動時にエラー`fail to notify all living drainer`を報告します。

    -   原因: Pumpが起動すると、状態`online`にあるすべてのDrainerノードに通知が送信されます。Drainerへの通知に失敗した場合、このエラーログが出力されます。

    -   解決策：binlogctlツールを使用して、各Drainerノードが正常かどうかを確認します。これは、状態`online`にあるすべてのDrainerノードが正常に動作していることを確認するためです。Drainerノードの状態が実際の動作状態と一致していない場合は、binlogctlツールを使用して状態を変更し、 Pumpを再起動してください。ケース[すべての生きている排水装置に通知できなかった](/tidb-binlog/handle-tidb-binlog-errors.md#fail-to-notify-all-living-drainer-is-returned-when-pump-is-started)参照してください。

-   6.1.9Drainerは`gen update sqls failed: table xxx: row data is corruption []`エラーを報告します。

    -   トリガー: アップストリームは`DROP COLUMN` DDLを実行しながら、このテーブルに対してDML操作を実行します。この問題はv3.0.6で修正されました。中国語版は[ケース820](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case820.md)ご覧ください。

-   6.1.10Drainerのレプリケーションがハングします。プロセスはアクティブなままですが、チェックポイントは更新されません。

    -   この問題はv3.0.4で修正されました。中国語版は[ケース741](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case741.md)ご覧ください。

-   6.1.11 いずれかのコンポーネントがパニックになります。

    -   [バグを報告する](https://github.com/pingcap/tidb-binlog/issues/new?labels=bug&#x26;template=bug-report.md) 。

### 6.2 データ移行 {#6-2-data-migration}

-   6.2.1 TiDB Data Migration (DM) は、MySQL/MariaDB から TiDB へのデータ移行をサポートする移行ツールです。詳細については、 [DMの概要](/dm/dm-overview.md)参照してください。

-   6.2.2 `Access denied for user 'root'@'172.31.43.27' (using password: YES)` `query status`実行したとき、またはログを確認したときに表示されます。

    -   すべてのDM設定ファイル内のデータベース関連のパスワードは、 `dmctl`で暗号化する必要があります。データベースパスワードが空の場合は、パスワードを暗号化する必要はありません。v1.0.6以降では、平文パスワードを使用できます。
    -   DM操作中は、上流データベースと下流データベースのユーザーには、対応する読み取り権限と書き込み権限が必要です。データ移行は、データレプリケーションタスクの開始時に自動的に[対応する権限を事前チェックする](/dm/dm-precheck.md) 。
    -   DM クラスターに DM-worker/DM-master/dmctl の異なるバージョンをデプロイするには、中国語の[AskTUGのケーススタディ](https://asktug.com/t/dm1-0-0-ga-access-denied-for-user/1049/5)参照してください。

-   6.2.3 レプリケーション タスクが中断され、 `driver: bad connection`エラーが返されます。

    -   エラー`driver: bad connection`は、DM と下流の TiDB データベース間の接続に異常 (ネットワーク障害や TiDB の再起動など) が発生し、現在のリクエストのデータがまだ TiDB に送信されていないことを示します。

        -   DM 1.0.0 GA より前のバージョンの場合は、 `stop-task`実行してタスクを停止し、 `start-task`を実行してタスクを再開します。
        -   DM 1.0.0 GA以降のバージョンでは、このタイプのエラーに対する自動再試行メカニズムが追加されています[＃265](https://github.com/pingcap/dm/pull/265)参照してください。

-   6.2.4 レプリケーション タスクが`invalid connection`エラーで中断されます。

    -   `invalid connection`エラーは、DMと下流TiDBデータベース間の接続に異常（ネットワーク障害、TiDBの再起動、TiKVのビジー状態など）が発生し、現在のリクエストのデータの一部がTiDBに送信されたことを示します。DMはレプリケーションタスクにおいて下流へのデータのレプリケーションを並行して行う機能を備えているため、タスクが中断されると複数のエラーが発生する可能性があります。これらのエラーは、 `query-status`または`query-error`実行することで確認できます。

        -   増分レプリケーション プロセス中に`invalid connection`エラーのみが発生した場合、DM はタスクを自動的に再試行します。
        -   DM が再試行しない、またはバージョンの問題により自動的に再試行できない場合 (自動再試行は v1.0.0-rc.1 で導入されています)、 `stop-task`使用してタスクを停止し、 `start-task`使用してタスクを再起動します。

-   6.2.5 リレーユニットがエラー`event from * in * diff from passed-in event *`報告するか、またはレプリケーションタスクが`get binlog error ERROR 1236 (HY000) and binlog checksum mismatch, data may be corrupted returned`などのbinlogの取得または解析に失敗するエラーで中断されます。

    -   DM がリレー ログまたは増分レプリケーションをプルするプロセス中に、アップストリームbinlogファイルのサイズが 4 GB を超えると、この 2 つのエラーが発生する可能性があります。

    -   原因：リレーログを書き込む際、DMはbinlogの位置とbinlogファイルのサイズに基づいてイベント検証を行い、複製されたbinlogの位置をチェックポイントとして保存する必要があります。しかし、公式MySQLはbinlogの位置をuint32で保存するため、4GBを超えるbinlogファイルのbinlogの位置がオーバーフローし、上記のエラーが発生します。

    -   解決：

        -   リレー処理ユニットの場合、 [手動でレプリケーションを回復する](https://pingcap.com/docs/tidb-data-migration/dev/error-handling/#the-relay-unit-throws-error-event-from--in--diff-from-passed-in-event--or-a-replication-task-is-interrupted-with-failing-to-get-or-parse-binlog-errors-like-get-binlog-error-error-1236-hy000-and-binlog-checksum-mismatch-data-may-be-corrupted-returned) 。
        -   binlogレプリケーション処理単位の場合、 [手動でレプリケーションを回復する](https://pingcap.com/docs/tidb-data-migration/dev/error-handling/#the-relay-unit-throws-error-event-from--in--diff-from-passed-in-event--or-a-replication-task-is-interrupted-with-failing-to-get-or-parse-binlog-errors-like-get-binlog-error-error-1236-hy000-and-binlog-checksum-mismatch-data-may-be-corrupted-returned) 。

-   6.2.6 DMレプリケーションが中断され、ログに`ERROR 1236 (HY000) The slave is connecting using CHANGE MASTER TO MASTER_AUTO_POSITION = 1, but the master has purged binary logs containing GTIDs that the slave requires.`返される

    -   マスターbinlogが消去されているかどうかを確認します。
    -   `relay.meta`で記録した位置情報を確認します。

        -   `relay.meta`空のGTID情報を記録しました。DM-workerは終了時または30秒ごとに、このGTID情報をメモリの`relay.meta`に保存します。DM-workerが上流のGTID情報を取得できない場合は、空のGTID情報を`relay.meta`に保存します。中国語では[ケース772](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case772.md)参照してください。

        -   `relay.meta`で記録されたbinlogイベントにより、不完全リカバリプロセスがトリガーされ、誤った GTID 情報が記録されます。この問題は v1.0.2 で修正されていますが、それ以前のバージョンでも発生する可能性があります。 <!--See [case-764](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case764.md).-->

-   6.2.7 DMレプリケーションプロセスでエラー`Error 1366: incorrect utf8 value eda0bdedb29d(\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd)`返されます。

    -   この値はMySQL 8.0またはTiDBには正常に書き込めませんが、 MySQL 5.7には書き込めます。1パラメータ`tidb_skip_utf8_check`有効にすると、データ形式のチェックをスキップできます。

### 6.3 TiDB Lightning {#6-3-tidb-lightning}

-   6.3.1 TiDB Lightningは、大量のデータをTiDBクラスタに高速かつ完全にインポートするためのツールです。1 [GitHub 上のTiDB Lightning](https://github.com/pingcap/tidb/tree/release-8.1/lightning)参照してください。

-   6.3.2 インポート速度が遅すぎます。

    -   `region-concurrency`設定が高すぎると、スレッドの競合が発生し、パフォーマンスが低下します。トラブルシューティングには以下の 3 つの方法があります。

        -   設定は、ログの先頭から`region-concurrency`検索すると見つかります。
        -   TiDB Lightning が他のサービス (Importer など) とサーバーを共有する場合、そのサーバーの CPU コアの合計数の`region-concurrency` ～ 75% を手動で設定する必要があります。
        -   CPUにクォータ（例えばKubernetesの設定による制限）がある場合、 TiDB Lightningはそれを読み取れない可能性があります。この場合も、 `region-concurrency`手動で減らす必要があります。

    -   インデックスを追加するたびに、各行に新しいKVペアが作成されます。インデックスがN個ある場合、実際にインポートされるサイズは、 [Dumpling](/dumpling-overview.md)の出力のサイズの約(N+1)倍になります。インデックスが無視できるほど小さい場合は、まずスキーマからインデックスを削除し、インポート完了後に`CREATE INDEX`の方法で再度追加することができます。

    -   TiDB Lightningのバージョンが古いです。最新バージョンをお試しください。インポート速度が向上する可能性があります。

-   6.3.3 `checksum failed: checksum mismatched remote vs local` .

    -   原因1: テーブルに既にデータが含まれている可能性があります。これらの古いデータは最終的なチェックサムに影響を与える可能性があります。

    -   原因 2: ターゲット データベースのチェックサムが 0 の場合、つまり何もインポートされていない場合は、クラスターが過負荷になっていて、データの取り込みに失敗している可能性があります。

    -   原因3: データソースがマシンによって生成され、 [Dumpling](/dumpling-overview.md)によってバックアップされていない場合は、テーブルの制約が満たされていることを確認してください。例:

        -   `AUTO_INCREMENT`列は正の値である必要があり、値「0」は含まれません。
        -   UNIQUE KEY と PRIMARY KEY には重複するエントリがあってはなりません。

    -   解決策: [トラブルシューティングの解決策](/tidb-lightning/troubleshoot-tidb-lightning.md#checksum-failed-checksum-mismatched-remote-vs-local)参照してください。

-   6.3.4 `Checkpoint for … has invalid status:(error code)`

    -   原因: チェックポイントが有効になっており、Lightning/Importer が以前に異常終了しています。データ破損を防ぐため、エラーが解決されるまでTiDB Lightning は起動しません。エラーコードは 25 未満の整数で、 `0, 3, 6, 9, 12, 14, 15, 17, 18, 20 and 21`などの値になります。この整数は、インポートプロセスにおいて予期せぬ終了が発生したステップを示します。整数が大きいほど、終了が発生するまでの時間が遅くなります。

    -   解決策: [トラブルシューティングの解決策](/tidb-lightning/troubleshoot-tidb-lightning.md#checkpoint-for--has-invalid-status-error-code)参照してください。

-   6.3.5 `cannot guess encoding for input file, please convert to UTF-8 manually`

    -   原因: TiDB Lightning はUTF-8 と GB-18030 エンコーディングのみをサポートしています。このエラーは、ファイルがこれらのいずれのエンコーディングにも該当しないことを意味します。また、過去の ALTER TABLE 実行により、ファイルに UTF-8 の文字列と GB-18030 の文字列が混在しているなど、エンコーディングが混在している可能性もあります。

    -   解決策: [トラブルシューティングの解決策](/tidb-lightning/troubleshoot-tidb-lightning.md#cannot-guess-encoding-for-input-file-please-convert-to-utf-8-manually)参照してください。

-   6.3.6 `[sql2kv] sql encode error = [types:1292]invalid time format: '{1970 1 1 0 45 0 0}'`

    -   原因: タイムスタンプ型のエントリに存在しない時刻値が含まれています。これは、夏時間の変更、または時刻値がサポート範囲（1970年1月1日から2038年1月19日）を超えていることが原因です。

    -   解決策: [トラブルシューティングの解決策](/tidb-lightning/troubleshoot-tidb-lightning.md#sql2kv-sql-encode-error--types1292invalid-time-format-1970-1-1-)参照してください。

## 7. 共通ログ分析 {#7-common-log-analysis}

### 7.1 TiDB {#7-1-tidb}

-   7.1.1 `GC life time is shorter than transaction duration` .

    トランザクションの継続時間が GC の有効期間 (デフォルトでは 10 分) を超えています。

    システム変数[`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)変更することで、GCの有効期間を延ばすことができます。ただし、このパラメータを変更することは推奨されません。トランザクションに`UPDATE`と`DELETE`ステートメントが多数含まれる場合、このパラメータを変更すると古いバージョンが大量に蓄積される可能性があるためです。

-   7.1.2 `txn takes too much time` .

    このエラーは、長時間 (590 秒以上) コミットされていないトランザクションをコミットした場合に返されます。

    アプリケーションでこのような長時間のトランザクションを実行する必要がある場合は、 `[tikv-client] max-txn-time-use = 590`パラメータとGC有効期間を増やすことでこの問題を回避できます。アプリケーションでこのような長時間のトランザクション実行が必要かどうかを確認することをお勧めします。

-   7.1.3 `coprocessor.go`レポート`request outdated` 。

    このエラーは、TiKV に送信されたコプロセッサ要求が TiKV のキューで 60 秒以上待機している場合に返されます。

    TiKV コプロセッサが長いキューに入っている理由を調査する必要があります。

-   7.1.4 `region_cache.go` `switch region peer to next due to send request fail`という大きな数値を報告し、エラーメッセージは`context deadline exceeded`です。

    TiKV へのリクエストがタイムアウトし、リージョンキャッシュがトリガーされてリクエストが他のノードに切り替えられました。ログの`addr`のフィールドに対して`grep "<addr> cancelled`コマンドを引き続き実行し、 `grep`結果に応じて以下の手順を実行してください。

    -   `send request is cancelled` : 送信フェーズでリクエストがタイムアウトしました。Grafana -&gt; **TiDB** -&gt; **Batch Client** / `Pending Request Count by TiKV`**の**監視を調べて、保留中のリクエスト数が128を超えているかどうかを確認できます。

        -   128より大きい場合はKVの処理能力を超える送信となるため、送信が滞ってしまいます。
        -   値が 128 以下の場合は、ログをチェックして、レポートが対応する KV の操作および保守の変更によって発生したものかどうかを確認します。それ以外の場合、このエラーは予期しないものであり、 [バグを報告する](https://github.com/pingcap/tidb/issues/new?labels=type%2Fbug&#x26;template=bug-report.md)実行する必要があります。

    -   `wait response is cancelled` : リクエストはTiKVに送信された後、タイムアウトしました。対応するTiKVアドレスの応答時間と、その時点のリージョンのPDおよびKVログを確認する必要があります。

-   7.1.5 `distsql.go`レポート`inconsistent index` 。

    データインデックスに不整合があるようです。報告されたインデックスがあるテーブルでコマンド`admin check table <TableName>`を実行してください。チェックに失敗した場合は、次のコマンドを実行してガベージコレクションを無効にし、 [バグを報告する](https://github.com/pingcap/tidb/issues/new?labels=type%2Fbug&#x26;template=bug-report.md)実行します。

    ```sql
    SET GLOBAL tidb_gc_enable = 0;
    ```

### 7.2 TiKV {#7-2-tikv}

-   7.2.1 `key is locked` .

    読み取りと書き込みが競合しています。読み取り要求でコミットされていないデータが検出されたため、データがコミットされるまで待機する必要があります。

    このエラーが少数であればビジネスに影響はありませんが、このエラーが多数発生すると、ビジネスにおいて読み取りと書き込みの競合が深刻であることを示します。

-   7.2.2 `write conflict` .

    これは、楽観的トランザクションにおける書き込み競合です。複数のトランザクションが同じキーを変更した場合、1つのトランザクションだけが成功し、他のトランザクションは自動的にタイムスタンプを再度取得して操作を再試行するため、ビジネスへの影響はありません。

    競合が深刻な場合、複数回の再試行後にトランザクションが失敗する可能性があります。この場合、悲観的ロックの使用をお勧めします。エラーの詳細と解決策については、 [楽観的トランザクションにおける書き込み競合のトラブルシューティング](/troubleshoot-write-conflicts.md)参照してください。

-   7.2.3 `TxnLockNotFound` .

    このトランザクションのコミットは遅すぎるため、Time To Live（TTL）の経過後に他のトランザクションによってロールバックされます。このトランザクションは自動的に再試行されるため、通常は業務に影響はありません。0.25MB以下のトランザクションの場合、デフォルトのTTLは3秒です。詳細については、 [`LockNotFound`エラー](/troubleshoot-lock-conflicts.md#locknotfound-error)ご覧ください。

-   7.2.4 `PessimisticLockNotFound` .

    `TxnLockNotFound`と同様です。悲観的トランザクションのコミットが遅すぎるため、他のトランザクションによってロールバックされます。

-   7.2.5 `stale_epoch` .

    リクエストのエポックが古いため、TiDBはルーティングを更新した後、リクエストを再送信します。業務への影響はありません。エポックは、リージョンで分割/結合操作が行われた場合、またはレプリカが移行された場合に変更されます。

-   7.2.6 `peer is not leader` .

    リクエストはLeaderではないレプリカに送信されました。エラー応答でどのレプリカが最新のLeaderであるかが示されている場合、TiDB はエラーに応じてローカルルーティングを更新し、最新のLeaderに新しいリクエストを送信します。通常、業務に影響はありません。

    v3.0以降のバージョンでは、TiDBは前のLeaderへのリクエストが失敗すると他のピアへのリクエストを試みます。そのため、TiKVログに`peer is not leader`頻繁に記録される可能性があります。送信失敗の根本原因を特定するには、TiDBの該当リージョンの`switch region peer to next due to send request fail`ログを確認してください。詳細は[7.1.4](#71-tidb)を参照してください。

    このエラーは、他の理由によりリージョンにLeaderがいない場合にも返される可能性があります。詳細については、 [4.4](#44-some-tikv-nodes-drop-leader-frequently)参照してください。
