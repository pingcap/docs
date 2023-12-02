---
title: TiDB Troubleshooting Map
summary: Learn how to troubleshoot common errors in TiDB.
---

# TiDB トラブルシューティング マップ {#tidb-troubleshooting-map}

このドキュメントでは、TiDB およびその他のコンポーネントの一般的な問題を要約します。関連する問題が発生した場合は、このマップを使用して問題を診断し、解決できます。

## 1. サービスが利用できない {#1-service-unavailable}

### 1.1 クライアントが<code>Region is Unavailable</code>エラーを報告する {#1-1-the-client-reports-code-region-is-unavailable-code-error}

-   1.1.1 `Region is Unavailable`エラーは、通常、リージョンが一定期間利用できないことが原因で発生します。 `TiKV server is busy`発生するか、 `not leader`または`epoch not match`原因で TiKV へのリクエストが失敗するか、TiKV へのリクエストがタイムアウトになる可能性があります。このような場合、TiDB は`backoff`の再試行メカニズムを実行します。 `backoff`しきい値 (デフォルトでは 20 秒) を超えると、エラーがクライアントに送信されます。しきい値`backoff`以内では、このエラーはクライアントには表示されません。

-   1.1.2 複数の TiKV インスタンスが同時に OOM になり、OOM 期間中にLeaderが存在しなくなります。中国語の[ケース-991](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case991.md)を参照してください。

