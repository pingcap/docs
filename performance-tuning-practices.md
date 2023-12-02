---
title: Performance Tuning Practices for OLTP Scenarios
summary: This document describes how to analyze and tune performance for OLTP workloads.
---

# OLTP シナリオの性能チューニングの実践 {#performance-tuning-practices-for-oltp-scenarios}

TiDB は、TiDB ダッシュボードの[Top SQL](/dashboard/top-sql.md)および[継続的なプロファイリング](/dashboard/continuous-profiling.md)の機能や TiDB [パフォーマンス概要ダッシュボード](/grafana-performance-overview-dashboard.md)など、包括的なパフォーマンス診断および分析機能を提供します。

このドキュメントでは、これらの機能を組み合わせて使用​​し、7 つの異なるランタイム シナリオで同じ OLTP ワークロードのパフォーマンスを分析および比較する方法について説明します。これは、TiDB のパフォーマンスを効率的に分析および調整するのに役立つパフォーマンス チューニング プロセスを示しています。

> **注記：**
>
> [Top SQL](/dashboard/top-sql.md)と[継続的なプロファイリング](/dashboard/continuous-profiling.md)デフォルトでは有効になっていません。事前に有効にしておく必要があります。

このドキュメントでは、これらのシナリオで同じアプリケーションを異なる JDBC 構成で実行することにより、アプリケーションとデータベース間のさまざまな相互作用によってシステム全体のパフォーマンスがどのような影響を受けるかを示し、パフォーマンスを向上させるために[TiDB を使用したJavaアプリケーション開発のベスト プラクティス](/best-practices/java-app-best-practices.md)を適用できるようにします。

## 環境の説明 {#environment-description}

このドキュメントでは、デモのためにコア バンキング OLTP ワークロードを取り上げます。シミュレーション環境の構成は以下のとおりです。

-   ワークロード用のアプリケーション開発言語: JAVA
-   ビジネスで使用するSQL文：合計200文、うち90％がSELECT文。これは、典型的な読み取り負荷の高い OLTP ワークロードです。
-   トランザクションで使用されるテーブル: 合計 60 テーブル。 12 のテーブルには更新操作が含まれており、残りの 48 のテーブルは読み取り専用です。
-   アプリケーションで使用される分離レベル: `read committed` 。
-   TiDB クラスター構成: 3 つの TiDB ノードと 3 つの TiKV ノード、各ノードに 16 個の CPU が割り当てられます。
-   クライアントサーバー構成: 36 CPU。

## シナリオ 1. クエリ インターフェイスを使用する {#scenario-1-use-the-query-interface}

### アプリケーション構成 {#application-configuration}

アプリケーションは、次の JDBC 構成を使用して、Query インターフェイスを通じてデータベースに接続します。

    useServerPrepStmts=false

### パフォーマンス分析 {#performance-analysis}

#### TiDB ダッシュボード {#tidb-dashboard}

以下の TiDB ダッシュボードの[Top SQL]ページから、非ビジネス SQL タイプ`SELECT @@session.tx_isolation`が最も多くのリソースを消費していることがわかります。 TiDB はこれらのタイプの SQL ステートメントを迅速に処理しますが、これらのタイプの SQL ステートメントは実行回数が最も多く、全体的な CPU 時間の消費量が最も多くなります。

![dashboard-for-query-interface](/media/performance/case1.png)

以下の TiDB のフレーム チャートから、SQL 実行中に`Compile`や`Optimize`などの関数の CPU 消費量が大きくなることがわかります。アプリケーションはクエリ インターフェイスを使用するため、TiDB は実行プラン キャッシュを使用できません。 TiDB は、各 SQL ステートメントの実行プランをコンパイルして生成する必要があります。

![flame-graph-for-query-interface](/media/performance/7.1.png)

-   ExecuteStmt CPU = 38% CPU 時間 = 23.84 秒
-   コンパイル CPU = 27% CPU 時間 = 17.17 秒
-   CPU の最適化 = 26% CPU 時間 = 16.41 秒

#### パフォーマンス概要ダッシュボード {#performance-overview-dashboard}

次のパフォーマンス概要ダッシュボードでデータベース時間の概要と QPS を確認してください。

![performance-overview-1-for-query-interface](/media/performance/j-1.png)

