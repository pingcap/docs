---
title: Performance Tuning Practices for OLTP Scenarios
summary: This document describes how to analyze and tune performance for OLTP workloads.
---

# OLTPシナリオの性能チューニングの実践 {#performance-tuning-practices-for-oltp-scenarios}

TiDBは、TiDBダッシュボードの[Top SQL](/dashboard/top-sql.md)および[継続的なプロファイリング](/dashboard/continuous-profiling.md)機能、TiDB [パフォーマンス概要ダッシュボード](/grafana-performance-overview-dashboard.md)など、包括的なパフォーマンス診断および分析機能を提供します。

このドキュメントでは、これらの機能を一緒に使用して、7つの異なるランタイムシナリオで同じOLTPワークロードのパフォーマンスを分析および比較する方法について説明します。これは、TiDBのパフォーマンスを効率的に分析および調整するのに役立つパフォーマンス調整プロセスを示しています。

> **ノート：**
>
> [Top SQL](/dashboard/top-sql.md)と[継続的なプロファイリング](/dashboard/continuous-profiling.md)はデフォルトでは有効になっていません。事前に有効にする必要があります。

このドキュメントでは、これらのシナリオで異なるJDBC構成を使用して同じアプリケーションを実行することにより、アプリケーションとデータベース間のさまざまな相互作用によってシステム全体のパフォーマンスがどのように影響を受けるかを示し、 [TiDBを使用してJavaアプリケーションを開発するためのベストプラクティス](/best-practices/java-app-best-practices.md)を適用してパフォーマンスを向上させることができます。

## 環境の説明 {#environment-description}

このドキュメントでは、デモンストレーションのために勘定系OLTPワークロードを使用します。シミュレーション環境の構成は次のとおりです。

-   ワークロード用のアプリケーション開発言語：JAVA
-   ビジネスで使用されるSQLステートメント：合計200ステートメント、そのうちの90％はSELECTステートメントです。これは、典型的な読み取りの多いOLTPワークロードです。
-   トランザクションで使用されるテーブル：合計60テーブル。 12のテーブルには更新操作が含まれ、残りの48のテーブルは読み取り専用です。
-   アプリケーションで使用される分離レベル： `read committed` 。
-   TiDBクラスタ構成：3つのTiDBノードと3つのTiKVノード、各ノードに16個のCPUが割り当てられています。
-   クライアントサーバー構成：36CPU。

## シナリオ1.クエリインターフェイスを使用する {#scenario-1-use-the-query-interface}

### アプリケーション構成 {#application-configuration}

アプリケーションは、次のJDBC構成を使用して、クエリインターフェイスを介してデータベースに接続します。

```
useServerPrepStmts=false
```

### パフォーマンス分析 {#performance-analysis}

#### TiDBダッシュボード {#tidb-dashboard}

以下のTiDBダッシュボードのTop SQLページから、非ビジネスSQLタイプ`SELECT @@session.tx_isolation`が最も多くのリソースを消費していることがわかります。 TiDBはこれらのタイプのSQLステートメントを迅速に処理しますが、これらのタイプのSQLステートメントは実行回数が最も多く、その結果、全体的なCPU時間の消費量が最も多くなります。

![dashboard-for-query-interface](/media/performance/case1.png)

次のTiDBのフレームチャートから、SQLの実行中に`Compile`や`Optimize`などの関数のCPU消費が重要であることがわかります。アプリケーションはクエリインターフェイスを使用するため、TiDBは実行プランキャッシュを使用できません。 TiDBは、SQLステートメントごとに実行プランをコンパイルして生成する必要があります。

![flame-graph-for-query-interface](/media/performance/7.1.png)

-   ExecuteStmt cpu = 38％cpu time = 23.84s
-   コンパイルCPU=27％CPU時間= 17.17s
-   CPUの最適化=26％CPU時間= 16.41s

#### パフォーマンス概要ダッシュボード {#performance-overview-dashboard}

次のパフォーマンス概要ダッシュボードで、データベース時間の概要とQPSを確認してください。

![performance-overview-1-for-query-interface](/media/performance/j-1.png)

