---
title: Performance Analysis and Tuning
summary: データベース時間に基づいてデータベース システムを最適化する方法と、パフォーマンス分析およびチューニングに TiDB パフォーマンス概要ダッシュボードを活用する方法を学習します。
---

# パフォーマンス分析とチューニング {#performance-analysis-and-tuning}

このドキュメントでは、データベース時間によるチューニング方法について説明し、パフォーマンス分析とチューニングに TiDB [パフォーマンス概要ダッシュボード](/grafana-performance-overview-dashboard.md)使用する方法を示します。

このドキュメントで説明する手法を用いることで、ユーザー応答時間とデータベース時間をグローバルかつトップダウンの視点から分析し、ユーザー応答時間のボトルネックがデータベースの問題に起因するかどうかを確認できます。ボトルネックがデータベースにある場合は、データベース時間の概要とSQLレイテンシーの内訳を使用してボトルネックを特定し、パフォーマンスを調整できます。

## データベース時間に基づくパフォーマンスチューニング {#performance-tuning-based-on-database-time}

TiDBは、SQL処理パスとデータベース時間を継続的に測定・収集します。そのため、TiDBではデータベースパフォーマンスのボトルネックを容易に特定できます。データベース時間メトリクスに基づいて、ユーザー応答時間のデータがない場合でも、次の2つの目標を達成できます。

-   トランザクション内の平均 SQL 処理レイテンシーと TiDB 接続のアイドル時間を比較して、ボトルネックが TiDB にあるかどうかを判断します。
-   ボトルネックが TiDB にある場合は、データベース時間の概要、色ベースのパフォーマンス データ、主要なメトリック、リソース使用率、トップレイテンシーのレイテンシの内訳に基づいて、分散システム内の正確なモジュールをさらに特定します。

### TiDB がボトルネックですか? {#is-tidb-the-bottleneck}

-   トランザクションにおけるTiDB接続の平均アイドル時間が平均SQL処理レイテンシーよりも長い場合、アプリケーションのトランザクションレイテンシーの原因はデータベースではありません。データベース時間はユーザー応答時間のごく一部を占めるに過ぎないため、ボトルネックはデータベース外にあると考えられます。

    この場合、データベースの外部コンポーネントを確認してください。例えば、アプリケーションサーバーに十分なハードウェアリソースがあるかどうか、アプリケーションからデータベースへのネットワークレイテンシーが過度に高くないかなどを確認します。

-   平均 SQL 処理レイテンシーがトランザクション内の TiDB 接続の平均アイドル時間よりも長い場合、トランザクションのボトルネックは TiDB にあり、データベース時間がユーザー応答時間の大部分を占めます。

### ボトルネックが TiDB にある場合、それをどのように特定しますか? {#if-the-bottleneck-is-in-tidb-how-to-identify-it}

次の図は、典型的なSQLプロセスを示しています。ほとんどのSQL処理パスがTiDBパフォーマンスメトリックでカバーされていることがわかります。データベース時間は様々なディメンションに分割され、それぞれ色分けされています。これにより、ワークロード特性を迅速に把握し、データベース内のボトルネックがあればそれを特定できます。

![database time decomposition chart](/media/performance/dashboard-diagnostics-time-relation.png)

データベース時間は、すべてのSQL処理時間の合計です。データベース時間を以下の3つの側面に分解すると、TiDBのボトルネックを迅速に特定するのに役立ちます。

-   SQL処理の種類別：どの種類のSQL文が最もデータベース時間を消費しているかを特定します。計算式は次のとおりです。

    `DB Time = Select Time + Insert Time + Update Time + Delete Time + Commit Time + ...`

-   SQL処理の4つのステップ（get_token/parse/compile/execute）ごとに、どのステップが最も時間を消費しているかを判断します。計算式は以下のとおりです。

    `DB Time = Get Token Time + Parse Time + Compile Time + Execute Time`

-   実行時間、TSO待機時間、KVリクエスト時間、実行再試行時間に基づいて、ボトルネックとなっている実行ステップを特定します。計算式は以下のとおりです。

    `Execute Time ~= TiDB Executor Time + KV Request Time + PD TSO Wait Time + Retried execution time`

## パフォーマンス概要ダッシュボードを使用したパフォーマンス分析とチューニング {#performance-analysis-and-tuning-using-the-performance-overview-dashboard}

このセクションでは、Grafana のパフォーマンス概要ダッシュボードを使用して、データベース時間に基づいてパフォーマンス分析とチューニングを実行する方法について説明します。

パフォーマンス概要ダッシュボードは、TiDB、PD、および TiKV のメトリックを調整し、それぞれを次のセクションで表示します。

-   データベース時間と SQL 実行時間の概要: 色分けされた SQL タイプ、SQL 実行フェーズ別のデータベース時間、およびさまざまな要求のデータベース時間により、データベースのワークロード特性とパフォーマンスのボトルネックを迅速に特定できます。
-   主要なメトリックとリソース使用率: データベース QPS、接続情報、アプリケーションとデータベース間の要求コマンド タイプ、データベース内部 TSO および KV 要求 OPS、および TiDB/TiKV リソースの使用率が含まれます。
-   トップダウンのレイテンシーの内訳: クエリレイテンシーと接続アイドル時間の比較、クエリレイテンシーの内訳、SQL 実行における TSO 要求と KV 要求のレイテンシー、および TiKV 内部書き込みレイテンシーの内訳が含まれます。

### データベース時間とSQL実行時間の概要 {#database-time-and-sql-execution-time-overview}

データベース時間メトリックは、TiDB が 1 秒あたりに SQL を処理するレイテンシーの合計であり、これは TiDB が 1 秒あたりにアプリケーションの SQL 要求を同時に処理する合計時間でもあります (アクティブな接続の数に等しい)。

パフォーマンス概要ダッシュボードには、以下の3つの積み上げ面グラフが表示されます。これらのグラフは、データベースのワークロードプロファイルを把握し、SQL実行中のステートメント、SQLフェーズ、TiKVまたはPDリクエストタイプの観点からボトルネックの原因を迅速に特定するのに役立ちます。

-   SQLタイプ別のデータベース時間
-   SQLフェーズ別データベース時間
-   SQL実行時間の概要

#### 色で調整 {#tune-by-color}

