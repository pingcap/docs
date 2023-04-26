---
title: SQL Tuning Overview
summary: Learn about how to tune SQL performance in TiDB Cloud.
---

# SQL チューニングの概要 {#sql-tuning-overview}

このドキュメントでは、 TiDB Cloudで SQL パフォーマンスを調整する方法を紹介します。最高の SQL パフォーマンスを得るには、次のことを実行できます。

-   SQL パフォーマンスを調整します。クエリ ステートメントの分析、実行計画の最適化、全テーブル スキャンの最適化など、SQL パフォーマンスを最適化する方法は多数あります。
-   スキーマ設計を最適化します。ビジネス ワークロードの種類によっては、トランザクションの競合やホットスポットを回避するためにスキーマを最適化する必要がある場合があります。

## SQL パフォーマンスの調整 {#tune-sql-performance}

SQL ステートメントのパフォーマンスを向上させるには、次の原則を考慮してください。

-   スキャンしたデータの範囲を最小限に抑えます。最小限の範囲のデータのみをスキャンし、すべてのデータをスキャンしないようにすることが常にベスト プラクティスです。
-   適切な索引を使用してください。 SQL ステートメントの`WHERE`句の各列について、対応するインデックスがあることを確認してください。そうしないと、 `WHERE`句がテーブル全体をスキャンし、パフォーマンスが低下します。
-   適切な結合タイプを使用してください。クエリ内の各テーブルのサイズと相関関係に応じて、適切な結合タイプを選択することが非常に重要です。一般に、TiDB のコストベースのオプティマイザは、最適な Join タイプを自動的に選択します。ただし、場合によっては、結合タイプを手動で指定する必要があります。詳細については、 [テーブル結合を使用するステートメントの説明](/explain-joins.md)を参照してください。
-   適切なstorageエンジンを使用します。 Hybrid Transactional and Analytical Processing (HTAP) ワークロードには、 TiFlashstorageエンジンを使用することをお勧めします。 [HTAP クエリ](/develop/dev-guide-hybrid-oltp-and-olap-queries.md)を参照してください。

TiDB Cloud は、クラスター上の低速クエリを分析するのに役立ついくつかのツールを提供します。次のセクションでは、スロー クエリを最適化するためのいくつかのアプローチについて説明します。

### [診断] タブでステートメントを使用する {#use-statement-on-the-diagnosis-tab}

TiDB Cloudコンソールは、 **SQL 診断**タブに<strong><a href="/tidb-cloud/tune-performance.md#statement-analysis">SQL ステートメント</a></strong>サブタブを提供します。クラスター上のすべてのデータベースの SQL ステートメントの実行統計を収集します。これを使用して、合計または 1 回の実行で長い時間を消費する SQL ステートメントを特定して分析できます。

このサブタブでは、(クエリ パラメータが一致しない場合でも) 同じ構造を持つ SQL クエリが同じ SQL ステートメントにグループ化されることに注意してください。たとえば、 `SELECT * FROM employee WHERE id IN (1, 2, 3)`と`select * from EMPLOYEE where ID in (4, 5)`はどちらも同じ SQL ステートメント`select * from employee where id in (...)`の一部です。

**Statement**でいくつかの重要な情報を確認できます。