-   SQLタイプ別のデータベース時間： `Select`ステートメントタイプがほとんどの時間を要します。
-   SQLフェーズごとのデータベース時間： `execute`フェーズと`compile`フェーズがほとんどの時間を要します。
-   SQL実行時間の概要： `Get` 、および`Cop`がほとんどの時間を要し`tso wait` 。
-   タイプ別のCPS： `Query`のコマンドのみが使用されます。
-   プランキャッシュOPSを使用したクエリ：データがない場合は、実行プランキャッシュがヒットしていないことを示します。
-   クエリ期間では、 `execute`と`compile`のレイテンシーが最も高い割合を占めます。
-   平均QPS=56.8k

クラスタのリソース消費量を確認します。TiDBCPUの平均使用率は925％、TiKV CPUの平均使用率は201％、TiKVIOの平均スループットは18.7MB/秒です。 TiDBのリソース消費は大幅に高くなります。

![performance-overview-2-for-query-interface](/media/performance/5.png)

### 分析の結論 {#analysis-conclusion}

実行回数が多く、TiDB CPU使用率が高くなる原因となる、これらの役に立たない非ビジネスSQLステートメントを排除する必要があります。

## シナリオ2.maxPerformance構成を使用する {#scenario-2-use-the-maxperformance-configuration}

### アプリケーション構成 {#application-configuration}

アプリケーションは、シナリオ1のJDBC接続文字列に新しいパラメーター`useConfigs=maxPerformance`を追加します。このパラメーターを使用して、JDBCからデータベースに送信されるSQLステートメント（たとえば、 `select @@session.transaction_read_only` ）を削除できます。完全な構成は次のとおりです。

```
useServerPrepStmts=false&useConfigs=maxPerformance
```

### パフォーマンス分析 {#performance-analysis}

#### TiDBダッシュボード {#tidb-dashboard}

以下のTiDBダッシュボードのTop SQLページから、最も多くのリソースを消費した`SELECT @@session.tx_isolation`が消えていることがわかります。

![dashboard-for-maxPerformance](/media/performance/case2.png)

次のTiDBのフレームチャートから、SQLの実行中に`Compile`や`Optimize`などの関数のCPU消費が依然として重要であることがわかります。

![flame-graph-for-maxPerformance](/media/performance/20220507-145257.jpg)

-   ExecuteStmt cpu = 43％cpu time = 35.84s
-   コンパイルCPU=31％CPU時間= 25.61s
-   CPUの最適化=30％CPU時間= 24.74s

#### パフォーマンス概要ダッシュボード {#performance-overview-dashboard}

データベース時間の概要とQPSのデータは次のとおりです。

![performance-overview-1-for-maxPerformance](/media/performance/j-2.png)

-   SQLタイプ別のデータベース時間： `Select`ステートメントタイプがほとんどの時間を要します。
-   SQLフェーズごとのデータベース時間： `execute`フェーズと`compile`フェーズがほとんどの時間を要します。
-   SQL実行時間の概要： `Get` 、および`Prewrite`がほとんどの時間を`tso wait` `Cop` 。
-   データベース時間では、 `execute`と`compile`のレイテンシーが最も高い割合を占めます。
-   タイプ別のCPS： `Query`のコマンドのみが使用されます。
-   平均QPS=24.2k（56.3kから24.2k）
-   実行プランのキャッシュはヒットしません。

シナリオ1からシナリオ2に、平均TiDB CPU使用率は925％から874％に低下し、平均TiKV CPU使用率は201％から約250％に増加します。

![performance-overview-2-for-maxPerformance](/media/performance/9.1.1.png)

主要なレイテンシメトリックの変更は次のとおりです。

![performance-overview-3-for-maxPerformance](/media/performance/9.2.2.png)

-   平均クエリ期間=1.12ms（479μsから1.12ms）
-   平均解析時間=84.7μs（37.2μsから84.7μs）
-   平均コンパイル時間=370μs（166μsから370μs）
-   平均実行時間=626μs（251μsから626μs）

### 分析の結論 {#analysis-conclusion}

シナリオ1と比較して、シナリオ2のQPSは大幅に減少しています。平均クエリ期間と平均`parse` 、および`compile`期間が大幅に増加し`execute`た。これは、シナリオ1の`select @@session.transaction_read_only`などのSQLステートメントが何度も実行され、処理時間が速いため、平均パフォーマンスデータが低下するためです。シナリオ2がそのようなステートメントをブロックした後、ビジネス関連のSQLステートメントのみが残るため、平均期間が長くなります。

