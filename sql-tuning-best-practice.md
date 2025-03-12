---
title: A Practical Guide for SQL Tuning
summary: パフォーマンスを向上させるために SQL クエリを最適化する方法を学習します。
---

# SQL チューニングの実践ガイド {#a-practical-guide-for-sql-tuning}

このガイドは、 TiDB SQLチューニングの初心者向けに設計されています。次の主要な原則に焦点を当てています。

-   参入障壁が低い: チューニングの概念と方法を段階的に紹介します。
-   実践指向: それぞれの最適化のヒントについて具体的な手順と例を提供します。
-   クイック スタート: 最も一般的で効果的な最適化方法を優先します。
-   緩やかな学習曲線: 複雑な理論ではなく実践的なテクニックを重視します。
-   シナリオベース: 実際のビジネスケースを使用して最適化の効果を実証します。

## SQLチューニング入門 {#introduction-to-sql-tuning}

SQL チューニングは、データベース パフォーマンスを最適化するために不可欠です。SQL チューニングでは、次の一般的な手順を通じて、SQL クエリの効率を体系的に改善します。

1.  影響の大きい SQL ステートメントを特定します。

    -   SQL 実行履歴を確認して、システム リソースを大量に消費したり、アプリケーションのワークロードに大きく影響したりするステートメントを見つけます。
    -   監視ツールとパフォーマンス メトリックを使用して、リソースを大量に消費するクエリを特定します。

2.  実行プランを分析します。

    -   特定されたステートメントに対してクエリ オプティマイザーによって生成された実行プランを調べます。
    -   これらのプランが合理的に効率的であり、適切なインデックスと結合方法が使用されているかどうかを確認します。

3.  最適化を実装する:

    非効率的な SQL ステートメントに最適化を実装します。最適化には、SQL ステートメントの書き換え、インデックスの追加または変更、統計の更新、データベース パラメータの調整などが含まれます。

以下の手順を繰り返す:

-   システムのパフォーマンスは目標要件を満たしています。
-   残りのステートメントについては、これ以上の改善はできません。

SQL チューニングは継続的なプロセスです。データ量が増え、クエリ パターンが変化するにつれて、次のことを行う必要があります。

-   クエリのパフォーマンスを定期的に監視します。
-   最適化戦略を再評価します。
-   新たなパフォーマンスの課題に対処するためにアプローチを調整します。

これらのプラクティスを一貫して適用することで、長期にわたって最適なデータベース パフォーマンスを維持できます。

## SQLチューニングの目的 {#goals-of-sql-tuning}

SQL チューニングの主な目的は次のとおりです。

-   エンドユーザーへの応答時間を短縮します。
-   クエリ実行中のリソース消費を最小限に抑えます。

これらの目標を達成するには、次の戦略を使用できます。

### クエリ実行を最適化する {#optimize-query-execution}

SQL チューニングは、クエリ機能を変更せずに同じワークロードをより効率的に処理する方法を見つけることに重点を置いています。クエリの実行は次のように最適化できます。

1.  実行計画の改善:
    -   より効率的な処理のためにクエリ構造を分析および変更します。
    -   適切なインデックスを使用して、データ アクセスと処理時間を短縮します。
    -   大規模なデータセットに対する分析クエリにTiFlashを有効にし、複雑な集計や結合に超並列処理 (MPP) エンジンを活用します。

2.  データアクセス方法の強化:
    -   カバーリング インデックスを使用して、テーブル全体のスキャンを回避し、インデックスから直接クエリを実行します。
    -   パーティション戦略を実装して、データスキャンを関連するパーティションに制限します。

例:

-   頻繁にクエリされる列にインデックスを作成すると、特にテーブルの小さな部分にアクセスするクエリの場合、リソースの使用量が大幅に削減されます。
-   完全なテーブルスキャンとソート操作を回避するために、限られた数のソートされた結果を返すクエリにはインデックスのみのスキャンを使用します。

### 作業負荷の分散をバランスよく行う {#balance-workload-distribution}

