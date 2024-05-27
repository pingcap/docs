---
title: Performance Tuning Practices for OLTP Scenarios
summary: このドキュメントでは、OLTP ワークロードのパフォーマンスを分析および調整する方法について説明します。
---

# OLTP シナリオの性能チューニングプラクティス {#performance-tuning-practices-for-oltp-scenarios}

TiDB は、TiDB ダッシュボードの[Top SQL](/dashboard/top-sql.md)および[継続的なプロファイリング](/dashboard/continuous-profiling.md)機能や、TiDB [パフォーマンス概要ダッシュボード](/grafana-performance-overview-dashboard.md)などの包括的なパフォーマンス診断および分析機能を提供します。

このドキュメントでは、これらの機能を組み合わせて使用​​し、7 つの異なるランタイム シナリオで同じ OLTP ワークロードのパフォーマンスを分析および比較する方法について説明します。これにより、TiDB のパフォーマンスを効率的に分析および調整するのに役立つパフォーマンス チューニング プロセスが示されます。

> **注記：**
>
> [Top SQL](/dashboard/top-sql.md)と[継続的なプロファイリング](/dashboard/continuous-profiling.md)デフォルトでは有効になっていません。事前に有効にする必要があります。

このドキュメントでは、これらのシナリオで同じアプリケーションを異なる JDBC 構成で実行することにより、アプリケーションとデータベース間のさまざまな相互作用が全体的なシステム パフォーマンスにどのように影響するかを示し、パフォーマンスを向上させるために[TiDB を使用したJavaアプリケーション開発のベスト プラクティス](/best-practices/java-app-best-practices.md)適用できるようにします。

## 環境の説明 {#environment-description}

このドキュメントでは、コア バンキングの OLTP ワークロードをデモンストレーションに使用します。シミュレーション環境の構成は次のとおりです。

-   ワークロードのアプリケーション開発言語: JAVA
-   業務で使用される SQL 文: 合計 200 文、そのうち 90% が SELECT 文です。これは典型的な読み取り中心の OLTP ワークロードです。
-   トランザクションで使用されるテーブル: 合計 60 テーブル。12 テーブルは更新操作に関連し、残りの 48 テーブルは読み取り専用です。
-   アプリケーションで使用される分離レベル: `read committed` 。
-   TiDB クラスター構成: 3 つの TiDB ノードと 3 つの TiKV ノード、各ノードに 16 個の CPU が割り当てられます。
-   クライアントサーバー構成: 36 個の CPU。

## シナリオ 1. クエリ インターフェースを使用する {#scenario-1-use-the-query-interface}

### アプリケーション構成 {#application-configuration}

アプリケーションは、次の JDBC 構成を使用して、クエリ インターフェイスを介してデータベースに接続します。

    useServerPrepStmts=false

### パフォーマンス分析 {#performance-analysis}

#### TiDBダッシュボード {#tidb-dashboard}

以下の TiDB ダッシュボードの[Top SQL]ページから、非ビジネス SQL タイプ`SELECT @@session.tx_isolation`が最も多くのリソースを消費していることがわかります。TiDB はこれらのタイプの SQL ステートメントを迅速に処理しますが、これらのタイプの SQL ステートメントは実行回数が最も多く、全体的な CPU 時間の消費量が最も高くなります。

![dashboard-for-query-interface](/media/performance/case1.png)

以下の TiDB のフレーム チャートから、SQL 実行中に`Compile`や`Optimize`などの関数の CPU 消費が顕著であることがわかります。アプリケーションは Query インターフェイスを使用するため、TiDB は実行プラン キャッシュを使用できません。TiDB は、SQL ステートメントごとに実行プランをコンパイルして生成する必要があります。

![flame-graph-for-query-interface](/media/performance/7.1.png)

-   ExecuteStmt CPU = 38% CPU 時間 = 23.84 秒
-   コンパイル CPU = 27% CPU 時間 = 17.17 秒
-   CPU を最適化 = 26% CPU 時間 = 16.41 秒

#### パフォーマンス概要ダッシュボード {#performance-overview-dashboard}

次のパフォーマンス概要ダッシュボードで、データベース時間の概要と QPS を確認します。

![performance-overview-1-for-query-interface](/media/performance/j-1.png)

