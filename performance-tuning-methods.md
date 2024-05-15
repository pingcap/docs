---
title: Performance Analysis and Tuning
summary: Learn how to optimize database system based on database time and how to utilize the TiDB Performance Overview dashboard for performance analysis and tuning.
---

# パフォーマンス分析とチューニング {#performance-analysis-and-tuning}

このドキュメントでは、データベース時間によるチューニング方法について説明し、パフォーマンス分析とチューニングに TiDB [パフォーマンス概要ダッシュボード](/grafana-performance-overview-dashboard.md)を使用する方法を示します。

このドキュメントで説明する方法を使用すると、ユーザー応答時間とデータベース時間をグローバルかつトップダウンの観点から分析し、ユーザー応答時間のボトルネックの原因がデータベースの問題であるかどうかを確認できます。ボトルネックがデータベースにある場合は、データベース時間の概要と SQLレイテンシーの内訳を使用してボトルネックを特定し、パフォーマンスを調整できます。

## データベース時間に基づくパフォーマンスチューニング {#performance-tuning-based-on-database-time}

TiDB は、SQL 処理パスとデータベース時間を継続的に測定して収集します。そのため、TiDB ではデータベース パフォーマンスのボトルネックを簡単に特定できます。データベース時間メトリックに基づいて、ユーザー応答時間に関するデータがなくても、次の 2 つの目標を達成できます。

-   トランザクション内の平均 SQL 処理レイテンシーと TiDB 接続のアイドル時間を比較して、ボトルネックが TiDB にあるかどうかを判断します。
-   ボトルネックが TiDB にある場合は、データベース時間の概要、色ベースのパフォーマンス データ、主要なメトリック、リソース使用率、トップダウンのレイテンシーの内訳に基づいて、分散システム内の正確なモジュールをさらに特定します。

### TiDB がボトルネックですか? {#is-tidb-the-bottleneck}

-   トランザクションにおける TiDB 接続の平均アイドル時間が平均 SQL 処理レイテンシーよりも長い場合、アプリケーションのトランザクションレイテンシーの原因はデータベースではありません。データベース時間はユーザー応答時間のほんの一部を占めるだけなので、ボトルネックはデータベース外にあることがわかります。

    この場合、データベースの外部コンポーネントを確認します。たとえば、アプリケーションサーバーに十分なハードウェア リソースがあるかどうか、アプリケーションからデータベースへのネットワークレイテンシーが過度に高くないかを確認します。

-   平均 SQL 処理レイテンシーがトランザクション内の TiDB 接続の平均アイドル時間よりも長い場合、トランザクションのボトルネックは TiDB にあり、データベース時間がユーザー応答時間の大部分を占めます。

### ボトルネックが TiDB にある場合、それをどのように特定しますか? {#if-the-bottleneck-is-in-tidb-how-to-identify-it}

次の図は、典型的な SQL プロセスを示しています。ほとんどの SQL 処理パスが TiDB パフォーマンス メトリックでカバーされていることがわかります。データベース時間はさまざまなディメンションに分割され、それに応じて色分けされています。ワークロードの特性をすばやく理解し、データベース内のボトルネックがあればそれを捕捉できます。

![database time decomposition chart](/media/performance/dashboard-diagnostics-time-relation.png)

データベース時間は、すべての SQL 処理時間の合計です。データベース時間を次の 3 つの次元に分割すると、TiDB のボトルネックをすばやく特定するのに役立ちます。

-   SQL 処理タイプ別: どのタイプの SQL ステートメントが最も多くのデータベース時間を消費するかを判断します。計算式は次のとおりです。

    `DB Time = Select Time + Insert Time + Update Time + Delete Time + Commit Time + ...`

-   SQL 処理の 4 つのステップ (get_token/parse/compile/execute) ごとに、どのステップに最も時間がかかるかを判断します。計算式は次のとおりです。

    `DB Time = Get Token Time + Parse Time + Compile Time + Execute Time`

-   実行時間、TSO 待機時間、KV 要求時間、実行再試行時間によって、どの実行ステップがボトルネックになっているかを判断します。式は次のとおりです。

    `Execute Time ~= TiDB Executor Time + KV Request Time + PD TSO Wait Time + Retried execution time`

## パフォーマンス概要ダッシュボードを使用したパフォーマンス分析とチューニング {#performance-analysis-and-tuning-using-the-performance-overview-dashboard}

このセクションでは、Grafana のパフォーマンス概要ダッシュボードを使用して、データベース時間に基づいてパフォーマンス分析とチューニングを実行する方法について説明します。

パフォーマンス概要ダッシュボードは、TiDB、PD、および TiKV のメトリックを調整し、それぞれを次のセクションで表示します。

-   データベース時間と SQL 実行時間の概要: 色分けされた SQL タイプ、SQL 実行フェーズ別のデータベース時間、さまざまなリクエストのデータベース時間により、データベースのワークロード特性とパフォーマンスのボトルネックをすばやく特定できます。
-   主要なメトリックとリソース使用率: データベース QPS、接続情報、アプリケーションとデータベース間の要求コマンド タイプ、データベース内部 TSO および KV 要求 OPS、および TiDB/TiKV リソースの使用率が含まれます。
-   トップダウンのレイテンシーの内訳: クエリレイテンシーと接続アイドル時間の比較、クエリレイテンシーの内訳、SQL 実行における TSO 要求と KV 要求のレイテンシー、および TiKV 内部書き込みレイテンシーの内訳が含まれます。

### データベース時間とSQL実行時間の概要 {#database-time-and-sql-execution-time-overview}

データベース時間メトリックは、TiDB が 1 秒あたりに SQL を処理するレイテンシーの合計であり、これは TiDB が 1 秒あたりにアプリケーションの SQL 要求を同時に処理する合計時間でもあります (アクティブな接続の数に等しい)。