アプリケーションがクエリインターフェイスを使用する場合、TiDBは実行プランキャッシュを使用できません。その結果、TiDBは実行プランをコンパイルするために大量のリソースを消費します。この場合、Prepared Statementインターフェイスを使用することをお勧めします。このインターフェイスは、TiDBの実行プランキャッシュを使用して、実行プランのコンパイルによって発生するTiDB CPU消費を減らし、遅延を減らします。

## シナリオ3.実行プランのキャッシュが有効になっていないプリペアドステートメントインターフェイスを使用する {#scenario-3-use-the-prepared-statement-interface-with-execution-plan-caching-not-enabled}

### アプリケーション構成 {#application-configuration}

アプリケーションは、次の接続構成を使用します。シナリオ2と比較すると、JDBCパラメーター`useServerPrepStmts`の値は`true`に変更されており、PreparedStatementインターフェースが有効になっていることを示しています。

```
useServerPrepStmts=true&useConfigs=maxPerformance"
```

### パフォーマンス分析 {#performance-analysis}

#### TiDBダッシュボード {#tidb-dashboard}

次のTiDBのフレームチャートから、Prepared Statementインターフェイスを有効にした後でも、 `CompileExecutePreparedStmt`と`Optimize`のCPU消費量が依然として重要であることがわかります。

![flame-graph-for-PrepStmts](/media/performance/3.1.1.png)

-   ExecutePreparedStmt cpu = 31％cpu time = 23.10s
-   prepareStmtExec cpu = 30％cpu time = 22.92s
-   CompileExecutePreparedStmt cpu = 24％cpu時間= 17.83s
-   CPUの最適化=23％CPU時間= 17.29s

#### パフォーマンス概要ダッシュボード {#performance-overview-dashboard}

プリペアドステートメントインターフェイスを使用した後のデータベース時間の概要とQPSのデータは次のとおりです。

![performance-overview-1-for-PrepStmts](/media/performance/j-3.png)

QPSは24.4kから19.7kに低下します。データベース時間の概要から、アプリケーションが3種類のPreparedコマンドを使用し、 `general`ステートメントタイプ（ `StmtPrepare`や`StmtClose`などのコマンドの実行時間を含む）がSQLタイプ別データベース時間で2番目に位置していることがわかります。これは、Prepared Statementインターフェースが使用されている場合でも、実行プランのキャッシュがヒットしないことを示しています。その理由は、 `StmtClose`コマンドが実行されると、TiDBは内部処理でSQLステートメントの実行プランキャッシュをクリアするためです。

-   SQLタイプ別のデータベース時間： `Select`のステートメントタイプがほとんどの時間を要し、その後に`general`のステートメントが続きます。
-   SQLフェーズごとのデータベース時間： `execute`フェーズと`compile`フェーズがほとんどの時間を要します。
-   SQL実行時間の概要： `Get` 、および`Prewrite`がほとんどの時間を`tso wait` `Cop` 。
-   タイプ別のCPS： `StmtExecute`種類のコマンド（ `StmtPrepare` ）が使用され`StmtClose` 。
-   平均QPS=19.7k（24.4kから19.7k）
-   実行プランのキャッシュはヒットしません。

TiDBの平均CPU使用率は874％から936％に増加します。

![performance-overview-1-for-PrepStmts](/media/performance/3-2.png)

主なレイテンシメトリックは次のとおりです。

![performance-overview-2-for-PrepStmts](/media/performance/3.4.png)

-   平均クエリ期間=528μs（1.12msから528μs）
-   平均解析期間=14.9μs（84.7μsから14.9μs）
-   平均コンパイル時間=374μs（370μsから374μs）
-   平均実行時間=649μs（626μsから649μs）

### 分析の結論 {#analysis-conclusion}

シナリオ2とは異なり、シナリオ3のアプリケーションは、プリペアドステートメントインターフェイスを有効にしますが、それでもキャッシュにヒットしません。さらに、シナリオ2には1つのCPS By Typeコマンドタイプ（ `Query` ）しかありませんが、シナリオ3にはさらに3 `StmtClose` `StmtPrepare`があり`StmtExecute` 。シナリオ2と比較すると、シナリオ3にはさらに2つのネットワークラウンドトリップ遅延があります。