データベース時間の内訳と実行時間の概要を示す図は、予想通りの時間消費と予想外の時間消費の両方を直感的に示します。そのため、パフォーマンスのボトルネックを迅速に特定し、ワークロードのプロファイルを把握できます。緑色と青色の領域は、通常の時間消費とリクエスト数を表します。これらの2つの図で、緑色または青色以外の領域が大きな割合を占めている場合、データベース時間の配分は不適切です。

-   SQL タイプ別のデータベース時間:

    -   青： `Select`ステートメント
    -   緑: `Update`および`Commit` `Insert` DMLステートメント
    -   赤: `StmtPrepare` `StmtReset`含む一般的`StmtClose` SQL `StmtFetch`

-   SQLフェーズ別データベース時間：SQL実行フェーズは緑色で、その他のフェーズは赤色で表示されます。緑色以外の領域が大きい場合は、実行フェーズ以外のフェーズでデータベース時間が大量に消費されていることを意味し、さらなる原因分析が必要です。よくあるシナリオとしては、準備済みのプランキャッシュが利用できないために、オレンジ色で表示されるコンパイルフェーズで大きな領域が消費されているケースが挙げられます。

-   SQL実行時間の概要：緑のメトリックは一般的なKV書き込みリクエスト（ `Prewrite`や`Commit`など）、青のメトリックは一般的なKV読み取りリクエスト（CopやGetなど）、紫のメトリックはTiFlash MPPリクエストを表します。その他の色のメトリックは、注意が必要な予期しない状況を表します。例えば、悲観的ロックKVリクエストは赤で、TSO待機は濃い茶色でマークされています。青や緑以外の領域が大きい場合、SQL実行中にボトルネックが発生していることを意味します。例：

    -   重大なロック競合が発生した場合、赤色の領域が大きな割合を占めることになります。
    -   TSO の待ち時間に過度に時間がかかってしまうと、濃い茶色の領域が大きな割合を占めることになります。

**例1: TPC-Cワークロード**

![TPC-C](/media/performance/tpcc_db_time.png)

-   SQL タイプ別のデータベース時間: 最も時間のかかるステートメントは、 `commit` 、 `update` 、 `select` 、および`insert`ステートメントです。
-   SQL フェーズ別のデータベース時間: 最も時間のかかるフェーズは緑色で表示される SQL 実行です。
-   SQL 実行時間の概要: SQL 実行で最も時間のかかる KV 要求は、緑色の`Prewrite`と`Commit`です。

    > **注記：**
    >
    > KVリクエストの合計時間が実行時間よりも長くなるのは正常です。これは、TiDBエグゼキューターが複数のTiKVに同時にKVリクエストを送信する可能性があるためです。その結果、KVリクエストの合計待機時間が実行時間よりも長くなります。前述のTPC-Cワークロードでは、トランザクションがコミットされる際に、TiDBは`Prewrite`つと`Commit`リクエストを複数のTiKVに同時に送信します。したがって、この例では、 `Prewrite` 、 `Commit` 、 `PessimisticLock`リクエストの合計時間は明らかに実行時間よりも長くなります。
    >
    > -   `execute`実行時間は、KVリクエストの合計時間と`tso_wait`目の実行時間の合計よりも大幅に長くなる可能性があります。これは、SQL実行時間のほとんどがTiDBエグゼキュータ内で費やされていることを意味します。以下に、よくある2つの例を示します。

          > - Example 1: After TiDB executor reads a large amount of data from TiKV, it needs to do complex join and aggregation inside TiDB, which consumes a lot of time.

    <!---->

          > - Example 2: The application experiences serious write statement lock conflicts. Frequent lock retries result in long `Retried execution time`.

**例2: OLTP読み取り中心のワークロード**

![OLTP](/media/performance/oltp_normal_db_time.png)

-   SQL タイプ別のデータベース時間: 時間のかかる主なステートメントは`SELECT` 、 `COMMIT` 、 `UPDATE` 、 `INSERT`で、その中で`SELECT`最も多くのデータベース時間を消費します。
-   SQL フェーズ別のデータベース時間: ほとんどの時間は緑色のフェーズ`execute`で消費されます。
-   SQL 実行時間の概要: SQL 実行フェーズでは、濃い茶色の`pd tso_wait` 、青色の`KV Get` 、緑色の`Prewrite`と`Commit`時間がかかっています。

**例3: 読み取り専用OLTPワークロード**

![OLTP](/media/performance/oltp_long_compile_db_time.png)

-   SQL タイプ別のデータベース時間: 主に`SELECT`ステートメントです。
-   SQLフェーズ別データベース時間：時間のかかる主なフェーズは、オレンジ色のフェーズ`compile`と緑色のフェーズ`execute`です。フェーズ`compile`のレイテンシが最も高く、TiDBが実行プランの生成に時間がかかりすぎていることを示しています。その後のパフォーマンスデータに基づいて根本原因をさらに特定する必要があります。
-   SQL 実行時間の概要: 青色の KV BatchGet 要求は、SQL 実行中に最も多くの時間を消費します。

> **注記：**
>
> 例3では、 `SELECT`ステートメントで複数のTiKVから数千行を同時に読み取る必要があります。そのため、 `BatchGet`リクエストの合計時間は実行時間よりもはるかに長くなります。

**例4: ロック競合ワークロード**

![OLTP](/media/performance/oltp_lock_contention_db_time.png)

-   SQL タイプ別のデータベース時間: 主に`UPDATE`ステートメントです。
-   SQL フェーズ別のデータベース時間: ほとんどの時間は緑色の実行フェーズで消費されます。
-   SQL実行時間の概要：赤で示されているKVリクエストPessimisticLockは、SQL実行中に最も多くの時間を消費しており、実行時間はKVリクエストの合計時間よりも明らかに長くなっています。これは、書き込みステートメントにおける深刻なロック競合と頻繁なロック再試行によって`Retried execution time`長くなっていることが原因です。現在、TiDBは`Retried execution time`測定していません。

**例5: HTAP CH-ベンチマークワークロード**

![HTAP](/media/performance/htap_tiflash_mpp.png)

