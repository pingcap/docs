---
title: SQL Tuning Overview
summary: Learn about how to tune SQL performance in TiDB Cloud.
---

# SQLチューニングの概要 {#sql-tuning-overview}

このドキュメントでは、 TiDB CloudでSQLパフォーマンスを調整する方法を紹介します。最高のSQLパフォーマンスを得るには、次のようにします。

-   SQLパフォーマンスを調整します。クエリステートメントの分析、実行プランの最適化、全表スキャンの最適化など、SQLのパフォーマンスを最適化する方法はたくさんあります。
-   スキーマ設計を最適化します。ビジネスワークロードのタイプによっては、トランザクションの競合やホットスポットを回避するためにスキーマを最適化する必要がある場合があります。

## SQLパフォーマンスの調整 {#tune-sql-performance}

SQLステートメントのパフォーマンスを向上させるには、次の原則を考慮してください。

-   スキャンしたデータの範囲を最小限に抑えます。最小限の範囲のデータのみをスキャンし、すべてのデータをスキャンしないようにすることが常にベストプラクティスです。
-   適切なインデックスを使用します。 SQLステートメントの`WHERE`句の各列について、対応するインデックスがあることを確認してください。そうしないと、 `WHERE`句がテーブル全体をスキャンし、パフォーマンスが低下します。
-   適切な結合タイプを使用してください。クエリ内の各テーブルのサイズと相関関係に応じて、適切な結合タイプを選択することが非常に重要です。通常、TiDBのコストベースのオプティマイザは、最適な結合タイプを自動的に選択します。ただし、場合によっては、結合タイプを手動で指定する必要があります。詳細については、 [テーブル結合を使用するステートメントを説明する](/explain-joins.md)を参照してください。
-   適切なストレージエンジンを使用してください。ハイブリッドトランザクションおよび分析処理（HTAP）ワークロードには、TiFlashストレージエンジンを使用することをお勧めします。 [HTAPクエリ](https://docs.pingcap.com/tidb/stable/dev-guide-hybrid-oltp-and-olap-queries)を参照してください。

TiDB Cloudは、クラスタ上の遅いクエリを分析するのに役立ついくつかのツールを提供します。次のセクションでは、遅いクエリを最適化するためのいくつかのアプローチについて説明します。

### [診断]タブの[ステートメントを使用] {#use-statement-on-the-diagnosis-tab}

TiDB Cloudコンソールには、[**診断**]タブに[<strong><a href="/tidb-cloud/tune-performance.md#statement-analysis">ステートメント</a></strong>]サブタブがあります。クラスタ上のすべてのデータベースのSQLステートメントの実行統計を収集します。これを使用して、合計または1回の実行で長い時間を消費するSQLステートメントを識別および分析できます。

このサブタブでは、同じ構造のSQLクエリが（クエリパラメータが一致しない場合でも）同じSQLステートメントにグループ化されることに注意してください。たとえば、 `SELECT * FROM employee WHERE id IN (1, 2, 3)`と`select * from EMPLOYEE where ID in (4, 5)`は両方とも同じSQLステートメント`select * from employee where id in (...)`の一部です。

**ステートメント**でいくつかの重要な情報を表示できます。

-   SQLステートメントの概要：SQLダイジェスト、SQLテンプレートID、現在表示されている時間範囲、実行プランの数、および実行が行われるデータベースを含みます。
-   実行プランリスト：SQLステートメントに複数の実行プランがある場合、リストが表示されます。さまざまな実行プランを選択でき、選択した実行プランの詳細がリストの下部に表示されます。実行プランが1つしかない場合、リストは表示されません。
-   実行プランの詳細：選択した実行プランの詳細を表示します。このようなSQLタイプの実行プランと対応する実行時間をいくつかの観点から収集して、より多くの情報を取得できるようにします。 [実行計画の詳細](https://docs.pingcap.com/tidb/stable/dashboard-statement-details#statement-execution-details-of-tidb-dashboard) （下の画像の領域3）を参照してください。

![Details](/media/dashboard/dashboard-statement-detail.png)

**ステートメント**ダッシュボードの情報に加えて、次のセクションで説明するように、 TiDB CloudのSQLのベストプラクティスもいくつかあります。

### 実行計画を確認する {#check-the-execution-plan}

[`EXPLAIN`](/explain-overview.md)を使用して、コンパイル中にステートメントのTiDBによって計算された実行プランを確認できます。言い換えると、TiDBは数百または数千の可能な実行プランを推定し、リソースの消費が最も少なく、実行が最も速い最適な実行プランを選択します。

TiDBによって選択された実行プランが最適でない場合は、 EXPLAINまたは[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)を使用して診断できます。

### 実行計画を最適化する {#optimize-the-execution-plan}

元のクエリテキストを`parser`で解析し、基本的な有効性を検証した後、TiDBは最初にクエリに論理的に同等の変更を加えます。詳細については、 [SQL論理最適化](/sql-logical-optimization.md)を参照してください。

これらの同等性の変更により、論理実行プランでのクエリの処理が容易になります。同等性が変更された後、TiDBは、元のクエリと同等のクエリプラン構造を取得し、データ分散とオペレーターの特定の実行オーバーヘッドに基づいて最終的な実行プランを取得します。詳細については、 [SQLの物理的最適化](/sql-physical-optimization.md)を参照してください。

また、TiDBは、 [実行プランキャッシュの準備](/sql-prepared-plan-cache.md)で紹介したように、実行プランキャッシュを有効にして、 `PREPARE`ステートメントを実行するときの実行プランの作成オーバーヘッドを削減することを選択できます。

### 全表スキャンを最適化する {#optimize-full-table-scan}

SQLクエリが遅い最も一般的な理由は、 `SELECT`ステートメントが全表スキャンを実行するか、誤ったインデックスを使用することです。 EXPLAINまたはEXPLAINを使用して、クエリの実行プランを表示し、実行が遅い原因を特定できます。最適化に使用できるものは[3つの方法](https://docs.pingcap.com/tidb/stable/dev-guide-optimize-sql)あります。

-   二次インデックスを使用する
-   カバーインデックスを使用する
-   プライマリインデックスを使用する

### DMLのベストプラクティス {#dml-best-practices}

[DMLのベストプラクティス](https://docs.pingcap.com/tidb/stable/dev-guide-optimize-sql-best-practices#dml-best-practices)を参照してください。

### 主キーを選択する際のDDLのベストプラクティス {#ddl-best-practices-when-selecting-primary-keys}

[主キーを選択する際に従うべきガイドライン](https://docs.pingcap.com/tidb/stable/dev-guide-create-table#guidelines-to-follow-when-selecting-primary-key)を参照してください。

### インデックスのベストプラクティス {#index-best-practices}

[インデックス作成のベストプラクティス](https://docs.pingcap.com/tidb/stable/dev-guide-index-best-practice)には、インデックスを作成してインデックスを使用するためのベストプラクティスが含まれています。

インデックスの作成速度はデフォルトでは控えめであり、シナリオによってはインデックス作成プロセスを[変数の変更](https://docs.pingcap.com/tidb/stable/dev-guide-optimize-sql-best-practices#add-index-best-practices)加速できます。

<!--
### Use the slow log memory mapping table

You can query the contents of the slow query log by querying the [INFORMATION_SCHEMA.SLOW_QUERY](/identify-slow-queries.md#memory-mapping-in-slow-log) table, and find the structure in the [`SLOW_QUERY`](/information-schema/information-schema-slow-query.md) table. Using this table, you can perform queries using different fields to find potential problems.

The recommended analysis process for slow queries is as follows.

1. [Identify the performance bottleneck of the query](/analyze-slow-queries.md#identify-the-performance-bottleneck-of-the-query). That is, identify the part of the query process that takes long time.
2. [Analyze system issues](/analyze-slow-queries.md#analyze-system-issues). According to the bottleneck point, combine the monitoring, logging and other information at that time to find the possible causes.
3. [Analyze optimizer issues](/analyze-slow-queries.md#analyze-optimizer-issues). Analyze whether there is a better execution plan.
-->

## スキーマ設計を最適化する {#optimize-schema-design}

それでもSQLパフォーマンスチューニングに基づいてパフォーマンスを向上させることができない場合は、トランザクションの競合やホットスポットを回避するために、スキーマ設計とデータ読み取りモデルを確認する必要があります。

### トランザクションの競合 {#transaction-conflicts}

トランザクションの競合を見つけて解決する方法の詳細については、 [ロックの競合のトラブルシューティング](https://docs.pingcap.com/tidb/stable/troubleshoot-lock-conflicts#troubleshoot-lock-conflicts)を参照してください。

### ホットスポットの問題 {#hotspot-issues}

[キービジュアライザー](/tidb-cloud/tune-performance.md#key-visualizer)を使用してホットスポットの問題を分析できます。

Key Visualizerを使用して、TiDBクラスターの使用パターンを分析し、トラフィックのホットスポットをトラブルシューティングできます。このページでは、時間の経過に伴うTiDBクラスターのトラフィックを視覚的に表現します。

KeyVisualizerで次の情報を確認できます。最初にいくつ[基本概念](https://docs.pingcap.com/tidb/stable/dashboard-key-visualizer#basic-concepts)を理解する必要があるかもしれません。

-   時間の経過に伴う全体的なトラフィックを示す大きなヒートマップ
-   ヒートマップの座標に関する詳細情報
-   左側に表示されるテーブルやインデックスなどの識別情報

Key Visualizerには、 [4つの一般的なヒートマップの結果](https://docs.pingcap.com/tidb/stable/dashboard-key-visualizer#common-heatmap-types)があります。

-   均等に分散されたワークロード：望ましい結果
-   X軸（時間）に沿って交互に明るさと暗さ：ピーク時にリソースをチェックする必要があります
-   Y軸に沿って交互に明るさと暗さ：生成されたホットスポットの集約の程度を確認する必要があります
-   明るい対角線：ビジネスモデルを確認する必要があります

X軸とY軸が交互に明るい場合と暗い場合の両方で、読み取りと書き込みの圧力に対処する必要があります。

SQLパフォーマンスの最適化の詳細については、SQLFAQの[SQLの最適化](https://docs.pingcap.com/tidb/stable/sql-faq#sql-optimization)を参照してください。