パフォーマンス概要ダッシュボードには、次の 3 つの積み上げ面グラフが表示されます。これらは、データベース ワークロード プロファイルを理解し、SQL 実行中のステートメント、SQL フェーズ、TiKV または PD 要求タイプの観点からボトルネックの原因をすばやく特定するのに役立ちます。

-   SQL タイプ別のデータベース時間
-   SQL フェーズごとのデータベース時間
-   SQL 実行時間の概要

#### 色で調整 {#tune-by-color}

データベース時間の内訳と実行時間の概要の図には、予想される時間消費と予想外の時間消費の両方が直感的に表示されます。そのため、パフォーマンスのボトルネックをすばやく特定し、ワークロード プロファイルを把握できます。緑色と青色の領域は、通常の時間消費とリクエストを表します。これら 2 つの図で緑色または青色以外の領域が大きな割合を占めている場合、データベース時間の配分は不適切です。

-   SQL タイプ別のデータベース時間:

    -   青: `Select`ステートメント
    -   `Insert` : `Update`およびその他のDML `Commit`
    -   `StmtClose` `StmtPrepare` `StmtReset`一般的な`StmtFetch`タイプ

-   SQL フェーズ別のデータベース時間: 一般的に、SQL 実行フェーズは緑色で、他のフェーズは赤色で表示されます。緑色以外の領域が大きい場合は、実行フェーズ以外のフェーズで多くのデータベース時間が消費されていることを意味し、さらに原因分析が必要です。一般的なシナリオとしては、準備されたプラン キャッシュが利用できないために、オレンジ色で表示されるコンパイル フェーズが大きな領域を占めるというものがあります。

-   SQL 実行時間の概要: 緑のメトリックは一般的な KV 書き込み要求 ( `Prewrite`や`Commit`など)、青のメトリックは一般的な KV 読み取り要求 (Cop や Get など)、紫のメトリックはTiFlash MPP 要求を表し、他の色のメトリックは注意が必要な予期しない状況を表します。たとえば、悲観的ロック KV 要求は赤でマークされ、TSO 待機は濃い茶色でマークされます。青または緑以外の領域が大きい場合は、SQL 実行中にボトルネックが発生していることを意味します。例:

    -   重大なロック競合が発生した場合、赤い領域が大きな割合を占めることになります。
    -   TSO の待機に過剰な時間が費やされると、濃い茶色の領域が大きな割合を占めることになります。

**例1: TPC-Cワークロード**

![TPC-C](/media/performance/tpcc_db_time.png)

-   SQL タイプ別のデータベース時間: 最も時間のかかるステートメントは、 `commit` 、 `update` 、 `select` 、および`insert`ステートメントです。
-   SQL フェーズ別のデータベース時間: 最も時間のかかるフェーズは緑色で表示される SQL 実行です。
-   SQL 実行時間の概要: SQL 実行で最も時間のかかる KV 要求は、緑色の`Prewrite`と`Commit`です。

    > **注記：**
    >
    > KV 要求の合計時間が実行時間よりも長くなるのは正常です。TiDB エグゼキュータが KV 要求を複数の TiKV に同時に送信し、KV 要求の合計待機時間が実行時間よりも長くなる可能性があるためです。前述の TPC-C ワークロードでは、トランザクションがコミットされると、TiDB は`Prewrite`と`Commit`要求を複数の TiKV に同時に送信します。したがって、この例の`Prewrite` 、 `Commit` 、および`PessimisticsLock`の要求の合計時間は、明らかに実行時間よりも長くなります。
    >
    > -   `execute`目の時間は、KV 要求の合計時間と`tso_wait`目の時間の合計よりも大幅に長くなる可能性があります。これは、SQL 実行時間のほとんどが TiDB エグゼキュータ内で費やされていることを意味します。一般的な例を 2 つ示します。

          > - Example 1: After TiDB executor reads a large amount of data from TiKV, it needs to do complex join and aggregation inside TiDB, which consumes a lot of time.

    <!---->

          > - Example 2: The application experiences serious write statement lock conflicts. Frequent lock retries result in long `Retried execution time`.

**例 2: OLTP 読み取り負荷の高いワークロード**

![OLTP](/media/performance/oltp_normal_db_time.png)

-   SQL タイプ別のデータベース時間: 時間のかかる主なステートメントは`SELECT` 、 `COMMIT` 、 `UPDATE` 、 `INSERT`で、その中で`SELECT`最も多くのデータベース時間を消費します。
-   SQL フェーズ別のデータベース時間: ほとんどの時間は緑色のフェーズ`execute`で消費されます。
-   SQL 実行時間の概要: SQL 実行フェーズでは、濃い茶色の`pd tso_wait` 、青色の`KV Get` 、緑色の`Prewrite`と`Commit`に時間がかかります。

**例3: 読み取り専用OLTPワークロード**

![OLTP](/media/performance/oltp_long_compile_db_time.png)

-   SQL タイプ別のデータベース時間: 主に`SELECT`ステートメントです。
-   SQL フェーズ別のデータベース時間: 時間のかかる主なフェーズは、オレンジ色の`compile`と緑色の`execute`です。フェーズ`compile`のレイテンシが最も高いのは、TiDB が実行プランを生成するのに時間がかかりすぎていることを示しています。その後のパフォーマンス データに基づいて、根本原因をさらに特定する必要があります。
-   SQL 実行時間の概要: 青色の KV BatchGet 要求は、SQL 実行中に最も多くの時間を消費します。

> **注記：**
>
> 例 3 では、 `SELECT`ステートメントで複数の TiKV から数千行を同時に読み取る必要があります。そのため、 `BatchGet`のリクエストの合計時間は実行時間よりもはるかに長くなります。

**例4: ロック競合ワークロード**

![OLTP](/media/performance/oltp_lock_contention_db_time.png)

