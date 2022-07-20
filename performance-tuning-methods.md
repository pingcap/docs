---
title: Performance Analysis and Tuning
summary: Learn how to optimize database system based on database time and how to utilize the TiDB Performance Overview dashboard for performance analysis and tuning.
---

# パフォーマンス分析とチューニング {#performance-analysis-and-tuning}

このドキュメントでは、データベース時間ごとのチューニングアプローチについて説明し、パフォーマンス分析とチューニングに[パフォーマンス概要ダッシュボード](/grafana-performance-overview-dashboard.md)を使用する方法を示します。

このドキュメントで説明する方法を使用すると、ユーザーの応答時間とデータベース時間をグローバルおよびトップダウンの観点から分析して、ユーザーの応答時間のボトルネックがデータベースの問題に起因するかどうかを確認できます。ボトルネックがデータベースにある場合は、データベース時間の概要とSQLレイテンシの内訳を使用して、ボトルネックを特定し、パフォーマンスを調整できます。

## データベース時間に基づくパフォーマンス調整 {#performance-tuning-based-on-database-time}

TiDBは、SQL処理パスとデータベース時間を常に測定および収集しています。したがって、TiDBのデータベースパフォーマンスのボトルネックを簡単に特定できます。データベースの時間メトリックに基づいて、ユーザーの応答時間に関するデータがなくても、次の2つの目標を達成できます。

-   SQL処理の平均待機時間とトランザクション内のTiDB接続のアイドル時間とを比較して、ボトルネックがTiDBにあるかどうかを判断します。
-   ボトルネックがTiDBにある場合は、データベース時間の概要、色ベースのパフォーマンスデータ、主要なメトリック、リソース使用率、およびトップダウンの遅延の内訳に基づいて、分散システム内の正確なモジュールをさらに特定します。

### TiDBがボトルネックになっていますか？ {#is-tidb-the-bottleneck}

-   トランザクションでのTiDB接続の平均アイドル時間が平均SQL処理遅延よりも長い場合、データベースはアプリケーションのトランザクション遅延の責任を負いません。データベース時間はユーザーの応答時間のごく一部しかかかりません。これは、ボトルネックがデータベースの外部にあることを示しています。

    この場合、データベースの外部コンポーネントを確認してください。たとえば、アプリケーションサーバーに十分なハードウェアリソースがあるかどうか、およびアプリケーションからデータベースまでのネットワーク遅延が過度に高いかどうかを判断します。

-   SQL処理の平均待ち時間がトランザクション内のTiDB接続の平均アイドル時間よりも長い場合、トランザクションのボトルネックはTiDBにあり、データベース時間はユーザー応答時間の大部分を占めます。

### ボトルネックがTiDBにある場合、それを特定する方法は？ {#if-the-bottleneck-is-in-tidb-how-to-identify-it}

次の図は、一般的なSQLプロセスを示しています。ほとんどのSQL処理パスがTiDBパフォーマンスメトリックでカバーされていることがわかります。データベース時間はさまざまなディメンションに分割され、それに応じて色分けされます。ワークロードの特性をすばやく理解し、データベース内のボトルネックがあればそれを見つけることができます。

![database time decomposition chart](/media/performance/dashboard-diagnostics-time-relation.png)

データベース時間は、すべてのSQL処理時間の合計です。データベース時間を次の3つの次元に分類すると、TiDBのボトルネックをすばやく特定するのに役立ちます。

-   SQL処理タイプ別：どのタイプのSQLステートメントがデータベース時間を最も消費するかを判別します。式は次のとおりです。

    `DB Time = Select Time + Insert Time + Update Time + Delete Time + Commit Time + ...`

-   SQL処理の4つのステップ（get_token / parse / compile / execute）によって：どのステップが最も時間を消費するかを決定します。式は次のとおりです。

    `DB Time = Get Token Time + Parse Time + Compile Time + Execute Time`

-   エグゼキュータ時間、TSO待機時間、KV要求時間、および実行再試行時間によって：どの実行ステップがボトルネックを構成しているかを判別します。式は次のとおりです。

    `Execute Time ~= TiDB Executor Time + KV Request Time + PD TSO Wait Time + Retried execution time`

## パフォーマンス概要ダッシュボードを使用したパフォーマンス分析とチューニング {#performance-analysis-and-tuning-using-the-performance-overview-dashboard}

このセクションでは、Grafanaのパフォーマンス概要ダッシュボードを使用してデータベース時間に基づいてパフォーマンス分析とチューニングを実行する方法について説明します。

パフォーマンスの概要ダッシュボードは、TiDB、PD、およびTiKVのメトリックを調整し、次のセクションでそれぞれを示します。

-   データベース時間とSQL実行時間の概要：色分けされたSQLタイプ、SQL実行フェーズごとのデータベース時間、およびさまざまな要求のデータベース時間は、データベースのワークロード特性とパフォーマンスのボトルネックをすばやく特定するのに役立ちます。
-   主要なメトリックとリソース使用率：データベースQPS、接続情報、アプリケーションとデータベース間の要求コマンドタイプ、データベース内部TSOおよびKV要求OPS、およびTiDB/TiKVリソース使用量が含まれます。
-   トップダウンレイテンシの内訳：クエリレイテンシと接続アイドル時間の比較、クエリレイテンシの内訳、SQL実行でのTSOリクエストとKVリクエストのレイテンシ、TiKV内部書き込みレイテンシの内訳などが含まれます。

