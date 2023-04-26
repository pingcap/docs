---
title: Performance Analysis and Tuning
summary: Learn how to optimize database system based on database time and how to utilize the TiDB Performance Overview dashboard for performance analysis and tuning.
---

# パフォーマンス分析とチューニング {#performance-analysis-and-tuning}

このドキュメントでは、データベース時間によるチューニング アプローチについて説明し、TiDB [パフォーマンス概要ダッシュボード](/grafana-performance-overview-dashboard.md)を使用してパフォーマンス分析とチューニングを行う方法を示します。

このドキュメントで説明する方法を使用すると、グローバルおよびトップダウンの観点からユーザー応答時間とデータベース時間を分析して、ユーザー応答時間のボトルネックがデータベースの問題によって引き起こされているかどうかを確認できます。ボトルネックがデータベースにある場合は、データベース時間の概要と SQLレイテンシーの内訳を使用して、ボトルネックを特定し、パフォーマンスを調整できます。

## データベース時間に基づくパフォーマンス チューニング {#performance-tuning-based-on-database-time}

TiDB は、SQL 処理パスとデータベース時間を常に測定および収集しています。したがって、TiDB でのデータベース パフォーマンスのボトルネックを特定するのは簡単です。データベース時間メトリックに基づいて、ユーザー応答時間に関するデータがなくても、次の 2 つの目標を達成できます。

-   トランザクション内の TiDB 接続のアイドル時間と SQL 処理の平均レイテンシーを比較して、ボトルネックが TiDB にあるかどうかを判断します。
-   ボトルネックが TiDB にある場合は、データベース時間の概要、色ベースのパフォーマンス データ、主要なメトリック、リソース使用率、およびトップレイテンシーのレイテンシの内訳に基づいて、分散システム内の正確なモジュールをさらに特定します。

### TiDB がボトルネックですか? {#is-tidb-the-bottleneck}

-   トランザクション内の TiDB 接続の平均アイドル時間が SQL 処理の平均レイテンシーよりも長い場合、データベースはアプリケーションのトランザクションレイテンシーの原因ではありません。データベース時間は、ユーザー応答時間のごく一部しか占めていません。これは、ボトルネックがデータベースの外にあることを示しています。

    この場合、データベースの外部コンポーネントを確認してください。たとえば、アプリケーションサーバーに十分なハードウェア リソースがあるかどうか、およびアプリケーションからデータベースへのネットワークレイテンシーが過度に長いかどうかを判断します。

-   SQL 処理の平均レイテンシーが、トランザクション内の TiDB 接続の平均アイドル時間よりも長い場合、トランザクションのボトルネックは TiDB にあり、データベース時間はユーザー応答時間の大部分を占めています。

### ボトルネックが TiDB にある場合、それを特定する方法は? {#if-the-bottleneck-is-in-tidb-how-to-identify-it}

次の図は、典型的な SQL プロセスを示しています。ほとんどの SQL 処理パスが TiDB パフォーマンス メトリックでカバーされていることがわかります。データベース時間はさまざまな次元に分類され、それに応じて色が付けられます。ワークロードの特性をすばやく理解し、データベース内のボトルネックがあればそれをキャッチできます。

![database time decomposition chart](/media/performance/dashboard-diagnostics-time-relation.png)

データベース時間は、すべての SQL 処理時間の合計です。データベース時間を次の 3 つの次元に分類すると、TiDB のボトルネックをすばやく特定するのに役立ちます。

-   SQL 処理タイプ別: どのタイプの SQL ステートメントが最もデータベース時間を消費しているかを判別します。式は次のとおりです。

    `DB Time = Select Time + Insert Time + Update Time + Delete Time + Commit Time + ...`

-   SQL 処理の 4 つのステップ (get_token/parse/compile/execute) によって、どのステップが最も時間を消費するかを判別します。式は次のとおりです。

    `DB Time = Get Token Time + Parse Time + Compile Time + Execute Time`

-   エグゼキューター時間、TSO 待機時間、KV 要求時間、および実行再試行時間によって: どの実行ステップがボトルネックを構成しているかを判別します。式は次のとおりです。

    `Execute Time ~= TiDB Executor Time + KV Request Time + PD TSO Wait Time + Retried execution time`

## パフォーマンス概要ダッシュボードを使用したパフォーマンス分析とチューニング {#performance-analysis-and-tuning-using-the-performance-overview-dashboard}

このセクションでは、Grafana のパフォーマンス概要ダッシュボードを使用して、データベース時間に基づいてパフォーマンス分析とチューニングを実行する方法について説明します。

Performance Overview ダッシュボードは、TiDB、PD、および TiKV のメトリックを調整し、それぞれを次のセクションに示します。

-   データベース時間と SQL 実行時間の概要: 色分けされた SQL の種類、SQL 実行フェーズごとのデータベース時間、およびさまざまな要求のデータベース時間により、データベースのワークロードの特性とパフォーマンスのボトルネックをすばやく特定できます。
-   主要なメトリックとリソース使用率: データベース QPS、接続情報、アプリケーションとデータベース間の要求コマンド タイプ、データベース内部 TSO および KV 要求 OPS、および TiDB/TiKV リソース使用率が含まれます。
-   トップダウンレイテンシーの内訳: クエリレイテンシーと接続アイドル時間の比較、クエリレイテンシーの内訳、SQL 実行における TSO 要求と KV リクエストのレイテンシー、および TiKV 内部書き込みレイテンシーの内訳が含まれています。

### データベース時間と SQL 実行時間の概要 {#database-time-and-sql-execution-time-overview}

データベース時間メトリックは、TiDB が 1 秒あたりに SQL を処理するレイテンシーの合計です。これは、TiDB が 1 秒あたりにアプリケーション SQL 要求を同時に処理する合計時間でもあります (アクティブな接続の数に等しい)。