-   SQL タイプ別のデータベース時間: `Select`ステートメント タイプがほとんどの時間を要します。
-   SQL フェーズごとのデータベース時間: ほとんどの時間がかかるのは`execute`フェーズと`compile`フェーズです。
-   SQL 実行時間の概要: `Get` 、 `Cop` 、および`tso wait`にほとんどの時間がかかります。
-   CPS By Type: `Query`コマンドのみが使用されます。
-   プラン キャッシュ OPS を使用したクエリ: データがない場合は、実行プラン キャッシュがヒットしないことを示します。
-   クエリ期間では、レイテンシー`execute`と`compile`が最も高い割合を占めます。
-   平均 QPS = 56.8k

クラスターのリソース消費量を確認します。TiDB CPU の平均使用率は 925%、TiKV CPU の平均使用率は 201%、TiKV IO の平均スループットは 18.7 MB/秒です。 TiDB のリソース消費量は大幅に多くなります。

![performance-overview-2-for-query-interface](/media/performance/5.png)

### 分析の結論 {#analysis-conclusion}

これらの無駄な非ビジネス SQL ステートメントは、実行回数が多く、TiDB の CPU 使用率が高くなる原因となるため、削除する必要があります。

## シナリオ 2. maxPerformance 構成を使用する {#scenario-2-use-the-maxperformance-configuration}

### アプリケーション構成 {#application-configuration}

アプリケーションは、シナリオ 1 の JDBC 接続文字列に新しいパラメーター`useConfigs=maxPerformance`を追加します。このパラメーターを使用すると、JDBC からデータベースに送信される SQL ステートメント (たとえば、 `select @@session.transaction_read_only` ) を削除できます。完全な構成は次のとおりです。

    useServerPrepStmts=false&useConfigs=maxPerformance

### パフォーマンス分析 {#performance-analysis}

#### TiDB ダッシュボード {#tidb-dashboard}

以下の TiDB ダッシュボードの[Top SQL]ページから、最も多くのリソースを消費した`SELECT @@session.tx_isolation`が消えていることがわかります。

![dashboard-for-maxPerformance](/media/performance/case2.png)

次の TiDB のフレーム チャートから、 `Compile`や`Optimize`などの関数の CPU 消費量が SQL 実行中に依然として顕著であることがわかります。

![flame-graph-for-maxPerformance](/media/performance/20220507-145257.jpg)

-   ExecuteStmt CPU = 43% CPU 時間 =35.84 秒
-   コンパイル CPU = 31% CPU 時間 =25.61 秒
-   CPU の最適化 = 30% CPU 時間 = 24.74 秒

#### パフォーマンス概要ダッシュボード {#performance-overview-dashboard}

データベース時間概要とQPSのデータは以下のとおりです。

![performance-overview-1-for-maxPerformance](/media/performance/j-2.png)

-   SQL タイプ別のデータベース時間: `Select`ステートメント タイプがほとんどの時間を要します。
-   SQL フェーズごとのデータベース時間: ほとんどの時間がかかるのは`execute`フェーズと`compile`フェーズです。
-   SQL 実行時間の概要: `Get` 、 `Cop` 、 `Prewrite` 、および`tso wait`にほとんどの時間がかかります。
-   データベース時間では、 `execute`と`compile`のレイテンシーが最も高い割合を占めます。
-   CPS By Type: `Query`コマンドのみが使用されます。
-   平均 QPS = 24.2k (56.3k から 24.2k)
-   実行プランのキャッシュがヒットしません。

シナリオ 1 からシナリオ 2 にかけて、平均 TiDB CPU 使用率は 925% から 874% に低下し、平均 TiKV CPU 使用率は 201% から約 250% に増加します。

![performance-overview-2-for-maxPerformance](/media/performance/9.1.1.png)

主要なレイテンシー指標の変更は次のとおりです。

![performance-overview-3-for-maxPerformance](/media/performance/9.2.2.png)

-   平均クエリ時間 = 1.12ms (479μs から 1.12ms)
-   平均解析時間 = 84.7μs (37.2μs から 84.7μs)
-   平均コンパイル時間 = 370μs (166μs から 370μs)
-   平均実行時間 = 626μs (251μs から 626μs)

### 分析の結論 {#analysis-conclusion}

シナリオ 1 と比較して、シナリオ 2 の QPS は大幅に低下しています。平均クエリ期間と平均`parse` 、 `compile` 、および`execute`の期間は大幅に増加しました。これは、シナリオ 1 の`select @@session.transaction_read_only`のような、実行回数が多く処理時間が速い SQL ステートメントは、平均パフォーマンス データを低下させるためです。シナリオ 2 でそのようなステートメントがブロックされた後は、ビジネス関連の SQL ステートメントのみが残るため、平均所要時間は長くなります。

