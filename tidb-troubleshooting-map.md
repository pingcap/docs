---
title: TiDB Troubleshooting Map
summary: TiDB の一般的なエラーをトラブルシューティングする方法を学びます。
---

# TiDB トラブルシューティング マップ {#tidb-troubleshooting-map}

このドキュメントでは、TiDB およびその他のコンポーネントの一般的な問題をまとめています。関連する問題が発生した場合、このマップを使用して問題を診断し、解決することができます。

## 1. サービスが利用できない {#1-service-unavailable}

### 1.1 クライアントが<code>Region is Unavailable</code> 」というエラーを報告する {#1-1-the-client-reports-code-region-is-unavailable-code-error}

-   1.1.1 `Region is Unavailable`エラーは通常、一定期間リージョンが利用できないために発生します。 `TiKV server is busy`発生するか、 `not leader`または`epoch not match`原因で TiKV へのリクエストが失敗するか、TiKV へのリクエストがタイムアウトします。このような場合、TiDB は`backoff`再試行メカニズムを実行します。 `backoff`がしきい値 (デフォルトでは 20 秒) を超えると、エラーがクライアントに送信されます。 `backoff`しきい値内では、このエラーはクライアントには表示されません。

-   1.1.2 複数の TiKV インスタンスが同時に OOM になり、OOM 期間中にLeaderが存在しなくなります。中国語では[ケース991](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case991.md)参照してください。

