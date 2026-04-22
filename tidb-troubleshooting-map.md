---
title: TiDB Troubleshooting Map
summary: TiDBでよく発生するエラーのトラブルシューティング方法を学びましょう。
---

# TiDBトラブルシューティングマップ {#tidb-troubleshooting-map}

このドキュメントでは、TiDBおよびその他のコンポーネントでよく発生する問題をまとめています。関連する問題が発生した際には、このマップを使用して問題を診断し、解決することができます。

## 1. サービス利用不可 {#1-service-unavailable}

### 1.1 クライアントから<code>Region is Unavailable</code>エラーが報告されました {#1-1-the-client-reports-code-region-is-unavailable-code-error}

-   1.1.1 `Region is Unavailable`エラーは通常、リージョンが一定期間利用できないことが原因です。 `TiKV server is busy`が発生する場合や、 `not leader`または`epoch not match` } が原因で TiKV へのリクエストが失敗するか、TiKV へのリクエストがタイムアウトする場合があります。このような場合、TiDB は`backoff`再試行メカニズムを実行します。 `backoff`がしきい値 (デフォルトでは 20 秒) を超えると、エラーがクライアントに送信されます。 `backoff`のしきい値内であれば、このエラーはクライアントには表示されません。

-   1.1.2 複数のTiKVインスタンスが同時にメモリ不足（OOM）になると、OOM期間中にLeaderが存在しない状態になります。中国語版の[ケース991](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case991.md)参照してください。