アプリケーションが Query インターフェイスを使用する場合、TiDB は実行プラン キャッシュを使用できないため、TiDB は実行プランをコンパイルするために大量のリソースを消費します。この場合、Prepared Statement インターフェイスを使用することをお勧めします。これは、TiDB の実行プラン キャッシュを使用して、実行プランのコンパイルによって発生する TiDB CPU 消費量を削減し、レイテンシーを短縮します。

## シナリオ 3. 実行プランのキャッシュが有効になっていない状態で Prepared Statement インターフェイスを使用する {#scenario-3-use-the-prepared-statement-interface-with-execution-plan-caching-not-enabled}

### アプリケーション構成 {#application-configuration}

アプリケーションは次の接続構成を使用します。シナリオ 2 と比較すると、JDBC パラメーター`useServerPrepStmts`の値が`true`に変更されており、Prepared Statement インターフェイスが有効であることが示されています。

    useServerPrepStmts=true&useConfigs=maxPerformance"

### パフォーマンス分析 {#performance-analysis}

#### TiDB ダッシュボード {#tidb-dashboard}

次の TiDB のフレーム チャートから、Prepared Statement インターフェイスが有効になった後も、 `CompileExecutePreparedStmt`と`Optimize`の CPU 消費量が依然として顕著であることがわかります。

![flame-graph-for-PrepStmts](/media/performance/3.1.1.png)

-   ExecutePreparedStmt CPU = 31% CPU 時間 = 23.10 秒
-   prepareStmtExec CPU = 30% CPU 時間 = 22.92 秒
-   CompileExecutePreparedStmt CPU = 24% CPU 時間 = 17.83 秒
-   CPU の最適化 = 23% CPU 時間 = 17.29 秒

#### パフォーマンス概要ダッシュボード {#performance-overview-dashboard}

Prepared Statement インターフェイスを使用した後のデータベース時間の概要と QPS のデータは次のようになります。

![performance-overview-1-for-PrepStmts](/media/performance/j-3.png)

QPS は 24.4k から 19.7k に低下します。データベース時間の概要から、アプリケーションは 3 種類の準備済みコマンドを使用しており、 `general`ステートメント タイプ ( `StmtPrepare`や`StmtClose`などのコマンドの実行時間を含む) が SQL タイプ別のデータベース時間で 2 位になっていることがわかります。これは、Prepared Statement インターフェイスが使用されても、実行プラン キャッシュにヒットしないことを示しています。その理由は、 `StmtClose`コマンドが実行されると、TiDB が内部処理で SQL ステートメントの実行プラン キャッシュをクリアするためです。

-   SQL タイプ別のデータベース時間: `Select`ステートメント タイプがほとんどの時間を要し、次に`general`ステートメントが続きます。
-   SQL フェーズごとのデータベース時間: ほとんどの時間がかかるのは`execute`フェーズと`compile`フェーズです。
-   SQL 実行時間の概要: `Get` 、 `Cop` 、 `Prewrite` 、および`tso wait`にほとんどの時間がかかります。
-   CPS By Type: 3 種類のコマンド ( `StmtPrepare` 、 `StmtExecute` 、 `StmtClose` ) が使用されます。
-   平均 QPS = 19.7k (24.4k から 19.7k)
-   実行プランのキャッシュがヒットしません。

TiDB の平均 CPU 使用率は 874% から 936% に増加しました。

![performance-overview-1-for-PrepStmts](/media/performance/3-2.png)

主要なレイテンシーメトリクスは次のとおりです。

![performance-overview-2-for-PrepStmts](/media/performance/3.4.png)

-   平均クエリ時間 = 528μs (1.12ms から 528μs)
-   平均解析時間 = 14.9μs (84.7μs から 14.9μs)
-   平均コンパイル時間 = 374μs (370μs から 374μs)
-   平均実行時間 = 649μs (626μs から 649μs)

### 分析の結論 {#analysis-conclusion}

シナリオ 2 とは異なり、シナリオ 3 のアプリケーションは Prepared Statement インターフェイスを有効にしますが、依然としてキャッシュにヒットできません。さらに、シナリオ 2 には CPS By Type コマンド タイプ ( `Query` ) が 1 つだけありますが、シナリオ 3 にはさらに 3 つのコマンド タイプ ( `StmtPrepare` 、 `StmtExecute` 、 `StmtClose` ) があります。シナリオ 2 と比較して、シナリオ 3 ではネットワークの往復遅延が 2 つ増えています。