-   SQL タイプ別のデータベース時間: 主に`UPDATE`ステートメントです。
-   SQL フェーズ別のデータベース時間: ほとんどの時間は緑色の実行フェーズで消費されます。
-   SQL 実行時間の概要: 赤で表示されている KV 要求 PessimisticLock は、SQL 実行中に最も多くの時間を消費し、実行時間は KV 要求の合計時間よりも明らかに長くなっています。これは、書き込みステートメントでの深刻なロック競合と頻繁なロック再試行によって発生します`Retried execution time` 。現在、TiDB は`Retried execution time`を測定しません。

**例5: HTAP CH-ベンチマークワークロード**

![HTAP](/media/performance/htap_tiflash_mpp.png)

-   SQL タイプ別のデータベース時間: 主に`SELECT`ステートメントです。
-   SQL フェーズ別のデータベース時間: ほとんどの時間は緑色の実行フェーズで消費されます。
-   SQL 実行時間の概要: 紫色で表示される`tiflash_mpp`リクエストは、SQL 実行中に最も多くの時間を消費します。次に、青色の`Cop`のリクエストを含む KV リクエストと、緑色の`Prewrite`のリクエストと`Commit`リクエストが続きます。

### TiDB の主要メトリクスとクラスタ リソースの使用率 {#tidb-key-metrics-and-cluster-resource-utilization}

#### 1秒あたりのクエリ数、1秒あたりのコマンド数、準備済みプランキャッシュ {#query-per-second-command-per-second-and-prepared-plan-cache}

パフォーマンス概要の次の 3 つのパネルを確認することで、アプリケーションのワークロード タイプ、アプリケーションが TiDB と対話する方法、アプリケーションが TiDB [準備されたプランキャッシュ](/sql-prepared-plan-cache.md)を最大限に活用しているかどうかを確認できます。

-   QPS: Query Per Second の略。アプリケーションによって実行された SQL ステートメントの数を示します。
-   タイプ別 CPS: Command Per Second の略。コマンドは、MySQL プロトコル固有のコマンドを示します。クエリ ステートメントは、クエリ コマンドまたはプリペアドステートメントのいずれかによって TiDB に送信できます。
-   プラン キャッシュ OPS を使用するクエリ: `avg-hit` 、TiDB クラスターで 1 秒あたりに実行プラン キャッシュを使用するクエリの数であり、 `avg-miss` 、TiDB クラスターで 1 秒あたりに実行プラン キャッシュを使用しないクエリの数です。

    `avg-hit + avg-miss`は`StmtExecute`に等しく、これは 1 秒あたりに実行されるすべてのクエリの数です。TiDB で準備済みプラン キャッシュを有効にすると、次の 3 つのシナリオが発生します。

    -   準備されたプラン キャッシュにヒットしません`avg-hit` (1 秒あたりのヒット数) は 0 で、 `avg-miss` 1 秒あたりのコマンド数`StmtExecute`に相当します。考えられる理由は次のとおりです。
        -   アプリケーションはクエリ インターフェイスを使用しています。
        -   アプリケーションは`StmtExecute`の実行ごとに`StmtClose`コマンドを呼び出すため、キャッシュされたプランはクリーンアップされます。
        -   `StmtExecute`によって実行されるすべてのステートメントは[キャッシュ条件](/sql-prepared-plan-cache.md)を満たさないため、実行プラン キャッシュにヒットできません。
    -   準備されたすべてのプラン キャッシュがヒットします`avg-hit` (1 秒あたりのヒット数) は 1 秒あたり`StmtExecute`のコマンドの数に等しく、 `avg-miss` (1 秒あたりのヒットなしの数) は 0 です。
    -   準備されたプラン キャッシュの一部がヒットしました: `avg-hit` (1 秒あたりのヒット数) は、1 秒あたりのコマンド数`StmtExecute`より少なくなります。準備されたプラン キャッシュには既知の制限があります。たとえば、サブクエリをサポートしていないため、サブクエリを含む SQL ステートメントでは準備されたプラン キャッシュを使用できません。

**例1: TPC-Cワークロード**

TPC-C のワークロード`INSERT` `UPDATE` `SELECT` 。合計 QPS は 1 秒あたり`StmtExecute`コマンドの数に等しく、後者は Queries Using Plan Cache OPS パネルの`avg-hit`にほぼ等しくなります。理想的には、クライアントはプリペアドステートメントのオブジェクトをキャッシュします。このようにして、SQL ステートメントが実行されると、キャッシュされたステートメントが直接呼び出されます。すべての SQL 実行は準備されたプラン キャッシュにヒットし、実行プランを生成するために再コンパイルする必要はありません。

![TPC-C](/media/performance/tpcc_qps.png)

**例 2: 準備されたプラン キャッシュは、読み取り専用 OLTP ワークロードのクエリ コマンドには使用できません。**

このワークロードでは、 `Commit QPS` = `Rollback QPS` = `Select QPS` 。アプリケーションは自動コミット同時実行を有効にしており、接続プールから接続がフェッチされるたびにロールバックが実行されます。その結果、これら 3 つのステートメントは同じ回数実行されます。

![OLTP-Query](/media/performance/oltp_long_compile_qps.png)

-   QPS パネルの赤い太線は失敗したクエリを表し、右側の Y 軸は失敗したクエリの数を示します。0 以外の値は、失敗したクエリが存在することを意味します。
-   合計 QPS は、CPS By Type パネルのクエリの数と等しく、クエリ コマンドがアプリケーションによって使用されています。
-   準備されたプラン キャッシュがクエリ コマンドに使用できないため、プラン キャッシュを使用するクエリ OPS パネルにはデータがありません。つまり、TiDB はクエリ実行ごとに実行プランを解析して生成する必要があります。その結果、TiDB による CPU 消費が増加すると、コンパイル時間が長くなります。

**例 3: OLTP ワークロードに対して準備プリペアドステートメントが有効になっている場合、準備済みプラン キャッシュは利用できません。**