Performance Overview ダッシュボードには、次の 3 つの積み上げ面グラフが表示されます。これらは、データベースのワークロード プロファイルを理解し、ステートメント、SQL フェーズ、および SQL 実行中の TiKV または PD リクエスト タイプに関してボトルネックの原因を迅速に特定するのに役立ちます。

-   SQL タイプ別のデータベース時間
-   SQLフェーズ別データベース時間
-   SQL 実行時間の概要

#### 色で調整 {#tune-by-color}

データベース時間の内訳と実行時間の概要の図は、予想される時間消費と予想外の時間消費の両方を直感的に示します。したがって、パフォーマンスのボトルネックをすばやく特定し、ワークロード プロファイルを学習できます。緑と青のエリアは、通常の消費時間とリクエストを表しています。これらの 2 つの図で緑色または青色以外の領域がかなりの割合を占めている場合、データベースの時間分布は不適切です。

-   SQL タイプ別のデータベース時間:

    -   青: `Select`ステートメント
    -   緑: `Update` 、 `Insert` 、 `Commit`およびその他の DML ステートメント
    -   赤: `StmtPrepare` 、 `StmtReset` 、 `StmtFetch` 、および`StmtClose`を含む一般的な SQL タイプ

-   SQL フェーズ別のデータベース時間: 一般的に、SQL 実行フェーズは緑色で、その他のフェーズは赤色で表示されます。緑以外の領域が大きい場合は、実行フェーズ以外のフェーズで多くのデータベース時間が費やされていることを意味し、さらなる原因分析が必要です。一般的なシナリオは、準備されたプラン キャッシュが利用できないために、オレンジ色で示されたコンパイル フェーズが大きな領域を占有することです。

-   SQL 実行時間の概要: 緑色のメトリックは一般的な KV 書き込み要求 ( `Prewrite`や`Commit`など) を表し、青色のメトリックは一般的な KV 読み取り要求 (Cop や Get など) を表し、紫色のメトリックはTiFlash MPP 要求を表し、その他の色のメトリックは注意が必要な予期しない状況を表します。たとえば、悲観的ロック KV 要求は赤でマークされ、TSO 待機は濃い茶色でマークされます。青または緑以外の領域が大きい場合は、SQL 実行中にボトルネックがあることを意味します。例えば：

    -   重大なロック競合が発生した場合、赤い領域が大きな割合を占めます。
    -   TSO の待機に過度の時間が費やされると、こげ茶色の領域が大きな割合を占めます。

**例 1: TPC-C ワークロード**

![TPC-C](/media/performance/tpcc_db_time.png)

-   SQL タイプ別のデータベース時間: 最も時間がかかるステートメントは、 `commit` 、 `update` 、 `select` 、および`insert`ステートメントです。
-   SQL フェーズごとのデータベース時間: 最も時間がかかるフェーズは、緑の SQL 実行です。
-   SQL 実行時間の概要: SQL 実行で最も時間がかかる KV 要求は、緑色の`Prewrite`と`Commit`です。

    > **ノート：**
    >
    > KV 要求の合計時間が実行時間よりも長くなるのは正常です。 TiDB executor が KV リクエストを複数の TiKV に同時に送信する可能性があるため、KV リクエストの合計待機時間が実行時間よりも長くなります。前述の TPC-C ワークロードでは、トランザクションがコミットされると、TiDB は`Prewrite`つと`Commit`リクエストを複数の TiKV に同時に送信します。したがって、この例の`Prewrite` 、 `Commit` 、および`PessimisticsLock`リクエストの合計時間は、実行時間よりも明らかに長くなります。
    >
    > -   `execute`時間は、KV 要求の合計時間に`tso_wait`時間を加えた時間よりも大幅に長くなる場合もあります。これは、SQL 実行時間のほとんどが TiDB executor 内で費やされることを意味します。次に、2 つの一般的な例を示します。

    ```
      > - Example 1: After TiDB executor reads a large amount of data from TiKV, it needs to do complex join and aggregation inside TiDB, which consumes a lot of time.
    ```

    ```
      > - Example 2: The application experiences serious write statement lock conflicts. Frequent lock retries result in long `Retried execution time`.
    ```

**例 2: OLTP 読み取り負荷の高いワークロード**

![OLTP](/media/performance/oltp_normal_db_time.png)

-   SQL タイプ別のデータベース時間: 時間のかかる主なステートメントは`SELECT` 、 `COMMIT` 、 `UPDATE` 、および`INSERT`であり、そのうち`SELECT`最も多くのデータベース時間を消費します。
-   SQL フェーズごとのデータベース時間: ほとんどの時間は、緑の`execute`フェーズで消費されます。
-   SQL 実行時間の概要: SQL 実行フェーズでは、濃い茶色の`pd tso_wait` 、青色の`KV Get` 、緑色の`Prewrite`と`Commit`が時間がかかります。

**例 3: 読み取り専用の OLTP ワークロード**

![OLTP](/media/performance/oltp_long_compile_db_time.png)

-   SQL タイプ別のデータベース時間: 主に`SELECT`のステートメントです。
-   SQL フェーズごとのデータベース時間: 時間のかかる主要なフェーズは、オレンジ色の`compile`と緑色の`execute`です。 `compile`フェーズのレイテンシーが最も高く、TiDB が実行計画を生成するのに時間がかかりすぎており、その後のパフォーマンス データに基づいて根本原因をさらに特定する必要があることを示しています。
-   SQL 実行時間の概要: 青色の KV BatchGet リクエストは、SQL 実行中に最も多くの時間を消費します。

> **ノート：**
>
> 例 3 では、 `SELECT`ステートメントで複数の TiKV から同時に数千行を読み取る必要があります。したがって、 `BatchGet`要求の合計時間は、実行時間よりもはるかに長くなります。

**例 4: ロック競合ワークロード**

![OLTP](/media/performance/oltp_lock_contention_db_time.png)