-   QPS の減少の分析: **[CPS By Type]**ペインから、シナリオ 2 には CPS By Type コマンド タイプ ( `Query` ) が 1 つだけあるのに対し、シナリオ 3 にはさらに 3 つのコマンド タイプ ( `StmtPrepare` 、 `StmtExecute` 、 `StmtClose` ) があることがわかります。 `StmtPrepare`と`StmtClose`は QPS でカウントされない非従来コマンドであるため、QPS が低下します。特殊なコマンド`StmtPrepare`と`StmtClose` `general` SQL タイプにカウントされるため、シナリオ 3 のデータベース概要には`general`時間が表示され、データベース時間の 4 分の 1 以上を占めます。
-   平均クエリ時間の大幅な減少の分析: シナリオ 3 で新たに追加された`StmtPrepare`および`StmtClose`コマンド タイプについては、それらのクエリ時間は TiDB 内部処理で個別に計算されます。 TiDB はこれら 2 種類のコマンドを非常に高速に実行するため、平均クエリ時間が大幅に短縮されます。

シナリオ 3 では Prepared Statement インターフェイスを使用しますが、多くのアプリケーション フレームワークはメモリリークを防ぐために`StmtExecute`の後に`StmtClose`メソッドを呼び出すため、実行プラン キャッシュは依然としてヒットしません。 v6.0.0 以降、グローバル変数`tidb_ignore_prepared_cache_close_stmt=on;`を設定できるようになりました。その後、アプリケーションが`StmtClose`メソッドを呼び出した場合でも、TiDB はキャッシュされた実行プランをクリアしないため、次回の SQL 実行では既存の実行プランを再利用し、実行プランを繰り返しコンパイルすることを回避できます。

## シナリオ 4. Prepared Statement インターフェイスを使用し、実行プランのキャッシュを有効にする {#scenario-4-use-the-prepared-statement-interface-and-enable-execution-plan-caching}

### アプリケーション構成 {#application-configuration}

アプリケーションの構成はシナリオ 3 と同じままです。アプリケーションが`StmtClose`トリガーしてもキャッシュにヒットしない問題を解決するために、次のパラメーターが構成されます。

-   TiDB グローバル変数`set global tidb_ignore_prepared_cache_close_stmt=on;`を設定します (TiDB v6.0.0 以降、デフォルトでは`off`が導入されました)。
-   TiDB 構成項目`prepared-plan-cache: {enabled: true}`を設定して、プラン キャッシュ機能を有効にします。

### パフォーマンス分析 {#performance-analysis}

#### TiDB ダッシュボード {#tidb-dashboard}

TiDB CPU 使用率のフレーム チャートから、 `CompileExecutePreparedStmt`と`Optimize`では大きな CPU 消費がないことがわかります。 CPU の 25% は、 `PlanBuilder`や`parseSQL`などの Prepare の解析関連関数を含む`Prepare`コマンドによって消費されます。

PreparseStmt CPU = 25% CPU 時間 = 12.75 秒

![flame-graph-for-3-commands](/media/performance/4.2.png)

#### パフォーマンス概要ダッシュボード {#performance-overview-dashboard}

[パフォーマンス概要] ダッシュボードで最も重要な変更は`compile`フェーズの平均時間で、シナリオ 3 の 8.95 秒/秒から 1.18 秒/秒に短縮されます。実行プラン キャッシュを使用するクエリの数は、値`StmtExecute`にほぼ等しくなります。 QPS が増加すると、1 秒あたり`Select`ステートメントで消費されるデータベース時間が減少し、1 秒あたり`general`ステートメントのタイプで消費されるデータベース時間が増加します。

![performance-overview-1-for-3-commands](/media/performance/j-4.png)

-   SQL タイプ別のデータベース時間: `Select`ステートメント タイプが最も時間がかかります。
-   SQL フェーズごとのデータベース時間: `execute`フェーズにほとんどの時間がかかります。
-   SQL 実行時間の概要: `tso wait` 、 `Get` 、および`Cop`にほとんどの時間がかかります。
-   実行計画キャッシュがヒットしました。プラン キャッシュを使用したクエリ OPS の値は、1 秒あたり`StmtExecute`にほぼ等しくなります。
-   CPS By Type: 3 種類のコマンド (シナリオ 3 と同じ)
-   シナリオ 3 と比較すると、QPS が増加するため、 `general`ステートメントにかかる時間が長くなります。
-   平均 QPS = 22.1k (19.7k から 22.1k)