-   SQL タイプ別のデータベース時間: 主に`SELECT`ステートメントです。
-   SQL フェーズ別のデータベース時間: ほとんどの時間は緑色の実行フェーズで消費されます。
-   SQL 実行時間の概要: 紫色で表示される`tiflash_mpp`のリクエストは、SQL 実行中に最も多くの時間を消費します。次に、青色の`Cop`のリクエストを含む KV リクエストと、緑色の`Prewrite`番目のリクエストと`Commit`リクエストが続きます。

### TiDB の主要メトリクスとクラスタ リソースの使用率 {#tidb-key-metrics-and-cluster-resource-utilization}

#### 1秒あたりのクエリ数、1秒あたりのコマンド数、準備済みプランキャッシュ {#query-per-second-command-per-second-and-prepared-plan-cache}

パフォーマンス概要の次の 3 つのパネルを確認することで、アプリケーションのワークロード タイプ、アプリケーションが TiDB と対話する方法、アプリケーションが TiDB [準備されたプランキャッシュ](/sql-prepared-plan-cache.md)最大限に活用しているかどうかを知ることができます。

-   QPS: Query Per Second（1秒あたりのクエリ数）の略。アプリケーションによって実行されたSQL文の数を示します。
-   CPSタイプ別：Command Per Secondの略。コマンドはMySQLプロトコル固有のコマンドを示します。クエリ文は、クエリコマンドまたはプリペアドステートメントのいずれかによってTiDBに送信できます。
-   プラン キャッシュ OPS を使用するクエリ: `avg-hit` 、TiDB クラスターで 1 秒あたりに実行プラン キャッシュを使用するクエリの数であり、 `avg-miss` 、TiDB クラスターで 1 秒あたりに実行プラン キャッシュを使用しないクエリの数です。

    `avg-hit + avg-miss`は`StmtExecute`に等しく、これは1秒あたりに実行される全クエリ数です。TiDBで準備済みプランキャッシュを有効にすると、以下の3つのシナリオが発生します。

    -   準備されたプランキャッシュにヒットしません。1（1秒あたりのヒット`avg-hit` ）は`avg-miss` 1秒あたりのコマンド数`StmtExecute`に相当します。考えられる理由は次のとおりです。
        -   アプリケーションはクエリ インターフェイスを使用しています。
        -   アプリケーションは`StmtExecute`実行ごとに`StmtClose`コマンドを呼び出すため、キャッシュされたプランはクリーンアップされます。
        -   `StmtExecute`によって実行されるすべてのステートメントは[キャッシュ条件](/sql-prepared-plan-cache.md)満たさないため、実行プラン キャッシュにヒットできません。
    -   準備されたすべてのプラン キャッシュがヒットします。1 (1 秒あたりのヒット数) `avg-hit` 1 秒あたり`StmtExecute`コマンドの数に等しく、 `avg-miss` (1 秒あたりのヒットがない数) は 0 です。
    -   準備済みプランキャッシュの一部がヒットしました。1（1秒あたりのヒット数） `avg-hit` 、1秒あたりのコマンド数`StmtExecute`より少ないです。準備済みプランキャッシュには既知の制限があります。例えば、サブクエリをサポートしていないため、サブクエリを含むSQL文では準備済みプランキャッシュを使用できません。

**例1: TPC-Cワークロード**

TPC-C ワークロードは主に`UPDATE` 、 `SELECT` 、 `INSERT`文です。合計 QPS は 1 秒あたり`StmtExecute`コマンドの数に等しく、後者は Queries Using Plan Cache OPS パネルでほぼ`avg-hit`に等しくなります。理想的には、クライアントはプリペアドステートメントのオブジェクトをキャッシュします。これにより、SQL ステートメントの実行時にキャッシュされたステートメントが直接呼び出されます。すべての SQL 実行は準備済みプランキャッシュにヒットするため、実行プランを生成するために再コンパイルする必要はありません。

![TPC-C](/media/performance/tpcc_qps.png)

**例 2: 準備されたプラン キャッシュは読み取り専用 OLTP ワークロードのクエリ コマンドには使用できません**

このワークロードでは、 `Commit QPS` = `Rollback QPS` = `Select QPS` 。アプリケーションは自動コミット同時実行を有効にしており、接続プールから接続がフェッチされるたびにロールバックが実行されます。その結果、これら3つの文は同じ回数実行されます。

![OLTP-Query](/media/performance/oltp_long_compile_qps.png)

-   QPSパネルの赤い太線は失敗したクエリを表し、右側のY軸は失敗したクエリの数を示しています。0以外の値は、失敗したクエリが存在することを意味します。
-   合計 QPS は、CPS By Type パネルのクエリの数と等しく、クエリ コマンドがアプリケーションによって使用されています。
-   プランキャッシュを使用するクエリOPSパネルにはデータが表示されません。これは、クエリコマンドで準備されたプランキャッシュが利用できないためです。つまり、TiDBはクエリ実行ごとに実行プランを解析して生成する必要があります。その結果、TiDBによるCPU消費量の増加に伴い、コンパイル時間が長くなります。

**例3: OLTPワークロードに対してプリペアドステートメントが有効になっている場合、準備済みプランキャッシュは利用できません**

`StmtPrepare`回 = `StmtExecute`回 = `StmtClose`回 ~= `StmtFetch`回。アプリケーションは準備 &gt; 実行 &gt; フェッチ &gt; クローズのループを使用します。プリペアドステートメントオブジェクトのリークを防ぐため、多くのアプリケーションフレームワークは`execute`フェーズの後に`close`呼び出します。これにより、2つの問題が発生します。

-   SQL 実行には 4 つのコマンドと 4 回のネットワーク ラウンドトリップが必要です。
-   プランキャッシュを使用するクエリのOPSは0で、準備されたプランキャッシュのヒットがゼロであることを示しています。1 `StmtClose`のコマンドはデフォルトでキャッシュされた実行プランをクリアし、次の`StmtPrepare`コマンドで実行プランを再度生成する必要があります。

> **注記：**
>
> TiDB v6.0.0以降では、グローバル変数（ `set global tidb_ignore_prepared_cache_close_stmt=on;` ）を介して、 `StmtClose`コマンドによるキャッシュされた実行プランのクリアを防止できます。これにより、後続の実行では準備されたプランキャッシュを利用できます。

![OLTP-Prepared](/media/performance/oltp_prepared_statement_no_plan_cache.png)

