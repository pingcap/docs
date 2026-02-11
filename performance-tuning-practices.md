---
title: Performance Tuning Practices for OLTP Scenarios
summary: このドキュメントでは、OLTP ワークロードのパフォーマンスを分析および調整する方法について説明します。
---

# OLTPシナリオの性能チューニングの実践 {#performance-tuning-practices-for-oltp-scenarios}

TiDB は、TiDB ダッシュボードの[Top SQL](/dashboard/top-sql.md)と[継続的なプロファイリング](/dashboard/continuous-profiling.md)機能や、TiDB [パフォーマンス概要ダッシュボード](/grafana-performance-overview-dashboard.md)などの包括的なパフォーマンス診断および分析機能を提供します。

このドキュメントでは、これらの機能を組み合わせて使用​​し、7 つの異なるランタイム シナリオで同じ OLTP ワークロードのパフォーマンスを分析および比較する方法について説明します。これにより、TiDB のパフォーマンスを効率的に分析および調整するのに役立つパフォーマンス チューニング プロセスが示されます。

> **注記：**
>
> [Top SQL](/dashboard/top-sql.md)と[継続的なプロファイリング](/dashboard/continuous-profiling.md)デフォルトでは有効になっていません。事前に有効にする必要があります。

このドキュメントでは、これらのシナリオで同じアプリケーションを異なる JDBC 構成で実行することにより、アプリケーションとデータベース間のさまざまな相互作用が全体的なシステム パフォーマンスにどのように影響するかを示し、パフォーマンスを向上させるために[TiDB を使用したJavaアプリケーション開発のベスト プラクティス](/develop/java-app-best-practices.md)適用できるようにします。

## 環境の説明 {#environment-description}

このドキュメントでは、銀行業務のコアOLTPワークロードを例に挙げて説明します。シミュレーション環境の構成は次のとおりです。

-   ワークロードのアプリケーション開発言語: JAVA
-   業務で使用されるSQL文：合計200文、そのうち90%がSELECT文です。これは典型的な読み取り中心のOLTPワークロードです。
-   トランザクションで使用されるテーブル: 合計 60 テーブル。12 テーブルは更新操作に関連し、残りの 48 テーブルは読み取り専用です。
-   アプリケーションで使用される分離レベル: `read committed` 。
-   TiDB クラスター構成: 3 つの TiDB ノードと 3 つの TiKV ノード、各ノードに 16 個の CPU が割り当てられます。
-   クライアントサーバー構成: 36 個の CPU。

## シナリオ1. クエリインターフェースを使用する {#scenario-1-use-the-query-interface}

### アプリケーション構成 {#application-configuration}

アプリケーションは、次の JDBC 構成を使用して、クエリ インターフェイスを介してデータベースに接続します。

    useServerPrepStmts=false

### パフォーマンス分析 {#performance-analysis}

#### TiDBダッシュボード {#tidb-dashboard}

下記のTiDBダッシュボードの「Top SQL」ページを見ると、非ビジネスSQLタイプ`SELECT @@session.tx_isolation`最も多くのリソースを消費していることがわかります。TiDBはこれらのタイプのSQL文を迅速に処理しますが、実行回数が最も多く、全体的なCPU消費時間も最も高くなります。

![dashboard-for-query-interface](/media/performance/case1.png)

以下のTiDBのフレームチャートから、SQL実行中に`Compile`や`Optimize`などの関数のCPU消費が顕著であることがわかります。アプリケーションはQueryインターフェースを使用しているため、TiDBは実行プランキャッシュを使用できません。TiDBはSQL文ごとにコンパイルして実行プランを生成する必要があります。

![flame-graph-for-query-interface](/media/performance/7.1.png)

-   ExecuteStmt CPU = 38% CPU時間 = 23.84秒
-   コンパイルCPU = 27% CPU時間 = 17.17秒
-   CPUを最適化 = 26%、CPU時間 = 16.41秒

#### パフォーマンス概要ダッシュボード {#performance-overview-dashboard}

次のパフォーマンス概要ダッシュボードで、データベース時間の概要と QPS を確認します。

![performance-overview-1-for-query-interface](/media/performance/j-1.png)