`StmtPreare`回 = `StmtExecute`回 = `StmtClose`回 ~= `StmtFetch`回。アプリケーションは、準備 &gt; 実行 &gt; フェッチ &gt; 閉じるループを使用します。プリペアドステートメントオブジェクトのリークを防ぐために、多くのアプリケーション フレームワークは`execute`フェーズの後に`close`を呼び出します。これにより、2 つの問題が発生します。

-   SQL の実行には 4 つのコマンドと 4 回のネットワーク ラウンドトリップが必要です。
-   プラン キャッシュを使用したクエリの OPS は 0 で、準備されたプラン キャッシュのヒットがゼロであることを示します。1 `StmtClose`コマンドは、デフォルトでキャッシュされた実行プランをクリアし、次の`StmtPreare`コマンドは実行プランを再度生成する必要があります。

> **注記：**
>
> TiDB v6.0.0 以降では、グローバル変数 ( `set global tidb_ignore_prepared_cache_close_stmt=on;` ) を介して、 `StmtClose`コマンドがキャッシュされた実行プランをクリアするのを防ぐことができます。このようにして、後続の実行は準備されたプラン キャッシュをヒットすることができます。

![OLTP-Prepared](/media/performance/oltp_prepared_statement_no_plan_cache.png)

**例4: 準備されたステートメントにリソースリークがある**

1 秒あたり`StmtPrepare`コマンドの数は 1 秒あたり`StmtClose`コマンドの数よりもはるかに多く、これはアプリケーションに準備済みステートメントのオブジェクト リークがあることを示しています。

![OLTP-Query](/media/performance/prepared_statement_leaking.png)

-   QPS パネルでは、赤い太線は失敗したクエリの数を示し、右側のY軸は数値の座標値を示します。この例では、1 秒あたりの失敗したクエリの数は 74.6 です。
-   CPS By Type パネルでは、1 秒あたり`StmtPrepare`コマンドの数が 1 秒あたり`StmtClose`コマンドの数よりはるかに多く、準備されたステートメントのアプリケーションでオブジェクト リークが発生していることを示しています。
-   プラン キャッシュを使用したクエリ OPS パネルでは、 `avg-miss`タイプ別の CPS パネルの`StmtExecute`とほぼ等しく、ほとんどすべての SQL 実行で実行プラン キャッシュが失われていることを示しています。

#### KV/TSO リクエスト OPS とソース別の KV リクエスト時間 {#kv-tso-request-ops-and-kv-request-time-by-source}

-   KV/TSO リクエスト OPS パネルでは、1 秒あたりの KV および TSO リクエストの統計を表示できます。統計のうち、 `kv request total` TiDB から TiKV へのすべてのリクエストの合計を表します。TiDB から PD および TiKV へのリクエストの種類を観察することで、クラスター内のワークロード プロファイルを把握できます。
-   KV リクエスト時間 (ソース別) パネルでは、各 KV リクエスト タイプとすべてのリクエスト ソースの時間比率を表示できます。
    -   kv 要求合計時間: 1 秒あたりの KV およびTiFlash要求の処理時間の合計。
    -   各 KV リクエストと対応するリクエスト ソースは積み上げ棒グラフを形成し、 `external`通常のビジネス リクエストを識別し、 `internal`内部アクティビティ リクエスト (DDL やauto analyzeリクエストなど) を識別します。

**例 1: 忙しい作業負荷**

![TPC-C](/media/performance/tpcc_source_sql.png)

この TPC-C ワークロードでは、

-   1 秒あたりの KV リクエストの総数は 79,700 です。リクエスト数の多い順に、リクエスト タイプは`Prewrite` 、 `Commit` 、 `PessimisticsLock` 、 `BatchGet`です。
-   KV 処理時間のほとんどは`Commit-external_Commit`と`Prewrite-external_Commit`に費やされており、最も時間のかかる KV 要求は外部コミット ステートメントからの`Commit`と`Prewrite`であることがわかります。

**例2: ワークロードを分析する**

![OLTP](/media/performance/internal_stats.png)

このワークロードでは、クラスター内で実行されているステートメントは`ANALYZE`だけです。

-   1 秒あたりの KV リクエストの合計数は 35.5 で、1 秒あたりの Cop リクエストの数は 9.3 です。
-   KV 処理時間の大部分は`Cop-internal_stats`に費やされており、これは最も時間のかかる KV 要求が内部`ANALYZE`操作のうちの`Cop`であることを示しています。

#### TiDB CPU、TiKV CPU、および IO 使用量 {#tidb-cpu-tikv-cpu-and-io-usage}

TiDB CPU パネルと TiKV CPU/IO MBps パネルでは、平均、最大、デルタ (最大 CPU 使用率から最小 CPU 使用率を引いた値) を含む TiDB と TiKV の論理 CPU 使用率と IO スループットを観察できます。これに基づいて、TiDB と TiKV の全体的な CPU 使用率を判断できます。

-   `delta`値に基づいて、TiDB の CPU 使用率が不均衡であるかどうか (通常はアプリケーション接続の不均衡を伴う)、およびクラスター内に読み取り/書き込みのホット スポットがあるかどうかを判断できます。
-   TiDB および TiKV のリソース使用状況の概要を把握することで、クラスター内にリソースのボトルネックがあるかどうか、また TiKV または TiDB のスケールアウトが必要かどうかをすぐに判断できます。

**例 1: TiDB リソースの使用率が高い**

このワークロードでは、各 TiDB と TiKV は 8 個の CPU で構成されています。

![TPC-C](/media/performance/tidb_high_cpu.png)

-   TiDB の平均、最大、デルタ CPU 使用率はそれぞれ 575%、643%、136% です。
-   TiKV の平均、最大、およびデルタ CPU 使用率は、それぞれ 146%、215%、および 118% です。TiKV の平均、最大、およびデルタ I/O スループットは、それぞれ 9.06 MB/秒、19.7 MB/秒、および 17.1 MB/秒です。

