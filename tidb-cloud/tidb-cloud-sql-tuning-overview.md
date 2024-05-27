---
title: SQL Tuning Overview
summary: TiDB Cloudで SQL パフォーマンスを調整する方法について説明します。
---

# SQL チューニングの概要 {#sql-tuning-overview}

このドキュメントでは、TiDB Cloudで SQL パフォーマンスを調整する方法を紹介します。最高の SQL パフォーマンスを得るには、次の操作を実行できます。

-   SQL パフォーマンスを調整します。クエリ ステートメントの分析、実行プランの最適化、完全なテーブル スキャンの最適化など、SQL パフォーマンスを最適化する方法は多数あります。
-   スキーマ設計を最適化します。ビジネス ワークロードの種類によっては、トランザクションの競合やホットスポットを回避するためにスキーマを最適化する必要がある場合があります。

## SQLパフォーマンスの調整 {#tune-sql-performance}

SQL ステートメントのパフォーマンスを向上させるには、次の原則を考慮してください。

-   スキャンするデータの範囲を最小限に抑えます。常に、最小限の範囲のデータのみをスキャンし、すべてのデータをスキャンしないようにすることがベスト プラクティスです。
-   適切なインデックスを使用します。SQL ステートメントの`WHERE`節の各列には、対応するインデックスがあることを確認してください。そうでない場合、 `WHERE`節はテーブル全体をスキャンし、パフォーマンスが低下します。
-   適切な結合タイプを使用します。クエリ内の各テーブルのサイズと相関関係に応じて、適切な結合タイプを選択することが非常に重要です。通常、TiDB のコストベース オプティマイザーは最適な結合タイプを自動的に選択します。ただし、場合によっては結合タイプを手動で指定する必要があります。詳細については、 [テーブル結合を使用するステートメントを説明する](/explain-joins.md)参照してください。
-   適切なstorageエンジンを使用します。ハイブリッド トランザクションおよび分析処理 (HTAP) ワークロードには、 TiFlashstorageエンジンを使用することをお勧めします。1 [HTAP クエリ](/develop/dev-guide-hybrid-oltp-and-olap-queries.md)参照してください。

TiDB Cloud は、クラスター上の低速クエリを分析するのに役立ついくつかのツールを提供します。次のセクションでは、低速クエリを最適化するためのいくつかの方法について説明します。

### 診断タブのステートメントを使用する {#use-statement-on-the-diagnosis-tab}

TiDB Cloudコンソールの**[診断]**タブには**<a href="/tidb-cloud/tune-performance.md#statement-analysis">[SQL ステートメント]</a>**サブタブがあります。このサブタブは、クラスター上のすべてのデータベースの SQL ステートメントの実行統計を収集します。これを使用して、合計または 1 回の実行で長い時間を消費する SQL ステートメントを識別して分析できます。

このサブタブでは、同じ構造を持つ SQL クエリ (クエリ パラメータが一致しない場合でも) が同じ SQL ステートメントにグループ化されることに注意してください。たとえば、 `SELECT * FROM employee WHERE id IN (1, 2, 3)`と`select * from EMPLOYEE where ID in (4, 5)`どちらも同じ SQL ステートメント`select * from employee where id in (...)`の一部です。

**ステートメント**でいくつかの重要な情報を表示できます。