-   SQL タイプ別のデータベース時間: `Select`ステートメント タイプがほとんどの時間を費やします。
-   SQL フェーズ別のデータベース時間: フェーズ`execute`と`compile`にほとんどの時間がかかります。
-   SQL 実行時間の概要: `Get` 、および`tso wait` `Cop`ほとんどの時間がかかります。
-   タイプ別 CPS: `Query`コマンドのみが使用されます。
-   プラン キャッシュ OPS を使用したクエリ: データなしは、実行プラン キャッシュがヒットしていないことを示します。
-   クエリ期間では、レイテンシー`execute`と`compile`割合が最も高くなります。
-   平均QPS = 56.8k

クラスタのリソース消費量を確認すると、TiDB CPUの平均使用率は925%、TiKV CPUの平均使用率は201%、TiKV IOの平均スループットは18.7 MB/sでした。TiDBのリソース消費量が大幅に高くなっています。

![performance-overview-2-for-query-interface](/media/performance/5.png)

### 分析の結論 {#analysis-conclusion}

実行回数が多く、TiDB の CPU 使用率が高くなる原因となる、ビジネスには関係のない無駄な SQL ステートメントを排除する必要があります。

## シナリオ2. maxPerformance構成を使用する {#scenario-2-use-the-maxperformance-configuration}

### アプリケーション構成 {#application-configuration}

シナリオ1では、アプリケーションはJDBC接続文字列に新しいパラメータ`useConfigs=maxPerformance`を追加します。このパラメータを使用することで、JDBCからデータベースに送信されるSQL文（例： `select @@session.transaction_read_only` ）を削減できます。完全な設定は次のとおりです。

    useServerPrepStmts=false&useConfigs=maxPerformance

### パフォーマンス分析 {#performance-analysis}

#### TiDBダッシュボード {#tidb-dashboard}

下記の TiDB ダッシュボードのTop SQLページを見ると、最も多くのリソースを消費していた`SELECT @@session.tx_isolation`消えていることがわかります。

![dashboard-for-maxPerformance](/media/performance/case2.png)

次の TiDB のフレーム チャートから、SQL 実行中に`Compile`や`Optimize`などの関数の CPU 消費が依然として大きいことがわかります。

![flame-graph-for-maxPerformance](/media/performance/20220507-145257.jpg)

-   ExecuteStmt CPU = 43% CPU時間 =35.84秒
-   コンパイルCPU = 31% CPU時間 = 25.61秒
-   CPUを最適化 = 30% CPU時間 = 24.74秒

#### パフォーマンス概要ダッシュボード {#performance-overview-dashboard}

データベースの時間概要と QPS のデータは次のとおりです。

![performance-overview-1-for-maxPerformance](/media/performance/j-2.png)

-   SQL タイプ別のデータベース時間: `Select`ステートメント タイプがほとんどの時間を費やします。
-   SQL フェーズ別のデータベース時間: フェーズ`execute`と`compile`にほとんどの時間がかかります。
-   SQL 実行時間の概要: `Get` `Prewrite`および`tso wait` `Cop`ほとんどの時間がかかります。
-   データベース時間では、レイテンシー`execute`と`compile`割合が最も高くなります。
-   タイプ別 CPS: `Query`コマンドのみが使用されます。
-   平均QPS = 24.2k (56.3kから24.2k)
-   実行プラン キャッシュにヒットしません。

シナリオ 1 からシナリオ 2 にかけて、TiDB の平均 CPU 使用率は 925% から 874% に低下し、TiKV の平均 CPU 使用率は 201% から約 250% に増加します。

![performance-overview-2-for-maxPerformance](/media/performance/9.1.1.png)

主要なレイテンシーメトリックの変更は次のとおりです。

![performance-overview-3-for-maxPerformance](/media/performance/9.2.2.png)

-   平均クエリ実行時間 = 1.12ms (479μsから1.12ms)
-   平均解析時間 = 84.7μs (37.2μsから84.7μs)
-   平均コンパイル時間 = 370μs (166μsから370μs)
-   平均実行時間 = 626μs (251μsから626μs)

### 分析の結論 {#analysis-conclusion}

シナリオ1と比較して、シナリオ2のQPSは大幅に減少しました。平均クエリ実行時間と、 `parse` `compile` `execute`実行時間が大幅に増加しました。これは、シナリオ1の`select @@session.transaction_read_only`のような、実行回数が多く処理時間が短いSQL文が平均パフォーマンスデータを低下させたためです。シナリオ2ではこれらのSQL文がブロックされ、業務関連のSQL文のみが残るため、平均実行時間が増加します。