TiDB の平均 CPU 使用率は 936% から 827% に低下します。

![performance-overview-2-for-3-commands](/media/performance/4.4.png)

平均`compile`時間は 374 us から 53.3 us へと大幅に減少しました。 QPSが上がるので平均`execute`回も伸びます。

![performance-overview-3-for-3-commands](/media/performance/4.5.png)

-   平均クエリ時間 = 426μs (528μs から 426μs)
-   平均解析時間 = 12.3μs (14.8μs から 12.3μs)
-   平均コンパイル時間 = 53.3μs (374μs から 53.3μs)
-   平均実行時間 = 699μs (649μs から 699us)

### 分析の結論 {#analysis-conclusion}

シナリオ 3 と比較すると、シナリオ 4 でも 3 種類のコマンドが使用されます。違いは、シナリオ 4 では実行プラン キャッシュがヒットするため、コンパイル時間が大幅に短縮され、クエリ時間が短縮され、QPS が向上します。

`StmtPrepare`と`StmtClose`コマンドはデータベース時間を大幅に消費し、アプリケーションが SQL ステートメントを実行するたびにアプリケーションと TiDB の間の対話の数が増加するためです。次のシナリオでは、JDBC 構成を通じてこれら 2 つのコマンドの呼び出しを排除することで、パフォーマンスをさらに調整します。

## シナリオ 5. クライアント側で準備されたオブジェクトをキャッシュする {#scenario-5-cache-prepared-objects-on-the-client-side}

### アプリケーション構成 {#application-configuration}

シナリオ 4 と比較すると、以下で説明するように、3 つの新しい JDBC パラメーター`cachePrepStmts=true&prepStmtCacheSize=1000&prepStmtCacheSqlLimit=20480`が構成されています。

-   `cachePrepStmts = true` : Prepared Statement オブジェクトをクライアント側でキャッシュし、StmtPrepare および StmtClose の呼び出しを排除します。
-   `prepStmtCacheSize` : 値は 0 より大きくなければなりません。
-   `prepStmtCacheSqlLimit` : 値は SQL テキストの長さより大きくなければなりません。

シナリオ 5 の完全な JDBC 構成は次のとおりです。

    useServerPrepStmts=true&cachePrepStmts=true&prepStmtCacheSize=1000&prepStmtCacheSqlLimit=20480&useConfigs=maxPerformance

### パフォーマンス分析 {#performance-analysis}

#### TiDB ダッシュボード {#tidb-dashboard}

TiDB の次のフレーム チャートから、 `Prepare`コマンドによる高い CPU 消費量がなくなっていることがわかります。

-   ExecutePreparedStmt CPU = 22% CPU 時間 = 8.4 秒

![flame-graph-for-1-command](/media/performance/5.1.1.png)

#### パフォーマンス概要ダッシュボード {#performance-overview-dashboard}

[パフォーマンス概要] ダッシュボードでの最も注目すべき変更は、 **[タイプ別 CPS]**ペインの 3 つの Stmt コマンド タイプが 1 つのタイプに減り、 **[SQL タイプ別データベース時間]**ペインの`general`のステートメント タイプが消え、 **[QPS]**ペインの QPS です。 30.9kまで増加します。

![performance-overview-for-1-command](/media/performance/j-5.png)

-   SQL タイプ別のデータベース時間: `Select`ステートメント タイプがほとんどの時間を要し、 `general`ステートメント タイプは消滅します。
-   SQL フェーズごとのデータベース時間: `execute`フェーズにほとんどの時間がかかります。
-   SQL 実行時間の概要: `tso wait` 、 `Get` 、および`Cop`にほとんどの時間がかかります。
-   実行計画キャッシュがヒットしました。プラン キャッシュを使用したクエリ OPS の値は、1 秒あたり`StmtExecute`にほぼ等しくなります。
-   CPS By Type: `StmtExecute`コマンドのみが使用されます。
-   平均 QPS = 30.9k (22.1k から 30.9k)

TiDB の平均 CPU 使用率は 827% から 577% に低下します。 QPS が増加すると、平均 TiKV CPU 使用率は 313% まで増加します。

![performance-overview-for-2-command](/media/performance/j-5-cpu.png)

主要なレイテンシーメトリクスは次のとおりです。

![performance-overview-for-3-command](/media/performance/j-5-duration.png)