-   SQL タイプ別のデータベース時間: 主に`UPDATE`のステートメントです。
-   SQL フェーズごとのデータベース時間: ほとんどの時間は実行フェーズで緑色で消費されます。
-   SQL 実行時間の概要: 赤で示されている KV リクエスト PessimisticLock は、SQL 実行中に最も多くの時間を消費し、実行時間は KV リクエストの合計時間よりも明らかに長くなります。これは、書き込みステートメントでの重大なロック競合が原因で発生し、頻繁なロックの再試行が長引きます`Retried execution time` 。現在、TiDB は`Retried execution time`を測定していません。

**例 5: HTAP CH-Benchmark ワークロード**

![HTAP](/media/performance/htap_tiflash_mpp.png)

-   SQL タイプ別のデータベース時間: 主に`SELECT`のステートメントです。
-   SQL フェーズごとのデータベース時間: ほとんどの時間は実行フェーズで緑色で消費されます。
-   SQL 実行時間の概要: 紫色で示されている`tiflash_mpp`要求は、SQL の実行中に最も多くの時間を消費します。次に、青色の`Cop`の要求、緑色の`Prewrite`および`Commit`要求を含む KV 要求が続きます。

### TiDB の主要なメトリックとクラスター リソースの使用率 {#tidb-key-metrics-and-cluster-resource-utilization}

#### 1 秒あたりのクエリ、1 秒あたりのコマンド、Prepared-Plan-Cache {#query-per-second-command-per-second-and-prepared-plan-cache}

パフォーマンスの概要で次の 3 つのパネルを確認することで、アプリケーションのワークロードの種類、アプリケーションが TiDB と対話する方法、およびアプリケーションが TiDB [準備済みプラン キャッシュ](/sql-prepared-plan-cache.md)十分に活用しているかどうかを知ることができます。

-   QPS: Query Per Second の略。アプリケーションによって実行された SQL ステートメントの数を示します。
-   タイプ別 CPS: Command Per Second の略。 Command は、MySQL プロトコル固有のコマンドを示します。クエリ ステートメントは、クエリ コマンドまたはプリペアドステートメントのいずれかによって TiDB に送信できます。
-   プラン キャッシュを使用するクエリ OPS: `avg-hit`は、TiDB クラスターで 1 秒あたりの実行プラン キャッシュを使用するクエリの数であり、 `avg-miss`は、TiDB クラスターで 1 秒あたりの実行プラン キャッシュを使用しないクエリの数です。

    `avg-hit + avg-miss`は`StmtExecute`に等しく、これは 1 秒あたりに実行されるすべてのクエリの数です。準備済みプラン キャッシュが TiDB で有効になっている場合、次の 3 つのシナリオが発生します。

    -   準備されたプラン キャッシュはヒットしません。1 ( `avg-hit`秒あたりのヒット数) は 0 であり、 `avg-miss`秒あたり`StmtExecute`コマンドの数に等しくなります。考えられる理由は次のとおりです。
        -   アプリケーションはクエリ インターフェイスを使用しています。
        -   アプリケーションは`StmtExecute`回実行するたびに`StmtClose`コマンドを呼び出すため、キャッシュされたプランはクリーンアップされます。
        -   `StmtExecute`によって実行されたすべてのステートメントは[キャッシュ条件](/sql-prepared-plan-cache.md)を満たしていないため、実行プランのキャッシュにヒットできません。
    -   準備されたすべてのプラン キャッシュがヒットします。1 ( `avg-hit`秒あたりのヒット数) は 1 秒あたりの`StmtExecute`コマンドの数に等しく、 `avg-miss` (1 秒あたりのヒットなしの数) は 0 です。
    -   一部の準備済みプラン キャッシュがヒットします。1 ( `avg-hit`秒あたりのヒット数) は、1 秒あたりの`StmtExecute`コマンドの数よりも少なくなります。準備済みプラン キャッシュには既知の制限があります。たとえば、サブクエリはサポートされていないため、サブクエリを含む SQL ステートメントでは準備済みプラン キャッシュを使用できません。

**例 1: TPC-C ワークロード**

TPC-C ワークロードは、主に`UPDATE` 、 `SELECT` 、および`INSERT`ステートメントです。合計 QPS は 1 秒あたり`StmtExecute`コマンドの数に等しく、後者は Plan Cache OPS パネルを使用したクエリで`avg-hit`にほぼ等しくなります。理想的には、クライアントはプリペアドステートメントのオブジェクトをキャッシュします。このように、SQL ステートメントが実行されると、キャッシュされたステートメントが直接呼び出されます。すべての SQL 実行は準備されたプラン キャッシュにヒットし、実行プランを生成するために再コンパイルする必要はありません。

![TPC-C](/media/performance/tpcc_qps.png)

**例 2: 読み取り専用の OLTP ワークロードでクエリ コマンドに使用できない準備済みプラン キャッシュ**

このワークロードでは、 `Commit QPS` = `Rollback QPS` = `Select QPS`です。アプリケーションは自動コミット同時実行を有効にしており、接続が接続プールからフェッチされるたびにロールバックが実行されます。その結果、これら 3 つのステートメントは同じ回数実行されます。

![OLTP-Query](/media/performance/oltp_long_compile_qps.png)

-   QPS パネルの赤い太線は失敗したクエリを表し、右側の Y 軸は失敗したクエリの数を示します。 0 以外の値は、失敗したクエリが存在することを意味します。
-   合計 QPS は、CPS By Type パネルのクエリ数と等しく、クエリ コマンドはアプリケーションによって使用されています。
-   プラン キャッシュを使用したクエリ OPS パネルにはデータがありません。これは、準備されたプラン キャッシュがクエリ コマンドで使用できないためです。これは、TiDB がクエリ実行ごとに実行計画を解析して生成する必要があることを意味します。その結果、TiDB による CPU 消費の増加に伴い、コンパイル時間が長くなります。