アプリケーションがクエリインターフェースを使用する場合、TiDBは実行プランキャッシュを使用できないため、実行プランのコンパイルに多くのリソースを消費します。このような場合は、TiDBの実行プランキャッシュを使用するPrepared Statementインターフェースの使用をお勧めします。Prepared Statementインターフェースは、実行プランのコンパイルによるTiDBのCPU消費量を削減し、レイテンシーを短縮します。

## シナリオ3. 実行プランのキャッシュを有効にせずにPrepared Statementインターフェースを使用する {#scenario-3-use-the-prepared-statement-interface-with-execution-plan-caching-not-enabled}

### アプリケーション構成 {#application-configuration}

アプリケーションは以下の接続構成を使用します。シナリオ2と比較すると、JDBCパラメータ`useServerPrepStmts`の値が`true`に変更されており、Prepared Statementインターフェースが有効になっていることを示しています。

    useServerPrepStmts=true&useConfigs=maxPerformance"

### パフォーマンス分析 {#performance-analysis}

#### TiDBダッシュボード {#tidb-dashboard}

次の TiDB のフレーム チャートから、Prepared Statement インターフェイスを有効にした後でも、 `CompileExecutePreparedStmt`と`Optimize`の CPU 消費量が依然として大きいことがわかります。

![flame-graph-for-PrepStmts](/media/performance/3.1.1.png)

-   ExecutePreparedStmt CPU = 31% CPU時間 = 23.10秒
-   preparedStmtExec CPU = 30% CPU時間 = 22.92秒
-   CompileExecutePreparedStmt CPU = 24% CPU時間 = 17.83秒
-   CPUを最適化 = 23% CPU時間 = 17.29秒

#### パフォーマンス概要ダッシュボード {#performance-overview-dashboard}

Prepared Statement インターフェイスを使用した後、データベース時間の概要と QPS のデータは次のようになります。

![performance-overview-1-for-PrepStmts](/media/performance/j-3.png)

QPSは24.4kから19.7kに低下しています。データベース時間の概要を見ると、アプリケーションが3種類のPreparedコマンドを使用しており、 `general`ステートメントタイプ（ `StmtPrepare`や`StmtClose`などのコマンドの実行時間を含む）がSQLタイプ別のデータベース時間で2番目に多いことがわかります。これは、Prepared Statementインターフェースを使用しても、実行プランキャッシュにヒットしていないことを示しています。これは、 `StmtClose`コマンド実行時に、TiDBが内部処理でSQL文の実行プランキャッシュをクリアするためです。

-   SQL タイプ別のデータベース時間: `Select`ステートメント タイプが最も時間がかかり、次に`general`ステートメントが続きます。
-   SQL フェーズ別のデータベース時間: フェーズ`execute`と`compile`にほとんどの時間がかかります。
-   SQL 実行時間の概要: `Get` `Prewrite`および`tso wait` `Cop`ほとんどの時間がかかります。
-   タイプ別 CPS: 3 種類のコマンド`StmtClose` `StmtPrepare` ) `StmtExecute`使用されます。
-   平均QPS = 19.7k (24.4kから19.7k)
-   実行プラン キャッシュにヒットしません。

TiDB の平均 CPU 使用率は 874% から 936% に増加します。

![performance-overview-1-for-PrepStmts](/media/performance/3-2.png)

主要なレイテンシーメトリックは次のとおりです。

![performance-overview-2-for-PrepStmts](/media/performance/3.4.png)

-   平均クエリ実行時間 = 528μs (1.12msから528μs)
-   平均解析時間 = 14.9μs (84.7μsから14.9μs)
-   平均コンパイル時間 = 374μs (370μsから374μs)
-   平均実行時間 = 649μs (626μsから649μs)

### 分析の結論 {#analysis-conclusion}

シナリオ2とは異なり、シナリオ3のアプリケーションはPrepared Statementインターフェースを有効にしていますが、それでもキャッシュにヒットしません。さらに、シナリオ2ではCPS By Typeコマンドの種類が1つ（ `Query` ）しかありませんが、シナリオ3ではコマンドの種類が3つ（ `StmtPrepare` ） `StmtClose`あります。シナリオ2と比較すると、シナリオ3 `StmtExecute`ネットワークのラウンドトリップ遅延が2つ多くなっています。

