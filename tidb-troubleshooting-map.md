---
title: TiDB Troubleshooting Map
summary: Learn how to troubleshoot common errors in TiDB.
---

# TiDBトラブルシューティングマップ {#tidb-troubleshooting-map}

このドキュメントは、TiDBおよびその他のコンポーネントの一般的な問題をまとめたものです。このマップを使用して、関連する問題が発生したときに問題を診断および解決できます。

## 1.利用できないサービス {#1-service-unavailable}

### 1.1クライアント<code>Region is Unavailable</code>エラーを報告する {#1-1-the-client-reports-code-region-is-unavailable-code-error}

-   1.1.1 `Region is Unavailable`エラーは通常、リージョンが一定期間利用できないことが原因です。 `TiKV server is busy`が発生するか、 `not leader`または`epoch not match`が原因でTiKVへの要求が失敗するか、TiKVへの要求がタイムアウトする可能性があります。このような場合、TiDBは`backoff`の再試行メカニズムを実行します。 `backoff`がしきい値（デフォルトでは20秒）を超えると、エラーがクライアントに送信されます。 `backoff`のしきい値内では、このエラーはクライアントには表示されません。

-   1.1.2複数のTiKVインスタンスが同時にOOMであるため、OOM期間中にリーダーは発生しません。中国語の[ケース-991](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case991.md)を参照してください。