**例 3: 準備済みプリペアドステートメントプラン キャッシュを使用できない**

`StmtPreare`回= `StmtExecute`回= `StmtClose`回~= `StmtFetch`回。アプリケーションは、準備 &gt; 実行 &gt; フェッチ &gt; クローズ ループを使用します。プリペアドステートメントオブジェクトのリークを防ぐために、多くのアプリケーション フレームワークは`execute`フェーズの後に`close`を呼び出します。これにより、2 つの問題が生じます。

-   SQL の実行には、4 つのコマンドと 4 つのネットワーク ラウンド トリップが必要です。
-   プラン キャッシュを使用するクエリ OPS は 0 であり、準備されたプラン キャッシュのヒットがゼロであることを示します。 `StmtClose`コマンドはデフォルトでキャッシュされた実行計画をクリアし、次の`StmtPreare`コマンドは実行計画を再度生成する必要があります。

> **ノート：**
>
> TiDB v6.0.0 以降では、グローバル変数 ( `set global tidb_ignore_prepared_cache_close_stmt=on;` ) を介して`StmtClose`コマンドがキャッシュされた実行プランをクリアするのを防ぐことができます。このようにして、後続の実行は、準備されたプラン キャッシュにヒットする可能性があります。

![OLTP-Prepared](/media/performance/oltp_prepared_statement_no_plan_cache.png)

**例 4: プリペアド ステートメントにリソース リークがある**

1 秒あたり`StmtPrepare`コマンドの数は、1 秒あたり`StmtClose`コマンドよりもはるかに多く、アプリケーションで準備済みステートメントのオブジェクト リークが発生していることを示しています。

![OLTP-Query](/media/performance/prepared_statement_leaking.png)

-   QPS パネルでは、赤い太線が失敗したクエリの数を示し、右側のY軸はその数の座標値を示します。この例では、1 秒あたりの失敗したクエリの数は 74.6 です。
-   CPS By Type パネルでは、1 秒あたり`StmtPrepare`コマンドの数が 1 秒あたり`StmtClose`コマンドよりもはるかに多く、これはプリペアド ステートメントのアプリケーションでオブジェクト リークが発生していることを示しています。
-   プラン キャッシュを使用したクエリ OPS パネルでは、タイプ別の CPS パネルでは`avg-miss`が`StmtExecute`とほぼ等しく、ほとんどすべての SQL 実行で実行プラン キャッシュが失われていることを示しています。

#### ソース別の KV/TSO 要求 OPS および KV 要求時間 {#kv-tso-request-ops-and-kv-request-time-by-source}

-   KV/TSO Request OPS パネルでは、1 秒あたりの KV および TSO 要求の統計を表示できます。統計の中で、 `kv request total` TiDB から TiKV へのすべてのリクエストの合計を表します。 TiDB から PD および TiKV へのリクエストのタイプを観察することで、クラスター内のワークロード プロファイルを把握できます。
-   [KV Request Time By Source] パネルでは、各 KV リクエスト タイプとすべてのリクエスト ソースの時間比率を表示できます。
    -   kv リクエストの合計時間: 1 秒あたりの KV およびTiFlashリクエストの合計処理時間。
    -   各 KV 要求と`external`する要求ソースは積み上げ棒グラフを形成します。1 は通常のビジネス要求を示し、 `internal`内部アクティビティ要求 (DDL やauto analyze要求など) を示します。

**例 1: ビジー ワークロード**

![TPC-C](/media/performance/tpcc_source_sql.png)

この TPC-C ワークロードでは:

-   1 秒あたりの KV リクエストの総数は 79,700 です。上位のリクエスト タイプは、リクエスト数の順に`Prewrite` 、 `Commit` 、 `PessimisticsLock` 、および`BatchGet`です。
-   KV 処理時間のほとんどは`Commit-external_Commit`と`Prewrite-external_Commit`に費やされます。これは、最も時間のかかる KV 要求が外部コミット ステートメントからの`Commit`と`Prewrite`であることを示しています。

**例 2: ワークロードを分析する**

![OLTP](/media/performance/internal_stats.png)

このワークロードでは、クラスターで実行されているステートメントは`ANALYZE`だけです。

-   1 秒あたりの KV リクエストの総数は 35.5 で、1 秒あたりの Cop リクエストの数は 9.3 です。
-   KV 処理時間のほとんどは`Cop-internal_stats`に費やされます。これは、最も時間のかかる KV 要求が内部`ANALYZE`操作からの`Cop`あることを示しています。

#### TiDB CPU、TiKV CPU、および IO 使用率 {#tidb-cpu-tikv-cpu-and-io-usage}

TiDB CPU および TiKV CPU/IO MBps パネルでは、TiDB および TiKV の論理 CPU 使用率と IO スループットを観察できます。これには、平均、最大、デルタ (最大 CPU 使用率から最小 CPU 使用率を差し引いたもの) が含まれます。 TiDB と TiKV の全体的な CPU 使用率。

-   `delta`値に基づいて、TiDB の CPU 使用率が不均衡であるかどうか (通常、アプリケーション接続の不均衡を伴う)、およびクラスター内に読み取り/書き込みのホット スポットがあるかどうかを判断できます。
-   TiDB と TiKV のリソース使用量の概要を使用すると、クラスターにリソースのボトルネックがあるかどうか、および TiKV または TiDB にスケールアウトが必要かどうかをすばやく判断できます。

**例 1: TiDB リソースの使用率が高い**

このワークロードでは、TiDB と TiKV はそれぞれ 8 個の CPU で構成されています。

![TPC-C](/media/performance/tidb_high_cpu.png)

-   TiDB の平均、最大、デルタ CPU 使用率は、それぞれ 575%、643%、136% です。
-   TiKV の平均、最大、デルタ CPU 使用率は、それぞれ 146%、215%、118% です。 TiKV の平均、最大、デルタ I/O スループットは、それぞれ 9.06 MB/秒、19.7 MB/秒、17.1 MB/秒です。