-   QPS の減少に関する分析： **「CPS By Type」**ペインを見ると、シナリオ 2 には「CPS By Type `StmtExecute`コマンドタイプが 1 つ ( `Query` ) しか存在しないのに対し、シナリオ 3 にはさらに 3 つのコマンドタイプ ( `StmtPrepare` ) が存在する`StmtClose` `StmtClose` `StmtPrepare`にカウントされない非従来型コマンドであるため、QPS が減少しています。非従来型コマンドの`StmtPrepare`と`StmtClose`は`general` SQL タイプにカウントされるため、シナリオ 3 のデータベース概要には`general`時間が表示され、これはデータベース時間の 4 分の 1 以上を占めています。
-   平均クエリ時間が大幅に短縮された理由の分析：シナリオ3で新たに追加されたコマンドタイプ`StmtPrepare`と`StmtClose`については、TiDB内部処理においてクエリ時間が個別に計算されます。TiDBはこれらの2種類のコマンドを非常に高速に実行するため、平均クエリ時間が大幅に短縮されます。

シナリオ3ではPrepared Statementインターフェースを使用していますが、多くのアプリケーションフレームワークはメモリリークを防ぐためにメソッド`StmtExecute`の後にメソッド`StmtClose`を呼び出すため、実行プランのキャッシュは依然としてアクセスされません。v6.0.0以降では、グローバル変数`tidb_ignore_prepared_cache_close_stmt=on;`を設定できます。その後、アプリケーションがメソッド`StmtClose`を呼び出しても、TiDBはキャッシュされた実行プランをクリアしません。そのため、次のSQL実行では既存の実行プランを再利用でき、実行プランの繰り返しコンパイルを回避できます。

## シナリオ4. Prepared Statement インターフェースを使用して実行プランのキャッシュを有効にする {#scenario-4-use-the-prepared-statement-interface-and-enable-execution-plan-caching}

### アプリケーション構成 {#application-configuration}

アプリケーション構成はシナリオ 3 と同じままです。アプリケーションが`StmtClose`トリガーしてもキャッシュにヒットしない問題を解決するために、次のパラメータが構成されています。

-   TiDB グローバル変数`set global tidb_ignore_prepared_cache_close_stmt=on;`を設定します (TiDB v6.0.0 以降に導入、デフォルトは`off` )。
-   プラン キャッシュ機能を有効にするには、TiDB 構成項目`prepared-plan-cache: {enabled: true}`を設定します。

### パフォーマンス分析 {#performance-analysis}

#### TiDBダッシュボード {#tidb-dashboard}

TiDB CPU 使用率のフレーム チャートから、 `CompileExecutePreparedStmt`と`Optimize` CPU 消費量が大幅に増加していないことがわかります。CPU の 25% は`Prepare`コマンドによって消費されており、これには`PlanBuilder`や`parseSQL`などの Prepare の解析関連の関数が含まれています。

PreparseStmt CPU = 25% CPU 時間 = 12.75秒

![flame-graph-for-3-commands](/media/performance/4.2.png)

#### パフォーマンス概要ダッシュボード {#performance-overview-dashboard}

パフォーマンス概要ダッシュボードで最も顕著な変化は、フェーズ`compile`の平均時間です。シナリオ3の8.95秒/秒から1.18秒/秒に短縮されています。実行プランキャッシュを使用するクエリの数は、 `StmtExecute`の値とほぼ等しくなります。QPSの増加に伴い、1秒あたり`Select`ステートメントのデータベース消費時間は減少し、1秒あたり`general`ステートメントのデータベース消費時間は増加しています。

![performance-overview-1-for-3-commands](/media/performance/j-4.png)

-   SQL タイプ別のデータベース時間: `Select`ステートメント タイプが最も時間がかかります。
-   SQL フェーズ別のデータベース時間: フェーズ`execute`がほとんどの時間を費やします。
-   SQL 実行時間の概要: `tso wait` 、および`Cop` `Get`ほとんどの時間がかかります。
-   実行プランキャッシュがヒットしました。プランキャッシュを使用するクエリのOPSの値は、1秒あたり約`StmtExecute`です。
-   CPSタイプ別: 3種類のコマンド（シナリオ3と同じ）
-   シナリオ 3 と比較すると、QPS が増加したため、 `general`ステートメントで消費される時間が長くなります。
-   平均QPS = 22.1k (19.7kから22.1k)

平均 TiDB CPU 使用率は 936% から 827% に低下します。

