---
title: SQL Tuning Overview
summary: TiDB Cloudで SQL のパフォーマンスをチューニングする方法について学びましょう。
---

# SQLチューニングの概要 {#sql-tuning-overview}

このドキュメントでは、TiDB Cloudで SQL のパフォーマンスをチューニングする方法について説明します。最高の SQL パフォーマンスを得るには、次の操作を実行できます。

-   SQLのパフォーマンスを最適化しましょう。SQLのパフォーマンスを最適化する方法は数多くあり、クエリ文の分析、実行プランの最適化、フルテーブルスキャンの最適化などが挙げられます。
-   スキーマ設計を最適化してください。業務ワークロードの種類によっては、トランザクションの競合やホットスポットを回避するために、スキーマを最適化する必要がある場合があります。

## SQLパフォーマンスのチューニング {#tune-sql-performance}

SQL文のパフォーマンスを向上させるには、以下の原則を考慮してください。

-   スキャン対象データの範囲を最小限に抑えましょう。常に、必要最小限のデータのみをスキャンし、すべてのデータをスキャンすることは避けるのが最善策です。
-   適切なインデックスを使用してください。SQL文の`WHERE`句の各列には、対応するインデックスが存在することを確認してください。そうでない場合、 `WHERE`句はテーブル全体をスキャンするため、パフォーマンスが低下します。
-   適切な結合タイプを使用してください。クエリ内の各テーブルのサイズと相関関係に応じて、適切な結合タイプを選択することが非常に重要です。一般に、TiDB のコストベースのオプティマイザーは、最適な結合タイプを自動的に選択します。ただし、場合によっては、結合タイプを手動で指定する必要がある場合があります。詳細については、[テーブル結合を使用するステートメントについて説明します](/explain-joins.md)参照してください。
-   適切なストレージエンジンを使用してください。ハイブリッドトランザクションおよび分析処理（HTAP）ワークロードには、 TiFlashストレージエンジンを使用することをお勧めします。HTAP [HTAPクエリ](/develop/dev-guide-hybrid-oltp-and-olap-queries.md)を参照してください。

TiDB Cloudには、スロークエリを分析するのに役立つツールがいくつか用意されています。以下のセクションでは、スロークエリを最適化するためのいくつかの方法について説明します。

### 診断ページの「使用説明書」を参照してください。 {#use-statement-on-the-diagnosis-page}