-   SQL タイプ別のデータベース時間: `Select`ステートメント タイプが最も多くの時間を費やします。
-   SQL フェーズ別のデータベース時間: フェーズ`execute`と`compile`がほとんどの時間を費やします。
-   SQL 実行時間の概要: `Get` 、および`Cop` `tso wait`ほとんどの時間がかかります。
-   タイプ別 CPS: `Query`コマンドのみが使用されます。
-   プラン キャッシュ OPS を使用したクエリ: データなしは、実行プラン キャッシュがヒットしていないことを示します。
-   クエリ期間では、レイテンシー`execute`と`compile`の割合が最も高くなります。
-   平均 QPS = 56.8k

クラスターのリソース消費量を確認します。TiDB CPU の平均使用率は 925%、TiKV CPU の平均使用率は 201%、TiKV IO の平均スループットは 18.7 MB/秒です。TiDB のリソース消費量が大幅に高くなっています。

![performance-overview-2-for-query-interface](/media/performance/5.png)

### 分析の結論 {#analysis-conclusion}

実行回数が多く、TiDB の CPU 使用率が高くなる原因となる、ビジネスに関係のない無駄な SQL ステートメントを排除する必要があります。

## シナリオ2. maxPerformance構成を使用する {#scenario-2-use-the-maxperformance-configuration}

### アプリケーション構成 {#application-configuration}

アプリケーションは、シナリオ 1 の JDBC 接続文字列に新しいパラメータ`useConfigs=maxPerformance`を追加します。このパラメータを使用すると、JDBC からデータベースに送信される SQL 文 (たとえば、 `select @@session.transaction_read_only` ) を削除できます。完全な構成は次のとおりです。

    useServerPrepStmts=false&useConfigs=maxPerformance

### パフォーマンス分析 {#performance-analysis}

#### TiDBダッシュボード {#tidb-dashboard}

下記の TiDB ダッシュボードのTop SQLページを見ると、最も多くのリソースを消費していた`SELECT @@session.tx_isolation`が消えていることがわかります。

![dashboard-for-maxPerformance](/media/performance/case2.png)

次の TiDB のフレーム チャートから、SQL 実行中に`Compile`や`Optimize`などの関数の CPU 消費が依然として大きいことがわかります。

![flame-graph-for-maxPerformance](/media/performance/20220507-145257.jpg)

-   ExecuteStmt CPU = 43% CPU 時間 =35.84 秒
-   コンパイル CPU = 31% CPU 時間 =25.61 秒
-   CPU を最適化 = 30% CPU 時間 = 24.74 秒

#### パフォーマンス概要ダッシュボード {#performance-overview-dashboard}

データベースの時間概要と QPS のデータは次のとおりです。

![performance-overview-1-for-maxPerformance](/media/performance/j-2.png)

-   SQL タイプ別のデータベース時間: `Select`ステートメント タイプが最も多くの時間を費やします。
-   SQL フェーズ別のデータベース時間: フェーズ`execute`と`compile`がほとんどの時間を費やします。
-   SQL 実行時間`Cop`概要: `Get` `Prewrite`および`tso wait`ほとんどの時間がかかります。
-   データベース時間では、レイテンシー`execute`と`compile`の割合が最も高くなります。
-   タイプ別 CPS: `Query`コマンドのみが使用されます。
-   平均 QPS = 24.2k (56.3k から 24.2k)
-   実行プラン キャッシュにヒットしません。

シナリオ 1 からシナリオ 2 にかけて、TiDB CPU の平均使用率は 925% から 874% に低下し、TiKV CPU の平均使用率は 201% から約 250% に増加します。

![performance-overview-2-for-maxPerformance](/media/performance/9.1.1.png)

主要なレイテンシーメトリックの変更は次のとおりです。

![performance-overview-3-for-maxPerformance](/media/performance/9.2.2.png)

-   平均クエリ期間 = 1.12ms (479μs から 1.12ms)
-   平均解析時間 = 84.7μs (37.2μs から 84.7μs)
-   平均コンパイル時間 = 370μs (166μs から 370μs)
-   平均実行時間 = 626μs (251μs から 626μs)

### 分析の結論 {#analysis-conclusion}

シナリオ 1 と比較すると、シナリオ 2 の QPS は大幅に減少しています。平均クエリ期間と平均`parse` 、 `compile` 、 `execute`期間は大幅に増加しています。これは、シナリオ 1 の`select @@session.transaction_read_only`などの実行回数が多く、処理時間が速い SQL 文が平均パフォーマンス データを下げるためです。シナリオ 2 でこのような文がブロックされると、ビジネス関連の SQL 文のみが残るため、平均期間が増加します。

