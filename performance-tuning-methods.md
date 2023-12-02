---
title: Performance Analysis and Tuning
summary: Learn how to optimize database system based on database time and how to utilize the TiDB Performance Overview dashboard for performance analysis and tuning.
---

# パフォーマンスの分析とチューニング {#performance-analysis-and-tuning}

このドキュメントでは、データベース時間ごとのチューニング手法について説明し、パフォーマンス分析とチューニングに TiDB [パフォーマンス概要ダッシュボード](/grafana-performance-overview-dashboard.md)を使用する方法を示します。

このドキュメントで説明する方法を使用すると、ユーザー応答時間とデータベース時間をグローバルかつトップダウンの観点から分析し、ユーザー応答時間のボトルネックがデータベースの問題によって引き起こされているかどうかを確認できます。ボトルネックがデータベースにある場合は、データベース時間の概要と SQLレイテンシーの内訳を使用してボトルネックを特定し、パフォーマンスを調整できます。

## データベース時間に基づいたパフォーマンスのチューニング {#performance-tuning-based-on-database-time}

TiDB は、SQL 処理パスとデータベース時間を常に測定および収集しています。したがって、TiDB のデータベース パフォーマンスのボトルネックを簡単に特定できます。データベース時間のメトリクスに基づいて、ユーザーの応答時間に関するデータがなくても、次の 2 つの目標を達成できます。

-   平均 SQL 処理レイテンシーとトランザクション内の TiDB 接続のアイドル時間を比較することで、ボトルネックが TiDB にあるかどうかを判断します。
-   ボトルネックが TiDB にある場合は、データベース時間の概要、色ベースのパフォーマンス データ、主要なメトリクス、リソース使用率、およびトップレイテンシーの遅延の内訳に基づいて、分散システム内の正確なモジュールをさらに特定します。

### TiDB がボトルネックですか? {#is-tidb-the-bottleneck}

-   トランザクション内の TiDB 接続の平均アイドル時間が平均 SQL 処理レイテンシーよりも高い場合、データベースはアプリケーションのトランザクションレイテンシーの原因ではありません。データベース時間はユーザー応答時間のごく一部のみを占めており、ボトルネックがデータベースの外側にあることを示しています。

    この場合、データベースの外部コンポーネントを確認してください。たとえば、アプリケーションサーバーに十分なハードウェア リソースがあるかどうか、およびアプリケーションからデータベースまでのネットワークレイテンシーが過度に大きいかどうかを判断します。

-   平均 SQL 処理レイテンシーがトランザクション内の TiDB 接続の平均アイドル時間よりも高い場合、トランザクションのボトルネックは TiDB にあり、データベース時間がユーザー応答時間の大部分を占めています。

### ボトルネックが TiDB にある場合、それを特定するにはどうすればよいでしょうか? {#if-the-bottleneck-is-in-tidb-how-to-identify-it}

次の図は、一般的な SQL プロセスを示しています。ほとんどの SQL 処理パスが TiDB パフォーマンス メトリックでカバーされていることがわかります。データベース時間はさまざまな次元に分類され、それに応じて色分けされます。ワークロードの特性をすぐに理解し、データベース内にボトルネックがある場合はそれを捕捉できます。

![database time decomposition chart](/media/performance/dashboard-diagnostics-time-relation.png)

データベース時間は、すべての SQL 処理時間の合計です。データベース時間を次の 3 つの次元に分類すると、TiDB のボトルネックを迅速に特定するのに役立ちます。

-   SQL 処理タイプ別: どのタイプの SQL ステートメントが最もデータベース時間を消費するかを判断します。式は次のとおりです。

    `DB Time = Select Time + Insert Time + Update Time + Delete Time + Commit Time + ...`

-   SQL 処理の 4 つのステップ (get_token/parse/compile/execute) によって、どのステップが最も時間を消費するかを判断します。式は次のとおりです。

    `DB Time = Get Token Time + Parse Time + Compile Time + Execute Time`

-   実行時間、TSO 待機時間、KV 要求時間、および実行再試行時間によって: どの実行ステップがボトルネックになっているかを判断します。式は次のとおりです。

    `Execute Time ~= TiDB Executor Time + KV Request Time + PD TSO Wait Time + Retried execution time`

## パフォーマンス概要ダッシュボードを使用したパフォーマンス分析とチューニング {#performance-analysis-and-tuning-using-the-performance-overview-dashboard}

このセクションでは、Grafana のパフォーマンス概要ダッシュボードを使用して、データベース時間に基づいてパフォーマンス分析とチューニングを実行する方法について説明します。

パフォーマンス概要ダッシュボードは、TiDB、PD、および TiKV のメトリクスを調整し、次のセクションにそれぞれのメトリクスを表示します。

-   データベース時間と SQL 実行時間の概要: 色分けされた SQL タイプ、SQL 実行フェーズ別のデータベース時間、さまざまなリクエストのデータベース時間により、データベースのワークロードの特性とパフォーマンスのボトルネックを迅速に特定できます。
-   主要なメトリクスとリソース使用率: データベース QPS、接続情報、アプリケーションとデータベース間のリクエスト コマンド タイプ、データベース内部 TSO および KV リクエスト OPS、TiDB/TiKV リソース使用率が含まれます。
-   トップダウンレイテンシーの内訳: クエリレイテンシーと接続アイドル時間の比較、クエリレイテンシーの内訳、SQL 実行における TSO リクエストと KV リクエストのレイテンシー、TiKV 内部書き込みレイテンシーの内訳が含まれます。

### データベース時間と SQL 実行時間の概要 {#database-time-and-sql-execution-time-overview}

データベース時間メトリックは、TiDB が 1 秒あたりに SQL を処理するレイテンシーの合計であり、TiDB が 1 秒あたりにアプリケーション SQL リクエストを同時に処理する合計時間でもあります (アクティブな接続の数に等しい)。