### データベース時間とSQL実行時間の概要 {#database-time-and-sql-execution-time-overview}

データベース時間メトリックは、TiDBが1秒あたりのSQLを処理する待ち時間の合計です。これは、TiDBが1秒あたりのアプリケーションSQL要求を同時に処理する合計時間でもあります（アクティブな接続の数に等しい）。

パフォーマンスの概要ダッシュボードには、次の3つのスタック領域グラフが表示されます。これらは、データベースのワークロードプロファイルを理解し、SQL実行中のステートメント、SQLフェーズ、およびTiKVまたはPD要求タイプの観点からボトルネックの原因をすばやく特定するのに役立ちます。

-   SQLタイプ別のデータベース時間
-   SQLフェーズごとのデータベース時間
-   SQL実行時間の概要

#### 色で調整 {#tune-by-color}

データベース時間の内訳と実行時間の概要の図は、予想される時間と予期しない時間の両方を直感的に示しています。したがって、パフォーマンスのボトルネックをすばやく特定し、ワークロードプロファイルを学習できます。緑と青の領域は、通常の時間の消費と要求を表しています。これらの2つの図で、緑以外または青以外の領域がかなりの割合を占めている場合、データベースの時間分布は不適切です。

-   SQLタイプ別のデータベース時間：

    -   青： `Select`ステートメント
    -   緑`Commit` `Update`およびその他の`Insert`ステートメント
    -   赤`StmtFetch` `StmtPrepare` 、および`StmtReset`を含む一般的なSQL `StmtClose`

-   SQLフェーズごとのデータベース時間：SQL実行フェーズは緑色で、その他のフェーズは一般的に赤色で表示されます。緑以外の領域が大きい場合は、実行フェーズ以外のフェーズで多くのデータベース時間が消費され、さらに原因分析が必要になることを意味します。一般的なシナリオは、準備されたプランキャッシュが利用できないため、オレンジ色で示されているコンパイルフェーズが大きな領域を占めることです。

-   SQL実行時間の概要：緑色のメトリックは一般的なKV書き込み要求（ `Prewrite`や`Commit`など）を表し、青色のメトリックは一般的なKV読み取り要求（CopやGetなど）を表し、他の色のメトリックは予期しない状況を表します。注意を払う。たとえば、ペシミスティックロックKV要求は赤でマークされ、TSO待機はダークブラウンでマークされます。青以外または緑以外の領域が大きい場合は、SQLの実行中にボトルネックがあることを意味します。例えば：

    -   深刻なロックの競合が発生した場合、赤い領域が大きな割合を占めます。
    -   TSOの待機に過度の時間がかかると、暗褐色の領域が大きな割合を占めます。

**例1：TPC-Cワークロード**

![TPC-C](/media/performance/tpcc_db_time.png)

-   SQLタイプ別のデータベース時間：最も時間のかかるステートメントは、 `commit` 、および`select` `insert` `update` 。
-   SQLフェーズごとのデータベース時間：最も時間のかかるフェーズは、緑色のSQL実行です。
-   SQL実行時間の概要：SQL実行で最も時間のかかるKV要求は、緑色の`Prewrite`と`Commit`です。

    > **ノート：**
    >
    > 通常、KV要求の合計時間は実行時間よりも長くなります。 TiDBエグゼキュータがKV要求を複数のTiKVに同時に送信する可能性があるため、KV要求の合計待機時間は実行時間より長くなります。前述のTPC-Cワークロードでは、トランザクションがコミットされると、TiDBは`Prewrite`つと`Commit`の要求を複数のTiKVに同時に送信します。したがって、この例の`Prewrite` 、および`Commit`リクエストの合計時間は、実行時間よりも明らかに長くなり`PessimisticsLock` 。
    >
    > -   `execute`回は、KVリクエストの合計時間に`tso_wait`回を加えた時間よりも大幅に長くなる場合もあります。これは、SQLの実行時間が主にTiDBエグゼキュータ内で費やされることを意味します。 2つの一般的な例を次に示します。

    ```
      > - Example 1: After TiDB executor reads a large amount of data from TiKV, it needs to do complex join and aggregation inside TiDB, which consumes a lot of time.
    ```

    ```
      > - Example 2: The application experiences serious write statement lock conflicts. Frequent lock retries result in long `Retried execution time`.
    ```

**例2：OLTPの読み取りが多いワークロード**

![OLTP](/media/performance/oltp_normal_db_time.png)

-   SQLタイプ別のデータベース時間：主な時間のかかるステートメントは`SELECT` 、および`UPDATE`であり、そのうち`INSERT` `COMMIT`がほとんどのデータベース時間を消費し`SELECT` 。
-   SQLフェーズごとのデータベース時間：ほとんどの時間は、緑色の`execute`フェーズで消費されます。
-   SQL実行時間の概要：SQL実行フェーズでは、 `pd tso_wait`はダークブラウン、 `KV Get`はブルー、 `Prewrite`と`Commit`はグリーンで時間がかかります。

**例3：読み取り専用のOLTPワークロード**

![OLTP](/media/performance/oltp_long_compile_db_time.png)