-   平均クエリ時間 = 690μs (426μs から 690μs)
-   平均解析時間 = 13.5μs (12.3μs から 13.5μs )
-   平均コンパイル時間 = 49.7μs (53.3μs から 49.7μs)
-   平均実行時間 = 623μs (699μs から 623μs)
-   avg pd tso 待機時間 = 196μs (224μs から 196μs)
-   接続アイドル期間 avg-in-txn = 608μs (250μs から 608μs)

### 分析の結論 {#analysis-conclusion}

-   シナリオ 4 と比較すると、シナリオ 5 の**[CPS By Type]**ペインには`StmtExecute`コマンドのみがあり、これによりネットワークの 2 つの往復が回避され、システム全体の QPS が向上します。
-   QPS が増加した場合、解析時間、コンパイル時間、実行時間の点でレイテンシーは減少しますが、代わりにクエリ時間が増加します。これは、TiDB が`StmtPrepare`と`StmtClose`非常に高速に処理し、これら 2 つのコマンド タイプを削除すると平均クエリ時間が増加するためです。
-   SQL フェーズごとのデータベース時間では、 `execute`最も時間がかかり、データベース時間に近くなります。 SQL 実行時間の概要では、 `tso wait`ほとんどの時間を要し、 `execute`時間の 4 分の 1 以上が TSO の待機にかかります。
-   `tso wait`秒間に1回の合計は5.46秒です。平均`tso wait`回は 196 us、1 秒あたり`tso cmd`回の回数は 28k で、QPS の 30.9k に非常に近いです。これは、TiDB の分離レベル`read committed`の実装に従って、トランザクション内のすべての SQL ステートメントが PD から TSO を要求する必要があるためです。

TiDB v6.0 は`rc read`を提供します。これは、 `tso cmd`を減らすことで`read committed`分離レベルを最適化します。この機能はグローバル変数`set global tidb_rc_read_check_ts=on;`によって制御されます。この変数が有効な場合、TiDB のデフォルト動作は`repeatable-read`分離レベルと同じように動作します。この場合、PD から取得する必要があるのは`start-ts`と`commit-ts`だけです。トランザクション内のステートメントは、最初に`start-ts`を使用して TiKV からデータを読み取ります。 TiKV から読み取られたデータが`start-ts`より前の場合、データは直接返されます。 TiKV から読み取られたデータが`start-ts`より後の場合、データは破棄されます。 TiDB は PD から TSO を要求し、読み取りを再試行します。後続のステートメントの`for update ts` 、最新の PD TSO が使用されます。

## シナリオ 6: <code>tidb_rc_read_check_ts</code>変数を有効にして TSO リクエストを削減する {#scenario-6-enable-the-code-tidb-rc-read-check-ts-code-variable-to-reduce-tso-requests}

### アプリケーション構成 {#application-configuration}

シナリオ 5 と比較すると、アプリケーション構成は同じままです。唯一の違いは、 `set global tidb_rc_read_check_ts=on;`変数が TSO 要求を減らすように構成されていることです。

### パフォーマンス分析 {#performance-analysis}

#### ダッシュボード {#dashboard}

TiDB CPU のフレーム チャートには大きな変化はありません。

-   ExecutePreparedStmt CPU = 22% CPU 時間 = 8.4 秒

![flame-graph-for-rc-read](/media/performance/6.2.2.png)

#### パフォーマンス概要ダッシュボード {#performance-overview-dashboard}

RC 読み取りを使用した後、QPS は 30.9k から 34.9k に増加し、1 秒あたりに消費される`tso wait`時間は 5.46 秒から 456 ミリ秒に減少しました。

![performance-overview-1-for-rc-read](/media/performance/j-6.png)

-   SQL タイプ別のデータベース時間: `Select`ステートメント タイプがほとんどの時間を要します。
-   SQL フェーズごとのデータベース時間: `execute`フェーズにほとんどの時間がかかります。
-   SQL 実行時間の概要: `Get` 、 `Cop` 、および`Prewrite`にほとんどの時間がかかります。
-   実行計画キャッシュがヒットしました。プラン キャッシュを使用したクエリ OPS の値は、1 秒あたり`StmtExecute`にほぼ等しくなります。
-   CPS By Type: `StmtExecute`コマンドのみが使用されます。
-   平均 QPS = 34.9k (30.9k から 34.9k)

`tso cmd`秒あたり 1 は 28.3k から 2.7k に減少します。

![performance-overview-2-for-rc-read](/media/performance/j-6-cmd.png)

平均 TiDB CPU は 603% に増加します (577% から 603%)。

![performance-overview-3-for-rc-read](/media/performance/j-6-cpu.png)

主要なレイテンシーメトリクスは次のとおりです。