パフォーマンス概要ダッシュボードには、次の 3 つの積み上げ面グラフが表示されます。これらは、データベースのワークロード プロファイルを理解し、SQL 実行中のステートメント、SQL フェーズ、TiKV または PD リクエスト タイプの観点からボトルネックの原因を迅速に特定するのに役立ちます。

-   SQL タイプ別のデータベース時間
-   SQLフェーズごとのデータベース時間
-   SQL実行時間の概要

#### 色で調整する {#tune-by-color}

データベース時間の内訳と実行時間の概要を示す図は、予想される時間消費と予想外の時間消費の両方を直感的に示します。したがって、パフォーマンスのボトルネックを迅速に特定し、ワークロード プロファイルを把握できます。緑と青の領域は、通常の時間消費とリクエストを表します。これら 2 つの図で非緑または非青の領域が大きな割合を占めている場合、データベースの時間分布は不適切です。

-   SQL タイプ別のデータベース時間:

    -   青: `Select`ステートメント
    -   緑: `Update` 、 `Insert` 、 `Commit`およびその他の DML ステートメント
    -   赤: 一般的な SQL タイプ ( `StmtPrepare` 、 `StmtReset` 、 `StmtFetch` 、および`StmtClose`を含む)

-   SQL フェーズ別のデータベース時間: 通常、SQL 実行フェーズは緑色で、その他のフェーズは赤色で表示されます。緑色以外の領域が大きい場合は、実行フェーズ以外のフェーズで多くのデータベース時間が消費されていることを意味し、さらなる原因分析が必要になります。一般的なシナリオは、準備されたプラン キャッシュが利用できないために、オレンジ色で示されているコンパイル フェーズで大きな領域が必要になるというものです。

-   SQL 実行時間の概要: 緑色のメトリックは一般的な KV 書き込みリクエスト ( `Prewrite`や`Commit`など) を表し、青色のメトリックは一般的な KV 読み取りリクエスト (Cop や Get など) を表し、紫のメトリックはTiFlash MPP リクエストを表し、その他の色のメトリックは注意が必要な予期せぬ事態に備えてください。たとえば、悲観的ロック KV 要求は赤でマークされ、TSO 待機は濃い茶色でマークされます。青以外または緑以外の領域が大きい場合は、SQL 実行中にボトルネックがあることを意味します。例えば：

    -   深刻なロック競合が発生した場合、赤い領域が大きな割合を占めます。
    -   TSO の待機に時間がかかりすぎると、濃い茶色の領域の割合が大きくなります。

**例 1: TPC-C ワークロード**

![TPC-C](/media/performance/tpcc_db_time.png)

-   SQL タイプ別のデータベース時間: 最も時間のかかるステートメントは、 `commit` 、 `update` 、 `select` 、および`insert`ステートメントです。
-   SQL フェーズごとのデータベース時間: 最も時間がかかるフェーズは、緑色の SQL 実行です。
-   SQL 実行時間の概要: SQL 実行で最も時間がかかる KV リクエストは緑色の`Prewrite`と`Commit`です。

    > **注記：**
    >
    > KV 要求の合計時間が実行時間よりも長いのは正常です。 TiDB エグゼキュータは KV リクエストを複数の TiKV に同時に送信する可能性があるため、KV リクエストの合計待ち時間が実行時間よりも長くなる場合があります。前述の TPC-C ワークロードでは、トランザクションがコミットされると、TiDB は`Prewrite`と`Commit`リクエストを複数の TiKV に同時に送信します。したがって、この例の`Prewrite` 、 `Commit` 、および`PessimisticsLock`リクエストの合計時間は、明らかに実行時間よりも長くなります。
    >
    > -   `execute`時間は、KV リクエストに`tso_wait`時間を加えた合計時間より大幅に長くなる場合もあります。これは、SQL 実行時間の大部分が TiDB エグゼキュータ内で費やされることを意味します。以下に 2 つの一般的な例を示します。

          > - Example 1: After TiDB executor reads a large amount of data from TiKV, it needs to do complex join and aggregation inside TiDB, which consumes a lot of time.

    <!---->

          > - Example 2: The application experiences serious write statement lock conflicts. Frequent lock retries result in long `Retried execution time`.

**例 2: OLTP 読み取り負荷の高いワークロード**

![OLTP](/media/performance/oltp_normal_db_time.png)

-   SQL タイプ別のデータベース時間: 時間のかかる主なステートメントは`SELECT` 、 `COMMIT` 、 `UPDATE` 、および`INSERT`で、このうち`SELECT`最もデータベース時間を消費します。
-   SQL フェーズごとのデータベース時間: 緑色の`execute`フェーズでほとんどの時間が消費されます。
-   SQL 実行時間の概要: SQL 実行フェーズでは、濃い茶色の`pd tso_wait` 、青色の`KV Get` 、緑色の`Prewrite`と`Commit`に時間がかかります。

**例 3: 読み取り専用の OLTP ワークロード**

![OLTP](/media/performance/oltp_long_compile_db_time.png)

-   SQL タイプ別のデータベース時間: 主に`SELECT`のステートメントです。
-   SQL フェーズごとのデータベース時間: 主な時間のかかるフェーズは、オレンジ色の`compile`と緑色の`execute`フェーズです。 `compile`フェーズのレイテンシが最も高く、TiDB が実行プランを生成するのに時間がかかりすぎるため、その後のパフォーマンス データに基づいて根本原因をさらに特定する必要があることを示しています。
-   SQL 実行時間の概要: 青色の KV BatchGet リクエストは、SQL 実行中に最も多くの時間を消費します。

> **注記：**
>
> 例 3 では、 `SELECT`ステートメントは複数の TiKV から数千行を同時に読み取る必要があります。したがって、 `BatchGet`リクエストの合計時間は実行時間よりもはるかに長くなります。

**例 4: ロック競合のワークロード**

![OLTP](/media/performance/oltp_lock_contention_db_time.png)