-   SQLタイプ別のデータベース時間：主に`SELECT`のステートメントです。
-   SQLフェーズごとのデータベース時間：時間のかかる主なフェーズは、オレンジ色の`compile`つと緑色の`execute`です。 `compile`フェーズの遅延が最も高く、TiDBが実行プランの生成に時間がかかりすぎていることを示しています。根本的な原因は、後続のパフォーマンスデータに基づいてさらに特定する必要があります。
-   SQL実行時間の概要：青色のKV BatchGetリクエストは、SQL実行中に最も多くの時間を消費します。

> **ノート：**
>
> 例3では、 `SELECT`のステートメントが複数のTiKVから数千行を同時に読み取る必要があります。したがって、 `BatchGet`の要求の合計時間は、実行時間よりもはるかに長くなります。

**例4：競合ワークロードをロックする**

![OLTP](/media/performance/oltp_lock_contention_db_time.png)

-   SQLタイプ別のデータベース時間：主に`UPDATE`のステートメントです。
-   SQLフェーズごとのデータベース時間：ほとんどの時間は、実行フェーズで緑色で消費されます。
-   SQL実行時間の概要：赤で示されているKV要求PessimisticLockは、SQL実行中に最も多くの時間を消費し、実行時間は明らかにKV要求の合計時間よりも長くなります。これは、書き込みステートメントでの深刻なロックの競合と、頻繁なロックの再試行によって`Retried execution time`が長くなることが原因です。現在、TiDBは`Retried execution time`を測定しません。

### TiDBの主要なメトリックとクラスタリソースの使用率 {#tidb-key-metrics-and-cluster-resource-utilization}

#### 1秒あたりのクエリ、1秒あたりのコマンド、およびPrepared-Plan-Cache {#query-per-second-command-per-second-and-prepared-plan-cache}

[パフォーマンスの概要]の次の3つのパネルを確認することで、アプリケーションのワークロードタイプ、アプリケーションがTiDBとどのように相互作用するか、およびアプリケーションがTiDB1を完全に利用しているかどうかを確認でき[準備された計画キャッシュ](/sql-prepared-plan-cache.md) 。

-   QPS：1秒あたりのクエリの略。アプリケーションによって実行されたSQLステートメントの数を示します。
-   タイプ別のCPS：1秒あたりのコマンドの略。コマンドは、MySQLプロトコル固有のコマンドを示します。クエリステートメントは、クエリコマンドまたはプリペアドステートメントのいずれかによってTiDBに送信できます。
-   プランキャッシュOPSを使用したクエリ：TiDBクラスタが1秒あたりに準備されたプランキャッシュにヒットしたカウント。準備されたプランキャッシュは、 `prepared statement`のコマンドのみをサポートします。準備されたプランキャッシュがTiDBで有効になっている場合、次の3つのシナリオが発生します。

    -   準備されたプランキャッシュがヒットしません：1秒あたりのプランキャッシュヒット数は0です。アプリケーションがクエリインターフェイスを使用しているか、StmtExecuteの実行ごとにStmtCloseコマンドを呼び出してキャッシュされたプランをクリーンアップします。
    -   準備されたすべてのプランキャッシュがヒットします。1秒あたりのヒット数は、1秒あたりのStmtExecuteコマンドの数と同じです。
    -   いくつかの準備されたプランキャッシュがヒットしました：1秒あたりのヒット数は、1秒あたりのStmtExecuteコマンドの数よりも少なくなっています。準備済みプランキャッシュには既知の制限があります。たとえば、サブクエリをサポートしていません。サブクエリを含むSQLステートメントは、準備済みプランキャッシュを利用できません。

**例1：TPC-Cワークロード**

TPC-Cワークロードは、主に`UPDATE` 、および`SELECT`ステートメント`INSERT` 。合計QPSは、1秒あたりのStmtExecuteの数に等しく、後者は、プランキャッシュOPSを使用したクエリにほぼ等しくなります。理想的には、クライアントはプリペアドステートメントのオブジェクトをキャッシュします。このように、SQLステートメントが実行されると、キャッシュされたステートメントが直接呼び出されます。すべてのSQL実行は準備されたプランキャッシュにヒットし、実行プランを生成するために再コンパイルする必要はありません。

![TPC-C](/media/performance/tpcc_qps.png)

**例2：読み取り専用OLTPワークロードでクエリコマンドに使用できない準備済みプランキャッシュ**

このワークロードでは、 `Commit QPS` = `Rollback QPS` = `Select QPS`です。アプリケーションは自動コミット同時実行を有効にしており、接続が接続プールからフェッチされるたびにロールバックが実行されます。その結果、これら3つのステートメントは同じ回数実行されます。

![OLTP-Query](/media/performance/oltp_long_compile_qps.png)

-   QPSパネルの赤い太線は失敗したクエリを表し、右側のY軸は失敗したクエリの数を示します。 0以外の値は、失敗したクエリが存在することを意味します。
-   合計QPSは、[CPS By Type]パネルのクエリ数と同じです。このクエリコマンドは、アプリケーションによって使用されています。
-   準備されたプランキャッシュはクエリコマンドで使用できないため、[プランキャッシュを使用したクエリOPS]パネルにはデータがありません。つまり、TiDBは、クエリを実行するたびに実行プランを解析して生成する必要があります。その結果、TiDBによるCPU消費量が増えると、コンパイル時間が長くなります。