**例4: 準備されたステートメントにリソースリークがある**

1 秒あたり`StmtPrepare`コマンドの数は 1 秒あたり`StmtClose`コマンドの数よりはるかに多く、これはアプリケーションに準備されたステートメントのオブジェクト リークがあることを示しています。

![OLTP-Query](/media/performance/prepared_statement_leaking.png)

-   QPSパネルでは、赤い太線が失敗したクエリの数を示し、右側のY軸がその数値の座標値を示しています。この例では、1秒あたりの失敗したクエリの数は74.6です。
-   CPS By Type パネルでは、1 秒あたり`StmtPrepare`コマンドの数が 1 秒あたり`StmtClose`コマンドの数よりはるかに多く、準備されたステートメントのアプリケーションでオブジェクト リークが発生していることを示しています。
-   プラン キャッシュを使用したクエリ OPS パネルでは、 `avg-miss`タイプ別 CPS パネルの`StmtExecute`とほぼ等しく、ほとんどすべての SQL 実行で実行プラン キャッシュが失われていることを示しています。

#### KV/TSO 要求 OPS とソース別の KV 要求時間 {#kv-tso-request-ops-and-kv-request-time-by-source}

-   KV/TSOリクエストOPSパネルでは、1秒あたりのKVおよびTSOリクエストの統計情報を確認できます。統計情報のうち、 `kv request total` TiDBからTiKVへのすべてのリクエストの合計を表します。TiDBからPDおよびTiKVへのリクエストの種類を観察することで、クラスター内のワークロードプロファイルを把握できます。
-   KV リクエスト時間 (ソース別) パネルでは、各 KV リクエスト タイプとすべてのリクエスト ソースの時間比率を表示できます。
    -   kv 要求合計時間: 1 秒あたりの KV およびTiFlash要求の処理時間の合計。
    -   各 KV リクエストと対応するリクエスト ソースは積み上げ棒グラフを形成し、 `external`通常のビジネス リクエストを識別し、 `internal`内部アクティビティ リクエスト (DDL やauto analyzeリクエストなど) を識別します。

**例1: 忙しい作業負荷**

![TPC-C](/media/performance/tpcc_source_sql.png)

この TPC-C ワークロードでは、

-   1秒あたりのKVリクエストの総数は79,700です。リクエスト数の多い順に、リクエストタイプ`BatchGet` `Prewrite` `Commit` `PessimisticLock`
-   KV 処理時間のほとんどは`Commit-external_Commit`と`Prewrite-external_Commit`に費やされており、最も時間のかかる KV 要求は外部コミット ステートメントからの`Commit`と`Prewrite`あることがわかります。

**例2: ワークロードを分析する**

![OLTP](/media/performance/internal_stats.png)

このワークロードでは、クラスター内で実行されているステートメントは`ANALYZE`だけです。

-   1 秒あたりの KV リクエストの合計数は 35.5 で、1 秒あたりの Cop リクエストの数は 9.3 です。
-   KV 処理時間のほとんどは`Cop-internal_stats`に費やされており、最も時間のかかる KV 要求は内部`ANALYZE`操作のうちの`Cop`であることを示しています。

#### CPUとメモリの使用量 {#cpu-and-memory-usage}

TiDB、TiKV、PDのCPU/メモリパネルでは、平均CPU、最大CPU、デルタCPU（最大CPU使用率から最小CPU使用率を引いた値）、CPUクォータ、最大メモリ使用量など、それぞれの論理CPU使用率とメモリメモリ量を監視できます。これらの指標に基づいて、TiDB、TiKV、PDの全体的なリソース使用状況を把握できます。

-   `delta`値に基づいて、TiDB または TiKV の CPU 使用率が不均衡かどうかを判断できます。TiDB の場合、 `delta`高い場合、通常、TiDB インスタンス間のアプリケーション接続が不均衡であることを意味します。TiKV の場合、 `delta`が高い場合、通常、クラスター内に読み取り/書き込みのホットスポットがあることを意味します。
-   TiDB、TiKV、PD のリソース使用状況の概要を把握することで、クラスター内にリソースのボトルネックがあるかどうか、TiKV、TiDB、PD にスケールアウトまたはスケールアップが必要かどうかをすぐに判断できます。

**例1: TiKVリソースの使用率が高い**

次の TPC-C ワークロードでは、TiDB と TiKV はそれぞれ 16 個の CPU で構成されています。PD は 4 個の CPU で構成されています。

![TPC-C](/media/performance/tpcc_cpu_memory.png)

-   TiDBの平均、最大、差分CPU使用率はそれぞれ761%、934%、322%です。最大メモリ使用量は6.86GiBです。
-   TiKVの平均CPU使用率、最大CPU使用率、差分CPU使用率はそれぞれ1343%、1505%、283%です。最大メモリ使用量は27.1 GiBです。
-   PDの最大CPU使用率は59.1%です。最大メモリ使用量は221MiBです。

当然のことながら、TiKV は CPU を多く消費します。これは、TPC-C が書き込み中心のシナリオであるため、当然のことです。パフォーマンスを向上させるには、TiKV をスケールアウトすることをお勧めします。

#### データトラフィック {#data-traffic}

読み取りおよび書き込みトラフィック パネルでは、TiDB クラスター内のトラフィック パターンに関する分析情報が提供され、クライアントからデータベースへのデータ フローや内部コンポーネント間のデータ フローを包括的に監視できます。

-   トラフィックを読み取る

    -   `TiDB -> Client` : TiDBからクライアントへの送信トラフィック統計
    -   `Rocksdb -> TiKV` :storageレイヤー内での読み取り操作中に TiKV が RocksDB から取得するデータフロー

-   トラフィックを書き込む

    -   `Client -> TiDB` : クライアントから TiDB への受信トラフィック統計
    -   `TiDB -> TiKV: general` : フォアグラウンドトランザクションが TiDB から TiKV に書き込まれる速度
    -   `TiDB -> TiKV: internal` : 内部トランザクションが TiDB から TiKV に書き込まれる速度
    -   `TiKV -> Rocksdb` : TiKVからRocksDBへの書き込み操作の流れ
    -   `RocksDB Compaction` : RocksDBの圧縮操作によって生成される読み取りおよび書き込みI/Oフローの合計。2 `RocksDB Compaction` `TiKV -> Rocksdb`よりも大幅に大きく、平均行サイズが512バイトを超える場合は、min-blob-sizeを`"512B"`または`"1KB"`に設定し、blob-file-compressionを`"zstd"`に設定することで、Titanによる圧縮I/Oフローを削減できます。

        ```toml
        [rocksdb.titan]
        enabled = true
        [rocksdb.defaultcf.titan]
        min-blob-size = "1KB"
        blob-file-compression = "zstd"
        ```