アプリケーションがクエリ インターフェイスを使用する場合、TiDB は実行プラン キャッシュを使用できないため、実行プランをコンパイルするために TiDB が大量のリソースを消費することになります。この場合、TiDB の実行プラン キャッシュを使用して実行プランのコンパイルによる TiDB CPU 消費を減らし、レイテンシーを短縮する Prepared Statement インターフェイスを使用することをお勧めします。

## シナリオ 3. 実行プランのキャッシュを有効にせずに Prepared Statement インターフェイスを使用する {#scenario-3-use-the-prepared-statement-interface-with-execution-plan-caching-not-enabled}

### アプリケーション構成 {#application-configuration}

アプリケーションでは、次の接続構成を使用します。シナリオ 2 と比較すると、JDBC パラメータ`useServerPrepStmts`の値が`true`に変更され、Prepared Statement インターフェイスが有効になっていることが示されます。

    useServerPrepStmts=true&useConfigs=maxPerformance"

### パフォーマンス分析 {#performance-analysis}

#### TiDBダッシュボード {#tidb-dashboard}

次の TiDB のフレーム チャートから、Prepared Statement インターフェイスを有効にした後でも、 `CompileExecutePreparedStmt`と`Optimize`の CPU 消費が依然として大きいことがわかります。

![flame-graph-for-PrepStmts](/media/performance/3.1.1.png)

-   ExecutePreparedStmt CPU = 31% CPU 時間 = 23.10 秒
-   preparedStmtExec CPU = 30% CPU 時間 = 22.92 秒
-   CompileExecutePreparedStmt CPU = 24% CPU 時間 = 17.83 秒
-   CPU を最適化 = 23% CPU 時間 = 17.29 秒

#### パフォーマンス概要ダッシュボード {#performance-overview-dashboard}

Prepared Statement インターフェイスを使用した後、データベース時間の概要と QPS のデータは次のようになります。

![performance-overview-1-for-PrepStmts](/media/performance/j-3.png)

QPS は 24.4k から 19.7k に低下しています。Database Time Overview から、アプリケーションが 3 種類の Prepared コマンドを使用しており、 `general`ステートメント タイプ ( `StmtPrepare`や`StmtClose`などのコマンドの実行時間を含む) が Database Time by SQL Type で 2 位になっていることがわかります。これは、Prepared Statement インターフェイスを使用しても、実行プラン キャッシュにヒットしないことを示しています。これは、 `StmtClose`コマンドを実行すると、TiDB が内部処理で SQL ステートメントの実行プラン キャッシュをクリアするためです。

-   SQL タイプ別のデータベース時間: `Select`ステートメント タイプが最も時間がかかり、次に`general`ステートメント タイプが続きます。
-   SQL フェーズ別のデータベース時間: フェーズ`execute`と`compile`がほとんどの時間を費やします。
-   SQL 実行時間`Cop`概要: `Get` `Prewrite`および`tso wait`ほとんどの時間がかかります。
-   タイプ`StmtClose` CPS: 3 `StmtExecute` `StmtPrepare`が使用されます。
-   平均 QPS = 19.7k (24.4k から 19.7k)
-   実行プラン キャッシュにヒットしません。

TiDB の平均 CPU 使用率は 874% から 936% に増加します。

![performance-overview-1-for-PrepStmts](/media/performance/3-2.png)

主要なレイテンシーメトリックは次のとおりです。

![performance-overview-2-for-PrepStmts](/media/performance/3.4.png)

-   平均クエリ時間 = 528μs (1.12ms から 528μs)
-   平均解析時間 = 14.9μs (84.7μs から 14.9μs)
-   平均コンパイル時間 = 374μs (370μs から 374μs)
-   平均実行時間 = 649μs (626μs から 649μs)

### 分析の結論 {#analysis-conclusion}

シナリオ 2 とは異なり、シナリオ 3 のアプリケーションは Prepared Statement インターフェイスを有効にしますが、それでもキャッシュにヒットしません。さらに、シナリオ 2 には CPS By Type コマンド タイプが 1 つ ( `Query` ) しかありませんが、シナリオ 3 にはコマンド タイプが 3 つ ( `StmtPrepare` 、 `StmtExecute` 、 `StmtClose` ) 多くあります。シナリオ 2 と比較すると、シナリオ 3 にはネットワーク ラウンドトリップ遅延が 2 つ多くあります。