**例3：OLTPワークロードに対してプリペアドステートメントが有効になっているため、プリペアドプランキャッシュを使用できません**

`StmtPreare`回= `StmtExecute`回= `StmtClose`回〜= `StmtFetch`回。アプリケーションは、準備&gt;実行&gt;フェッチ&gt;クローズループを使用します。プリペアドステートメントオブジェクトのリークを防ぐために、多くのアプリケーションフレームワークは`execute`フェーズの後に`close`を呼び出します。これにより、2つの問題が発生します。

-   SQLの実行には、4つのコマンドと4つのネットワークラウンドトリップが必要です。
-   プランキャッシュを使用したクエリOPSは0であり、準備されたプランキャッシュのヒットがゼロであることを示します。 `StmtClose`コマンドはデフォルトでキャッシュされた実行プランをクリアし、次の`StmtPreare`コマンドは実行プランを再度生成する必要があります。

> **ノート：**
>
> TiDB v6.0.0以降では、 `StmtClose`コマンドがグローバル変数（ `set global tidb_ignore_prepared_cache_close_stmt=on;` ）を介してキャッシュされた実行プランをクリアしないようにすることができます。このようにして、後続の実行は準備された計画キャッシュにヒットする可能性があります。

![OLTP-Prepared](/media/performance/oltp_prepared_statement_no_plan_cache.png)

#### KV/TSOリクエストOPSおよび接続情報 {#kv-tso-request-ops-and-connection-information}

KV / TSOリクエストOPSパネルでは、1秒あたりのKVおよびTSOリクエストの統計を表示できます。統計の中で、 `kv request total`はTiDBからTiKVへのすべてのリクエストの合計を表します。 TiDBからPDおよびTiKVへのリクエストのタイプを監視することで、クラスタ内のワークロードプロファイルを把握できます。

[接続数]パネルでは、接続の総数とTiDBごとの接続数を表示できます。カウントは、接続の総数が正常であり、TiDBごとの接続数が偶数であるかどうかを判断するのに役立ちます。 `active connections`は、アクティブな接続の数を記録します。これは、1秒あたりのデータベース時間に相当します。

**例1：ビジーなワークロード**

![TPC-C](/media/performance/tpcc_kv_conn.png)

このTPC-Cワークロードでは：

-   1秒あたりのKVリクエストの総数は104,200です。上位のリクエストタイプは、 `BatchGet`数の`Commit`に`PessimisticsLock` `Prewrite` 。
-   接続の総数は810で、3つのTiDBインスタンスに均等に分散されています。アクティブな接続の数は787.1です。したがって、接続の97％がアクティブであり、データベースがこのシステムのボトルネックであることを示しています。

**例2：アイドルワークロード**

![OLTP](/media/performance/cloud_long_idle_kv_conn.png)

このワークロードでは：

-   1秒あたりのKVリクエストの総数は2600で、1秒あたりのTSOリクエストの数は1100です。
-   接続の総数は410で、3つのTiDBインスタンスに均等に分散されています。アクティブな接続の数はわずか2.5であり、データベースシステムが比較的アイドル状態であることを示しています。

#### TiDB CPU、TiKV CPU、およびIOの使用 {#tidb-cpu-tikv-cpu-and-io-usage}

TiDBCPUおよびTiKVCPU/ IO MBpsパネルでは、TiDBおよびTiKVの論理CPU使用率とIOスループットを観察できます。これには、平均、最大、およびデルタ（最大CPU使用率から最小CPU使用率を引いたもの）が含まれ、これに基づいて決定できます。 TiDBとTiKVの全体的なCPU使用率。

-   `delta`の値に基づいて、TiDBのCPU使用率が不均衡であるか（通常は不均衡なアプリケーション接続を伴う）、クラスタ間に読み取り/書き込みホットスポットがあるかどうかを判断できます。
-   TiDBおよびTiKVリソースの使用状況の概要を使用すると、クラスタにリソースのボトルネックがあるかどうか、およびTiKVまたはTiDBのスケールアウトが必要かどうかをすばやく判断できます。

**例1：TiDBリソースの使用率が高い**

このワークロードでは、各TiDBおよびTiKVは8個のCPUで構成されています。

![TPC-C](/media/performance/tidb_high_cpu.png)

-   TiDBの平均、最大、およびデルタCPU使用率は、それぞれ575％、643％、および136％です。
-   TiKVの平均、最大、およびデルタCPU使用率は、それぞれ146％、215％、および118％です。 TiKVの平均、最大、およびデルタI / Oスループットは、それぞれ9.06 MB / s、19.7 MB / s、および17.1 MB/sです。

明らかに、TiDBはより多くのCPUを消費します。これは、8CPUのボトルネックしきい値に近い値です。 TiDBをスケールアウトすることをお勧めします。

**例2：TiKVリソースの使用率が高い**

以下のTPC-Cワークロードでは、各TiDBおよびTiKVは16個のCPUで構成されています。

![TPC-C](/media/performance/tpcc_cpu_io.png)