![performance-overview-2-for-3-commands](/media/performance/4.4.png)

平均`compile`の処理時間は374usから53.3usへと大幅に短縮されました。QPSが上昇したため、平均`execute`あたりの処理時間も増加しています。

![performance-overview-3-for-3-commands](/media/performance/4.5.png)

-   平均クエリ実行時間 = 426μs (528μsから426μs)
-   平均解析時間 = 12.3μs (14.8μsから12.3μs)
-   平均コンパイル時間 = 53.3μs (374μsから53.3μs)
-   平均実行時間 = 699μs (649μsから699us)

### 分析の結論 {#analysis-conclusion}

シナリオ3と比較すると、シナリオ4でも3種類のコマンドが使用されます。違いは、シナリオ4では実行プランキャッシュが使用されるため、コンパイル時間が大幅に短縮され、クエリの実行時間も短縮され、QPSが向上することです。

`StmtPrepare`と`StmtClose`コマンドはデータベース処理時間を大量に消費し、アプリケーションがSQL文を実行するたびにアプリケーションとTiDB間のやり取りの回数を増加させます。次のシナリオでは、JDBC設定を通じてこれらの2つのコマンドの呼び出しを削減することで、パフォーマンスをさらにチューニングします。

## シナリオ5. クライアント側で準備されたオブジェクトをキャッシュする {#scenario-5-cache-prepared-objects-on-the-client-side}

### アプリケーション構成 {#application-configuration}

シナリオ 4 と比較して、以下に説明するように、3 つの新しい JDBC パラメータ`cachePrepStmts=true&prepStmtCacheSize=1000&prepStmtCacheSqlLimit=20480`が構成されます。

-   `cachePrepStmts = true` : クライアント側で Prepared Statement オブジェクトをキャッシュし、StmtPrepare および StmtClose の呼び出しを排除します。
-   `prepStmtCacheSize` : 値は 0 より大きくなければなりません。
-   `prepStmtCacheSqlLimit` : 値は SQL テキストの長さより大きくなければなりません。

シナリオ 5 では、完全な JDBC 構成は次のようになります。

    useServerPrepStmts=true&cachePrepStmts=true&prepStmtCacheSize=1000&prepStmtCacheSqlLimit=20480&useConfigs=maxPerformance

### パフォーマンス分析 {#performance-analysis}

#### TiDBダッシュボード {#tidb-dashboard}

次の TiDB のフレーム チャートから、コマンド`Prepare`の高い CPU 消費がなくなったことがわかります。

-   ExecutePreparedStmt CPU = 22% CPU時間 = 8.4秒

![flame-graph-for-1-command](/media/performance/5.1.1.png)

#### パフォーマンス概要ダッシュボード {#performance-overview-dashboard}

パフォーマンス概要ダッシュボードで最も注目すべき変更点は、 **CPS By Type**ペインの 3 つの Stmt コマンド タイプが 1 つに減り、 **Database Time by SQL Type**ペインの`general`ステートメント タイプが消え、 **QPS**ペインの QPS が 30.9k に増加したことです。

![performance-overview-for-1-command](/media/performance/j-5.png)

-   SQL タイプ別のデータベース時間: `Select`ステートメント タイプが最も多くの時間を費やし、 `general`ステートメント タイプは消えます。
-   SQL フェーズ別のデータベース時間: フェーズ`execute`がほとんどの時間を費やします。
-   SQL 実行時間の概要: `tso wait` 、および`Cop` `Get`ほとんどの時間がかかります。
-   実行プランキャッシュがヒットしました。プランキャッシュを使用するクエリのOPSの値は、1秒あたり約`StmtExecute`です。
-   タイプ別 CPS: `StmtExecute`コマンドのみが使用されます。
-   平均QPS = 30.9k (22.1kから30.9k)

TiDBの平均CPU使用率は827%から577%に低下しました。QPSが増加すると、TiKVの平均CPU使用率は313%に増加しました。

![performance-overview-for-2-command](/media/performance/j-5-cpu.png)

主要なレイテンシーメトリックは次のとおりです。

![performance-overview-for-3-command](/media/performance/j-5-duration.png)

-   平均クエリ実行時間 = 690μs (426μsから690μs)
-   平均解析時間 = 13.5μs (12.3μsから13.5μs)
-   平均コンパイル時間 = 49.7μs (53.3μsから49.7μs)
-   平均実行時間 = 623μs (699us から 623μs)
-   平均 pd tso 待機時間 = 196μs (224μs から 196μs)
-   接続アイドル時間 avg-in-txn = 608μs (250μsから608μs)