-   1.1.3 TiKVは`TiKV server is busy`を報告し、 `backoff`回を超えています。詳細については、 [4.3](#43-the-client-reports-the-server-is-busy-error)を参照してください。 `TiKV server is busy`は内部フロー制御メカニズムの結果であり、 `backoff`回でカウントされるべきではありません。この問題は修正されます。

-   1.1.4複数のTiKVインスタンスの開始に失敗したため、リージョン内にリーダーが存在しません。複数のTiKVインスタンスが物理マシンにデプロイされている場合、ラベルが適切に構成されていないと、物理マシンに障害が発生すると、リージョン内にリーダーが存在しなくなる可能性があります。中国語の[ケース-228](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case228.md)を参照してください。

-   1.1.5フォロワーの適用が前のエポックで遅れている場合、フォロワーがリーダーになった後、 `epoch not match`でリクエストを拒否します。中国語の[ケース-958](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case958.md)を参照してください（TiKVはそのメカニズムを最適化する必要があります）。

### 1.2 PDエラーにより、サービスが利用できなくなります {#1-2-pd-errors-cause-service-unavailable}

[5つのPDの問題](#5-pd-issues)を参照してください。

## 2.レイテンシーが大幅に増加します {#2-latency-increases-significantly}

### 2.1一時的な増加 {#2-1-transient-increase}

-   2.1.1 TiDB実行プランが間違っていると、遅延が増加します。 [3.3](#33-wrong-execution-plan)を参照してください。
-   2.1.2PDリーダー選出問題またはOOM。 [5.2](#52-pd-election)と[5.3](#53-pd-oom)を参照してください。
-   2.1.3一部のTiKVインスタンスでは、かなりの数のリーダーがドロップします。 [4.4](#44-some-tikv-nodes-drop-leader-frequently)を参照してください。

### 2.2持続的かつ大幅な増加 {#2-2-persistent-and-significant-increase}

-   2.2.1TiKVシングルスレッドのボトルネック

    -   TiKVインスタンスのリージョンが多すぎると、単一のgRPCスレッドがボトルネックになります（Grafana-&gt; **TiKV** <strong>-details-</strong> &gt; <strong>Thread CPU / gRPC CPU Per Thread</strong>メトリックを確認してください）。 v3.x以降のバージョンでは、 `Hibernate Region`を有効にして問題を解決できます。中国語の[ケース-612](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case612.md)を参照してください。

    -   v3.0より前のバージョンでは、raftstoreスレッドまたはapplyスレッドがボトルネックになったときに（ **Grafana-** &gt; <strong>TiKV-details-</strong> &gt; <strong>Thread CPU /</strong> raftstoreCPUおよび<strong>AsyncapplyCPU</strong>メトリックが`80%`を超える）、TiKV（v2 .x）インスタンスまたはマルチスレッドを使用したv3.xへのアップグレード。 <!-- See [case-517](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case517.md) in Chinese. -->

-   2.2.2CPU負荷が増加します。

-   2.2.3TiKVの遅い書き込み。 [4.5](#45-tikv-write-is-slow)を参照してください。

-   2.2.4TiDBの間違った実行プラン。 [3.3](#33-wrong-execution-plan)を参照してください。

## 3.TiDBの問題 {#3-tidb-issues}

### 3.1 DDL {#3-1-ddl}

-   3.1.1 `decimal`フィールドの長さを変更すると、エラー`ERROR 1105 (HY000): unsupported modify decimal column precision`が報告されます。 <!--See [case-1004](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case517.md) in Chinese.--> TiDBは、 `decimal`フィールドの長さの変更をサポートしていません。

-   3.1.2 TiDB DDLジョブがハングするか、実行が遅い（ `admin show ddl jobs`を使用してDDLの進行状況を確認する）

    -   原因1：他のコンポーネント（PD / TiKV）とのネットワークの問題。

    -   原因2：初期バージョンのTiDB（v3.0.8より前）では、同時実行性が高いためにゴルーチンが多いため、内部負荷が大きくなります。

    -   原因3：初期バージョン（v2.1.15およびバージョン&lt;v3.0.0-rc1）では、PDインスタンスがTiDBキーの削除に失敗するため、すべてのDDL変更が2つのリースを待機します。

    -   その他の不明な原因については、 [バグを報告](https://github.com/pingcap/tidb/issues/new?labels=type%2Fbug&#x26;template=bug-report.md) 。

    -   解決：

        -   原因1については、TiDBとTiKV/PD間のネットワーク接続を確認してください。
        -   原因2および3の場合、問題は後のバージョンですでに修正されています。 TiDBを新しいバージョンにアップグレードできます。
        -   その他の原因については、DDL所有者を移行する次のソリューションを使用できます。

    -   DDL所有者の移行：

        -   TiDBサーバーに接続できる場合は、所有者選択コマンドを再度実行します`curl -X POST http://{TiDBIP}:10080/ddl/owner/resign`
        -   TiDBサーバーに接続できない場合は、 `tidb-ctl`を使用してPDクラスタのetcdからDDL所有者を削除し、再選をトリガーします`tidb-ctl etcd delowner [LeaseID] [flags] + ownerKey`

-   3.1.3TiDBはログに`information schema is changed`のエラーを報告します

    -   原因1：DML操作がDDLの下にある表に触れています。 `admin show ddl job`を使用して、現在進行中のDDLを確認できます。

    -   原因2：現在のDML操作の実行時間が長すぎます。この間、多くのDDL操作が実行されるため、 `schema version`の変更が1024を超えます。新しいバージョン`lock table`でも、スキーマのバージョンが変更される可能性があります。

    -   原因3：現在DMLステートメントを実行しているTiDBインスタンスが新しい`schema information`をロードできません（PDまたはTiKVのネットワークの問題が原因である可能性があります）。この間、多くのDDLステートメントが実行され（ `lock table`を含む）、 `schema version`の変更が1024を超えます。

    -   解決策：関連するDML操作は失敗後に再試行するため、最初の2つの原因はアプリケーションに影響を与えません。原因3については、TiDBとTiKV/PD間のネットワークを確認する必要があります。

    -   背景： `schema version`の数の増加は、各DDL変更操作の`schema state`の数と一致しています。たとえば、 `create table`操作には1つのバージョン変更があり、 `add column`操作には4つのバージョン変更があります。したがって、列変更操作が多すぎると、 `schema version`が急速に増加する可能性があります。詳しくは[オンラインスキーマの変更](https://static.googleusercontent.com/media/research.google.com/zh-CN//pubs/archive/41376.pdf)をご覧ください。

-   3.1.4TiDBはログに`information schema is out of date`を報告します

    -   原因1：DMLステートメントを実行しているTiDBサーバーが`graceful kill`で停止し、終了する準備をしています。 DMLステートメントを含むトランザクションの実行時間が1つのDDLリースを超えています。トランザクションがコミットされると、エラーが報告されます。

    -   原因2：TiDBサーバーは、DMLステートメントの実行中にPDまたはTiKVに接続できません。その結果、TiDBサーバーが1つのDDLリース（デフォルトでは`45s` ）内で新しいスキーマをロードしなかったか、TiDBサーバーが`keep alive`の設定でPDから切断されました。

    -   原因3：TiKVの負荷が高いか、ネットワークがタイムアウトしました。 **Grafana-** &gt; <strong>TiDB</strong>および<strong>TiKV</strong>でノードの負荷を確認します。

    -   解決：

        -   原因1については、TiDBの起動時にDML操作を再試行してください。
        -   原因2については、TiDBサーバーとPD/TiKV間のネットワークを確認してください。
        -   原因3については、TiKVがビジーである理由を調査してください。 [4つのTiKVの問題](#4-tikv-issues)を参照してください。

### 3.2OOMの問題 {#3-2-oom-issues}

-   3.2.1症状

    -   クライアント：クライアントはエラー`ERROR 2013 (HY000): Lost connection to MySQL server during query`を報告します。

    -   ログを確認する

        -   `dmesg -T | grep tidb-server`を実行します。結果には、エラーが発生した時点のOOM-killerログが表示されます。

        -   エラーが発生した後の時点（つまり、tidb-serverが再起動したとき）の前後に「WelcometoTiDB」ログイン`tidb.log`をgrepします。

        -   `fatal error: runtime: out of memory` `tidb_stderr.log` `cannot allocate memory` 。

        -   v2.1.8以前のバージョンでは、 `tidb_stderr.log`の`fatal error: stack overflow`をgrepできます。

    -   モニター：tidb-serverインスタンスのメモリ使用量は、短期間に急激に増加します。

-   3.2.2OOMの原因となるSQLステートメントを見つけます。 （現在、TiDBのすべてのバージョンでSQLを正確に特定することはできません。特定した後、OOMがSQLステートメントによって引き起こされているかどうかを分析する必要があります。）

    -   バージョン&gt;=v3.0.0の場合、grep &quot;expensive_query&quot; `tidb.log` 。そのログメッセージは、タイムアウトした、またはメモリクォータを超えたSQLクエリを記録します。

    -   バージョン&lt;v3.0.0の場合、メモリクォータを超えるSQLクエリを見つけるために、grep「メモリがクォータを超えています」を`tidb.log`で指定します。

    > **ノート：**
    >
    > 単一のSQLメモリ使用量のデフォルトのしきい値は`1GB`です。このパラメーターは、システム変数[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)を構成することで設定できます。

-   3.2.3OOMの問題を軽減する

    -   `SWAP`を有効にすることで、大規模なクエリによるメモリの過剰使用によって引き起こされるOOMの問題を軽減できます。メモリが不足している場合、この方法はI / Oオーバーヘッドのために、大規模なクエリのパフォーマンスに影響を与える可能性があります。パフォーマンスへの影響の程度は、残りのメモリスペースとディスクI/O速度によって異なります。

-   3.2.4OOMの一般的な理由

    -   SQLクエリには`join`があります。 `explain`を使用してSQLステートメントを表示すると、 `join`操作で`HashJoin`アルゴリズムが選択され、 `inner`テーブルが大きいことがわかります。

    -   1つの`UPDATE/DELETE`クエリのデータ量が多すぎます。中国語の[ケース-882](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case882.md)を参照してください。

    -   SQLには、 `Union`で接続された複数のサブクエリが含まれています。中国語の[ケース-1828](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case1828.md)を参照してください。

### 3.3間違った実行計画 {#3-3-wrong-execution-plan}

-   3.3.1症状

    -   SQLクエリの実行時間は、以前の実行に比べてはるかに長いか、実行プランが突然変更されます。実行プランが低速ログに記録されている場合は、実行プランを直接比較できます。

    -   SQLクエリの実行時間は、MySQLなどの他のデータベースに比べてはるかに長くなります。実行プランを他のデータベースと比較して、 `Join Order`などの違いを確認します。

    -   遅いログでは、SQL実行時間`Scan Keys`の数が多くなります。

-   3.3.2実行計画を調査する

    -   `explain analyze {SQL}` 。実行時間が許容できる場合は、 `explain analyze`の結果の`count`と`execution info`の`row`の数を比較します。 `TableScan/IndexScan`行に大きな違いが見つかった場合は、統計が正しくない可能性があります。他の行に大きな違いが見つかった場合、問題は統計にない可能性があります。

    -   `select count(*)` 。実行プランに`join`の操作が含まれている場合、 `explain analyze`には時間がかかる場合があります。 `TableScan/IndexScan`の条件に対して`select count(*)`を実行し、 `explain`の結果の`row count`の情報を比較することにより、問題が統計にあるかどうかを確認できます。

-   3.3.3緩和

    -   v3.0以降のバージョンでは、 `SQL Bind`機能を使用して実行プランをバインドします。

    -   統計を更新します。問題の原因が統計であるとおおまかに確信している場合は、 [統計をダンプする](/statistics.md#export-statistics) 。 `modify count/row count` in `show stats_meta`が特定の値（たとえば、0.3）より大きいなど、原因が古い統計である場合、またはテーブルに時間列のインデックスがある場合は、 `analyze table`を使用して回復を試みることができます。 `auto analyze`が構成されている場合は、 `tidb_auto_analyze_ratio`のシステム変数が大きすぎる（たとえば、0.3より大きい）かどうか、および現在の時刻が`tidb_auto_analyze_start_time`から`tidb_auto_analyze_end_time`の間であるかどうかを確認します。

    -   その他の状況では、 [バグを報告](https://github.com/pingcap/tidb/issues/new?labels=type%2Fbug&#x26;template=bug-report.md) 。

### 3.4SQL実行エラー {#3-4-sql-execution-error}

-   3.4.1クライアントは`ERROR 1265(01000) Data Truncated`のエラーを報告します。これは、TiDBが内部で`Decimal`型の精度を計算する方法が、MySQLの精度と互換性がないためです。この問題はv3.0.10（ [＃14438](https://github.com/pingcap/tidb/pull/14438) ）で修正されています。

    -   原因：

        MySQLでは、2つの高精度`Decimal`が分割され、結果が最大10進精度（ `30` ）を超える場合、 `30`桁のみが予約され、エラーは報告されません。

        TiDBでは、計算結果はMySQLと同じですが、 `Decimal`を表すデータ構造内では、10進精度のフィールドは実際の精度を保持します。

        例として`(0.1^30) / 10`を取り上げます。精度が最大で`30`であるため、TiDBとMySQLの結果は両方とも`0`です。ただし、TiDBでは、10進精度のフィールドは`31`のままです。

        複数の`Decimal`分割の後、結果が正しい場合でも、この精度フィールドはますます大きくなり、最終的にTiDBのしきい値（ `72` ）を超える可能性があり、 `Data Truncated`エラーが報告されます。

        `Decimal`の乗算では、範囲外がバイパスされ、精度が最大精度制限に設定されるため、この問題は発生しません。

    -   解決策： `Cast(xx as decimal(a, b))`を手動で追加することで、この問題を回避できます。ここで、 `a`と`b`がターゲット精度です。

## 4.TiKVの問題 {#4-tikv-issues}

### 4.1 TiKVがパニックになり、起動に失敗する {#4-1-tikv-panics-and-fails-to-start}

-   `sync-log = false` 。マシンの電源をオフにすると、 `unexpected raft log index: last_index X < applied_index Y`エラーが返されます。

    この問題は予想されます。 `tikv-ctl`を使用してリージョンを復元できます。

-   4.1.2 TiKVが仮想マシンにデプロイされている場合、仮想マシンが強制終了されるか、物理マシンの電源がオフになると、 `entries[X, Y]  is unavailable from storage`エラーが報告されます。

    この問題は予想されます。仮想マシンの`fsync`は信頼できないため、 `tikv-ctl`を使用してリージョンを復元する必要があります。

-   4.1.3その他の予期しない原因については、 [バグを報告](https://github.com/tikv/tikv/issues/new?template=bug-report.md) 。

### 4.2 TiKV OOM {#4-2-tikv-oom}

-   4.2.1 `block-cache`の構成が大きすぎると、OOMが発生する可能性があります。

    問題の原因を確認するには、モニター**Grafana-** &gt; <strong>TiKV-details</strong>で対応するインスタンスを選択して、RocksDBの`block cache size`を確認します。

    その間、 `[storage.block-cache] capacity = # "1GB"`パラメータが正しく設定されているか確認してください。デフォルトでは、TiKVの`block-cache`はマシンの合計メモリの`45%`に設定されています。 TiKVは物理マシンのメモリを取得するため、コンテナにTiKVをデプロイするときに、このパラメータを明示的に指定する必要があります。これは、コンテナのメモリ制限を超える可能性があります。

-   4.2.2コプロセッサーは多くの大きなクエリを受け取り、大量のデータを返します。 gRPCは、コプロセッサーがデータを返すのと同じ速さでデータを送信できず、その結果OOMになります。

    原因を確認するには、モニターの**Grafana-** &gt; <strong>TiKV-</strong> details-&gt; coprocessor Overviewを表示して、 `response size`が`network outbound`トラフィックを超えているかどうかを確認でき<strong>ます</strong>。

-   4.2.3他のコンポーネントはメモリを占有しすぎます。

    この問題は予期しないものです。あなたは[バグを報告](https://github.com/tikv/tikv/issues/new?template=bug-report.md)することができます。

### 4.3クライアントが<code>server is busy</code>エラーであると報告する {#4-3-the-client-reports-the-code-server-is-busy-code-error}

モニターの**Grafana-** &gt; <strong>TiKV-</strong> &gt;<strong>エラー</strong>を表示して、ビジーの特定の原因を確認します。 `server is busy`は、TiKVのフロー制御メカニズムによって引き起こされます。これは、 `tidb/ti-client`に現在圧力がかかりすぎていることを通知し、後で再試行します。

-   4.3.1TiKVRocksDBが`write stall`に遭遇します。

    TiKVインスタンスには2つのRocksDBインスタンスがあります`data/raft`つはRaftログを保存するためのもので、もう`data/db`つは実際のデータを保存するためのものです。ログで`grep "Stalling" RocksDB`を実行すると、ストールの具体的な原因を確認できます。 RocksDBログは`LOG`で始まるファイルであり、 `LOG`は現在のログです。

    -   `level0 sst`が多すぎるとストールが発生します。 `[rocksdb] max-sub-compactions = 2` （または3）パラメーターを追加して、 `level0 sst`の圧縮を高速化できます。 level0からlevel1への圧縮タスクは、同時に実行されるいくつかのサブタスク（サブタスクの最大数は`max-sub-compactions`の値）に分割されます。中国語の[ケース-815](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case815.md)を参照してください。

    -   `pending compaction bytes`が多すぎるとストールが発生します。ディスクI/Oは、ビジネスのピーク時に書き込み操作に追いつくことができません。対応するCFの`soft-pending-compaction-bytes-limit`と`hard-pending-compaction-bytes-limit`を増やすことで、この問題を軽減できます。

        -   デフォルト値の`[rocksdb.defaultcf] soft-pending-compaction-bytes-limit`は`64GB`です。保留中の圧縮バイトがしきい値に達すると、RocksDBは書き込み速度を遅くします。 `[rocksdb.defaultcf] soft-pending-compaction-bytes-limit`を設定でき`128GB` 。

        -   デフォルト値の`hard-pending-compaction-bytes-limit`は`256GB`です。保留中の圧縮バイトがしきい値に達すると（保留中の圧縮バイトが`soft-pending-compaction-bytes-limit`に達した後、RocksDBは書き込みを遅くするため、これは発生しない可能性があります）、RocksDBは書き込み操作を停止します。 `hard-pending-compaction-bytes-limit`から`512GB`まで設定できます。 <!-- See [case-275](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case275.md) in Chinese.-->

        -   ディスクI/O容量が長時間書き込みに追いつかない場合は、ディスクをスケールアップすることをお勧めします。ディスクスループットが上限に達し、書き込みストールが発生する場合（たとえば、SATASSDがNVMESSDよりもはるかに低い場合）、CPUリソースは十分ですが、より高い圧縮率の圧縮アルゴリズムを適用できます。このようにして、CPUリソースがディスクリソースと交換され、ディスクへの負荷が軽減されます。

        -   デフォルトのCF圧縮で高圧が発生した場合は、 `[rocksdb.defaultcf] compression-per-level`パラメーターを`["no", "no", "lz4", "lz4", "lz4", "zstd", "zstd"]`から`["no", "no", "zstd", "zstd", "zstd", "zstd", "zstd"]`に変更します。

    -   memtableが多すぎると、ストールが発生します。これは通常、インスタント書き込みの量が多く、メモリテーブルがディスクにゆっくりフラッシュする場合に発生します。ディスクの書き込み速度を改善できず、この問題がビジネスのピーク時にのみ発生する場合は、対応するCFの`max-write-buffer-number`を増やすことで軽減できます。

        -   たとえば、 `[rocksdb.defaultcf] max-write-buffer-number`を`8`に設定します（デフォルトでは`5` ）。より多くのmemtableがメモリ内にある可能性があるため、これによりピーク時により多くのメモリ使用量が発生する可能性があることに注意してください。

-   `scheduler too busy`

    -   深刻な書き込みの競合。 `latch wait duration`は高いです。モニター**Grafana-** &gt; <strong>TiKV-</strong> details-&gt;スケジューラープリ<strong>ライト</strong>/<strong>スケジューラーコミット</strong>で`latch wait duration`を表示できます。書き込みタスクがスケジューラーに積み重なると、保留中の書き込みタスクが`[storage] scheduler-pending-write-threshold`で設定されたしきい値（100MB）を超えます。 `MVCC_CONFLICT_COUNTER`に対応するメトリックを表示することで、原因を確認できます。

    -   書き込みが遅いと、書き込みタスクが山積みになります。 TiKVに書き込まれているデータが、 `[storage] scheduler-pending-write-threshold`で設定されたしきい値（100MB）を超えています。 [4.5](#45-tikv-write-is-slow)を参照してください。

-   `raftstore is busy` 。メッセージの処理は、メッセージの受信よりも遅くなります。短期`channel full`ステータスはサービスに影響しませんが、エラーが長期間続く場合は、リーダーの切り替えが発生する可能性があります。

    -   `append log`はストールに遭遇します。 [4.3.1](#43-the-client-reports-the-server-is-busy-error)を参照してください。
    -   `append log duration`はハイであり、メッセージの処理が遅くなります。 [4.5](#45-tikv-write-is-slow)を参照して、 `append log duration`が高い理由を分析できます。
    -   raftstoreは、大量のメッセージを瞬時に受信し（TiKV Raftメッセージダッシュボードをチェックインします）、それらの処理に失敗します。通常、短期`channel full`ステータスはサービスに影響しません。

-   4.3.4TiKVコプロセッサーがキューに入っています。積み上げられたタスクの数が`coprocessor threads * readpool.coprocessor.max-tasks-per-worker-[normal|low|high]`を超えています。大きなクエリが多すぎると、コプロセッサにタスクが積み重なってしまいます。実行プランの変更によって多数のテーブルスキャン操作が発生するかどうかを確認する必要があります。 [3.3](#33-wrong-execution-plan)を参照してください。

### 4.4一部のTiKVノードはリーダーを頻繁にドロップします {#4-4-some-tikv-nodes-drop-leader-frequently}

-   4.4.1TiKVが再起動されたための再選

    -   TiKVがパニックになった後、systemdによってプルアップされ、正常に実行されます。 TiKVログを表示することで、panicが発生したかどうかを確認できます。この問題は予期しないものであるため、発生した場合は[バグを報告](https://github.com/tikv/tikv/issues/new?template=bug-report.md)です。

    -   TiKVはサードパーティによって停止または強制終了され、systemdによってプルアップされます。 `dmesg`とTiKVログを表示して原因を確認してください。

    -   TiKVはOOMであり、再起動します。 [4.2](#42-tikv-oom)を参照してください。

    -   `THP` （Transparent Hugepage）を動的に調整するため、TiKVがハングします。中国語のケース[ケース-500](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case500.md)を参照してください。

-   4.4.2 TiKV RocksDBで書き込みストールが発生したため、再選されました。モニターの**Grafana-** &gt; <strong>TiKV-details-</strong> &gt;<strong>エラー</strong>が`server is busy`を示しているかどうかを確認できます。 [4.3.1](#43-the-client-reports-the-server-is-busy-error)を参照してください。

-   4.4.3ネットワークの分離による再選。

### 4.5TiKVの書き込みが遅い {#4-5-tikv-write-is-slow}

-   4.5.1 TiKV gRPCの`prewrite/commit/raw-put`期間を表示して、TiKV書き込みが少ないかどうかを確認します（RawKVクラスターの場合のみ）。一般的に、 [パフォーマンスマップ](https://github.com/pingcap/tidb-map/blob/master/maps/performance-map.png)に従って遅いフェーズを見つけることができます。一般的な状況のいくつかを以下に示します。

-   4.5.2スケジューラCPUがビジーです（トランザクションkvの場合のみ）。

    prewrite / commitの`scheduler command duration`は、 `scheduler latch wait duration`と`storage async write duration`の合計よりも長くなります。スケジューラワーカーは、 `scheduler-worker-pool-size` * 100％の80％を超えるなど、CPUの需要が高いか、マシン全体のCPUリソースが比較的制限されています。書き込みワークロードが大きい場合は、 `[storage] scheduler-worker-pool-size`の設定が小さすぎないか確認してください。

    その他の状況では、 [バグを報告](https://github.com/tikv/tikv/issues/new?template=bug-report.md) 。

-   4.5.3追加ログが遅い。

    TiKVGrafanaの**Raft** / `append log duration`は高く、通常はディスクの書き込み操作が遅いためです。 RocksDBの`WAL Sync Duration max`の値--raftを確認することで、原因を確認できます。

    その他の状況では、 [バグを報告](https://github.com/tikv/tikv/issues/new?template=bug-report.md) 。

-   4.5.4raftstoreスレッドはビジーです。

    **Raft Propose** / `propose wait duration`は、TiKVGrafanaの追加ログ期間よりも大幅に長くなっています。次の方法を取ります。

    -   `[raftstore] store-pool-size`構成値が小さすぎないか確認してください。値は`1`の範囲で、大きすぎないように設定することをお勧めし`5` 。
    -   本機のCPUリソースが不足していないか確認してください。

-   4.5.5適用が遅い。

    TiKVGrafanaの**Raft** / `apply log duration`は高く、通常は高い<strong>Raft Propose</strong> / `apply wait duration`が付属しています。考えられる原因は次のとおりです。

    -   `[raftstore] apply-pool-size`は小さすぎ（ `1`の値を設定し、大きすぎないことをお勧めし`5` ）、**スレッドCPU** / `apply CPU`は大きすぎます。

    -   マシンのCPUリソースが不足しています。

    -   リージョン書き込みホットスポット。単一の適用スレッドはCPU使用率が高くなります。現在、改善されている単一のリージョンのホットスポットの問題に適切に対処することはできません。各スレッドのCPU使用率を表示するには、Grafana式を変更して`by (instance, name)`を追加します。

    -   RocksDBの書き込みが遅い。 **RocksDB kv** / `max write duration`は高いです。 1つのRaftログに複数のKVが含まれる場合があります。 RocksDBに書き込む場合、128KVが書き込みバッチでRocksDBに書き込まれます。したがって、適用ログはRocksDBでの複数の書き込みに関連付けられている可能性があります。

    -   その他の状況では、 [バグを報告](https://github.com/tikv/tikv/issues/new?template=bug-report.md) 。

-   4.5.6Raftコミットログが遅い。

    TiKVGrafanaの**Raft** / `commit log duration`は高いです（このメトリックは、v4.x以降のGrafanaでのみサポートされています）。すべてのリージョンは、独立したRaftグループに対応しています。 Raftには、TCPのスライディングウィンドウメカニズムと同様のフロー制御メカニズムがあります。 `[raftstore] raft-max-inflight-msgs = 256`パラメータを設定することにより、スライディングウィンドウのサイズを制御できます。書き込みホットスポットがあり、 `commit log duration`が高い場合は、 `1024`に増やすなど、パラメーターを調整できます。

-   4.5.7その他の状況については、 [パフォーマンスマップ](https://github.com/pingcap/tidb-map/blob/master/maps/performance-map.png)の書き込みパスを参照して、原因を分析してください。

## 5.PDの問題 {#5-pd-issues}

### 5.1PDスケジューリング {#5-1-pd-scheduling}

-   5.1.1マージ

    -   テーブル全体の空のリージョンはマージできません。 TiKVの`[coprocessor] split-region-on-table`パラメーターを変更する必要があります。これは、v4.xではデフォルトで`false`に設定されています。中国語の[ケース-896](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case896.md)を参照してください。

    -   リージョンのマージが遅い。 **Grafana-** &gt; <strong>PD-</strong> &gt; <strong>operator</strong>のモニターダッシュボードにアクセスすると、マージされた演算子が生成されているかどうかを確認できます。マージを加速するには、 `merge-schedule-limit`の値を増やします。

-   5.1.2レプリカを追加するか、レプリカをオンライン/オフラインで取得します

    -   TiKVディスクは容量の80％を使用し、PDはレプリカを追加しません。この状況では、ミスピアの数が増えるため、TiKVをスケールアウトする必要があります。中国語の[ケース-801](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case801.md)を参照してください。

    -   TiKVノードがオフラインになると、一部のリージョンを他のノードに移行できなくなります。この問題はv3.0.4（ [＃5526](https://github.com/tikv/tikv/pull/5526) ）で修正されています。中国語の[ケース-870](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case870.md)を参照してください。

-   5.1.3バランス

    -   リーダー/リージョンの数は均等に分散されていません。中国語の[ケース-394](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case394.md)と[ケース-759](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case759.md)を参照してください。主な原因は、天びんがリージョン/リーダーのサイズに基づいてスケジューリングを実行するため、カウントの不均一な分布が発生する可能性があることです。 TiDB 4.0では、 `[leader-schedule-policy]`パラメータが導入されました。これにより、Leaderのスケジューリングポリシーを`count`ベースまたは`size`ベースに設定できます。

### 5.2PD選挙 {#5-2-pd-election}

-   5.2.1PDスイッチリーダー。

    -   原因1：ディスク。 PDノードが配置されているディスクには、完全なI/O負荷があります。 I/Oの需要が高くディスクの状態が良好な他のコンポーネントとともにPDが展開されているかどうかを調査します。 **Grafana-** &gt;<strong>ディスクパフォーマンス</strong>-&gt;<strong>レイテンシ</strong>/<strong>ロード</strong>でモニターメトリックを表示することで、原因を確認できます。必要に応じて、FIOツールを使用してディスクのチェックを実行することもできます。中国語の[ケース-292](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case292.md)を参照してください。

    -   原因2：ネットワーク。 PDログには`lost the TCP streaming connection`が表示されます。 PDノード間のネットワークに問題があるかどうかを確認し、モニター**Grafana-** &gt; <strong>PD-</strong> &gt; <strong>etcd</strong>で`round trip`を表示して、原因を確認する必要があります。中国語の[ケース-177](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case177.md)を参照してください。

    -   原因3：システム負荷が高い。ログには`server is likely overloaded`が表示されます。中国語の[ケース-214](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case214.md)を参照してください。

-   5.2.2 PDがリーダーを選出できないか、選出が遅い。

    -   PDはリーダーを選出できません：PDログには`lease is not expired`が表示されます。 [この問題](https://github.com/etcd-io/etcd/issues/10355)はv3.0.xおよびv2.1.19で修正されました。中国語の[ケース-875](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case875.md)を参照してください。

    -   選挙は遅い：リージョンの読み込み期間は長い。この問題は、PDログで`grep "regions cost"`を実行することで確認できます。結果が`load 460927 regions cost 11.77099s`秒などの秒単位の場合は、リージョンの読み込みが遅いことを意味します。 `use-region-storage`を`true`に設定すると、v3.0で`region storage`機能を有効にできます。これにより、リージョンの読み込み時間が大幅に短縮されます。中国語の[ケース-429](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case429.md)を参照してください。

-   5.2.3TiDBがSQLステートメントを実行するとPDがタイムアウトしました。

    -   PDにリーダーがないか、リーダーを切り替えます。 [5.2.1](#52-pd-election)と[5.2.2](#52-pd-election)を参照してください。

    -   ネットワークの問題。モニター**Grafana-** &gt; <strong>blackbox_exporter-</strong> &gt; <strong>pingレイテンシー</strong>にアクセスして、TiDBからPDリーダーへのネットワークが正常に実行されているかどうかを確認します。

    -   PDパニック。 [バグを報告](https://github.com/pingcap/pd/issues/new?labels=kind%2Fbug&#x26;template=bug-report.md) 。

    -   PDはOOMです。 [5.3](#53-pd-oom)を参照してください。

    -   問題に他の原因がある場合は、 `curl http://127.0.0.1:2379/debug/pprof/goroutine?debug=2`と[バグを報告](https://github.com/pingcap/pd/issues/new?labels=kind%2Fbug&#x26;template=bug-report.md)を実行してゴルーチンを取得します。

-   5.2.4その他の問題

    -   PDは`FATAL`エラーを報告し、ログは`range failed to find revision pair`を示します。この問題はv3.0.8（ [＃2040](https://github.com/pingcap/pd/pull/2040) ）で修正されています。詳しくは中国語[ケース-947](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case947.md)をご覧ください。

    -   その他の状況では、 [バグを報告](https://github.com/pingcap/pd/issues/new?labels=kind%2Fbug&#x26;template=bug-report.md) 。

### 5.3PDルーム {#5-3-pd-oom}

-   5.3.1 `/api/v1/regions`インターフェースを使用する場合、リージョンが多すぎるとPDOOMが発生する可能性があります。この問題はv3.0.8（ [＃1986](https://github.com/pingcap/pd/pull/1986) ）で修正されています。

-   5.3.2ローリングアップグレード中のPDOOM。 gRPCメッセージのサイズは制限されておらず、モニターはTCPInSegsが比較的大きいことを示しています。この問題はv3.0.6（ [＃1952](https://github.com/pingcap/pd/pull/1952) ）で修正されています。 <!--For details, see [case-852](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case852.md).-->

### 5.4Grafanaディスプレイ {#5-4-grafana-display}

-   **5.4.1Grafana-** &gt; <strong>PD-</strong> &gt;<strong>クラスタ</strong>-&gt;<strong>ロール</strong>のモニターにフォロワーが表示されます。 Grafana式の問題はv3.0.8で修正されています。

## 6.エコシステムツール {#6-ecosystem-tools}

### 6.1TiDBBinlog {#6-1-tidb-binlog}

-   6.1.1 TiDB Binlogは、TiDBから変更を収集し、ダウンストリームのTiDBまたはMySQLプラットフォームへのバックアップとレプリケーションを提供するツールです。詳細については、 [GitHubのBinlog](https://github.com/pingcap/tidb-binlog)を参照してください。

-   6.1.2Pump/Drainerステータスの`Update Time`は正常に更新され、ログに異常は表示されませんが、ダウンストリームにデータは書き込まれません。

    -   BinlogはTiDB構成で有効になっていません。 TiDBの`[binlog]`の構成を変更します。

-   Drainerの`sarama`は`EOF`エラーを報告します。

    -   DrainerのKafkaクライアントバージョンがKafkaのバージョンと矛盾しています。 `[syncer.to] kafka-version`の構成を変更する必要があります。

-   6.1.4 DrainerはKafkaへの書き込みに失敗してパニックになり、Kafkaは`Message was too large`のエラーを報告します。

    -   binlogデータが大きすぎるため、Kafkaに書き込まれる単一のメッセージが大きすぎます。 Kafkaの次の構成を変更する必要があります。

        ```conf
        message.max.bytes=1073741824
        replica.fetch.max.bytes=1073741824
        fetch.message.max.bytes=1073741824
        ```

        詳しくは中国語[ケース-789](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case789.md)をご覧ください。

-   6.1.5アップストリームとダウンストリームで一貫性のないデータ

    -   一部のTiDBノードはbinlogを有効にしません。 v3.0.6以降のバージョンでは、 [http://127.0.0.1:10080/info/all](http://127.0.0.1:10080/info/all)のインターフェースにアクセスすることで、すべてのノードのbinlogステータスを確認できます。 v3.0.6より前のバージョンの場合、構成ファイルを表示してbinlogステータスを確認できます。

    -   一部のTiDBノードは`ignore binlog`ステータスになります。 v3.0.6以降のバージョンでは、 [http://127.0.0.1:10080/info/all](http://127.0.0.1:10080/info/all)インターフェースにアクセスして、すべてのノードのbinlogステータスを確認できます。 v3.0.6より前のバージョンの場合は、TiDBログをチェックして、 `ignore binlog`キーワードが含まれているかどうかを確認してください。

    -   タイムスタンプ列の値は、アップストリームとダウンストリームで一貫していません。

        -   これは、異なるタイムゾーンが原因で発生します。 Drainerがアップストリームおよびダウンストリームデータベースと同じタイムゾーンにあることを確認する必要があります。 Drainerは`/etc/localtime`からタイムゾーンを取得し、 `TZ`環境変数をサポートしていません。中国語の[ケース-826](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case826.md)を参照してください。

        -   TiDBでは、タイムスタンプのデフォルト値は`null`ですが、 MySQL 5.7 （MySQL 8を含まない）の同じデフォルト値が現在の時刻です。したがって、アップストリームTiDBのタイムスタンプが`null`で、ダウンストリームがMySQL 5.7の場合、タイムスタンプ列のデータに一貫性がありません。 binlogを有効にする前に、アップストリームで`set @@global.explicit_defaults_for_timestamp=on;`を実行する必要があります。

    -   その他の状況では、 [バグを報告](https://github.com/pingcap/tidb-binlog/issues/new?labels=bug&#x26;template=bug-report.md) 。

-   6.1.6遅いレプリケーション

    -   ダウンストリームはTiDB/MySQLであり、アップストリームは頻繁にDDL操作を実行します。中国語の[ケース-1023](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case1023.md)を参照してください。

    -   ダウンストリームはTiDB/MySQLであり、複製されるテーブルには主キーと一意のインデックスがないため、binlogのパフォーマンスが低下します。主キーまたは一意のインデックスを追加することをお勧めします。

    -   ダウンストリームがファイルに出力する場合は、出力ディスクまたはネットワークディスクの速度が遅いかどうかを確認してください。

    -   その他の状況では、 [バグを報告](https://github.com/pingcap/tidb-binlog/issues/new?labels=bug&#x26;template=bug-report.md) 。

-   6.1.7Pumpはbinlogを書き込めず、 `no space left on device`エラーを報告します。

    -   ローカルディスク容量は、 Pumpがbinlogデータを正常に書き込むには不十分です。ディスクスペースをクリーンアップしてから、 Pumpを再起動する必要があります。

-   6.1.8Pumpは、起動時に`fail to notify all living drainer`のエラーを報告します。

    -   原因： Pumpが起動すると、 `online`状態にあるすべてのDrainerノードに通知します。 Drainerへの通知に失敗した場合、このエラーログが出力されます。

    -   解決策：binlogctlツールを使用して、各Drainerノードが正常かどうかを確認します。これは、 `online`状態のすべてのDrainerノードが正常に機能していることを確認するためです。 Drainerノードの状態が実際の動作ステータスと一致しない場合は、binlogctlツールを使用してその状態を変更してから、 Pumpを再起動します。ケース[通知に失敗するすべての生きている水切り](/tidb-binlog/handle-tidb-binlog-errors.md#fail-to-notify-all-living-drainer-is-returned-when-pump-is-started)を参照してください。

-   Drainerは`gen update sqls failed: table xxx: row data is corruption []`のエラーを報告します。

    -   トリガー：アップストリームは、 `DROP COLUMN`のDDLを実行しながら、このテーブルに対してDML操作を実行します。この問題はv3.0.6で修正されています。中国語の[ケース-820](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case820.md)を参照してください。

-   Drainerドレイナーレプリケーションがハングしています。プロセスはアクティブなままですが、チェックポイントは更新されません。

    -   この問題はv3.0.4で修正されています。中国語の[ケース-741](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case741.md)を参照してください。

-   6.1.11コンポーネントがパニックになります。

    -   [バグを報告](https://github.com/pingcap/tidb-binlog/issues/new?labels=bug&#x26;template=bug-report.md) 。

### 6.2データ移行 {#6-2-data-migration}

-   6.2.1 TiDBデータ移行（DM）は、MySQL/MariaDBからTiDBへのデータ移行をサポートする移行ツールです。詳細については、 [GitHubのDM](https://github.com/pingcap/dm/)を参照してください。

-   6.2.2 `Access denied for user 'root'@'172.31.43.27' (using password: YES)`は、 `query status`を実行するか、ログを確認するタイミングを示しています。

    -   すべてのDM構成ファイルのデータベース関連のパスワードは`dmctl`で暗号化する必要があります。データベースのパスワードが空の場合、パスワードを暗号化する必要はありません。 v1.0.6以降、クリアテキストのパスワードを使用できます。
    -   DM操作中、アップストリームおよびダウンストリームデータベースのユーザーは、対応する読み取りおよび書き込み権限を持っている必要があります。データ複製タスクの開始時に、データ移行も自動的に[対応する特権を事前にチェックします](/dm/dm-precheck.md)になります。
    -   異なるバージョンのDM-worker/DM-master / dmctlをDMクラスタにデプロイするには、中国語の[AskTUGのケーススタディ](https://asktug.com/t/dm1-0-0-ga-access-denied-for-user/1049/5)を参照してください。

-   6.2.3レプリケーションタスクが中断され、 `driver: bad connection`のエラーが返されます。

    -   `driver: bad connection`エラーは、DMとダウンストリームTiDBデータベース間の接続に異常（ネットワーク障害、TiDB再起動など）が発生し、現在の要求のデータがまだTiDBに送信されていないことを示します。

        -   DM 1.0.0 GAより前のバージョンの場合は、 `stop-task`を実行してタスクを停止し、 `start-task`を実行してタスクを再開します。
        -   DM 1.0.0 GA以降のバージョンでは、このタイプのエラーの自動再試行メカニズムが追加されています。 [＃265](https://github.com/pingcap/dm/pull/265)を参照してください。

-   6.2.4レプリケーションタスクは`invalid connection`エラーで中断されます。

    -   `invalid connection`エラーは、DMとダウンストリームTiDBデータベース間の接続に異常（ネットワーク障害、TiDB再起動、TiKVビジーなど）が発生し、現在の要求のデータの一部がに送信されたことを示します。 TiDB。 DMには、レプリケーションタスクでデータをダウンストリームに同時にレプリケートする機能があるため、タスクが中断されると、いくつかのエラーが発生する可能性があります。これらのエラーは、 `query-status`または`query-error`を実行することで確認できます。

        -   インクリメンタルレプリケーションプロセス中に`invalid connection`のエラーのみが発生した場合、DMはタスクを自動的に再試行します。
        -   バージョンの問題が原因でDMが再試行しないか、自動再試行に失敗する場合（v1.0.0-rc.1で自動再試行が導入されています）、 `stop-task`を使用してタスクを停止し、 `start-task`を使用してタスクを再開します。

-   6.2.5リレーユニットがエラー`event from * in * diff from passed-in event *`を報告するか、 `get binlog error ERROR 1236 (HY000) and binlog checksum mismatch, data may be corrupted returned`などのbinlogの取得または解析に失敗するエラーでレプリケーションタスクが中断されます

    -   DMがリレーログまたはインクリメンタルレプリケーションをプルするプロセス中に、アップストリームbinlogファイルのサイズが4 GBを超えると、この2つのエラーが発生する可能性があります。

    -   原因：リレー・ログを書き込む場合、DMはbinlog位置とbinlogファイル・サイズに基づいてイベント検証を実行し、複製されたbinlog位置をチェックポイントとして保管する必要があります。ただし、公式のMySQLはuint32を使用してbinlogの位置を格納します。つまり、4 GBを超えるbinlogファイルのbinlogの位置がオーバーフローすると、上記のエラーが発生します。

    -   解決：

        -   リレー処理装置の場合、 [レプリケーションを手動で回復する](https://pingcap.com/docs/tidb-data-migration/dev/error-handling/#the-relay-unit-throws-error-event-from--in--diff-from-passed-in-event--or-a-replication-task-is-interrupted-with-failing-to-get-or-parse-binlog-errors-like-get-binlog-error-error-1236-hy000-and-binlog-checksum-mismatch-data-may-be-corrupted-returned) 。
        -   binlogレプリケーション処理ユニットの場合、 [レプリケーションを手動で回復する](https://pingcap.com/docs/tidb-data-migration/dev/error-handling/#the-relay-unit-throws-error-event-from--in--diff-from-passed-in-event--or-a-replication-task-is-interrupted-with-failing-to-get-or-parse-binlog-errors-like-get-binlog-error-error-1236-hy000-and-binlog-checksum-mismatch-data-may-be-corrupted-returned) 。

-   6.2.6 DMレプリケーションが中断され、ログが`ERROR 1236 (HY000) The slave is connecting using CHANGE MASTER TO MASTER_AUTO_POSITION = 1, but the master has purged binary logs containing GTIDs that the slave requires.`を返します

    -   マスターbinlogがパージされているかどうかを確認します。
    -   `relay.meta`に記録されている位置情報を確認してください。

        -   `relay.meta`は空のGTID情報を記録しました。 DM-workerは、終了時または30秒ごとにGTID情報をメモリに`relay.meta`に保存します。 DM-workerがアップストリームGTID情報を取得しない場合、空のGTID情報を`relay.meta`に保存します。中国語の[ケース-772](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case772.md)を参照してください。

        -   `relay.meta`で記録されたbinlogイベントは、不完全な回復プロセスをトリガーし、間違ったGTID情報を記録します。この問題はv1.0.2で修正されており、以前のバージョンで発生する可能性があります。 <!--See [case-764](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case764.md).-->

-   6.2.7DMレプリケーションプロセスはエラー`Error 1366: incorrect utf8 value eda0bdedb29d(\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd)`を返します。

    -   この値はMySQL8.0またはTiDBに正常に書き込むことはできませんが、 MySQL 5.7に書き込むことはできます。 `tidb_skip_utf8_check`パラメータを有効にすると、データ形式のチェックをスキップできます。

### 6.3 TiDB Lightning {#6-3-tidb-lightning}

-   6.3.1 TiDB Lightningは、大量のデータをTiDBクラスタに高速に完全にインポートするためのツールです。 [GitHubのTiDB Lightning](https://github.com/pingcap/tidb-lightning)を参照してください。

-   6.3.2インポート速度が遅すぎます。

    -   `region-concurrency`の設定が高すぎると、スレッドの競合が発生し、パフォーマンスが低下します。トラブルシューティングする3つの方法：

        -   設定は、ログの先頭から`region-concurrency`を検索して見つけることができます。
        -   TiDB Lightningがサーバーを他のサービス（インポーターなど）と共有する場合は、そのサーバー上のCPUコアの総数の`region-concurrency` ％を手動で設定する必要があります。
        -   CPUにクォータがある場合（たとえば、Kubernetes設定によって制限されている場合）、 TiDB Lightningはこれを読み取れない可能性があります。この場合、 `region-concurrency`も手動で減らす必要があります。

    -   インデックスを追加するたびに、行ごとに新しいKVペアが導入されます。 N個のインデックスがある場合、インポートされる実際のサイズは、 [Mydumper](https://docs.pingcap.com/tidb/v4.0/mydumper-overview)の出力のサイズの約（N + 1）倍になります。インデックスが無視できる場合は、最初にスキーマからインデックスを削除し、インポートの完了後に`CREATE INDEX`を介してインデックスを追加し直すことができます。

    -   TiDB Lightningのバージョンは古いです。最新バージョンを試してください。インポート速度が向上する可能性があります。

-   `checksum failed: checksum mismatched remote vs local` 。

    -   原因1：テーブルにすでにデータが含まれている可能性があります。これらの古いデータは、最終チェックサムに影響を与える可能性があります。

    -   原因2：ターゲット・データベースのチェックサムが0の場合、つまり何もインポートされていない場合、クラスタが過熱してデータの取り込みに失敗している可能性があります。

    -   原因3：データソースがマシンによって生成され、 [Mydumper](https://docs.pingcap.com/tidb/v4.0/mydumper-overview)によってバックアップされていない場合は、テーブルの制約を尊重していることを確認してください。例えば：

        -   `AUTO_INCREMENT`列は正である必要があり、値「0」は含まれません。
        -   UNIQUEキーとPRIMARYKEYには、重複するエントリがあってはなりません。

    -   解決策： [トラブルシューティングソリューション](/tidb-lightning/tidb-lightning-faq.md#checksum-failed-checksum-mismatched-remote-vs-local)を参照してください。

-   6.3.4 `Checkpoint for … has invalid status:(error code)`

    -   原因：チェックポイントが有効になっていて、Lightning/Importerが以前に異常終了しました。偶発的なデータ破損を防ぐために、エラーが解決されるまでTiDB Lightningは起動しません。エラーコードは25未満の整数で、可能な値は`0, 3, 6, 9, 12, 14, 15, 17, 18, 20 and 21`です。整数は、インポートプロセスで予期しない終了が発生するステップを示します。整数が大きいほど、終了は遅くなります。

    -   解決策： [トラブルシューティングソリューション](/tidb-lightning/tidb-lightning-faq.md#checkpoint-for--has-invalid-status-error-code)を参照してください。

-   6.3.5 `ResourceTemporarilyUnavailable("Too many open engines …: 8")`

    -   原因：同時エンジンファイルの数が、tikv-importerで指定された制限を超えています。これは、設定ミスが原因である可能性があります。また、設定が正しい場合でも、以前にtidb-lightningが異常終了した場合は、エンジンファイルがダングリングオープン状態のままになることがあり、このエラーも発生する可能性があります。
    -   解決策： [トラブルシューティングソリューション](/tidb-lightning/tidb-lightning-faq.md#resourcetemporarilyunavailabletoo-many-open-engines--)を参照してください。

-   6.3.6 `cannot guess encoding for input file, please convert to UTF-8 manually`

    -   原因： TiDB Lightningは、UTF-8およびGB-18030エンコーディングのみをサポートします。このエラーは、ファイルがこれらのエンコーディングのいずれにも含まれていないことを意味します。また、過去のALTER TABLEの実行により、ファイルにUTF-8の文字列とGB-18030の別の文字列が含まれるなど、エンコードが混在している可能性もあります。

    -   解決策： [トラブルシューティングソリューション](/tidb-lightning/tidb-lightning-faq.md#cannot-guess-encoding-for-input-file-please-convert-to-utf-8-manually)を参照してください。

-   6.3.7 `[sql2kv] sql encode error = [types:1292]invalid time format: '{1970 1 1 0 45 0 0}'`

    -   原因：タイムスタンプタイプのエントリに、存在しない時間値があります。これは、DSTの変更、または時間値がサポートされている範囲（1970年1月1日から2038年1月19日まで）を超えたことが原因です。

    -   解決策： [トラブルシューティングソリューション](/tidb-lightning/tidb-lightning-faq.md#sql2kv-sql-encode-error--types1292invalid-time-format-1970-1-1-)を参照してください。

## 7.常用対数分析 {#7-common-log-analysis}

### 7.1 TiDB {#7-1-tidb}

-   `GC life time is shorter than transaction duration` 。

    トランザクション期間がGCの有効期間（デフォルトでは10分）を超えています。

    [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)のシステム変数を変更することにより、GCの寿命を延ばすことができます。通常、このパラメーターを変更することはお勧めしません。このパラメーターを変更すると、このトランザクションに`UPDATE`および`DELETE`ステートメントが多数ある場合、多くの古いバージョンが積み重なる可能性があるためです。

-   `txn takes too much time` 。

    このエラーは、長期間（590秒以上）コミットされていないトランザクションをコミットした場合に返されます。

    アプリケーションでこのような長時間のトランザクションを実行する必要がある場合は、この問題を回避するために`[tikv-client] max-txn-time-use = 590`パラメーターとGCライフタイムを増やすことができます。アプリケーションにこれほど長いトランザクション時間が必要かどうかを確認することをお勧めします。

-   `coprocessor.go`レポート`request outdated` 。

    このエラーは、TiKVに送信されたコプロセッサー要求がTiKVのキューで60秒以上待機した場合に返されます。

    TiKVコプロセッサーが長いキューにある理由を調査する必要があります。

-   7.1.4 `region_cache.go`は多数の`switch region peer to next due to send request fail`を報告し、エラーメッセージは`context deadline exceeded`です。

    TiKVの要求がタイムアウトになり、領域キャッシュがトリガーされて、要求が他のノードに切り替わります。ログの`addr`フィールドで`grep "<addr> cancelled`コマンドを引き続き実行し、 `grep`の結果に従って次の手順を実行できます。

    -   `send request is cancelled` ：送信フェーズ中にリクエストがタイムアウトしました。監視中の**Grafana-** &gt; <strong>TiDB-</strong> &gt; <strong>Batch Client</strong> / `Pending Request Count by TiKV`を調査し、保留中のリクエスト数が128を超えているかどうかを確認できます。

        -   値が128より大きい場合、送信はKVの処理能力を超えているため、送信は山積みになります。
        -   値が128以下の場合は、ログをチェックして、レポートが対応するKVの操作および保守の変更によって引き起こされているかどうかを確認します。それ以外の場合、このエラーは予期しないものであり、 [バグを報告](https://github.com/pingcap/tidb/issues/new?labels=type%2Fbug&#x26;template=bug-report.md)にする必要があります。

    -   `wait response is cancelled` ：リクエストはTiKVに送信された後にタイムアウトになりました。対応するTiKVアドレスの応答時間を確認する必要があり、その時点でリージョンはPDとKVにログインします。

-   `distsql.go`レポート`inconsistent index` 。

    データインデックスに一貫性がないようです。報告されたインデックスがあるテーブルで`admin check table <TableName>`コマンドを実行します。チェックに失敗した場合は、次のコマンドを実行してガベージコレクションを無効にします[バグを報告](https://github.com/pingcap/tidb/issues/new?labels=type%2Fbug&#x26;template=bug-report.md) ：

    ```sql
    SET GLOBAL tidb_gc_enable = 0;
    ```

### 7.2 TiKV {#7-2-tikv}

-   `key is locked` 。

    読み取りと書き込みに競合があります。読み取り要求は、コミットされていないデータを検出し、データがコミットされるまで待機する必要があります。

    このエラーの数が少ないとビジネスに影響はありませんが、このエラーの数が多い場合は、ビジネスで読み取りと書き込みの競合が深刻であることを示しています。

-   `write conflict` 。

    これは、楽観的なトランザクションにおける書き込みと書き込みの競合です。複数のトランザクションが同じキーを変更した場合、1つのトランザクションのみが成功し、他のトランザクションは自動的にタイムスタンプを再取得して操作を再試行しますが、ビジネスに影響はありません。

    競合が深刻な場合、複数回の再試行後にトランザクションが失敗する可能性があります。この場合、ペシミスティックロックを使用することをお勧めします。

-   `TxnLockNotFound` 。

    このトランザクションのコミットは遅すぎます。これは、TTL後に他のトランザクションによってロールバックされます（デフォルトでは、小さなトランザクションの場合は3秒）。このトランザクションは自動的に再試行されるため、通常、ビジネスに影響はありません。

-   `PessimisticLockNotFound` 。

    `TxnLockNotFound`に似ています。悲観的なトランザクションのコミットは遅すぎるため、他のトランザクションによってロールバックされます。

-   `stale_epoch` 。

    リクエストエポックは古くなっているため、ルーティングを更新した後、TiDBはリクエストを再送信します。事業への影響はありません。リージョンに分割/マージ操作があるか、レプリカが移行されると、エポックが変更されます。

-   `peer is not leader` 。

    リクエストは、リーダーではないレプリカに送信されます。エラー応答がどのレプリカが最新のリーダーであるかを示している場合、TiDBはエラーに従ってローカルルーティングを更新し、最新のリーダーに新しい要求を送信します。通常、ビジネスは影響を受けません。

    v3.0以降のバージョンでは、前のリーダーへの要求が失敗した場合、TiDBは他のピアを試行します。これにより、TiKVログで頻繁に`peer is not leader`が発生する可能性があります。 TiDBの対応するリージョンの`switch region peer to next due to send request fail`のログを確認して、送信の失敗の根本的な原因を特定できます。詳しくは[7.1.4](#71-tidb)をご覧ください。

    このエラーは、他の理由でリージョンにリーダーがいない場合にも返される可能性があります。詳細については、 [4.4](#44-some-tikv-nodes-drop-leader-frequently)を参照してください。