**例1: TPC-Cワークロードの読み取りおよび書き込みトラフィック**

以下は、TPC-C ワークロードの読み取りおよび書き込みトラフィックの例です。

-   トラフィックを読み取る

    -   `TiDB -> Client` : 14.2 MB/秒
    -   `Rocksdb -> TiKV` : 469 MB/秒。読み取り操作（ `SELECT`ステートメント）と書き込み操作（ `INSERT` 、および`DELETE`ステートメント）の両方で`UPDATE`トランザクションをコミットする前にRocksDBからTiKVにデータを読み込む必要があることに注意してください。

-   トラフィックを書き込む

    -   `Client -> TiDB` : 5.05 MB/秒
    -   `TiDB -> TiKV: general` : 13.1 MB/秒
    -   `TiDB -> TiKV` : 内部: 5.07 KB/秒
    -   `TiKV -> Rocksdb` : 109 MB/秒
    -   `RocksDB Compaction` : 567 MB/秒

![TPC-C](/media/performance/tpcc_read_write_traffic.png)

**例2: Titanを有効にする前と後の書き込みトラフィック**

以下の例は、Titan を有効にする前後のパフォーマンスの変化を示しています。6KB のレコードの挿入ワークロードでは、Titan によって書き込みトラフィックとコンパクション I/O が大幅に削減され、TiKV の全体的なパフォーマンスとリソース使用率が向上します。

-   Titan を有効にする前にトラフィックを書き込む

    -   `Client -> TiDB` : 510 MB/秒
    -   `TiDB -> TiKV: general` : 187 MB/秒
    -   `TiDB -> TiKV: internal` : 3.2 KB/秒
    -   `TiKV -> Rocksdb` : 753 MB/秒
    -   `RocksDB Compaction` : 10.6 GB/秒

    ![Titan Disable](/media/performance/titan_disable.png)

-   Titan が有効になった後の書き込みトラフィック

    -   `Client -> TiDB` : 586 MB/秒
    -   `TiDB -> TiKV: general` : 295 MB/秒
    -   `TiDB -> TiKV: internal` : 3.66 KB/秒
    -   `TiKV -> Rocksdb` : 1.21 GB/秒
    -   `RocksDB Compaction` : 4.68 MB/秒

    ![Titan Enable](/media/performance/titan_enable.png)

### クエリレイテンシーの内訳と主要なレイテンシー指標 {#query-latency-breakdown-and-key-latency-metrics}

レイテンシーパネルには平均値と99パーセンタイルが表示されます。平均値は全体的なボトルネックの特定に役立ち、99パーセンタイル、999パーセンタイル、または999パーセンタイルは、レイテンシージッターの顕著な変化の有無を判断するのに役立ちます。

#### 期間、接続アイドル期間、接続数 {#duration-connection-idle-duration-and-connection-count}

「期間」パネルには、すべてのステートメントの平均レイテンシー、および各SQLタイプの平均レイテンシーが表示されます。「接続アイドル期間」パネルには、平均およびP99接続アイドル期間が表示されます。接続アイドル期間には、以下の2つの状態が含まれます。

-   in-txn: 接続がトランザクション内にある場合、前の SQL を処理してから次の SQL ステートメントを受信するまでの間隔。
-   not-in-txn: 接続がトランザクション内にない場合に、前の SQL を処理してから次の SQL ステートメントを受信するまでの間隔。

アプリケーションは同じデータベース接続でトランザクションを実行します。平均クエリレイテンシーと接続アイドル時間を比較することで、TiDBがシステム全体のボトルネックになっているのか、それともユーザー応答時間のジッターがTiDBによって引き起こされているのかを判断できます。

-   アプリケーション ワークロードが読み取り専用ではなく、トランザクションが含まれている場合は、平均クエリレイテンシーを`avg-in-txn`と比較することで、データベースの内部と外部でのトランザクション処理の割合を判別し、ユーザー応答時間のボトルネックを特定できます。
-   アプリケーションのワークロードが読み取り専用であるか、自動コミット モードがオンの場合は、平均クエリレイテンシーを`avg-not-in-txn`と比較できます。

実際の顧客シナリオでは、ボトルネックがデータベースの外部にあることは珍しくありません。次に例を示します。

-   クライアントサーバーの構成が低すぎるため、CPU リソースが使い果たされています。
-   HAProxy は TiDB クラスター プロキシとして使用され、HAProxy CPU リソースが使い果たされています。
-   HAProxy は TiDB クラスター プロキシとして使用され、高ワークロードでは HAProxyサーバーのネットワーク帯域幅が消費されます。
-   アプリケーションサーバーからデータベースへのネットワークレイテンシーが高い。例えば、パブリッククラウド環境では、アプリケーションとTiDBクラスタが同じリージョンに存在しない、またはDNSワークロードバランサとTiDBクラスタが同じリージョンに存在しない場合、ネットワークレイテンシーが高くなります。
-   ボトルネックとなっているのはクライアントアプリケーションです。アプリケーションサーバーのCPUコアとNumaリソースを最大限に活用できていません。例えば、TiDBへの数千ものJDBC接続を確立するのに、たった1つのJVMしか使用されていません。

「接続数」パネルでは、総接続数と各TiDBノードの接続数を確認できます。これにより、総接続数が正常かどうか、また各TiDBノードの接続数が不均衡かどうかを確認できます。1 `active connections`アクティブな接続数を示し、これは1秒あたりのデータベース時間に相当します。右側のY軸（ `disconnection/s` ）は、クラスター内の1秒あたりの切断数を示しており、アプリケーションが短い接続を使用しているかどうかを判断するのに役立ちます。

**例1: 切断回数が多すぎる**

![high disconnection/s](/media/performance/high_disconnections.png)

このワークロードでは、次のようになります。