-   QPSの減少の分析：[ **CPS By Type** ]ペインから、シナリオ2には1つのCPS By Typeコマンドタイプ（ `Query` ）しかなく、シナリオ3にはさらに3 `StmtExecute`のコマンドタイプ（ `StmtPrepare` ）があることがわかり`StmtClose` 。 `StmtPrepare`と`StmtClose`は、QPSでカウントされない非従来型のコマンドであるため、QPSが削減されます。非従来型のコマンド`StmtPrepare`および`StmtClose`は`general`タイプでカウントされるため、シナリオ3のデータベース概要に`general`時間が表示され、データベース時間の4分の1以上を占めます。
-   平均クエリ期間の大幅な減少の分析：シナリオ3で新しく追加された`StmtPrepare`および`StmtClose`コマンドタイプの場合、それらのクエリ期間はTiDB内部処理で個別に計算されます。 TiDBは、これら2種類のコマンドを非常に高速に実行するため、平均クエリ期間が大幅に短縮されます。

シナリオ3はプリペアドステートメントインターフェイスを使用しますが、多くのアプリケーションフレームワークがメモリリークを防ぐために`StmtExecute`の後に`StmtClose`メソッドを呼び出すため、実行プランキャッシュはヒットしません。 v6.0.0以降では、グローバル変数`tidb_ignore_prepared_cache_close_stmt=on;`を設定できます。その後、アプリケーションが`StmtClose`メソッドを呼び出しても、TiDBはキャッシュされた実行プランをクリアしないため、次のSQL実行は既存の実行プランを再利用し、実行プランを繰り返しコンパイルすることを回避できます。

## シナリオ4.プリペアドステートメントインターフェイスを使用して、実行プランのキャッシュを有効にします {#scenario-4-use-the-prepared-statement-interface-and-enable-execution-plan-caching}

### アプリケーション構成 {#application-configuration}

アプリケーションの構成はシナリオ3と同じです。アプリケーションが`StmtClose`をトリガーしてもキャッシュにヒットしないという問題を解決するために、次のパラメーターが構成されます。

-   TiDBグローバル変数`set global tidb_ignore_prepared_cache_close_stmt=on;`を設定します（TiDB v6.0.0以降に導入されました。デフォルトでは`off` ）。
-   プランキャッシュ機能を有効にするには、TiDB構成項目`prepared-plan-cache: {enabled: true}`を設定します。

### パフォーマンス分析 {#performance-analysis}

#### TiDBダッシュボード {#tidb-dashboard}

TiDB CPU使用率のフレームチャートから、 `CompileExecutePreparedStmt`と`Optimize`には大きなCPU消費量がないことがわかります。 CPUの25％は、 `PlanBuilder`や`parseSQL`などのPrepareの解析関連関数を含む`Prepare`コマンドによって消費されます。

PreparseStmt cpu = 25％cpu時間= 12.75s

![flame-graph-for-3-commands](/media/performance/4.2.png)

#### パフォーマンス概要ダッシュボード {#performance-overview-dashboard}

パフォーマンスの概要ダッシュボードで最も重要な変更は、 `compile`フェーズの平均時間であり、シナリオ3の8.95秒/秒から1.18秒/秒に短縮されます。実行プランキャッシュを使用するクエリの数は、値`StmtExecute`とほぼ同じです。 QPSの増加に伴い、1秒あたり`Select`ステートメントで消費されるデータベース時間は減少し、1秒あたり`general`ステートメントで消費されるデータベース時間は増加します。

![performance-overview-1-for-3-commands](/media/performance/j-4.png)

-   SQLタイプ別のデータベース時間： `Select`ステートメントタイプが最も時間がかかります。
-   SQLフェーズごとのデータベース時間： `execute`フェーズはほとんどの時間を要します。
-   SQL実行時間の概要： `tso wait` 、および`Get`がほとんどの時間を要し`Cop` 。
-   実行プランのキャッシュがヒットしました。プランキャッシュOPSを使用したクエリの値は、おおよそ`StmtExecute`秒あたり1になります。
-   タイプ別のCPS：3種類のコマンド（シナリオ3と同じ）
-   シナリオ3と比較すると、QPSが増加するため、 `general`のステートメントにかかる時間が長くなります。
-   平均QPS=22.1k（19.7kから22.1k）

TiDBの平均CPU使用率は936％から827％に低下します。