-   1.1.3 TiKV は`TiKV server is busy`報告し、 `backoff`回数を超えています。詳細については、 [4.3](#43-the-client-reports-the-server-is-busy-error)を参照してください。 `TiKV server is busy`内部フロー制御メカニズムの結果であり、 `backoff`回数にはカウントされません。この問題は修正される予定です。

-   1.1.4 複数の TiKV インスタンスの起動に失敗し、リージョンにLeaderが存在しない状態になります。物理マシンに複数の TiKV インスタンスがデプロイされている場合、ラベルが適切に構成されていないと、物理マシンの障害によりリージョンにLeaderが存在しない状態になる可能性があります。中国語の[ケース228](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case228.md)参照してください。

-   1.1.5Followerの適用が前のエポックで遅れている場合、FollowerがLeaderになった後、 `epoch not match`で要求を拒否します。 中国語では[ケース-958](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case958.md)参照してください (TiKV はメカニズムを最適化する必要があります)。

### 1.2 PDエラーによりサービスが利用できなくなる {#1-2-pd-errors-cause-service-unavailable}

[5 PDの問題](#5-pd-issues)を参照してください。

## 2. レイテンシーが大幅に増加する {#2-latency-increases-significantly}

### 2.1 一時的な増加 {#2-1-transient-increase}

-   2.1.1 間違った TiDB 実行プランによりレイテンシーが増加します。 [3.3](#33-wrong-execution-plan)を参照してください。
-   2.1.2 PDLeader選挙問題またはOOM。1と[5.2](#52-pd-election) [5.3](#53-pd-oom)参照してください。
-   2.1.3 一部の TiKV インスタンスで多数のLeaderがドロップします。1 [4.4](#44-some-tikv-nodes-drop-leader-frequently)参照してください。
-   2.1.4 その他の原因については[読み取りおよび書き込み遅延の増加のトラブルシューティング](/troubleshoot-cpu-issues.md)参照。

### 2.2 持続的かつ大幅な増加 {#2-2-persistent-and-significant-increase}

-   2.2.1 TiKV シングルスレッドボトルネック

    -   TiKV インスタンス内のリージョンが多すぎると、単一の gRPC スレッドがボトルネックになります ( **Grafana** -&gt; **TiKV 詳細**-&gt;**スレッド CPU/gRPC CPU スレッドあたりの**メトリックを確認してください)。v3.x 以降のバージョンでは、 `Hibernate Region`有効にして問題を解決できます。中国語では[ケース612](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case612.md)参照してください。

    -   v3.0 より前のバージョンでは、raftstore スレッドまたは適用スレッドがボトルネックになった場合 ( **Grafana** -&gt; **TiKV-details** -&gt; **Thread CPU/raft store CPU**および**Async apply CPU**メトリックが`80%`を超える)、TiKV (v2.x) インスタンスをスケールアウトするか、マルチスレッドで v3.x にアップグレードできます。 <!-- See [case-517](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case517.md) in Chinese. -->

-   2.2.2 CPU負荷が増加します。

-   2.2.3 TiKV低速書き込み。1 [4.5](#45-tikv-write-is-slow)参照してください。

-   2.2.4 TiDB 実行プランが間違っています。1 [3.3](#33-wrong-execution-plan)参照してください。

-   2.2.5 その他の原因については[読み取りおよび書き込み遅延の増加のトラブルシューティング](/troubleshoot-cpu-issues.md)参照。

## 3. TiDBの問題 {#3-tidb-issues}

### 3.1 ドキュメント {#3-1-ddl}

-   3.1.1 `decimal`フィールドの長さを変更すると、エラー`ERROR 1105 (HY000): unsupported modify decimal column precision`が報告されます。 <!--See [case-1004](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case517.md) in Chinese.--> TiDB は`decimal`フィールドの長さの変更をサポートしていません。

-   3.1.2 TiDB DDL ジョブがハングしたり、実行が遅くなる (DDL の進行状況を確認するには`admin show ddl jobs`使用します)

    -   原因 1: TiDB はバージョン 6.3.0 で[メタデータロック](/metadata-lock.md)導入し、バージョン 6.5.0 以降のバージョンではデフォルトで有効になっています。DDL 操作に関係するテーブルが、コミットされていないトランザクションに関係するテーブルと交差している場合、トランザクションがコミットまたはロールバックされるまで、DDL 操作はブロックされます。

    -   原因 2: 他のコンポーネント (PD/TiKV) とのネットワークの問題。

    -   原因 3: TiDB の初期バージョン (v3.0.8 より前) では、高同時実行での goroutine が多数あるため、内部負荷が高くなります。

    -   原因 4: 初期バージョン (v2.1.15 およびバージョン &lt; v3.0.0-rc1) では、PD インスタンスが TiDB キーの削除に失敗し、すべての DDL 変更が 2 つのリースを待機することになります。

    -   その他の原因不明の場合、 [バグを報告する](https://github.com/pingcap/tidb/issues/new?labels=type%2Fbug&#x26;template=bug-report.md) 。

    -   解決：

        -   原因 1 の場合、TiDB と TiKV/PD 間のネットワーク接続を確認してください。
        -   原因 2 および 3 については、問題は以降のバージョンですでに修正されています。TiDB を以降のバージョンにアップグレードできます。
        -   その他の原因の場合は、DDL 所有者を移行する次の解決策を使用できます。

    -   DDL 所有者の移行:

        -   TiDBサーバーに接続できる場合は、所有者選出コマンドを再度実行します`curl -X POST http://{TiDBIP}:10080/ddl/owner/resign`
        -   TiDBサーバーに接続できない場合は、 `tidb-ctl`使用してPDクラスターのetcdからDDL所有者を削除し、再選挙をトリガーします`tidb-ctl etcd delowner [LeaseID] [flags] + ownerKey`

-   3.1.3 TiDBがログに`information schema is changed`エラーを報告する

    -   詳しい原因と解決策については[`Information schema is changed`エラーが報告される理由](/faq/sql-faq.md#what-triggers-the-information-schema-is-changed-error)参照してください。

    -   背景: 増加した`schema version`の数は、各 DDL 変更操作の`schema state`の数と一致しています。たとえば、 `create table`操作ではバージョン変更が 1 つあり、 `add column`操作ではバージョン変更が 4 つあります。したがって、列変更操作が多すぎると、 `schema version`急速に増加する可能性があります。詳細については、 [オンラインスキーマ変更](https://static.googleusercontent.com/media/research.google.com/zh-CN//pubs/archive/41376.pdf)を参照してください。

-   3.1.4 TiDBはログに`information schema is out of date`報告します

    -   原因 1: DML ステートメントを実行している TiDBサーバーが`graceful kill`で停止し、終了する準備をしています。DML ステートメントを含むトランザクションの実行時間が 1 DDL リースを超えています。トランザクションがコミットされるとエラーが報告されます。

    -   原因 2: TiDBサーバーは、 DML ステートメントの実行時に PD または TiKV に接続できません。その結果、TiDBサーバーは1 つの DDL リース (デフォルトでは`45s` ) 内で新しいスキーマをロードしなかったか、 `keep alive`設定で TiDBサーバーがPD から切断されました。

    -   原因 3: TiKV の**負荷**が高いか、ネットワークがタイムアウトしています。Grafana -&gt; **TiDB**および**TiKV**でノード負荷を確認してください。

    -   解決：

        -   原因 1 の場合、TiDB の起動時に DML 操作を再試行します。
        -   原因 2 の場合、TiDBサーバーと PD/TiKV 間のネットワークを確認してください。
        -   原因 3 については、TiKV がビジー状態になっている理由を調査します。 [4 TiKVの問題](#4-tikv-issues)を参照してください。

### 3.2 OOMの問題 {#3-2-oom-issues}

-   3.2.1 症状

    -   クライアント: クライアントがエラー`ERROR 2013 (HY000): Lost connection to MySQL server during query`を報告します。

    -   ログを確認する

        -   `dmesg -T | grep tidb-server`を実行します。結果には、エラーが発生した時点付近の OOM-killer ログが表示されます。

        -   エラーが発生した後の時点（つまり、tidb-server が再起動した時点）の「Welcome to TiDB」ログ`tidb.log`を grep します。

        -   `tidb_stderr.log`の`fatal error: runtime: out of memory`または`cannot allocate memory` grep します。

        -   v2.1.8 以前のバージョンでは、 `tidb_stderr.log`の`fatal error: stack overflow` grep できます。

    -   モニター: tidb-server インスタンスのメモリ使用量が短期間で急増します。

-   3.2.2 OOM の原因となる SQL ステートメントを特定します。(現在、TiDB のすべてのバージョンでは SQL を正確に特定できません。SQL ステートメントを特定した後でも、OOM の原因が SQL ステートメントにあるかどうかを分析する必要があります。)

    -   バージョン &gt;= v3.0.0 の場合、 `tidb.log`で &quot;expensive_query&quot; を grep します。このログ メッセージには、タイムアウトになったかメモリクォータを超えた SQL クエリが記録されます。

    -   バージョン &lt; v3.0.0 の場合、 `tidb.log`で grep &quot;メモリ exceeds quota&quot; を実行して、メモリクォータを超える SQL クエリを見つけます。

    > **注記：**
    >
    > 単一の SQLメモリ使用量のデフォルトのしきい値は`1GB`です。このパラメータは、システム変数[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)を構成することで設定できます。

-   3.2.3 OOMの問題を軽減する

    -   `SWAP`有効にすると、大規模なクエリによるメモリの過剰使用によって発生する OOM の問題を軽減できます。メモリが不足している場合、この方法は I/O オーバーヘッドにより大規模なクエリのパフォーマンスに影響を与える可能性があります。パフォーマンスが影響を受ける程度は、残りのメモリ領域とディスク I/O 速度によって異なります。

-   3.2.4 OOMの典型的な理由

    -   SQL クエリには`join`あります。 `explain`使用して SQL ステートメントを表示すると、 `join`操作で`HashJoin`アルゴリズムが選択され、 `inner`テーブルが大きいことがわかります。

    -   `UPDATE/DELETE`回のクエリのデータ量が大きすぎます。中国語では[ケース-882](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case882.md)参照してください。

    -   SQL には`Union`で接続された複数のサブクエリが含まれています。中国語では[ケース-1828](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case1828.md)参照してください。

OOM のトラブルシューティングの詳細については、 [TiDB OOM の問題のトラブルシューティング](/troubleshoot-tidb-oom.md)参照してください。

### 3.3 実行計画が間違っている {#3-3-wrong-execution-plan}

-   3.3.1 症状

    -   SQL クエリの実行時間が前回の実行時間に比べて大幅に長くなったり、実行プランが突然変更されたりします。実行プランがスロー ログに記録されている場合は、実行プランを直接比較できます。

    -   SQL クエリの実行時間は、MySQL などの他のデータベースに比べてかなり長くなります。 `Join Order`などの違いを確認するには、実行プランを他のデータベースと比較します。

    -   スローログではSQL実行時間`Scan Keys`の数値が大きいです。

-   3.3.2 実行計画を調査する

    -   実行時間が許容`explain analyze {SQL}`内であれば、 `explain analyze`の結果の`count`と`execution info`の`row`を比較します。 `TableScan/IndexScan`行に大きな差が見つかった場合、統計が間違っている可能性があります。 他の行に大きな差が見つかった場合、問題は統計にない可能性があります。

    -   `select count(*)` 。実行プランに`join`操作が含まれている場合、 `explain analyze`長い時間がかかる可能性があります。 `TableScan/IndexScan`の条件に対して`select count(*)`を実行し、 `explain`結果の`row count`情報を比較することで、統計に問題があるかどうかを確認できます。

-   3.3.3 緩和策

    -   v3.0 以降のバージョンでは、 `SQL Bind`機能を使用して実行プランをバインドします。

    -   統計を更新します。問題の原因が統計[統計をダンプする](/statistics.md#export-statistics)にあることがほぼ確実な場合は、 `show stats_meta`の`modify count/row count`が特定の値 (たとえば、0.3) より大きい、またはテーブルに時間列のインデックスがあるなど、統計が古いことが原因である場合は、 `analyze table`使用して回復を試みることができます。 `auto analyze`が設定されている場合は、 `tidb_auto_analyze_ratio`システム変数が大きすぎないか (たとえば、0.3 より大きい)、および現在の時刻が`tidb_auto_analyze_start_time`から`tidb_auto_analyze_end_time`の間であるかどうかを確認します。

    -   その他の状況では、 [バグを報告する](https://github.com/pingcap/tidb/issues/new?labels=type%2Fbug&#x26;template=bug-report.md) 。

### 3.4 SQL実行エラー {#3-4-sql-execution-error}

-   3.4.1 クライアントは`ERROR 1265(01000) Data Truncated`エラーを報告します。これは、TiDBが`Decimal`型の精度を内部的に計算する方法がMySQLの方法と互換性がないためです。この問題はv3.0.10（ [＃14438](https://github.com/pingcap/tidb/pull/14438) ）で修正されました。

    -   原因：

        MySQL では、2 つの大きな精度の`Decimal`除算し、結果が最大小数点精度 ( `30` ) を超える場合、 `30`桁のみが予約され、エラーは報告されません。

        TiDB では、計算結果は MySQL と同じですが、 `Decimal`表すデータ構造内で、小数精度のフィールドが実際の精度を保持します。

        `(0.1^30) / 10`例に挙げます。精度は最大`30`であるため、TiDB と MySQL の結果はどちらも`0`なります。ただし、TiDB では、小数点精度のフィールドは依然として`31`です。

        `Decimal`除算を複数回行うと、結果が正しいにもかかわらず、この精度フィールドがどんどん大きくなり、最終的にTiDB（ `72` ）のしきい値を超え、 `Data Truncated`エラーが報告されます。

        `Decimal`の乗算では、範囲外が回避され、精度が最大精度制限に設定されるため、この問題は発生しません。

    -   解決策: `a`と`b`ターゲット精度である場合に、 `Cast(xx as decimal(a, b))`手動で追加することでこの問題を回避できます。

### 3.5 クエリが遅い問題 {#3-5-slow-query-issues}

遅いクエリを識別するには、 [遅いクエリを特定する](/identify-slow-queries.md)参照してください。遅いクエリを分析して処理するには、 [遅いクエリを分析する](/analyze-slow-queries.md)参照してください。

### 3.6 ホットスポットの問題 {#3-6-hotspot-issues}

分散データベースである TiDB には、アプリケーションの負荷をさまざまなコンピューティング ノードまたはstorageノードにできるだけ均等に分散して、サーバーリソースをより有効に活用するための負荷分散メカニズムがあります。ただし、特定のシナリオでは、一部のアプリケーションの負荷が適切に分散されない場合があり、パフォーマンスに影響を及ぼし、ホットスポットとも呼ばれる単一の高負荷ポイントが形成される可能性があります。

TiDB は、ホットスポットのトラブルシューティング、解決、回避のための完全なソリューションを提供します。負荷ホットスポットを分散することで、QPS の向上やレイテンシーの削減など、全体的なパフォーマンスを向上させることができます。詳細なソリューションについては、 [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)参照してください。

### 3.7 ディスクI/O使用率が高い {#3-7-high-disk-i-o-usage}

CPU ボトルネックとトランザクション競合によるボトルネックをトラブルシューティングした後、TiDB の応答が遅くなった場合は、現在のシステム ボトルネックを特定するために I/O メトリックを確認する必要があります。TiDB での I/O 使用率が高い問題を特定して対処する方法については、 [ディスクI/O使用率が高い場合のトラブルシューティング](/troubleshoot-high-disk-io.md)参照してください。

### 3.8 ロックの競合 {#3-8-lock-conflicts}

TiDB は完全な分散トランザクションをサポートします。v3.0 以降、TiDB は楽観的トランザクション モードと悲観的トランザクション モードを提供します。ロック関連の問題のトラブルシューティング方法と、楽観的と悲観的ロックの競合の処理方法については、 [ロック競合のトラブルシューティング](/troubleshoot-lock-conflicts.md)参照してください。

### 3.9 データとインデックスの不一致 {#3-9-inconsistency-between-data-and-indexes}

TiDB は、トランザクションまたは[`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md)のステートメントを実行するときに、データとインデックス間の一貫性をチェックします。チェックの結果、レコードのキー値と対応するインデックスのキー値が一致していないことが判明した場合、つまり、行データを格納するキー値のペアと、そのインデックスを格納する対応するキー値のペアが一致していない場合 (たとえば、インデックスが多すぎる、またはインデックスが欠落している)、TiDB はデータ不一致エラーを報告し、関連するエラーをエラー ログに出力。

不整合エラーの詳細とチェックをバイパスする方法については、 [データとインデックス間の不整合のトラブルシューティング](/troubleshoot-data-inconsistency-errors.md)参照してください。

## 4. TiKVの問題 {#4-tikv-issues}

### 4.1 TiKVがパニックを起こして起動に失敗する {#4-1-tikv-panics-and-fails-to-start}

-   4.1.1 `sync-log = false` . マシンの電源を切った後に`unexpected raft log index: last_index X < applied_index Y`エラーが返されます。

    この問題は予想通りです。1 `tikv-ctl`使用してリージョンを復元できます。

-   4.1.2 TiKV が仮想マシンに展開されている場合、仮想マシンが強制終了されるか物理マシンの電源がオフになると、 `entries[X, Y] is unavailable from storage`エラーが報告されます。

    この問題は予想通りです。仮想マシンの`fsync`信頼できないため、 `tikv-ctl`使用してリージョンを復元する必要があります。

-   4.1.3 その他の予期せぬ原因の場合、 [バグを報告する](https://github.com/tikv/tikv/issues/new?template=bug-report.md) .

### 4.2 TiKV OOM {#4-2-tikv-oom}

-   4.2.1 `block-cache`構成が大きすぎると、OOM が発生する可能性があります。

    問題の原因を確認するには、モニター**Grafana** -&gt; **TiKV-details**で対応するインスタンスを選択して、RocksDB の`block cache size`確認します。

    一方で、 `[storage.block-cache] capacity = # "1GB"`パラメータが適切に設定されているかどうかを確認してください。デフォルトでは、TiKV の`block-cache`マシンの合計メモリの`45%`に設定されています。TiKV は物理マシンのメモリを取得するため、コンテナのメモリ制限を超える可能性があるため、コンテナに TiKV をデプロイするときにこのパラメータを明示的に指定する必要があります。

-   4.2.2コプロセッサーは多数の大きなクエリを受信し、大量のデータを返します。gRPC はコプロセッサがデータを返すのと同じ速さでデータを送信できず、OOM が発生します。

    原因を確認するには、モニター**Grafana** -&gt; **TiKV-details** -&gt; **coprocessor summary**を表示して、 `response size` `network outbound`トラフィックを超えているかどうかを確認します。

-   4.2.3 他のコンポーネントがメモリを大量に占有します。

    この問題は予期されていません。 [バグを報告する](https://github.com/tikv/tikv/issues/new?template=bug-report.md)実行できます。

### 4.3 クライアントが<code>server is busy</code>エラーを報告する {#4-3-the-client-reports-the-code-server-is-busy-code-error}

モニター**Grafana** -&gt; **TiKV** -&gt;**エラー**を表示して、ビジーの具体的な原因を確認します。7 `server is busy` TiKV のフロー制御メカニズムによって発生し、TiKV の負荷が現在高すぎるため後で再試行することを`tidb/ti-client`通知します。

-   4.3.1 TiKV RocksDB の遭遇`write stall` 。

    TiKV インスタンスには 2 つの RocksDB インスタンスがあり、 `data/raft`にはRaftログを保存し、もう`data/db`つには実際のデータを保存します。ログで`grep "Stalling" RocksDB`実行すると、ストールの具体的な原因を確認できます。RocksDB ログは`LOG`で始まるファイルで、 `LOG`現在のログです。 `write stall`は RocksDB にネイティブに組み込まれたパフォーマンス低下メカニズムです。RocksDB で`write stall`発生すると、システムのパフォーマンスが大幅に低下します。v5.2.0 より前のバージョンでは、TiDB は`write stall`に遭遇すると`ServerIsBusy`エラーを直接クライアントに返すことで、すべての書き込み要求をブロックしようとしていましたが、これにより QPS パフォーマンスが急激に低下する可能性があります。v5.2.0 以降、TiKV は、 `write stall`が発生したときに`server is busy`クライアントに返すという以前のメカニズムに代わる、スケジューリングレイヤーで書き込み要求を動的に遅延させることで書き込みを抑制する新しいフロー制御メカニズムを導入しています。新しいフロー制御メカニズムはデフォルトで有効になっており、TiKV は`KvDB`および`RaftDB` (memtable を除く) の`write stall`メカニズムを自動的に無効にします。ただし、保留中の要求の数が特定のしきい値を超えると、フロー制御メカニズムは引き続き有効になり、一部またはすべての書き込み要求を拒否し、クライアントに`server is busy`エラーを返します。詳細な説明としきい値については、 [フロー制御設定](/tikv-configuration-file.md#storageflow-control)参照してください。

    -   保留中の圧縮バイトが多すぎるために`server is busy`エラーが発生した場合は、 [`soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit)および[`hard-pending-compaction-bytes-limit`](/tikv-configuration-file.md#hard-pending-compaction-bytes-limit)パラメータの値を増やすことでこの問題を軽減できます。

        -   保留中の圧縮バイトが`soft-pending-compaction-bytes-limit`パラメータの値 (デフォルトでは`192GiB` ) に達すると、フロー制御メカニズムは一部の書き込み要求を拒否し始めます (クライアントに`ServerIsBusy`を返すことによって)。この場合、このパラメータの値を`[storage.flow-control] soft-pending-compaction-bytes-limit = "384GiB"`に増やすことができます。

        -   保留中の圧縮バイトが`hard-pending-compaction-bytes-limit`パラメータの値（デフォルトでは`1024GiB` ）に達すると、フロー制御メカニズムはすべての書き込み要求を拒否し始めます（クライアントに`ServerIsBusy`を返します）。しきい値`soft-pending-compaction-bytes-limit`に達するとフロー制御メカニズムが介入して書き込み速度を遅くするため、このシナリオが発生する可能性は低くなります。発生した場合は、このパラメータの値を`[storage.flow-control] hard-pending-compaction-bytes-limit = "2048GiB"`に増やすことができます。

        -   ディスク I/O 容量が長時間書き込みに追いつかない場合は、ディスクをスケールアップすることをお勧めします。ディスク スループットが上限に達して書き込みが停止した場合 (たとえば、SATA SSD が NVME SSD よりはるかに低い場合)、CPU リソースが十分であれば、より高い圧縮率の圧縮アルゴリズムを適用できます。この方法では、CPU リソースがディスク リソースと交換され、ディスクへの負荷が軽減されます。

        -   デフォルトの CF 圧縮で高圧が発生する場合は、 `[rocksdb.defaultcf] compression-per-level`パラメータを`["no", "no", "lz4", "lz4", "lz4", "zstd", "zstd"]`から`["no", "no", "zstd", "zstd", "zstd", "zstd", "zstd"]`に変更します。

    -   memtable が多すぎると、ストールが発生します。これは通常、インスタント書き込みの量が多く、memtable がディスクにフラッシュされるのが遅い場合に発生します。ディスク書き込み速度を改善できず、この問題がビジネスのピーク時にのみ発生する場合は、対応する CF の`max-write-buffer-number`増やすことで軽減できます。

        -   たとえば、 `[rocksdb.defaultcf] max-write-buffer-number` `8`に設定します (デフォルトは`5` )。これにより、メモリ内のメモリテーブルが増えるため、ピーク時のメモリ使用量が増加する可能性があることに注意してください。

-   4.3.2 `scheduler too busy`

    -   深刻な書き込み競合`latch wait duration`が高い。モニター**Grafana** -&gt; **TiKV-details** -&gt; **scheduler prewrite** / **scheduler commit**で`latch wait duration`確認できます。スケジューラに書き込みタスクが溜まると、保留中の書き込みタスクが`[storage] scheduler-pending-write-threshold`で設定したしきい値 (100MB) を超えます。15 に該当するメトリックを確認することで`MVCC_CONFLICT_COUNTER`を確認できます。

    -   書き込み速度が遅いため、書き込みタスクが溜まります。TiKV に書き込まれるデータが`[storage] scheduler-pending-write-threshold`で設定されたしきい値 (100 MB) を超えています[4.5](#45-tikv-write-is-slow)を参照してください。

-   4.3.3 `raftstore is busy` . メッセージの処理がメッセージの受信よりも遅くなります。 `channel full`の状態は短期的にはサービスに影響しませんが、エラーが長時間続くと、Leaderの切り替えが発生する可能性があります。

    -   `append log`エンカウンターストール。2 を参照してください[4.3.1](#43-the-client-reports-the-server-is-busy-error)
    -   `append log duration`は高いため、メッセージの処理が遅くなります[4.5](#45-tikv-write-is-slow)を参照して、 `append log duration`が高い理由を分析できます。
    -   raftstore は、大量のメッセージを瞬時に受信し (TiKV Raftメッセージ ダッシュボードで確認)、処理に失敗します。通常、短期的な`channel full`ステータスはサービスに影響しません。

-   4.3.4 TiKV コプロセッサがキュー内にあります。蓄積されたタスクの数が`coprocessor threads * readpool.coprocessor.max-tasks-per-worker-[normal|low|high]`超えています。大規模なクエリが多すぎると、タスクがコプロセッサに蓄積されます。実行プランの変更によって大量のテーブル スキャン操作が発生していないかどうかを確認する必要があります。 [3.3](#33-wrong-execution-plan)を参照してください。

### 4.4 一部のTiKVノードは頻繁にLeaderをドロップする {#4-4-some-tikv-nodes-drop-leader-frequently}

-   4.4.1 TiKVの再開による再選挙

    -   TiKV がパニックした後、systemd によって引き上げられ、正常に動作します。TiKV ログを表示することで、panicが発生したかどうかを確認できます。この問題は予期しないものであるため、発生した場合は[バグを報告する](https://github.com/tikv/tikv/issues/new?template=bug-report.md) 。

    -   TiKV はサードパーティによって停止または強制終了され、その後 systemd によってプルアップされます。1 と TiKV ログ`dmesg`表示して原因を確認してください。

    -   TiKV は OOM であり、再起動が発生します[4.2](#42-tikv-oom)を参照してください。

    -   `THP` (Transparent Hugepage) を動的に調整しているため、TiKV がハングします。中国語のケース[ケース-500](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case500.md)を参照してください。

-   4.4.2 TiKV RocksDB が書き込み停止に遭遇し、その結果再選出が行われます。モニター**Grafana** -&gt; **TiKV-details** -&gt; **errors**に`server is busy`表示されているかどうかを確認できます[4.3.1](#43-the-client-reports-the-server-is-busy-error)を参照してください。

-   4.4.3 ネットワーク分離による再選。

### 4.5 TiKVの書き込みが遅い {#4-5-tikv-write-is-slow}

-   4.5.1 TiKV gRPC の`prewrite/commit/raw-put`期間を表示して、TiKV 書き込みが低いかどうかを確認します (RawKV クラスターのみ)。通常、 [パフォーマンスマップ](https://github.com/pingcap/tidb-map/blob/master/maps/performance-map.png)に従って遅いフェーズを見つけることができます。一般的な状況をいくつか次に示します。

-   4.5.2 スケジューラ CPU がビジー状態です (トランザクション kv のみ)。

    プレライト/コミットの`scheduler command duration`が`scheduler latch wait duration`と`storage async write duration`の合計よりも長くなっています。スケジューラワーカーの CPU 需要が高く、 `scheduler-worker-pool-size` * 100% の 80% 以上になっているか、マシン全体の CPU リソースが比較的限られています。書き込みワークロードが大きい場合は、 `[storage] scheduler-worker-pool-size`設定が小さすぎないか確認してください。

    その他の状況では、 [バグを報告する](https://github.com/tikv/tikv/issues/new?template=bug-report.md) 。

-   4.5.3 ログの追加が遅い。

    TiKV Grafana の**Raft IO** / `append log duration`が高くなっているのは、通常、ディスク書き込み操作が遅いためです。RocksDB - raft の`WAL Sync Duration max`値を確認することで原因を確認できます。

    その他の状況では、 [バグを報告する](https://github.com/tikv/tikv/issues/new?template=bug-report.md) 。

-   4.5.4 raftstore スレッドがビジー状態です。

    **Raft Propose** / `propose wait duration`は、TiKV Grafana のログ追加期間よりも大幅に大きくなります。次の方法を実行します。

    -   `[raftstore] store-pool-size`設定値が小さすぎないか確認してください。値は`1` ～ `5`間で、大きすぎないように設定することをお勧めします。
    -   マシン上の CPU リソースが不足していないかどうかを確認します。

-   4.5.5 適用が遅いです。

    TiKV Grafana の**Raft IO** / `apply log duration`が高くなっています。これは通常、 **Raft Propose** / `apply wait duration`も高いことを意味します。考えられる原因は次のとおりです。

    -   `[raftstore] apply-pool-size`は小さすぎます ( `1`から`5`間で大きすぎない値を設定することを推奨します)。また、 **Thread CPU** / `apply CPU`は大きすぎます。

    -   マシン上の CPU リソースが不足しています。

    -   リージョン書き込みホットスポット。単一の適用スレッドの CPU 使用率が高くなります。現在、単一のリージョンのホットスポット問題に適切に対処することはできませんが、これは改善中です。各スレッドの CPU 使用率を表示するには、Grafana 式を変更して`by (instance, name)`を追加します。

    -   RocksDB の書き込みが遅いです。RocksDB **kv** / `max write duration`が高くなっています。1 つのRaftログに複数の KV が含まれている可能性があります。RocksDB に書き込むと、128 個の KV が書き込みバッチで RocksDB に書き込まれます。したがって、適用ログは RocksDB の複数の書き込みに関連付けられている可能性があります。

    -   その他の状況では、 [バグを報告する](https://github.com/tikv/tikv/issues/new?template=bug-report.md) 。

-   4.5.6 Raftコミット ログが遅い。

    TiKV Grafana の**Raft IO** / `commit log duration`は高いです (このメトリックは、Grafana v4.x 以降でのみサポートされています)。すべてのリージョンは、独立したRaftグループに対応しています。Raftには、TCP のスライディング ウィンドウ メカニズムに似たフロー制御メカニズムがあります。5 `[raftstore] raft-max-inflight-msgs = 256`を構成することで、スライディング ウィンドウのサイズを制御できます。書き込みホット スポットがあり、 `commit log duration`が高い場合は、パラメータを`1024`に増やすなどして調整できます。

-   4.5.7 その他の状況については、 [パフォーマンスマップ](https://github.com/pingcap/tidb-map/blob/master/maps/performance-map.png)の書き込みパスを参照して原因を分析します。

## 5. PDの問題 {#5-pd-issues}

### 5.1 PDスケジュール {#5-1-pd-scheduling}

-   5.1.1 マージ

    -   テーブル間の空の領域は結合できません。TiKV の`[coprocessor] split-region-on-table`パラメータを変更する必要があります。このパラメータは、v4.x ではデフォルトで`false`に設定されています。中国語の[ケース-896](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case896.md)参照してください。

    -   リージョンのマージが遅いです。Grafana -&gt; **PD** -&gt;**オペレーター**のモニターダッシュボードにアクセスして、マージされた**オペレーター**が生成されたかどうかを確認できます。マージを高速化するには、 `merge-schedule-limit`の値を増やします。

-   5.1.2 レプリカの追加またはレプリカのオンライン/オフライン化

    -   TiKV ディスクは容量の 80% を使用し、PD はレプリカを追加しません。この状況では、ミス ピアの数が増えるため、TiKV をスケール アウトする必要があります。中国語では[ケース-801](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case801.md)参照してください。

    -   TiKVノードがオフラインになると、一部のリージョンを他のノードに移行できなくなります。この問題はv3.0.4（ [＃5526](https://github.com/tikv/tikv/pull/5526) ）で修正されました。中国語版は[ケース-870](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case870.md)ご覧ください。

-   5.1.3 バランス

    -   Leader/ リージョン の数が均等に配分されていません。中国語では[ケース394](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case394.md)と[ケース759](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case759.md)参照してください。主な原因は、バランスがリージョン/ Leaderのサイズに基づいてスケジュールを実行するため、数が均等に配分されない可能性があることです。TiDB 4.0 では、 `[leader-schedule-policy]`パラメータが導入され、 Leaderのスケジュール ポリシーを`count`ベースまたは`size`ベースに設定できるようになりました。

### 5.2 PD選挙 {#5-2-pd-election}

-   5.2.1 PD スイッチLeader。

    -   原因 1: ディスク。PD ノードが配置されているディスクの I/O 負荷が最大になっています。PD が、I/O 需要の高い他のコンポーネントと一緒にデプロイされているかどうか、およびディスクの状態を調べます。原因を確認するには、 **Grafana** -&gt;**ディスク パフォーマンス**-&gt;**レイテンシー**/**負荷**のモニター メトリックを表示します。必要に応じて、FIO ツールを使用してディスクのチェックを実行することもできます。中国語の[ケース292](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case292.md)参照してください。

    -   原因 2: ネットワーク。PD ログには`lost the TCP streaming connection`表示されます。PD ノード間のネットワークに問題がないか確認し、モニター**Grafana** -&gt; **PD** -&gt; **etcd**で`round trip`表示して原因を確認する必要があります。中国語では[ケース177](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case177.md)参照してください。

    -   原因 3: システム負荷が高い。ログには`server is likely overloaded`と表示されます。中国語では[ケース214](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case214.md)参照してください。

-   5.2.2 PD がLeaderを選出できない、または選出が遅い。

    -   PD がLeaderを選出できません: PD ログには`lease is not expired`と表示されます。3 [この号](https://github.com/etcd-io/etcd/issues/10355) v3.0.x および v2.1.19 で修正されました。中国語では[ケース-875](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case875.md)参照してください。

    -   選挙が遅い:リージョンの読み込み時間が長いです。この問題は、PD ログで`grep "regions cost"`実行することで確認できます。結果が`load 460927 regions cost 11.77099s`などの秒単位の場合、リージョンの読み込みが遅いことを意味します。v3.0 で`use-region-storage`を`true`に設定することで`region storage`機能を有効にでき、リージョンの読み込み時間が大幅に短縮されます。中国語では[ケース429](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case429.md)参照してください。

-   5.2.3 TiDB が SQL ステートメントを実行すると PD がタイムアウトします。

    -   PD にLeaderがいない、またはLeaderが切り替わります。 [5.2.1](#52-pd-election)と[5.2.2](#52-pd-election)を参照してください。

    -   ネットワークの問題。モニター**Grafana** -&gt; **blackbox_exporter** -&gt; **pingレイテンシー**にアクセスして、TiDB から PDLeaderへのネットワークが正常に動作しているかどうかを確認します。

    -   PDはパニックに陥る[バグを報告する](https://github.com/pingcap/pd/issues/new?labels=kind%2Fbug&#x26;template=bug-report.md) .

    -   PDは[5.3](#53-pd-oom)です。1を参照してください。

    -   問題に他の原因がある場合は、 `curl http://127.0.0.1:2379/debug/pprof/goroutine?debug=2`と[バグを報告する](https://github.com/pingcap/pd/issues/new?labels=kind%2Fbug&#x26;template=bug-report.md)実行して goroutine を取得します。

-   5.2.4 その他の問題

    -   PDは`FATAL`エラーを報告し、ログには`range failed to find revision pair`表示されます。この問題はv3.0.8（ [＃2040](https://github.com/pingcap/pd/pull/2040) ）で修正されました。詳細については、中国語の[ケース947](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case947.md)参照してください。

    -   その他の状況では、 [バグを報告する](https://github.com/pingcap/pd/issues/new?labels=kind%2Fbug&#x26;template=bug-report.md) 。

### 5.3 PD OOM {#5-3-pd-oom}

-   5.3.1 `/api/v1/regions`インターフェースを使用すると、リージョンが多すぎると PD OOM が発生する可能性があります。この問題は v3.0.8 ( [＃1986](https://github.com/pingcap/pd/pull/1986) ) で修正されました。

-   5.3.2 ローリングアップグレード中のPD OOM。gRPCメッセージのサイズは制限されておらず、モニターはTCP InSegsが比較的大きいことを示しています。この問題はv3.0.6（ [＃1952](https://github.com/pingcap/pd/pull/1952) ）で修正されました。 <!--For details, see [case-852](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case852.md).-->

### 5.4 Grafanaディスプレイ {#5-4-grafana-display}

-   5.4.1 **Grafana** -&gt; **PD** -&gt;**クラスター**-&gt;**ロール**のモニターにフォロワーが表示されます。Grafana 式の問題は v3.0.8 で修正されました。

## 6. エコシステムツール {#6-ecosystem-tools}

### 6.1 データ移行 {#6-1-data-migration}

-   6.1.1 TiDB Data Migration (DM) は、MySQL/MariaDB から TiDB へのデータ移行をサポートする移行ツールです。詳細については、 [DMの概要](/dm/dm-overview.md)参照してください。

-   6.1.2 `Access denied for user 'root'@'172.31.43.27' (using password: YES)` `query status`実行したとき、またはログを確認したときに表示されます。

    -   すべての DM 構成ファイル内のデータベース関連のパスワードは`dmctl`で暗号化する必要があります。データベース パスワードが空の場合、パスワードを暗号化する必要はありません。クリアテキスト パスワードは v1.0.6 以降で使用できます。
    -   DM 操作中、上流および下流データベースのユーザーは、対応する読み取りおよび書き込み権限を持っている必要があります。データ移行は、データ複製タスクの開始時に自動的に実行さ[対応する権限を事前チェックする](/dm/dm-precheck.md)ます。
    -   DM クラスターに DM-worker/DM-master/dmctl の異なるバージョンをデプロイするには、中国語の[AskTUGのケーススタディ](https://asktug.com/t/dm1-0-0-ga-access-denied-for-user/1049/5)参照してください。

-   6.1.3 レプリケーション タスクが中断され、 `driver: bad connection`エラーが返されます。

    -   エラー`driver: bad connection`は、DM と下流の TiDB データベース間の接続に異常 (ネットワーク障害や TiDB の再起動など) が発生し、現在のリクエストのデータがまだ TiDB に送信されていないことを示します。

        -   DM 1.0.0 GA より前のバージョンの場合は、 `stop-task`実行してタスクを停止し、 `start-task`を実行してタスクを再起動します。
        -   DM 1.0.0 GA 以降のバージョンでは、このタイプのエラーに対する自動再試行メカニズムが追加されています。 [＃265](https://github.com/pingcap/dm/pull/265)参照してください。

-   6.1.4 レプリケーション タスクが`invalid connection`エラーで中断されます。

    -   `invalid connection`エラーは、DM と下流の TiDB データベース間の接続に異常が発生し (ネットワーク障害、TiDB の再起動、TiKV ビジーなど)、現在のリクエストのデータの一部が TiDB に送信されたことを示します。DM はレプリケーション タスクで下流にデータを並行してレプリケーションする機能があるため、タスクが中断されるといくつかのエラーが発生する可能性があります。これらのエラーは、 `query-status`または`query-error`実行することで確認できます。

        -   増分レプリケーション プロセス中に`invalid connection`エラーのみが発生した場合、DM はタスクを自動的に再試行します。
        -   バージョンの問題により DM が再試行しない、または自動的に再試行できない場合 (自動再試行は v1.0.0-rc.1 で導入されています)、 `stop-task`使用してタスクを停止し、 `start-task`使用してタスクを再起動します。

-   6.1.5 リレーユニットがエラー`event from * in * diff from passed-in event *`報告するか、またはレプリケーションタスクが`get binlog error ERROR 1236 (HY000) and binlog checksum mismatch, data may be corrupted returned`などのbinlogの取得または解析に失敗するエラーで中断されます。

    -   DM がリレー ログまたは増分レプリケーションをプルするプロセス中に、アップストリームbinlogファイルのサイズが 4 GB を超えると、この 2 つのエラーが発生する可能性があります。

    -   原因: リレー ログを書き込む際、DM はbinlog の位置とbinlogファイルのサイズに基づいてイベント検証を実行し、複製されたbinlog の位置をチェックポイントとして保存する必要があります。ただし、公式の MySQL は uint32 を使用してbinlog の位置を保存するため、4 GB を超えるbinlogファイルのbinlog の位置がオーバーフローし、上記のエラーが発生します。

    -   解決：

        -   リレー処理装置の場合、 [手動でレプリケーションを回復する](https://pingcap.com/docs/tidb-data-migration/dev/error-handling/#the-relay-unit-throws-error-event-from--in--diff-from-passed-in-event--or-a-replication-task-is-interrupted-with-failing-to-get-or-parse-binlog-errors-like-get-binlog-error-error-1236-hy000-and-binlog-checksum-mismatch-data-may-be-corrupted-returned) 。
        -   binlogレプリケーション処理単位の場合、 [手動でレプリケーションを回復する](https://pingcap.com/docs/tidb-data-migration/dev/error-handling/#the-relay-unit-throws-error-event-from--in--diff-from-passed-in-event--or-a-replication-task-is-interrupted-with-failing-to-get-or-parse-binlog-errors-like-get-binlog-error-error-1236-hy000-and-binlog-checksum-mismatch-data-may-be-corrupted-returned) 。

-   6.1.6 DMレプリケーションが中断され、ログに`ERROR 1236 (HY000) The slave is connecting using CHANGE MASTER TO MASTER_AUTO_POSITION = 1, but the master has purged binary logs containing GTIDs that the slave requires.`返される

    -   マスターbinlogが消去されているかどうかを確認します。
    -   `relay.meta`で記録した位置情報を確認します。

        -   `relay.meta`空の GTID 情報を記録しています。DM-worker は終了時または 30 秒ごとに`relay.meta`に GTID 情報をメモリに保存します。DM-worker が上流の GTID 情報を取得しない場合は、空の GTID 情報を`relay.meta`に保存します。中国語では[ケース772](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case772.md)参照してください。

        -   `relay.meta`で記録されたbinlogイベントにより、不完全なリカバリ プロセスがトリガーされ、間違った GTID 情報が記録されます。この問題は v1.0.2 で修正されており、以前のバージョンでも発生する可能性があります。 <!--See [case-764](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case764.md).-->

-   6.1.7 DMレプリケーションプロセスがエラー`Error 1366: incorrect utf8 value eda0bdedb29d(\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd)`を返します。

    -   この値は MySQL 8.0 または TiDB に正常に書き込むことができませんが、 MySQL 5.7には書き込むことができます`tidb_skip_utf8_check`パラメータを有効にすると、データ形式のチェックをスキップできます。

### 6.2 TiDB Lightning {#6-2-tidb-lightning}

-   6.2.1 TiDB Lightningは、大量のデータを TiDB クラスターに高速かつ完全にインポートするためのツールです。 [GitHub 上のTiDB Lightning](https://github.com/pingcap/tidb/tree/release-8.5/lightning)参照してください。

-   6.2.2 インポート速度が遅すぎます。

    -   `region-concurrency`設定が高すぎると、スレッドの競合が発生し、パフォーマンスが低下します。トラブルシューティングには 3 つの方法があります。

        -   設定は、ログの先頭から`region-concurrency`検索すると見つかります。
        -   TiDB Lightning が他のサービス (たとえば、Importer) とサーバーを共有する場合は、そのサーバーの CPU コアの合計数の`region-concurrency` ～ 75% を手動で設定する必要があります。
        -   CPU にクォータがある場合 (Kubernetes 設定によって制限されている場合など)、 TiDB Lightning はこれを読み取ることができない可能性があります。この場合、 `region-concurrency`も手動で減らす必要があります。

    -   インデックスを追加するたびに、各行に新しい KV ペアが導入されます。インデックスが N 個ある場合、インポートされる実際のサイズは、 [Dumpling](/dumpling-overview.md)出力のサイズの約 (N+1) 倍になります。インデックスが無視できるほど小さい場合は、最初にスキーマからインデックスを削除し、インポートが完了した後に`CREATE INDEX`経由で再度追加することができます。

    -   TiDB Lightningのバージョンが古いです。最新バージョンをお試しください。インポート速度が向上する可能性があります。

-   6.2.3 `checksum failed: checksum mismatched remote vs local` .

    -   原因 1: テーブルにすでにデータがある可能性があります。これらの古いデータは最終的なチェックサムに影響を与える可能性があります。

    -   原因 2: ターゲット データベースのチェックサムが 0 の場合、つまり何もインポートされていない場合は、クラスターが過熱していて、データを取り込めない可能性があります。

    -   原因 3: データ ソースがマシンによって生成され、 [Dumpling](/dumpling-overview.md)によってバックアップされていない場合は、テーブルの制約に準拠していることを確認します。例:

        -   `AUTO_INCREMENT`列は正の値である必要があり、値「0」は含まれません。
        -   UNIQUE KEY と PRIMARY KEY には重複するエントリがあってはなりません。

    -   解決策: [トラブルシューティングの解決策](/tidb-lightning/troubleshoot-tidb-lightning.md#checksum-failed-checksum-mismatched-remote-vs-local)参照してください。

-   6.2.4 `Checkpoint for … has invalid status:(error code)`

    -   原因: チェックポイントが有効になっており、Lightning/Importer が以前に異常終了しました。偶発的なデータ破損を防ぐため、エラーが解決されるまでTiDB Lightning は起動しません。エラー コードは 25 未満の整数で、可能な値は`0, 3, 6, 9, 12, 14, 15, 17, 18, 20 and 21`です。整数は、インポート プロセスで予期しない終了が発生したステップを示します。整数が大きいほど、終了が遅くなります。

    -   解決策: [トラブルシューティングの解決策](/tidb-lightning/troubleshoot-tidb-lightning.md#checkpoint-for--has-invalid-status-error-code)参照してください。

-   6.2.5 `cannot guess encoding for input file, please convert to UTF-8 manually`

    -   原因: TiDB Lightning は、UTF-8 および GB-18030 エンコードのみをサポートしています。このエラーは、ファイルがこれらのエンコードのいずれでもないことを意味します。また、過去の ALTER TABLE 実行により、UTF-8 の文字列と GB-18030 の別の文字列を含むなど、ファイルにエンコードが混在している可能性もあります。

    -   解決策: [トラブルシューティングの解決策](/tidb-lightning/troubleshoot-tidb-lightning.md#cannot-guess-encoding-for-input-file-please-convert-to-utf-8-manually)参照してください。

-   6.2.6 `[sql2kv] sql encode error = [types:1292]invalid time format: '{1970 1 1 0 45 0 0}'`

    -   原因: タイムスタンプ タイプのエントリに存在しない時間値があります。これは、DST の変更または時間値がサポートされている範囲 (1970 年 1 月 1 日から 2038 年 1 月 19 日まで) を超えたことが原因です。

    -   解決策: [トラブルシューティングの解決策](/tidb-lightning/troubleshoot-tidb-lightning.md#sql2kv-sql-encode-error--types1292invalid-time-format-1970-1-1-)参照してください。

## 7. 共通ログ分析 {#7-common-log-analysis}

### 7.1 ティDB {#7-1-tidb}

-   7.1.1 `GC life time is shorter than transaction duration` .

    トランザクションの継続時間が GC の有効期間 (デフォルトでは 10 分) を超えています。

    [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)システム変数を変更することで、GC の有効期間を延ばすことができます。通常、このパラメータを変更することはお勧めしません。このトランザクションに`UPDATE`および`DELETE`ステートメントが多数含まれている場合、パラメータを変更すると古いバージョンが大量に蓄積される可能性があるためです。

-   7.1.2 `txn takes too much time` .

    このエラーは、長時間 (590 秒以上) コミットされていないトランザクションをコミットしたときに返されます。

    アプリケーションでこのような長時間のトランザクションを実行する必要がある場合は、 `[tikv-client] max-txn-time-use = 590`パラメータと GC 有効期間を増やすことでこの問題を回避できます。アプリケーションでこのような長いトランザクション時間が必要かどうかを確認することをお勧めします。

-   7.1.3 `coprocessor.go`レポート`request outdated` 。

    このエラーは、TiKV に送信されたコプロセッサ要求が TiKV のキューで 60 秒以上待機している場合に返されます。

    TiKV コプロセッサが長いキューに入っている理由を調査する必要があります。

-   7.1.4 `region_cache.go` `switch region peer to next due to send request fail`という大きな数値を報告し、エラーメッセージは`context deadline exceeded`です。

    TiKV のリクエストがタイムアウトし、リージョン キャッシュがトリガーされてリクエストが他のノードに切り替えられます。ログの`addr`フィールドで`grep "<addr> cancelled`コマンドを引き続き実行し、 `grep`結果に応じて次の手順を実行できます。

    -   `send request is cancelled` : 送信フェーズ中にリクエストがタイムアウトしました。Grafana -&gt; **TiDB** -&gt; **Batch Client** / `Pending Request Count by TiKV`**の**監視を調査して、保留中のリクエスト数が 128 より大きいかどうかを確認できます。

        -   値が 128 より大きい場合、送信が KV の処理能力を超えるため、送信が重なってしまいます。
        -   値が 128 より大きくない場合は、ログをチェックして、レポートが対応する KV の操作および保守の変更によって発生したものかどうかを確認します。それ以外の場合、このエラーは予期しないものであり、 [バグを報告する](https://github.com/pingcap/tidb/issues/new?labels=type%2Fbug&#x26;template=bug-report.md)実行する必要があります。

    -   `wait response is cancelled` : リクエストは TiKV に送信された後にタイムアウトしました。その時点で PD と KV に記録される対応する TiKV アドレスとリージョンの応答時間を確認する必要があります。

-   7.1.5 `distsql.go`レポート`inconsistent index` 。

    データ インデックスに矛盾があるようです。報告されたインデックスがあるテーブルで`admin check table <TableName>`コマンドを実行します。チェックが失敗した場合は、次のコマンドを実行してガベージコレクションを無効にし、 [バグを報告する](https://github.com/pingcap/tidb/issues/new?labels=type%2Fbug&#x26;template=bug-report.md)実行します。

    ```sql
    SET GLOBAL tidb_gc_enable = 0;
    ```

### 7.2 ティクヴィ {#7-2-tikv}

-   7.2.1 `key is locked` .

    読み取りと書き込みに競合があります。読み取り要求でコミットされていないデータが検出されたため、データがコミットされるまで待機する必要があります。

    このエラーが少数であればビジネスに影響はありませんが、このエラーが多数発生すると、ビジネスにおいて読み取りと書き込みの競合が深刻であることを示します。

-   7.2.2 `write conflict` .

    これは、楽観的トランザクションにおける書き込み-書き込み競合です。複数のトランザクションが同じキーを変更した場合、1 つのトランザクションのみが成功し、他のトランザクションは自動的にタイムスタンプを再度取得して操作を再試行するため、ビジネスには影響しません。

    競合が深刻な場合は、複数回の再試行後にトランザクションが失敗する可能性があります。この場合は、悲観的ロックを使用することをお勧めします。エラーと解決策の詳細については、 [楽観的トランザクションにおける書き込み競合のトラブルシューティング](/troubleshoot-write-conflicts.md)参照してください。

-   7.2.3 `TxnLockNotFound` .

    このトランザクションのコミットは遅すぎるため、Time To Live (TTL) 後に他のトランザクションによってロールバックされます。このトランザクションは自動的に再試行されるため、通常はビジネスに影響はありません。サイズが 0.25 MB 以下のトランザクションの場合、デフォルトの TTL は 3 秒です。詳細については、 [`LockNotFound`エラー](/troubleshoot-lock-conflicts.md#locknotfound-error)参照してください。

-   7.2.4 `PessimisticLockNotFound` .

    `TxnLockNotFound`と同様です。悲観的トランザクションのコミットが遅すぎるため、他のトランザクションによってロールバックされます。

-   7.2.5 `stale_epoch` .

    リクエスト エポックが古いため、TiDB はルーティングを更新した後にリクエストを再送信します。ビジネスには影響しません。リージョンで分割/マージ操作が行われるか、レプリカが移行されると、エポックが変更されます。

-   7.2.6 `peer is not leader` .

    リクエストはLeaderではないレプリカに送信されます。エラー応答にどのレプリカが最新のLeaderであるかが示されている場合、TiDB はエラーに従ってローカルルーティングを更新し、最新のLeaderに新しいリクエストを送信します。通常、業務には影響しません。

    v3.0 以降のバージョンでは、以前のLeaderへのリクエストが失敗した場合、TiDB は他のピアを試行するため、TiKV ログに`peer is not leader`頻繁に記録される可能性があります。送信失敗の根本原因を特定するには、TiDB の対応するリージョンの`switch region peer to next due to send request fail`ログを確認してください。詳細については、 [7.1.4](#71-tidb)を参照してください。

    このエラーは、他の理由によりリージョンにLeaderが存在しない場合にも返される可能性があります。詳細については、 [4.4](#44-some-tikv-nodes-drop-leader-frequently)参照してください。