-   QPS の減少に関する分析: **CPS By Type**ペインから、シナリオ 2 には CPS By Type コマンド タイプが 1 つ ( `Query` ) しかなく、シナリオ 3 にはさらに 3 つのコマンド タイプ ( `StmtPrepare` 、 `StmtExecute` 、 `StmtClose` ) があることがわかります`StmtPrepare`と`StmtClose` QPS でカウントされない非従来型コマンドであるため、QPS が減少します。非従来型コマンド`StmtPrepare`と`StmtClose`は`general` SQL タイプにカウントされるため、シナリオ 3 のデータベース概要には`general`時間が表示され、データベース時間の 4 分の 1 以上を占めています。
-   平均クエリ時間が大幅に短縮された理由の分析: シナリオ 3 で新たに追加されたコマンド タイプ`StmtPrepare`と`StmtClose`については、クエリ時間は TiDB の内部処理で個別に計算されます。TiDB はこれら 2 種類のコマンドを非常に高速に実行するため、平均クエリ時間が大幅に短縮されます。

シナリオ 3 では Prepared Statement インターフェイスが使用されていますが、多くのアプリケーション フレームワークはメモリリークを防ぐために`StmtExecute`の後に`StmtClose`メソッドを呼び出すため、実行プラン キャッシュはまだヒットしません。v6.0.0 以降では、グローバル変数`tidb_ignore_prepared_cache_close_stmt=on;`を設定できます。その後、アプリケーションが`StmtClose`メソッドを呼び出しても、TiDB はキャッシュされた実行プランをクリアしないため、次の SQL 実行では既存の実行プランを再利用でき、実行プランを繰り返しコンパイルする必要がなくなります。

## シナリオ 4. Prepared Statement インターフェースを使用して実行プランのキャッシュを有効にする {#scenario-4-use-the-prepared-statement-interface-and-enable-execution-plan-caching}

### アプリケーション構成 {#application-configuration}

アプリケーション構成はシナリオ 3 と同じままです。アプリケーションが`StmtClose`トリガーしてもキャッシュにヒットしない問題を解決するために、次のパラメータが構成されています。

-   TiDB グローバル変数`set global tidb_ignore_prepared_cache_close_stmt=on;`を設定します (TiDB v6.0.0 以降で導入され、デフォルトは`off` )。
-   プラン キャッシュ機能を有効にするには、TiDB 構成項目`prepared-plan-cache: {enabled: true}`を設定します。

### パフォーマンス分析 {#performance-analysis}

#### TiDBダッシュボード {#tidb-dashboard}

TiDB CPU 使用率のフレーム チャートから、 `CompileExecutePreparedStmt`と`Optimize`では CPU 消費量が大幅に増加していないことがわかります。CPU の 25% は`Prepare`コマンドによって消費されており、これには`PlanBuilder`や`parseSQL`などの Prepare の解析関連関数が含まれています。

PreparseStmt CPU = 25% CPU 時間 = 12.75 秒

![flame-graph-for-3-commands](/media/performance/4.2.png)

#### パフォーマンス概要ダッシュボード {#performance-overview-dashboard}

パフォーマンス概要ダッシュボードでは、最も大きな変化はフェーズ`compile`の平均時間で、シナリオ 3 の 8.95 秒/秒から 1.18 秒/秒に短縮されています。実行プラン キャッシュを使用するクエリの数は、 `StmtExecute`の値とほぼ等しくなります。QPS が増加すると、1 秒あたり`Select`ステートメントで消費されるデータベース時間は減少し、1 秒あたり`general`ステートメントのタイプで消費されるデータベース時間は増加します。

![performance-overview-1-for-3-commands](/media/performance/j-4.png)

-   SQL タイプ別のデータベース時間: `Select`ステートメント タイプが最も時間がかかります。
-   SQL フェーズ別のデータベース時間: フェーズ`execute`がほとんどの時間を費やします。
-   SQL 実行時間の概要: `tso wait` 、および`Get` `Cop`ほとんどの時間がかかります。
-   実行プラン キャッシュがヒットしました。プラン キャッシュ OPS を使用するクエリの値は、1 秒あたりおよそ`StmtExecute`相当します。
-   タイプ別CPS: 3種類のコマンド(シナリオ3と同じ)
-   シナリオ 3 と比較すると、QPS が増加したため、 `general`ステートメントで消費される時間が長くなります。
-   平均 QPS = 22.1k (19.7k から 22.1k)