![performance-overview-2-for-3-commands](/media/performance/4.4.png)

平均`compile`回は、374usから53.3usに大幅に減少します。 QPSが増加するため、平均`execute`時間も増加します。

![performance-overview-3-for-3-commands](/media/performance/4.5.png)

-   平均クエリ期間=426μs（528μsから426μs）
-   平均解析期間=12.3μs（14.8μsから12.3μs）
-   平均コンパイル時間=53.3μs（374μsから53.3μs）
-   平均実行時間=699μs（649μsから699us）

### 分析の結論 {#analysis-conclusion}

シナリオ3と比較すると、シナリオ4でも3つのコマンドタイプが使用されます。違いは、シナリオ4が実行プランのキャッシュにヒットすることです。これにより、コンパイル期間が大幅に短縮され、クエリ期間が短縮され、QPSが向上します。

`StmtPrepare`および`StmtClose`コマンドはデータベースにかなりの時間を消費し、アプリケーションがSQLステートメントを実行するたびにアプリケーションとTiDB間の相互作用の数を増やすためです。次のシナリオでは、JDBC構成を介してこれら2つのコマンドの呼び出しを排除することにより、パフォーマンスをさらに調整します。

## シナリオ5.クライアント側で準備されたオブジェクトをキャッシュする {#scenario-5-cache-prepared-objects-on-the-client-side}

### アプリケーション構成 {#application-configuration}

シナリオ4と比較すると、以下で説明するように、3つの新しいJDBCパラメーター`cachePrepStmts=true&prepStmtCacheSize=1000&prepStmtCacheSqlLimit=20480`が構成されます。

-   `cachePrepStmts = true` ：クライアント側でPrepared Statementオブジェクトをキャッシュします。これにより、StmtPrepareおよびStmtCloseの呼び出しが排除されます。
-   `prepStmtCacheSize` ：値は0より大きくなければなりません。
-   `prepStmtCacheSqlLimit` ：値はSQLテキストの長さより大きくなければなりません。

シナリオ5では、完全なJDBC構成は次のとおりです。

```
useServerPrepStmts=true&cachePrepStmts=true&prepStmtCacheSize=1000&prepStmtCacheSqlLimit=20480&useConfigs=maxPerformance
```

### パフォーマンス分析 {#performance-analysis}

#### TiDBダッシュボード {#tidb-dashboard}

次のTiDBのフレームチャートから、 `Prepare`コマンドの高いCPU消費量がなくなっていることがわかります。

-   ExecutePreparedStmt cpu = 22％cpu time = 8.4s

![flame-graph-for-1-command](/media/performance/5.1.1.png)

#### パフォーマンス概要ダッシュボード {#performance-overview-dashboard}

パフォーマンスの概要ダッシュボードで最も注目すべき変更は、[ **CPS By Type** ]ペインの3つのStmtコマンドタイプが1つのタイプにドロップし、[ <strong>Database Time by SQL Type</strong> ]ペインの`general`のステートメントタイプが非表示になり、[QPS]ペインの<strong>QPS</strong>が非表示になることです。 30.9kに増加します。

![performance-overview-for-1-command](/media/performance/j-5.png)

-   SQLタイプ別のデータベース時間： `Select`ステートメントタイプはほとんどの時間を要し、 `general`ステートメントタイプは消えます。
-   SQLフェーズごとのデータベース時間： `execute`フェーズはほとんどの時間を要します。
-   SQL実行時間の概要： `tso wait` 、および`Get`がほとんどの時間を要し`Cop` 。
-   実行プランのキャッシュがヒットしました。プランキャッシュOPSを使用したクエリの値は、おおよそ`StmtExecute`秒あたり1になります。
-   タイプ別のCPS： `StmtExecute`のコマンドのみが使用されます。
-   平均QPS=30.9k（22.1kから30.9k）

TiDBの平均CPU使用率は、827％から577％に低下します。 QPSが増加すると、平均TiKV CPU使用率は313％に増加します。

![performance-overview-for-2-command](/media/performance/j-5-cpu.png)

主なレイテンシメトリックは次のとおりです。

![performance-overview-for-3-command](/media/performance/j-5-duration.png)