-   TiDBの平均、最大、およびデルタCPU使用率は、それぞれ883％、962％、および153％です。
-   TiKVの平均、最大、およびデルタCPU使用率は、それぞれ1288％、1360％、および126％です。 TiKVの平均、最大、およびデルタI / Oスループットは、それぞれ130 MB / s、153 MB / s、および53.7 MB/sです。

明らかに、TiKVはより多くのCPUを消費します。これは、TPC-Cが書き込みの多いシナリオであるために予想されます。パフォーマンスを向上させるために、TiKVをスケールアウトすることをお勧めします。

### レイテンシーの内訳と主要なレイテンシーメトリックを照会する {#query-latency-breakdown-and-key-latency-metrics}

レイテンシーパネルは、平均値と99パーセンタイルを提供します。平均値は全体的なボトルネックを特定するのに役立ち、99パーセンタイルまたは999パーセンタイルまたは999パーセンタイルは、重大な遅延ジッターがあるかどうかを判断するのに役立ちます。

#### 期間と接続アイドル期間 {#duration-and-connection-idle-duration}

[期間]パネルには、すべてのステートメントの平均レイテンシとP99レイテンシ、および各SQLタイプの平均レイテンシが含まれています。 [接続アイドル期間]パネルには、平均およびP99接続アイドル期間が含まれています。接続アイドル期間には、次の2つの状態が含まれます。

-   in-txn：接続がトランザクション内にある場合に、前のSQLを処理してから次のSQLステートメントを受信するまでの間隔。
-   not-in-txn：接続がトランザクション内にない場合に、前のSQLを処理してから次のSQLステートメントを受信するまでの間隔。

アプリケーションは、同じデータベース接続でトランザクションを実行します。平均クエリ遅延と接続アイドル期間を比較することで、TiDBがシステム全体のボトルネックであるかどうか、またはユーザーの応答時間のジッターがTiDBによって引き起こされているかどうかを判断できます。

-   アプリケーションのワークロードが読み取り専用ではなく、トランザクションが含まれている場合、平均クエリ待機時間を`avg-in-txn`と比較することで、データベース内外のトランザクション処理の割合を判断し、ユーザーの応答時間のボトルネックを特定できます。
-   アプリケーションのワークロードが読み取り専用であるか、自動コミットモードがオンになっている場合は、平均クエリ待機時間を`avg-not-in-txn`と比較できます。

実際の顧客のシナリオでは、ボトルネックがデータベースの外部にあることは珍しくありません。次に例を示します。

-   クライアントサーバー構成が低すぎて、CPUリソースが使い果たされています。
-   HAProxyはTiDBクラスタプロキシとして使用され、HAProxyCPUリソースが使い果たされています。
-   HAProxyはTiDBクラスタプロキシとして使用され、HAProxyサーバーのネットワーク帯域幅は高いワークロードの下で使い果たされます。
-   アプリケーションサーバーからデータベースへのネットワーク遅延は長いです。たとえば、パブリッククラウドの展開では、アプリケーションとTiDBクラスタが同じリージョンにないか、DNSワークロードバランサーとTiDBクラスタが同じリージョンにないため、ネットワーク遅延が高くなります。
-   ボトルネックはクライアントアプリケーションにあります。アプリケーションサーバーのCPUコアとNumaリソースを十分に活用することはできません。たとえば、TiDBへの数千のJDBC接続を確立するために使用されるJVMは1つだけです。

**例1：TiDBはユーザーの応答時間のボトルネックです**

![TiDB is the Bottleneck](/media/performance/tpcc_duration_idle.png)

このTPC-Cワークロードでは：

-   すべてのSQLステートメントの平均レイテンシーとP99レイテンシーは、それぞれ477usと3.13msです。 commitステートメント、insertステートメント、およびqueryステートメントの平均待機時間は、それぞれ2.02ミリ秒、609ミリ秒、および468usです。
-   トランザクション`avg-in-txn`の平均接続アイドル時間は171usです。

平均クエリレイテンシは`avg-in-txn`を大幅に上回っています。これは、トランザクションの主なボトルネックがデータベース内にあることを意味します。

**例2：ユーザーの応答時間のボトルネックはTiDBにありません**

![TiDB is the Bottleneck](/media/performance/cloud_query_long_idle.png)

このワークロードでは、平均クエリ遅延は1.69ミリ秒、 `avg-in-txn`は18ミリ秒です。これは、TiDBがトランザクションでSQLステートメントを処理するために平均1.69ミリ秒を費やし、次のステートメントを受信するために18ミリ秒待機する必要があることを示します。

平均クエリレイテンシは`avg-in-txn`よりも大幅に短くなっています。ユーザーの応答時間のボトルネックはTiDBにはありません。この例は、アプリケーションとデータベースが同じリージョンにないため、アプリケーションとデータベース間のネットワーク遅延が大きいと接続アイドル時間が非常に長くなるパブリッククラウド環境です。

#### 期間の解析、コンパイル、および実行 {#parse-compile-and-execute-duration}

TiDBには、クエリステートメントの送信から結果の返送まで[典型的な処理フロー](/sql-optimization-concepts.md)があります。

TiDBでのSQL処理は、 `get token` 、および`compile`の`parse`つのフェーズで構成されてい`execute` 。