平均 TiDB CPU 使用率は 936% から 827% に低下します。

![performance-overview-2-for-3-commands](/media/performance/4.4.png)

平均`compile`時間は 374 us から 53.3 us に大幅に減少しました。QPS が増加するため、平均`execute`時間も増加します。

![performance-overview-3-for-3-commands](/media/performance/4.5.png)

-   平均クエリ時間 = 426μs (528μs から 426μs)
-   平均解析時間 = 12.3μs (14.8μs から 12.3μs)
-   平均コンパイル時間 = 53.3μs (374μs から 53.3μs)
-   平均実行時間 = 699μs (649μs から 699us)

### 分析の結論 {#analysis-conclusion}

シナリオ 3 と比較すると、シナリオ 4 でも 3 つのコマンド タイプが使用されます。違いは、シナリオ 4 では実行プラン キャッシュがヒットするため、コンパイル時間が大幅に短縮され、クエリ時間も短縮され、QPS が向上することです。

`StmtPrepare`と`StmtClose`コマンドはデータベース時間を大量に消費し、アプリケーションが SQL ステートメントを実行するたびにアプリケーションと TiDB 間の対話回数が増えるためです。次のシナリオでは、JDBC 構成を通じてこれら 2 つのコマンドの呼び出しを排除することで、パフォーマンスをさらに調整します。

## シナリオ5. クライアント側で準備されたオブジェクトをキャッシュする {#scenario-5-cache-prepared-objects-on-the-client-side}

### アプリケーション構成 {#application-configuration}

シナリオ 4 と比較して、以下に説明するように 3 つの新しい JDBC パラメータ`cachePrepStmts=true&prepStmtCacheSize=1000&prepStmtCacheSqlLimit=20480`が構成されます。

-   `cachePrepStmts = true` : クライアント側で Prepared Statement オブジェクトをキャッシュし、StmtPrepare および StmtClose の呼び出しを排除します。
-   `prepStmtCacheSize` : 値は 0 より大きくなければなりません。
-   `prepStmtCacheSqlLimit` : 値は SQL テキストの長さより大きくなければなりません。

シナリオ 5 では、完全な JDBC 構成は次のようになります。

    useServerPrepStmts=true&cachePrepStmts=true&prepStmtCacheSize=1000&prepStmtCacheSqlLimit=20480&useConfigs=maxPerformance

### パフォーマンス分析 {#performance-analysis}

#### TiDBダッシュボード {#tidb-dashboard}

次の TiDB のフレーム チャートから、コマンド`Prepare`の高い CPU 消費がなくなったことがわかります。

-   ExecutePreparedStmt CPU = 22% CPU 時間 = 8.4 秒

![flame-graph-for-1-command](/media/performance/5.1.1.png)

#### パフォーマンス概要ダッシュボード {#performance-overview-dashboard}

パフォーマンス概要ダッシュボードで最も注目すべき変更点は、 **CPS By Type**ペインの 3 つの Stmt コマンド タイプが 1 つに減り、 **Database Time by SQL Type**ペインの`general`ステートメント タイプが消え、 **QPS**ペインの QPS が 30.9k に増加したことです。

![performance-overview-for-1-command](/media/performance/j-5.png)

-   SQL タイプ別のデータベース時間: `Select`ステートメント タイプが最も多くの時間を費やし、 `general`ステートメント タイプは消えます。
-   SQL フェーズ別のデータベース時間: フェーズ`execute`がほとんどの時間を費やします。
-   SQL 実行時間の概要: `tso wait` 、および`Get` `Cop`ほとんどの時間がかかります。
-   実行プラン キャッシュがヒットしました。プラン キャッシュ OPS を使用するクエリの値は、1 秒あたりおよそ`StmtExecute`相当します。
-   タイプ別 CPS: `StmtExecute`コマンドのみが使用されます。
-   平均 QPS = 30.9k (22.1k から 30.9k)

TiDB の平均 CPU 使用率は 827% から 577% に低下します。QPS が増加すると、TiKV の平均 CPU 使用率は 313% に増加します。

![performance-overview-for-2-command](/media/performance/j-5-cpu.png)

主要なレイテンシーメトリックは次のとおりです。

![performance-overview-for-3-command](/media/performance/j-5-duration.png)