### 分析の結論 {#analysis-conclusion}

-   シナリオ 4 と比較すると、シナリオ 5 の**CPS By Type**ペインには`StmtExecute`コマンドのみがあり、これにより 2 回のネットワーク ラウンド トリップが回避され、システム全体の QPS が向上します。
-   QPSが増加すると、解析時間、コンパイル時間、実行時間の観点からレイテンシーは減少しますが、クエリ時間は増加します。これは、TiDBが`StmtPrepare`と`StmtClose`非常に高速に処理するため、これら2つのコマンドタイプを削除すると平均クエリ時間が増加するためです。
-   SQLフェーズ別データベース時間では、 `execute`最も時間がかかり、データベース時間とほぼ一致しています。一方、SQL実行時間の概要では、 `tso wait`最も時間がかかり、 `execute`の4分の1以上がTSOの待機に費やされています。
-   1秒あたり`tso wait`回の実行時間の合計は5.46秒です。3 `tso wait`実行時間の平均は196マイクロ秒、1秒あたり`tso cmd`回の実行時間は28,000回で、QPSの30,900に非常に近い値です。これは、TiDBの分離レベル`read committed`の実装により、トランザクション内のすべてのSQL文がPDにTSOを要求する必要があるためです。

TiDB v6.0 は`rc read`提供します。これは`tso cmd`削減することで`read committed`分離レベルを最適化します。この機能はグローバル変数`set global tidb_rc_read_check_ts=on;`によって制御されます。この変数を有効にすると、TiDB のデフォルトの動作は`repeatable-read`分離レベルと同じように動作し、PD から取得する必要があるのは`start-ts`と`commit-ts`です。トランザクション内のステートメントは、最初に`start-ts`使用して TiKV からデータを読み取ります。TiKV から読み取られたデータが`start-ts`より前の場合、データは直接返されます。TiKV から読み取られたデータが`start-ts`より後の場合、データは破棄されます。TiDB は PD から TSO を要求し、読み取りを再試行します。後続のステートメントの`for update ts`では、最新の PD TSO が使用されます。

## シナリオ6: <code>tidb_rc_read_check_ts</code>変数を有効にしてTSOリクエストを削減する {#scenario-6-enable-the-code-tidb-rc-read-check-ts-code-variable-to-reduce-tso-requests}

### アプリケーション構成 {#application-configuration}

シナリオ5と比較すると、アプリケーション構成は同じです。唯一の違いは、変数`set global tidb_rc_read_check_ts=on;`がTSOリクエストを削減するように設定されていることです。

### パフォーマンス分析 {#performance-analysis}

#### ダッシュボード {#dashboard}

TiDB CPU のフレーム チャートには大きな変化はありません。

-   ExecutePreparedStmt CPU = 22% CPU時間 = 8.4秒

![flame-graph-for-rc-read](/media/performance/6.2.2.png)

#### パフォーマンス概要ダッシュボード {#performance-overview-dashboard}

RC 読み取りを使用した後、QPS は 30.9k から 34.9k に増加し、 `tso wait`秒あたりに消費される時間は 5.46 秒から 456 ミリ秒に減少します。

![performance-overview-1-for-rc-read](/media/performance/j-6.png)

-   SQL タイプ別のデータベース時間: `Select`ステートメント タイプがほとんどの時間を費やします。
-   SQL フェーズ別のデータベース時間: フェーズ`execute`がほとんどの時間を費やします。
-   SQL 実行時間の概要: `Get` 、および`Prewrite` `Cop`ほとんどの時間がかかります。
-   実行プランキャッシュがヒットしました。プランキャッシュを使用するクエリのOPSの値は、1秒あたり約`StmtExecute`です。
-   タイプ別 CPS: `StmtExecute`コマンドのみが使用されます。
-   平均QPS = 34.9k (30.9kから34.9k)

1秒あたり`tso cmd`は28.3kから2.7kに減少します。

![performance-overview-2-for-rc-read](/media/performance/j-6-cmd.png)

平均 TiDB CPU は 603% に増加します (577% から 603%)。

![performance-overview-3-for-rc-read](/media/performance/j-6-cpu.png)

主要なレイテンシーメトリックは次のとおりです。