TiDB のような分散アーキテクチャでは、TiKV ノード間でワークロードを分散することが、最適なパフォーマンスを得るために不可欠です。読み取りおよび書き込みのホットスポットを特定して解決するには、 [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md#optimization-of-small-table-hotspots)参照してください。

これらの戦略を実装することで、TiDB クラスターが利用可能なすべてのリソースを効率的に利用し、個々の TiKV ノードでのワークロードの不均一な分散やシリアル化によって発生するボトルネックを回避できるようになります。

## 高負荷SQLを特定する {#identify-high-load-sql}

リソースを大量に消費する SQL ステートメントを識別する最も効率的な方法は、 [TiDBダッシュボード](/dashboard/dashboard-overview.md)使用することです。また、ビューやログなどの他のツールを使用して、負荷の高い SQL ステートメントを識別することもできます。

### TiDBダッシュボードを使用してSQL文を監視する {#monitor-sql-statements-using-tidb-dashboard}

#### SQL ステートメント ページ {#sql-statements-page}

[TiDBダッシュボード](/dashboard/dashboard-overview.md)で[**SQL ステートメント**ページ](/dashboard/dashboard-statement-list.md)に移動して、次の点を確認します。

-   合計レイテンシーが最も高い SQL ステートメント。これは、複数回の実行にわたって実行に最も長い時間がかかるステートメントです。
-   各 SQL ステートメントが実行された回数。実行頻度が最も高いステートメントを識別するのに役立ちます。
-   各 SQL ステートメントをクリックすると、 `EXPLAIN ANALYZE`結果が表示され、実行の詳細が表示されます。

TiDB は、リテラルとバインド変数を`?`に置き換えることで、SQL ステートメントをテンプレートに正規化します。この正規化とソートのプロセスにより、最適化が必要な可能性のある、最もリソースを消費するクエリをすばやく識別できます。

![sql-statements-default](/media/sql-tuning/sql-statements-default.png)

#### スロークエリページ {#slow-queries-page}

[TiDBダッシュボード](/dashboard/dashboard-overview.md)で[**スロークエリ**ページ](/dashboard/dashboard-slow-query.md)に移動して次の項目を見つけます。

-   最も遅い SQL クエリ。
-   TiKV から最も多くのデータを読み取る SQL クエリ。
-   詳細な実行分析を行うには、クエリをクリックして`EXPLAIN ANALYZE`出力します。

**「低速クエリ」**ページには、SQL 実行頻度は表示されません。クエリの実行時間が単一インスタンスの[`tidb_slow_log_threshold`](/tidb-configuration-file.md#tidb_slow_log_threshold)構成項目を超えると、このページにクエリが表示されます。

![slow-query-default](/media/sql-tuning/slow-query-default.png)

### 他のツールを使用してTop SQLを特定する {#use-other-tools-to-identify-top-sql}

TiDB ダッシュボードに加えて、他のツールを使用してリソースを大量に消費する SQL クエリを特定できます。各ツールは独自の洞察を提供し、さまざまな分析シナリオに役立ちます。これらのツールを組み合わせて使用すると、包括的な SQL パフォーマンスの監視と最適化が可能になります。

-   [TiDBダッシュボードのTop SQLページ](/dashboard/top-sql.md)
-   ログ: [スロークエリログ](/identify-slow-queries.md)と[TiDB ログ内の高価なクエリ](/identify-expensive-queries.md)
-   閲覧数: [`cluster_statements_summary`ビュー](/statement-summary-tables.md#the-cluster-tables-for-statement-summary)と[`cluster_processlist`ビュー](/information-schema/information-schema-processlist.md#cluster_processlist)

### 特定されたSQL文に関するデータを収集する {#gather-data-on-identified-sql-statements}

識別された上位の SQL ステートメントについては、 [`PLAN REPLAYER`](/sql-plan-replayer.md)使用して TiDB クラスターから SQL 実行情報を取得して保存できます。このツールは、実行環境を再作成してさらに分析するのに役立ちます。SQL 実行情報をエクスポートするには、次の構文を使用します。

```sql
PLAN REPLAYER DUMP EXPLAIN [ANALYZE] [WITH STATS AS OF TIMESTAMP expression] sql-statement;
```

実行プランと実際のパフォーマンス メトリックの両方が提供されるため、クエリ パフォーマンスに関するより正確な分析情報が得られるため、可能な限り`EXPLAIN ANALYZE`使用してください。

## SQL チューニング ガイド {#sql-tuning-guide}

このガイドでは、TiDB での SQL クエリの最適化に関する初心者向けの実用的なアドバイスを提供します。これらのベスト プラクティスに従うことで、クエリのパフォーマンスを向上させ、SQL チューニングを効率化できます。このガイドでは、次のトピックについて説明します。

-   [クエリ処理を理解する](#understand-query-processing)
    -   [クエリ処理ワークフロー](#query-processing-workflow)
    -   [オプティマイザーの基礎](#optimizer-fundamentals)
    -   [統計管理](#statistics-management)
-   [実行計画を理解する](#understand-execution-plans)
    -   [TiDBが実行計画を構築する方法](#how-tidb-builds-an-execution-plan)
    -   [実行計画を生成して表示する](#generate-and-display-execution-plans)
    -   [実行プランの読み取り: 最初の子を最初に](#read-execution-plans-first-child-first)
    -   [実行計画のボトルネックを特定する](#identify-bottlenecks-in-execution-plans)
-   [TiDBのインデックス戦略](#index-strategy-in-tidb)
    -   [複合指数戦略ガイドライン](#composite-index-strategy-guidelines)
    -   [インデックス作成のコスト](#the-cost-of-indexing)
    -   [カバーインデックスを使用したSQLチューニング](#sql-tuning-with-a-covering-index)
    -   [ソートを含む複合インデックスを使用したSQLチューニング](#sql-tuning-with-a-composite-index-involving-sorting)
    -   [複合インデックスを使用した効率的なフィルタリングとソートのための SQL チューニング]#sql-tuning-with-composite-indexes-for-efficient-filtering-and-sorting
-   [TiFlashを使用する場合](#when-to-use-tiflash)
    -   [分析クエリ](#analytical-query)
    -   [SaaS 任意フィルタリングワークロード](#saas-arbitrary-filtering-workloads)

### クエリ処理を理解する {#understand-query-processing}

このセクションでは、クエリ処理ワークフロー、オプティマイザーの基礎、および統計管理について説明します。

#### クエリ処理ワークフロー {#query-processing-workflow}

クライアントが TiDB に SQL ステートメントを送信すると、ステートメントは TiDBサーバーのプロトコルレイヤーを通過します。このレイヤーはTiDBサーバーとクライアント間の接続を管理し、SQL ステートメントを受信して​​、データをクライアントに返します。

![workflow](/media/sql-tuning/workflow-tiflash.png)

上の図では、プロトコルレイヤーの右側に TiDBサーバーのオプティマイザーがあり、次のように SQL ステートメントを処理します。

1.  SQL ステートメントはプロトコルレイヤーを介して SQL オプティマイザーに到達し、抽象構文ツリー (AST) に解析されます。
2.  TiDB は、それが[ポイントゲット](/explain-indexes.md#point_get-and-batch_point_get)ステートメントであるかどうかを識別します。1 ステートメントには、 `SELECT * FROM t WHERE pk_col = 1`や`SELECT * FROM t WHERE uk_col IN (1,2,3)`の主キーまたは一意のキーを介した単純な 1 つのテーブル検索が含まれます。 `Point Get`ステートメントの場合、TiDB は後続の最適化手順をスキップし、SQL エグゼキュータでの実行に直接進みます。
3.  クエリが`Point Get`でない場合、 AST は論理変換され、TiDB は特定のルールに基づいて SQL を論理的に書き換えます。
4.  論理変換後、TiDB はコストベースの最適化を通じて AST を処理します。
5.  コストベースの最適化では、オプティマイザーは統計を使用して適切な演算子を選択し、物理的な実行プランを生成します。
6.  生成された物理実行プランは、実行のために TiDB ノードの SQL 実行プログラムに送信されます。
7.  従来の単一ノード データベースとは異なり、TiDB は、データを含む TiKV ノードやTiFlashノードに演算子またはコプロセッサをプッシュダウンします。このアプローチでは、データが格納されている実行プランの一部を処理し、分散アーキテクチャを効率的に利用し、リソースを並列で使用して、ネットワーク データ転送を削減します。その後、TiDB ノード エグゼキュータが最終結果を組み立ててクライアントに返します。

#### オプティマイザーの基礎 {#optimizer-fundamentals}

TiDB はコストベース オプティマイザー (CBO) を使用して、SQL ステートメントの最も効率的な実行プランを決定します。オプティマイザーはさまざまな実行戦略を評価し、推定コストが最も低いものを選択します。コストは次のような要因によって異なります。

-   SQL文
-   スキーマ設計
-   統計には以下が含まれます:
    -   表の統計
    -   インデックス統計
    -   カラム統計

これらの入力に基づいて、コスト モデルは、TiDB が SQL ステートメントを実行する方法を詳細に示す実行プランを生成します。これには次の内容が含まれます。

-   アクセス方法
-   結合方法
-   参加順序

オプティマイザの有効性は、受け取る情報の品質によって決まります。最適なパフォーマンスを実現するには、統計が最新であり、インデックスが適切に設計されていることを確認してください。

#### 統計管理 {#statistics-management}

統計はTiDB オプティマイザにとって不可欠です。TiDB は統計をオプティマイザの入力として使用し、SQL 実行プランの各ステップで処理される行数を推定します。

統計は次の 2 つのレベルに分かれています。

-   **テーブル レベルの統計**: テーブル内の行の合計数と、最後の統計収集以降に変更された行数が含まれます。
-   **インデックス/列レベルの統計**: ヒストグラム、Count-Min Sketch、Top-N (最も出現回数の多い値またはインデックス)、さまざまな値の分布と量、NULL 値の数などの詳細情報が含まれます。

統計の正確性と健全性を確認するには、次の SQL ステートメントを使用できます。

-   [`SHOW STATS_META`](/sql-statements/sql-statement-show-stats-meta.md) : テーブル統計に関するメタデータを表示します。

    ```sql
    SHOW STATS_META WHERE table_name='T2'\G;
    ```

        *************************** 1. row ***************************
                  Db_name: test
               Table_name: T2
           Partition_name:
              Update_time: 2023-05-11 02:16:50
             Modify_count: 10000
                Row_count: 20000
        1 row in set (0.03 sec)

-   [`SHOW STATS_HEALTHY`](/sql-statements/sql-statement-show-stats-healthy.md) : テーブル統計のヘルス ステータスを表示します。

    ```sql
    SHOW STATS_HEALTHY WHERE table_name='T2'\G;
    ```

        *************************** 1. row ***************************
               Db_name: test
            Table_name: T2
        Partition_name:
               Healthy: 50
        1 row in set (0.00 sec)

TiDB には、統計を収集するための 2 つの方法 (自動収集と手動収集) が用意されています。ほとんどの場合、自動収集で十分です。TiDB は、特定の条件が満たされると自動収集をトリガーします。一般的なトリガー条件には、次のものがあります。

-   [`tidb_auto_analyze_ratio`](/system-variables.md#tidb_auto_analyze_ratio) : 健康トリガー。
-   [`tidb_auto_analyze_start_time`](/system-variables.md#tidb_auto_analyze_start_time)および[`tidb_auto_analyze_end_time`](/system-variables.md#tidb_auto_analyze_end_time) : 自動統計収集の時間ウィンドウ。

```sql
SHOW VARIABLES LIKE 'tidb\_auto\_analyze%';
```

    +-----------------------------------------+-------------+
    | Variable_name                           | Value       |
    +-----------------------------------------+-------------+
    | tidb_auto_analyze_ratio                 | 0.5         |
    | tidb_auto_analyze_start_time            | 00:00 +0000 |
    | tidb_auto_analyze_end_time              | 23:59 +0000 |
    +-----------------------------------------+-------------+

場合によっては、自動収集ではニーズを満たせないことがあります。デフォルトでは、 `00:00`から`23:59`間に行われるため、分析ジョブはいつでも実行できます。オンライン ビジネスへのパフォーマンスの影響を最小限に抑えるために、統計収集の開始時間と終了時間を特定して設定できます。

`ANALYZE TABLE table_name`ステートメントを使用して手動で統計を収集できます。これにより、サンプル レート、上位 N 値の数などの設定を調整したり、特定の列のみの統計を収集したりできます。

手動収集後、後続の自動収集ジョブは新しい設定を継承することに注意してください。つまり、手動収集中に行われたカスタマイズは、将来の自動分析に適用されます。

テーブル統計のロックは、次のシナリオで役立ちます。

-   表の統計はすでにデータを適切に表しています。
-   テーブルは非常に大きいため、統計の収集には時間がかかります。
-   特定の時間枠内でのみ統計を維持したい。

テーブルの統計をロックするには、 [`LOCK STATS table_name`](/sql-statements/sql-statement-lock-stats.md)ステートメントを使用できます。

詳細については[統計](/statistics.md)参照してください。

### 実行計画を理解する {#understand-execution-plans}

実行プランには、TiDB が SQL クエリを実行するために従う手順の詳細が記載されています。このセクションでは、TiDB が実行プランを構築する方法と、実行プランを生成、表示、解釈する方法について説明します。

#### TiDBが実行計画を構築する方法 {#how-tidb-builds-an-execution-plan}

SQL ステートメントは、TiDB オプティマイザーで主に 3 つの最適化段階を経ます。

1.  [前処理](#1-pre-processing)
2.  [論理変換](#2-logical-transformation)
3.  [コストベースの最適化](#3-cost-based-optimization)

##### 1. 前処理 {#1-pre-processing}

前処理中に、TiDB は SQL 文を[`Point_Get`](/explain-indexes.md#point_get-and-batch_point_get)または[`Batch_Point_Get`](/explain-indexes.md#point_get-and-batch_point_get)を使用して実行できるかどうかを判断します。これらの操作では、主キーまたは一意のキーを使用して、正確なキー検索を通じて TiKV から直接読み取ります。プランが`Point_Get`または`Batch_Point_Get`に該当する場合、直接キー検索が行にアクセスする最も効率的な方法であるため、オプティマイザーは論理変換とコストベースの最適化手順をスキップします。

以下は`Point_Get`クエリの例です。

```sql
EXPLAIN SELECT id, name FROM emp WHERE id = 901;
```

    +-------------+---------+------+---------------+---------------+
    | id          | estRows | task | access object | operator info |
    +-------------+---------+------+---------------+---------------+
    | Point_Get_1 | 1.00    | root | table:emp     | handle:901    |
    +-------------+---------+------+---------------+---------------+

##### 2. 論理変換 {#2-logical-transformation}

論理変換中、TiDB は`SELECT`リスト、 `WHERE`述語、およびその他の条件に基づいて SQL 文を最適化します。クエリに注釈を付けて書き換えるための論理実行プランを生成します。この論理プランは、次の段階であるコストベースの最適化で使用されます。変換では、列のプルーニング、パーティションのプルーニング、結合の並べ替えなどのルールベースの最適化が適用されます。このプロセスはルールベースで自動であるため、通常は手動調整は不要です。

詳細については[SQL 論理最適化](/sql-logical-optimization.md)参照してください。

##### 3. コストベースの最適化 {#3-cost-based-optimization}

TiDB オプティマイザは、統計を使用して、SQL ステートメントの各ステップで処理される行数を推定し、各ステップにコストを割り当てます。コストベースの最適化中、オプティマイザは、インデックス アクセスや結合方法など、考えられるすべてのプランの選択肢を評価し、各プランの合計コストを計算します。次に、オプティマイザは、合計コストが最小の実行プランを選択します。

次の図は、コストベースの最適化中に考慮されるさまざまなデータ アクセス パスと行セット操作を示しています。データ取得パスについては、オプティマイザーはインデックス スキャンとフル テーブル スキャンの間で最も効率的な方法を決定し、行ベースの TiKVstorageからデータを取得するか、列ベースのTiFlashstorageからデータを取得するかを決定します。

オプティマイザは、集計、結合、ソートなど、行セットを操作する操作も評価します。たとえば、集計演算子は`HashAgg`または`StreamAgg`いずれかを使用し、結合メソッドは`HashJoin` 、 `MergeJoin` 、または`IndexJoin`から選択できます。

さらに、物理最適化フェーズには、式と演算子を物理storageエンジンにプッシュダウンすることが含まれます。物理プランは、次のように、基盤となるstorageエンジンに基づいてさまざまなコンポーネントに配布されます。

-   ルート タスクは TiDBサーバー上で実行されます。
-   Cop (コプロセッサー) タスクは TiKV 上で実行されます。
-   MPP タスクはTiFlash上で実行されます。

この分散により、コンポーネント間のコラボレーションが可能になり、クエリ処理が効率化されます。

![cost-based-optimization](/media/sql-tuning/cost-based-optimization.png)

詳細については[SQL 物理最適化](/sql-physical-optimization.md)参照してください。

#### 実行計画を生成して表示する {#generate-and-display-execution-plans}

TiDB ダッシュボードから実行プラン情報にアクセスするだけでなく、 `EXPLAIN`ステートメントを使用して SQL クエリの実行プランを表示できます。3 出力には`EXPLAIN`の列が含まれます。

-   `id` : オペレータ名とステップの一意の識別子。
-   `estRows` : 特定のステップからの推定行数。
-   `task` : オペレータが実行されるレイヤーを示します。たとえば、 `root` TiDBサーバーでの実行を示し、 `cop[tikv]` TiKV での実行を示し、 `mpp[tiflash]` TiFlashでの実行を示します。
-   `access object` : 行ソースが配置されているオブジェクト。
-   `operator info` : ステップ内の演算子に関する追加の詳細。

```sql
EXPLAIN SELECT COUNT(*) FROM trips WHERE start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59';
```

    +--------------------------+-------------+--------------+-------------------+----------------------------------------------------------------------------------------------------+
    | id                       | estRows     | task         | access object     | operator info                                                                                      |
    +--------------------------+-------------+--------------+-------------------+----------------------------------------------------------------------------------------------------+
    | StreamAgg_20             | 1.00        | root         |                   | funcs:count(Column#13)->Column#11                                                                  |
    | └─TableReader_21         | 1.00        | root         |                   | data:StreamAgg_9                                                                                   |
    |   └─StreamAgg_9          | 1.00        | cop[tikv]    |                   | funcs:count(1)->Column#13                                                                          |
    |     └─Selection_19       | 250.00      | cop[tikv]    |                   | ge(trips.start_date, 2017-07-01 00:00:00.000000), le(trips.start_date, 2017-07-01 23:59:59.000000) |
    |       └─TableFullScan_18 | 10000.00    | cop[tikv]    | table:trips       | keep order:false, stats:pseudo                                                                     |
    +--------------------------+-------------+--------------+-------------------+----------------------------------------------------------------------------------------------------+
    5 rows in set (0.00 sec)

`EXPLAIN`とは異なり、 `EXPLAIN ANALYZE`対応する SQL 文を実行し、その実行時情報を記録し、実行プランとともに実行時情報を返します。この実行時情報は、クエリ実行のデバッグに不可欠です。詳細については、 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)参照してください。

`EXPLAIN ANALYZE`出力には以下が含まれます。

-   `actRows` : 演算子によって出力される行数。
-   `execution info` : 演算子の詳細な実行情報。2 `time` 、すべてのサブ演算子の合計実行時間を含む合計`wall time`表します。演算子が親演算子によって何度も呼び出される場合は、時間は累積時間を参照します。
-   `memory` : 演算子によって使用されるメモリ。
-   `disk` : オペレータが使用するディスク容量。

以下は例です。書式設定を改善するために、一部の属性とテーブル列は省略されています。

```sql
EXPLAIN ANALYZE
SELECT SUM(pm.m_count) / COUNT(*) 
FROM (
    SELECT COUNT(m.name) m_count
    FROM universe.moons m
    RIGHT JOIN (
        SELECT p.id, p.name
        FROM universe.planet_categories c
        JOIN universe.planets p
            ON c.id = p.category_id 
            AND c.name = 'Jovian'
    ) pc ON m.planet_id = pc.id
    GROUP BY pc.name
) pm;
```

    +-----------------------------------------+.+---------+-----------+---------------------------+----------------------------------------------------------------+.+-----------+---------+
    | id                                      |.| actRows | task      | access object             | execution info                                                 |.| memory    | disk    |
    +-----------------------------------------+.+---------+-----------+---------------------------+----------------------------------------------------------------+.+-----------+---------+
    | Projection_14                           |.| 1       | root      |                           | time:1.39ms, loops:2, RU:1.561975, Concurrency:OFF             |.| 9.64 KB   | N/A     |
    | └─StreamAgg_16                          |.| 1       | root      |                           | time:1.39ms, loops:2                                           |.| 1.46 KB   | N/A     |
    |   └─Projection_40                       |.| 4       | root      |                           | time:1.38ms, loops:4, Concurrency:OFF                          |.| 8.24 KB   | N/A     |
    |     └─HashAgg_17                        |.| 4       | root      |                           | time:1.36ms, loops:4, partial_worker:{...}, final_worker:{...} |.| 82.1 KB   | N/A     |
    |       └─HashJoin_19                     |.| 25      | root      |                           | time:1.29ms, loops:2, build_hash_table:{...}, probe:{...}      |.| 2.25 KB   | 0 Bytes |
    |         ├─HashJoin_35(Build)            |.| 4       | root      |                           | time:1.08ms, loops:2, build_hash_table:{...}, probe:{...}      |.| 25.7 KB   | 0 Bytes |
    |         │ ├─IndexReader_39(Build)       |.| 1       | root      |                           | time:888.5µs, loops:2, cop_task: {...}                         |.| 286 Bytes | N/A     |
    |         │ │ └─IndexRangeScan_38         |.| 1       | cop[tikv] | table:c, index:name(name) | tikv_task:{time:0s, loops:1}, scan_detail: {...}               |.| N/A       | N/A     |
    |         │ └─TableReader_37(Probe)       |.| 10      | root      |                           | time:543.7µs, loops:2, cop_task: {...}                         |.| 577 Bytes | N/A     |
    |         │   └─TableFullScan_36          |.| 10      | cop[tikv] | table:p                   | tikv_task:{time:0s, loops:1}, scan_detail: {...}               |.| N/A       | N/A     |
    |         └─TableReader_22(Probe)         |.| 28      | root      |                           | time:671.7µs, loops:2, cop_task: {...}                         |.| 876 Bytes | N/A     |
    |           └─TableFullScan_21            |.| 28      | cop[tikv] | table:m                   | tikv_task:{time:0s, loops:1}, scan_detail: {...}               |.| N/A       | N/A     |
    +-----------------------------------------+.+---------+-----------+---------------------------+----------------------------------------------------------------+.+-----------+---------+

#### 実行プランの読み取り: 最初の子を最初に {#read-execution-plans-first-child-first}

遅い SQL クエリを診断するには、実行プランの読み方を理解する必要があります。重要な原則は**、「最初の子が最初 - 再帰降下」**です。プラン内の各演算子は行のセットを生成し、実行順序によってこれらの行がプラン ツリー内をどのように流れるかが決まります。

「最初の子が先」ルールは、演算子が出力を生成する前に、すべての子演算子から行を取得する必要があることを意味します。たとえば、結合演算子は、結合を実行するために両方の子演算子からの行を必要とします。「再帰降下」ルールは、各演算子が子の出力に依存するため、実際のデータは下から上に流れますが、プランを上から下に分析することを意味します。

実行プランを読むときは、次の 2 つの重要な概念を考慮してください。

-   親子相互作用: 親演算子は子演算子を順番に呼び出しますが、複数回循環する場合もあります。たとえば、インデックス検索またはネストされたループ結合では、親は最初の子から行のバッチをフェッチし、次に 2 番目の子から 0 行以上の行を取得します。このプロセスは、最初の子の結果セットが完全に処理されるまで繰り返されます。

-   ブロッキング演算子と非ブロッキング演算子: 演算子はブロッキングまたは非ブロッキングのいずれかになります。
    -   `TopN`や`HashAgg`などのブロッキング演算子は、データを親に渡す前に、結果セット全体を作成する必要があります。
    -   `IndexLookup`や`IndexJoin`などの非ブロッキング演算子は、必要に応じて行を段階的に生成して渡します。

実行プランを読むときは、上から下に向かって読み進めてください。次の例では、プラン ツリーのリーフ ノードは`TableFullScan_18`で、完全なテーブル スキャンを実行します。このスキャンからの行は`Selection_19`演算子によって使用され、 `ge(trips.start_date, 2017-07-01 00:00:00.000000), le(trips.start_date, 2017-07-01 23:59:59.000000)`に基づいてデータがフィルター処理されます。次に、group-by 演算子`StreamAgg_9`最終的な集計`COUNT(*)`実行します。

これら 3 つの演算子 ( `TableFullScan_18` 、 `Selection_19` 、および`StreamAgg_9` ) は TiKV ( `cop[tikv]`としてマーク) にプッシュダウンされ、TiKV での早期フィルタリングと集約が可能になり、TiKV と TiDB 間のデータ転送が削減されます。最後に、 `TableReader_21` `StreamAgg_9`からデータを読み取り、 `StreamAgg_20`最終的な集約`count(*)`実行します。

```sql
EXPLAIN SELECT COUNT(*) FROM trips WHERE start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59';
```

    +--------------------------+-------------+--------------+-------------------+----------------------------------------------------------------------------------------------------+
    | id                       | estRows     | task         | access object     | operator info                                                                                      |
    +--------------------------+-------------+--------------+-------------------+----------------------------------------------------------------------------------------------------+
    | StreamAgg_20             | 1.00        | root         |                   | funcs:count(Column#13)->Column#11                                                                  |
    | └─TableReader_21         | 1.00        | root         |                   | data:StreamAgg_9                                                                                   |
    |   └─StreamAgg_9          | 1.00        | cop[tikv]    |                   | funcs:count(1)->Column#13                                                                          |
    |     └─Selection_19       | 250.00      | cop[tikv]    |                   | ge(trips.start_date, 2017-07-01 00:00:00.000000), le(trips.start_date, 2017-07-01 23:59:59.000000) |
    |       └─TableFullScan_18 | 10000.00    | cop[tikv]    | table:trips       | keep order:false, stats:pseudo                                                                     |
    +--------------------------+-------------+--------------+-------------------+----------------------------------------------------------------------------------------------------+
    5 rows in set (0.00 sec)

次の例では、プラン ツリーの最初のリーフ ノードである`IndexRangeScan_47`調べることから始めます。オプティマイザーは、 `name(name)`インデックスから取得できる`stars`テーブルから`name`と`id`列のみを選択します。その結果、 `stars`のルート リーダーは`IndexReader_48`ではなく`TableReader`なります。

`stars`と`planets`の結合はハッシュ結合です ( `HashJoin_44` )。7 テーブルは`planets`テーブルスキャンを使用してアクセスされます ( `TableFullScan_45` )。結合後、 `TopN_26`と`TopN_19`それぞれ`ORDER BY`句と`LIMIT`句を適用します。最後の演算子`Projection_16`は最後の列`t5.name`を選択します。

```sql
EXPLAIN 
SELECT t5.name 
FROM (
    SELECT p.name, p.gravity, p.distance_from_sun 
    FROM universe.planets p 
    JOIN universe.stars s
        ON s.id = p.sun_id 
        AND s.name = 'Sun'
    ORDER BY p.distance_from_sun ASC 
    LIMIT 5
) t5
ORDER BY t5.gravity DESC 
LIMIT 3;
```

    +-----------------------------------+----------+-----------+---------------------------+
    | id                                | estRows  | task      | access object             |
    +-----------------------------------+----------+-----------+---------------------------+
    | Projection_16                     | 3.00     | root      |                           |
    | └─TopN_19                         | 3.00     | root      |                           |
    |   └─TopN_26                       | 5.00     | root      |                           |
    |     └─HashJoin_44                 | 5.00     | root      |                           |
    |       ├─IndexReader_48(Build)     | 1.00     | root      |                           |
    |       │ └─IndexRangeScan_47       | 1.00     | cop[tikv] | table:s, index:name(name) |
    |       └─TableReader_46(Probe)     | 10.00    | root      |                           |
    |         └─TableFullScan_45        | 10.00    | cop[tikv] | table:p                   |
    +-----------------------------------+----------+-----------+---------------------------+

次の図は、2 番目の実行プランのプラン ツリーを示しています。

![execution-plan-traverse](/media/sql-tuning/execution-plan-traverse.png)

実行プランは、プラン ツリーの後順トラバーサル (左、右、ルート) に対応して、上から下への、最初の子を先頭とするトラバーサルに従います。

この計画は次の順序で読むことができます。

1.  一番上から`Projection_16`から始めます。
2.  その子`TopN_19`に移動します。
3.  `TopN_26`に進みます。
4.  `HashJoin_44`に進みます。
5.  `HashJoin_44`の場合、最初にその左側の (Build) 子を処理します。
    -   `IndexReader_48`
    -   `IndexRangeScan_47`
6.  `HashJoin_44`の場合、その右側の (Probe) 子を処理します。
    -   `TableReader_46`
    -   `TableFullScan_45`

このトラバーサルにより、各演算子の入力が演算子自体の前に処理され、効率的なクエリ実行が可能になります。

#### 実行計画のボトルネックを特定する {#identify-bottlenecks-in-execution-plans}

実行プランを分析する場合、 `actRows` (実際の行数) と`estRows` (推定行数) を比較して、オプティマイザの推定値の精度を評価します。これらの値に大きな差がある場合は、統計が古くなっているか不正確である可能性があり、クエリ プランが最適でない可能性があります。

遅いクエリのボトルネックを特定するには、次の手順を実行します。

1.  実行時間が長い演算子に焦点を当てて、セクション`execution info`上から下まで確認します。
2.  かなりの時間を消費する最初の子演算子の場合:
    -   推定精度を評価するには、 `actRows`と`estRows`を比較します。
    -   実行時間の長さやその他のメトリックなど、 `execution info`の詳細なメトリックを分析します。
    -   潜在的なリソース制約について、 `memory`と`disk`使用状況を確認します。
3.  これらの要因を相関させて、パフォーマンスの問題の根本原因を特定します。たとえば、 `TableFullScan`操作で`actRows`カウントが高く、 `execution info`で実行時間が長い場合は、インデックスの作成を検討します。 `HashJoin`操作でメモリ使用量と実行時間が高い場合は、結合順序を最適化するか、別の結合方法を使用することを検討します。

次の実行プランでは、クエリは 5 分 51 秒間実行された後、キャンセルされます。主な問題は次のとおりです。

1.  重大な過小評価: 最初のリーフノード`IndexReader_76` `index_orders_on_adjustment_id(adjustment_id)`インデックスからデータを読み取ります。実際の行数 ( `actRows` ) は 256,811,189 で、推定された 1 行 ( `estRows` ) よりも大幅に高くなっています。
2.  メモリ オーバーフロー: この過小評価により、ハッシュ結合演算子`HashJoin_69`予想よりもはるかに多くのデータを含むハッシュ テーブルを構築し、過剰なメモリ(22.6 GB) とディスク領域 (7.65 GB) を消費します。
3.  クエリの終了: `HashJoin_69`およびそれより上の演算子の`0`の`actRows`値は、一致する行がないか、リソースの制約によりクエリが終了したことを示します。この場合、ハッシュ結合はメモリを大量に消費し、メモリ制御メカニズムがトリガーされてクエリが終了します。
4.  結合順序が正しくありません: この非効率的な計画の根本的な原因は、 `estRows` `IndexRangeScan_75`に対して大幅に過小評価し、オプティマイザーが誤った結合順序を選択することです。

これらの問題に対処するには、特にテーブル`orders`とインデックス`index_orders_on_adjustment_id`テーブル統計が最新であることを確認します。

    +-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------...----------------------+
    | id                                 | estRows   | estCost      | actRows   | task      | access object                                                                          | execution info ...| memory   | disk     |
    +-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------...----------------------+
    | TopN_19                            | 1.01      | 461374372.63 | 0         | root      |                                                                                        | time:5m51.1s, l...| 0 Bytes  | 0 Bytes  |
    | └─IndexJoin_32                     | 1.01      | 460915067.45 | 0         | root      |                                                                                        | time:5m51.1s, l...| 0 Bytes  | N/A      |
    |   ├─HashJoin_69(Build)             | 1.01      | 460913065.41 | 0         | root      |                                                                                        | time:5m51.1s, l...| 21.6 GB  | 7.65 GB  |
    |   │ ├─IndexReader_76(Build)        | 1.00      | 18.80        | 256805045 | root      |                                                                                        | time:1m4.1s, lo...| 12.4 MB  | N/A      |
    |   │ │ └─IndexRangeScan_75          | 1.00      | 186.74       | 256811189 | cop[tikv] | table:orders, index:index_orders_on_adjustment_id(adjustment_id)                       | tikv_task:{proc...| N/A      | N/A      |
    |   │ └─Projection_74(Probe)         | 30652.93  | 460299612.60 | 1024      | root      |                                                                                        | time:1.08s, loo...| 413.4 KB | N/A      |
    |   │   └─IndexLookUp_73             | 30652.93  | 460287375.95 | 6144      | root      | partition:all                                                                          | time:1.08s, loo...| 107.8 MB | N/A      |
    |   │     ├─IndexRangeScan_70(Build) | 234759.64 | 53362737.50  | 390699    | cop[tikv] | table:rates, index:index_rates_on_label_id(label_id)                                   | time:29.6ms, lo...| N/A      | N/A      |
    |   │     └─Selection_72(Probe)      | 30652.93  | 110373973.91 | 187070    | cop[tikv] |                                                                                        | time:36.8s, loo...| N/A      | N/A      |
    |   │       └─TableRowIDScan_71      | 234759.64 | 86944962.10  | 390699    | cop[tikv] | table:rates                                                                            | tikv_task:{proc...| N/A      | N/A      |
    |   └─TableReader_28(Probe)          | 0.00      | 43.64        | 0         | root      |                                                                                        |                ...| N/A      | N/A      |
    |     └─Selection_27                 | 0.00      | 653.96       | 0         | cop[tikv] |                                                                                        |                ...| N/A      | N/A      |
    |       └─TableRangeScan_26          | 1.01      | 454.36       | 0         | cop[tikv] | table:labels                                                                           |                ...| N/A      | N/A      |
    +-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------...----------------------+

次の実行プランは、テーブル`orders`の誤った推定を修正した後の期待される結果を示しています。クエリの実行時間は 1.96 秒になりました。これは、以前の 5 分 51 秒から大幅に改善されています。

-   正確な推定: `estRows`値が`actRows`ほぼ一致するようになりました。これは、統計が更新され、より正確になったことを示しています。
-   効率的な結合順序: クエリは`labels`テーブルの`TableReader`から始まり、続いて`rates`テーブルの`IndexJoin` 、さらに`orders`テーブルの`IndexJoin`続きます。この結合順序は、実際のデータ分散でより効率的に機能します。
-   メモリオーバーフローなし: 前のプランとは異なり、この実行ではメモリやディスクの使用量過多の兆候は見られず、クエリが予想されるリソース制限内で実行されていることを示しています。

この最適化されたプランは、クエリ パフォーマンスにおける正確な統計と適切な結合順序の重要性を示しています。実行時間の短縮 (351 秒から 1.96 秒) は、推定エラーへの対処の影響を示しています。

    +---------------------------------------+----------+---------+-----------+----------------------------------------------------------------------------------------+---------------...+----------+------+
    | id                                    | estRows  | actRows | task      | access object                                                                          | execution info...| memory   | disk |
    +---------------------------------------+----------+---------+-----------+----------------------------------------------------------------------------------------+---------------...+----------+------+
    | Limit_24                              | 1000.00  | 1000    | root      |                                                                                        | time:1.96s, lo...| N/A      | N/A  |
    | └─IndexJoin_88                        | 1000.00  | 1000    | root      |                                                                                        | time:1.96s, lo...| 1.32 MB  | N/A  |
    |   ├─IndexJoin_99(Build)               | 1000.00  | 2458    | root      |                                                                                        | time:1.96s, lo...| 77.7 MB  | N/A  |
    |   │ ├─TableReader_109(Build)          | 6505.62  | 158728  | root      |                                                                                        | time:1.26s, lo...| 297.0 MB | N/A  |
    |   │ │ └─Selection_108                 | 6505.62  | 171583  | cop[tikv] |                                                                                        | tikv_task:{pro...| N/A      | N/A  |
    |   │ │   └─TableRangeScan_107          | 80396.43 | 179616  | cop[tikv] | table:labels                                                                           | tikv_task:{pro...| N/A      | N/A  |
    |   │ └─Projection_98(Probe)            | 1000.00  | 2458    | root      |                                                                                        | time:2.13s, lo...| 59.2 KB  | N/A  |
    |   │   └─IndexLookUp_97                | 1000.00  | 2458    | root      | partition:all                                                                          | time:2.13s, lo...| 1.20 MB  | N/A  |
    |   │     ├─Selection_95(Build)         | 6517.14  | 6481    | cop[tikv] |                                                                                        | time:798.6ms, ...| N/A      | N/A  |
    |   │     │ └─IndexRangeScan_93         | 6517.14  | 6481    | cop[tikv] | table:rates, index:index_rates_on_label_id(label_id)                                   | tikv_task:{pro...| N/A      | N/A  |
    |   │     └─Selection_96(Probe)         | 1000.00  | 2458    | cop[tikv] |                                                                                        | time:444.4ms, ...| N/A      | N/A  |
    |   │       └─TableRowIDScan_94         | 6517.14  | 6481    | cop[tikv] | table:rates                                                                            | tikv_task:{pro...| N/A      | N/A  |
    |   └─TableReader_84(Probe)             | 984.56   | 1998    | root      |                                                                                        | time:207.6ms, ...| N/A      | N/A  |
    |     └─Selection_83                    | 984.56   | 1998    | cop[tikv] |                                                                                        | tikv_task:{pro...| N/A      | N/A  |
    |       └─TableRangeScan_82             | 1000.00  | 2048    | cop[tikv] | table:orders                                                                           | tikv_task:{pro...| N/A      | N/A  |
    +---------------------------------------+----------+---------+-----------+----------------------------------------------------------------------------------------+---------------...+----------+------+

詳細については[TiDB クエリ実行プランの概要](/explain-overview.md)および[`EXPLAIN`ウォークスルー](/explain-walkthrough.md)参照してください。

### TiDBのインデックス戦略 {#index-strategy-in-tidb}

TiDB は、SQLレイヤー(TiDB サーバー) とstorageレイヤー(TiKV) を分離する分散 SQL データベースです。従来のデータベースとは異なり、TiDB はバッファー プールを使用してコンピューティング ノードにデータをキャッシュしません。そのため、SQL クエリのパフォーマンスとクラスター全体のパフォーマンスは、処理する必要のあるキー値 (KV) RPC 要求の数に依存します。一般的な KV RPC 要求には、 `Point_Get` 、 `Batch_Point_Get` 、およびコプロセッサー があります。

TiDB のパフォーマンスを最適化するには、インデックスを効果的に使用することが不可欠です。インデックスを使用すると、KV RPC 要求の数を大幅に削減できます。KV RPC 要求が減ると、クエリのパフォーマンスとシステム効率が向上します。次に、インデックスの最適化に役立ついくつかの重要な戦略を示します。

-   テーブル全体のスキャンを避けてください。
-   ソート操作を避けてください。
-   行の検索を減らすには、カバーリング インデックスを使用するか、不要な列を除外します。

このセクションでは、一般的なインデックス作成戦略とインデックス作成コストについて説明します。また、SQL チューニングのための複合インデックスとカバーリング インデックスに重点を置き、TiDB での効果的なインデックス作成の 3 つの実用的な例を示します。

#### 複合指数戦略ガイドライン {#composite-index-strategy-guidelines}

効率的な複合インデックスを作成するには、列を戦略的に順序付けます。列の順序は、インデックスがデータをフィルタリングおよび並べ替える効率に直接影響します。

複合インデックスの推奨列順序ガイドラインに従ってください。

1.  直接アクセスするには、インデックス プレフィックス列から始めます。
    -   同等の条件を持つ列
    -   条件が`IS NULL`ある列

2.  次に並べ替え用の列を追加します。
    -   インデックスでソート操作を処理できるようにする
    -   ソートを有効にし、TiKV へのプッシュダウンを制限する
    -   ソート順を維持する

3.  行の検索を減らすために追加のフィルタリング列を含めます。
    -   日時列の時間範囲条件
    -   `!=`などの他`IS NOT NULL` `<>`でない条件

4.  カバー インデックスを最大限に活用するには、 `SELECT`リストから列を追加するか、集計に使用します。

#### インデックス作成のコスト {#the-cost-of-indexing}

インデックスはクエリのパフォーマンスを向上させることができますが、考慮すべきコストも発生します。

-   書き込み時のパフォーマンスへの影響:
    -   非クラスター化インデックスを使用すると、シングルフェーズコミットの最適化の可能性が低くなります。
    -   追加のインデックスごとに書き込み操作が遅くなります ( `INSERT` 、 `UPDATE` 、 `DELETE`など)。
    -   データが変更された場合は、影響を受けるすべてのインデックスを更新する必要があります。
    -   テーブルに含まれるインデックスの数が多いほど、書き込みパフォーマンスへの影響が大きくなります。

-   リソース消費:
    -   インデックスには追加のディスク領域が必要です。
    -   頻繁にアクセスされるインデックスをキャッシュするには、より多くのメモリが必要です。
    -   バックアップおよびリカバリ操作に時間がかかります。

-   ホットスポットリスクを記述する:
    -   セカンダリ インデックスは書き込みホットスポットを作成する可能性があります。たとえば、単調に増加する datetime インデックスは、テーブル書き込み時にホットスポットを引き起こします。
    -   ホットスポットはパフォーマンスの大幅な低下につながる可能性があります。

以下にいくつかのベストプラクティスを示します。

-   パフォーマンス上の明らかな利点がある場合にのみインデックスを作成します。
-   [`TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md)使用してインデックスの使用状況統計を定期的に確認します。
-   インデックスを設計するときは、ワークロードの書き込み/読み取り比率を考慮してください。

#### カバーインデックスを使用したSQLチューニング {#sql-tuning-with-a-covering-index}

カバーリング インデックスには、 `WHERE`と`SELECT`句で参照されるすべての列が含まれます。カバーリング インデックスを使用すると、追加のインデックス検索が不要になり、クエリのパフォーマンスが大幅に向上します。

次のクエリでは、2,597,411 行のインデックス検索が必要で、実行に 46.4 秒かかります。TiDB は、 `logs_idx`インデックス範囲スキャンに 67 の cop タスク ( `IndexRangeScan_11` ) をディスパッチし、テーブル アクセスに 301 の cop タスク ( `TableRowIDScan_12` ) をディスパッチします。

```sql
SELECT
  SUM(`logs`.`amount`)
FROM
  `logs`
WHERE
  `logs`.`user_id` = 1111
  AND `logs`.`snapshot_id` IS NULL
  AND `logs`.`status` IN ('complete', 'failure')
  AND `logs`.`source_type` != 'online'
  AND (
    `logs`.`source_type` IN ('user', 'payment')
    OR `logs`.`source_type` IN (
      'bank_account',
    )
    AND `logs`.`target_type` IN ('bank_account')
  );
```

元の実行計画は次のとおりです。

    +-------------------------------+------------+---------+-----------+--------------------------------------------------------------------------+------------------------------------------------------------+
    | id                            | estRows    | actRows | task      | access object                                                            | execution info                                             | 
    +-------------------------------+------------+---------+-----------+--------------------------------------------------------------------------+------------------------------------------------------------+
    | HashAgg_18                   | 1.00       | 2571625.22 | 1       | root      |                                                              | time:46.4s, loops:2, partial_worker:{wall_time:46.37,   ...|
    | └─IndexLookUp_19             | 1.00       | 2570096.68 | 301     | root      |                                                              | time:46.4s, loops:2, index_task: {total_time: 45.8s,    ...|
    |   ├─IndexRangeScan_11(Build) | 1309.50    | 317033.98  | 2597411 | cop[tikv] | table:logs, index:logs_idx(snapshot_id, user_id, status)     | time:228ms, loops:2547, cop_task: {num: 67, max: 2.17s, ...|
    |   └─HashAgg_7(Probe)         | 1.00       | 588434.48  | 301     | cop[tikv] |                                                              | time:3m46.7s, loops:260, cop_task: {num: 301,           ...|
    |     └─Selection_13           | 1271.37    | 561549.27  | 2566562 | cop[tikv] |                                                              | tikv_task:{proc max:10s, min:0s, avg: 915.3ms,          ...|
    |       └─TableRowIDScan_12    | 1309.50    | 430861.31  | 2597411 | cop[tikv] | table:logs                                                   | tikv_task:{proc max:10s, min:0s, avg: 908.7ms,          ...|
    +-------------------------------+------------+---------+-----------+--------------------------------------------------------------------------+------------------------------------------------------------+

クエリのパフォーマンスを向上させるには、 `source_type` 、 `target_type` 、および`amount`列を含むカバー インデックスを作成します。この最適化により、追加のテーブル検索が不要になり、実行時間が 90 ミリ秒に短縮され、TiDB はデータ スキャンのために TiKV に cop タスクを 1 つだけ送信する必要があります。

インデックスを作成したら、 `ANALYZE TABLE`ステートメントを実行して統計を収集します。TiDB では、インデックスを作成しても統計は自動的に更新されないため、テーブルを分析すると、オプティマイザーが新しいインデックスを選択するようになります。

```sql
CREATE INDEX logs_covered ON logs(snapshot_id, user_id, status, source_type, target_type, amount); 
ANALYZE TABLE logs INDEX logs_covered;
```

新しい実行プランは次のとおりです。

    +-------------------------------+------------+---------+-----------+---------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------+
    | id                            | estRows    | actRows | task      | access object                                                                                                                   | execution info                              |
    +-------------------------------+------------+---------+-----------+---------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------+
    | HashAgg_13                    | 1.00       | 1       | root      |                                                                                                                                 | time:90ms, loops:2, RU:158.885311,       ...|
    | └─IndexReader_14              | 1.00       | 1       | root      |                                                                                                                                 | time:89.8ms, loops:2, cop_task: {num: 1, ...|
    |   └─HashAgg_6                 | 1.00       | 1       | cop[tikv] |                                                                                                                                 | tikv_task:{time:88ms, loops:52},         ...|
    |     └─Selection_12            | 5245632.33 | 52863   | cop[tikv] |                                                                                                                                 | tikv_task:{time:80ms, loops:52}          ...|
    |       └─IndexRangeScan_11     | 5245632.33 | 52863   | cop[tikv] | table:logs, index:logs_covered(snapshot_id, user_id, status, source_type, target_type, amount)                                  | tikv_task:{time:60ms, loops:52}          ...|
    +-------------------------------+------------+---------+-----------+---------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------+

#### ソートを含む複合インデックスを使用したSQLチューニング {#sql-tuning-with-a-composite-index-involving-sorting}

フィルタリング列と並べ替え列の両方を含む複合インデックスを作成することで、 `ORDER BY`句のクエリを最適化できます。このアプローチにより、TiDB は必要な順序を維持しながら効率的にデータにアクセスできるようになります。

たとえば、特定の条件に基づいて`test`からデータを取得する次のクエリを考えます。

```sql
EXPLAIN ANALYZE SELECT  
test.*
FROM
  test
WHERE
  test.snapshot_id = 459840
  AND test.id > 998464
ORDER BY
  test.id ASC
LIMIT
  1000
```

実行プランには 170 ミリ秒の期間が示されています。TiDB は`test_index`使用して、フィルター`snapshot_id = 459840`で`IndexRangeScan_20`実行します。次に、テーブルからすべての列を取得し、 `IndexLookUp_23`後に 5,715 行を TiDB に返します。TiDB はこれらの行を並べ替えて 1,000 行を返します。

`id`列目は主キーなので、 `test_idx`インデックスに暗黙的に含まれています。ただし、 `test_idx`はインデックス プレフィックス列`snapshot_id`の後に 2 つの追加列 ( `user_id`と`status` ) が含まれているため、 `IndexRangeScan_20`順序が保証されません。その結果、 `id`の順序は保持されません。

当初の計画は次のとおりです。

    +------------------------------+---------+---------+-----------+----------------------------------------------------------+-----------------------------------------------+--------------------------------------------+
    | id                           | estRows | actRows | task      | access object                                            | execution info                                | operator info                              | 
    +------------------------------+---------+---------+-----------+----------------------------------------------------------+-----------------------------------------------+--------------------------------------------+
    | id                           | estRows | actRows | task      | access object                                            | execution info                             ...| test.id, offset:0, count:1000              | 
    | TopN_10                      | 19.98   | 1000    | root      |                                                          | time:170.6ms, loops:2                      ...|                                            |
    | └─IndexLookUp_23             | 19.98   | 5715    | root      |                                                          | time:166.6ms, loops:7                      ...|                                            | 
    |   ├─Selection_22(Build)      | 19.98   | 5715    | cop[tikv] |                                                          | time:18.6ms, loops:9, cop_task: {num: 3,   ...| gt(test.id, 998464)                        | 
    |   │ └─IndexRangeScan_20      | 433.47  | 7715    | cop[tikv] | table:test, index:test_idx(snapshot_id, user_id, status) | tikv_task:{proc max:4ms, min:4ms, avg: 4ms ...| range:[459840,459840], keep order:false    |
    |   └─TableRowIDScan_21(Probe) | 19.98   | 5715    | cop[tikv] | table:test                                               | time:301.6ms, loops:10, cop_task: {num: 3, ...| keep order:false                           | 
    +------------------------------+---------+---------+-----------+----------------------------------------------------------+-----------------------------------------------+--------------------------------------------+

クエリを最適化するには、 `(snapshot_id)`に新しいインデックスを作成します。これにより、 `id`各`snapshot_id`グループ内でソートされるようになります。このインデックスを使用すると、実行時間は 96 ミリ秒に短縮されます。 `keep order`プロパティは`IndexRangeScan_33`の`true`になり、 `TopN` `Limit`に置き換えられます。その結果、 `IndexLookUp_35` 1,000 行のみを TiDB に返すため、追加のソート操作は不要になります。

以下は、最適化されたインデックスを使用したクエリ ステートメントです。

```sql
CREATE INDEX test_new ON test(snapshot_id);
ANALYZE TABLE test INDEX test_new;
```

新しい計画は次のとおりです。

    +----------------------------------+---------+---------+-----------+----------------------------------------------+----------------------------------------------+----------------------------------------------------+
    | id                               | estRows | actRows | task      | access object                                | execution info                               | operator info                                      |
    +----------------------------------+---------+---------+-----------+----------------------------------------------+----------------------------------------------+----------------------------------------------------+
    | Limit_14                         | 17.59   | 1000    | root      |                                              | time:96.1ms, loops:2, RU:92.300155           | offset:0, count:1000                               |
    | └─IndexLookUp_35                 | 17.59   | 1000    | root      |                                              | time:96.1ms, loops:1, index_task:         ...|                                                    |
    |   ├─IndexRangeScan_33(Build)     | 17.59   | 5715    | cop[tikv] | table:test, index:test_new(snapshot_id)      | time:7.25ms, loops:8, cop_task: {num: 3,  ...| range:(459840 998464,459840 +inf], keep order:true |
    |   └─TableRowIDScan_34(Probe)     | 17.59   | 5715    | cop[tikv] | table:test                                   | time:232.9ms, loops:9, cop_task: {num: 3, ...| keep order:false                                   |
    +----------------------------------+---------+---------+-----------+----------------------------------------------+----------------------------------------------+----------------------------------------------------+

#### 効率的なフィルタリングとソートのための複合インデックスを使用したSQLチューニング {#sql-tuning-with-composite-indexes-for-efficient-filtering-and-sorting}

次のクエリの実行には 11 分 9 秒かかりますが、これは 101 行のみを返すクエリとしては長すぎます。パフォーマンスの低下は、いくつかの要因によって発生します。

-   非効率的なインデックスの使用: オプティマイザーは`created_at`のインデックスを選択し、結果として 25,147,450 行がスキャンされます。
-   大規模な中間結果セット: 日付範囲フィルターを適用した後も、12,082,311 行の処理が必要です。
-   遅延フィルタリング: テーブルにアクセスした後、最も選択的な述語`(mode, user_id, and label_id)`適用され、結果として 16,604 行が生成されます。
-   ソートのオーバーヘッド: 16,604 行の最終ソート操作により、追加の処理時間が発生します。

クエリステートメントは次のとおりです。

```sql
SELECT `orders`.*
FROM `orders`
WHERE 
    `orders`.`mode` = 'production'
    AND `orders`.`user_id` = 11111
    AND orders.label_id IS NOT NULL
    AND orders.created_at >= '2024-04-07 18:07:52'
    AND orders.created_at <= '2024-05-11 18:07:52'
    AND orders.id >= 1000000000
    AND orders.id < 1500000000
ORDER BY orders.id DESC 
LIMIT 101;
```

`orders`の既存のインデックスは次のとおりです。

```sql
PRIMARY KEY (`id`),
UNIQUE KEY `index_orders_on_adjustment_id` (`adjustment_id`),
KEY `index_orders_on_user_id` (`user_id`),
KEY `index_orders_on_label_id` (`label_id`),
KEY `index_orders_on_created_at` (`created_at`)
```

元の実行計画は次のとおりです。

    +--------------------------------+-----------+---------+-----------+--------------------------------------------------------------------------------+-----------------------------------------------------+----------------------------------------------------------------------------------------+----------+------+
    | id                             | estRows   | actRows | task      | access object                                                                  | execution info                                      | operator info                                                                          | memory   | disk |
    +--------------------------------+-----------+---------+-----------+--------------------------------------------------------------------------------+-----------------------------------------------------+----------------------------------------------------------------------------------------+----------+------+
    | TopN_10                        | 101.00    | 101     | root      |                                                                                | time:11m9.8s, loops:2                               | orders.id:desc, offset:0, count:101                                                    | 271 KB   | N/A  |
    | └─IndexLookUp_39               | 173.83    | 16604   | root      |                                                                                | time:11m9.8s, loops:19, index_task: {total_time:...}|                                                                                        | 20.4 MB  | N/A  |
    |   ├─Selection_37(Build)        | 8296.70   | 12082311| cop[tikv] |                                                                                | time:26.4ms, loops:11834, cop_task: {num: 294, m...}| ge(orders.id, 1000000000), lt(orders.id, 1500000000)                                   | N/A      | N/A  |
    |   │ └─IndexRangeScan_35        | 6934161.90| 25147450| cop[tikv] | table:orders, index:index_orders_on_created_at(created_at)                     | tikv_task:{proc max:2.15s, min:0s, avg: 58.9ms, ...}| range:[2024-04-07 18:07:52,2024-05-11 18:07:52), keep order:false                      | N/A      | N/A  |
    |   └─Selection_38(Probe)        | 173.83    | 16604   | cop[tikv] |                                                                                | time:54m46.2s, loops:651, cop_task: {num: 1076, ...}| eq(orders.mode, "production"), eq(orders.user_id, 11111), not(isnull(orders.label_id)) | N/A      | N/A  |
    |     └─TableRowIDScan_36        | 8296.70   | 12082311| cop[tikv] | table:orders                                                                   | tikv_task:{proc max:44.8s, min:0s, avg: 3.33s, p...}| keep order:false                                                                       | N/A      | N/A  |
    +--------------------------------+-----------+---------+-----------+--------------------------------------------------------------------------------+-----------------------------------------------------+----------------------------------------------------------------------------------------+----------+------+

`orders(user_id, mode, id, created_at, label_id)`に複合インデックス`idx_composite`を作成すると、クエリのパフォーマンスが大幅に向上します。実行時間は 11 分 9 秒からわずか 5.3 ミリ秒に短縮され、クエリは 126,000 倍以上高速化します。この大幅な改善は、次の理由によります。

-   効率的なインデックスの使用: 新しいインデックスにより、最も選択的な述語である`user_id` 、 `mode` 、 `id`インデックス範囲スキャンが可能になります。これにより、スキャンされる行数が数百万行からわずか 224 行に削減されます。
-   インデックスのみのソート: 実行プランの`keep order:true` 、ソートがインデックス構造を使用して実行されることを示し、個別のソート操作は不要になります。
-   早期フィルタリング: 最も選択的な述語が最初に適用され、さらにフィルタリングされる前に結果セットが 224 行に削減されます。
-   制限プッシュダウン: `LIMIT`句がインデックス スキャンにプッシュダウンされ、101 行が見つかった時点でスキャンを早期に終了できるようになります。

このケースは、適切に設計されたインデックスがクエリのパフォーマンスに大きく影響することを示しています。インデックス構造をクエリの述語、並べ替え順序、および必要な列に合わせることで、クエリのパフォーマンスが 5 桁以上向上します。

```sql
CREATE INDEX idx_composite ON orders(user_id, mode, id, created_at, label_id);
ANALYZE TABLE orders index idx_composite;
```

新しい実行プランは次のとおりです。

    +--------------------------------+-----------+---------+-----------+--------------------------------------------------------------------------------+-----------------------------------------------------+----------------------------------------------------------------------------------------------------------------------+----------+------+
    | id                             | estRows   | actRows | task      | access object                                                                  | execution info                                      | operator info                                                                                                        | memory   | disk |
    +--------------------------------+-----------+---------+-----------+--------------------------------------------------------------------------------+-----------------------------------------------------+----------------------------------------------------------------------------------------------------------------------+----------+------+
    | IndexLookUp_32                 | 101.00    | 101     | root      |                                                                                | time:5.3ms, loops:2, RU:3.435006, index_task: {t...}| limit embedded(offset:0, count:101)                                                                                  | 128.5 KB | N/A  |
    | ├─Limit_31(Build)              | 101.00    | 101     | cop[tikv] |                                                                                | time:1.35ms, loops:1, cop_task: {num: 1, max: 1....}| offset:0, count:101                                                                                                  | N/A      | N/A  |
    | │ └─Selection_30               | 535.77    | 224     | cop[tikv] |                                                                                | tikv_task:{time:0s, loops:3}                        | ge(orders.created_at, 2024-04-07 18:07:52), le(orders.created_at, 2024-05-11 18:07:52), not(isnull(orders.label_id)) | N/A      | N/A  |
    | │   └─IndexRangeScan_28        | 503893.42 | 224     | cop[tikv] | table:orders, index:idx_composite(user_id, mode, id, created_at, label_id)     | tikv_task:{time:0s, loops:3}                        | range:[11111 "production" 1000000000,11111 "production" 1500000000), keep order:true, desc                           | N/A      | N/A  |
    | └─TableRowIDScan_29(Probe)     | 101.00    | 101     | cop[tikv] | table:orders                                                                   | time:2.9ms, loops:2, cop_task: {num: 3, max: 2.7...}| keep order:false                                                                                                     | N/A      | N/A  |
    +--------------------------------+-----------+---------+-----------+--------------------------------------------------------------------------------+-----------------------------------------------------+----------------------------------------------------------------------------------------------------------------------+----------+------+

### TiFlashを使用する場合 {#when-to-use-tiflash}

このセクションでは、TiDB でTiFlash を使用するタイミングについて説明します。TiFlashは、複雑な計算、集計、大規模なデータセットのスキャンを伴う分析クエリ向けに最適化されています。列指向のstorage形式と MPP モードにより、これらのシナリオでのパフォーマンスが大幅に向上します。

TiFlash は次のシナリオで使用します。

-   大規模データ分析: TiFlash は、広範なデータ スキャンを必要とする OLAP ワークロードに対してより高速なパフォーマンスを提供します。列指向storageと MPP 実行モードにより、TiKV と比較してクエリ効率が最適化されます。
-   複雑なスキャン、集計、結合: TiFlash は、必要な列のみを読み取ることで、集計や結合が重いクエリをより効率的に処理します。
-   混合ワークロード: トランザクション (OLTP) ワークロードと分析 (OLAP) ワークロードの両方が同時に実行されるハイブリッド環境では、 TiFlash はトランザクション クエリに対する TiKV のパフォーマンスに影響を与えることなく分析クエリを処理します。
-   任意のフィルタリング要件を持つ SaaS アプリケーション: クエリには、多くの場合、多数の列にわたるフィルタリングが含まれます。すべての列にインデックスを付けるというのは、特にクエリにテナント ID が主キーの一部として含まれている場合、現実的ではありません。TiFlashは、主キーによってデータを並べ替えてクラスター化するため、このようなワークロードに適しています。1 [遅い実現](/tiflash/tiflash-late-materialization.md)により、 TiFlash は効率的なテーブル範囲スキャンを可能にし、複数のインデックスを維持するオーバーヘッドなしでクエリのパフォーマンスを向上させます。

TiFlash を戦略的に使用すると、クエリ パフォーマンスが向上し、データ集約型の分析クエリに対する TiDB のリソース使用が最適化されます。次のセクションでは、 TiFlashの使用例を示します。

#### 分析クエリ {#analytical-query}

このセクションでは、TiKV およびTiFlashstorageエンジンでの TPC-H クエリ 14 の実行パフォーマンスを比較します。

TPC-H クエリ 14 では、テーブル`order_line`と`item`を結合します。クエリは TiKV では**21.1 秒**かかりますが、 TiFlash MPP モードを使用すると**1.41 秒**しかかからず、15 倍高速になります。

-   TiKVプラン: TiDBは`lineitem`テーブルから3,864,397行、 `part`テーブルから1000万行を取得します。ハッシュ結合操作( `HashJoin_21` )とそれに続く投影( `Projection_38` )および集計( `HashAgg_9` )操作はTiDBで実行されます。
-   TiFlashプラン: オプティマイザーは、 `order_line`と`item`テーブルの両方のTiFlashレプリカを検出します。コスト見積もりに基づいて、TiDB は MPP モードを自動的に選択し、クエリ全体をTiFlash列指向storageエンジン内で実行します。これにはテーブル スキャン、ハッシュ結合、列投影、集計が含まれ、TiKV プランと比較してパフォーマンスが大幅に向上します。

クエリは次のとおりです。

```sql
select 100.00 * sum(case when i_data like 'PR%' then ol_amount else 0 end) / (1+sum(ol_amount)) as promo_revenue
from order_line, item
where ol_i_id = i_id and ol_delivery_d >= '2007-01-02 00:00:00.000000' and ol_delivery_d < '2030-01-02 00:00:00.000000';
```

TiKV での実行プランは次のとおりです。

    +-------------------------------+--------------+-----------+-----------+----------------+----------------------------------------------+
    | ID                            | ESTROWS      | ACTROWS   | TASK      | ACCESS OBJECT  | EXECUTION INFO                               |
    +-------------------------------+--------------+-----------+-----------+----------------+----------------------------------------------+
    | Projection_8                  | 1.00         | 1         | root      |                | time:21.1s, loops:2, RU:1023225.707561, ...  |
    | └─HashAgg_9                   | 1.00         | 1         | root      |                | time:21.1s, loops:2, partial_worker:{ ...    |
    |   └─Projection_38             | 3839984.46   | 3864397   | root      |                | time:21.1s, loops:3776, Concurrency:5        |
    |     └─HashJoin_21             | 3839984.46   | 3864397   | root      |                | time:21.1s, loops:3776, build_hash_table:... |
    |       ├─TableReader_24(Build) | 3826762.62   | 3864397   | root      |                | time:18.4s, loops:3764, cop_task: ...        |
    |       │ └─Selection_23        | 3826762.62   | 3864397   | cop[tikv] |                | tikv_task:{proc max:717ms, min:265ms, ...    |
    |       │   └─TableFullScan_22  | 300005811.00 | 300005811 | cop[tikv] | table:lineitem | tikv_task:{proc max:685ms, min:252ms, ...    |
    |       └─TableReader_26(Probe) | 10000000.00  | 10000000  | root      |                | time:1.29s, loops:9780, cop_task: ...        |
    |         └─TableFullScan_25    | 10000000.00  | 10000000  | cop[tikv] | table:part     | tikv_task:{proc max:922ms, min:468ms, ...    |
    +-------------------------------+--------------+-----------+-----------+----------------+----------------------------------------------+

TiFlashでの実行プランは次のとおりです。

    +--------------------------------------------+-------------+----------+--------------+----------------+--------------------------------------+
    | ID                                         | ESTROWS     | ACTROWS  | TASK         | ACCESS OBJECT  | EXECUTION INFO                       |
    +--------------------------------------------+-------------+----------+--------------+----------------+--------------------------------------+
    | Projection_8                               | 1.00        | 1        | root         |                | time:1.41s, loops:2, RU:45879.127909 |
    | └─HashAgg_52                               | 1.00        | 1        | root         |                | time:1.41s, loops:2, ...             |
    |   └─TableReader_54                         | 1.00        | 1        | root         |                | time:1.41s, loops:2, ...             |
    |     └─ExchangeSender_53                    | 1.00        | 1        | mpp[tiflash] |                | tiflash_task:{time:1.41s, ...        |
    |       └─HashAgg_13                         | 1.00        | 1        | mpp[tiflash] |                | tiflash_task:{time:1.41s, ...        |
    |         └─Projection_74                    | 3813443.11  | 3864397  | mpp[tiflash] |                | tiflash_task:{time:1.4s, ...         |
    |           └─Projection_51                  | 3813443.11  | 3864397  | mpp[tiflash] |                | tiflash_task:{time:1.39s, ...        |
    |             └─HashJoin_50                  | 3813443.11  | 3864397  | mpp[tiflash] |                | tiflash_task:{time:1.39s, ...        |
    |               ├─ExchangeReceiver_31(Build) | 3800312.67  | 3864397  | mpp[tiflash] |                | tiflash_task:{time:1.05s, ...        |
    |               │ └─ExchangeSender_30        | 3800312.67  | 3864397  | mpp[tiflash] |                | tiflash_task:{time:1.2s, ...         |
    |               │   └─TableFullScan_28       | 3800312.67  | 3864397  | mpp[tiflash] | table:lineitem | tiflash_task:{time:1.15s, ...        |
    |               └─ExchangeReceiver_34(Probe) | 10000000.00 | 10000000 | mpp[tiflash] |                | tiflash_task:{time:1.24s, ...        |
    |                 └─ExchangeSender_33        | 10000000.00 | 10000000 | mpp[tiflash] |                | tiflash_task:{time:1.4s, ...         |
    |                   └─TableFullScan_32       | 10000000.00 | 10000000 | mpp[tiflash] | table:part     | tiflash_task:{time:59.2ms, ...       |
    +--------------------------------------------+-------------+----------+--------------+----------------+--------------------------------------+

#### SaaS 任意フィルタリングワークロード {#saas-arbitrary-filtering-workloads}

SaaS アプリケーションでは、テーブルでテナント ID を含む複合主キーが使用されることがよくあります。次の例は、これらのシナリオでTiFlash がクエリ パフォーマンスを大幅に向上させる方法を示しています。

##### ケーススタディ: マルチテナント データ アクセス {#case-study-multi-tenant-data-access}

複合主キーを持つテーブルを考えてみましょう: `(tenantId, objectTypeId, objectId)` 。このテーブルの典型的なクエリ パターンは次のとおりです。

-   数百または数千の列にランダム フィルターを適用しながら、特定のテナントおよびオブジェクト タイプの最初の N レコードを取得します。これにより、すべての可能なフィルターの組み合わせに対してインデックスを作成することは非現実的になります。クエリには、フィルター処理後の並べ替え操作も含まれる場合があります。
-   フィルター条件に一致するレコードの合計数を計算します。

##### パフォーマンス比較 {#performance-comparison}

異なるstorageエンジンで同じクエリを実行すると、パフォーマンスに大きな違いが見られます。

-   TiKV プラン: TiKV でのクエリには 2 分 38.6 秒かかります。1 `TableRangeScan`データが 5,121 のリージョンに分散されているため、5,121 の cop タスクを送信します。
-   TiFlashプラン: 同じクエリはTiFlash MPP エンジンではわずか 3.44 秒で実行され、約 46 倍高速になります。TiFlashは主キーでソートされたデータを保存するため、主キーのプレフィックスでフィルタリングされたクエリでは、完全なテーブル スキャンではなく`TableRangeScan`スキャンを使用します。TiFlashTiFlash、TiKV の 5,121 タスクと比較して、2 つの MPP タスクのみが必要です。

クエリステートメントは次のとおりです。

```sql
WITH `results` AS (
  SELECT field1, field2, field3, field4
  FROM usertable
  where tenantId = 1234 and objectTypeId = 6789
),
`limited_results` AS (
  SELECT field1, field2, field3, field4
  FROM `results` LIMIT 100
)
SELECT field1, field2, field3, field4
FROM
  (
    SELECT 100 `__total__`, field1, field2, field3, field4
    FROM `limited_results`
    UNION ALL
    SELECT count(*) `__total__`, field1, field2, field3, field4
    FROM `results`
  ) `result_and_count`;
```

TiKV での実行プランは次のとおりです。

    +--------------------------------+-----------+---------+-----------+-----------------------+-----------------------------------------------------+
    | id                             | estRows   | actRows | task      | access object         | execution info                                      |
    +--------------------------------+-----------+---------+-----------+-----------------------+-----------------------------------------------------+
    | Union_18                       | 101.00    | 101     | root      |                       | time:2m38.6s, loops:3, RU:8662189.451027            |
    | ├─Limit_20                     | 100.00    | 100     | root      |                       | time:23ms, loops:2                                  |
    | │ └─TableReader_25             | 100.00    | 100     | root      |                       | time:23ms, loops:1, cop_task: {num: 1, max: 22.8...}|
    | │   └─Limit_24                 | 100.00    | 100     | cop[tikv] |                       | tikv_task:{time:21ms, loops:3}, scan_detail: {...}  |
    | │     └─TableRangeScan_22      | 100.00    | 100     | cop[tikv] | table:usertable       | tikv_task:{time:21ms, loops:3}                      |
    | └─Projection_26                | 1.00      | 1       | root      |                       | time:2m38.6s, loops:2, Concurrency:OFF              |
    |   └─HashAgg_34                 | 1.00      | 1       | root      |                       | time:2m38.6s, loops:2, partial_worker:{...}, fin.. .|
    |     └─TableReader_35           | 1.00      | 5121    | root      |                       | time:2m38.6s, loops:7, cop_task: {num: 5121, max:...|
    |       └─HashAgg_27             | 1.00      | 5121    | cop[tikv] |                       | tikv_task:{proc max:0s, min:0s, avg: 462.8ms, p...} |
    |         └─TableRangeScan_32    | 10000000  | 10000000| cop[tikv] | table:usertable       | tikv_task:{proc max:0s, min:0s, avg: 460.5ms, p...} |
    +--------------------------------+-----------+---------+-----------+-----------------------+-----------------------------------------------------+

TiFlashでの実行プランは次のとおりです。

    +--------------------------------+-----------+---------+--------------+--------------------+-----------------------------------------------------+
    | id                             | estRows   | actRows | task         | access object      | execution info                                      |
    +--------------------------------+-----------+---------+--------------+--------------------+-----------------------------------------------------+
    | Union_18                       | 101.00    | 101     | root         |                    | time:3.44s, loops:3, RU:0.000000                    |
    | ├─Limit_22                     | 100.00    | 100     | root         |                    | time:146.7ms, loops:2                               |
    | │ └─TableReader_30             | 100.00    | 100     | root         |                    | time:146.7ms, loops:1, cop_task: {num: 1, max: 0...}|
    | │   └─ExchangeSender_29        | 100.00    | 0       | mpp[tiflash] |                    |                                                     |
    | │     └─Limit_28               | 100.00    | 0       | mpp[tiflash] |                    |                                                     |
    | │       └─TableRangeScan_27    | 100.00    | 0       | mpp[tiflash] | table:usertable    |                                                     |
    | └─Projection_31                | 1.00      | 1       | root         |                    | time:3.42s, loops:2, Concurrency:OFF                |
    |   └─HashAgg_49                 | 1.00      | 1       | root         |                    | time:3.42s, loops:2, partial_worker:{...}, fin...   |
    |     └─TableReader_51           | 1.00      | 2       | root         |                    | time:3.42s, loops:2, cop_task: {num: 4, max: 0...}  |
    |       └─ExchangeSender_50      | 1.00      | 2       | mpp[tiflash] |                    | tiflash_task:{proc max:3.4s, min:3.15s, avg: 3...}  |
    |         └─HashAgg_36           | 1.00      | 2       | mpp[tiflash] |                    | tiflash_task:{proc max:3.4s, min:3.15s, avg: 3...}  |
    |           └─TableRangeScan_48 | 10000000   | 10000000| mpp[tiflash] | table:usertable    | tiflash_task:{proc max:3.4s, min:3.15s, avg: 3...}  |
    +--------------------------------+-----------+---------+--------------+--------------------+-----------------------------------------------------+

##### TiKVとTiFlash間のクエリルーティング {#query-routing-between-tikv-and-tiflash}

大量のマルチテナント データを含むテーブルに対してTiFlashレプリカを有効にすると、オプティマイザーは行数に基づいてクエリを TiKV またはTiFlashのいずれかにルーティングします。

-   小規模テナント: TiKV は、テーブル範囲スキャンによる小規模クエリに高い同時実行性を提供するため、データ サイズが小さいテナントに適しています。
-   大規模テナント: 大規模なデータセット (この場合は 1,000 万行など) を持つテナントの場合、 TiFlash は次の利点により効率的です。
    -   TiFlash は、特定のインデックスを必要とせずに動的なフィルタリング条件を処理します。
    -   TiDB は、 `COUNT` 、 `SORT` 、および`LIMIT`操作をTiFlashにプッシュダウンできます。
    -   TiFlash は、列指向storageを使用して必要な列のみをスキャンします。