-   SQL タイプ別のデータベース時間: 主に`UPDATE`のステートメントです。
-   SQL フェーズ別のデータベース時間: ほとんどの時間は緑色の実行フェーズで消費されます。
-   SQL 実行時間の概要: 赤で示されている KV リクエスト PessimisticLock は SQL 実行中に最も多くの時間を消費し、その実行時間は明らかに KV リクエストの合計時間より長くなります。これは、書き込みステートメントでの深刻なロックの競合と、頻繁なロックの再試行により時間が長くなることが原因で発生します`Retried execution time` 。現在、TiDB は`Retried execution time`を測定しません。

**例 5: HTAP CH ベンチマーク ワークロード**

![HTAP](/media/performance/htap_tiflash_mpp.png)

-   SQL タイプ別のデータベース時間: 主に`SELECT`のステートメントです。
-   SQL フェーズ別のデータベース時間: ほとんどの時間は緑色の実行フェーズで消費されます。
-   SQL 実行時間の概要: 紫色で示されている`tiflash_mpp`リクエストが SQL 実行中に最も多くの時間を消費し、次に青色の`Cop`リクエストを含む KV リクエスト、緑色の`Prewrite`と`Commit`リクエストが続きます。

### TiDB の主要なメトリクスとクラスターのリソース使用率 {#tidb-key-metrics-and-cluster-resource-utilization}

#### 1 秒あたりのクエリ、1 秒あたりのコマンド、および準備済みプラン キャッシュ {#query-per-second-command-per-second-and-prepared-plan-cache}

パフォーマンスの概要で次の 3 つのパネルを確認すると、アプリケーションのワークロード タイプ、アプリケーションが TiDB とどのように対話するか、アプリケーションが TiDB を完全に活用しているかどうかを知ることができます[準備されたプランのキャッシュ](/sql-prepared-plan-cache.md) 。

-   QPS: Query Per Second の略。アプリケーションによって実行された SQL ステートメントの数を示します。
-   CPS By Type: Command Per Second の略。 Command は、MySQL プロトコル固有のコマンドを示します。クエリ ステートメントは、クエリ コマンドまたはプリペアドステートメントのいずれかによって TiDB に送信できます。
-   プラン キャッシュ OPS を使用するクエリ: `avg-hit`は、TiDB クラスター内の 1 秒あたりの実行プラン キャッシュを使用するクエリの数、 `avg-miss`は、TiDB クラスター内の 1 秒あたりの実行プラン キャッシュを使用しないクエリの数です。

    `avg-hit + avg-miss`は`StmtExecute`に等しく、これは 1 秒あたりに実行されるすべてのクエリの数です。 TiDB で準備済みプラン キャッシュが有効になっている場合、次の 3 つのシナリオが発生します。

    -   準備されたプラン キャッシュがヒットしない場合: `avg-hit` (1 秒あたりのヒット数) は 0、3 は`avg-miss`秒あたり`StmtExecute`コマンドの数に等しくなります。考えられる理由は次のとおりです。
        -   アプリケーションはクエリ インターフェイスを使用しています。
        -   アプリケーションは`StmtExecute`回実行するたびに`StmtClose`コマンドを呼び出すため、キャッシュされたプランはクリーンアップされます。
        -   `StmtExecute`によって実行されるすべてのステートメントは[キャッシュ条件](/sql-prepared-plan-cache.md)を満たさないため、実行プラン キャッシュにヒットできません。
    -   準備されたすべてのプラン キャッシュがヒットします。1 ( `avg-hit`秒あたりのヒット数) は 1 秒あたりの`StmtExecute`コマンドの数に等しく、 `avg-miss` (1 秒あたりのヒットなしの数) は 0 です。
    -   準備されたプラン キャッシュの一部がヒットします。1 ( `avg-hit`秒あたりのヒット数) は、1 秒あたりのコマンド数`StmtExecute`よりも少ないです。準備されたプラン キャッシュには既知の制限があります。たとえば、サブクエリはサポートされていないため、サブクエリを含む SQL ステートメントは準備されたプラン キャッシュを使用できません。

**例 1: TPC-C ワークロード**

TPC-C ワークロードは主に`UPDATE` 、 `SELECT` 、および`INSERT`ステートメントです。合計 QPS は 1 秒あたり`StmtExecute`コマンドの数に等しく、後者は [プラン キャッシュ OPS を使用したクエリ] パネルの`avg-hit`にほぼ等しくなります。理想的には、クライアントはプリペアドステートメントのオブジェクトをキャッシュします。このようにして、キャッシュされたステートメントは、SQL ステートメントの実行時に直接呼び出されます。すべての SQL 実行は準備されたプラン キャッシュにヒットするため、実行プランを生成するために再コンパイルする必要はありません。

![TPC-C](/media/performance/tpcc_qps.png)

**例 2: 読み取り専用 OLTP ワークロードでは、準備されたプラン キャッシュがクエリ コマンドに使用できない**

このワークロードでは、 `Commit QPS` = `Rollback QPS` = `Select QPS`です。アプリケーションでは自動コミット同時実行が有効になっており、接続が接続プールからフェッチされるたびにロールバックが実行されます。結果として、これら 3 つのステートメントは同じ回数実行されます。

![OLTP-Query](/media/performance/oltp_long_compile_qps.png)

-   QPS パネルの赤い太線は失敗したクエリを表し、右側の Y 軸は失敗したクエリの数を示します。 0 以外の値は、失敗したクエリが存在することを意味します。
-   合計 QPS は、CPS By Type パネルのクエリの数と等しくなります。クエリ コマンドはアプリケーションによって使用されています。
-   準備されたプラン キャッシュはクエリ コマンドでは使用できないため、[プラン キャッシュを使用したクエリ OPS] パネルにはデータがありません。これは、TiDB がクエリ実行ごとに実行プランを解析して生成する必要があることを意味します。その結果、TiDB による CPU 消費量が増加し、コンパイル時間が長くなります。

**例 3: OLTP ワークロードに対してプリペアドステートメントが有効になっている場合、プリペアド プラン キャッシュは使用できません**