-   SQL ステートメントの概要: SQL ダイジェスト、SQL テンプレート ID、現在表示されている時間範囲、実行計画の数、および実行が行われるデータベースを含みます。
-   実行計画リスト: SQL ステートメントに複数の実行計画がある場合、リストが表示されます。さまざまな実行計画を選択でき、選択した実行計画の詳細がリストの下部に表示されます。実行計画が 1 つしかない場合、リストは表示されません。
-   実行計画の詳細: 選択した実行計画の詳細を表示します。このような SQL タイプの実行計画と対応する実行時間をいくつかの観点から収集して、より多くの情報を取得できるようにします。 [実行計画の詳細](https://docs.pingcap.com/tidb/stable/dashboard-statement-details#statement-execution-details-of-tidb-dashboard)を参照してください (下の画像の領域 3)。

![Details](/media/dashboard/dashboard-statement-detail.png)

**Statement**ダッシュボードの情報に加えて、次のセクションで説明するように、 TiDB Cloudの SQL ベスト プラクティスもいくつかあります。

### 実行計画を確認する {#check-the-execution-plan}

[`EXPLAIN`](/explain-overview.md)を使用して、コンパイル中に TiDB によって計算されたステートメントの実行計画を確認できます。つまり、TiDB は数百または数千の実行計画を推定し、リソースの消費が最も少なく、実行速度が最も速い最適な実行計画を選択します。

TiDB によって選択された実行計画が最適でない場合は、 EXPLAINまたは[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)を使用して診断できます。

### 実行計画を最適化する {#optimize-the-execution-plan}

元のクエリ テキストを`parser`で解析し、基本的な有効性を検証した後、TiDB は最初に論理的に同等の変更をクエリに加えます。詳細については、 [SQL 論理最適化](/sql-logical-optimization.md)を参照してください。

これらの等価性の変更により、クエリは論理実行プランで処理しやすくなります。同等性が変化した後、TiDB は元のクエリと同等のクエリ プラン構造を取得し、データ分散とオペレーターの特定の実行オーバーヘッドに基づいて最終的な実行プランを取得します。詳細については、 [SQL 物理最適化](/sql-physical-optimization.md)を参照してください。

また、TiDB は、実行計画キャッシュを有効にして、 `PREPARE`ステートメントを実行するときの実行計画の作成オーバーヘッドを削減することもできます ( [実行計画キャッシュの準備](/sql-prepared-plan-cache.md)で紹介)。

### テーブル全体のスキャンを最適化する {#optimize-full-table-scan}

SQL クエリが遅くなる最も一般的な理由は、 `SELECT`ステートメントが全テーブル スキャンを実行するか、不適切なインデックスを使用することです。 EXPLAINまたはEXPLAIN ANALYZE を使用して、クエリの実行計画を表示し、実行が遅い原因を突き止めることができます。最適化に使用できるものは[3つの方法](/develop/dev-guide-optimize-sql.md)あります。

-   セカンダリ インデックスを使用する
-   カバリングインデックスを使用
-   プライマリ インデックスを使用

### DML のベスト プラクティス {#dml-best-practices}

[DML のベスト プラクティス](/develop/dev-guide-optimize-sql-best-practices.md#dml-best-practices)を参照してください。

### 主キーを選択する際の DDL のベスト プラクティス {#ddl-best-practices-when-selecting-primary-keys}

[主キーを選択する際に従うべきガイドライン](/develop/dev-guide-create-table.md#guidelines-to-follow-when-selecting-primary-key)を参照してください。

### インデックスのベスト プラクティス {#index-best-practices}

[インデックス作成のベスト プラクティス](/develop/dev-guide-index-best-practice.md)は、インデックスの作成とインデックスの使用に関するベスト プラクティスが含まれています。

インデックス作成の速度はデフォルトでは控えめであり、一部のシナリオではインデックス作成プロセスを[変数の変更](/develop/dev-guide-optimize-sql-best-practices.md#add-index-best-practices)高速化できます。

<!--
### Use the slow log memory mapping table

You can query the contents of the slow query log by querying the [INFORMATION_SCHEMA.SLOW_QUERY](/identify-slow-queries.md#memory-mapping-in-slow-log) table, and find the structure in the [`SLOW_QUERY`](/information-schema/information-schema-slow-query.md) table. Using this table, you can perform queries using different fields to find potential problems.

The recommended analysis process for slow queries is as follows.

1. [Identify the performance bottleneck of the query](/analyze-slow-queries.md#identify-the-performance-bottleneck-of-the-query). That is, identify the part of the query process that takes long time.
2. [Analyze system issues](/analyze-slow-queries.md#analyze-system-issues). According to the bottleneck point, combine the monitoring, logging and other information at that time to find the possible causes.
3. [Analyze optimizer issues](/analyze-slow-queries.md#analyze-optimizer-issues). Analyze whether there is a better execution plan.
-->

## スキーマ設計の最適化 {#optimize-schema-design}

それでも SQL パフォーマンス チューニングに基づいてパフォーマンスを向上できない場合は、スキーマの設計とデータ読み取りモデルを確認して、トランザクションの競合とホットスポットを回避する必要があります。

### トランザクションの競合 {#transaction-conflicts}

トランザクションの競合を見つけて解決する方法の詳細については、 [ロック競合のトラブルシューティング](https://docs.pingcap.com/tidb/stable/troubleshoot-lock-conflicts#troubleshoot-lock-conflicts)を参照してください。

### ホットスポットの問題 {#hotspot-issues}

[キー ビジュアライザー](/tidb-cloud/tune-performance.md#key-visualizer)を使用して、ホットスポットの問題を分析できます。

Key Visualizer を使用して、TiDB クラスターの使用パターンを分析し、トラフィックのホットスポットをトラブルシューティングできます。このページでは、TiDB クラスターのトラフィックを経時的に視覚的に表現しています。

Key Visualizer で次の情報を確認できます。最初にいくつかの[基本概念](https://docs.pingcap.com/tidb/stable/dashboard-key-visualizer#basic-concepts)理解する必要があるかもしれません。

-   時間の経過に伴う全体的なトラフィックを示す大きなヒート マップ
-   ヒートマップの座標に関する詳細情報
-   左側に表示される表や索引などの識別情報

Key Visualizer には[4 つの一般的なヒート マップの結果](https://docs.pingcap.com/tidb/stable/dashboard-key-visualizer#common-heatmap-types)があります。

-   均等に分散されたワークロード: 望ましい結果
-   X軸（時間）に沿って明暗が交互に変化：ピーク時にリソースを確認する必要があります
-   Y 軸に沿って明暗が交互に変化: 生成されたホットスポットの凝集度を確認する必要があります
-   明るい斜線：ビジネスモデルの確認が必要

X 軸と Y 軸が交互に明るい部分と暗い部分のどちらの場合でも、読み取りと書き込みの圧力に対処する必要があります。

SQL パフォーマンスの最適化の詳細については、SQL FAQ の[SQL の最適化](https://docs.pingcap.com/tidb/stable/sql-faq#sql-optimization)を参照してください。