-   平均クエリ期間 = 690μs (426μs から 690μs)
-   平均解析時間 = 13.5μs (12.3μsから13.5μs)
-   平均コンパイル時間 = 49.7μs (53.3μs から 49.7μs)
-   平均実行時間 = 623μs (699us から 623μs)
-   平均 pd tso 待機時間 = 196μs (224μs から 196μs)
-   接続アイドル時間 avg-in-txn = 608μs (250μs から 608μs)

### 分析の結論 {#analysis-conclusion}

-   シナリオ 4 と比較すると、シナリオ 5 の**[CPS By Type]**ペインには`StmtExecute`コマンドのみがあり、これにより 2 回のネットワーク ラウンド トリップが回避され、システム全体の QPS が向上します。
-   QPS が増加すると、解析時間、コンパイル時間、実行時間の観点からレイテンシーは減少しますが、代わりにクエリ時間は増加します。これは、TiDB が`StmtPrepare`と`StmtClose`非常に速く処理し、これら 2 つのコマンド タイプを削除すると平均クエリ時間が増加するためです。
-   SQL フェーズ別のデータベース時間では、 `execute`最も時間がかかり、データベース時間に近くなります。一方、SQL 実行時間の概要では、 `tso wait`最も時間がかかり、 `execute`時間の 4 分の 1 以上が TSO の待機に費やされます。
-   1 秒あたりの合計`tso wait`回は 5.46 秒です。平均`tso wait`回は 196 us で、1 秒あたり`tso cmd`回の数は 28k であり、これは QPS の 30.9k に非常に近いです。これは、TiDB の`read committed`分離レベルの実装に従って、トランザクション内のすべての SQL ステートメントが PD から TSO を要求する必要があるためです。

TiDB v6.0 は`rc read`提供します。これは`tso cmd`を削減することで`read committed`分離レベルを最適化します。この機能は、グローバル変数`set global tidb_rc_read_check_ts=on;`によって制御されます。この変数を有効にすると、TiDB のデフォルトの動作は`repeatable-read`分離レベルと同じように動作し、PD から取得する必要があるのは`start-ts`と`commit-ts`のみです。トランザクション内のステートメントは、最初に`start-ts`使用して TiKV からデータを読み取ります。TiKV から読み取られたデータが`start-ts`より前の場合、データは直接返されます。TiKV から読み取られたデータが`start-ts`より後の場合、データは破棄されます。TiDB は PD から TSO を要求し、読み取りを再試行します。後続のステートメントの`for update ts`では、最新の PD TSO が使用されます。

## シナリオ6: <code>tidb_rc_read_check_ts</code>変数を有効にしてTSOリクエストを減らす {#scenario-6-enable-the-code-tidb-rc-read-check-ts-code-variable-to-reduce-tso-requests}

### アプリケーション構成 {#application-configuration}

シナリオ 5 と比較すると、アプリケーション構成は同じままです。唯一の違いは、 `set global tidb_rc_read_check_ts=on;`変数が TSO 要求を減らすように構成されていることです。

### パフォーマンス分析 {#performance-analysis}

#### ダッシュボード {#dashboard}

TiDB CPU のフレーム チャートには大きな変化はありません。

-   ExecutePreparedStmt CPU = 22% CPU 時間 = 8.4 秒

![flame-graph-for-rc-read](/media/performance/6.2.2.png)

#### パフォーマンス概要ダッシュボード {#performance-overview-dashboard}

RC 読み取りを使用した後、QPS は 30.9k から 34.9k に増加し、 `tso wait`秒あたりに消費される時間は 5.46 秒から 456 ミリ秒に減少します。

![performance-overview-1-for-rc-read](/media/performance/j-6.png)

-   SQL タイプ別のデータベース時間: `Select`ステートメント タイプが最も多くの時間を費やします。
-   SQL フェーズ別のデータベース時間: フェーズ`execute`がほとんどの時間を費やします。
-   SQL 実行時間の概要: `Get` 、および`Cop` `Prewrite`ほとんどの時間がかかります。
-   実行プラン キャッシュがヒットしました。プラン キャッシュ OPS を使用するクエリの値は、1 秒あたりおよそ`StmtExecute`相当します。
-   タイプ別 CPS: `StmtExecute`コマンドのみが使用されます。
-   平均 QPS = 34.9k (30.9k から 34.9k)

1 秒あたり`tso cmd` 28.3k から 2.7k に減少します。

![performance-overview-2-for-rc-read](/media/performance/j-6-cmd.png)

平均 TiDB CPU は 603% に増加します (577% から 603%)。

![performance-overview-3-for-rc-read](/media/performance/j-6-cpu.png)