-   `get token` ：通常は数マイクロ秒のみで、無視できます。トークンは、単一のTiDBインスタンスへの接続数が[トークン制限](/tidb-configuration-file.md)の制限に達した場合にのみ制限されます。
-   `parse` ：クエリステートメントは抽象構文木（AST）に解析されます。
-   `compile` ：実行計画は、 `parse`フェーズのASTと統計に基づいてコンパイルされます。 `compile`フェーズには、論理最適化と物理最適化が含まれます。論理最適化は、関係代数に基づく列の枝刈りなどのルールによってクエリプランを最適化します。物理最適化は、コストベースのオプティマイザによる統計によって実行プランのコストを見積もり、コストが最も低い物理実行プランを選択します。
-   `execute` ：SQLステートメントの実行にかかる時間。 TiDBは、最初にグローバルに一意のタイムスタンプTSOを待機します。次に、エグゼキュータは、実行プラン内のオペレータのキー範囲に基づいてTiKV APIリクエストを作成し、それをTiKVに配布します。 `execute`時間には、TSO待機時間、KV要求時間、およびTiDBエグゼキュータがデータの処理に費やした時間が含まれます。

アプリケーションが`query`つまたは`StmtExecute`のMySQLコマンドインターフェイスのみを使用する場合は、次の式を使用して、平均遅延のボトルネックを特定できます。

```
avg Query Duration = avg Get Token + avg Parse Duration + avg Compile Duration + avg Execute Duration
```

通常、 `execute`フェーズが`query`のレイテンシーの大部分を占めます。ただし、次の場合、 `parse`フェーズと`compile`フェーズも大きな役割を果たす可能性があります。