明らかに、TiDB はより多くの CPU を消費します。これは、ボトルネックのしきい値である 8 CPU に近づいています。 TiDB をスケールアウトすることをお勧めします。

**例 2: TiKV リソースの使用率が高い**

以下の TPC-C ワークロードでは、TiDB と TiKV はそれぞれ 16 個の CPU で構成されています。

![TPC-C](/media/performance/tpcc_cpu_io.png)

-   TiDB の平均、最大、デルタ CPU 使用率は、それぞれ 883%、962%、153% です。
-   TiKV の平均、最大、デルタ CPU 使用率は、それぞれ 1288%、1360%、126% です。 TiKV の平均、最大、デルタ I/O スループットは、それぞれ 130 MB/秒、153 MB/秒、53.7 MB/秒です。

明らかに、TiKV はより多くの CPU を消費します。これは、TPC-C が書き込みの多いシナリオであるためです。パフォーマンスを向上させるために、TiKV をスケールアウトすることをお勧めします。

### クエリレイテンシーの内訳と主要なレイテンシーメトリック {#query-latency-breakdown-and-key-latency-metrics}

レイテンシーパネルには、平均値と 99 パーセンタイルが表示されます。平均値は全体的なボトルネックを特定するのに役立ちますが、99 パーセンタイルまたは 999 パーセンタイルまたは 999 番目の値は、重大なレイテンシージッターがあるかどうかを判断するのに役立ちます。

#### 期間、接続アイドル期間、および接続数 {#duration-connection-idle-duration-and-connection-count}

[期間] パネルには、すべてのステートメントの平均および P99レイテンシーと、各 SQL タイプの平均レイテンシーが含まれています。 Connection Idle Duration パネルには、平均および P99 接続アイドル時間が含まれています。接続のアイドル期間には、次の 2 つの状態が含まれます。

-   in-txn: 接続がトランザクション内にある場合に、前の SQL を処理してから次の SQL ステートメントを受信するまでの間隔。
-   not-in-txn: 接続がトランザクション内にない場合に、前の SQL を処理してから次の SQL ステートメントを受信するまでの間隔。

アプリケーションは、同じデータベース接続でトランザクションを実行します。クエリの平均レイテンシーと接続のアイドル時間を比較することで、TiDB がシステム全体のボトルネックになっているかどうか、またはユーザー応答時間のジッターが TiDB によって引き起こされているかどうかを判断できます。

-   アプリケーションのワークロードが読み取り専用ではなく、トランザクションが含まれている場合、クエリの平均レイテンシーを`avg-in-txn`と比較することで、データベース内外でトランザクションを処理する割合を判断し、ユーザー応答時間のボトルネックを特定できます。
-   アプリケーションのワークロードが読み取り専用であるか、自動コミット モードがオンの場合、平均クエリレイテンシーを`avg-not-in-txn`と比較できます。

実際の顧客のシナリオでは、ボトルネックがデータベースの外部にあることは珍しくありません。たとえば、次のようになります。

-   クライアントサーバーの構成が低すぎて、CPU リソースが使い果たされています。
-   HAProxy は TiDB クラスター プロキシとして使用され、HAProxy の CPU リソースが使い果たされます。
-   HAProxy は TiDB クラスター プロキシとして使用され、ワークロードが高いと HAProxyサーバーのネットワーク帯域幅が使い果たされます。
-   アプリケーションサーバーからデータベースへのネットワークレイテンシーが高い。たとえば、パブリック クラウドの展開では、アプリケーションと TiDB クラスターが同じリージョンにないか、dns ワークロード バランサーと TiDB クラスターが同じリージョンにないため、ネットワークレイテンシーが高くなります。
-   ボトルネックはクライアント アプリケーションにあります。アプリケーション サーバーの CPU コアと Numa リソースを十分に活用できません。たとえば、TiDB への何千もの JDBC 接続を確立するために、1 つの JVM だけが使用されます。

[接続数] パネルでは、合計接続数と各 TiDB ノードの接続数を確認できます。これにより、合計接続数が正常かどうか、および各 TiDB ノードの接続数が偏っているかどうかを判断できます。 `active connections`アクティブな接続の数を示します。これは、1 秒あたりのデータベース時間と同じです。右側のY軸 ( `disconnection/s` ) は、クラスター内の 1 秒あたりの切断数を示します。これは、アプリケーションが短い接続を使用しているかどうかを判断するために使用できます。

**例 1: 切断数/秒が多すぎる**

![high disconnection/s](/media/performance/high_disconnections.png)

このワークロードでは:

-   すべての SQL ステートメントの平均レイテンシーと P99レイテンシーは、それぞれ 10.8 ミリ秒と 84.1 ミリ秒です。
-   トランザクション`avg-in-txn`の平均接続アイドル時間は 9.4 ミリ秒です。
-   クラスターへの合計接続数は 3,700 で、各 TiDB ノードへの接続数は 1,800 です。アクティブな接続の平均数は 40.3 で、ほとんどの接続がアイドル状態であることを示しています。 `disonnnection/s`の平均数は 55.8 で、アプリケーションが頻繁に接続と切断を行っていることを示しています。短い接続の動作は、TiDB リソースと応答時間に一定の影響を与えます。

**例 2: TiDB がユーザー応答時間のボトルネックになっている**

![TiDB is the Bottleneck](/media/performance/tpcc_duration_idle.png)

この TPC-C ワークロードでは:

-   すべての SQL ステートメントの平均レイテンシーと P99レイテンシーは、それぞれ 477 us と 3.13 ms です。 commit ステートメント、insert ステートメント、query ステートメントの平均レイテンシは、それぞれ 2.02 ms、609 us、468 us です。
-   トランザクション`avg-in-txn`の平均接続アイドル時間は 171 us です。