`StmtPreare`回＝ `StmtExecute`回＝ `StmtClose`回～＝ `StmtFetch`回となります。アプリケーションは、準備 &gt; 実行 &gt; フェッチ &gt; 閉じるループを使用します。 プリペアドステートメントオブジェクトのリークを防ぐために、多くのアプリケーション フレームワークは`execute`フェーズの後に`close`を呼び出します。これにより 2 つの問題が生じます。

-   SQL の実行には 4 つのコマンドと 4 つのネットワーク ラウンドトリップが必要です。
-   プラン キャッシュを使用したクエリ OPS は 0 で、準備されたプラン キャッシュのゼロ ヒットを示します。 `StmtClose`コマンドはデフォルトでキャッシュされた実行プランをクリアし、次の`StmtPreare`コマンドは実行プランを再度生成する必要があります。

> **注記：**
>
> TiDB v6.0.0 以降では、 `StmtClose`コマンドがグローバル変数 ( `set global tidb_ignore_prepared_cache_close_stmt=on;` ) を介してキャッシュされた実行プランをクリアしないようにすることができます。このようにして、後続の実行は準備されたプラン キャッシュにヒットする可能性があります。

![OLTP-Prepared](/media/performance/oltp_prepared_statement_no_plan_cache.png)

**例 4: 準備されたステートメントにリソース リークがある**

1 秒あたり`StmtPrepare`コマンドの数は、1 秒あたり`StmtClose`コマンドの数よりもはるかに多く、アプリケーションでプリペアド ステートメントのオブジェクト リークがあることを示しています。

![OLTP-Query](/media/performance/prepared_statement_leaking.png)

-   QPS パネルでは、赤い太線は失敗したクエリの数を示し、右側のY軸はその数値の座標値を示します。この例では、1 秒あたりの失敗したクエリの数は 74.6 です。
-   「CPS By Type」パネルでは、1 秒あたり`StmtPrepare`コマンドの数が`StmtClose`コマンドよりもはるかに多く、プリペアド ステートメントのアプリケーションでオブジェクト リークが発生していることを示しています。
-   [プラン キャッシュを使用したクエリ OPS] パネルでは、 `avg-miss`は [タイプ別 CPS] パネルの`StmtExecute`とほぼ同じです。これは、ほぼすべての SQL 実行が実行プラン キャッシュを見逃していることを示しています。

#### ソースごとの KV/TSO リクエスト OPS および KV リクエスト時間 {#kv-tso-request-ops-and-kv-request-time-by-source}

-   「KV/TSO リクエスト OPS」パネルでは、1 秒あたりの KV リクエストと TSO リクエストの統計を表示できます。統計のうち、 `kv request total` TiDB から TiKV へのすべてのリクエストの合計を表します。 TiDB から PD および TiKV へのリクエストのタイプを観察することで、クラスター内のワークロード プロファイルを把握できます。
-   [ソース別 KV リクエスト時間] パネルでは、各 KV リクエスト タイプとすべてのリクエスト ソースの時間比率を表示できます。
    -   kv リクエストの合計時間: 1 秒あたりの KV リクエストとTiFlashリクエストの合計処理時間。
    -   各 KV リクエストと対応するリクエスト ソースは積み上げ棒グラフを形成します`external`は通常のビジネス リクエストを示し、 `internal`内部アクティビティ リクエスト (DDL やauto analyzeリクエストなど) を示します。

**例 1: 忙しいワークロード**

![TPC-C](/media/performance/tpcc_source_sql.png)

この TPC-C ワークロードでは次のようになります。

-   1 秒あたりの KV リクエストの総数は 79,700 です。上位のリクエスト タイプは、リクエスト数の順に`Prewrite` 、 `Commit` 、 `PessimisticsLock` 、および`BatchGet`です。
-   KV 処理時間のほとんどは`Commit-external_Commit`と`Prewrite-external_Commit`に費やされており、最も時間のかかる KV リクエストは外部コミット ステートメントからの`Commit`と`Prewrite`であることを示しています。

**例 2: ワークロードの分析**

![OLTP](/media/performance/internal_stats.png)

このワークロードでは、クラスター内で実行されているステートメントは`ANALYZE`だけです。

-   1 秒あたりの KV リクエストの総数は 35.5 で、1 秒あたりの Cop リクエストの数は 9.3 です。
-   KV 処理時間のほとんどは`Cop-internal_stats`に費やされており、最も時間のかかる KV リクエストは内部`ANALYZE`の操作のうちの`Cop`であることを示しています。

#### TiDB CPU、TiKV CPU、および IO の使用率 {#tidb-cpu-tikv-cpu-and-io-usage}