-   平均クエリ期間=690μs（426μsから690μs）
-   平均解析期間=13.5μs（12.3μsから13.5μs）
-   平均コンパイル時間=49.7μs（53.3μsから49.7μs）
-   平均実行時間=623μs（699usから623μs）
-   avg pdtso待機時間=196μs（224μsから196μs）
-   接続アイドル期間avg-in-txn=608μs（250μsから608μs）

### 分析の結論 {#analysis-conclusion}

-   シナリオ4と比較すると、シナリオ5の[ **CPS By Type** ]ペインには`StmtExecute`コマンドのみがあり、2回のネットワークラウンドトリップを回避し、システム全体のQPSを向上させます。
-   QPSが増加すると、解析期間、コンパイル期間、および実行期間の観点からレイテンシが減少しますが、代わりにクエリ期間が増加します。これは、TiDBが`StmtPrepare`と`StmtClose`を非常に高速に処理し、これら2つのコマンドタイプを削除すると、平均クエリ時間が長くなるためです。
-   SQLフェーズによるデータベース時間では、 `execute`が最も時間がかかり、データベース時間に近いです。 SQL実行時間の概要では、 `tso wait`がほとんどの時間かかり、 `execute`時間の4分の1以上がTSOの待機にかかります。
-   1秒あたりの合計`tso wait`回は5.46秒です。平均`tso wait`回は196us、1秒間の`tso cmd`回は28kで、QPSの30.9kに非常に近い値です。これは、TiDBの`read committed`分離レベルの実装によれば、トランザクション内のすべてのSQLステートメントがPDからTSOを要求する必要があるためです。

TiDB v6.0は`rc read`を提供します。これは、 `tso cmd`を減らすことによって`read committed`の分離レベルを最適化します。この機能は、グローバル変数`set global tidb_rc_read_check_ts=on;`によって制御されます。この変数を有効にすると、TiDBのデフォルトの動作は`repeatable-read`分離レベルと同じように機能し、PDから`start-ts`と`commit-ts`のみを取得する必要があります。トランザクション内のステートメントは、 `start-ts`を使用して最初にTiKVからデータを読み取ります。 TiKVから読み取られたデータが`start-ts`より前の場合、データは直接返されます。 TiKVから読み取ったデータが`start-ts`より後の場合、データは破棄されます。 TiDBはPDにTSOを要求し、読み取りを再試行します。後続の`for update ts`のステートメントは、最新のPDTSOを使用します。

## シナリオ6： <code>tidb_rc_read_check_ts</code>変数を有効にして、TSO要求を減らします {#scenario-6-enable-the-code-tidb-rc-read-check-ts-code-variable-to-reduce-tso-requests}

### アプリケーション構成 {#application-configuration}

シナリオ5と比較すると、アプリケーション構成は同じままです。唯一の違いは、 `set global tidb_rc_read_check_ts=on;`の変数がTSO要求を減らすように構成されていることです。

### パフォーマンス分析 {#performance-analysis}

#### ダッシュボード {#dashboard}

TiDBCPUのフレームチャートに大きな変更はありません。

-   ExecutePreparedStmt cpu = 22％cpu time = 8.4s

![flame-graph-for-rc-read](/media/performance/6.2.2.png)

#### パフォーマンス概要ダッシュボード {#performance-overview-dashboard}

RC読み取りを使用した後、QPSは30.9kから34.9kに増加し、1秒あたりに消費される`tso wait`時間は5.46秒から456ミリ秒に減少します。

![performance-overview-1-for-rc-read](/media/performance/j-6.png)

-   SQLタイプ別のデータベース時間： `Select`ステートメントタイプがほとんどの時間を要します。
-   SQLフェーズごとのデータベース時間： `execute`フェーズはほとんどの時間を要します。
-   SQL実行時間の概要： `Get` 、および`Cop`がほとんどの時間を要し`Prewrite` 。
-   実行プランのキャッシュがヒットしました。プランキャッシュOPSを使用したクエリの値は、おおよそ`StmtExecute`秒あたり1になります。
-   タイプ別のCPS： `StmtExecute`のコマンドのみが使用されます。
-   平均QPS=34.9k（30.9kから34.9k）

`tso cmd`秒あたり1は、28.3kから2.7kに低下します。

![performance-overview-2-for-rc-read](/media/performance/j-6-cmd.png)

平均的なTiDBCPUは603％に増加します（577％から603％に）。

