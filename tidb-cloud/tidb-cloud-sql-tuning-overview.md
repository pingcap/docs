---
title: SQL Tuning Overview
summary: Learn about how to tune SQL performance in TiDB Cloud.
---

# SQLチューニングの概要 {#sql-tuning-overview}

このドキュメントでは、 TiDB Cloudで SQL パフォーマンスを調整する方法を紹介します。最高の SQL パフォーマンスを得るには、次のことを実行できます。

-   SQL のパフォーマンスを調整します。 SQL パフォーマンスを最適化するには、クエリ ステートメントの分析、実行計画の最適化、テーブル全体のスキャンの最適化など、さまざまな方法があります。
-   スキーマ設計を最適化します。ビジネス ワークロードの種類によっては、トランザクションの競合やホットスポットを回避するためにスキーマを最適化する必要がある場合があります。

## SQLのパフォーマンスを調整する {#tune-sql-performance}

SQL ステートメントのパフォーマンスを向上させるには、次の原則を考慮してください。

-   スキャンデータの範囲を最小限に抑えます。常に、最小限の範囲のデータのみをスキャンし、すべてのデータをスキャンすることを避けることがベスト プラクティスです。
-   適切なインデックスを使用してください。 SQL ステートメントの`WHERE`句の各列に、対応するインデックスがあることを確認してください。そうしないと、 `WHERE`節によってテーブル全体がスキャンされ、パフォーマンスが低下します。
-   適切な結合タイプを使用してください。クエリ内の各テーブルのサイズと相関関係に応じて、適切な結合タイプを選択することが非常に重要です。一般に、TiDB のコストベースのオプティマイザーは、最適な結合タイプを自動的に選択します。ただし、場合によっては、結合タイプを手動で指定する必要がある場合があります。詳細は[テーブル結合を使用する Explain ステートメント](/explain-joins.md)を参照してください。
-   適切なstorageエンジンを使用します。ハイブリッド トランザクションおよび分析処理 (HTAP) ワークロードには、 TiFlashstorageエンジンを使用することをお勧めします。 [HTAP クエリ](/develop/dev-guide-hybrid-oltp-and-olap-queries.md)を参照してください。

TiDB Cloud には、クラスター上の遅いクエリの分析に役立つツールがいくつか用意されています。次のセクションでは、遅いクエリを最適化するためのいくつかのアプローチについて説明します。

### 「診断」タブの「ステートメントを使用」 {#use-statement-on-the-diagnosis-tab}

TiDB Cloudコンソールには、 **[診断]**タブに**<a href="/tidb-cloud/tune-performance.md#statement-analysis">[SQL ステートメント]</a>**サブタブがあります。クラスター上のすべてのデータベースの SQL ステートメントの実行統計を収集します。これを使用すると、合計または 1 回の実行で長時間かかる SQL ステートメントを特定して分析できます。

このサブタブでは、同じ構造を持つ SQL クエリ (クエリ パラメータが一致しない場合でも) が同じ SQL ステートメントにグループ化されることに注意してください。たとえば、 `SELECT * FROM employee WHERE id IN (1, 2, 3)`と`select * from EMPLOYEE where ID in (4, 5)`はどちらも同じ SQL ステートメント`select * from employee where id in (...)`の一部です。

いくつかの重要な情報は**Statement**で確認できます。