-   1.1.3 TiKV は`TiKV server is busy`を報告し、 `backoff`時間を超過します。詳細については、 [4.3](#43-the-client-reports-the-server-is-busy-error)を参照してください。 `TiKV server is busy`は内部フロー制御メカニズムの結果であり、 `backoff`時間にカウントされるべきではありません。この問題は修正されます。

-   1.1.4 複数の TiKV インスタンスの起動に失敗し、リージョンにLeaderが存在しない状態になる。物理マシンに複数の TiKV インスタンスがデプロイされている場合、ラベルが正しく設定されていないと、物理マシンの障害によってリージョンにLeaderが存在しない状態になることがあります。中国語の[ケース228](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case228.md)参照してください。

-   1.1.5Followerの申請が前のエポックで遅延した場合、FollowerがLeaderになった後、 `epoch not match`を使用してリクエストを拒否します。中国語の[ケース958](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case958.md)参照してください（TiKV はそのメカニズムを最適化する必要があります）。

### 1.2 PDエラーによりサービスが利用できなくなる {#1-2-pd-errors-cause-service-unavailable}

[5つのPD問題](#5-pd-issues)を参照。

## 2. 遅延が大幅に増加する {#2-latency-increases-significantly}

### 2.1 一時的な増加 {#2-1-transient-increase}

-   2.1.1 TiDB の実行プランが間違っているとレイテンシーが増加します[3.3](#33-wrong-execution-plan)を参照してください。
-   2.1.2 PDLeader選挙問題またはOOM。5.2および[5.2](#52-pd-election) [5.3](#53-pd-oom)参照してください。
-   2.1.3 一部のTiKVインスタンスでLeaderが多数ドロップする[4.4](#44-some-tikv-nodes-drop-leader-frequently)を参照。
-   2.1.4 他の原因については、[読み取り/書き込みレイテンシの増加に関するトラブルシューティング](/troubleshoot-cpu-issues.md)参照してください。

### 2.2 持続的かつ著しい増加 {#2-2-persistent-and-significant-increase}

-   2.2.1 TiKVシングルスレッドのボトルネック

    -   TiKVインスタンス内のリージョンが多すぎると、単一のgRPCスレッドがボトルネックになります（ **Grafana** -&gt; **TiKV-details** -&gt; **Thread CPU/gRPC CPU Per Thread**メトリックを確認してください）。v3.x以降のバージョンでは、 `Hibernate Region`を有効にすることでこの問題を解決できます。中国語の[ケース612](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case612.md)参照してください。

    -   v3.0より前のバージョンでは、raftstoreスレッドまたはapplyスレッドがボトルネックになった場合（ **Grafana** -&gt; **TiKV-details** -&gt; **Thread CPU/raft store CPU**および**Async apply CPU**メトリクスが`80%`を超える場合）、TiKV（v2.x）インスタンスをスケールアウトするか、マルチスレッド対応のv3.xにアップグレードできます。 <!-- See [case-517](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case517.md) in Chinese. -->

-   2.2.2 CPU負荷が増加する。

-   2.2.3 TiKV の書き込み速度が遅い[4.5](#45-tikv-write-is-slow)を参照してください。

-   2.2.4 TiDB の実行プランが間違っています[3.3](#33-wrong-execution-plan)を参照してください。

-   2.2.5 他の原因については、[読み取り/書き込みレイテンシの増加に関するトラブルシューティング](/troubleshoot-cpu-issues.md)参照してください。

## 3. TiDBの問題 {#3-tidb-issues}

### 3.1 DDL {#3-1-ddl}

-   3.1.1 `ERROR 1105 (HY000): unsupported modify decimal column precision`フィールドの長さを変更すると、エラー`decimal`が報告されます。 <!--See [case-1004](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case517.md) in Chinese.--> TiDB は`decimal`フィールドの長さを変更することをサポートしていません。

-   3.1.2 TiDB DDL ジョブがハングアップするか、実行が遅くなる（DDL の進行状況を確認するには`admin show ddl jobs`を使用してください）

    -   原因1：TiDBはv6.3.0で「[メタデータロック](/metadata-lock.md)を導入し、v6.5.0以降のバージョンではデフォルトで有効にしています。DDL操作に関わるテーブルが、コミットされていないトランザクションに関わるテーブルと重複している場合、トランザクションがコミットまたはロールバックされるまでDDL操作はブロックされます。

    -   原因2：他のコンポーネント（PD/TiKV）とのネットワークの問題。

    -   原因3：TiDBの初期バージョン（v3.0.8より前）は、多数のゴルーチンが高並行性で動作するため、内部負荷が非常に高い。

    -   原因4：初期バージョン（v2.1.15およびv3.0.0-rc1未満のバージョン）では、PDインスタンスがTiDBキーを削除できず、すべてのDDL変更が2リース分待機することになります。

    -   その他の原因不明の場合は[バグを報告する](https://github.com/pingcap/tidb/issues/new?labels=type%2Fbug&#x26;template=bug-report.md)。

    -   解決：

        -   原因1については、TiDBとTiKV/PD間のネットワーク接続を確認してください。
        -   原因2と3については、後のバージョンで既に修正されています。TiDBを最新バージョンにアップグレードしてください。
        -   その他の原因については、DDL所有者を移行するという以下の解決策を使用できます。

    -   DDL所有者の移行:

        -   TiDBサーバーに接続できる場合は、所有者選出コマンドを再度実行してください： `curl -X POST http://{TiDBIP}:10080/ddl/owner/resign`
        -   TiDBサーバーに接続できない場合は、 `tidb-ctl`を使用してPDクラスタのetcdからDDLオーナーを削除し、再選出をトリガーしてください： `tidb-ctl etcd delowner [LeaseID] [flags] + ownerKey`

-   3.1.3 TiDB のログに`information schema is changed`エラーが報告される

    -   詳細な原因と解決策については、 [`Information schema is changed`エラーが報告される理由](/faq/sql-faq.md#what-triggers-the-information-schema-is-changed-error)を参照してください。

    -   背景： `schema version`の増加数は、各 DDL 変更操作の`schema state`の数と一致しています。たとえば、 `create table`操作ではバージョン変更が 1 回、 `add column`操作ではバージョン変更が 4 回発生します。したがって、列変更操作が多すぎると`schema version`急速に増加する可能性があります。詳細は[オンラインスキーマの変更](https://static.googleusercontent.com/media/research.google.com/zh-CN//pubs/archive/41376.pdf)を参照してください。

-   3.1.4 TiDB はログに`information schema is out of date`を報告します

    -   原因1：DMLステートメントを実行しているTiDBサーバーが`graceful kill`によって停止され、終了準備状態になります。DMLステートメントを含むトランザクションの実行時間が1つのDDLリースを超えています。トランザクションのコミット時にエラーが報告されます。

    -   原因2：TiDBサーバーがDMLステートメントの実行中にPDまたはTiKVに接続できません。その結果、TiDBサーバーは1つのDDLリース（デフォルトでは`45s`内に新しいスキーマをロードできなかったか、TiDBサーバーが`keep alive`設定でPDから切断されました。

    -   原因3：TiKVの負荷が高いか、ネットワークがタイムアウトしました。Grafana**の****TiDB**と**TiKV**でノードの負荷を確認してください。

    -   解決：

        -   原因1については、TiDB起動時にDML操作を再試行してください。
        -   原因2については、TiDBサーバーとPD/TiKV間のネットワークを確認してください。
        -   原因 3 については、TiKV がビジーである理由を調査します。 [TiKVに関する4つの問題](#4-tikv-issues)を参照。

### 3.2 メモリ不足の問題 {#3-2-oom-issues}

-   3.2.1 症状

    -   クライアント: クライアントからエラー`ERROR 2013 (HY000): Lost connection to MySQL server during query`が報告されました。

    -   ログを確認してください

        -   `dmesg -T | grep tidb-server`を実行してください。結果として、エラーが発生した時点付近の OOM-killer ログが表示されます。

        -   エラーが発生した時点（つまり、tidb-serverが再起動した時点）の前後の`tidb.log`にある「Welcome to TiDB」ログをgrepします。

        -   `fatal error: runtime: out of memory`または`cannot allocate memory` `tidb_stderr.log`内で検索します。

        -   v2.1.8以前のバージョンでは、 `fatal error: stack overflow`内で`tidb_stderr.log` } を grep できます。

    -   監視：tidb-serverインスタンスのメモリ使用量が短時間で急激に増加します。

-   3.2.2 OOMを引き起こすSQL文を特定します。（現在、TiDBのすべてのバージョンではSQL文を正確に特定できません。SQL文を特定した後、OOMがそのSQL文によって引き起こされているかどうかを分析する必要があります。）

    -   バージョン3.0.0以降の場合、 `tidb.log`内の「expensive_query」をgrepしてください。このログメッセージには、タイムアウトした、またはメモリ割り当て量を超過したSQLクエリが記録されています。

    -   バージョンが v3.0.0 未満の場合、 `tidb.log`で &quot;メモリ exceeded quota&quot; を grep して、メモリクォータを超える SQL クエリを特定します。

    > **注記：**
    >
    > 単一の SQLメモリ使用量のデフォルトのしきい値は`1GB`です。このパラメータは、システム変数[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)設定することで設定できます。

-   3.2.3 メモリ不足問題​​の軽減

    -   `SWAP`を有効にすることで、大規模クエリによるメモリの過剰使用が原因で発生する OOM の問題を軽減できます。メモリが不足している場合、この方法は I/O オーバーヘッドにより大規模クエリのパフォーマンスに影響を与える可能性があります。パフォーマンスへの影響の程度は、残りのメモリ容量とディスク I/O 速度によって異なります。

-   3.2.4 メモリ不足が発生する典型的な理由

    -   SQL クエリには`join`が含まれています。 `explain`を使用して SQL ステートメントを表示すると、 `join`操作で`HashJoin`アルゴリズムが選択され、 `inner`テーブルが大きいことがわかります。

    -   単一の`UPDATE/DELETE`クエリのデータ量が大きすぎます。中国語の[ケース882](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case882.md)参照してください。

    -   SQL文には`Union`で接続された複数のサブクエリが含まれています。中国語版の[ケース1828](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case1828.md)を参照してください。

OOM のトラブルシューティングの詳細については、 [TiDBのメモリ不足問題​​のトラブルシューティング](/troubleshoot-tidb-oom.md)を参照してください。

### 3.3 実行計画の誤り {#3-3-wrong-execution-plan}

-   3.3.1 症状

    -   SQLクエリの実行時間が以前の実行時と比べて大幅に長くなっている、または実行プランが突然変更されている場合。実行プランがスローログに記録されている場合は、実行プランを直接比較できます。

    -   SQLクエリの実行時間は、MySQLなどの他のデータベースと比較して非常に長くなっています。 `Join Order`などの他のデータベースと実行プランを比較して違いを確認してください。

    -   スローログでは、SQL実行時間`Scan Keys`の数が多くなっています。

-   3.3.2 実行計画の調査

    -   `explain analyze {SQL}` 。実行時間が許容範囲内であれば、 `count`の結果の`explain analyze`と`row`の`execution info` 3-PLACEHOLDER-E}} の数を比較します。 `TableScan/IndexScan`行で大きな差が見つかった場合は、統計情報が間違っている可能性があります。他の行で大きな差が見つかった場合は、統計情報に問題がない可能性があります。

    -   `select count(*)` 。実行プランに`join`操作が含まれている場合、 `explain analyze`の実行に時間がかかる場合があります。 `select count(*)`を実行し、 `TableScan/IndexScan`の結果に含まれる`row count`の情報を比較することで、 `explain`情報にあるかどうかを確認できます。

-   3.3.3 緩和策

    -   v3.0以降のバージョンでは、 `SQL Bind`機能を使用して実行プランをバインドします。

    -   統計情報を更新します。問題の原因が統計情報にあるとおおよそ確信できる場合は、[統計情報を捨てる](/statistics.md#export-statistics)。原因が古い統計情報である場合、例えば`modify count/row count`の`show stats_meta`が特定の値 (例えば 0.3) より大きい場合、またはテーブルに時間列のインデックスがある場合、 `analyze table`を使用して復旧を試みることもできます。 `auto analyze`が設定されている場合は、 `tidb_auto_analyze_ratio`システム変数が大きすぎる (例えば 0.3 より大きい) かどうか、および現在時刻が`tidb_auto_analyze_start_time`と`tidb_auto_analyze_end_time`の間にあるかどうかを確認してください。

    -   その他の状況については、 [バグを報告する](https://github.com/pingcap/tidb/issues/new?labels=type%2Fbug&#x26;template=bug-report.md)。

### 3.4 SQL実行エラー {#3-4-sql-execution-error}

-   3.4.1 クライアントは`ERROR 1265(01000) Data Truncated`エラーを報告します。これは、TiDB が内部的に`Decimal`型の精度を計算する方法が MySQL の計算方法と互換性がないためです。この問題は v3.0.10 ( [#14438](https://github.com/pingcap/tidb/pull/14438) ) で修正されました。

    -   原因：

        MySQL では、2 つの大きな精度`Decimal`を割り算し、結果が最大小数精度 ( `30`を超える場合、 `30`桁のみが予約され、エラーは報告されません。

        TiDB では、計算結果は MySQL と同じですが、 `Decimal`を表すデータ構造内では、小数点精度のフィールドが実際の精度を保持します。

        `(0.1^30) / 10`例にとってみましょう。TiDB と MySQL の結果はどちらも`0`です。これは、精度が最大でも`30`だからです。ただし、TiDB では、10 進精度のフィールドは依然として`31`です。

        `Decimal`の除算を複数回行った後、結果は正しいものの、この精度フィールドはどんどん大きくなり、最終的に TiDB のしきい値 ( `72`超え、 `Data Truncated`エラーが報告されます。

        `Decimal`の乗算では、範囲外が回避され、精度が最大精度制限に設定されるため、この問題は発生しません。

    -   解決策： `Cast(xx as decimal(a, b))`と`a`目標精度として、 `b` } を手動で追加することで、この問題を回避できます。

### 3.5 クエリの遅延に関する問題 {#3-5-slow-query-issues}

遅いクエリを特定するには、[遅いクエリを特定する](/identify-slow-queries.md)参照してください。遅いクエリを分析して処理するには、[遅いクエリを分析する](/analyze-slow-queries.md)参照してください。

### 3.6 ホットスポットの問題 {#3-6-hotspot-issues}

分散データベースであるTiDBは、サーバーリソースをより有効活用するために、アプリケーションの負荷をさまざまなコンピューティングノードやstorageノードに均等に分散させるロードバランシングメカニズムを備えています。しかし、特定のシナリオでは、アプリケーションの負荷が適切に分散されない場合があり、パフォーマンスに影響を与え、ホットスポットと呼ばれる高負荷の一点が発生する可能性があります。

TiDB は、ホットスポットのトラブルシューティング、解決、回避のための完全なソリューションを提供します。負荷ホットスポットのバランスをとることで、QPS の向上やレイテンシーの削減など、全体的なパフォーマンスを向上させることができます。詳細な解決策については、[ホットスポットの問題をトラブルシューティングする](/troubleshoot-hot-spot-issues.md)参照してください。

### 3.7 ディスクI/O使用率が高い {#3-7-high-disk-i-o-usage}

CPU ボトルネックとトランザクションの競合によって引き起こされるボトルネックのトラブルシューティングを行った後に TiDB の応答が遅くなった場合は、現在のシステム ボトルネックを特定するために I/O メトリックを確認する必要があります。 TiDB での高い I/O 使用率の問題を特定して処理する方法については、[ディスクI/O使用率が高い場合のトラブルシューティング](/troubleshoot-high-disk-io.md)参照してください。

### 3.8 ロックの競合 {#3-8-lock-conflicts}

TiDB は完全な分散トランザクションをサポートします。 v3.0 以降、TiDB は楽観的トランザクション モードと悲観的トランザクション モードを提供します。ロック関連の問題のトラブルシューティング方法、および楽観的ロックと悲観的ロックの競合の処理方法については、[ロックの競合をトラブルシューティングする](/troubleshoot-lock-conflicts.md)参照してください。

### 3.9 データと指標の不整合 {#3-9-inconsistency-between-data-and-indexes}

TiDB は、トランザクションの実行時または[`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md)ステートメントの実行時に、データとインデックスの一貫性をチェックします。チェックの結果、レコードのキーと値、および対応するインデックスのキーと値が一致しない、つまり、行データを格納するキーと値のペアと、そのインデックスを格納する対応するキーと値のペアが一致しない（例えば、インデックスが多すぎる、またはインデックスが欠落している）ことが判明した場合、TiDB はデータ不整合エラーを報告し、関連するエラーをエラー ログに出力。

不整合エラーとチェックを回避する方法の詳細については、 [データとインデックス間の不整合のトラブルシューティング](/troubleshoot-data-inconsistency-errors.md)参照してください。

## 4. TiKVに関する問題 {#4-tikv-issues}

### 4.1 TiKVがパニックを起こして起動に失敗する {#4-1-tikv-panics-and-fails-to-start}

-   4.1.1 TiKVが仮想マシンにデプロイされている場合、仮想マシンが強制終了されたり、物理マシンが電源オフになったりすると、 `entries[X, Y] is unavailable from storage`エラーが報告されます。

    この問題は想定内のものです。仮想マシンの`fsync`は信頼性が低いため、 `tikv-ctl`を使用してリージョンを復元する必要があります。

-   4.1.2 その他の予期せぬ原因については、 [バグを報告する](https://github.com/tikv/tikv/issues/new?template=bug-report.md)。

### 4.2 TiKV OOM {#4-2-tikv-oom}

-   4.2.1 `block-cache`の設定が大きすぎると、メモリ不足が発生する可能性があります。

    問題の原因を確認するには、モニター**Grafana** -&gt; **TiKV-details**で該当するインスタンスを選択して RocksDB の`block cache size`を確認してください。

    一方、 `[storage.block-cache] capacity = # "1GB"`パラメータが正しく設定されているか確認してください。デフォルトでは、TiKV の`block-cache`はマシンの総メモリの`45%`に設定されています。TiKV は物理マシンのメモリを取得するため、コンテナのメモリ制限を超える可能性があるため、コンテナに TiKV をデプロイする際にはこのパラメータを明示的に指定する必要があります。

-   4.2.2コプロセッサーが多数の大きなクエリを受信し、大量のデータを返します。gRPC は、コプロセッサがデータを返す速度に追いつかず、結果としてメモリ不足エラーが発生します。

    原因を確認するには、モニター**Grafana** -&gt; **TiKV-details** -&gt; coprocessor overview を表示して`response size`が`network outbound`のトラフィックを超えているかどうかを確認でき**ます**。

-   4.2.3 他のコンポーネントがメモリを過剰に消費している。

    この問題は予期せぬものです。 [バグを報告する](https://github.com/tikv/tikv/issues/new?template=bug-report.md)ことができます。

### 4.3 クライアントが<code>server is busy</code>と報告するエラー {#4-3-the-client-reports-the-code-server-is-busy-code-error}

ビジー状態の具体的な原因を確認するには、モニター**Grafana** -&gt; **TiKV** -&gt; **errors を**確認してください。 `server is busy` 、TiKV のフロー制御メカニズムが原因で発生しており、TiKV が現在過負荷状態にあるため後で再試行することを`tidb/ti-client`に通知します。

-   4.3.1 TiKV RocksDB は`write stall`を検出します。

    TiKV インスタンスには 2 つの RocksDB インスタンスがあり、1 つは`data/raft`にありRaftログを格納し、もう 1 つは`data/db`にあり実際のデータを格納します。ログで`grep "Stalling" RocksDB`を実行すると、停止の具体的な原因を確認できます。RocksDB ログは`LOG`で始まるファイルで、 `LOG`が現在のログです。 `write stall`は RocksDB にネイティブに組み込まれたパフォーマンス低下メカニズムです。RocksDB で`write stall`が発生すると、システムのパフォーマンスが大幅に低下します。バージョン 5.2.0 より前のバージョンでは、TiDB は`ServerIsBusy`に遭遇すると、 `write stall`エラーをクライアントに直接返すことで、すべての書き込み要求をブロックしようとしますが、これにより QPS パフォーマンスが急激に低下する可能性があります。バージョン 5.2.0 以降、TiKV は、スケジューリングレイヤーで書き込み要求を動的に遅延させることで書き込みを抑制する新しいフロー制御メカニズムを導入し、 `server is busy`が発生したときにクライアントに`write stall`を返す以前のメカニズムに取って代わります。新しいフロー制御メカニズムはデフォルトで有効になっており、TiKV は`write stall`および`KvDB` (memtable を除く) の`RaftDB`メカニズムを自動的に無効にします。ただし、保留中のリクエスト数が一定のしきい値を超えると、フロー制御メカニズムは引き続き有効になり、一部またはすべての書き込みリクエストを拒否し、 `server is busy`エラーをクライアントに返します。詳細な説明としきい値については、 [フロー制御構成](/tikv-configuration-file.md#storageflow-control)を参照してください。

    -   `server is busy`エラーが、保留中の圧縮バイト数が多すぎるために発生する場合は、 [`soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit)および[`hard-pending-compaction-bytes-limit`](/tikv-configuration-file.md#hard-pending-compaction-bytes-limit)パラメータの値を増やすことで、この問題を軽減できます。

        -   保留中の圧縮バイト数が`soft-pending-compaction-bytes-limit`パラメータの値 (デフォルトでは`192GiB` ) に達すると、フロー制御メカニズムは一部の書き込み要求を拒否し始めます ( `ServerIsBusy`をクライアントに返します)。この場合、このパラメータの値を増やすことができます。たとえば、 `[storage.flow-control] soft-pending-compaction-bytes-limit = "384GiB"`のようにです。

        -   保留中の圧縮バイト数が`hard-pending-compaction-bytes-limit`パラメータの値 (デフォルトでは`1024GiB` ) に達すると、フロー制御メカニズムはすべての書き込み要求を拒否し始めます ( `ServerIsBusy`をクライアントに返します)。フロー制御メカニズムは`soft-pending-compaction-bytes-limit`のしきい値に達した後に書き込み速度を遅くするため、このシナリオが発生する可能性は低くなります。発生した場合は、このパラメータの値を増やすことができます (たとえば`[storage.flow-control] hard-pending-compaction-bytes-limit = "2048GiB"`など)。

        -   ディスクのI/O容量が長時間にわたって書き込み速度に追いつかない場合は、ディスクの容量を増やすことをお勧めします。ディスクのスループットが上限に達し、書き込みが停止する場合（例えば、SATA SSDはNVMe SSDよりも大幅に低い）、CPUリソースが十分であれば、より高い圧縮率の圧縮アルゴリズムを適用することができます。こうすることで、CPUリソースをディスクリソースに振り向け、ディスクへの負荷を軽減できます。

        -   デフォルトのCF圧縮で高圧が検出された場合は、 `[rocksdb.defaultcf] compression-per-level`パラメータを`["no", "no", "lz4", "lz4", "lz4", "zstd", "zstd"]`から`["no", "no", "zstd", "zstd", "zstd", "zstd", "zstd"]`に変更します。

    -   memtable が多すぎると、処理が停止します。これは通常、インスタント書き込みの量が多く、memtable がディスクにフラッシュされるのが遅い場合に発生します。ディスク書き込み速度を改善できない場合、またこの問題が業務のピーク時にのみ発生する場合は、対応する CF の`max-write-buffer-number`を増やすことで軽減できます。

        -   例えば、 `[rocksdb.defaultcf] max-write-buffer-number`を`8`に設定します (デフォルトでは`5`です)。ただし、これにより、メモリ内に保持される memtable が増えるため、ピーク時のメモリ使用量が増加する可能性があることに注意してください。

-   4.3.2 `scheduler too busy`

    -   深刻な書き込み競合が発生しています。 `latch wait duration`値が高くなります。モニター**Grafana** -&gt; **TiKV-details** -&gt; **scheduler prewrite** / **scheduler commit**で`latch wait duration`を確認できます。スケジューラで書き込みタスクが蓄積されると、保留中の書き込みタスクが`[storage] scheduler-pending-write-threshold` (100MB) で設定されたしきい値を超えます。 `MVCC_CONFLICT_COUNTER`に対応するメトリックを確認することで、原因を検証できます。

    -   書き込み速度が遅いと、書き込みタスクが蓄積されます。TiKV に書き込まれるデータが`[storage] scheduler-pending-write-threshold` (100MB) で設定されたしきい値を超えています[4.5](#45-tikv-write-is-slow)を参照してください。

-   4.3.3 `raftstore is busy` 。メッセージの処理がメッセージの受信よりも遅くなっています。短期間の`channel full`状態はサービスに影響しませんが、エラーが長時間続くとLeaderの切り替えが発生する可能性があります。

    -   `append log`は停止に遭遇します[4.3.1](#43-the-client-reports-the-server-is-busy-error)を参照してください。
    -   `append log duration`値が高いため、メッセージの処理が遅くなります。 `append log duration`値が高い理由については、 [4.5](#45-tikv-write-is-slow)を参照してください。
    -   raftstore は、大量のメッセージを瞬時に受信し (TiKV Raftメッセージ ダッシュボードで確認できます)、処理に失敗します。通常、この一時的な`channel full`ステータスはサービスに影響を与えません。

-   4.3.4 TiKV コプロセッサがキューに入っています。スタックされたタスクの数が`coprocessor threads * readpool.coprocessor.max-tasks-per-worker-[normal|low|high]`を超えています。大きなクエリが多すぎると、コプロセッサでタスクがスタックされます。実行プランの変更によってテーブルスキャン操作が大量に発生していないか確認する必要があります[3.3](#33-wrong-execution-plan)を参照してください。

### 4.4 一部のTiKVノードは頻繁にLeaderをドロップする {#4-4-some-tikv-nodes-drop-leader-frequently}

-   4.4.1 TiKVが再起動されたため再選が行われる

    -   TiKVがパニックを起こした後、systemdによって起動され、正常に動作します。TiKVログを確認することで[バグを報告する](https://github.com/tikv/tikv/issues/new?template=bug-report.md)panicが発生したかどうかを確認できます。この問題は予期しないため、発生した場合。

    -   TiKV が第三者によって停止または強制終了され、その後 systemd によって起動されました。原因を確認するには`dmesg`と TiKV ログを参照してください。

    -   TiKV がメモリ不足のため再起動します[4.2](#42-tikv-oom)を参照してください。

    -   TiKV は、 `THP` (透明巨大ページ) の動的な調整が原因でハングアップしています。中国語の[ケース500](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case500.md)参照してください。

-   4.4.2 TiKV RocksDB で書き込み停止が発生し、再選出が行われます。モニター**Grafana** -&gt; **TiKV-details** -&gt; **errors**に`server is busy`が表示されているかどうかを確認してください[4.3.1](#43-the-client-reports-the-server-is-busy-error)を参照してください。

-   4.4.3 ネットワークの孤立による再選出。

### 4.5 TiKVへの書き込みが遅い {#4-5-tikv-write-is-slow}

-   4.5.1 TiKV gRPC の`prewrite/commit/raw-put`の継続時間を表示して、TiKV 書き込みが遅いかどうかを確認します (RawKV クラスターの場合のみ)。一般に、 [パフォーマンスマップ](https://github.com/pingcap/tidb-map/blob/master/maps/performance-map.png)に従って遅い段階を特定できます。よくある状況のいくつかを以下に示します。

-   4.5.2 スケジューラのCPUがビジー状態です（トランザクションkvのみ）。

    prewrite/commit の`scheduler command duration`が`scheduler latch wait duration`と`storage async write duration`の合計よりも長くなっています。スケジューラワーカーの CPU 要求が高く、例えば`scheduler-worker-pool-size` * 100% の 80% を超えているか、マシン全体の CPU リソースが比較的限られています。書き込みワークロードが大きい場合は、 `[storage] scheduler-worker-pool-size`の設定が小さすぎないか確認してください。

    その他の状況については、 [バグを報告する](https://github.com/tikv/tikv/issues/new?template=bug-report.md)。

-   4.5.3 ログの追加処理が遅い。

    TiKV Grafana の**Raft IO** / `append log duration`値が高い場合、通常はディスク書き込み操作が遅いことが原因です。RocksDB - raft の`WAL Sync Duration max`の値を確認することで原因を特定できます。

    その他の状況については、 [バグを報告する](https://github.com/tikv/tikv/issues/new?template=bug-report.md)。

-   4.5.4 raftstore スレッドがビジー状態です。

    **Raft Propose** / `propose wait duration`は、TiKV Grafana の追記ログ期間よりもかなり長くなっています。以下の方法を試してください。

    -   `[raftstore] store-pool-size`の設定値が小さすぎないか確認してください。値は`1`と`5`の間に設定し、大きすぎないようにすることをお勧めします。
    -   マシンのCPUリソースが不足していないか確認してください。

-   4.5.5 適用処理が遅い。

    TiKV Grafana の**Raft IO** / `apply log duration`高い状態です。これは通常、 **Raft Propose** / `apply wait duration`高い状態と関連しています。考えられる原因は以下のとおりです。

    -   `[raftstore] apply-pool-size`が小さすぎます ( `1`と`5`の間に値を設定し、大きすぎないようにすることをお勧めします)。また、 **Thread CPU** / `apply CPU`が大きいです。

    -   マシンのCPUリソースが不足しています。

    -   リージョン書き込みホットスポット。単一の適用スレッドでCPU使用率が高くなっています。現在、単一のリージョンでのホットスポット問題を適切に処理することはできませんが、改善中です。各スレッドのCPU使用率を表示するには、Grafana式を変更して`by (instance, name)`を追加してください。

    -   RocksDBへの書き込みが遅い。RocksDB**のkv** / `max write duration`が高い。1つのRaftログに複数のKVが含まれる可能性がある。RocksDBへの書き込み時には、1回の書き込みバッチで128個のKVがRocksDBに書き込まれる。そのため、適用ログはRocksDBへの複数の書き込みに関連付けられる可能性がある。

    -   その他の状況については、 [バグを報告する](https://github.com/tikv/tikv/issues/new?template=bug-report.md)。

-   4.5.6 Raftのコミットログが遅い。

    TiKV Grafana の**Raft IO** / `commit log duration`が高い (このメトリックは Grafana v4.x 以降でのみサポートされています)。各リージョンは独立したRaftグループに対応します。Raftには、TCP のスライディング ウィンドウ メカニズムと同様のフロー制御メカニズムがあります。スライディング ウィンドウのサイズは`[raftstore] raft-max-inflight-msgs = 256`パラメータを設定することで制御できます。書き込みホットスポットがあり、 `commit log duration`が高い場合は、 `1024`に増やすなど、パラメータを調整できます。

-   4.5.7 その他の場合は、 [パフォーマンスマップ](https://github.com/pingcap/tidb-map/blob/master/maps/performance-map.png)上の書き込みパスを参照し、原因を分析してください。

## 5. PD問題 {#5-pd-issues}

### 5.1 PDスケジューリング {#5-1-pd-scheduling}

-   5.1.1 マージ

    -   テーブルをまたいで空の領域はマージできません。TiKV の`[coprocessor] split-region-on-table`パラメータを変更する必要があります。このパラメータは、v4.x ではデフォルトで`false`に設定されています。詳細は中国語の[ケース896](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case896.md)参照してください。

    -   リージョンのマージは遅いです。マージされたオペレーターが生成されているかどうかは、 **Grafana** -&gt; **PD** -&gt; **operator**のモニターダッシュボードにアクセスして確認できます。マージを高速化するには、 `merge-schedule-limit`の値を増やしてください。

-   5.1.2 レプリカの追加またはオンライン/オフラインでのレプリカの削除

    -   TiKVディスクが容量の80%を使用し、PDがレプリカを追加しない場合、ミスピア数が増加するため、TiKVをスケールアウトする必要があります。詳細は中国語版の[ケース801](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case801.md)を参照してください。

    -   TiKVノードがオフラインになると、一部のリージョンを他のノードに移行できなくなる問題がありました。この問題はv3.0.4で修正されました（ [#5526](https://github.com/tikv/tikv/pull/5526) ）。中国語版の[ケース870](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case870.md)参照してください。

-   5.1.3 バランス

    -   Leader/リージョンの数が均等に分布していません。中国語の[ケース394](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case394.md)と[ケース759](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case759.md)を参照してください。主な原因は、バランス調整がリージョン/Leaderのサイズに基づいてスケジューリングを実行するため、数の分布が不均等になる可能性があることです。TiDB 4.0では、 `[leader-schedule-policy]`パラメータが導入され、Leaderのスケジューリングポリシーを`count`ベースまたは`size`ベースに設定できるようになりました。

### 5.2 PD選挙 {#5-2-pd-election}

-   5.2.1 PD スイッチLeader。

    -   原因1：ディスク。PDノードが配置されているディスクのI/O負荷が最大になっています。PDがI/O負荷の高い他のコンポーネントと一緒にデプロイされているかどうか、およびディスクの状態を調査してください。Grafana**の**「**ディスクパフォ​​ーマンス**」→ **「レイテンシー**/**負荷」**でモニターメトリックを確認することで原因を特定できます。必要に応じて、FIOツールを使用してディスクのチェックを実行することもできます。中国語の[ケース292](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case292.md)参照してください。

    -   原因 2: ネットワーク。PD ログに`lost the TCP streaming connection`が表示されます。PD ノード間のネットワークに問題がないか確認し、モニター**Grafana** -&gt; **PD** -&gt; **etcd**で`round trip`を表示して原因を検証する必要があります。中国語の[ケース177](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case177.md)参照してください。

    -   原因3：システム負荷が高い。ログには`server is likely overloaded`と表示されます。中国語の[ケース214](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case214.md)参照してください。

-   5.2.2 PDはLeaderを選出できないか、選挙が遅い。

    -   PD はLeaderを選出できません: PD ログには`lease is not expired`が表示されます。 [この問題は](https://github.com/etcd-io/etcd/issues/10355)v3.0.x および v2.1.19 で修正されました。中国語の[ケース875](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case875.md)参照してください。

    -   選挙が遅い：リージョンの読み込み時間が長い。この問題は、PD ログで`grep "regions cost"`実行することで確認できます。結果が`load 460927 regions cost 11.77099s`のように秒単位の場合、リージョンの読み込みが遅いことを意味します。v3.0 では、 `region storage`を`use-region-storage`に設定することで`true`機能を有効にでき、リージョンの読み込み時間を大幅に短縮できます。詳細は、 [ケース429](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case429.md) （中国語）を参照してください。

-   5.2.3 TiDBがSQLステートメントを実行する際にPDがタイムアウトしました。

    -   PDにはLeaderが存在しない、またはLeaderが切り替わります[5.2.1](#52-pd-election)および[5.2.2](#52-pd-election)を参照してください。

    -   ネットワークの問題です。Grafana -&gt; **blackbox_exporter** -&gt; **ping レイテンシー**モニターにアクセスして、 **TiDB**から PD Leaderへのネットワークが正常に動作しているかどうかを確認してください。

    -   PD パニック。 [バグを報告する](https://github.com/pingcap/pd/issues/new?labels=kind%2Fbug&#x26;template=bug-report.md)。

    -   PDはOOMです[5.3](#53-pd-oom)を参照してください。

    -   問題に他の原因がある場合は、 `curl http://127.0.0.1:2379/debug/pprof/goroutine?debug=2`を実行して goroutine を取得し、 [バグを報告する](https://github.com/pingcap/pd/issues/new?labels=kind%2Fbug&#x26;template=bug-report.md)。

-   5.2.4 その他の問題

    -   PD は`FATAL`エラーを報告し、ログには`range failed to find revision pair`と表示されます。この問題は v3.0.8 ( [#2040](https://github.com/pingcap/pd/pull/2040) ) で修正されました。詳細は、中国語の[ケース947](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case947.md)参照してください。

    -   その他の状況については、 [バグを報告する](https://github.com/pingcap/pd/issues/new?labels=kind%2Fbug&#x26;template=bug-report.md)。

### 5.3 PD OOM {#5-3-pd-oom}

-   5.3.1 `/api/v1/regions`インターフェースを使用する場合、リージョンが多すぎると PD OOM が発生する可能性があります。この問題は v3.0.8 ( [#1986](https://github.com/pingcap/pd/pull/1986) ) で修正されました。

-   5.3.2 ローリングアップグレード中にPD OOMが発生します。gRPCメッセージのサイズに制限がなく、モニターにはTCP InSegsが比較的大きいことが示されています。この問題はv3.0.6で修正されました（ [#1952](https://github.com/pingcap/pd/pull/1952) ）。 <!--For details, see [case-852](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case852.md).-->

### 5.4 Grafanaの表示 {#5-4-grafana-display}

-   5.4.1 **Grafana** -&gt; **PD** -&gt; **cluster** -&gt; **role**のモニターにフォロワーが表示されます。Grafana の式に関する問題は v3.0.8 で修正されました。

## 6. エコシステムツール {#6-ecosystem-tools}

### 6.1 データ移行 {#6-1-data-migration}

-   6.1.1 TiDBデータ移行（DM）は、MySQL/MariaDBからTiDBへのデータ移行をサポートする移行ツールです。詳細については、 [DMの概要](/dm/dm-overview.md)参照してください。

-   6.1.2 `Access denied for user 'root'@'172.31.43.27' (using password: YES)` `query status`を実行したとき、またはログを確認したときに表示されます。

    -   すべてのDM設定ファイル内のデータベース関連のパスワードは`dmctl`で暗号化する必要があります。データベースパスワードが空の場合は、パスワードを暗号化する必要はありません。バージョン1.0.6以降では、平文パスワードを使用できます。
    -   DM 操作中、アップストリームおよびダウンストリーム データベースのユーザーは、対応する読み取りおよび書き込み権限を持っている必要があります。データ移行も、データ複製タスクの開始時に自動的に[対応する権限を事前チェックします](/dm/dm-precheck.md)。
    -   DM クラスターに異なるバージョンの DM-worker/DM-master/dmctl をデプロイするには、 [AskTUGに関するケーススタディ](https://pingkai.cn/tidbcommunity/forum/t/topic/1049/5)参照してください。

-   6.1.3 レプリケーション タスクが`driver: bad connection`エラーで中断されました。

    -   `driver: bad connection`エラーは、DM と下流の TiDB データベース間の接続で異常が発生したこと (ネットワーク障害や TiDB の再起動など) と、現在のリクエストのデータがまだ TiDB に送信されていないことを示しています。

        -   DM 1.0.0 GA より前のバージョンでは、 `stop-task`を実行してタスクを停止し、 `start-task`を実行してタスクを再起動します。
        -   DM 1.0.0 GA以降のバージョンでは、この種のエラーに対する自動再試行メカニズムが追加されています。詳細は[#265](https://github.com/pingcap/dm/pull/265)を参照してください。

-   6.1.4 レプリケーション タスクが`invalid connection`エラーで中断されました。

    -   `invalid connection`エラーは、DM と下流の TiDB データベース間の接続で異常 (ネットワーク障害、TiDB の再起動、TiKV のビジーなど) が発生し、現在のリクエストのデータの一部が TiDB に送信されたことを示しています。DM はレプリケーション タスクで下流にデータを同時にレプリケートする機能があるため、タスクが中断されるといくつかのエラーが発生する可能性があります。これらのエラーは`query-status`または`query-error`を実行して確認できます。

        -   増分レプリケーション処理中に`invalid connection`エラーのみが発生した場合、DM はタスクを自動的に再試行します。
        -   DM がリトライしない、またはバージョン問題のために自動的にリトライできない場合 (自動リトライは v1.0.0-rc.1 で導入されました)、 `stop-task`を使用してタスクを停止し、 `start-task`を使用してタスクを再起動します。

-   6.1.5 リレーユニットがエラー`event from * in * diff from passed-in event *`を報告するか、レプリケーション タスクがbinlogの取得または解析に失敗するエラー（例: `get binlog error ERROR 1236 (HY000) and binlog checksum mismatch, data may be corrupted returned`で中断される。

    -   DMがリレーログを取得するプロセス、または増分レプリケーションのプロセス中に、アップストリームのbinlogファイルのサイズが4GBを超えると、次の2つのエラーが発生する可能性があります。

    -   原因：リレーログを書き込む際、DMはbinlogの位置とbinlogファイルのサイズに基づいてイベント検証を行い、複製されたbinlogの位置をチェックポイントとして保存する必要があります。しかし、公式のMySQLはbinlogの位置を保存するためにuint32を使用しているため、4GBを超えるbinlogファイルのbinlogの位置がオーバーフローし、上記のエラーが発生します。

    -   解決：

        -   中継処理装置の場合、 [レプリケーションを手動で復旧する](https://pingcap.com/docs/tidb-data-migration/dev/error-handling/#the-relay-unit-throws-error-event-from--in--diff-from-passed-in-event--or-a-replication-task-is-interrupted-with-failing-to-get-or-parse-binlog-errors-like-get-binlog-error-error-1236-hy000-and-binlog-checksum-mismatch-data-may-be-corrupted-returned)。
        -   binlogレプリケーション処理ユニットの場合、 [レプリケーションを手動で復旧する](https://pingcap.com/docs/tidb-data-migration/dev/error-handling/#the-relay-unit-throws-error-event-from--in--diff-from-passed-in-event--or-a-replication-task-is-interrupted-with-failing-to-get-or-parse-binlog-errors-like-get-binlog-error-error-1236-hy000-and-binlog-checksum-mismatch-data-may-be-corrupted-returned)。

-   6.1.6 DMレプリケーションが中断され、ログに`ERROR 1236 (HY000) The slave is connecting using CHANGE MASTER TO MASTER_AUTO_POSITION = 1, but the master has purged binary logs containing GTIDs that the slave requires.`が返されます。

    -   マスターbinlogがパージされているかどうかを確認してください。
    -   `relay.meta`に記録されている位置情報を確認してください。

        -   `relay.meta`は空の GTID 情報を記録しました。DM-worker は終了時または 30 秒ごとに、メモリ内の GTID 情報を`relay.meta`に保存します。DM-worker が上流の GTID 情報を取得できない場合は、空の GTID 情報を`relay.meta`に保存します。詳細は、 [ケース772](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case772.md) （中国語）を参照してください。

        -   `relay.meta`に記録されたbinlogイベントにより、不完全なリカバリプロセスがトリガーされ、誤ったGTID情報が記録されます。この問題はv1.0.2で修正されていますが、それ以前のバージョンでは発生する可能性があります。 <!--See [case-764](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case764.md).-->

-   6.1.7 DM レプリケーション プロセスでエラー`Error 1366: incorrect utf8 value eda0bdedb29d(\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd)`が返されます。

    -   この値は MySQL 8.0 または TiDB には正常に書き込めませんが、 MySQL 5.7には書き込めます。 `tidb_skip_utf8_check`パラメータを有効にすることで、データ形式のチェックをスキップできます。

### 6.2 TiDB Lightning {#6-2-tidb-lightning}

-   6.2.1 TiDB Lightningは、大量のデータを TiDB クラスタに高速に完全インポートするためのツールです。TiDB [TiDB Lightning （GitHub）](https://github.com/pingcap/tidb/tree/release-8.5/lightning)を参照してください。

-   6.2.2 インポート速度が遅すぎる。

    -   `region-concurrency`設定値が高すぎるため、スレッド競合が発生し、パフォーマンスが低下します。トラブルシューティング方法は次の 3 つです。

        -   設定は、ログの先頭から`region-concurrency`検索することで見つけることができます。
        -   TiDB Lightning が他のサービス (たとえば Importer) とサーバーを共有している場合は、 `region-concurrency`そのサーバーの CPU コアの総数の 75% に手動で設定する必要があります。
        -   CPU にクォータが設定されている場合 (例えば、Kubernetes の設定によって制限されている場合)、 TiDB Lightning はこの値を読み取れない可能性があります。この場合、 `region-concurrency`も手動で減らす必要があります。

    -   インデックスを追加するたびに、各行に新しいキーバリューペアが追加されます。インデックスがN個ある場合、実際にインポートされるサイズは、 [Dumpling](/dumpling-overview.md)出力のサイズのおよそ(N+1)倍になります。インデックスが無視できるほど小さい場合は、最初にスキーマからインデックスを削除し、インポート完了後に`CREATE INDEX`を使用して再度追加することができます。

    -   TiDB Lightningのバージョンが古いです。最新バージョンをお試しください。インポート速度が向上する可能性があります。

-   6.2.3 `checksum failed: checksum mismatched remote vs local` 。

    -   原因１：テーブルに既にデータが存在する可能性があります。これらの古いデータは最終的なチェックサムに影響を与える可能性があります。

    -   原因2：ターゲットデータベースのチェックサムが0（つまり何もインポートされていない）の場合、クラスタが過熱していてデータの取り込みに失敗している可能性があります。

    -   原因3：データソースがマシンによって生成され、 [Dumpling](/dumpling-overview.md)によってバックアップされていない場合は、テーブルの制約を遵守していることを確認してください。例：

        -   `AUTO_INCREMENT`列は正の値である必要があり、「0」という値を含んではいけません。
        -   UNIQUEキーとPRIMARYキーには重複するエントリがあってはなりません。

    -   解決策: [トラブルシューティングソリューション](/tidb-lightning/troubleshoot-tidb-lightning.md#checksum-failed-checksum-mismatched-remote-vs-local)を参照してください。

-   6.2.4 `Checkpoint for … has invalid status:(error code)`

    -   原因：チェックポイントが有効になっており、Lightning/Importerが以前に異常終了しています。データの破損を防ぐため、エラーが解消されるまでTiDB Lightningは起動しません。エラーコードは25未満の整数で、 `0, 3, 6, 9, 12, 14, 15, 17, 18, 20 and 21`などの値になります。この整数は、インポート処理で予期しない終了が発生したステップを示します。整数値が大きいほど、終了が発生したステップが遅くなります。

    -   解決策: [トラブルシューティングソリューション](/tidb-lightning/troubleshoot-tidb-lightning.md#checkpoint-for--has-invalid-status-error-code)を参照してください。

-   6.2.5 `cannot guess encoding for input file, please convert to UTF-8 manually`

    -   原因： TiDB LightningはUTF-8とGB-18030エンコーディングのみをサポートしています。このエラーは、ファイルがこれらのいずれのエンコーディングでもないことを意味しています。また、過去のALTER TABLE実行により、ファイルにUTF-8の文字列とGB-18030の文字列が混在している可能性もあります。

    -   解決策: [トラブルシューティングソリューション](/tidb-lightning/troubleshoot-tidb-lightning.md#cannot-guess-encoding-for-input-file-please-convert-to-utf-8-manually)を参照してください。

-   6.2.6 `[sql2kv] sql encode error = [types:1292]invalid time format: '{1970 1 1 0 45 0 0}'`

    -   原因：タイムスタンプ型のエントリに、存在しない時刻値が含まれています。これは、夏時間の変更、または時刻値がサポート範囲（1970年1月1日から2038年1月19日まで）を超えていることが原因です。

    -   解決策: [トラブルシューティングソリューション](/tidb-lightning/troubleshoot-tidb-lightning.md#sql2kv-sql-encode-error--types1292invalid-time-format-1970-1-1-)を参照してください。

## 7. 一般的なログ分析 {#7-common-log-analysis}

### 7.1 TiDB {#7-1-tidb}

-   7.1.1 `GC life time is shorter than transaction duration` 。

    トランザクションの実行時間がGCの有効期間（デフォルトでは10分）を超えています。

    [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)システム変数を変更することで、GC の有効期間を延長できます。ただし、このパラメータを変更することは一般的に推奨されません。このトランザクションに`UPDATE`および`DELETE`ステートメントが多数含まれている場合、このパラメータを変更すると、多くの古いバージョンが蓄積される可能性があるためです。

-   7.1.2 `coprocessor.go`は`request outdated`を報告します。

    このエラーは、TiKVに送信されたコプロセッサ要求がTiKVのキューで60秒以上待機した場合に返されます。

    TiKVコプロセッサが長いキューに入っている理由を調査する必要があります。

-   7.1.3 `region_cache.go`は`switch region peer to next due to send request fail`を多数報告し、エラー メッセージは`context deadline exceeded`です。

    TiKV へのリクエストがタイムアウトし、リージョン キャッシュがリクエストを他のノードに切り替えるようにトリガーされました。ログの`grep "<addr> cancelled`フィールドで`addr`コマンドを引き続き実行し、 `grep`の結果に応じて以下の手順を実行してください。

    -   `send request is cancelled` : 送信フェーズ中にリクエストがタイムアウトしました。Grafana -&gt; **TiDB** -&gt; **Batch Client** / `Pending Request Count by TiKV`の監視**画面**で、保留中のリクエスト数が 128 を超えているかどうかを確認してください。

        -   値が128より大きい場合、送信はKVの処理能力を超え、送信が蓄積されます。
        -   値が128を超えない場合は、ログを確認して、レポートが該当するKVの運用および保守の変更によって発生したかどうかを確認してください。そうでない場合は、このエラーは予期しないものであり、 [バグを報告する](https://github.com/pingcap/tidb/issues/new?labels=type%2Fbug&#x26;template=bug-report.md)必要があります。

    -   `wait response is cancelled` : リクエストが TiKV に送信された後、タイムアウトしました。対応する TiKV アドレスの応答時間と、その時点の PD および KV のリージョンログを確認する必要があります。

-   7.1.4 `distsql.go`は`inconsistent index`を報告します。

    データインデックスに矛盾があるようです。報告されたインデックスが存在するテーブルで`admin check table <TableName>`コマンドを実行してください。チェックが失敗した場合は、次のコマンドを実行して[バグを報告する](https://github.com/pingcap/tidb/issues/new?labels=type%2Fbug&#x26;template=bug-report.md)ガベージコレクションを無効にしてください。:

    ```sql
    SET GLOBAL tidb_gc_enable = 0;
    ```

### 7.2 TiKV {#7-2-tikv}

-   7.2.1 `key is locked` 。

    読み取りと書き込みが競合しています。読み取り要求は、コミットされていないデータに遭遇したため、データがコミットされるまで待機する必要があります。

    このエラーの発生件数が少ない場合は業務に影響はありませんが、発生件数が多い場合は、業務において読み書きの競合が深刻であることを示しています。

-   7.2.2 `write conflict` 。

    これは、楽観的トランザクションにおける書き込み競合です。複数のトランザクションが同じキーを変更した場合、1つのトランザクションのみが成功し、他のトランザクションは自動的にタイムスタンプを再取得して操作を再試行するため、業務に影響はありません。

    競合が深刻な場合は、複数回の再試行後にトランザクションが失敗する可能性があります。この場合、悲観的ロックを使用することをお勧めします。エラーと解決策の詳細については、[楽観的トランザクションにおける書き込み競合のトラブルシューティング](/troubleshoot-write-conflicts.md)参照してください。

-   7.2.3 `TxnLockNotFound` 。

    このトランザクションのコミットが遅すぎるため、有効期限（TTL）経過後に他のトランザクションによってロールバックされます。このトランザクションは自動的に再試行されるため、通常は業務に影響はありません。トランザクションのサイズが0.25MB以下の場合、デフォルトのTTLは3秒です。詳細については、 [`LockNotFound`エラー](/troubleshoot-lock-conflicts.md#locknotfound-error)を参照してください。

-   7.2.4 `PessimisticLockNotFound` 。

    `TxnLockNotFound`と同様です。悲観的トランザクションのコミットが遅すぎるため、他のトランザクションによってロールバックされます。

-   7.2.5 `stale_epoch` 。

    リクエストのエポックが古いため、TiDB はルーティングを更新した後にリクエストを再送信します。業務への影響はありません。エポックは、リージョンで分割/マージ操作が行われた場合、またはレプリカが移行された場合に変更されます。

-   7.2.6 `peer is not leader` 。

    リクエストはLeaderではないレプリカに送信されます。エラー応答で最新のLeaderがどのレプリカであるかが示された場合、TiDB はエラーに基づいてローカルルーティングを更新し、最新のLeaderに新しいリクエストを送信します。通常、業務には影響はありません。

    v3.0以降のバージョンでは、TiDBは前のLeaderへのリクエストが失敗した場合に他のピアを試行するため、TiKVログに`peer is not leader`頻繁に記録される可能性があります。送信失敗の根本原因を特定するには、TiDBの該当するリージョンの`switch region peer to next due to send request fail`ログを確認してください。詳細については、 [7.1.4](#71-tidb)を参照してください。

    このエラーは、他の理由でリージョンにLeaderがいない場合にも返される可能性があります。詳細については、 [4.4](#44-some-tikv-nodes-drop-leader-frequently)参照してください。