-   すべての SQL ステートメントの平均レイテンシーと P99レイテンシーは、それぞれ 10.8 ミリ秒と 84.1 ミリ秒です。
-   トランザクション`avg-in-txn`の平均接続アイドル時間は 9.4 ミリ秒です。
-   クラスタへの総接続数は3,700で、各TiDBノードへの接続数は1,800です。アクティブ接続の平均数は40.3で、ほとんどの接続がアイドル状態であることを示しています。1 `disconnection/s`平均数は55.8で、アプリケーションが頻繁に接続と切断を繰り返していることを示しています。短い接続の動作は、TiDBのリソースと応答時間に一定の影響を与えます。

**例2: TiDBがユーザー応答時間のボトルネックとなっている**

![TiDB is the Bottleneck](/media/performance/tpcc_duration_idle.png)

この TPC-C ワークロードでは、

-   すべてのSQL文の平均レイテンシーとP99レイテンシーはそれぞれ477マイクロ秒と3.13ミリ秒です。コミット文、挿入文、クエリ文の平均レイテンシはそれぞれ2.02ミリ秒、609マイクロ秒、468マイクロ秒です。
-   トランザクション`avg-in-txn`の平均接続アイドル時間は 171 マイクロ秒です。

平均クエリレイテンシーは`avg-in-txn`よりも大幅に大きいため、トランザクションの主なボトルネックはデータベース内にあることを意味します。

**例3: TiDBはユーザー応答時間のボトルネックではない**

![TiDB is not Bottleneck](/media/performance/cloud_query_long_idle.png)

このワークロードでは、平均クエリレイテンシーは 1.69 ミリ秒、 `avg-in-txn` 18 ミリ秒です。これは、TiDB がトランザクション内の SQL ステートメントを処理するために平均 1.69 ミリ秒を費やし、その後、次のステートメントを受信するために 18 ミリ秒待機する必要があることを示しています。

平均クエリレイテンシーは`avg-in-txn`を大幅に下回っています。ユーザー応答時間のボトルネックはTiDBではありません。この例はパブリッククラウド環境におけるもので、アプリケーションとデータベースが同じリージョンにないため、アプリケーションとデータベース間のネットワークレイテンシーが高く、接続アイドル時間が非常に長くなります。

#### 解析、コンパイル、実行時間 {#parse-compile-and-execute-duration}

TiDB では、クエリ ステートメントの送信から結果の返送までに[典型的な処理フロー](/sql-optimization-concepts.md)かかります。

TiDB での SQL 処理は、 `get token` 、 `parse` 、 `compile` 、 `execute` 4 つのフェーズで構成されます。

-   `get token` : 通常は数マイクロ秒程度で無視できます。トークンは、単一のTiDBインスタンスへの接続数が[トークン制限](/tidb-configuration-file.md)上限に達した場合にのみ制限されます。
-   `parse` : クエリ ステートメントは抽象構文ツリー (AST) に解析されます。
-   `compile` : 実行計画は、第`parse`フェーズのASTと統計情報に基づいて作成されます。第`compile`フェーズには、論理最適化と物理最適化が含まれます。論理最適化では、リレーショナル代数に基づく列プルーニングなどのルールに従ってクエリプランを最適化します。物理最適化では、コストベースオプティマイザによって統計情報に基づいて実行計画のコストを推定し、最もコストが低い物理実行計画を選択します。
-   `execute` : SQL文の実行にかかる時間。TiDBはまず、グローバルに一意なタイムスタンプTSOを待機します。 `execute` 、エグゼキュータは実行プラン内のオペレータのキー範囲に基づいてTiKV APIリクエストを構築し、TiKVに配布します。2時間には、TSOの待機時間、KVリクエスト時間、およびTiDBエグゼキュータによるデータ処理時間が含まれます。

アプリケーションが`query`または`StmtExecute` MySQL コマンド インターフェイスのみを使用する場合は、次の式を使用して平均レイテンシーのボトルネックを特定できます。

    avg Query Duration = avg Get Token + avg Parse Duration + avg Compile Duration + avg Execute Duration

通常、 `query`レイテンシーのうち、第`execute`フェーズが大部分を占めます。ただし、以下の場合には、第`parse`フェーズと`compile`フェーズも大きな割合を占めることがあります。