明らかに、TiDB はより多くの CPU を消費し、8 CPU のボトルネックしきい値に近づいています。TiDB をスケールアウトすることをお勧めします。

**例 2: TiKV リソースの使用率が高い**

以下の TPC-C ワークロードでは、各 TiDB と TiKV は 16 個の CPU で構成されています。

![TPC-C](/media/performance/tpcc_cpu_io.png)

-   TiDB の平均、最大、デルタ CPU 使用率はそれぞれ 883%、962%、153% です。
-   TiKV の平均、最大、およびデルタ CPU 使用率は、それぞれ 1288%、1360%、および 126% です。TiKV の平均、最大、およびデルタ I/O スループットは、それぞれ 130 MB/秒、153 MB/秒、および 53.7 MB/秒です。

明らかに、TiKV はより多くの CPU を消費しますが、これは TPC-C が書き込みが多いシナリオであるため予想されたことです。パフォーマンスを向上させるには、TiKV をスケールアウトすることをお勧めします。

### クエリのレイテンシーの内訳と主要なレイテンシー指標 {#query-latency-breakdown-and-key-latency-metrics}

レイテンシーパネルには、平均値と 99 パーセンタイルが表示されます。平均値は全体的なボトルネックの特定に役立ち、99 パーセンタイルまたは 999 パーセンタイルは、レイテンシージッターが大きく発生しているかどうかを判断するのに役立ちます。

#### 期間、接続アイドル期間、接続数 {#duration-connection-idle-duration-and-connection-count}

期間パネルには、すべてのステートメントの平均および P99レイテンシーと、各 SQL タイプの平均レイテンシーが表示されます。接続アイドル期間パネルには、平均および P99 接続アイドル期間が表示されます。接続アイドル期間には、次の 2 つの状態が含まれます。

-   in-txn: 接続がトランザクション内にある場合、前の SQL を処理してから次の SQL ステートメントを受信するまでの間隔。
-   not-in-txn: 接続がトランザクション内にない場合に、前の SQL を処理してから次の SQL ステートメントを受信するまでの間隔。

アプリケーションは同じデータベース接続でトランザクションを実行します。平均クエリレイテンシーと接続アイドル期間を比較することで、TiDB がシステム全体のボトルネックになっているのか、それともユーザー応答時間のジッターが TiDB によって発生しているのかを判断できます。

-   アプリケーション ワークロードが読み取り専用ではなく、トランザクションが含まれている場合は、平均クエリレイテンシーを`avg-in-txn`と比較することで、データベースの内外でのトランザクション処理の割合を判別し、ユーザー応答時間のボトルネックを特定できます。
-   アプリケーションのワークロードが読み取り専用であるか、自動コミット モードがオンになっている場合は、平均クエリ待機レイテンシーを`avg-not-in-txn`と比較できます。

実際の顧客シナリオでは、ボトルネックがデータベースの外部にあることは珍しくありません。次に例を示します。

-   クライアントサーバーの構成が低すぎるため、CPU リソースが使い果たされています。
-   HAProxy は TiDB クラスター プロキシとして使用され、HAProxy CPU リソースが使い果たされています。
-   HAProxy は TiDB クラスター プロキシとして使用され、高負荷時には HAProxyサーバーのネットワーク帯域幅が消費されます。
-   アプリケーションサーバーからデータベースへのネットワークレイテンシーが高くなります。たとえば、パブリック クラウドのデプロイメントでは、アプリケーションと TiDB クラスターが同じリージョンにないか、DNS ワークロード バランサーと TiDB クラスターが同じリージョンにないため、ネットワークレイテンシーが高くなります。
-   ボトルネックはクライアント アプリケーションにあります。アプリケーション サーバーの CPU コアと Numa リソースを十分に活用できません。たとえば、TiDB への何千もの JDBC 接続を確立するために、1 つの JVM のみが使用されます。

接続数パネルでは、接続の合計数と各 TiDB ノードの接続数を確認できます。これにより、接続の合計数が正常かどうか、および各 TiDB ノードの接続数が不均衡かどうかを判断することができます。1 `active connections`アクティブな接続数を示し、これは 1 秒あたりのデータベース時間に相当します。右側のY軸 ( `disconnection/s` ) は、クラスター内の 1 秒あたりの切断数を示し、これを使用して、アプリケーションが短い接続を使用しているかどうかを判断できます。

**例1: 切断回数が多すぎる**

![high disconnection/s](/media/performance/high_disconnections.png)

このワークロードでは、

-   すべての SQL ステートメントの平均レイテンシーと P99レイテンシーは、それぞれ 10.8 ミリ秒と 84.1 ミリ秒です。
-   トランザクション`avg-in-txn`の平均接続アイドル時間は 9.4 ミリ秒です。
-   クラスターへの接続総数は 3,700 で、各 TiDB ノードへの接続数は 1,800 です。アクティブ接続の平均数は 40.3 で、ほとんどの接続がアイドル状態であることを示しています。1 `disonnnection/s`平均数は 55.8 で、アプリケーションが頻繁に接続と切断を行っていることを示しています。短い接続の動作は、TiDB リソースと応答時間に一定の影響を及ぼします。

**例2: TiDBがユーザー応答時間のボトルネックとなっている**

![TiDB is the Bottleneck](/media/performance/tpcc_duration_idle.png)

この TPC-C ワークロードでは、

-   すべての SQL ステートメントの平均レイテンシーと P99レイテンシーは、それぞれ 477 マイクロ秒と 3.13 ミリ秒です。コミット ステートメント、挿入ステートメント、クエリ ステートメントの平均レイテンシは、それぞれ 2.02 ミリ秒、609 マイクロ秒、468 マイクロ秒です。
-   トランザクション`avg-in-txn`の平均接続アイドル時間は 171 マイクロ秒です。