![performance-overview-4-for-rc-read](/media/performance/j-6-duration.png)

-   平均クエリ実行時間 = 533μs (690μsから533μs)
-   平均解析時間 = 13.4μs (13.5μsから13.4μs)
-   平均コンパイル時間 = 50.3μs (49.7μsから50.3μs)
-   平均実行時間 = 466μs (623μsから466μs)
-   平均 pd tso 待機時間 = 171μs (196μs から 171μs)

### 分析の結論 {#analysis-conclusion}

RC Read を`set global tidb_rc_read_check_ts=on;`有効にした後、RC Read によって`tso cmd`の時間が大幅に短縮され、 `tso wait`と平均クエリ期間が短縮され、QPS が向上しました。

現在のデータベース時間とレイテンシーの両方のボトルネックはフェーズ`execute`にあり、このフェーズでは`Get`と`Cop`の読み取りリクエストが最も高い割合を占めています。このワークロードのテーブルのほとんどは読み取り専用か、ほとんど変更されないため、TiDB v6.0.0以降でサポートされている小さなテーブルのキャッシュ機能を使用して、これらの小さなテーブルのデータをキャッシュすることで、KV読み取りリクエストの待機時間とリソース消費を削減できます。

## シナリオ7: 小さなテーブルキャッシュを使用する {#scenario-7-use-the-small-table-cache}

### アプリケーション構成 {#application-configuration}

シナリオ6と比較して、アプリケーション構成は同じです。唯一の違いは、シナリオ7では、ビジネス用に読み取り専用テーブルをキャッシュするために、 `alter table t1 cache;`ようなSQL文を使用する点です。

### パフォーマンス分析 {#performance-analysis}

#### TiDBダッシュボード {#tidb-dashboard}

TiDB CPU のフレーム チャートには大きな変化はありません。

![flame-graph-for-table-cache](/media/performance/7.2.png)

#### パフォーマンス概要ダッシュボード {#performance-overview-dashboard}

QPSは34.9kから40.9kに増加し、KVリクエストタイプはフェーズ`execute`からフェーズ`Prewrite`とフェーズ`Commit`への変更で最も時間がかかります。1秒あたり`Get`のデータベース処理時間は5.33秒から1.75秒に短縮され、1秒あたり`Cop`のデータベース処理時間は3.87秒から1.09秒に短縮されます。

![performance-overview-1-for-table-cache](/media/performance/j-7.png)

-   SQL タイプ別のデータベース時間: `Select`ステートメント タイプがほとんどの時間を費やします。
-   SQL フェーズ別のデータベース時間: フェーズ`execute`と`compile`にほとんどの時間がかかります。
-   SQL 実行時間の概要: `Prewrite` 、および`Get` `Commit`ほとんどの時間がかかります。
-   実行プランキャッシュがヒットしました。プランキャッシュを使用するクエリのOPSの値は、1秒あたり約`StmtExecute`です。
-   タイプ別 CPS: `StmtExecute`コマンドのみが使用されます。
-   平均QPS = 40.9k (34.9kから40.9k)

平均 TiDB CPU 使用率は 603% から 478% に低下し、平均 TiKV CPU 使用率は 346% から 256% に低下します。

![performance-overview-2-for-table-cache](/media/performance/j-7-cpu.png)

平均クエリレイテンシーは533usから313usに短縮されました。平均`execute`レイテンシーは466usから250usに短縮されました。

![performance-overview-3-for-table-cache](/media/performance/j-7-duration.png)

-   平均クエリ実行時間 = 313μs (533μsから313μs)
-   平均解析時間 = 11.9μs (13.4μsから11.9μs)
-   平均コンパイル時間 = 47.7μs (50.3μsから47.7μs)
-   平均実行時間 = 251μs (466μsから251μs)

### 分析の結論 {#analysis-conclusion}

すべての読み取り専用テーブルをキャッシュした後、 `Execute Duration`は大幅に低下します。これは、すべての読み取り専用テーブルが TiDB にキャッシュされ、それらのテーブルに対して TiKV でデータをクエリする必要がないため、クエリ期間が短縮され、QPS が増加するためです。