主要なレイテンシーメトリックは次のとおりです。

![performance-overview-4-for-rc-read](/media/performance/j-6-duration.png)

-   平均クエリ期間 = 533μs (690μs から 533μs)
-   平均解析時間 = 13.4μs (13.5μsから13.4μs)
-   平均コンパイル時間 = 50.3μs (49.7μs から 50.3μs)
-   平均実行時間 = 466μs (623μs から 466μs)
-   平均 pd tso 待機時間 = 171μs (196μs から 171μs)

### 分析の結論 {#analysis-conclusion}

RC Read を`set global tidb_rc_read_check_ts=on;`有効にした後、RC Read は`tso cmd`の時間を大幅に短縮し、 `tso wait`と平均クエリ期間を短縮して、QPS を向上させます。

現在のデータベース時間とレイテンシーの両方のボトルネックは、 `Get`と`Cop`の読み取り要求の割合が最も高いフェーズ`execute`にあります。このワークロードのテーブルのほとんどは読み取り専用であるか、ほとんど変更されないため、TiDB v6.0.0 以降でサポートされている小さなテーブルのキャッシュ機能を使用して、これらの小さなテーブルのデータをキャッシュし、KV 読み取り要求の待機時間とリソース消費を削減できます。

## シナリオ7: 小さなテーブルキャッシュを使用する {#scenario-7-use-the-small-table-cache}

### アプリケーション構成 {#application-configuration}

シナリオ 6 と比較すると、アプリケーション構成は同じままです。唯一の違いは、シナリオ 7 では、 `alter table t1 cache;`などの SQL ステートメントを使用して、ビジネス用の読み取り専用テーブルをキャッシュすることです。

### パフォーマンス分析 {#performance-analysis}

#### TiDBダッシュボード {#tidb-dashboard}

TiDB CPU のフレーム チャートには大きな変化はありません。

![flame-graph-for-table-cache](/media/performance/7.2.png)

#### パフォーマンス概要ダッシュボード {#performance-overview-dashboard}

QPS は 34.9k から 40.9k に増加し、KV 要求タイプは`execute`フェーズから`Prewrite`および`Commit`への変更で最も時間がかかります。1 秒あたり`Get`によって消費されるデータベース時間は 5.33 秒から 1.75 秒に減少し、1 秒あたり`Cop`によって消費されるデータベース時間は 3.87 秒から 1.09 秒に減少します。

![performance-overview-1-for-table-cache](/media/performance/j-7.png)

-   SQL タイプ別のデータベース時間: `Select`ステートメント タイプが最も多くの時間を費やします。
-   SQL フェーズ別のデータベース時間: フェーズ`execute`と`compile`がほとんどの時間を費やします。
-   SQL 実行時間の概要: `Prewrite` 、および`Commit` `Get`ほとんどの時間がかかります。
-   実行プラン キャッシュがヒットしました。プラン キャッシュ OPS を使用するクエリの値は、1 秒あたりおよそ`StmtExecute`相当します。
-   タイプ別 CPS: `StmtExecute`コマンドのみが使用されます。
-   平均 QPS = 40.9k (34.9k から 40.9k)

平均 TiDB CPU 使用率は 603% から 478% に低下し、平均 TiKV CPU 使用率は 346% から 256% に低下します。

![performance-overview-2-for-table-cache](/media/performance/j-7-cpu.png)

平均クエリレイテンシーは533 us から 313 us に短縮されます。平均`execute`レイテンシーは466 us から 250 us に短縮されます。

![performance-overview-3-for-table-cache](/media/performance/j-7-duration.png)

-   平均クエリ期間 = 313μs (533μs から 313μs)
-   平均解析時間 = 11.9μs (13.4μs から 11.9μs)
-   平均コンパイル時間 = 47.7μs (50.3μs から 47.7μs)
-   平均実行時間 = 251μs (466μs から 251μs)

### 分析の結論 {#analysis-conclusion}

すべての読み取り専用テーブルをキャッシュした後、 `Execute Duration`大幅に低下します。これは、すべての読み取り専用テーブルが TiDB にキャッシュされ、それらのテーブルに対して TiKV でデータをクエリする必要がないため、クエリ期間が短縮され、QPS が増加するためです。