![performance-overview-3-for-rc-read](/media/performance/j-6-cpu.png)

主なレイテンシメトリックは次のとおりです。

![performance-overview-4-for-rc-read](/media/performance/j-6-duration.png)

-   平均クエリ期間=533μs（690μsから533μs）
-   平均解析期間=13.4μs（13.5μsから13.4μs）
-   平均コンパイル時間=50.3μs（49.7μsから50.3μs）
-   平均実行時間=466μs（623μsから466μs）
-   avg pdtso待機時間=171μs（196μsから171μs）

### 分析の結論 {#analysis-conclusion}

RC読み取りを`set global tidb_rc_read_check_ts=on;`だけ有効にすると、RC読み取りは`tso cmd`の時間を大幅に短縮し、 `tso wait`と平均クエリ期間を短縮し、QPSを向上させます。

現在のデータベース時間と待機時間の両方のボトルネックは`execute`フェーズにあり、 `Get`と`Cop`の読み取り要求が最も高い割合を占めます。このワークロードのほとんどのテーブルは読み取り専用であるか、ほとんど変更されないため、TiDB v6.0.0以降でサポートされている小さなテーブルのキャッシュ機能を使用して、これらの小さなテーブルのデータをキャッシュし、KV読み取り要求の待機時間とリソース消費を減らすことができます。 。

## シナリオ7：小さなテーブルキャッシュを使用する {#scenario-7-use-the-small-table-cache}

### アプリケーション構成 {#application-configuration}

シナリオ6と比較すると、アプリケーション構成は同じままです。唯一の違いは、シナリオ7では`alter table t1 cache;`などのSQLステートメントを使用して、ビジネス用の読み取り専用テーブルをキャッシュすることです。

### パフォーマンス分析 {#performance-analysis}

#### TiDBダッシュボード {#tidb-dashboard}

TiDBCPUのフレームチャートに大きな変更はありません。

![flame-graph-for-table-cache](/media/performance/7.2.png)

#### パフォーマンス概要ダッシュボード {#performance-overview-dashboard}

QPSは34.9kから40.9kに増加し、KV要求タイプは`execute`フェーズから`Prewrite`および`Commit`への変更に最も時間がかかります。 1秒あたり`Get`で消費されるデータベース時間は5.33秒から1.75秒に減少し、1秒あたり`Cop`で消費されるデータベース時間は3.87秒から1.09秒に減少します。

![performance-overview-1-for-table-cache](/media/performance/j-7.png)

-   SQLタイプ別のデータベース時間： `Select`ステートメントタイプがほとんどの時間を要します。
-   SQLフェーズごとのデータベース時間： `execute`フェーズと`compile`フェーズがほとんどの時間を要します。
-   SQL実行時間の概要： `Prewrite` 、および`Commit`がほとんどの時間を要し`Get` 。
-   実行プランのキャッシュがヒットしました。プランキャッシュOPSを使用したクエリの値は、おおよそ`StmtExecute`秒あたり1になります。
-   タイプ別のCPS： `StmtExecute`のコマンドのみが使用されます。
-   平均QPS=40.9k（34.9kから40.9k）

平均TiDBCPU使用率は603％から478％に低下し、平均TiKV CPU使用率は346％から256％に低下します。

![performance-overview-2-for-table-cache](/media/performance/j-7-cpu.png)

平均クエリレイテンシは533usから313usに低下します。平均`execute`レイテンシは、466usから250usに低下します。

![performance-overview-3-for-table-cache](/media/performance/j-7-duration.png)

-   平均クエリ期間=313μs（533μsから313μs）
-   平均解析期間=11.9μs（13.4μsから11.9μs）
-   平均コンパイル時間=47.7μs（50.3μsから47.7μs）
-   平均実行時間=251μs（466μsから251μs）

### 分析の結論 {#analysis-conclusion}

すべての読み取り専用テーブルをキャッシュした後、すべての読み取り専用テーブルがTiDBにキャッシュされ、それらのテーブルのTiKVでデータをクエリする必要がないため、 `Execute Duration`が大幅に減少します。そのため、クエリ期間が短縮され、QPSが増加します。