平均クエリレイテンシーは`avg-in-txn`を大幅に上回っています。これは、トランザクションの主なボトルネックがデータベース内にあることを意味します。

**例 3: TiDB はユーザー応答時間のボトルネックではない**

![TiDB is not Bottleneck](/media/performance/cloud_query_long_idle.png)

このワークロードでは、平均クエリレイテンシーは 1.69 ミリ秒で、 `avg-in-txn`は 18 ミリ秒です。これは、TiDB がトランザクションで SQL ステートメントを処理するために平均 1.69 ミリ秒を費やし、次のステートメントを受信するために 18 ミリ秒待機する必要があることを示しています。

クエリの平均レイテンシーは`avg-in-txn`よりも大幅に低くなっています。ユーザー応答時間のボトルネックは TiDB にはありません。この例はパブリック クラウド環境にあります。この環境では、アプリケーションとデータベースが同じリージョンにないため、アプリケーションとデータベース間のネットワークレイテンシー時間が長くなり、接続のアイドル時間が非常に長くなります。

#### 解析、コンパイル、および実行時間 {#parse-compile-and-execute-duration}

TiDB では、クエリ ステートメントを送信してから結果を返すまでが[典型的な処理の流れ](/sql-optimization-concepts.md)です。

TiDB での SQL 処理は、 `get token` 、 `parse` 、 `compile` 、および`execute`の 4 つのフェーズで構成されます。

-   `get token` : 通常は数マイクロ秒であり、無視できます。トークンは、1 つの TiDB インスタンスへの接続数が[トークン制限](/tidb-configuration-file.md)制限に達した場合にのみ制限されます。
-   `parse` : クエリ ステートメントは抽象構文ツリー (AST) に解析されます。
-   `compile` : 実行計画は、 `parse`フェーズの AST と統計に基づいてコンパイルされます。 `compile`フェーズには、論理最適化と物理最適化が含まれます。論理最適化は、関係代数に基づく列の刈り込みなどのルールによってクエリ プランを最適化します。物理的最適化は、コストベースのオプティマイザーによる統計によって実行計画のコストを見積もり、コストが最も低い物理的な実行計画を選択します。
-   `execute` : SQL ステートメントの実行にかかる時間。 TiDB はまず、グローバルに一意のタイムスタンプ TSO を待ちます。次に、エグゼキュータは、実行計画のオペレータのキー範囲に基づいて TiKV API リクエストを構築し、それを TiKV に配布します。 `execute`時間には、TSO 待機時間、KV 要求時間、および TiDB エグゼキューターがデータの処理に費やした時間が含まれます。

アプリケーションが`query`または`StmtExecute` MySQL コマンド インターフェイスのみを使用する場合、次の式を使用して、平均レイテンシーのボトルネックを特定できます。

```
avg Query Duration = avg Get Token + avg Parse Duration + avg Compile Duration + avg Execute Duration
```

通常、 `execute`フェーズは`query`のレイテンシーの大部分を占めます。ただし、次の場合には、第`parse`と`compile`フェーズも大きな役割を果たします。