これは楽観的結果です。実際の業務では、読み取り専用テーブルのデータは TiDB がすべてをキャッシュするには大きすぎる可能性があるからです。もう 1 つの制限は、小さなテーブル キャッシュ機能は書き込み操作をサポートしますが、書き込み操作ではすべての TiDB ノードのキャッシュが最初に無効になることを保証するためにデフォルトで 3 秒の待機時間が必要であり、レイテンシー要件が厳しいアプリケーションでは実現できない可能性があることです。

## まとめ {#summary}

次の表は、7 つの異なるシナリオのパフォーマンスを示しています。

| メトリクス | シナリオ1 | シナリオ2  | シナリオ3 | シナリオ4 | シナリオ5 | シナリオ6 | シナリオ7 | シナリオ5とシナリオ2の比較（％） | シナリオ7とシナリオ3の比較（％） |
| ----- | ----- | ------ | ----- | ----- | ----- | ----- | ----- | ----------------- | ----------------- |
| クエリ期間 | 479μs | 1120μs | 528μs | 426μs | 690μs | 533μs | 313μs | -38%              | -51%              |
| 品質保証  | 56.3k | 24.2k  | 19.7k | 22.1k | 30.9k | 34.9k | 40.9k | +28%              | +108%             |

これらのシナリオでは、シナリオ 2 はアプリケーションがクエリ インターフェイスを使用する一般的なシナリオであり、シナリオ 5 はアプリケーションが準備済みステートメント インターフェイスを使用する理想的なシナリオです。

-   シナリオ 2 とシナリオ 5 を比較すると、 Javaアプリケーション開発のベスト プラクティスを使用し、クライアント側で Prepared Statement オブジェクトをキャッシュすると、各 SQL ステートメントで実行プラン キャッシュをヒットするために必要なコマンドとデータベース操作が 1 つだけになり、クエリのレイテンシーが 38% 短縮され、QPS が 28% 増加する一方で、TiDB の平均 CPU 使用率は 936% から 577% に低下することがわかります。
-   シナリオ 2 とシナリオ 7 を比較すると、シナリオ 5 に RC 読み取りや小さなテーブル キャッシュなどの最新の TiDB 最適化機能を追加すると、レイテンシーが 51% 削減され、QPS が 108% 増加し、平均 TiDB CPU 使用率が 936% から 478% に低下することがわかります。

各シナリオのパフォーマンスを比較すると、次の結論を導き出すことができます。

-   TiDB の実行プラン キャッシュは、OLTP パフォーマンス チューニングにおいて重要な役割を果たします。v6.0.0 から導入された RC 読み取り機能と小規模テーブル キャッシュ機能も、このワークロードのさらなるパフォーマンス チューニングにおいて重要な役割を果たします。

-   TiDB は、MySQL プロトコルのさまざまなコマンドと互換性があります。Prepared Statement インターフェイスを使用し、次の JDBC 接続パラメータを設定すると、アプリケーションは最高のパフォーマンスを実現できます。

        useServerPrepStmts=true&cachePrepStmts=true&prepStmtCacheSize=1000&prepStmtCacheSqlLimit=20480&useConfigs= maxPerformance

-   パフォーマンス分析とチューニングには、TiDB ダッシュボード (たとえば、 Top SQL機能や継続的なプロファイリング機能) とパフォーマンス概要ダッシュボードを使用することをお勧めします。

    -   [Top SQL](/dashboard/top-sql.md)機能を使用すると、実行中にデータベース内の各 SQL ステートメントの CPU 消費量を視覚的に監視および調査して、データベースのパフォーマンスの問題をトラブルシューティングできます。
    -   [継続的なプロファイリング](/dashboard/continuous-profiling.md)使用すると、TiDB、TiKV、PD の各インスタンスからパフォーマンス データを継続的に収集できます。アプリケーションが異なるインターフェイスを使用して TiDB と対話する場合、TiDB の CPU 消費量の違いは非常に大きくなります。
    -   [パフォーマンス概要ダッシュボード](/grafana-performance-overview-dashboard.md)を使用すると、データベース時間と SQL 実行時間の内訳情報の概要を取得できます。データベース時間に基づいてパフォーマンスを分析および診断し、システム全体のパフォーマンスのボトルネックが TiDB にあるかどうかを判断できます。ボトルネックが TiDB にある場合は、データベース時間とレイテンシーの内訳、および負荷プロファイルとリソース使用率を使用して、TiDB 内のパフォーマンスのボトルネックを特定し、それに応じてパフォーマンスを調整できます。

これらの機能を組み合わせて使用​​することで、実際のアプリケーションのパフォーマンスを効率的に分析および調整できます。