これは楽観的結果です。実際の業務では、読み取り専用テーブルのデータはTiDBがすべてをキャッシュするには大きすぎる可能性があります。また、小さなテーブルのキャッシュ機能は書き込み操作をサポートしますが、書き込み操作にはデフォルトで3秒間の待機時間が必要であり、これはすべてのTiDBノードのキャッシュが無効化されることを保証するためです。これは、レイテンシー要件が厳しいアプリケーションには適さない可能性があります。

## まとめ {#summary}

次の表には、7 つの異なるシナリオのパフォーマンスが示されています。

| メトリクス | シナリオ1 | シナリオ2  | シナリオ3 | シナリオ4 | シナリオ5 | シナリオ6 | シナリオ7 | シナリオ5とシナリオ2の比較（％） | シナリオ7とシナリオ3の比較（％） |
| ----- | ----- | ------ | ----- | ----- | ----- | ----- | ----- | ----------------- | ----------------- |
| クエリ期間 | 479μs | 1120μs | 528μs | 426μs | 690μs | 533μs | 313μs | -38%              | -41%              |
| QPS   | 56.3k | 24.2k  | 19.7k | 22.1k | 30.9k | 34.9k | 40.9k | +28%              | +108%             |

これらのシナリオでは、シナリオ 2 はアプリケーションがクエリ インターフェイスを使用する一般的なシナリオであり、シナリオ 5 はアプリケーションが準備済みステートメント インターフェイスを使用する理想的なシナリオです。

-   シナリオ 5 とシナリオ 2 を比較すると、 Javaアプリケーション開発のベスト プラクティスを使用し、クライアント側で Prepared Statement オブジェクトをキャッシュすることで、各 SQL ステートメントで実行プラン キャッシュをヒットするために必要なコマンドとデータベース操作が 1 つだけになり、クエリのレイテンシーが 38% 短縮され、QPS が 28% 増加し、TiDB の平均 CPU 使用率が 936% から 577% に低下していることがわかります。
-   シナリオ 7 とシナリオ 3 を比較すると、シナリオ 5 に RC 読み取りや小さなテーブル キャッシュなどの最新の TiDB 最適化機能を追加すると、レイテンシーが41% 削減され、QPS が 108% 増加し、平均 TiDB CPU 使用率が 936% から 478% に低下することがわかります。

各シナリオのパフォーマンスを比較すると、次のような結論を導き出すことができます。

-   TiDBの実行計画キャッシュは、OLTPパフォーマンスチューニングにおいて重要な役割を果たします。バージョン6.0.0から導入されたRC Read機能とスモールテーブルキャッシュ機能も、このワークロードのさらなるパフォーマンスチューニングにおいて重要な役割を果たします。

-   TiDBはMySQLプロトコルの様々なコマンドと互換性があります。Prepared Statementインターフェースを使用し、以下のJDBC接続パラメータを設定することで、アプリケーションは最高のパフォーマンスを実現できます。

        useServerPrepStmts=true&cachePrepStmts=true&prepStmtCacheSize=1000&prepStmtCacheSqlLimit=20480&useConfigs=maxPerformance

-   パフォーマンス分析とチューニングには、TiDB ダッシュボード (たとえば、 Top SQL機能や継続的なプロファイリング機能) とパフォーマンス概要ダッシュボードを使用することをお勧めします。

    -   [Top SQL](/dashboard/top-sql.md)機能を使用すると、実行中にデータベース内の各 SQL ステートメントの CPU 消費量を視覚的に監視および調査して、データベースのパフォーマンスの問題をトラブルシューティングできます。
    -   [継続的なプロファイリング](/dashboard/continuous-profiling.md)使用すると、TiDB、TiKV、PD の各インスタンスからパフォーマンスデータを継続的に収集できます。アプリケーションが TiDB とやり取りするために異なるインターフェースを使用する場合、TiDB の CPU 消費量に大きな差が生じます。
    -   [パフォーマンス概要ダッシュボード](/grafana-performance-overview-dashboard.md)使用すると、データベース時間とSQL実行時間の内訳情報の概要を取得できます。データベース時間に基づいてパフォーマンスを分析・診断することで、システム全体のパフォーマンスボトルネックがTiDBにあるかどうかを判断できます。ボトルネックがTiDBにある場合は、データベース時間とレイテンシーの内訳、負荷プロファイル、リソース使用率を使用して、TiDB内のパフォーマンスボトルネックを特定し、それに応じてパフォーマンスを調整できます。

これらの機能を組み合わせて使用​​することで、実際のアプリケーションのパフォーマンスを効率的に分析および調整できます。