平均クエリレイテンシーは`avg-in-txn`よりも大幅に大きいため、トランザクションの主なボトルネックはデータベース内にあることを意味します。

**例3: TiDBはユーザー応答時間のボトルネックではない**

![TiDB is not Bottleneck](/media/performance/cloud_query_long_idle.png)

このワークロードでは、平均クエリレイテンシーは 1.69 ミリ秒で、 `avg-in-txn` 18 ミリ秒です。これは、TiDB がトランザクション内の SQL ステートメントを処理するのに平均 1.69 ミリ秒を費やし、その後次のステートメントを受信するのに 18 ミリ秒待機する必要があることを示しています。

平均クエリレイテンシーは`avg-in-txn`より大幅に低くなっています。ユーザー応答時間のボトルネックは TiDB にはありません。この例はパブリック クラウド環境にあり、アプリケーションとデータベースが同じリージョンにないため、アプリケーションとデータベース間のネットワークレイテンシーが高く、接続アイドル時間が非常に長くなります。

#### 解析、コンパイル、実行にかかる時間 {#parse-compile-and-execute-duration}

TiDB では、クエリ ステートメントの送信から結果の返送までに[典型的な処理フロー](/sql-optimization-concepts.md)必要です。

TiDB での SQL 処理は、 `get token` 、 `parse` 、 `compile` 、 `execute` 4 つのフェーズで構成されます。

-   `get token` : 通常は数マイクロ秒のみで、無視できます。トークンは、単一の TiDB インスタンスへの接続数が[トークン制限](/tidb-configuration-file.md)制限に達した場合にのみ制限されます。
-   `parse` : クエリ ステートメントは抽象構文ツリー (AST) に解析されます。
-   `compile` : 実行プランは、フェーズ`parse`の AST と統計に基づいてコンパイルされます。フェーズ`compile`には、論理最適化と物理最適化が含まれます。論理最適化では、リレーショナル代数に基づく列プルーニングなどのルールによってクエリ プランが最適化されます。物理最適化では、コストベースのオプティマイザーによって統計によって実行プランのコストが見積もられ、コストが最も低い物理実行プランが選択されます。
-   `execute` : SQL ステートメントを実行するのにかかる時間。TiDB は最初にグローバルに一意のタイムスタンプ TSO を待機します。次に、エグゼキュータは実行プラン内のオペレータのキー範囲に基づいて TiKV API 要求を構築し、それを TiKV に配布します。2 時間には`execute` TSO 待機時間、KV 要求時間、および TiDB エグゼキュータがデータ処理に費やした時間が含まれます。

アプリケーションが`query`または`StmtExecute` MySQL コマンド インターフェイスのみを使用する場合は、次の式を使用して平均レイテンシーのボトルネックを特定できます。

    avg Query Duration = avg Get Token + avg Parse Duration + avg Compile Duration + avg Execute Duration

通常、 `execute`フェーズが`query`のレイテンシーの大部分を占めます。ただし、次の場合には`parse`フェーズと`compile`フェーズも大きな部分を占めることがあります。