![performance-overview-4-for-rc-read](/media/performance/j-6-duration.png)

-   平均クエリ時間 = 533μs (690μs から 533μs)
-   平均解析時間 = 13.4μs (13.5μs から 13.4μs )
-   平均コンパイル時間 = 50.3μs (49.7μs から 50.3μs)
-   平均実行時間 = 466μs (623μs から 466μs)
-   avg pd tso 待機時間 = 171μs (196μs から 171μs)

### 分析の結論 {#analysis-conclusion}

RC Read を`set global tidb_rc_read_check_ts=on;`で有効にすると、RC Read により`tso cmd`の時間が大幅に短縮され、 `tso wait`と平均クエリ時間が短縮され、QPS が向上します。

現在のデータベース時間とレイテンシーの両方のボトルネックは`execute`フェーズにあり、 `Get`と`Cop`の読み取りリクエストが最も高い割合を占めます。このワークロードのテーブルのほとんどは読み取り専用であるか、ほとんど変更されないため、TiDB v6.0.0 以降でサポートされている小さなテーブル キャッシュ機能を使用して、これらの小さなテーブルのデータをキャッシュし、KV 読み取りリクエストの待機時間とリソース消費を削減できます。 。

## シナリオ 7: 小さなテーブル キャッシュを使用する {#scenario-7-use-the-small-table-cache}

### アプリケーション構成 {#application-configuration}

シナリオ 6 と比較すると、アプリケーション構成は同じままです。唯一の違いは、シナリオ 7 では、 `alter table t1 cache;`などの SQL ステートメントを使用して、ビジネス用の読み取り専用テーブルをキャッシュすることです。

### パフォーマンス分析 {#performance-analysis}

#### TiDB ダッシュボード {#tidb-dashboard}

TiDB CPU のフレーム チャートには大きな変化はありません。

![flame-graph-for-table-cache](/media/performance/7.2.png)

#### パフォーマンス概要ダッシュボード {#performance-overview-dashboard}

QPS は 34.9k から 40.9k に増加し、KV 要求タイプは`execute`フェーズから`Prewrite`および`Commit`への変更に最も時間がかかります。 `Get`秒あたり 7 で消費されるデータベース時間は 5.33 秒から 1.75 秒に減少し、1 秒あたり`Cop`で消費されるデータベース時間は 3.87 秒から 1.09 秒に減少します。

![performance-overview-1-for-table-cache](/media/performance/j-7.png)

-   SQL タイプ別のデータベース時間: `Select`ステートメント タイプがほとんどの時間を要します。
-   SQL フェーズごとのデータベース時間: ほとんどの時間がかかるのは`execute`フェーズと`compile`フェーズです。
-   SQL 実行時間の概要: `Prewrite` 、 `Commit` 、および`Get`にほとんどの時間がかかります。
-   実行計画キャッシュがヒットしました。プラン キャッシュを使用したクエリ OPS の値は、1 秒あたり`StmtExecute`にほぼ等しくなります。
-   CPS By Type: `StmtExecute`コマンドのみが使用されます。
-   平均 QPS = 40.9k (34.9k から 40.9k)

TiDB の平均 CPU 使用率は 603% から 478% に低下し、TiKV の平均 CPU 使用率は 346% から 256% に低下しました。

![performance-overview-2-for-table-cache](/media/performance/j-7-cpu.png)

平均クエリレイテンシーは533 マイクロ秒から 313 マイクロ秒に減少します。平均`execute`レイテンシーは466 マイクロ秒から 250 マイクロ秒に減少します。

![performance-overview-3-for-table-cache](/media/performance/j-7-duration.png)

-   平均クエリ時間 = 313μs (533μs から 313μs)
-   平均解析時間 = 11.9μs (13.4μs から 11.9μs)
-   平均コンパイル時間 = 47.7μs (50.3μs から 47.7μs)
-   平均実行時間 = 251μs (466μs から 251μs)

### 分析の結論 {#analysis-conclusion}

すべての読み取り専用テーブルをキャッシュした後は、 `Execute Duration`大幅に低下します。これは、すべての読み取り専用テーブルが TiDB にキャッシュされ、それらのテーブルに対して TiKV 内のデータをクエリする必要がないためです。そのため、クエリ時間が短縮され、QPS が増加します。