-   1.1.3 TiKV は`TiKV server is busy`報告し、 `backoff`時間を超えています。詳細については、 [4.3](#43-the-client-reports-the-server-is-busy-error)を参照してください。 `TiKV server is busy`は内部フロー制御メカニズムの結果であり、 `backoff`時間にはカウントされません。この問題は修正される予定です。

-   1.1.4 複数の TiKV インスタンスの起動に失敗し、リージョン内にLeaderが存在しなくなりました。複数の TiKV インスタンスが物理マシンにデプロイされている場合、ラベルが適切に構成されていないと、物理マシンの障害によってリージョン内にLeaderが存在しなくなる可能性があります。中国語の[ケース-228](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case228.md)を参照してください。

-   1.1.5Followerの適用が前のエポックで遅れている場合、FollowerがLeaderになった後、リクエストは`epoch not match`で拒否されます。中国語の[ケース-958](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case958.md)参照してください (TiKV はメカニズムを最適化する必要があります)。

### 1.2 PD エラーによりサービスが利用できなくなる {#1-2-pd-errors-cause-service-unavailable}

[5 PDの問題](#5-pd-issues)を参照してください。

## 2. レイテンシが大幅に増加する {#2-latency-increases-significantly}

### 2.1 過渡的な増加 {#2-1-transient-increase}

-   2.1.1 間違った TiDB 実行計画によりレイテンシーが増加します。 [3.3](#33-wrong-execution-plan)を参照してください。
-   2.1.2 PDLeader選挙の問題または OOM。 [5.2](#52-pd-election)と[5.3](#53-pd-oom)を参照してください。
-   2.1.3 一部の TiKV インスタンスでかなりの数のLeaderがドロップします。 [4.4](#44-some-tikv-nodes-drop-leader-frequently)を参照してください。
-   2.1.4 その他の原因については、 [読み取りおよび書き込み遅延の増加のトラブルシューティング](/troubleshoot-cpu-issues.md)を参照してください。

### 2.2 持続的かつ大幅な増加 {#2-2-persistent-and-significant-increase}

-   2.2.1 TiKV シングルスレッドのボトルネック

    -   TiKV インスタンス内のリージョンが多すぎると、単一の gRPC スレッドがボトルネックになります ( **Grafana** -&gt; **TiKV の詳細**-&gt;**スレッド CPU/スレッドあたりの gRPC CPU**メトリックを確認してください)。 v3.x 以降のバージョンでは、 `Hibernate Region`有効にすることで問題を解決できます。中国語の[ケース-612](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case612.md)を参照してください。

    -   v3.0 より前のバージョンでは、raftstore スレッドまたは適用スレッドがボトルネックになる場合 ( **Grafana** -&gt; **TiKV-details** -&gt;**スレッド CPU/raft ストア CPU**および**非同期適用 CPU**メトリクスが`80%`を超える)、TiKV (v2) をスケールアウトできます。 .x) インスタンスを使用するか、マルチスレッドを使用して v3.x にアップグレードします。 <!-- See [case-517](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case517.md) in Chinese. -->

-   2.2.2 CPU負荷が増加します。

-   2.2.3 TiKV の書き込みが遅い。 [4.5](#45-tikv-write-is-slow)を参照してください。

-   2.2.4 TiDB の実行計画が間違っています。 [3.3](#33-wrong-execution-plan)を参照してください。

-   2.2.5 その他の原因については、 [読み取りおよび書き込み遅延の増加のトラブルシューティング](/troubleshoot-cpu-issues.md)を参照してください。

## 3. TiDB の問題 {#3-tidb-issues}

### 3.1 DDL {#3-1-ddl}

-   3.1.1 `decimal`フィールドの長さを変更すると、エラー`ERROR 1105 (HY000): unsupported modify decimal column precision`が報告されます。 <!--See [case-1004](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case517.md) in Chinese.--> TiDB は`decimal`フィールドの長さの変更をサポートしていません。

-   3.1.2 TiDB DDL ジョブがハングする、または実行が遅い (DDL の進行状況を確認するには`admin show ddl jobs`を使用します)

    -   原因 1: 他のコンポーネント (PD/TiKV) でのネットワークの問題。

    -   原因 2: TiDB の初期バージョン (v3.0.8 より前) では、高い同時実行性で多数の goroutine が使用されるため、内部負荷が高くなります。

    -   原因 3: 初期のバージョン (v2.1.15 およびバージョン &lt; v3.0.0-rc1) では、PD インスタンスが TiDB キーの削除に失敗するため、すべての DDL 変更が 2 つのリースを待機することになります。

    -   その他の不明な原因については、 [バグを報告](https://github.com/pingcap/tidb/issues/new?labels=type%2Fbug&#x26;template=bug-report.md) 。

    -   解決：

        -   原因 1 の場合は、TiDB と TiKV/PD の間のネットワーク接続を確認してください。
        -   原因 2 と 3 の問題は、以降のバージョンですでに修正されています。 TiDB を新しいバージョンにアップグレードできます。
        -   他の原因の場合は、次の DDL 所有者を移行する解決策を使用できます。

    -   DDL 所有者の移行:

        -   TiDBサーバーに接続できる場合は、所有者選択コマンドを再度実行します`curl -X POST http://{TiDBIP}:10080/ddl/owner/resign`
        -   TiDBサーバーに接続できない場合は、 `tidb-ctl`を使用して PD クラスターの etcd から DDL 所有者を削除し、再選択をトリガーします。 `tidb-ctl etcd delowner [LeaseID] [flags] + ownerKey`

-   3.1.3 TiDB がログに`information schema is changed`エラーを報告する

    -   詳細な原因と解決策については、 [`Information schema is changed`エラーが報告される理由](/faq/sql-faq.md#what-triggers-the-information-schema-is-changed-error)を参照してください。

    -   背景: 増加した数値`schema version`各 DDL 変更操作の数値`schema state`と一致しています。たとえば、 `create table`オペレーションには 1 つのバージョン変更があり、 `add column`オペレーションには 4 つのバージョン変更があります。したがって、列変更操作が多すぎると、 `schema version`が急速に増加する可能性があります。詳細は[オンラインでのスキーマ変更](https://static.googleusercontent.com/media/research.google.com/zh-CN//pubs/archive/41376.pdf)を参照してください。

-   3.1.4 TiDB がログに`information schema is out of date`報告する

    -   原因 1: DML ステートメントを実行している TiDBサーバーが`graceful kill`によって停止され、終了の準備をしています。 DML ステートメントを含むトランザクションの実行時間が 1 つの DDL リースを超えています。トランザクションがコミットされるとエラーが報告されます。

    -   原因 2: TiDBサーバーは、 DML ステートメントの実行中に PD または TiKV に接続できません。その結果、TiDBサーバーは1 つの DDL リース (デフォルトでは`45s` ) 以内に新しいスキーマをロードしなかったか、TiDBサーバーが`keep alive`設定で PD から切断されました。

    -   原因 3: TiKV の負荷が高いか、ネットワークがタイムアウトしました。 **Grafana** -&gt; **TiDB**および**TiKV**でノードの負荷を確認します。

    -   解決：

        -   原因 1 の場合は、TiDB の起動時に DML 操作を再試行します。
        -   原因 2 の場合は、TiDBサーバーと PD/TiKV の間のネットワークを確認してください。
        -   原因 3 については、TiKV がビジーである理由を調査します。 [4 TiKVの問題](#4-tikv-issues)を参照してください。

### 3.2 OOM の問題 {#3-2-oom-issues}

-   3.2.1 症状

    -   クライアント: クライアントはエラー`ERROR 2013 (HY000): Lost connection to MySQL server during query`を報告します。

    -   ログを確認してください

        -   `dmesg -T | grep tidb-server`を実行します。結果には、エラーが発生した時点付近の OOM-killer ログが表示されます。

        -   エラー発生後の時点 (つまり、tidb-server が再起動する時点) の「TiDB へようこそ」ログを`tidb.log`で grep します。

        -   Grep `fatal error: runtime: out of memory`または`cannot allocate memory` in `tidb_stderr.log` 。

        -   v2.1.8 以前のバージョンでは、 `tidb_stderr.log`の`fatal error: stack overflow`を grep できます。

    -   モニター: tidb-server インスタンスのメモリ使用量が短期間で急激に増加します。

-   3.2.2 OOM の原因となっている SQL ステートメントを特定します。 (現在、TiDB のすべてのバージョンでは SQL を正確に見つけることができません。SQL ステートメントを見つけた後も、OOM が SQL ステートメントによって引き起こされているかどうかを分析する必要があります。)

    -   バージョン &gt;= v3.0.0 の場合は、 `tidb.log`で &quot;expensive_query&quot; を grep します。このログ メッセージには、タイムアウトしたか、メモリクォータを超過した SQL クエリが記録されます。

    -   v3.0.0 より前のバージョンの場合は、 `tidb.log`で grep &quot;メモリ がクォータを超えています&quot; を実行して、メモリクォータを超えている SQL クエリを見つけます。

    > **注記：**
    >
    > 単一の SQLメモリ使用量のデフォルトのしきい値は`1GB`です。このパラメータは、システム変数[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)を構成することで設定できます。

-   3.2.3 OOM の問題を軽減する

    -   `SWAP`を有効にすると、大規模なクエリによるメモリの過剰使用によって引き起こされる OOM 問題を軽減できます。メモリが不十分な場合、この方法は I/O オーバーヘッドにより大規模なクエリのパフォーマンスに影響を与える可能性があります。パフォーマンスに影響する程度は、メモリの残量とディスクの I/O 速度によって異なります。

-   3.2.4 OOM の一般的な理由

    -   SQL クエリには`join`があります。 `explain`使用して SQL ステートメントを表示すると、 `join`操作で`HashJoin`アルゴリズムが選択され、 `inner`テーブルが大きいことがわかります。

    -   1 つの`UPDATE/DELETE`クエリのデータ量が大きすぎます。中国語の[ケース-882](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case882.md)を参照してください。

    -   SQL には、 `Union`で接続された複数のサブクエリが含まれています。中国語の[ケース-1828](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case1828.md)を参照してください。

OOM のトラブルシューティングの詳細については、 [TiDB OOM の問題のトラブルシューティング](/troubleshoot-tidb-oom.md)を参照してください。

### 3.3 間違った実行計画 {#3-3-wrong-execution-plan}

-   3.3.1 症状

    -   SQL クエリの実行時間が以前の実行に比べて大幅に長くなったり、実行計画が突然変更されたりする。実行計画が低速ログに記録されている場合は、実行計画を直接比較できます。

    -   SQL クエリの実行時間は、MySQL などの他のデータベースに比べて非常に長くなります。実行計画を他のデータベースと比較して、 `Join Order`などの違いを確認します。

    -   スローログではSQL実行時間`Scan Keys`の数が多くなります。

-   3.3.2 実行計画の調査

    -   `explain analyze {SQL}` 。実行時間が許容範囲内であれば、 `explain analyze`の結果の`count`と`execution info`の結果の`row`の数を比較します。 `TableScan/IndexScan`行で大きな差が見つかった場合は、統計が正しくない可能性があります。他の行で大きな差が見つかった場合、問題は統計に含まれていない可能性があります。

    -   `select count(*)` 。実行計画に`join`操作が含まれている場合、 `explain analyze`時間がかかる可能性があります。 `TableScan/IndexScan`の条件に対して`select count(*)`実行し、 `explain`結果の`row count`情報を比較することで、統計に問題があるかどうかを確認できます。

-   3.3.3 緩和策

    -   v3.0 以降のバージョンの場合は、 `SQL Bind`機能を使用して実行プランをバインドします。

    -   統計を更新します。問題の原因が統計にあることが大まかに確信できる場合は、 [統計をダンプする](/statistics.md#export-statistics) 。原因が古い統計 ( `show stats_meta`の`modify count/row count`特定の値 (0.3 など) より大きい場合、またはテーブルに時刻列のインデックスがある場合) である場合は、 `analyze table`使用して回復を試みることができます。 `auto analyze`が設定されている場合は、システム変数`tidb_auto_analyze_ratio`が大きすぎるかどうか (たとえば、0.3 より大きいかどうか)、および現在時刻が`tidb_auto_analyze_start_time`から`tidb_auto_analyze_end_time`の間にあるかどうかを確認してください。

    -   その他の状況の場合は、 [バグを報告](https://github.com/pingcap/tidb/issues/new?labels=type%2Fbug&#x26;template=bug-report.md) 。

### 3.4 SQL実行エラー {#3-4-sql-execution-error}

-   3.4.1 クライアントは`ERROR 1265(01000) Data Truncated`エラーを報告します。これは、TiDB が内部で`Decimal`型の精度を計算する方法が MySQL の計算方法と互換性がないためです。この問題は v3.0.10 ( [#14438](https://github.com/pingcap/tidb/pull/14438) ) で修正されました。

    -   原因：

        MySQL では、2 つの大きな精度の`Decimal`を除算し、その結果が最大 10 進精度 ( `30` ) を超える場合、 `30`桁のみが予約され、エラーは報告されません。

        TiDB では、計算結果は MySQL と同じですが、 `Decimal`を表すデータ構造内では、小数精度のフィールドが実際の精度を保持します。

        `(0.1^30) / 10`例に挙げます。 TiDB と MySQL の結果は両方とも`0`です。これは、精度が最大`30`であるためです。ただし、TiDB では、10 進精度のフィールドは`31`のままです。

        複数の`Decimal`除算の後、結果が正しい場合でも、この精度フィールドはますます大きくなり、最終的には TiDB ( `72` ) のしきい値を超え、 `Data Truncated`エラーが報告されます。

        `Decimal`の乗算では、範囲外がバイパスされ、精度が最大精度制限に設定されるため、この問題は発生しません。

    -   解決策: `a`と`b`がターゲット精度である`Cast(xx as decimal(a, b))`手動で追加することで、この問題を回避できます。

### 3.5 遅いクエリの問題 {#3-5-slow-query-issues}

遅いクエリを特定するには、 [遅いクエリを特定する](/identify-slow-queries.md)を参照してください。遅いクエリを分析して処理するには、 [遅いクエリを分析する](/analyze-slow-queries.md)参照してください。

### 3.6 ホットスポットの問題 {#3-6-hotspot-issues}

分散データベースとして、TiDB には、アプリケーションの負荷をさまざまなコンピューティング ノードまたはstorageノードにできるだけ均等に分散して、サーバーリソースを有効に活用する負荷分散メカニズムが備わっています。ただし、特定のシナリオでは、一部のアプリケーション負荷を適切に分散できず、パフォーマンスに影響を及ぼし、ホットスポットとも呼ばれる高負荷の単一点が形成される可能性があります。

TiDB は、ホットスポットのトラブルシューティング、解決、回避のための完全なソリューションを提供します。負荷ホットスポットのバランスをとることで、QPS の向上やレイテンシーの削減など、全体的なパフォーマンスを向上させることができます。詳細な解決策については、 [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)を参照してください。

### 3.7 ディスク I/O 使用率が高い {#3-7-high-disk-i-o-usage}

CPU ボトルネックとトランザクションの競合によって引き起こされるボトルネックのトラブルシューティングを行った後に TiDB の応答が遅くなった場合は、現在のシステム ボトルネックを特定するために I/O メトリックを確認する必要があります。 TiDB での高い I/O 使用率の問題を特定して処理する方法については、 [ディスク I/O 使用量が多い場合のトラブルシューティング](/troubleshoot-high-disk-io.md)を参照してください。

### 3.8 ロックの競合 {#3-8-lock-conflicts}

TiDB は完全な分散トランザクションをサポートします。 v3.0 以降、TiDB は楽観的トランザクション モードと悲観的トランザクション モードを提供します。ロック関連の問題のトラブルシューティング方法、および楽観的ロックと悲観的ロックの競合の処理方法については、 [ロックの競合のトラブルシューティング](/troubleshoot-lock-conflicts.md)を参照してください。

### 3.9 データとインデックスの不一致 {#3-9-inconsistency-between-data-and-indexes}

TiDB は、トランザクション[`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md)ステートメントを実行するときに、データとインデックス間の一貫性をチェックします。チェックで、レコードのキーと値、および対応するインデックスのキーと値が矛盾していることが判明した場合、つまり、行データを格納するキーと値のペアと、そのインデックスを格納する対応するキーと値のペアが一致しない場合 (たとえば、インデックスを増やすか、インデックスが欠落している場合)、TiDB はデータ不整合エラーを報告し、関連するエラーをエラー ログに出力。

不整合エラーとチェックをバイパスする方法の詳細については、 [データとインデックス間の不一致のトラブルシューティング](/troubleshoot-data-inconsistency-errors.md)を参照してください。

## 4. TiKVの問題 {#4-tikv-issues}

### 4.1 TiKV がパニックになり起動に失敗する {#4-1-tikv-panics-and-fails-to-start}

-   4.1.1 `sync-log = false` ．マシンの電源をオフにすると、エラー`unexpected raft log index: last_index X < applied_index Y`が返されます。

    この問題は予想されています。 `tikv-ctl`を使用してリージョンを復元できます。

-   4.1.2 TiKV が仮想マシンにデプロイされている場合、仮想マシンが強制終了されるか、物理マシンがパワーオフされると、 `entries[X, Y] is unavailable from storage`エラーが報告されます。

    この問題は予想されています。仮想マシンの`fsync`信頼できないため、 `tikv-ctl`使用してリージョンを復元する必要があります。

-   4.1.3 その他の予期せぬ原因については、 [バグを報告](https://github.com/tikv/tikv/issues/new?template=bug-report.md) 。

### 4.2 TiKV OOM {#4-2-tikv-oom}

-   4.2.1 `block-cache`構成が大きすぎる場合、OOM が発生する可能性があります。

    問題の原因を確認するには、モニター**Grafana** -&gt; **TiKV-details**で対応するインスタンスを選択して、RocksDB の`block cache size`を確認します。

    その間、 `[storage.block-cache] capacity = # "1GB"`パラメータが正しく設定されているかどうかを確認してください。デフォルトでは、TiKV の`block-cache`マシンの合計メモリの`45%`に設定されています。 TiKV は物理マシンのメモリを取得するため、コンテナに TiKV をデプロイするときにこのパラメータを明示的に指定する必要があります。これは、コンテナのメモリ制限を超える可能性があります。

-   4.2.2コプロセッサーは多くの大規模なクエリを受信し、大量のデータを返します。 gRPC は、コプロセッサがデータを返すのと同じくらい早くデータを送信できないため、OOM が発生します。

    原因を確認するには、モニター**Grafana** -&gt; **TiKV 詳細**-&gt;**コプロセッサー概要**を表示して、 `response size` `network outbound`トラフィックを超えているかどうかを確認できます。

-   4.2.3 他のコンポーネントが大量のメモリを占有します。

    この問題は予期せぬものです。 [バグを報告](https://github.com/tikv/tikv/issues/new?template=bug-report.md)を行うことができます。

### 4.3 クライアントが<code>server is busy</code>エラーを報告する {#4-3-the-client-reports-the-code-server-is-busy-code-error}

モニター**Grafana** -&gt; **TiKV** -&gt;**エラーを**表示して、ビジーの具体的な原因を確認します。 `server is busy`は、TiKV のフロー制御メカニズムによって発生し、TiKV が現在過剰な圧力を受けているため、後で再試行することを`tidb/ti-client`に通知します。

-   4.3.1 TiKV RocksDB との遭遇`write stall` 。

    TiKV インスタンスには 2 つの RocksDB インスタンスがあり、 `data/raft`つはRaftログを保存するため、もう 1 つは`data/db`で実際のデータを保存します。ログで`grep "Stalling" RocksDB`を実行すると、ストールの具体的な原因を確認できます。 RocksDB ログは`LOG`で始まるファイルで、 `LOG`が現在のログです。

    -   `level0 sst`が多すぎるとストールの原因になります。 `[rocksdb] max-sub-compactions = 2` (または 3) パラメータを追加すると、 `level0 sst`圧縮を高速化できます。 level0 から level1 までの圧縮タスクは、複数のサブタスク (サブタスクの最大数は`max-sub-compactions` ) に分割され、同時に実行されます。中国語の[ケース-815](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case815.md)を参照してください。

    -   `pending compaction bytes`が多すぎるとストールの原因になります。ビジネスのピーク時には、ディスク I/O が書き込み操作に追いつけなくなります。対応する CF の`soft-pending-compaction-bytes-limit`と`hard-pending-compaction-bytes-limit`を増やすことで、この問題を軽減できます。

        -   デフォルト値の`[rocksdb.defaultcf] soft-pending-compaction-bytes-limit`は`64GB`です。保留中の圧縮バイトがしきい値に達すると、RocksDB は書き込み速度を遅くします。 `[rocksdb.defaultcf] soft-pending-compaction-bytes-limit` ～ `128GB`まで設定できます。

        -   デフォルト値の`hard-pending-compaction-bytes-limit`は`256GB`です。保留中の圧縮バイトがしきい値に達すると (保留中の圧縮バイトが`soft-pending-compaction-bytes-limit`に達すると、RocksDB は書き込み速度を低下させるため、このようなことは起こりそうにありません)、RocksDB は書き込み操作を停止します。 `hard-pending-compaction-bytes-limit` ～ `512GB`まで設定できます。 <!-- See [case-275](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case275.md) in Chinese.-->

        -   ディスク I/O 容量が長時間書き込みに追いつかない場合は、ディスクをスケールアップすることをお勧めします。 CPU リソースが十分であるにもかかわらず、ディスク スループットが上限に達して書き込み停止が発生する場合 (たとえば、SATA SSD が NVME SSD よりも大幅に低い場合)、より高い圧縮率の圧縮アルゴリズムを適用することができます。このようにして、CPU リソースがディスク リソースと交換され、ディスクへの負荷が軽減されます。

        -   デフォルトの CF 圧縮で高圧が発生した場合は、 `[rocksdb.defaultcf] compression-per-level`パラメーターを`["no", "no", "lz4", "lz4", "lz4", "zstd", "zstd"]`から`["no", "no", "zstd", "zstd", "zstd", "zstd", "zstd"]`に変更します。

    -   memtable が多すぎるとストールが発生します。これは通常、インスタント書き込みの量が多く、memtable のディスクへのフラッシュが遅い場合に発生します。ディスクの書き込み速度を改善できず、この問題がビジネスのピーク時にのみ発生する場合は、対応する CF の`max-write-buffer-number`増やすことで問題を軽減できます。

        -   たとえば、 `[rocksdb.defaultcf] max-write-buffer-number` ～ `8`を設定します (デフォルトでは`5` )。これにより、メモリ内にさらに多くのメモリが存在する可能性があるため、ピーク時にメモリ使用量が増加する可能性があることに注意してください。

-   4.3.2 `scheduler too busy`

    -   深刻な書き込み競合。 `latch wait duration`高いですね。 `latch wait duration`は、モニター**Grafana** -&gt; **TiKV-details** -&gt;**スケジューラー事前書き込み**/**スケジューラーコミット**で表示できます。スケジューラに書き込みタスクが溜まると、保留中の書き込みタスクが`[storage] scheduler-pending-write-threshold`で設定した閾値（100MB）を超えます。 `MVCC_CONFLICT_COUNTER`に対応するメトリックを表示することで原因を確認できます。

    -   書き込みが遅いと、書き込みタスクが溜まってしまいます。 TiKV に書き込まれているデータが、 `[storage] scheduler-pending-write-threshold`で設定されたしきい値 (100MB) を超えています。 [4.5](#45-tikv-write-is-slow)を参照してください。

-   4.3.3 `raftstore is busy` .メッセージの処理は、メッセージの受信よりも遅くなります。短期的な`channel full`ステータスはサービスに影響しませんが、エラーが長期間続く場合は、Leaderスイッチが発生する可能性があります。

    -   `append log`エンカウント失速。 [4.3.1](#43-the-client-reports-the-server-is-busy-error)を参照してください。
    -   `append log duration`は高いため、メッセージの処理が遅くなります。 [4.5](#45-tikv-write-is-slow)を参照して、 `append log duration`が高い理由を分析できます。
    -   raftstore は大量のメッセージを瞬時に受信しますが (TiKV Raftメッセージ ダッシュボードで確認してください)、それらの処理に失敗します。通常、短期`channel full`ステータスはサービスに影響しません。

-   4.3.4 TiKV コプロセッサーはキュー内にあります。溜まっているタスクの数が`coprocessor threads * readpool.coprocessor.max-tasks-per-worker-[normal|low|high]`を超えています。大規模なクエリが多すぎると、コプロセッサにタスクが積み重なります。実行計画の変更によって多数のテーブル スキャン操作が発生するかどうかを確認する必要があります。 [3.3](#33-wrong-execution-plan)を参照してください。

### 4.4 一部の TiKV ノードがLeaderを頻繁にドロップする {#4-4-some-tikv-nodes-drop-leader-frequently}

-   4.4.1 TiKV 再開による再選

    -   TiKV がパニックになった後、systemd によってプルアップされ、正常に実行されます。panicが発生したかどうかは、TiKV ログを表示することで確認できます。この問題は予期しないものであるため、発生した場合は[バグを報告](https://github.com/tikv/tikv/issues/new?template=bug-report.md) 。

    -   TiKV はサードパーティによって停止または強制終了され、systemd によって引き上げられます。 `dmesg`およびTiKVログを参照して原因を確認してください。

    -   TiKV は OOM であるため、再起動が発生します。 [4.2](#42-tikv-oom)を参照してください。

    -   TiKV は、 `THP` (透明な巨大ページ) を動的に調整するためにハングします。中国語のケース[ケース-500](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case500.md)を参照してください。

-   4.4.2 TiKV RocksDB で書き込みストールが発生し、再選択が発生します。モニター**Grafana** -&gt; **TiKV-details** -&gt;**エラー**に`server is busy`表示されるかどうかを確認できます。 [4.3.1](#43-the-client-reports-the-server-is-busy-error)を参照してください。

-   4.4.3 ネットワーク分離による再選。

### 4.5 TiKV 書き込みが遅い {#4-5-tikv-write-is-slow}

-   4.5.1 TiKV gRPC の`prewrite/commit/raw-put`時間を表示して、TiKV 書き込みが低いかどうかを確認します (RawKV クラスターの場合のみ)。一般に、 [パフォーマンスマップ](https://github.com/pingcap/tidb-map/blob/master/maps/performance-map.png)に従って低速フェーズを特定できます。よくある状況のいくつかを以下に示します。

-   4.5.2 スケジューラ CPU がビジー状態です (トランザクション kv のみ)。

    prewrite/commit の`scheduler command duration` `scheduler latch wait duration`と`storage async write duration`の合計よりも長くなります。スケジューラー ワーカーの CPU 要求が高い ( `scheduler-worker-pool-size` * 100% の 80% 以上など)、またはマシン全体の CPU リソースが比較的制限されています。書き込みワークロードが大きい場合は、 `[storage] scheduler-worker-pool-size`の設定が小さすぎるかどうかを確認してください。

    その他の状況の場合は、 [バグを報告](https://github.com/tikv/tikv/issues/new?template=bug-report.md) 。

-   4.5.3 ログの追加が遅い。

    TiKV Grafana の**Raft IO** / `append log duration`が高いのは、通常、ディスク書き込み操作が遅いためです。 RocksDB - raft の`WAL Sync Duration max`値を確認することで原因を確認できます。

    その他の状況の場合は、 [バグを報告](https://github.com/tikv/tikv/issues/new?template=bug-report.md) 。

-   4.5.4 raftstore スレッドはビジー状態です。

    **Raft Propose** / `propose wait duration`は、TiKV Grafana の追加ログ期間よりも大幅に長くなります。次の方法を取ります。

    -   `[raftstore] store-pool-size`設定値が小さすぎないか確認してください。値は`1` ～ `5`の間で、大きすぎない値に設定することをお勧めします。
    -   マシンのCPUリソースが不足していないか確認してください。

-   4.5.5 適用が遅い。

    TiKV Grafana の**Raft IO** / `apply log duration`は高く、通常は高い**Raft Propose** / `apply wait duration`が付属します。考えられる原因は次のとおりです。

    -   `[raftstore] apply-pool-size`は小さすぎます (大きすぎない`1` ～ `5`の値を設定することをお勧めします)。Thread **CPU** / `apply CPU`は大きすぎます。

    -   マシンの CPU リソースが不足しています。

    -   リージョン書き込みホットスポット。単一の適用スレッドでは CPU 使用率が高くなります。現在、単一のリージョンでのホット スポットの問題に適切に対処できませんが、現在改善中です。各スレッドの CPU 使用率を表示するには、Grafana 式を変更して`by (instance, name)`を追加します。

    -   RocksDB の書き込みが遅い。 **RocksDB kv** / `max write duration`は高いです。単一のRaftログには複数の KV が含まれる場合があります。 RocksDB に書き込む場合、書き込みバッチで 128 KV が RocksDB に書き込まれます。したがって、適用ログは RocksDB の複数の書き込みに関連付けられている可能性があります。

    -   その他の状況の場合は、 [バグを報告](https://github.com/tikv/tikv/issues/new?template=bug-report.md) 。

-   4.5.6 Raft のコミットログが遅い。

    TiKV Grafana の**Raft IO** / `commit log duration`は高いです (このメトリックは v4.x 以降の Grafana でのみサポートされています)。すべてのリージョンは独立したRaftグループに対応します。 Raft には、TCP のスライディング ウィンドウ メカニズムと同様のフロー制御メカニズムがあります。 `[raftstore] raft-max-inflight-msgs = 256`パラメータを設定することで、スライディング ウィンドウのサイズを制御できます。書き込みホットスポットがあり、 `commit log duration`が高い場合は、パラメータを`1024`に増やすなどして調整できます。

-   4.5.7 その他の場合は、 [パフォーマンスマップ](https://github.com/pingcap/tidb-map/blob/master/maps/performance-map.png)の書き込みパスを参照して原因を解析してください。

## 5.PDの問題 {#5-pd-issues}

### 5.1 PD スケジューリング {#5-1-pd-scheduling}

-   5.1.1 マージ

    -   テーブル間の空の領域をマージすることはできません。 TiKV の`[coprocessor] split-region-on-table`パラメータを変更する必要があります。v4.x ではデフォルトで`false`に設定されています。中国語の[ケース-896](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case896.md)を参照してください。

    -   リージョンのマージが遅い。マージされたオペレーターが生成されているかどうかは、 **Grafana** -&gt; **PD** -&gt; **Operator**でモニター ダッシュボードにアクセスすることで確認できます。マージを高速化するには、 `merge-schedule-limit`の値を増やします。

-   5.1.2 レプリカの追加またはレプリカのオンライン/オフライン化

    -   TiKV ディスクは容量の 80% を使用し、PD はレプリカを追加しません。この状況では、ミスピアの数が増加するため、TiKV をスケールアウトする必要があります。中国語の[ケース-801](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case801.md)を参照してください。

    -   TiKV ノードがオフラインになると、一部のリージョンを他のノードに移行できなくなります。この問題は v3.0.4 ( [#5526](https://github.com/tikv/tikv/pull/5526) ) で修正されました。中国語の[ケース-870](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case870.md)を参照してください。

-   5.1.3 バランス

    -   Leader/リージョンの数は均等に分散されていません。中国語の[ケース-394](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case394.md)と[ケース-759](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case759.md)を参照してください。主な原因は、天びんがリージョン/Leaderのサイズに基づいてスケジューリングを実行するため、カウントが不均一に分散される可能性があることです。 TiDB 4.0 では、 `[leader-schedule-policy]`パラメータが導入され、Leaderのスケジューリング ポリシーを`count`ベースまたは`size`ベースに設定できるようになります。

### 5.2 PDの選出 {#5-2-pd-election}

-   5.2.1 PD スイッチLeader。

    -   原因 1: ディスク。 PD ノードが配置されているディスクには、完全な I/O 負荷がかかっています。 PD が、I/O 要求の高い他のコンポーネントおよびディスクの健全性とともにデプロイされているかどうかを調査します。 **Grafana** -&gt;**ディスクパフォ​​ーマンス**-&gt;**レイテンシー**/**負荷**でモニターメトリクスを表示することで、原因を確認できます。必要に応じて、FIO ツールを使用してディスクのチェックを実行することもできます。中国語の[ケース-292](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case292.md)を参照してください。

    -   原因 2: ネットワーク。 PD ログには`lost the TCP streaming connection`が表示されます。 PD ノード間のネットワークに問題があるかどうかを確認し、モニターの**Grafana** -&gt; **PD** -&gt; **etcd**の`round trip`表示して原因を検証する必要があります。中国語の[ケース-177](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case177.md)を参照してください。

    -   原因 3: システム負荷が高い。ログには`server is likely overloaded`表示されます。中国語の[ケース-214](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case214.md)を参照してください。

-   5.2.2 PD がLeaderを選出できない、または選出が遅い。

    -   PD はLeaderを選出できません: PD ログには`lease is not expired`表示されます。 [この問題](https://github.com/etcd-io/etcd/issues/10355) v3.0.x および v2.1.19 で修正されました。中国語の[ケース-875](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case875.md)を参照してください。

    -   選挙が遅い:リージョンの読み込み時間が長い。 PD ログで`grep "regions cost"`を実行すると、この問題を確認できます。結果が`load 460927 regions cost 11.77099s`などの秒単位の場合は、リージョンの読み込みが遅いことを意味します。 v3.0 では`use-region-storage`を`true`に設定することで`region storage`機能を有効にすることができ、これによりリージョンの読み込み時間が大幅に短縮されます。中国語の[ケース-429](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case429.md)を参照してください。

-   5.2.3 TiDB が SQL ステートメントを実行すると PD がタイムアウトしました。

    -   PD にはLeaderが存在しないか、Leaderを切り替えます。 [5.2.1](#52-pd-election)と[5.2.2](#52-pd-election)を参照してください。

    -   ネットワークの問題。 **Grafana** -&gt; **blackbox_exporter** -&gt; **ping レイテンシー**モニターにアクセスして、TiDB から PD Leaderまでのネットワークが正常に動作しているかどうかを確認します。

    -   PDはパニックに陥ります。 [バグを報告](https://github.com/pingcap/pd/issues/new?labels=kind%2Fbug&#x26;template=bug-report.md) .

    -   PDはOOMです。 [5.3](#53-pd-oom)を参照してください。

    -   問題に他の原因がある場合は、 `curl http://127.0.0.1:2379/debug/pprof/goroutine?debug=2`と[バグを報告](https://github.com/pingcap/pd/issues/new?labels=kind%2Fbug&#x26;template=bug-report.md)を実行して goroutine を取得します。

-   5.2.4 その他の問題

    -   PD は`FATAL`エラーを報告し、ログには`range failed to find revision pair`が表示されます。この問題は v3.0.8 ( [#2040](https://github.com/pingcap/pd/pull/2040) ) で修正されました。詳細については、中国語の[ケース-947](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case947.md)を参照してください。

    -   その他の状況の場合は、 [バグを報告](https://github.com/pingcap/pd/issues/new?labels=kind%2Fbug&#x26;template=bug-report.md) 。

### 5.3 PD OOM {#5-3-pd-oom}

-   5.3.1 `/api/v1/regions`インターフェイスを使用する場合、リージョンが多すぎると PD OOM が発生する可能性があります。この問題は v3.0.8 ( [#1986](https://github.com/pingcap/pd/pull/1986) ) で修正されました。

-   5.3.2 ローリング アップグレード中の PD OOM。 gRPC メッセージのサイズは制限されておらず、モニターには TCP InSegs が比較的大きいことが示されています。この問題は v3.0.6 ( [#1952](https://github.com/pingcap/pd/pull/1952) ) で修正されました。 <!--For details, see [case-852](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case852.md).-->

### 5.4 グラファナ表示 {#5-4-grafana-display}

-   5.4.1 **Grafana** -&gt; **PD** -&gt;**クラスター**-&gt;**ロール**のモニターにはフォロワーが表示されます。 Grafana 式の問題は v3.0.8 で修正されました。

## 6. エコシステムツール {#6-ecosystem-tools}

### 6.1 TiDBBinlog {#6-1-tidb-binlog}

-   6.1.1 TiDB Binlog は、 TiDB から変更を収集し、ダウンストリームの TiDB または MySQL プラットフォームにバックアップとレプリケーションを提供するツールです。詳細は[GitHub 上の TiDBBinlog](https://github.com/pingcap/tidb-binlog)を参照してください。

-   6.1.2Pump/Drainerステータスの`Update Time`正常に更新され、ログには異常は表示されませんが、下流にはデータが書き込まれません。

    -   TiDB 構成ではBinlog が有効になっていません。 TiDB の`[binlog]`構成を変更します。

-   6.1.3 `sarama` in Drainer は`EOF`エラーを報告します。

    -   Drainerの Kafka クライアントのバージョンは、Kafka のバージョンと一致しません。 `[syncer.to] kafka-version`構成を変更する必要があります。

-   6.1.4 Drainer がKafka への書き込みに失敗してパニックになり、Kafka は`Message was too large`エラーを報告します。

    -   binlogデータが大きすぎるため、Kafka に書き込まれる単一メッセージが大きすぎます。 Kafka の次の構成を変更する必要があります。

        ```conf
        message.max.bytes=1073741824
        replica.fetch.max.bytes=1073741824
        fetch.message.max.bytes=1073741824
        ```

        詳細については、中国語の[ケース-789](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case789.md)を参照してください。

-   6.1.5 上流と下流での不整合なデータ

    -   一部の TiDB ノードはbinlog を有効にしません。 v3.0.6 以降のバージョンでは、 [http://127.0.0.1:10080/info/all](http://127.0.0.1:10080/info/all)インターフェイスにアクセスしてすべてのノードのbinlogステータスを確認できます。 v3.0.6 より前のバージョンの場合は、構成ファイルを表示してbinlogステータスを確認できます。

    -   一部の TiDB ノードは`ignore binlog`ステータスになります。 v3.0.6 以降のバージョンでは、 [http://127.0.0.1:10080/info/all](http://127.0.0.1:10080/info/all)インターフェイスにアクセスしてすべてのノードのbinlogステータスを確認できます。 v3.0.6 より前のバージョンの場合は、TiDB ログをチェックして、 `ignore binlog`キーワードが含まれているかどうかを確認してください。

    -   タイムスタンプ列の値がアップストリームとダウンストリームで一致しません。

        -   これはタイムゾーンの違いが原因で発生します。 Drainer がアップストリームおよびダウンストリーム データベースと同じタイム ゾーンにあることを確認する必要があります。 Drainer はタイムゾーンを`/etc/localtime`から取得し、環境変数`TZ`をサポートしません。中国語の[ケース-826](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case826.md)を参照してください。

        -   TiDB では、タイムスタンプのデフォルト値は`null`ですが、 MySQL 5.7 (MySQL 8 を除く) の同じデフォルト値は現在時刻です。したがって、アップストリーム TiDB のタイムスタンプが`null`で、ダウンストリームがMySQL 5.7である場合、タイムスタンプ列のデータは一貫性がありません。 binlogを有効にする前に、アップストリームで`set @@global.explicit_defaults_for_timestamp=on;`を実行する必要があります。

    -   その他の状況の場合は、 [バグを報告](https://github.com/pingcap/tidb-binlog/issues/new?labels=bug&#x26;template=bug-report.md) 。

-   6.1.6 遅いレプリケーション

    -   ダウンストリームは TiDB/MySQL で、アップストリームは頻繁に DDL 操作を実行します。中国語の[ケース-1023](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case1023.md)を参照してください。

    -   ダウンストリームは TiDB/MySQL であり、レプリケートされるテーブルには主キーも一意のインデックスもないため、 binlogのパフォーマンスが低下します。主キーまたは一意のインデックスを追加することをお勧めします。

    -   ダウンストリームがファイルに出力する場合は、出力ディスクまたはネットワーク ディスクが低速かどうかを確認してください。

    -   その他の状況の場合は、 [バグを報告](https://github.com/pingcap/tidb-binlog/issues/new?labels=bug&#x26;template=bug-report.md) 。

-   6.1.7Pumpはbinlogを書き込めず、 `no space left on device`エラーを報告します。

    -   ローカル ディスク容量が不足しているため、 Pump はbinlogデータを正常に書き込むことができません。ディスク領域をクリーンアップしてから、 Pumpを再起動する必要があります。

-   6.1.8Pumpは起動時に`fail to notify all living drainer`エラーを報告します。

    -   原因:Pumpが開始されると、状態`online`にあるすべてのDrainerノードに通知されます。 Drainerへの通知に失敗した場合、このエラー ログが出力されます。

    -   解決策: binlogctl ツールを使用して、各Drainerノードが正常かどうかを確認します。これは、 `online`状態のすべてのDrainerノードが正常に動作していることを確認するためです。 Drainerノードの状態が実際の動作ステータスと一致しない場合は、 binlogctl ツールを使用してその状態を変更し、 Pumpを再起動します。ケース[すべての生きている排水者への通知に失敗する](/tidb-binlog/handle-tidb-binlog-errors.md#fail-to-notify-all-living-drainer-is-returned-when-pump-is-started)を参照してください。

-   6.1.9 Drainer は`gen update sqls failed: table xxx: row data is corruption []`エラーを報告します。

    -   トリガー: アップストリームは`DROP COLUMN` DDL を実行しながら、このテーブルに対して DML 操作を実行します。この問題は v3.0.6 で修正されました。中国語の[ケース-820](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case820.md)を参照してください。

-   6.1.10Drainerのレプリケーションがハングします。プロセスはアクティブなままですが、チェックポイントは更新されません。

    -   この問題は v3.0.4 で修正されました。中国語の[ケース-741](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case741.md)を参照してください。

-   6.1.11 すべてのコンポーネントがパニックになります。

    -   [バグを報告](https://github.com/pingcap/tidb-binlog/issues/new?labels=bug&#x26;template=bug-report.md) 。

### 6.2 データの移行 {#6-2-data-migration}

-   6.2.1 TiDB Data Migration (DM) は、MySQL/MariaDB から TiDB へのデータ移行をサポートする移行ツールです。詳細は[GitHub の DM](https://github.com/pingcap/dm/)を参照してください。

-   6.2.2 `Access denied for user 'root'@'172.31.43.27' (using password: YES)` `query status`実行するか、ログを確認すると表示されます。

    -   すべての DM 構成ファイル内のデータベース関連のパスワードは、 `dmctl`で暗号化する必要があります。データベースのパスワードが空の場合、パスワードを暗号化する必要はありません。 v1.0.6 以降、平文パスワードが使用できるようになりました。
    -   DM 操作中、アップストリームおよびダウンストリーム データベースのユーザーは、対応する読み取りおよび書き込み権限を持っている必要があります。データ複製タスクの開始中に、データ移行も[対応する権限を事前チェックします](/dm/dm-precheck.md)に行われます。
    -   DM クラスターに異なるバージョンの DM-worker/DM-master/dmctl をデプロイするには、中国語の[AskTUG のケーススタディ](https://asktug.com/t/dm1-0-0-ga-access-denied-for-user/1049/5)を参照してください。

-   6.2.3 レプリケーション タスクが中断され、 `driver: bad connection`エラーが返されます。

    -   `driver: bad connection`エラーは、DM とダウンストリーム TiDB データベース間の接続で異常が発生し (ネットワーク障害や TiDB の再起動など)、現在のリクエストのデータがまだ TiDB に送信されていないことを示します。

        -   DM 1.0.0 GA より前のバージョンの場合は、 `stop-task`を実行してタスクを停止し、 `start-task`を実行してタスクを再開します。
        -   DM 1.0.0 GA 以降のバージョンでは、このタイプのエラーに対する自動再試行メカニズムが追加されています。 [#265](https://github.com/pingcap/dm/pull/265)を参照してください。

-   6.2.4 レプリケーション タスクが`invalid connection`エラーで中断される。

    -   `invalid connection`エラーは、DM とダウンストリーム TiDB データベース間の接続で異常が発生し (ネットワーク障害、TiDB の再起動、TiKV ビジーなど)、現在のリクエストのデータの一部が TiDB に送信されたことを示します。 DM にはレプリケーション タスクでデータをダウンストリームに同時にレプリケートする機能があるため、タスクが中断されるといくつかのエラーが発生する可能性があります。これらのエラーは、 `query-status`または`query-error`を実行して確認できます。

        -   増分レプリケーション プロセス中にエラーが`invalid connection`だけ発生した場合、DM はタスクを自動的に再試行します。
        -   DM が再試行しない場合、またはバージョンの問題により自動的に再試行に失敗する場合 (自動再試行は v1.0.0-rc.1 で導入されています)、 `stop-task`を使用してタスクを停止し、 `start-task`使用してタスクを再開します。

-   6.2.5 リレー ユニットがエラー`event from * in * diff from passed-in event *`を報告するか、レプリケーション タスクがbinlogの取得または解析に失敗するエラー ( `get binlog error ERROR 1236 (HY000) and binlog checksum mismatch, data may be corrupted returned`など) で中断されます。

    -   DM がリレー ログまたは増分レプリケーションを取得するプロセス中に、アップストリームのbinlogファイルのサイズが 4 GB を超える場合、この 2 つのエラーが発生する可能性があります。

    -   原因: リレー ログを書き込むとき、DM はbinlogの位置とbinlogログ ファイルのサイズに基づいてイベント検証を実行し、レプリケートされたbinlogの位置をチェックポイントとして保存する必要があります。ただし、公式の MySQL は uint32 を使用してbinlogの位置を保存します。これは、4 GB を超えるbinlogファイルのbinlogの位置がオーバーフローし、上記のエラーが発生することを意味します。

    -   解決：

        -   中継処理ユニットの場合、 [レプリケーションを手動で回復する](https://pingcap.com/docs/tidb-data-migration/dev/error-handling/#the-relay-unit-throws-error-event-from--in--diff-from-passed-in-event--or-a-replication-task-is-interrupted-with-failing-to-get-or-parse-binlog-errors-like-get-binlog-error-error-1236-hy000-and-binlog-checksum-mismatch-data-may-be-corrupted-returned) ．
        -   binlogレプリケーション処理ユニットの場合、 [レプリケーションを手動で回復する](https://pingcap.com/docs/tidb-data-migration/dev/error-handling/#the-relay-unit-throws-error-event-from--in--diff-from-passed-in-event--or-a-replication-task-is-interrupted-with-failing-to-get-or-parse-binlog-errors-like-get-binlog-error-error-1236-hy000-and-binlog-checksum-mismatch-data-may-be-corrupted-returned) 。

-   6.2.6 DM レプリケーションが中断され、ログが`ERROR 1236 (HY000) The slave is connecting using CHANGE MASTER TO MASTER_AUTO_POSITION = 1, but the master has purged binary logs containing GTIDs that the slave requires.`を返す

    -   マスターbinlogがパージされているかどうかを確認します。
    -   `relay.meta`で記録した位置情報を確認します。

        -   `relay.meta`には空の GTID 情報が記録されています。 DM-worker は、終了時または 30 秒ごとに、メモリ内の GTID 情報を`relay.meta`に保存します。 DM-worker は上流の GTID 情報を取得できなかった場合、空の GTID 情報を`relay.meta`に保存します。中国語の[ケース-772](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case772.md)を参照してください。

        -   `relay.meta`で記録されたbinlogイベントにより、不完全なリカバリ プロセスがトリガーされ、間違った GTID 情報が記録されます。この問題は v1.0.2 で修正されており、それ以前のバージョンでも発生する可能性があります。 <!--See [case-764](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case764.md).-->

-   6.2.7 DM レプリケーション プロセスがエラー`Error 1366: incorrect utf8 value eda0bdedb29d(\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd)`を返します。

    -   この値は MySQL 8.0 または TiDB に正常に書き込むことはできませんが、 MySQL 5.7には書き込むことができます。 `tidb_skip_utf8_check`パラメータを有効にすると、データ形式のチェックをスキップできます。

### 6.3 TiDB Lightning {#6-3-tidb-lightning}

-   6.3.1 TiDB Lightning は、大量のデータを TiDB クラスターに高速に完全インポートするためのツールです。 [GitHub 上のTiDB Lightning](https://github.com/pingcap/tidb/tree/release-7.5/br/pkg/lightning)を参照してください。

-   6.3.2 インポート速度が遅すぎます。

    -   `region-concurrency`の設定が高すぎると、スレッドの競合が発生し、パフォーマンスが低下します。トラブルシューティングを行う 3 つの方法:

        -   設定は、ログの先頭から検索`region-concurrency`で見つけることができます。
        -   TiDB Lightning が他のサービス (たとえば、インポーター) とサーバーを共有する場合は、そのサーバー上の合計 CPU コア数の`region-concurrency` ～ 75% を手動で設定する必要があります。
        -   CPU にクォータがある場合 (たとえば、Kubernetes 設定によって制限されている場合)、 TiDB Lightning はこれを読み取れない可能性があります。この場合、手動で`region-concurrency`を減らす必要もあります。

    -   インデックスを追加するたびに、行ごとに新しい KV ペアが導入されます。 N 個のインデックスがある場合、インポートされる実際のサイズは、 [Dumpling](/dumpling-overview.md)の出力サイズの約 (N+1) 倍になります。インデックスが無視できる場合は、まずスキーマからインデックスを削除し、インポートの完了後に`CREATE INDEX`を介して追加し直すことができます。

    -   TiDB Lightningのバージョンが古いです。最新バージョンを試してください。インポート速度が向上する可能性があります。

-   6.3.3 `checksum failed: checksum mismatched remote vs local` .

    -   原因 1: テーブルにはすでにデータが含まれている可能性があります。これらの古いデータは最終チェックサムに影響を与える可能性があります。

    -   原因 2: ターゲット データベースのチェックサムが 0 の場合 (何もインポートされていないことを意味します)、クラスタが熱くなりすぎてデータの取り込みに失敗している可能性があります。

    -   原因 3: データ ソースがマシンによって生成され、 [Dumpling](/dumpling-overview.md)によってバックアップされていない場合は、テーブルの制約が尊重されていることを確認してください。例えば：

        -   `AUTO_INCREMENT`列は正である必要があり、値「0」を含めることはできません。
        -   UNIQUE キーと PRIMARY KEY には重複したエントリがあってはなりません。

    -   解決策: [トラブルシューティングの解決策](/tidb-lightning/troubleshoot-tidb-lightning.md#checksum-failed-checksum-mismatched-remote-vs-local)を参照してください。

-   6.3.4 `Checkpoint for … has invalid status:(error code)`

    -   原因: チェックポイントが有効になっており、Lightning/Importer が以前に異常終了しました。偶発的なデータ破損を防ぐため、エラーが解決されるまでTiDB Lightning は起動しません。エラー コードは 25 未満の整数で、可能な値は`0, 3, 6, 9, 12, 14, 15, 17, 18, 20 and 21`です。整数は、インポート プロセスで予期しない終了が発生したステップを示します。整数が大きいほど、終了が遅くなります。

    -   解決策: [トラブルシューティングの解決策](/tidb-lightning/troubleshoot-tidb-lightning.md#checkpoint-for--has-invalid-status-error-code)を参照してください。

-   6.3.5 `cannot guess encoding for input file, please convert to UTF-8 manually`

    -   原因: TiDB Lightning は、 UTF-8 および GB-18030 エンコーディングのみをサポートします。このエラーは、ファイルがこれらのエンコーディングのいずれでもないことを意味します。過去の ALTER TABLE 実行により、ファイルに UTF-8 の文字列と GB-18030 の別の文字列が含まれるなど、エンコーディングが混在している可能性もあります。

    -   解決策: [トラブルシューティングの解決策](/tidb-lightning/troubleshoot-tidb-lightning.md#cannot-guess-encoding-for-input-file-please-convert-to-utf-8-manually)を参照してください。

-   6.3.6 `[sql2kv] sql encode error = [types:1292]invalid time format: '{1970 1 1 0 45 0 0}'`

    -   原因: タイムスタンプ タイプのエントリに存在しない時刻値が含まれています。これは、DST の変更または時刻値がサポートされている範囲 (1970 年 1 月 1 日から 2038 年 1 月 19 日まで) を超えているためです。

    -   解決策: [トラブルシューティングの解決策](/tidb-lightning/troubleshoot-tidb-lightning.md#sql2kv-sql-encode-error--types1292invalid-time-format-1970-1-1-)を参照してください。

## 7. 共通ログ分析 {#7-common-log-analysis}

### 7.1 TiDB {#7-1-tidb}

-   7.1.1 `GC life time is shorter than transaction duration` ．

    トランザクション期間が GC 有効期間 (デフォルトでは 10 分) を超えています。

    [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)システム変数を変更すると、GC の寿命を延ばすことができます。一般に、このパラメータを変更することはお勧めできません。このトランザクションに多数の`UPDATE`と`DELETE`ステートメントがある場合、このパラメータを変更すると古いバージョンが大量に蓄積される可能性があるためです。

-   7.1.2 `txn takes too much time` .

    このエラーは、長期間 (590 秒以上) コミットされていないトランザクションをコミットすると返されます。

    アプリケーションでこのような長時間のトランザクションを実行する必要がある場合は、 `[tikv-client] max-txn-time-use = 590`パラメータと GC 有効期間を長くして、この問題を回避できます。アプリケーションにそれほど長いトランザクション時間が必要かどうかを確認することをお勧めします。

-   7.1.3 `coprocessor.go`レポート`request outdated` 。

    このエラーは、TiKV に送信されたコプロセッサー要求が TiKV のキュー内で 60 秒以上待機した場合に返されます。

    TiKV コプロセッサーが長いキューに入っている理由を調査する必要があります。

-   7.1.4 `region_cache.go` `switch region peer to next due to send request fail`という大きな数を報告し、エラー メッセージは`context deadline exceeded`です。

    TiKV のリクエストがタイムアウトになり、リージョン キャッシュがトリガーされてリクエストが他のノードに切り替わりました。ログの`addr`フィールドに対して`grep "<addr> cancelled`コマンドを引き続き実行し、 `grep`結果に応じて次の手順を実行できます。

    -   `send request is cancelled` : リクエストは送信フェーズ中にタイムアウトしました。 **Grafana** -&gt; **TiDB** -&gt; **Batch Client** / `Pending Request Count by TiKV`のモニタリングを調査し、保留中のリクエスト数が 128 を超えているかどうかを確認できます。

        -   128より大きい場合はKVの処理能力を超えて送信が溜まってしまいます。
        -   値が 128 以下の場合は、ログをチェックして、レポートが対応する KV の運用およびメンテナンスの変更によって引き起こされたものであるかどうかを確認します。それ以外の場合、このエラーは予期しないものであるため、 [バグを報告](https://github.com/pingcap/tidb/issues/new?labels=type%2Fbug&#x26;template=bug-report.md)を行う必要があります。

    -   `wait response is cancelled` : リクエストは TiKV に送信された後にタイムアウトしました。対応する TiKV アドレスの応答時間と、その時点の PD および KV のリージョンログを確認する必要があります。

-   7.1.5 `distsql.go`レポート`inconsistent index` 。

    データインデックスが矛盾しているようです。報告されたインデックスがあるテーブルで`admin check table <TableName>`コマンドを実行します。チェックが失敗した場合は、次のコマンドと[バグを報告](https://github.com/pingcap/tidb/issues/new?labels=type%2Fbug&#x26;template=bug-report.md)を実行してガベージコレクションを無効にします。

    ```sql
    SET GLOBAL tidb_gc_enable = 0;
    ```

### 7.2 TiKV {#7-2-tikv}

-   7.2.1 `key is locked` ．

    読み取りと書き込みに競合があります。読み取りリクエストはコミットされていないデータを検出したため、データがコミットされるまで待つ必要があります。

    このエラーが少数であればビジネスに影響はありませんが、このエラーが多数発生する場合は、ビジネス内で読み取りと書き込みの競合が深刻であることを示しています。

-   7.2.2 `write conflict` .

    これは、楽観的トランザクションにおける書き込みと書き込みの競合です。複数のトランザクションが同じキーを変更した場合、1 つのトランザクションのみが成功し、他のトランザクションは自動的にタイムスタンプを再度取得して操作を再試行しますが、ビジネスには影響しません。

    競合が深刻な場合は、複数回の再試行後にトランザクションが失敗する可能性があります。この場合、悲観的ロックを使用することをお勧めします。エラーと解決策の詳細については、 [オプティミスティック トランザクションでの書き込み競合のトラブルシューティング](/troubleshoot-write-conflicts.md)を参照してください。

-   7.2.3 `TxnLockNotFound` .

    このトランザクションのコミットが遅すぎるため、Time To Live (TTL) 後に他のトランザクションによってロールバックされます。このトランザクションは自動的に再試行されるため、通常はビジネスに影響はありません。サイズが 0.25 MB 以下のトランザクションの場合、デフォルトの TTL は 3 秒です。詳細については、 [`LockNotFound`ファウンドエラー](/troubleshoot-lock-conflicts.md#locknotfound-error)参照してください。

-   7.2.4 `PessimisticLockNotFound` .

    `TxnLockNotFound`と同様です。悲観的トランザクションのコミットは遅すぎるため、他のトランザクションによってロールバックされます。

-   7.2.5 `stale_epoch` .

    リクエスト エポックが古いため、TiDB はルーティングを更新した後にリクエストを再送信します。ビジネスには影響ありません。リージョンで分割/マージ操作が行われるか、レプリカが移行されると、エポックが変更されます。

-   7.2.6 `peer is not leader` ．

    リクエストはLeaderではないレプリカに送信されます。エラー応答がどのレプリカが最新のLeaderであるかを示している場合、TiDB はエラーに従ってローカル ルーティングを更新し、新しいリクエストを最新のLeaderに送信します。通常、ビジネスには影響はありません。

    v3.0 以降のバージョンでは、以前のLeaderへのリクエストが失敗した場合、TiDB は他のピアを試行し、TiKV ログに`peer is not leader`頻繁に記録される可能性があります。 TiDB の対応するリージョンの`switch region peer to next due to send request fail`を確認して、送信失敗の根本原因を特定できます。詳細は[7.1.4](#71-tidb)を参照してください。

    このエラーは、他の理由によりリージョンにLeaderがない場合にも返される可能性があります。詳細は[4.4](#44-some-tikv-nodes-drop-leader-frequently)を参照してください。