-   `parse`フェーズのレイテンシーが長い: たとえば、 `query`ステートメントが長い場合、SQL テキストを解析するために多くの CPU が消費されます。
-   第`compile`フェーズでの長いレイテンシー: 準備されたプラン キャッシュがヒットしない場合、TiDB は SQL 実行ごとに実行プランをコンパイルする必要があります。 `compile`フェーズのレイテンシーは、数ミリ秒または数十ミリ秒、あるいはそれ以上になる可能性があります。準備されたプラン キャッシュがヒットしない場合、 `compile`フェーズで論理的および物理的な最適化が行われ、多くの CPU とメモリが消費され、Go ランタイム (TiDB は[`Go`](https://go.dev/)で記述されます) が圧迫され、他の TiDB コンポーネントのパフォーマンスに影響を与えます。準備されたプラン キャッシュは、TiDB で OLTP ワークロードを効率的に処理するために重要です。

**例 1: `compile`段階でのデータベースのボトルネック**

![Compile](/media/performance/long_compile.png)

前の図では、 `parse` 、 `compile` 、および`execute`フェーズの平均時間は、それぞれ 17.1 us、729 us、および 681 us です。アプリケーションは`query`コマンド インターフェイスを使用し、準備されたプラン キャッシュを使用できないため、 `compile`レイテンシーは高くなります。

**例 2: `execute`フェーズでのデータベースのボトルネック**

![Execute](/media/performance/long_execute.png)

この TPC-C ワークロードでは、 `parse` `compile`および`execute`フェーズの平均時間は、それぞれ 7.39 us、38.1 us、および 12.8 ms です。 `execute`フェーズは`query`レイテンシーのボトルネックです。

#### KV および TSO 要求期間 {#kv-and-tso-request-duration}

TiDB は、 `execute`フェーズで PD および TiKV と相互作用します。次の図に示すように、SQL 要求を処理する場合、TiDB は`parse`フェーズと`compile`フェーズに入る前に TSO を要求します。 PD クライアントは呼び出し元をブロックしませんが、 `TSFuture`を返し、バックグラウンドで TSO 要求を非同期的に送受信します。 PD クライアントが TSO 要求の処理を完了すると、 `TSFuture`が返されます。 `TSFuture`の所有者は、Wait メソッドを呼び出して最終的な TSO を取得する必要があります。 TiDB が`parse`および`compile`フェーズを終了すると、次の 2 つの状況が発生する可能性がある`execute`フェーズに入ります。

-   TSO 要求が完了すると、Wait メソッドはすぐに使用可能な TSO またはエラーを返します。
-   TSO 要求がまだ完了していない場合、TSO が使用可能になるかエラーが表示されるまで、Wait メソッドはブロックされます (gRPC 要求は送信されましたが、結果が返されず、ネットワークのレイテンシーが長くなります)。

TSO 待機時間は`TSO WAIT`として記録され、TSO 要求のネットワーク時間は`TSO RPC`として記録されます。 TSO 待機が完了すると、TiDB エグゼキューターは通常、読み取りまたは書き込み要求を TiKV に送信します。

-   一般的な KV 読み取り要求: `Get` 、 `BatchGet` 、および`Cop`
-   一般的な KV 書き込み要求: 2 フェーズ コミットの場合は`PessimisticLock` 、 `Prewrite`および`Commit`

![Execute](/media/performance/execute_phase.png)

このセクションのインジケーターは、次の 3 つのパネルに対応しています。

-   Avg TiDB KV Request Duration: TiDB によって測定された KV リクエストの平均レイテンシー
-   Avg TiKV GRPC Duration: TiKV で gPRC メッセージを処理する際の平均レイテンシー
-   PD TSO 待機/RPC 期間: TiDB エグゼキューター TSO 待機時間と TSO 要求 (RPC) のネットワークレイテンシー

`Avg TiDB KV Request Duration`と`Avg TiKV GRPC Duration`の関係は次のとおりです。

```
Avg TiDB KV Request Duration = Avg TiKV GRPC Duration + Network latency between TiDB and TiKV + TiKV gRPC processing time + TiDB gRPC processing time and scheduling latency
```

`Avg TiDB KV Request Duration`と`Avg TiKV GRPC Duration`の違いは、TiDB と TiKV によるネットワーク トラフィック、ネットワークレイテンシー、およびリソースの使用に密接に関連しています。

-   同じデータセンター内: 通常、差は 2 ミリ秒未満です。
-   同じリージョン内の異なるアベイラビリティ ゾーン: 通常、差は 5 ミリ秒未満です。

**例 1: 同じデータセンターにデプロイされたクラスターの低ワークロード**

![Same Data Center](/media/performance/oltp_kv_tso.png)

このワークロードでは、TiDB の平均`Prewrite`レイテンシーは 925 us で、TiKV 内の平均`kv_prewrite`処理レイテンシーは 720 us です。その差は約 200 us で、これは同じデータセンターでは正常です。平均 TSOレイテンシーは206 us で、RPC 時間は 144 us です。

**例 2: パブリック クラウド クラスターでの通常のワークロード**

![Cloud Env ](/media/performance/cloud_kv_tso.png)

この例では、TiDB クラスターは同じリージョン内の異なるデータ センターにデプロイされています。 TiDB の平均`commit`レイテンシーは 12.7 ミリ秒、TiKV 内部の平均`kv_commit`処理レイテンシーは10.2 ミリ秒で、約 2.5 ミリ秒の差があります。平均 TSO 待機レイテンシーは 3.12 ミリ秒で、RPC 時間は 693 ミリ秒です。

**例 3: パブリック クラウド クラスターで過負荷になっているリソース**

![Cloud Env, TiDB Overloaded](/media/performance/cloud_kv_tso_overloaded.png)

この例では、TiDB クラスターは同じリージョン内の異なるデータ センターにデプロイされており、TiDB ネットワークと CPU リソースは非常に過負荷になっています。 TiDB の平均`BatchGet`レイテンシーは 38.6 ミリ秒で、TiKV 内の平均`kv_batch_get`処理レイテンシーは6.15 ミリ秒です。その差は 32 ミリ秒以上あり、通常の値よりもはるかに高くなっています。平均 TSO 待機レイテンシーは 9.45 ミリ秒で、RPC 時間は 14.3 ミリ秒です。

#### ストレージの非同期書き込み期間、保存期間、および適用期間 {#storage-async-write-duration-store-duration-and-apply-duration}

TiKV は、次の手順で書き込み要求を処理します。

-   `scheduler worker`書き込み要求を処理し、トランザクションの整合性チェックを実行し、書き込み要求をキーと値のペアに変換して`raftstore`モジュールに送信します。
-   TiKV コンセンサス モジュール`raftstore` 、 Raftコンセンサス アルゴリズムを適用して、storageレイヤー(複数の TiKV で構成される) をフォールト トレラントにします。

    Raftstore は`Store`スレッドと`Apply`スレッドで構成されます。

    -   `Store`スレッドはRaftメッセージと新しい`proposals`を処理します。新しい`proposals`を受信すると、リーダー ノードの`Store`スレッドがローカルのRaft DB に書き込み、メッセージを複数のフォロワー ノードにコピーします。この`proposals`がほとんどのインスタンスで正常に永続化されると、 `proposals`正常にコミットされます。
    -   `Apply`スレッドは、コミットされた`proposals` KV DB に書き込みます。コンテンツが KV DB に正常に書き込まれると、 `Apply`スレッドは書き込み要求が完了したことを外部に通知します。

![TiKV Write](/media/performance/store_apply.png)

`Storage Async Write Duration`メトリクスは、書き込みリクエストが raftstore に入った後のレイテンシーを記録します。データはリクエストごとに収集されます。

`Storage Async Write Duration`メトリックには`Store Duration`と`Apply Duration` 2 つの部分が含まれます。次の式を使用して、書き込み要求のボトルネックが`Store`または`Apply`のステップにあるかどうかを判断できます。

```
avg Storage Async Write Duration = avg Store Duration + avg Apply Duration
```

> **ノート：**
>
> `Store Duration`と`Apply Duration`は v5.3.0 以降でサポートされています。

**例 1: v5.3.0 と v5.4.0 での同じ OLTP ワークロードの比較**

前の式によると、v5.4.0 の書き込みが多い OLTP ワークロードの QPS は、v5.3.0 よりも 14% 高くなります。

-   v5.3.0: 24.4 ミリ秒 ~= 17.7 ミリ秒 + 6.59 ミリ秒
-   v5.4.0: 21.4 ミリ秒 ~= 14.0 ミリ秒 + 7.33 ミリ秒

v5.4.0 では、gPRC モジュールがRaftログ レプリケーションを高速化するように最適化されており、v5.3.0 と比較して`Store Duration`減少しています。

v5.3.0:

![v5.3.0](/media/performance/v5.3.0_store_apply.png)

v5.4.0:

![v5.4.0](/media/performance/v5.4.0_store_apply.png)

**例 2: 保存期間がボトルネック**

前の式を適用します: 10.1 ミリ秒 ~= 9.81 ミリ秒 + 0.304 ミリ秒。この結果は、書き込みリクエストのレイテンシーのボトルネックが`Store Duration`であることを示しています。

![Store](/media/performance/cloud_store_apply.png)

#### コミット ログ期間、追加ログ期間、および適用ログ期間 {#commit-log-duration-append-log-duration-and-apply-log-duration}

`Commit Log Duration` 、 `Append Log Duration` 、および`Apply Log Duration` 、raftstore 内の主要な操作のレイテンシーメトリックです。これらのレイテンシーはバッチ操作レベルでキャプチャされ、各操作は複数の書き込み要求を組み合わせます。したがって、レイテンシは上記の`Store Duration`と`Apply Duration`に直接対応しません。

-   `Store`スレッドで実行された操作の`Commit Log Duration`および`Append Log Duration`記録時間。 `Commit Log Duration` 、 Raftログを他の TiKV ノードにコピーする時間が含まれています (raft-log の永続性を確保するため)。 `Commit Log Duration`は通常、リーダー用とフォロワー用の 2 つの`Append Log Duration`操作が含まれます。 `Commit Log Duration`は通常`Append Log Duration`よりも大幅に高くなります。これは、前者にはRaftログをネットワーク経由で他の TiKV ノードにコピーする時間が含まれているためです。
-   `Apply Log Duration` `Apply`のスレッドによる`apply` Raftログのレイテンシーを記録します。

`Commit Log Duration`が長い一般的なシナリオ:

-   TiKV の CPU リソースにボトルネックがあり、スケジューリングのレイテンシーが高い
-   `raftstore.store-pool-size`は小さすぎるか大きすぎる (大きすぎる値もパフォーマンスの低下を引き起こす可能性があります)
-   I/Oレイテンシーが高いため、 `Append Log Duration`レイテンシーが高くなります
-   TiKV ノード間のネットワークレイテンシーが大きい
-   gRPC スレッドの数が少なすぎます。CPU 使用率は GRPC スレッド間で不均一です。

`Apply Log Duration`が長い一般的なシナリオ:

-   TiKV の CPU リソースにボトルネックがあり、スケジューリングのレイテンシーが高い
-   `raftstore.apply-pool-size`は小さすぎるか大きすぎる (大きすぎる値もパフォーマンスの低下を引き起こす可能性があります)
-   I/Oレイテンシーが高い

**例 1: v5.3.0 と v5.4.0 での同じ OLTP ワークロードの比較**

v5.4.0 の書き込み負荷の高い OLTP ワークロードの QPS は、v5.3.0 と比較して 14% 向上しています。次の表は、3 つの主要なレイテンシを比較したものです。

| 平均継続時間     | v5.3.0 (ミリ秒) | v5.4.0 (ミリ秒) |
| :--------- | :----------- | :----------- |
| ログ期間の追加    | 0.27         | 0.303        |
| コミット ログの期間 | 13           | 8.68         |
| ログ期間の適用    | 0.457        | 0.514        |

v5.4.0 では、gPRC モジュールがRaftログ レプリケーションを高速化するように最適化されており、v5.3.0 と比較して`Commit Log Duration`と`Store Duration`が減少しています。

v5.3.0:

![v5.3.0](/media/performance/v5.3.0_commit_append_apply.png)

v5.4.0:

![v5.4.0](/media/performance/v5.4.0_commit_append_apply.png)

**例 2: コミット ログの期間がボトルネックである**

![Store](/media/performance/cloud_append_commit_apply.png)

-   平均`Append Log Duration` = 4.38 ミリ秒
-   平均`Commit Log Duration` = 7.92 ミリ秒
-   平均`Apply Log Duration` = 172 us

`Store`スレッドの場合、 `Commit Log Duration`は明らかに`Apply Log Duration`よりも高くなります。一方、 `Append Log Duration`は`Apply Log Duration`よりも大幅に高く、 `Store`スレッドが CPU と I/O の両方でボトルネックに悩まされている可能性があることを示しています。 `Commit Log Duration`と`Append Log Duration`減らすには、次の方法が考えられます。

-   TiKV CPU リソースが十分な場合は、 `raftstore.store-pool-size`の値を増やして`Store`スレッドを追加することを検討してください。
-   TiDB が v5.4.0 以降の場合は、 `raft-engine.enable: true`を設定して[`Raft Engine`](/tikv-configuration-file.md#raft-engine)を有効にすることを検討してください。 Raft Engine には軽い実行パスがあります。これにより、一部のシナリオでは、I/O 書き込みと書き込みのロングテールレイテンシーを削減できます。
-   TiKV の CPU リソースが十分にあり、TiDB が v5.3.0 以降の場合は、 `raftstore.store-io-pool-size: 1`を設定して[`StoreWriter`](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を有効にすることを検討してください。

## TiDB のバージョンが v6.1.0 より前の場合、Performance Overview ダッシュボードを使用するにはどうすればよいですか? {#if-my-tidb-version-is-earlier-than-v6-1-0-what-should-i-do-to-use-the-performance-overview-dashboard}

v6.1.0 以降、Grafana にはデフォルトでパフォーマンス概要ダッシュボードが組み込まれています。このダッシュボードは、TiDB v4.x および v5.x バージョンと互換性があります。 TiDB が v6.1.0 より前の場合は、次の図に示すように、手動で[`performance_overview.json`](https://github.com/pingcap/tidb/blob/master/metrics/grafana/performance_overview.json)をインポートする必要があります。

![Store](/media/performance/import_dashboard.png)