-   SQL ステートメントの概要: SQL ダイジェスト、SQL テンプレート ID、現在表示されている時間範囲、実行プランの数、実行が行われるデータベースなどが含まれます。
-   実行プラン リスト: SQL ステートメントに複数の実行プランがある場合は、リストが表示されます。異なる実行プランを選択でき、選択した実行プランの詳細がリストの下部に表示されます。実行プランが 1 つしかない場合は、リストは表示されません。
-   実行プランの詳細: 選択した実行プランの詳細を表示します。SQL タイプの実行プランと対応する実行時間を複数の観点から収集し、詳細情報の取得に役立ちます。1 (下の画像の領域[実行計画の詳細](https://docs.pingcap.com/tidb/stable/dashboard-statement-details#statement-execution-details-of-tidb-dashboard) ) を参照してください。

![Details](/media/dashboard/dashboard-statement-detail.png)

**ステートメント**ダッシュボードの情報に加えて、次のセクションで説明するように、TiDB Cloudの SQL ベスト プラクティスもいくつかあります。

### 実行計画を確認する {#check-the-execution-plan}

[`EXPLAIN`](/explain-overview.md)使用すると、コンパイル中に TiDB によって計算されたステートメントの実行プランを確認できます。つまり、TiDB は数百または数千の実行プランを推定し、消費するリソースが最も少なく、実行速度が最も速い最適な実行プランを選択します。

TiDB によって選択された実行プランが最適でない場合は、 EXPLAINまたは[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)使用して診断できます。

### 実行計画を最適化する {#optimize-the-execution-plan}

元のクエリ テキストを`parser`で解析し、基本的な有効性を検証した後、TiDB はまずクエリに対して論理的に同等の変更を加えます。詳細については、 [SQL 論理最適化](/sql-logical-optimization.md)を参照してください。

これらの等価性の変更により、クエリは論理実行プランで処理しやすくなります。等価性の変更後、TiDB は元のクエリと同等のクエリ プラン構造を取得し、その後、データ分布と演算子の特定の実行オーバーヘッドに基づいて最終的な実行プランを取得します。詳細については、 [SQL 物理最適化](/sql-physical-optimization.md)参照してください。

また、TiDB では、 [実行プランキャッシュの準備](/sql-prepared-plan-cache.md)で紹介されているように、 `PREPARE`ステートメントを実行するときに実行プランの作成オーバーヘッドを削減するために、実行プラン キャッシュを有効にすることを選択できます。

### フルテーブルスキャンの最適化 {#optimize-full-table-scan}

SQL クエリが遅くなる最も一般的な理由は、 `SELECT`ステートメントがフル テーブル スキャンを実行するか、間違ったインデックスを使用することですEXPLAINまたはEXPLAIN ANALYZE を使用して、クエリの実行プランを表示し、実行が遅い原因を特定できます。最適化に使用できるものは[3つの方法](/develop/dev-guide-optimize-sql.md)あります。

-   セカンダリインデックスを使用する
-   カバーインデックスを使用する
-   プライマリインデックスを使用する

### DMLのベストプラクティス {#dml-best-practices}

[DMLのベストプラクティス](/develop/dev-guide-optimize-sql-best-practices.md#dml-best-practices)参照。

### 主キーを選択する際の DDL のベスト プラクティス {#ddl-best-practices-when-selecting-primary-keys}

[主キーを選択する際のガイドライン](/develop/dev-guide-create-table.md#guidelines-to-follow-when-selecting-primary-key)参照。

### インデックスのベストプラクティス {#index-best-practices}

[インデックス作成のベストプラクティス](/develop/dev-guide-index-best-practice.md)には、インデックスの作成と使用に関するベスト プラクティスが含まれています。

デフォルトではインデックス作成の速度は控えめですが、シナリオによってはインデックス作成プロセスを[変数の変更](/develop/dev-guide-optimize-sql-best-practices.md#add-index-best-practices)高速化できます。

<!--
### Use the slow log memory mapping table

You can query the contents of the slow query log by querying the [INFORMATION_SCHEMA.SLOW_QUERY](/identify-slow-queries.md#memory-mapping-in-slow-log) table, and find the structure in the [`SLOW_QUERY`](/information-schema/information-schema-slow-query.md) table. Using this table, you can perform queries using different fields to find potential problems.

The recommended analysis process for slow queries is as follows.

1. [Identify the performance bottleneck of the query](/analyze-slow-queries.md#identify-the-performance-bottleneck-of-the-query). That is, identify the part of the query process that takes long time.
2. [Analyze system issues](/analyze-slow-queries.md#analyze-system-issues). According to the bottleneck point, combine the monitoring, logging and other information at that time to find the possible causes.
3. [Analyze optimizer issues](/analyze-slow-queries.md#analyze-optimizer-issues). Analyze whether there is a better execution plan.
-->

## スキーマ設計を最適化する {#optimize-schema-design}

SQL パフォーマンス チューニングを行ってもパフォーマンスが向上しない場合は、トランザクションの競合やホットスポットを回避するために、スキーマ設計とデータ読み取りモデルを確認する必要がある場合があります。

### トランザクションの競合 {#transaction-conflicts}

トランザクションの競合を特定して解決する方法の詳細については、 [ロック競合のトラブルシューティング](https://docs.pingcap.com/tidb/stable/troubleshoot-lock-conflicts#troubleshoot-lock-conflicts)を参照してください。

### ホットスポットの問題 {#hotspot-issues}

[キービジュアライザー](/tidb-cloud/tune-performance.md#key-visualizer)を使用してホットスポットの問題を分析できます。

Key Visualizer を使用すると、TiDB クラスターの使用パターンを分析し、トラフィックのホットスポットをトラブルシューティングできます。このページでは、TiDB クラスターのトラフィックの経時的な変化を視覚的に表示します。

Key Visualizer では次の情報を確認できます。まず、いくつか[基本概念](https://docs.pingcap.com/tidb/stable/dashboard-key-visualizer#basic-concepts)理解しておく必要があるかもしれません。

-   全体的なトラフィックを時間の経過とともに表示する大きなヒートマップ
-   ヒートマップの座標に関する詳細情報
-   左側に表示される表や索引などの識別情報

Key Visualizer には[4つの一般的なヒートマップの結果](https://docs.pingcap.com/tidb/stable/dashboard-key-visualizer#common-heatmap-types)あります。

-   均等に分散された作業負荷：望ましい結果
-   X軸（時間）に沿って明暗が交互に変化：ピーク時にリソースをチェックする必要がある
-   Y軸に沿って明暗が交互に変化：生成されたホットスポットの集約度合いを確認する必要がある
-   明るい斜線：ビジネスモデルを確認する必要がある

X 軸と Y 軸が交互に明暗を繰り返すどちらの場合も、読み取りおよび書き込みの圧力に対処する必要があります。

SQL パフォーマンスの最適化の詳細については、「SQL FAQ」の[SQL 最適化](https://docs.pingcap.com/tidb/stable/sql-faq#sql-optimization)参照してください。