-   `parse`フェーズでの待ち時間が長い：たとえば、 `query`ステートメントが長い場合、SQLテキストを解析するために多くのCPUが消費されます。
-   `compile`フェーズでの長い遅延：準備されたプランキャッシュがヒットしない場合、TiDBはSQL実行ごとに実行プランをコンパイルする必要があります。 `compile`フェーズの遅延は、数ミリ秒または数十ミリ秒、あるいはそれ以上になる可能性があります。準備されたプランキャッシュがヒットしない場合、論理的および物理的な最適化は`compile`フェーズで実行されます。これは、多くのCPUとメモリを消費し、Go Runtime（TiDBは[`Go`](https://go.dev/)で書き込まれます）をプレッシャーの下で作成し、他のTiDBコンポーネントのパフォーマンスに影響を与えます。準備されたプランキャッシュは、TiDBでOLTPワークロードを効率的に処理するために重要です。

**例1： `compile`フェーズでのデータベースのボトルネック**

![Compile](/media/performance/long_compile.png)

前の図では、 `parse` 、および`compile`フェーズの平均時間はそれぞれ17.1 us、729 us、および`execute`です。アプリケーションは`query`コマンドインターフェイスを使用し、準備されたプランキャッシュを使用できないため、 `compile`レイテンシは高くなります。

**例2： `execute`フェーズでのデータベースのボトルネック**

![Execute](/media/performance/long_execute.png)

このTPC-Cワークロードでは、 `parse` 、および`compile`フェーズの平均時間はそれぞれ7.39 us、38.1 us、および`execute`です。 `execute`フェーズは、 `query`レイテンシのボトルネックです。

#### KVおよびTSOリクエスト期間 {#kv-and-tso-request-duration}

TiDBは、 `execute`フェーズでPDおよびTiKVと相互作用します。次の図に示すように、SQL要求を処理する場合、TiDBは`parse`フェーズと`compile`フェーズに入る前にTSOを要求します。 PDクライアントは呼び出し元をブロックしませんが、 `TSFuture`を返し、バックグラウンドでTSO要求を非同期的に送受信します。 PDクライアントがTSO要求の処理を終了すると、 `TSFuture`を返します。 `TSFuture`の所有者は、最終的なTSOを取得するためにWaitメソッドを呼び出す必要があります。 TiDBが`parse`フェーズと`compile`フェーズを終了すると、 `execute`フェーズに入り、次の2つの状況が発生する可能性があります。

-   TSO要求が完了すると、Waitメソッドはすぐに使用可能なTSOまたはエラーを返します
-   TSO要求がまだ完了していない場合、TSOが使用可能になるか、エラーが表示されるまで、Waitメソッドはブロックされます（gRPC要求は送信されましたが、結果は返されず、ネットワーク遅延は高くなります）。

TSO待機時間は`TSO WAIT`として記録され、TSO要求のネットワーク時間は`TSO RPC`として記録されます。 TSO待機が完了した後、TiDBエグゼキュータは通常、読み取りまたは書き込み要求をTiKVに送信します。

-   一般的なKV読み取り要求`Cop` `Get` 、および`BatchGet`
-   一般的なKV書き込み要求： `Commit`フェーズコミットの場合は`PessimisticLock` 、および`Prewrite`

![Execute](/media/performance/execute_phase.png)

このセクションのインジケーターは、次の3つのパネルに対応しています。

-   平均TiDBKVリクエスト期間：TiDBによって測定されたKVリクエストの平均レイテンシ
-   平均TiKVGRPC期間：TiKVでgPRCメッセージを処理する際の平均遅延
-   PDTSO待機/RPC期間：TiDBエグゼキュータTSO待機時間とTSO要求のネットワーク遅延（RPC）

`Avg TiDB KV Request Duration`と`Avg TiKV GRPC Duration`の関係は次のとおりです。

```
Avg TiDB KV Request Duration = Avg TiKV GRPC Duration + Network latency between TiDB and TiKV + TiKV gRPC processing time + TiDB gRPC processing time and scheduling latency
```

`Avg TiDB KV Request Duration`と`Avg TiKV GRPC Duration`の違いは、ネットワークトラフィック、ネットワーク遅延、およびTiDBとTiKVによるリソースの使用に密接に関連しています。

-   同じデータセンターの場合：差は通常2ミリ秒未満です。
-   同じ地域の異なるアベイラビリティーゾーンの場合：通常、差は5ミリ秒未満です。

**例1：同じデータセンターにデプロイされたクラスターのワークロードが少ない**

![Same Data Center](/media/performance/oltp_kv_tso.png)

このワークロードでは、TiDBの平均`Prewrite`レイテンシーは925 usであり、TiKV内の平均`kv_prewrite`処理レイテンシーは720usです。違いは約200usで、これは同じデータセンターでは正常です。 TSOの平均待機待ち時間は206usで、RPC時間は144usです。

**例2：パブリッククラウドクラスターの通常のワークロード**

![Cloud Env ](/media/performance/cloud_kv_tso.png)

この例では、TiDBクラスターは同じ地域の異なるデータセンターに展開されています。 TiDBの平均`commit`レイテンシは12.7ミリ秒で、TiKV内の平均`kv_commit`処理レイテンシは10.2ミリ秒で、約2.5ミリ秒の差があります。 TSOの平均待機待ち時間は3.12ミリ秒で、RPC時間は693usです。

**例3：パブリッククラウドクラスターでリソースが過負荷になっている**

![Cloud Env, TiDB Overloaded](/media/performance/cloud_kv_tso_overloaded.png)

この例では、TiDBクラスターが同じ地域の異なるデータセンターに展開されており、TiDBネットワークとCPUリソースが大幅に過負荷になっています。 TiDBの平均`BatchGet`レイテンシは38.6ミリ秒で、TiKV内の平均`kv_batch_get`処理レイテンシは6.15ミリ秒です。差は32ミリ秒を超えており、通常の値よりもはるかに大きくなっています。 TSOの平均待機待ち時間は9.45ミリ秒で、RPC時間は14.3ミリ秒です。

#### ストレージ非同期書き込み期間、保存期間、および適用期間 {#storage-async-write-duration-store-duration-and-apply-duration}

TiKVは、次の手順で書き込み要求を処理します。

-   `scheduler worker`は、書き込み要求を処理し、トランザクションの整合性チェックを実行し、書き込み要求をキーと値のペアに変換して`raftstore`モジュールに送信します。
-   TiKVコンセンサスモジュール`raftstore`は、 Raftコンセンサスアルゴリズムを適用して、ストレージレイヤー（複数のTiKVで構成される）をフォールトトレラントにします。

    Raftstoreは、 `Store`のスレッドと`Apply`のスレッドで構成されています。

    -   `Store`スレッドはRaftメッセージと新しい`proposals`を処理します。新しい`proposals`を受信すると、リーダーノードの`Store`スレッドがローカルのRaft DBに書き込み、メッセージを複数のフォロワーノードにコピーします。ほとんどの場合、この`proposals`が正常に永続化されると、 `proposals`は正常にコミットされます。
    -   `Apply`スレッドは、コミットされた`proposals`をKVDBに書き込みます。コンテンツがKVDBに正常に書き込まれると、 `Apply`スレッドは書き込み要求が完了したことを外部に通知します。

![TiKV Write](/media/performance/store_apply.png)

`Storage Async Write Duration`メトリックは、書き込み要求がraftstoreに入った後のレイテンシーを記録します。データは、リクエストごとに収集されます。

`Storage Async Write Duration`メトリックには、 `Store Duration`と`Apply Duration`の2つの部分が含まれます。次の式を使用して、書き込み要求のボトルネックが`Store`ステップか`Apply`ステップかを判断できます。

```
avg Storage Async Write Duration = avg Store Duration + avg Apply Duration
```

> **ノート：**
>
> `Store Duration`および`Apply Duration`は、v5.3.0以降でサポートされています。

**例1：v5.3.0とv5.4.0の同じOLTPワークロードの比較**

前の式によると、v5.4.0の書き込みが多いOLTPワークロードのQPSは、v5.3.0のQPSよりも14％高くなっています。

-   v5.3.0：24.4ミリ秒〜=17.7ミリ秒+6.59ミリ秒
-   v5.4.0：21.4ミリ秒〜=14.0ミリ秒+7.33ミリ秒

v5.4.0では、gPRCモジュールが最適化されてRaftログのレプリケーションが高速化され、v5.3.0と比較して`Store Duration`が削減されています。

v5.3.0：

![v5.3.0](/media/performance/v5.3.0_store_apply.png)

v5.4.0：

![v5.4.0](/media/performance/v5.4.0_store_apply.png)

**例2：保存期間がボトルネック**

前の式を適用します：10.1ミリ秒〜=9.81ミリ秒+0.304ミリ秒。この結果は、書き込み要求のレイテンシのボトルネックが`Store Duration`にあることを示しています。

![Store](/media/performance/cloud_store_apply.png)

#### ログ期間のコミット、ログ期間の追加、およびログ期間の適用 {#commit-log-duration-append-log-duration-and-apply-log-duration}

`Commit Log Duration` 、および`Append Log Duration`は、 `Apply Log Duration`内の主要な操作のレイテンシメトリックです。これらのレイテンシーはバッチ操作レベルでキャプチャされ、各操作は複数の書き込み要求を組み合わせます。したがって、レイテンシーは上記の`Store Duration`と`Apply Duration`に直接対応していません。

-   `Commit Log Duration`および`Append Log Duration`は、 `Store`スレッドで実行された操作の時間を記録します。 `Commit Log Duration`には、 Raftログを他のTiKVノードにコピーする時間が含まれます（raftログの永続性を確保するため）。 `Commit Log Duration`には通常、2つの`Append Log Duration`の操作が含まれ、1つはリーダー用、もう1つはフォロワー用です。前者にはネットワークを介してRaftログを他のTiKVノードにコピーする時間が含まれるため、 `Commit Log Duration`は通常`Append Log Duration`よりも大幅に高くなります。
-   `Apply Log Duration`は、 `Apply`スレッドによる`apply`のRaftログのレイテンシーを記録します。

`Commit Log Duration`が長い一般的なシナリオ：

-   TiKV CPUリソースにボトルネックがあり、スケジューリングの待ち時間が長い
-   `raftstore.store-pool-size`は小さすぎるか大きすぎる（値が大きすぎるとパフォーマンスが低下する可能性もあります）
-   I / Oレイテンシーが高く、 `Append Log Duration`レイテンシーが高くなります
-   TiKVノード間のネットワーク遅延が高い
-   gRPCスレッドの数が少なすぎるため、CPU使用率がGRPCスレッド間で不均一です。

`Apply Log Duration`が長い一般的なシナリオ：

-   TiKV CPUリソースにボトルネックがあり、スケジューリングの待ち時間が長い
-   `raftstore.apply-pool-size`は小さすぎるか大きすぎる（値が大きすぎるとパフォーマンスが低下する可能性もあります）
-   I/Oレイテンシーが高い

**例1：v5.3.0とv5.4.0の同じOLTPワークロードの比較**

v5.4.0の書き込みが多いOLTPワークロードのQPSは、v5.3.0のQPSと比較して14％向上しています。次の表では、3つの主要なレイテンシを比較しています。

| 平均期間     | v5.3.0（ms） | v5.4.0（ms） |
| :------- | :--------- | :--------- |
| ログ期間の追加  | 0.27       | 0.303      |
| コミットログ期間 | 13         | 8.68       |
| ログ期間の適用  | 0.457      | 0.514      |

v5.4.0では、gPRCモジュールが最適化されてRaftログのレプリケーションが高速化され、v5.3.0と比較して`Commit Log Duration`と`Store Duration`が削減されています。

v5.3.0：

![v5.3.0](/media/performance/v5.3.0_commit_append_apply.png)

v5.4.0：

![v5.4.0](/media/performance/v5.4.0_commit_append_apply.png)

**例2：コミットログの期間がボトルネック**

![Store](/media/performance/cloud_append_commit_apply.png)

-   平均`Append Log Duration` =4.38ミリ秒
-   平均`Commit Log Duration` =7.92ミリ秒
-   平均`Apply Log Duration` =172 us

`Store`スレッドの場合、 `Commit Log Duration`は明らかに`Apply Log Duration`よりも高くなります。一方、 `Append Log Duration`は`Apply Log Duration`よりも大幅に高く、 `Store`スレッドがCPUとI/Oの両方でボトルネックに悩まされている可能性があることを示しています。 `Commit Log Duration`と`Append Log Duration`を減らすための可能な方法は次のとおりです。

-   TiKV CPUリソースが十分な場合は、 `raftstore.store-pool-size`の値を増やして`Store`スレッドを追加することを検討してください。
-   TiDBがv5.4.0以降の場合は、 `raft-engine.enable: true`を設定して[`Raft Engine`](/tikv-configuration-file.md#raft-engine)を有効にすることを検討してください。 Raft Engineには軽い実行パスがあります。これにより、一部のシナリオでI/O書き込みと書き込みのロングテールレイテンシを削減できます。
-   TiKV CPUリソースが十分で、TiDBがv5.3.0以降の場合は、 `raftstore.store-io-pool-size: 1`を設定して[`StoreWriter`](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を有効にすることを検討してください。

## TiDBのバージョンがv6.1.0より前の場合、パフォーマンス概要ダッシュボードを使用するにはどうすればよいですか？ {#if-my-tidb-version-is-earlier-than-v6-1-0-what-should-i-do-to-use-the-performance-overview-dashboard}

v6.1.0以降、Grafanaにはデフォルトでパフォーマンス概要ダッシュボードが組み込まれています。このダッシュボードは、TiDBv4.xおよびv5.xバージョンと互換性があります。 TiDBがv6.1.0より前の場合は、次の図に示すように、手動で[`performance_overview.json`](https://github.com/pingcap/tidb/blob/master/metrics/grafana/performance_overview.json)をインポートする必要があります。

![Store](/media/performance/import_dashboard.png)