TiDB CPU および TiKV CPU/IO MBps パネルでは、TiDB と TiKV の論理 CPU 使用率と IO スループット (平均、最大、デルタ (最大 CPU 使用率から最小 CPU 使用率を引いたもの) を含む）を観察でき、それに基づいて判断できます。 TiDB と TiKV の全体的な CPU 使用率。

-   `delta`値に基づいて、TiDB の CPU 使用率がアンバランスであるかどうか (通常はアプリケーション接続のアンバランスを伴う)、クラスター内に読み取り/書き込みホット スポットがあるかどうかを判断できます。
-   TiDB および TiKV リソースの使用状況の概要を使用すると、クラスター内にリソースのボトルネックがあるかどうか、および TiKV または TiDB のスケールアウトが必要かどうかをすぐに判断できます。

**例 1: TiDB リソースの使用量が多い**

このワークロードでは、各 TiDB と TiKV は 8 個の CPU で構成されています。

![TPC-C](/media/performance/tidb_high_cpu.png)

-   TiDB の平均、最大、デルタ CPU 使用率は、それぞれ 575%、643%、136% です。
-   TiKV の平均、最大、デルタ CPU 使用率は、それぞれ 146%、215%、118% です。 TiKV の平均、最大、デルタ I/O スループットは、それぞれ 9.06 MB/秒、19.7 MB/秒、17.1 MB/秒です。

明らかに、TiDB はより多くの CPU を消費します。これはボトルネックのしきい値である 8 CPU に近い値です。 TiDB をスケールアウトすることをお勧めします。

**例 2: TiKV リソースの使用率が高い**

以下の TPC-C ワークロードでは、各 TiDB と TiKV が 16 個の CPU で構成されています。

![TPC-C](/media/performance/tpcc_cpu_io.png)

-   TiDB の平均 CPU 使用率、最大 CPU 使用率、デルタ CPU 使用率は、それぞれ 883%、962%、153% です。
-   TiKV の平均、最大、デルタ CPU 使用率は、それぞれ 1288%、1360%、126% です。 TiKV の平均、最大、デルタ I/O スループットは、それぞれ 130 MB/秒、153 MB/秒、53.7 MB/秒です。

明らかに、TiKV はより多くの CPU を消費しますが、これは、TPC-C が書き込み負荷の高いシナリオであるため予想されます。パフォーマンスを向上させるために、TiKV をスケールアウトすることをお勧めします。

### クエリレイテンシーの内訳と主要なレイテンシーメトリクス {#query-latency-breakdown-and-key-latency-metrics}

レイテンシーパネルには、平均値と 99 パーセンタイルが表示されます。平均値は全体のボトルネックを特定するのに役立ち、99 パーセンタイルまたは 999 パーセンタイルまたは 999 パーセンタイルは、重大なレイテンシージッターがあるかどうかを判断するのに役立ちます。

#### 期間、接続アイドル期間、および接続数 {#duration-connection-idle-duration-and-connection-count}

[期間] パネルには、すべてのステートメントの平均レイテンシと P99レイテンシー、および各 SQL タイプの平均レイテンシーが含まれています。 [接続アイドル期間] パネルには、平均および P99 接続アイドル期間が含まれています。接続アイドル期間には、次の 2 つの状態が含まれます。

-   in-txn: 接続がトランザクション内にある場合の、前の SQL の処理と次の SQL ステートメントの受信の間の間隔。
-   not-in-txn: 接続がトランザクション内にない場合に、前の SQL を処理してから次の SQL ステートメントを受信するまでの間隔。

アプリケーションは同じデータベース接続を使用してトランザクションを実行します。平均クエリレイテンシー時間と接続アイドル期間を比較することで、TiDB がシステム全体のボトルネックであるかどうか、またはユーザー応答時間のジッターが TiDB によって引き起こされているかどうかを判断できます。

-   アプリケーションのワークロードが読み取り専用ではなく、トランザクションが含まれている場合、平均クエリレイテンシーを`avg-in-txn`と比較することで、データベース内外のトランザクション処理の割合を判断し、ユーザー応答時間のボトルネックを特定できます。
-   アプリケーションのワークロードが読み取り専用であるか、自動コミット モードがオンになっている場合は、平均クエリレイテンシーを`avg-not-in-txn`と比較できます。

実際の顧客のシナリオでは、ボトルネックがデータベースの外側にあることは珍しくありません。たとえば、次のとおりです。

-   クライアントサーバー構成が低すぎるため、CPU リソースが枯渇しています。
-   HAProxy が TiDB クラスター プロキシとして使用されており、HAProxy CPU リソースが枯渇しています。
-   HAProxy は TiDB クラスター プロキシとして使用され、ワー​​クロードが高くなると HAProxyサーバーのネットワーク帯域幅が使い果たされます。
-   アプリケーションサーバーからデータベースまでのネットワークレイテンシーが長くなります。たとえば、パブリック クラウド デプロイメントではアプリケーションと TiDB クラスターが同じリージョンにない、または DNS ワークロード バランサーと TiDB クラスターが同じリージョンにないため、ネットワークレイテンシーが高くなります。
-   ボトルネックはクライアント アプリケーションにあります。アプリケーション サーバーの CPU コアと Numa リソースを十分に活用できません。たとえば、TiDB への数千の JDBC 接続を確立するために、1 つの JVM だけが使用されます。

[接続数] パネルでは、接続の合計数と各 TiDB ノードの接続数を確認できます。これは、接続の合計数が正常かどうか、および各 TiDB ノードの接続数が不均衡かどうかを判断するのに役立ちます。 `active connections`アクティブな接続の数を示し、1 秒あたりのデータベース時間に等しくなります。右側のY軸 ( `disconnection/s` ) は、クラスター内の 1 秒あたりの切断数を示します。これは、アプリケーションが短い接続を使用しているかどうかを判断するために使用できます。

**例 1: 1 秒あたりの切断回数が多すぎる**

![high disconnection/s](/media/performance/high_disconnections.png)

このワークロードでは次のようになります。

-   すべての SQL ステートメントの平均レイテンシーと P99レイテンシーは、それぞれ 10.8 ミリ秒と 84.1 ミリ秒です。
-   トランザクション`avg-in-txn`の平均接続アイドル時間は 9.4 ミリ秒です。
-   クラスターへの接続の総数は 3,700 で、各 TiDB ノードへの接続の数は 1,800 です。アクティブな接続の平均数は 40.3 で、ほとんどの接続がアイドル状態であることを示しています。平均数`disonnnection/s`は 55.8 で、アプリケーションが頻繁に接続と切断を行っていることを示します。短い接続の動作は、TiDB リソースと応答時間に一定の影響を与えます。

**例 2: TiDB がユーザー応答時間のボトルネックになっている**

![TiDB is the Bottleneck](/media/performance/tpcc_duration_idle.png)

この TPC-C ワークロードでは次のようになります。

-   すべての SQL ステートメントの平均レイテンシーと P99レイテンシーは、それぞれ 477 マイクロ秒と 3.13 ミリ秒です。 commit ステートメント、insert ステートメント、query ステートメントの平均レイテンシは、それぞれ 2.02 ミリ秒、609 マイクロ秒、および 468 マイクロ秒です。
-   トランザクション`avg-in-txn`の平均接続アイドル時間は 171 us です。

平均クエリレイテンシーは`avg-in-txn`より大幅に大きく、これはトランザクションの主なボトルネックがデータベース内にあることを意味します。

**例 3: TiDB はユーザー応答時間のボトルネックではない**

![TiDB is not Bottleneck](/media/performance/cloud_query_long_idle.png)

このワークロードでは、平均クエリレイテンシーは 1.69 ミリ秒、 `avg-in-txn`は 18 ミリ秒です。これは、TiDB がトランザクション内の SQL ステートメントの処理に平均 1.69 ミリ秒を費やし、次のステートメントを受信するまでに 18 ミリ秒待つ必要があることを示しています。

平均クエリレイテンシーは`avg-in-txn`より大幅に小さくなります。ユーザー応答時間のボトルネックは TiDB にはありません。この例はパブリック クラウド環境にあります。この環境では、アプリケーションとデータベースが同じリージョンにないため、アプリケーションとデータベース間のネットワークレイテンシーが長くなり、接続アイドル時間が非常に長くなります。

#### 解析、コンパイル、および実行期間 {#parse-compile-and-execute-duration}

TiDB では、クエリ ステートメントの送信から結果が返されるまでは[一般的な処理フロー](/sql-optimization-concepts.md)です。

TiDB における SQL 処理は、 `get token` 、 `parse` 、 `compile` 、 `execute`の 4 つのフェーズで構成されます。

-   `get token` : 通常は数マイクロ秒だけなので無視できます。トークンは、単一の TiDB インスタンスへの接続数が制限[トークン制限](/tidb-configuration-file.md)に達した場合にのみ制限されます。
-   `parse` : クエリ ステートメントは抽象構文ツリー (AST) に解析されます。
-   `compile` : 実行計画は、 `parse`フェーズの AST と統計に基づいて作成されます。 `compile`フェーズには、論理的な最適化と物理的な最適化が含まれます。論理最適化は、リレーショナル代数に基づく列の枝刈りなどのルールによってクエリ プランを最適化します。物理的な最適化は、コストベースのオプティマイザーによる統計によって実行計画のコストを見積もり、最もコストが低い物理的な実行計画を選択します。
-   `execute` : SQL ステートメントの実行にかかる時間。 TiDB はまず、グローバルに一意のタイムスタンプ TSO を待ちます。次に、エグゼキュータは、実行プラン内のオペレータのキー範囲に基づいて TiKV API リクエストを構築し、それを TiKV に配布します。 `execute`時間には、TSO 待機時間、KV リクエスト時間、TiDB エグゼキュータがデータ処理に費やした時間が含まれます。

アプリケーションが`query`または`StmtExecute` MySQL コマンド インターフェイスのみを使用する場合、次の式を使用して平均レイテンシーのボトルネックを特定できます。

    avg Query Duration = avg Get Token + avg Parse Duration + avg Compile Duration + avg Execute Duration

通常、 `execute`フェーズが`query`のレイテンシーの大部分を占めます。ただし、次の場合には`parse`フェーズと`compile`フェーズが大きな役割を果たすこともあります。

-   `parse`フェーズでの長いレイテンシー: たとえば、 `query`のステートメントが長い場合、SQL テキストの解析に多くの CPU が消費されます。
-   `compile`フェーズでの長いレイテンシー: 準備されたプラン キャッシュがヒットしない場合、TiDB は SQL 実行ごとに実行プランをコンパイルする必要があります。 `compile`フェーズのレイテンシーは、数ミリ秒、数十ミリ秒、あるいはそれ以上になる場合があります。準備されたプラン キャッシュがヒットしない場合、論理的および物理的な最適化が`compile`フェーズで実行され、大量の CPU とメモリが消費され、Go ランタイム (TiDB は[`Go`](https://go.dev/)で書き込まれます) に負荷がかかり、他の TiDB コンポーネントのパフォーマンスに影響します。準備されたプラン キャッシュは、TiDB で OLTP ワークロードを効率的に処理するために重要です。

**例 1: `compile`段階でのデータベースのボトルネック**

![Compile](/media/performance/long_compile.png)

上の図では、 `parse` 、 `compile` 、および`execute`フェーズの平均時間は、それぞれ 17.1 us、729 us、および 681 us です。アプリケーションは`query`コマンド インターフェイスを使用し、準備されたプラン キャッシュを使用できないため、 `compile`レイテンシーは長くなります。

**例 2: `execute`フェーズにおけるデータベースのボトルネック**

![Execute](/media/performance/long_execute.png)

この TPC-C ワークロードでは、 `parse` 、 `compile`フェーズ、および`execute`フェーズの平均時間は、それぞれ 7.39 ミリ秒、38.1 ミリ秒、12.8 ミリ秒です。 `execute`フェーズは`query`レイテンシーのボトルネックです。

#### KV および TSO リクエストの期間 {#kv-and-tso-request-duration}

TiDB は`execute`フェーズで PD および TiKV と対話します。次の図に示すように、SQL リクエストを処理するとき、TiDB は`parse`と`compile`フェーズに入る前に TSO をリクエストします。 PD クライアントは呼び出し元をブロックしませんが、 `TSFuture`を返し、バックグラウンドで TSO 要求を非同期に送受信します。 PD クライアントは TSO 要求の処理を完了すると、 `TSFuture`を返します。 `TSFuture`の所有者は、Wait メソッドを呼び出して最終 TSO を取得する必要があります。 TiDB は`parse`と`compile`フェーズを完了すると`execute`フェーズに入り、次の 2 つの状況が発生する可能性があります。

-   TSO 要求が完了すると、Wait メソッドはすぐに使用可能な TSO またはエラーを返します。
-   TSO 要求がまだ完了していない場合、TSO が使用可能になるか、エラーが表示されるまで、Wait メソッドはブロックされます (gRPC 要求は送信されましたが、結果が返されず、ネットワークレイテンシーが長くなります)。

TSO 待機時間は`TSO WAIT`として記録され、TSO 要求のネットワーク時間は`TSO RPC`として記録されます。 TSO 待機が完了すると、TiDB エグゼキュータは通常、読み取りまたは書き込みリクエストを TiKV に送信します。

-   一般的な KV 読み取りリクエスト: `Get` 、 `BatchGet` 、および`Cop`
-   一般的な KV 書き込みリクエスト: 2 フェーズ コミットの場合は`PessimisticLock` 、 `Prewrite` 、および`Commit`

![Execute](/media/performance/execute_phase.png)

このセクションのインジケーターは、次の 3 つのパネルに対応しています。

-   平均 TiDB KV リクエスト期間: TiDB によって測定された KV リクエストの平均レイテンシー
-   平均 TiKV GRPC 継続時間: TiKV で gPRC メッセージを処理する際の平均レイテンシー
-   PD TSO 待機/RPC 期間: TiDB エグゼキュータの TSO 待機時間と TSO 要求 (RPC) のネットワークレイテンシー

`Avg TiDB KV Request Duration`と`Avg TiKV GRPC Duration`の関係は以下の通りです。

    Avg TiDB KV Request Duration = Avg TiKV GRPC Duration + Network latency between TiDB and TiKV + TiKV gRPC processing time + TiDB gRPC processing time and scheduling latency

`Avg TiDB KV Request Duration`と`Avg TiKV GRPC Duration`の違いは、ネットワーク トラフィック、ネットワークレイテンシー、TiDB と TiKV によるリソース使用量に密接に関係しています。

-   同じデータセンター内: 通常、その差は 2 ミリ秒未満です。
-   同じリージョン内の異なるアベイラビリティーゾーンの場合: 通常、その差は 5 ミリ秒未満です。

**例 1: 同じデータセンターにデプロイされたクラスターの低ワークロード**

![Same Data Center](/media/performance/oltp_kv_tso.png)

このワークロードでは、TiDB 上の平均`Prewrite`レイテンシーは 925 マイクロ秒、TiKV 内の平均`kv_prewrite`処理レイテンシーは 720 マイクロ秒です。その差は約 200 us ですが、これは同じデータセンター内では正常です。平均 TSO 待機レイテンシーは 206 マイクロ秒、RPC 時間は 144 マイクロ秒です。

**例 2: パブリック クラウド クラスター上の通常のワークロード**

![Cloud Env ](/media/performance/cloud_kv_tso.png)

この例では、TiDB クラスターが同じリージョン内の異なるデータセンターにデプロイされています。 TiDB 上の平均`commit`レイテンシーは 12.7 ミリ秒、TiKV 内の平均`kv_commit`処理レイテンシーは10.2 ミリ秒で、その差は約 2.5 ミリ秒です。平均 TSO 待機レイテンシーは 3.12 ミリ秒、RPC 時間は 693 マイクロ秒です。

**例 3: パブリック クラウド クラスター上のリソースが過負荷になっている**

![Cloud Env, TiDB Overloaded](/media/performance/cloud_kv_tso_overloaded.png)

この例では、TiDB クラスターが同じ地域内の異なるデータセンターにデプロイされており、TiDB ネットワークと CPU リソースが極度の過負荷になっています。 TiDB 上の平均`BatchGet`レイテンシーは 38.6 ミリ秒、TiKV 内の平均`kv_batch_get`処理レイテンシーは 6.15 ミリ秒です。その差は 32 ミリ秒以上あり、通常の値よりも大幅に大きくなります。平均 TSO 待機レイテンシーは 9.45 ミリ秒、RPC 時間は 14.3 ミリ秒です。

#### ストレージ非同期書き込み期間、保存期間、および適用期間 {#storage-async-write-duration-store-duration-and-apply-duration}

TiKV は、次の手順で書き込みリクエストを処理します。

-   `scheduler worker`書き込みリクエストを処理し、トランザクションの一貫性チェックを実行し、書き込みリクエストを`raftstore`モジュールに送信するキーと値のペアに変換します。
-   TiKV コンセンサス モジュール`raftstore` 、 Raftコンセンサス アルゴリズムを適用して、storageレイヤー(複数の TiKV で構成される) をフォールトトレラントにします。

    Raftstore は`Store`スレッドと`Apply`スレッドで構成されます。

    -   `Store`スレッドはRaftメッセージと新しい`proposals`を処理します。新しい`proposals`を受信すると、リーダー ノードの`Store`スレッドはローカルRaft DB に書き込み、メッセージを複数のフォロワー ノードにコピーします。ほとんどのインスタンスでこの`proposals`正常に永続化されると、 `proposals`正常にコミットされます。
    -   `Apply`スレッドは、コミットされた`proposals` KV DB に書き込みます。コンテンツが KV DB に正常に書き込まれると、スレッド`Apply`は書き込み要求が完了したことを外部に通知します。

![TiKV Write](/media/performance/store_apply.png)

`Storage Async Write Duration`メトリックは、書き込みリクエストが raftstore に入った後のレイテンシーを記録します。データはリクエストごとに収集されます。

`Storage Async Write Duration`メトリックには`Store Duration`と`Apply Duration` 2 つの部分が含まれています。次の式を使用して、書き込みリクエストのボトルネックがステップ`Store`またはステップ`Apply`にあるかどうかを判断できます。

    avg Storage Async Write Duration = avg Store Duration + avg Apply Duration

> **注記：**
>
> `Store Duration`と`Apply Duration`は v5.3.0 以降サポートされています。

**例 1: v5.3.0 と v5.4.0 の同じ OLTP ワークロードの比較**

前述の式によると、v5.4.0 の書き込み負荷の高い OLTP ワークロードの QPS は、v5.3.0 の QPS より 14% 高くなります。

-   v5.3.0: 24.4 ミリ秒 ~= 17.7 ミリ秒 + 6.59 ミリ秒
-   v5.4.0: 21.4 ミリ秒 ~= 14.0 ミリ秒 + 7.33 ミリ秒

v5.4.0 では、 Raftログ レプリケーションを高速化するために gPRC モジュールが最適化されており、v5.3.0 と比較して`Store Duration`が減少しています。

v5.3.0:

![v5.3.0](/media/performance/v5.3.0_store_apply.png)

v5.4.0:

![v5.4.0](/media/performance/v5.4.0_store_apply.png)

**例 2: 保存期間がボトルネックになっている**

前述の式を適用します: 10.1 ミリ秒 ~= 9.81 ミリ秒 + 0.304 ミリ秒。この結果は、書き込みリクエストのレイテンシーのボトルネックが`Store Duration`にあることを示しています。

![Store](/media/performance/cloud_store_apply.png)

#### ログ期間のコミット、ログ期間の追加、およびログ期間の適用 {#commit-log-duration-append-log-duration-and-apply-log-duration}

`Commit Log Duration` 、 `Append Log Duration` 、および`Apply Log Duration` 、raftstore 内の主要な操作のレイテンシーメトリックです。これらのレイテンシはバッチ操作レベルでキャプチャされ、各操作は複数の書き込みリクエストを組み合わせます。したがって、レイテンシは上記の`Store Duration`と`Apply Duration`に直接対応しません。

-   `Commit Log Duration`と`Append Log Duration` `Store`スレッドで実行された操作の時間を記録します。 `Commit Log Duration` Raftログを他の TiKV ノードにコピーする時間が含まれます (raft ログの永続性を確保するため)。 `Commit Log Duration`は通常、リーダー用とフォロワー用の 2 つの`Append Log Duration`操作が含まれます。 `Commit Log Duration`ネットワークを介して他の TiKV ノードにRaftログをコピーする時間が含まれるため、通常は`Append Log Duration`よりも大幅に高くなります。
-   `Apply Log Duration` `Apply`のスレッドによる`apply` Raftログのレイテンシーを記録します。

`Commit Log Duration`が長い一般的なシナリオ:

-   TiKV CPU リソースにボトルネックがあり、スケジューリングのレイテンシーが長い
-   `raftstore.store-pool-size`は小さすぎるか大きすぎるかのいずれかです (値が大きすぎるとパフォーマンスが低下する可能性もあります)
-   I/Oレイテンシーが高く、その結果`Append Log Duration`レイテンシーが高くなります
-   TiKV ノード間のネットワークレイテンシーが長い
-   gRPC スレッドの数が少なすぎるため、GRPC スレッド間で CPU 使用率が不均一です。

`Apply Log Duration`が長い一般的なシナリオ:

-   TiKV CPU リソースにボトルネックがあり、スケジューリングのレイテンシーが長い
-   `raftstore.apply-pool-size`は小さすぎるか大きすぎるかのいずれかです (値が大きすぎるとパフォーマンスが低下する可能性もあります)
-   I/Oレイテンシーが高い

**例 1: v5.3.0 と v5.4.0 の同じ OLTP ワークロードの比較**

v5.4.0 の書き込み負荷の高い OLTP ワークロードの QPS は、v5.3.0 と比較して 14% 向上しました。次の表は、3 つの主要なレイテンシを比較しています。

| 平均継続時間    | v5.3.0 (ミリ秒) | v5.4.0 (ミリ秒) |
| :-------- | :----------- | :----------- |
| ログ期間の追加   | 0.27         | 0.303        |
| コミットログの期間 | 13           | 8.68         |
| ログ期間の適用   | 0.457        | 0.514        |

v5.4.0 では、gPRC モジュールがRaftログ レプリケーションを高速化するように最適化されており、v5.3.0 と比較して`Commit Log Duration`と`Store Duration`が減少しています。

v5.3.0:

![v5.3.0](/media/performance/v5.3.0_commit_append_apply.png)

v5.4.0:

![v5.4.0](/media/performance/v5.4.0_commit_append_apply.png)

**例 2: コミットログの期間がボトルネックになる**

![Store](/media/performance/cloud_append_commit_apply.png)

-   平均`Append Log Duration` = 4.38 ミリ秒
-   平均`Commit Log Duration` = 7.92 ミリ秒
-   平均`Apply Log Duration` = 172 us

`Store`スレッドの場合、 `Commit Log Duration`は明らかに`Apply Log Duration`よりも高くなります。一方、 `Append Log Duration`は`Apply Log Duration`よりも大幅に高く、 `Store`スレッドが CPU と I/O の両方でボトルネックに悩まされている可能性があることを示しています。 `Commit Log Duration`と`Append Log Duration`減らすために考えられる方法は次のとおりです。

-   TiKV CPU リソースが十分な場合は、 `raftstore.store-pool-size`の値を増やして`Store`スレッドを追加することを検討してください。
-   TiDB が v5.4.0 以降の場合は、 `raft-engine.enable: true`を設定して[`Raft Engine`](/tikv-configuration-file.md#raft-engine)を有効にすることを検討してください。 Raft Engine には軽い実行パスがあります。これは、一部のシナリオで I/O 書き込みと書き込みのロングテールレイテンシーを削減するのに役立ちます。
-   TiKV CPU リソースが十分で、TiDB が v5.3.0 以降の場合は、 `raftstore.store-io-pool-size: 1`を設定して[`StoreWriter`](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)有効にすることを検討してください。

## TiDB バージョンが v6.1.0 より前の場合、パフォーマンス概要ダッシュボードを使用するにはどうすればよいですか? {#if-my-tidb-version-is-earlier-than-v6-1-0-what-should-i-do-to-use-the-performance-overview-dashboard}

v6.1.0 以降、Grafana にはデフォルトでパフォーマンス概要ダッシュボードが組み込まれています。このダッシュボードは、TiDB v4.x および v5.x バージョンと互換性があります。 TiDB が v6.1.0 より前の場合は、次の図に示すように、 [`performance_overview.json`](https://github.com/pingcap/tidb/blob/release-7.5/pkg/metrics/grafana/performance_overview.json)手動でインポートする必要があります。

![Store](/media/performance/import_dashboard.png)