TiDB Cloudコンソールには、 [**診断**](/tidb-cloud/tune-performance.md#view-the-diagnosis-page)上に[**SQLステートメント**](/tidb-cloud/tune-performance.md#statement-analysis)タブが用意されています。このタブでは、TiDB Cloudリソース上のすべてのデータベースの SQL ステートメントの実行統計情報を収集します。これを使用して、合計または単一の実行に長い時間を要する SQL ステートメントを特定し、分析することができます。

このページでは、構造が同じ SQL クエリ (クエリ パラメータが一致しない場合でも) は、同じ SQL ステートメントにグループ化されることに注意してください。たとえば、 `SELECT * FROM employee WHERE id IN (1, 2, 3)`と`select * from EMPLOYEE where ID in (4, 5)`は、どちらも同じ SQL ステートメント`select * from employee where id in (...)`の一部です。

**SQLステートメント**でいくつかの重要な情報を確認できます。

-   **SQLテンプレート**：SQLダイジェスト、SQLテンプレートID、現在表示されている時間範囲、実行プランの数、および実行が行われるデータベースが含まれます。

    ![Details0](/media/dashboard/dashboard-statement-detail0.png)

-   実行プラン一覧：SQL文に複数の実行プランがある場合、一覧が表示されます。複数の実行プランを選択すると、選択した実行プランの詳細が一覧の下部に表示されます。実行プランが1つしかない場合は、一覧は表示されません。

    ![Details1](/media/dashboard/dashboard-statement-detail1.png)

-   実行プランの詳細：選択した実行プランの詳細を表示します。各SQLタイプの実行プランと、複数の視点からの対応する実行時間を収集し、より多くの情報を取得するのに役立ちます。 [実行計画](https://docs.pingcap.com/tidb/stable/dashboard-statement-details#execution-plans)参照してください。

    ![Details2](/media/dashboard/dashboard-statement-detail2.png)

-   関連するスロークエリ

**ステートメント**ダッシュボードの情報に加えて、 TiDB CloudにはSQLのベストプラクティスもいくつかあり、以下のセクションで説明します。

### 実行計画を確認する {#check-the-execution-plan}

[`EXPLAIN`](/explain-overview.md)使用すると、コンパイル時にTiDBが計算したステートメントの実行プランを確認できます。つまり、TiDBは数百または数千もの実行プランを推定し、リソース消費が最も少なく、実行速度が最も速い最適な実行プランを選択します。

TiDBによって選択された実行プランが最適でない場合は、 EXPLAINまたは[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)使用して診断できます。

### 実行計画を最適化する {#optimize-the-execution-plan}

`parser`による元のクエリテキストの解析と基本的な妥当性検証の後、TiDB はまずクエリに対して論理的に同等の変更を行います。詳細については、 [SQL論理最適化](/sql-logical-optimization.md)参照してください。 .

これらの等価性の変更により、クエリは論理実行プランで扱いやすくなります。等価性の変更後、TiDB は元のクエリと等価なクエリ プラン構造を取得し、データ分布と演算子の特定の実行オーバーヘッドに基づいて最終的な実行プランを取得します。詳細については、 [SQLの物理的最適化](/sql-physical-optimization.md)参照してください。

また、実行プラン キャッシュを準備するで紹介したように、TiDB は、 `PREPARE`ステートメントの実行時に実行プランの作成オーバーヘッドを削減するために、[実行プランキャッシュを準備する](/sql-prepared-plan-cache.md)。

### フルテーブルスキャンを最適化 {#optimize-full-table-scan}

SQLクエリが遅くなる最も一般的な原因は、 `SELECT`ステートメントがフルテーブルスキャンを実行するか、不適切なインデックスを使用していることです。EXPLAINまたはEXPLAIN ANALYZEを使用してクエリの実行プランを表示し、実行が遅くなる原因を特定できます。最適化に使用できる[3つの方法](/develop/dev-guide-optimize-sql.md)あります。

-   セカンダリインデックスを使用する
-   カバーインデックスを使用する
-   プライマリーインデックスを使用する

### DMLのベストプラクティス {#dml-best-practices}

[DMLのベストプラクティス](/develop/dev-guide-optimize-sql-best-practices.md#dml-best-practices)を参照してください。

### 主キーを選択する際のDDLのベストプラクティス {#ddl-best-practices-when-selecting-primary-keys}

[主キーを選択する際に従うべきガイドライン](/develop/dev-guide-create-table.md#guidelines-to-follow-when-selecting-primary-key)参照してください。

### インデックスのベストプラクティス {#index-best-practices}

インデックス [インデックス作成のベストプラクティス](/develop/dev-guide-index-best-practice.md)ベストプラクティスには、インデックスの作成とインデックスの使用に関するベスト プラクティスが含まれています。

インデックスの作成速度はデフォルトでは控えめですが、シナリオによっては[変数の変更](/develop/dev-guide-optimize-sql-best-practices.md#add-index-best-practices)によってインデックス作成プロセスを高速化できます。

<!--
### Use the slow log memory mapping table

You can query the contents of the slow query log by querying the [INFORMATION_SCHEMA.SLOW_QUERY](/identify-slow-queries.md#memory-mapping-in-slow-log) table, and find the structure in the [`SLOW_QUERY`](/information-schema/information-schema-slow-query.md) table. Using this table, you can perform queries using different fields to find potential problems.

The recommended analysis process for slow queries is as follows.

1. [Identify the performance bottleneck of the query](/analyze-slow-queries.md#identify-the-performance-bottleneck-of-the-query). That is, identify the part of the query process that takes long time.
2. [Analyze system issues](/analyze-slow-queries.md#analyze-system-issues). According to the bottleneck point, combine the monitoring, logging and other information at that time to find the possible causes.
3. [Analyze optimizer issues](/analyze-slow-queries.md#analyze-optimizer-issues). Analyze whether there is a better execution plan.
-->

## スキーマ設計を最適化する {#optimize-schema-design}

SQLパフォーマンスチューニングを行ってもパフォーマンスが改善されない場合は、トランザクションの競合やホットスポットを回避するために、スキーマ設計とデータ読み取りモデルを見直す必要があるかもしれません。

### トランザクションの競合 {#transaction-conflicts}

トランザクションの競合を特定して解決する方法の詳細については、 [ロックの競合をトラブルシューティングする](https://docs.pingcap.com/tidb/stable/troubleshoot-lock-conflicts#troubleshoot-lock-conflicts)参照してください。

<CustomContent plan="starter,essential,dedicated">

### ホットスポットの問題 {#hotspot-issues}

[Key Visualizer](/tidb-cloud/tune-performance.md#key-visualizer)を使用してホットスポットの問題を分析できます。

Key Visualizerを使用すると、 TiDB Cloud Dedicatedクラスタの使用パターンを分析し、トラフィックのホットスポットをトラブルシューティングできます。このページでは、TiDB Cloud Dedicatedクラスタのトラフィックの推移を視覚的に表示します。

Key Visualizerでは、以下の情報を確認できます。まず、いくつかの[基本概念](https://docs.pingcap.com/tidb/stable/dashboard-key-visualizer#basic-concepts)を理解しておく必要があるかもしれません。

-   時間の経過に伴う全体の交通量を示す大きなヒートマップ
-   ヒートマップの座標に関する詳細情報
-   左側に表示される表や索引などの識別情報

Key Visualizerには[4つの一般的なヒートマップ結果](https://docs.pingcap.com/tidb/stable/dashboard-key-visualizer#common-heatmap-types)があります。

-   均等に分散されたワークロード：望ましい結果
-   X軸（時間）に沿って明るさと暗さが交互に変化する：ピーク時のリソースを確認する必要がある
-   Y軸に沿って明暗が交互に変化する：生成されたホットスポットの集積度をチェックする必要がある
-   明るい斜線：ビジネスモデルを見直す必要がある

X軸とY軸が交互に明暗を繰り返す場合、どちらのケースでも読み書き時の筆圧に対処する必要があります。

SQLのパフォーマンス[SQL最適化](https://docs.pingcap.com/tidb/stable/sql-faq#sql-optimization)を参照してください。

</CustomContent>