-   フェーズ`parse`での長いレイテンシー: たとえば、ステートメント`query`が長い場合、SQL テキストを解析するために多くの CPU が消費されます。
-   第`compile`フェーズでの長いレイテンシー：準備されたプランキャッシュにヒットしない場合、TiDBはSQL実行ごとに実行プランをコンパイルする必要があります。第`compile`フェーズのレイテンシーは数ミリ秒から数十ミリ秒、あるいはそれ以上になる場合があります。準備されたプランキャッシュにヒットしない場合、第`compile`フェーズで論理的および物理的な最適化が行われ、CPUとメモリを大量に消費し、Goランタイム（TiDBは[`Go`](https://go.dev/)で記述されています）に負担がかかり、他のTiDBコンポーネントのパフォーマンスに影響を与えます。準備されたプランキャッシュは、TiDBにおけるOLTPワークロードの効率的な処理に重要です。

**例1: `compile`フェーズにおけるデータベースのボトルネック**

![Compile](/media/performance/long_compile.png)

上の図では、 `execute` `parse`の平均時間はそれぞれ 17.1 `compile`秒、729 マイクロ秒、681 マイクロ秒です。フェーズ`compile`レイテンシーが高いのは、アプリケーションが`query`コマンドインターフェースを使用しており、準備済みプランキャッシュを使用できないためです。

**例2: `execute`フェーズにおけるデータベースのボトルネック**

![Execute](/media/performance/long_execute.png)

このTPC-Cワークロードでは、 `parse` 、 `compile` 、第`execute`フェーズの平均時間はそれぞれ7.39マイクロ秒、38.1マイクロ秒、12.8ミリ秒です。第`execute`フェーズが第`query`レイテンシーのレイテンシのボトルネックとなっています。

#### KVおよびTSOリクエスト期間 {#kv-and-tso-request-duration}

TiDB はフェーズ`execute`で PD および TiKV と連携します。次の図に示すように、SQL 要求を処理する際、TiDB はフェーズ`parse`および`compile`入る前に TSO を要求します。PD クライアントは呼び出し元をブロックせず、 `TSFuture`を返し、バックグラウンドで非同期的に TSO 要求を送受信します。PD クライアントは TSO 要求の処理を完了すると、 `TSFuture`返します。 `TSFuture`の所有者は、最後の TSO を取得するために Wait メソッドを呼び出す必要があります。TiDB はフェーズ`parse`および`compile`を完了するとフェーズ`execute`に入り、このフェーズでは次の 2 つの状況が発生する可能性があります。

-   TSO要求が完了した場合、Waitメソッドは利用可能なTSOまたはエラーを直ちに返します。
-   TSO 要求がまだ完了していない場合、TSO が利用可能になるかエラーが表示されるまで (gRPC 要求は送信されたが結果が返されず、ネットワークレイテンシーが高くなる)、Wait メソッドはブロックされます。

TSO待機時間は`TSO WAIT`と記録され、TSO要求のネットワーク時間は`TSO RPC`と記録されます。TSO待機が完了すると、TiDBエグゼキューターは通常、TiKVに読み取りまたは書き込み要求を送信します。

-   一般的な KV 読み取り要求: `Get` `BatchGet`および`Cop`
-   一般的`Commit` KV書き込み要求: 2フェーズコミット`Prewrite`場合は`PessimisticLock`

![Execute](/media/performance/execute_phase.png)

このセクションのインジケーターは、次の 3 つのパネルに対応しています。

-   平均 TiDB KV リクエスト期間: TiDB によって測定された KV リクエストの平均レイテンシー
-   平均 TiKV GRPC 期間: TiKV での gPRC メッセージの処理にかかる平均レイテンシー
-   PD TSO 待機/RPC 期間: TiDB エグゼキュータの TSO 待機時間と TSO 要求 (RPC) のネットワークレイテンシー

`Avg TiDB KV Request Duration`と`Avg TiKV GRPC Duration`の関係は以下のとおりです。

    Avg TiDB KV Request Duration = Avg TiKV GRPC Duration + Network latency between TiDB and TiKV + TiKV gRPC processing time + TiDB gRPC processing time and scheduling latency

`Avg TiDB KV Request Duration`と`Avg TiKV GRPC Duration`の違いは、ネットワーク トラフィック、ネットワークレイテンシー、および TiDB と TiKV によるリソース使用量に密接に関係しています。

-   同じデータセンター内: 差は通常 2 ミリ秒未満です。
-   同じリージョン内の異なるアベイラビリティゾーンの場合: 差は通常 5 ミリ秒未満です。

**例1: 同じデータセンターに展開されたクラスタのワークロードが低い**

![Same Data Center](/media/performance/oltp_kv_tso.png)

このワークロードでは、TiDBの平均`Prewrite`レイテンシーは925マイクロ秒、TiKV内の平均`kv_prewrite`処理レイテンシーは720マイクロ秒でした。この差は約200マイクロ秒で、これは同じデータセンターでは一般的な値です。TSOの平均待機レイテンシーは206マイクロ秒、RPC時間は144マイクロ秒でした。

**例2: パブリッククラウドクラスタ上の通常のワークロード**

![Cloud Env ](/media/performance/cloud_kv_tso.png)

この例では、TiDBクラスタは同じリージョン内の異なるデータセンターにデプロイされています。TiDBの平均`commit`レイテンシーは12.7ミリ秒、TiKV内の平均`kv_commit`処理レイテンシーは10.2ミリ秒で、約2.5ミリ秒の差があります。平均TSO待機レイテンシーは3.12ミリ秒、RPC時間は693マイクロ秒です。

**例3: パブリッククラウドクラスタのリソース過負荷**

![Cloud Env, TiDB Overloaded](/media/performance/cloud_kv_tso_overloaded.png)

この例では、TiDBクラスタは同一リージョン内の異なるデータセンターに展開されており、TiDBネットワークとCPUリソースが深刻な過負荷状態にあります。TiDBの平均`BatchGet`レイテンシーは38.6ms、TiKV内部の平均`kv_batch_get`処理レイテンシーは6.15msです。その差は32ms以上で、正常値を大幅に上回っています。平均TSO待機レイテンシーは9.45ms、RPC時間は14.3msです。

#### ストレージ非同期書き込み期間、保存期間、適用期間 {#storage-async-write-duration-store-duration-and-apply-duration}

TiKV は次の手順で書き込み要求を処理します。

-   `scheduler worker`書き込み要求を処理し、トランザクションの一貫性チェックを実行し、書き込み要求を`raftstore`モジュールに送信するキーと値のペアに変換します。
-   TiKV コンセンサス モジュール`raftstore` 、 Raftコンセンサス アルゴリズムを適用して、storageレイヤー(複数の TiKV で構成) をフォールト トレラントにします。

    Raftstore は`Store`スレッドと`Apply`スレッドで構成されています。

    -   `Store`スレッドはRaftメッセージと新しい`proposals`処理します。新しい`proposals`受信すると、リーダーノードの`Store`スレッドはローカルRaft DBに書き込み、メッセージを複数のフォロワーノードにコピーします。ほとんどの場合、この`proposals`正常に永続化されると、 `proposals`が正常にコミットされます。
    -   `Apply`番目のスレッドはコミットされた`proposals`データをKV DBに書き込みます。データがKV DBに正常に書き込まれると、 `Apply`番目のスレッドは書き込み要求が完了したことを外部に通知します。

![TiKV Write](/media/performance/store_apply.png)

`Storage Async Write Duration`のメトリックは、書き込みリクエストがraftstoreに入った後のレイテンシーを記録します。データはリクエストごとに収集されます。

`Storage Async Write Duration`メトリックは`Store Duration`と`Apply Duration` 2 つの部分で構成されます。次の式を使用して、書き込みリクエストのボトルネックが`Store`または`Apply`どちらのステップにあるかを判断できます。

    avg Storage Async Write Duration = avg Store Duration + avg Apply Duration

> **注記：**
>
> `Store Duration`と`Apply Duration` v5.3.0 以降でサポートされています。

**例1: v5.3.0とv5.4.0での同じOLTPワークロードの比較**

前述の式によると、書き込みが多い OLTP ワークロードの QPS は、v5.4.0 では v5.3.0 よりも 14% 高くなります。

-   v5.3.0: 24.4 ミリ秒 ~= 17.7 ミリ秒 + 6.59 ミリ秒
-   v5.4.0: 21.4 ミリ秒 ~= 14.0 ミリ秒 + 7.33 ミリ秒

v5.4.0 では、gPRC モジュールが最適化され、 Raftログのレプリケーションが高速化され、v5.3.0 と比較して`Store Duration`削減されました。

バージョン5.3.0:

![v5.3.0](/media/performance/v5.3.0_store_apply.png)

バージョン5.4.0:

![v5.4.0](/media/performance/v5.4.0_store_apply.png)

**例2: 保存期間がボトルネック**

上記の式を適用します：10.1 ms ~= 9.81 ms + 0.304 ms。この結果は、書き込み要求のレイテンシーのボトルネックが`Store Duration`にあることを示しています。

![Store](/media/performance/cloud_store_apply.png)

#### コミットログ期間、追加ログ期間、適用ログ期間 {#commit-log-duration-append-log-duration-and-apply-log-duration}

`Commit Log Duration` `Apply Log Duration` 、raftstore内の主要な操作のレイテンシー指標です。これらのレイテンシはバッチ操作レベルで計測され、各操作は複数の書き込みリクエストを組み合わせます。したがって、これら`Append Log Duration`レイテンシは前述の`Store Duration`と`Apply Duration`に直接対応するものではありません。

-   `Commit Log Duration`と`Append Log Duration` 、 `Store`スレッドで実行された操作時間を記録します。6 `Commit Log Duration`は、 Raftログを他の TiKV ノードにコピーする時間が含まれます (raft-log の永続性を確保するため)。8 `Commit Log Duration`は通常、リーダー用とフォロワー用の 2 つの`Append Log Duration`操作が含まれます。12 は、通常、 `Append Log Duration`よりも大幅に大きくなります。 `Commit Log Duration` 、前者には、ネットワークを介してRaftログを他の TiKV ノードにコピーする時間が含まれるためです。
-   `Apply Log Duration` `Apply`スレッドによる`apply` Raftログのレイテンシーを記録します。

`Commit Log Duration`が長い場合の一般的なシナリオ:

-   TiKV CPUリソースにボトルネックがあり、スケジューリングのレイテンシーが高い
-   `raftstore.store-pool-size`は小さすぎるか大きすぎるかのいずれかです（大きすぎる値はパフォーマンスの低下を引き起こす可能性もあります）
-   I/Oレイテンシーが高く、結果として`Append Log Duration`レイテンシーが高くなります。
-   TiKVノード間のネットワークレイテンシーは高い
-   gRPC スレッドの数が少なすぎるため、CPU 使用率が gRPC スレッド間で不均一になります。

`Apply Log Duration`が長い場合の一般的なシナリオ:

-   TiKV CPUリソースにボトルネックがあり、スケジューリングのレイテンシーが高い
-   `raftstore.apply-pool-size`は小さすぎるか大きすぎるかのいずれかです（大きすぎる値はパフォーマンスの低下を引き起こす可能性もあります）
-   I/Oレイテンシーが高い

**例1: v5.3.0とv5.4.0での同じOLTPワークロードの比較**

v5.4.0では、書き込み中心のOLTPワークロードのQPSがv5.3.0と比較して14%向上しました。次の表は、3つの主要なレイテンシを比較したものです。

| 平均期間      | v5.3.0 (ミリ秒) | v5.4.0 (ミリ秒) |
| :-------- | :----------- | :----------- |
| ログ追加期間    | 0.27         | 0.303        |
| コミットログの期間 | 13           | 8.68         |
| ログ期間を適用する | 0.457        | 0.514        |

v5.4.0 では、gPRC モジュールが最適化され、 Raftログのレプリケーションが高速化され、v5.3.0 と比較して`Commit Log Duration`と`Store Duration`削減されました。

バージョン5.3.0:

![v5.3.0](/media/performance/v5.3.0_commit_append_apply.png)

バージョン5.4.0:

![v5.4.0](/media/performance/v5.4.0_commit_append_apply.png)

**例2: コミットログ期間がボトルネック**

![Store](/media/performance/cloud_append_commit_apply.png)

-   平均`Append Log Duration` = 4.38ミリ秒
-   平均`Commit Log Duration` = 7.92ミリ秒
-   平均`Apply Log Duration` = 172 us

スレッド`Store`の場合、 `Commit Log Duration`明らかに`Apply Log Duration`よりも高い値です。一方、 `Append Log Duration` `Apply Log Duration`よりも大幅に高い値であり、スレッド`Store`はCPUとI/Oの両方でボトルネックが発生している可能性があることを示しています。13と`Commit Log Duration` `Append Log Duration`削減する方法としては、以下のものが考えられます。

-   TiKV CPU リソースが十分な場合は、 `raftstore.store-pool-size`の値を増やして`Store`スレッドを追加することを検討してください。
-   TiDBがv5.4.0以降の場合は、 `raft-engine.enable: true`設定して[`Raft Engine`](/tikv-configuration-file.md#raft-engine)有効にすることを検討してください。RaftRaft Engineは軽量な実行パスを備えています。これにより、I/O書き込みの削減と、一部のシナリオにおける書き込みのロングテールレイテンシーの削減に役立ちます。
-   TiKV CPU リソースが十分で、TiDB が v5.3.0 以降の場合は、 `raftstore.store-io-pool-size: 1`設定して[`StoreWriter`](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)有効にすることを検討してください。

## TiDB のバージョンが v6.1.0 より前の場合、パフォーマンス概要ダッシュボードを使用するにはどうすればよいですか? {#if-my-tidb-version-is-earlier-than-v6-1-0-what-should-i-do-to-use-the-performance-overview-dashboard}

Grafana v6.1.0以降、デフォルトでパフォーマンス概要ダッシュボードが組み込まれています。このダッシュボードはTiDB v4.xおよびv5.xバージョンと互換性があります。TiDBがv6.1.0より前の場合は、次の図に示すように、 [`performance_overview.json`](https://github.com/pingcap/tidb/blob/release-8.5/pkg/metrics/grafana/performance_overview.json)手動でインポートする必要があります。

![Store](/media/performance/import_dashboard.png)