実際のビジネスでは読み取り専用テーブルのデータが大きすぎて TiDB がすべてをキャッシュできない可能性があるため、これは楽観的結果です。もう 1 つの制限は、小規模テーブル キャッシュ機能は書き込み操作をサポートしていますが、すべての TiDB ノードのキャッシュが最初に無効化されることを保証するために、書き込み操作にはデフォルトで 3 秒の待機が必要であることです。これは、厳密なレイテンシー要件を持つアプリケーションでは実現できない可能性があります。

## まとめ {#summary}

次の表に、7 つの異なるシナリオのパフォーマンスを示します。

| メトリクス | シナリオ 1 | シナリオ 2 | シナリオ 3 | シナリオ 4 | シナリオ 5 | シナリオ 6 | シナリオ 7 | シナリオ 5 とシナリオ 2 の比較 (%) | シナリオ 7 とシナリオ 3 の比較 (%) |
| ----- | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ---------------------- | ---------------------- |
| クエリ期間 | 479μs  | 1120μs | 528μs  | 426μs  | 690μs  | 533μs  | 313μs  | -38%                   | -51%                   |
| QPS   | 56.3k  | 24.2k  | 19.7k  | 22.1k  | 30.9k  | 34.9k  | 40.9k  | +28%                   | +108%                  |

これらのシナリオでは、シナリオ 2 はアプリケーションが Query インターフェイスを使用する一般的なシナリオであり、シナリオ 5 はアプリケーションが Prepared Statement インターフェイスを使用する理想的なシナリオです。

-   シナリオ 2 とシナリオ 5 を比較すると、 Javaアプリケーション開発のベスト プラクティスを使用し、クライアント側で Prepared Statement オブジェクトをキャッシュすることにより、各 SQL ステートメントは実行プラン キャッシュにヒットするために 1 つのコマンドとデータベースの対話のみを必要とすることがわかります。クエリレイテンシーが 38% 低下し、QPS が 28% 増加しました。一方、平均 TiDB CPU 使用率は 936% から 577% に低下しました。
-   シナリオ 2 とシナリオ 7 を比較すると、シナリオ 5 に加えて RC 読み取りや小規模テーブル キャッシュなどの最新の TiDB 最適化機能により、レイテンシーが51% 削減され、QPS が 108% 向上していることがわかります。一方、平均 TiDB CPU使用率は 936% から 478% に低下します。

各シナリオのパフォーマンスを比較すると、次の結論を導き出すことができます。

-   TiDB の実行プラン キャッシュは、OLTP のパフォーマンス チューニングにおいて重要な役割を果たします。 v6.0.0 から導入された RC 読み取り機能と小さなテーブル キャッシュ機能も、このワークロードのさらなるパフォーマンス チューニングにおいて重要な役割を果たします。

-   TiDB は、MySQL プロトコルのさまざまなコマンドと互換性があります。 Prepared Statement インターフェイスを使用し、次の JDBC 接続パラメータを設定すると、アプリケーションは最高のパフォーマンスを達成できます。

        useServerPrepStmts=true&cachePrepStmts=true&prepStmtCacheSize=1000&prepStmtCacheSqlLimit=20480&useConfigs= maxPerformance

-   パフォーマンスの分析とチューニングには、TiDB ダッシュボード (たとえば、Top SQL機能や継続的プロファイリング機能) とパフォーマンス概要ダッシュボードを使用することをお勧めします。

    -   [Top SQL](/dashboard/top-sql.md)機能を使用すると、実行中のデータベース内の各 SQL ステートメントの CPU 消費量を視覚的に監視および調査して、データベースのパフォーマンスの問題をトラブルシューティングできます。
    -   [継続的なプロファイリング](/dashboard/continuous-profiling.md)を使用すると、TiDB、TiKV、PD の各インスタンスからパフォーマンス データを継続的に収集できます。アプリケーションが異なるインターフェイスを使用して TiDB と対話する場合、TiDB の CPU 消費量の違いは非常に大きくなります。
    -   [パフォーマンス概要ダッシュボード](/grafana-performance-overview-dashboard.md)を使用すると、データベース時間と SQL 実行時間の内訳情報の概要を取得できます。データベース時間に基づいてパフォーマンスを分析および診断し、システム全体のパフォーマンスのボトルネックが TiDB にあるかどうかを判断できます。ボトルネックが TiDB 内にある場合は、データベースの時間とレイテンシーの内訳、および負荷プロファイルとリソースの使用状況を使用して、TiDB 内のパフォーマンスのボトルネックを特定し、それに応じてパフォーマンスを調整できます。

これらの機能を組み合わせて使用​​すると、実際のアプリケーションのパフォーマンスを効率的に分析および調整できます。