実際のビジネスでは読み取り専用テーブルのデータが大きすぎてTiDBがすべてをキャッシュできない可能性があるため、これは楽観的な結果です。もう1つの制限は、小さなテーブルのキャッシュ機能は書き込み操作をサポートしますが、すべてのTiDBノードのキャッシュが最初に無効になるように、書き込み操作にはデフォルトで3秒の待機が必要です。これは、厳密な遅延要件を持つアプリケーションでは実行できない場合があります。

## 概要 {#summary}

次の表に、7つの異なるシナリオのパフォーマンスを示します。

| 指標    | シナリオ1 | シナリオ2  | シナリオ3 | シナリオ4 | シナリオ5 | シナリオ6 | シナリオ7 | シナリオ5とシナリオ2の比較（％） | シナリオ7とシナリオ3の比較（％） |
| ----- | ----- | ------ | ----- | ----- | ----- | ----- | ----- | ----------------- | ----------------- |
| クエリ期間 | 479μs | 1120μs | 528μs | 426μs | 690μs | 533μs | 313μs | -38％              | -51％              |
| QPS   | 56.3k | 24.2k  | 19.7k | 22.1k | 30.9k | 34.9k | 40.9k | + 28％             | + 108％            |

これらのシナリオでは、シナリオ2はアプリケーションがクエリインターフェイスを使用する一般的なシナリオであり、シナリオ5はアプリケーションがプリペアドステートメントインターフェイスを使用する理想的なシナリオです。

-   シナリオ2とシナリオ5を比較すると、Javaアプリケーション開発のベストプラクティスを使用し、クライアント側でPrepared Statementオブジェクトをキャッシュすることにより、各SQLステートメントが実行プランキャッシュに到達するために必要なコマンドとデータベースの相互作用は1つだけであることがわかります。クエリの待ち時間が38％減少し、QPSが28％増加し、TiDBの平均CPU使用率が936％から577％に減少しました。
-   シナリオ2とシナリオ7を比較すると、シナリオ5に加えてRC読み取りや小さなテーブルキャッシュなどの最新のTiDB最適化機能を使用すると、平均的なTiDB CPUが51％減少し、QPSが108％増加することがわかります。使用率は936％から478％に低下します。

各シナリオのパフォーマンスを比較することにより、次の結論を導き出すことができます。

-   TiDBの実行プランキャッシュは、OLTPパフォーマンスの調整において重要な役割を果たします。 v6.0.0から導入されたRC読み取りおよびスモールテーブルキャッシュ機能も、このワークロードのさらなるパフォーマンス調整において重要な役割を果たします。

-   TiDBは、MySQLプロトコルのさまざまなコマンドと互換性があります。プリペアドステートメントインターフェイスを使用し、次のJDBC接続パラメータを設定すると、アプリケーションは最高のパフォーマンスを実現できます。

    ```
    useServerPrepStmts=true&cachePrepStmts=true&prepStmtCacheSize=1000&prepStmtCacheSqlLimit=20480&useConfigs= maxPerformance
    ```

-   パフォーマンスの分析と調整には、TiDBダッシュボード（たとえば、Top SQL機能と継続的プロファイリング機能）とパフォーマンス概要ダッシュボードを使用することをお勧めします。

    -   [Top SQL](/dashboard/top-sql.md)つの機能を使用すると、実行中にデータベース内の各SQLステートメントのCPU消費量を視覚的に監視および調査して、データベースのパフォーマンスの問題をトラブルシューティングできます。
    -   [継続的なプロファイリング](/dashboard/continuous-profiling.md)を使用すると、TiDB、TiKV、およびPDの各インスタンスからパフォーマンスデータを継続的に収集できます。アプリケーションが異なるインターフェイスを使用してTiDBと対話する場合、TiDBのCPU消費量の違いは非常に大きくなります。
    -   [パフォーマンス概要ダッシュボード](/grafana-performance-overview-dashboard.md)を使用すると、データベース時間とSQL実行時間の内訳情報の概要を取得できます。データベース時間に基づいてパフォーマンスを分析および診断して、システム全体のパフォーマンスのボトルネックがTiDBにあるかどうかを判断できます。ボトルネックがTiDBにある場合は、データベースの時間と遅延の内訳、および負荷プロファイルとリソースの使用量を使用して、TiDB内のパフォーマンスのボトルネックを特定し、それに応じてパフォーマンスを調整できます。

これらの機能を組み合わせて使用することで、実際のアプリケーションのパフォーマンスを効率的に分析および調整できます。