-   フェーズ`parse`での長いレイテンシー: たとえば、ステートメント`query`が長い場合、SQL テキストを解析するために多くの CPU が消費されます。
-   `compile`フェーズでの長いレイテンシー: 準備されたプラン キャッシュ`compile`ヒットしない場合、TiDB は SQL 実行ごとに実行プランをコンパイルする必要があります。3 フェーズでのレイテンシーは、数ミリ秒から数十ミリ秒、あるいはそれ以上になることがあります。準備されたプラン キャッシュがヒットしない場合は、 `compile`フェーズで論理的および物理的な最適化が行われ、CPU とメモリが大量に消費され、Go ランタイム (TiDB は[`Go`](https://go.dev/)で記述されています) が圧迫され、他の TiDB コンポーネントのパフォーマンスに影響します。準備されたプラン キャッシュは、TiDB で OLTP ワークロードを効率的に処理するために重要です。

**例1: `compile`フェーズでのデータベースのボトルネック**

![Compile](/media/performance/long_compile.png)

上の図では、 `parse` 、 `compile` 、 `execute`フェーズの平均時間は、それぞれ 17.1 us、729 us、681 us です。 `compile`レイテンシーが高くなるのは、アプリケーションが`query`コマンド インターフェイスを使用し、準備されたプラン キャッシュを使用できないためです。

**例2: `execute`フェーズでのデータベースのボトルネック**

![Execute](/media/performance/long_execute.png)

この TPC-C ワークロードでは、フェーズ`parse`の平均時間`execute`それぞれ 7.39 マイクロ秒、38.1 マイクロ秒、12.8 ミリ秒`compile` 。フェーズ`execute`が`query`レイテンシーのボトルネックです。

#### KV および TSO リクエスト期間 {#kv-and-tso-request-duration}

TiDB は、フェーズ`execute`で PD および TiKV と対話します。次の図に示すように、SQL 要求を処理するときに、TiDB はフェーズ`parse`および`compile`に入る前に TSO を要求します。PD クライアントは呼び出し元をブロックせず、 `TSFuture`を返し、バックグラウンドで TSO 要求を非同期的に送受信します。PD クライアントは TSO 要求の処理を終了すると、 `TSFuture`を返します。 `TSFuture`の保持者は、最後の TSO を取得するために Wait メソッドを呼び出す必要があります。TiDB はフェーズ`parse`および`compile`を終了すると、フェーズ`execute`に入ります。このフェーズでは、次の 2 つの状況が発生する可能性があります。

-   TSO要求が完了した場合、Waitメソッドは利用可能なTSOまたはエラーを直ちに返します。
-   TSO リクエストがまだ完了していない場合、TSO が利用可能になるかエラーが表示されるまで (gRPC リクエストは送信されたが結果が返されず、ネットワークレイテンシーが高い)、Wait メソッドはブロックされます。

TSO 待機時間は`TSO WAIT`として記録され、TSO 要求のネットワーク時間は`TSO RPC`として記録されます。TSO 待機が完了すると、通常、TiDB エグゼキュータは読み取りまたは書き込み要求を TiKV に送信します。

-   一般的な KV 読み取り要求: `Get` `BatchGet`および`Cop`
-   一般的なKV書き込み要求`Commit` 2フェーズコミットの場合`Prewrite` `PessimisticLock`

![Execute](/media/performance/execute_phase.png)

このセクションのインジケーターは、次の 3 つのパネルに対応しています。

-   平均 TiDB KV リクエスト期間: TiDB によって測定された KV リクエストの平均レイテンシー
-   平均 TiKV GRPC 期間: TiKV での gPRC メッセージの処理の平均レイテンシー
-   PD TSO 待機/RPC 期間: TiDB エグゼキュータの TSO 待機時間と TSO 要求 (RPC) のネットワークレイテンシー

`Avg TiDB KV Request Duration`と`Avg TiKV GRPC Duration`の関係は次のようになります。

    Avg TiDB KV Request Duration = Avg TiKV GRPC Duration + Network latency between TiDB and TiKV + TiKV gRPC processing time + TiDB gRPC processing time and scheduling latency

`Avg TiDB KV Request Duration`と`Avg TiKV GRPC Duration`の違いは、ネットワーク トラフィック、ネットワークレイテンシー、および TiDB と TiKV によるリソース使用量に密接に関係しています。

-   同じデータセンター内: 差は通常 2 ミリ秒未満です。
-   同じリージョン内の異なるアベイラビリティゾーンの場合: 差は通常 5 ミリ秒未満です。

**例1: 同じデータセンターに展開されたクラスタのワークロードが低い**

![Same Data Center](/media/performance/oltp_kv_tso.png)

このワークロードでは、TiDB での平均`Prewrite`レイテンシーは 925 us で、TiKV 内での平均`kv_prewrite`処理レイテンシーは720 us です。この差は約 200 us で、同じデータ センターでは正常です。平均 TSO 待機レイテンシーは 206 us、RPC 時間は 144 us です。

**例 2: パブリック クラウド クラスタ上の通常のワークロード**

![Cloud Env ](/media/performance/cloud_kv_tso.png)

この例では、TiDB クラスターは同じリージョン内の異なるデータセンターに展開されています。TiDB の平均`commit`レイテンシーは 12.7 ミリ秒で、TiKV 内の平均`kv_commit`処理レイテンシーは10.2 ミリ秒で、約 2.5 ミリ秒の差があります。平均 TSO 待機レイテンシーは 3.12 ミリ秒、RPC 時間は 693 マイクロ秒です。

**例3: パブリッククラウドクラスタのリソース過負荷**

![Cloud Env, TiDB Overloaded](/media/performance/cloud_kv_tso_overloaded.png)

この例では、TiDB クラスターが同じリージョン内の異なるデータセンターに展開されており、TiDB ネットワークと CPU リソースが深刻な過負荷状態になっています。TiDB 上の平均`BatchGet`レイテンシーは 38.6 ミリ秒で、TiKV 内の平均`kv_batch_get`処理レイテンシーは 6.15 ミリ秒です。その差は 32 ミリ秒以上で、通常値よりもはるかに高くなっています。平均 TSO 待機レイテンシーは 9.45 ミリ秒、RPC 時間は 14.3 ミリ秒です。

#### ストレージ非同期書き込み期間、保存期間、適用期間 {#storage-async-write-duration-store-duration-and-apply-duration}

TiKV は次の手順で書き込み要求を処理します。

-   `scheduler worker`書き込み要求を処理し、トランザクションの一貫性チェックを実行し、書き込み要求をキーと値のペアに変換して`raftstore`モジュールに送信します。
-   TiKV コンセンサス モジュール`raftstore`は、 Raftコンセンサス アルゴリズムを適用して、storageレイヤー(複数の TiKV で構成) をフォールト トレラントにします。

    Raftstore は`Store`スレッドと`Apply`スレッドで構成されています。

    -   `Store`スレッドはRaftメッセージと新しい`proposals`を処理します。新しい`proposals`が受信されると、リーダー ノードの`Store`スレッドはローカルRaft DB に書き込み、メッセージを複数のフォロワー ノードにコピーします。ほとんどの場合、この`proposals`正常に永続化されると、 `proposals`が正常にコミットされます。
    -   `Apply`スレッドはコミットされた`proposals` KV DB に書き込みます。コンテンツが KV DB に正常に書き込まれると、 `Apply`スレッドは書き込み要求が完了したことを外部に通知します。

![TiKV Write](/media/performance/store_apply.png)

`Storage Async Write Duration`メトリックは、書き込み要求が raftstore に入った後のレイテンシーを記録します。データは要求ごとに収集されます。

`Storage Async Write Duration`メトリックには、 `Store Duration`と`Apply Duration` 2 つの部分が含まれます。次の式を使用して、書き込み要求のボトルネックが`Store`ステップにあるか`Apply`ステップにあるかを判断できます。

    avg Storage Async Write Duration = avg Store Duration + avg Apply Duration

> **注記：**
>
> `Store Duration`と`Apply Duration` v5.3.0 以降でサポートされています。

**例1: v5.3.0とv5.4.0での同じOLTPワークロードの比較**

前述の式によると、書き込みが多い OLTP ワークロードの QPS は、v5.4.0 では v5.3.0 よりも 14% 高くなります。

-   v5.3.0: 24.4 ミリ秒 ~= 17.7 ミリ秒 + 6.59 ミリ秒
-   v5.4.0: 21.4 ミリ秒 ~= 14.0 ミリ秒 + 7.33 ミリ秒

v5.4.0 では、gPRC モジュールが最適化され、 Raftログのレプリケーションが高速化され、v5.3.0 と比較して`Store Duration`削減されました。

v5.3.0:

![v5.3.0](/media/performance/v5.3.0_store_apply.png)

v5.4.0:

![v5.4.0](/media/performance/v5.4.0_store_apply.png)

**例2: 保存期間がボトルネック**

上記の式を適用します: 10.1 ms ~= 9.81 ms + 0.304 ms。結果は、書き込み要求のレイテンシーのボトルネックが`Store Duration`にあることを示しています。

![Store](/media/performance/cloud_store_apply.png)

#### コミットログ期間、追加ログ期間、適用ログ期間 {#commit-log-duration-append-log-duration-and-apply-log-duration}

`Commit Log Duration` `Apply Log Duration` `Append Log Duration`内の主要な操作のレイテンシーメトリックです。これらのレイテンシはバッチ操作レベルでキャプチャされ、各操作は複数の書き込み要求を組み合わせます。したがって、レイテンシは上記の`Store Duration`と`Apply Duration`に直接対応するわけではありません。

-   `Commit Log Duration`と`Append Log Duration` `Store`で実行された操作の時間を記録します`Commit Log Duration`には、 Raftログを他の TiKV ノードにコピーする時間が含まれます (raft-log の永続性を確保するため)。8 `Commit Log Duration`は通常、リーダー用とフォロワー用の 2 つ`Append Log Duration`操作が含まれます。12 `Commit Log Duration`通常、 `Append Log Duration`よりも大幅に高くなります。これは、前者には、ネットワークを介してRaftログを他の TiKV ノードにコピーする時間が含まれるためです。
-   `Apply Log Duration` `Apply`スレッドによる`apply`のRaftログのレイテンシーを記録します。

`Commit Log Duration`が長い一般的なシナリオ:

-   TiKV CPUリソースにボトルネックがあり、スケジューリングのレイテンシーが高い
-   `raftstore.store-pool-size`は小さすぎるか大きすぎるかのいずれかです (大きすぎる値はパフォーマンスの低下を引き起こす可能性もあります)
-   I/Oレイテンシーが高く、結果として`Append Log Duration`レイテンシーが高くなる
-   TiKVノード間のネットワークレイテンシーは高い
-   gRPC スレッドの数が少なすぎるため、GRPC スレッド間で CPU 使用率が不均一になります。

`Apply Log Duration`が長い一般的なシナリオ:

-   TiKV CPUリソースにボトルネックがあり、スケジューリングのレイテンシーが高い
-   `raftstore.apply-pool-size`は小さすぎるか大きすぎるかのいずれかです (大きすぎる値はパフォーマンスの低下を引き起こす可能性もあります)
-   I/Oレイテンシーが高い

**例1: v5.3.0とv5.4.0での同じOLTPワークロードの比較**

v5.4.0 の書き込み量が多い OLTP ワークロードの QPS は、v5.3.0 と比較して 14% 向上しています。次の表は、3 つの主要なレイテンシを比較したものです。

| 平均所要時間    | v5.3.0 (ミリ秒) | v5.4.0 (ミリ秒) |
| :-------- | :----------- | :----------- |
| ログ追加期間    | 0.27         | 0.303        |
| コミットログの期間 | 13           | 8.68         |
| ログ期間の適用   | 0.457        | 0.514        |

v5.4.0 では、gPRC モジュールが最適化され、 Raftログのレプリケーションが高速化され、v5.3.0 と比較して`Commit Log Duration`と`Store Duration`が削減されました。

v5.3.0:

![v5.3.0](/media/performance/v5.3.0_commit_append_apply.png)

v5.4.0:

![v5.4.0](/media/performance/v5.4.0_commit_append_apply.png)

**例2: コミットログ期間がボトルネックになる**

![Store](/media/performance/cloud_append_commit_apply.png)

-   平均`Append Log Duration` = 4.38 ミリ秒
-   平均`Commit Log Duration` = 7.92 ミリ秒
-   平均`Apply Log Duration` = 172 us

`Store`スレッドの場合、 `Commit Log Duration`は明らかに`Apply Log Duration`よりも高いです。一方、 `Append Log Duration`は`Apply Log Duration`よりも大幅に高いため、 `Store`スレッドは CPU と I/O の両方でボトルネックが発生している可能性があります。 `Commit Log Duration`と`Append Log Duration`減らすには、次の方法があります。

-   TiKV CPU リソースが十分な場合は、 `raftstore.store-pool-size`の値を増やして`Store`スレッドを追加することを検討してください。
-   TiDB が v5.4.0 以降の場合は、 `raft-engine.enable: true`設定して[`Raft Engine`](/tikv-configuration-file.md#raft-engine)有効にすることを検討してください。RaftRaft Engineには軽量実行パスがあります。これにより、一部のシナリオで I/O 書き込みと書き込みのロングテールレイテンシーを削減できます。
-   TiKV CPU リソースが十分であり、TiDB が v5.3.0 以降である場合は、 `raftstore.store-io-pool-size: 1`設定して[`StoreWriter`](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を有効にすることを検討してください。

## TiDB のバージョンが v6.1.0 より前の場合、パフォーマンス概要ダッシュボードを使用するにはどうすればよいでしょうか? {#if-my-tidb-version-is-earlier-than-v6-1-0-what-should-i-do-to-use-the-performance-overview-dashboard}

v6.1.0 以降、Grafana にはデフォルトでパフォーマンス概要ダッシュボードが組み込まれています。このダッシュボードは、TiDB v4.x および v5.x バージョンと互換性があります。TiDB が v6.1.0 より前の場合は、次の図に示すように、 [`performance_overview.json`](https://github.com/pingcap/tidb/blob/release-7.5/pkg/metrics/grafana/performance_overview.json)手動でインポートする必要があります。

![Store](/media/performance/import_dashboard.png)