-   SQL ステートメントの概要: SQL ダイジェスト、SQL テンプレート ID、現在表示されている時間範囲、実行プランの数、実行が行われるデータベースなど。
-   実行計画リスト: SQL ステートメントに複数の実行計画がある場合、リストが表示されます。さまざまな実行計画を選択でき、選択した実行計画の詳細がリストの下部に表示されます。実行プランが 1 つしかない場合、リストは表示されません。
-   実行計画の詳細: 選択した実行計画の詳細が表示されます。このような SQL タイプの実行計画とそれに対応する実行時間をいくつかの観点から収集し、より多くの情報を得るのに役立ちます。 [実行計画の詳細](https://docs.pingcap.com/tidb/stable/dashboard-statement-details#statement-execution-details-of-tidb-dashboard) (下の画像の領域 3) を参照してください。

![Details](/media/dashboard/dashboard-statement-detail.png)

**Statement**ダッシュボードの情報に加えて、次のセクションで説明するように、 TiDB Cloudの SQL ベスト プラクティスもいくつかあります。

### 実行計画を確認する {#check-the-execution-plan}

[`EXPLAIN`](/explain-overview.md)を使用すると、コンパイル中にステートメントに対して TiDB によって計算された実行計画を確認できます。言い換えれば、TiDB は、数百または数千の可能な実行プランを推定し、リソースの消費が最小限で最も高速に実行される最適な実行プランを選択します。

TiDB によって選択された実行計画が最適でない場合は、 EXPLAINまたは[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)を使用して診断できます。

### 実行計画を最適化する {#optimize-the-execution-plan}

元のクエリ テキストを`parser`で解析し、基本的な妥当性を検証した後、TiDB はまずクエリに論理的に同等の変更をいくつか加えます。詳細については、 [SQL論理最適化](/sql-logical-optimization.md)を参照してください。

これらの等価性の変更により、論理実行プランでのクエリの処理が容易になります。等価性が変更された後、TiDB は元のクエリと同等のクエリ プラン構造を取得し、データ分散とオペレーターの特定の実行オーバーヘッドに基づいて最終的な実行プランを取得します。詳細については、 [SQLの物理的な最適化](/sql-physical-optimization.md)を参照してください。

また、TiDB は、 [実行計画キャッシュの準備](/sql-prepared-plan-cache.md)で紹介したように、 `PREPARE`ステートメントの実行時に実行プランの作成オーバーヘッドを削減するために、実行プラン キャッシュを有効にすることを選択できます。

### フルテーブルスキャンを最適化する {#optimize-full-table-scan}

SQL クエリが遅くなる最も一般的な理由は、 `SELECT`ステートメントがテーブル全体のスキャンを実行するか、間違ったインデックスを使用することです。 EXPLAINまたはEXPLAIN ANALYZE を使用すると、クエリの実行計画を表示し、実行が遅い原因を特定できます。最適化に使用できるものは[3つの方法](/develop/dev-guide-optimize-sql.md)あります。

-   セカンダリインデックスを使用する
-   カバリングインデックスを使用する
-   プライマリインデックスを使用する

### DML のベスト プラクティス {#dml-best-practices}

[DML のベスト プラクティス](/develop/dev-guide-optimize-sql-best-practices.md#dml-best-practices)を参照してください。

### 主キーを選択する場合の DDL のベスト プラクティス {#ddl-best-practices-when-selecting-primary-keys}

[主キーを選択する際に従うべきガイドライン](/develop/dev-guide-create-table.md#guidelines-to-follow-when-selecting-primary-key)を参照してください。

### インデックスのベストプラクティス {#index-best-practices}

[インデックス作成のベスト プラクティス](/develop/dev-guide-index-best-practice.md)は、インデックスの作成とインデックスの使用に関するベスト プラクティスが含まれています。

インデックスの作成速度はデフォルトでは控えめで、シナリオによってはインデックス作成プロセスを[変数の変更](/develop/dev-guide-optimize-sql-best-practices.md#add-index-best-practices)加速することができます。

<!--
### Use the slow log memory mapping table

You can query the contents of the slow query log by querying the [INFORMATION_SCHEMA.SLOW_QUERY](/identify-slow-queries.md#memory-mapping-in-slow-log) table, and find the structure in the [`SLOW_QUERY`](/information-schema/information-schema-slow-query.md) table. Using this table, you can perform queries using different fields to find potential problems.

The recommended analysis process for slow queries is as follows.

1. [Identify the performance bottleneck of the query](/analyze-slow-queries.md#identify-the-performance-bottleneck-of-the-query). That is, identify the part of the query process that takes long time.
2. [Analyze system issues](/analyze-slow-queries.md#analyze-system-issues). According to the bottleneck point, combine the monitoring, logging and other information at that time to find the possible causes.
3. [Analyze optimizer issues](/analyze-slow-queries.md#analyze-optimizer-issues). Analyze whether there is a better execution plan.
-->

## スキーマ設計の最適化 {#optimize-schema-design}

SQL パフォーマンス チューニングに基づいてもパフォーマンスを向上させることができない場合は、トランザクションの競合やホットスポットを回避するために、スキーマ設計とデータ読み取りモデルを確認する必要がある場合があります。

### トランザクションの競合 {#transaction-conflicts}

トランザクションの競合を特定して解決する方法の詳細については、 [ロックの競合のトラブルシューティング](https://docs.pingcap.com/tidb/stable/troubleshoot-lock-conflicts#troubleshoot-lock-conflicts)を参照してください。

### ホットスポットの問題 {#hotspot-issues}

[キービジュアライザー](/tidb-cloud/tune-performance.md#key-visualizer)を使用してホットスポットの問題を分析できます。

Key Visualizer を使用すると、TiDB クラスターの使用パターンを分析し、トラフィック ホットスポットのトラブルシューティングを行うことができます。このページには、TiDB クラスターのトラフィックの経時的な視覚的表現が表示されます。

Key Visualizer では次の情報を確認できます。最初に[基本概念](https://docs.pingcap.com/tidb/stable/dashboard-key-visualizer#basic-concepts)を理解する必要があるかもしれません。

-   全体的なトラフィックを時間の経過とともに示す大きなヒート マップ
-   ヒートマップの座標に関する詳細情報
-   左側に表示される表や索引などの識別情報

Key Visualizer には[4 つの一般的なヒート マップ結果](https://docs.pingcap.com/tidb/stable/dashboard-key-visualizer#common-heatmap-types)あります。

-   均等に分散されたワークロード: 望ましい結果
-   X 軸 (時間) に沿って明暗が交互に現れる: ピーク時にリソースを確認する必要がある
-   Y 軸に沿って明暗が交互に現れる: 生成されたホットスポットの集合の程度を確認する必要がある
-   明るい斜線: ビジネス モデルを確認する必要があります

X 軸と Y 軸が交互に明暗を繰り返すどちらの場合も、読み取り圧力と書き込み圧力に対処する必要があります。

SQL パフォーマンスの最適化の詳細については、SQL FAQ の[SQLの最適化](https://docs.pingcap.com/tidb/stable/sql-faq#sql-optimization)を参照してください。
