---
title: Best Practices for Managing Indexes and Identifying Unused Indexes
summary: TiDB でインデックスを管理および最適化し、未使用のインデックスを識別して削除するためのベスト プラクティスを学習します。
aliases: ['/ja/tidb/stable/index-management-best-practices/']
---

# インデックスの管理と未使用のインデックスの特定に関するベストプラクティス {#best-practices-for-managing-indexes-and-identifying-unused-indexes}

インデックスは、データベースクエリのパフォーマンスを最適化し、大量のデータのスキャンの必要性を減らすために不可欠です。しかし、アプリケーションの進化、ビジネスロジックの変化、データ量の増加に伴い、元のインデックス設計では以下のような問題が発生することがあります。

-   未使用のインデックス: これらのインデックスはかつては関連していましたが、クエリ オプティマイザーによって選択されなくなり、storageを消費し、書き込み操作に不要なオーバーヘッドが追加されます。
-   非効率的なインデックス: 一部のインデックスはオプティマイザーによって使用されますが、予想よりも多くのデータをスキャンするため、ディスク I/O が増加し、クエリのパフォーマンスが低下します。

これらのインデックス作成の問題を放置すると、storageコストの増加、パフォーマンスの低下、運用効率の低下につながる可能性があります。TiDBのような分散SQLデータベースでは、分散クエリの規模と複数ノード間の調整の複雑さにより、インデックス作成の非効率性の影響はさらに大きくなります。そのため、データベースを最適化した状態に保つには、定期的なインデックス監査が不可欠です。

インデックスを積極的に識別して最適化すると、次のことが可能になります。

-   storageのオーバーヘッドを削減: 未使用のインデックスを削除すると、ディスク領域が解放され、長期的なstorageコストが削減されます。
-   書き込みパフォーマンスの向上: 不要なインデックスメンテナンスが排除されると、書き込みが多いワークロード ( `INSERT` 、 `UPDATE` 、 `DELETE`など) のパフォーマンスが向上します。
-   クエリ実行の最適化: 効率的なインデックスによりスキャンされる行数が削減され、クエリ速度と応答時​​間が向上します。
-   データベース管理を合理化します。インデックスが少なく、適切に最適化されているため、バックアップ、リカバリ、スキーマの変更が簡素化されます。

インデックスはビジネスロジックの変化に伴って進化するため、定期的なインデックス監査はデータベースメンテナンスの標準的な手順です。TiDBには、インデックスを安全かつ効果的に検出、評価、最適化するための組み込みの観測ツールが用意されています。

TiDB v8.0.0 では、インデックスの使用パターンを追跡し、データに基づいた意思決定を行うのに役立つ[`INFORMATION_SCHEMA.TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md)テーブルと[`sys.schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md)テーブルが導入されています。

このドキュメントでは、未使用または非効率的なインデックスを検出して削除し、TiDB のパフォーマンスと安定性を向上させるために使用できるツールについて説明します。

## TiDBインデックス最適化：データ駆動型アプローチ {#tidb-index-optimization-a-data-driven-approach}

インデックスはクエリパフォーマンスに不可欠ですが、適切な分析を行わずに削除すると、予期せぬパフォーマンス低下やシステムの不安定化につながる可能性があります。安全かつ効果的なインデックス管理を実現するために、TiDBには以下の機能を備えた組み込みの観測ツールが用意されています。

-   インデックスの使用状況をリアルタイムで追跡します。インデックスがアクセスされる頻度と、それがパフォーマンスの向上に貢献しているかどうかを特定します。
-   未使用のインデックスを検出します。データベースが最後に再起動されてから使用されていないインデックスを見つけます。
-   インデックスの効率を評価する: インデックスがデータを効果的にフィルター処理しているか、または過度の I/O オーバーヘッドを引き起こしているかを評価します。
-   インデックスの削除を安全にテストします。インデックスを削除する前に一時的にインデックスを非表示にして、そのインデックスに依存するクエリがないことを確認します。

TiDB は、次のツールを導入することでインデックスの最適化を簡素化します。

-   `INFORMATION_SCHEMA.TIDB_INDEX_USAGE` : インデックスの使用パターンとクエリ頻度を監視します。
-   `sys.schema_unused_indexes` : データベースが最後に再起動されてから使用されていないインデックスを一覧表示します。
-   非表示のインデックス: インデックスを完全に削除する前に、削除の影響をテストできます。

これらの観測ツールを使用することで、パフォーマンスの低下を招くことなく、冗長なインデックスを確実にクリーンアップできます。

## <code>TIDB_INDEX_USAGE</code>を使用してインデックスの使用状況を追跡する {#track-index-usage-using-code-tidb-index-usage-code}

[TiDB v8.0.0](/releases/release-8.0.0.md)で導入された`TIDB_INDEX_USAGE`システム テーブルは、インデックスの使用方法に関するリアルタイムの分析情報を提供し、クエリ パフォーマンスの最適化や不要なインデックスの削除に役立ちます。

具体的には、 `TIDB_INDEX_USAGE`システム テーブルを使用して次の操作を実行できます。

-   未使用のインデックスの検出: クエリによってアクセスされていないインデックスを識別し、安全に削除できるインデックスを判断するのに役立ちます。
-   インデックスの効率を分析する: インデックスが使用される頻度と、効率的なクエリ実行に貢献しているかどうかを追跡します。
-   クエリ パターンを評価する: インデックスが読み取り操作、データ スキャン、キー値 (KV) 要求にどのように影響するかを理解します。

[TiDB v8.4.0](/releases/release-8.4.0.md)から始まる`TIDB_INDEX_USAGE`システム テーブルには、クラスター化されたテーブルの主キーも含まれており、インデックスのパフォーマンスをより詳細に把握できます。

### <code>TIDB_INDEX_USAGE</code>の主要な指標 {#key-metrics-in-code-tidb-index-usage-code}

`TIDB_INDEX_USAGE`システム テーブルのフィールドを確認する場合は、次の SQL ステートメントを実行します。

```sql
USE INFORMATION_SCHEMA;
DESC TIDB_INDEX_USAGE;
```

```sql
+--------------------------+-------------+------+------+---------+-------+
| Field                    | Type        | Null | Key  | Default | Extra |
+--------------------------+-------------+------+------+---------+-------+
| TABLE_SCHEMA             | varchar(64) | YES  |      | NULL    |       |
| TABLE_NAME               | varchar(64) | YES  |      | NULL    |       |
| INDEX_NAME               | varchar(64) | YES  |      | NULL    |       |
| QUERY_TOTAL              | bigint(21)  | YES  |      | NULL    |       |
| KV_REQ_TOTAL             | bigint(21)  | YES  |      | NULL    |       |
| ROWS_ACCESS_TOTAL        | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_0      | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_0_1    | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_1_10   | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_10_20  | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_20_50  | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_50_100 | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_100    | bigint(21)  | YES  |      | NULL    |       |
| LAST_ACCESS_TIME         | datetime    | YES  |      | NULL    |       |
+--------------------------+-------------+------+------+---------+-------+
14 rows in set (0.00 sec)
```

これらの列の説明については、 [`TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md)参照してください。

### <code>TIDB_INDEX_USAGE</code>を使用して未使用および非効率的なインデックスを特定する {#identify-unused-and-inefficient-indexes-using-code-tidb-index-usage-code}

このセクションでは、 `TIDB_INDEX_USAGE`システム テーブルを使用して、未使用のインデックスと非効率的なインデックスを識別する方法について説明します。

-   未使用のインデックス:

    -   `QUERY_TOTAL = 0`場合、インデックスはどのクエリでも使用されていません。
    -   `LAST_ACCESS_TIME`かなり前のものを示している場合、インデックスはもはや関連がない可能性があります。

-   非効率的なインデックス:

    -   `PERCENTAGE_ACCESS_100`値が大きい場合は完全なインデックス スキャンが実行されることを意味し、インデックスが非効率的である可能性があります。
    -   `ROWS_ACCESS_TOTAL`と`QUERY_TOTAL`比較して、インデックスが使用量に比べてスキャンする行数が多すぎるかどうかを判断します。

`TIDB_INDEX_USAGE`システム テーブルを使用すると、インデックスのパフォーマンスに関する詳細な情報を取得できるため、不要なインデックスを削除し、クエリ実行を最適化することが容易になります。

### <code>TIDB_INDEX_USAGE</code>効果的に使用する {#use-code-tidb-index-usage-code-effectively}

次の点は、 `TIDB_INDEX_USAGE`システム テーブルを正しく理解して使用するのに役立ちます。

#### データの更新が遅れている {#data-updates-are-delayed}

パフォーマンスへの影響を最小限に抑えるため、 `TIDB_INDEX_USAGE`即座に更新されません。インデックス使用状況の指標は最大 5 分ほど遅延する場合があります。クエリを分析する際は、このレイテンシーにご注意ください。

#### インデックス使用状況データは保存されません {#index-usage-data-is-not-persisted}

`TIDB_INDEX_USAGE`システムテーブルは各 TiDB インスタンスのメモリ内にデータを保存し、永続化されません。TiDB ノードが再起動すると、そのノードのすべてのインデックス使用統計がクリアされます。

#### 履歴データを追跡する {#track-historical-data}

次の SQL ステートメントを使用して、インデックス使用状況のスナップショットを定期的にエクスポートできます。

```sql
SELECT * FROM INFORMATION_SCHEMA.TIDB_INDEX_USAGE INTO OUTFILE '/backup/index_usage_snapshot.csv';
```

これにより、時間の経過に伴うスナップショットの比較による履歴追跡が可能になり、インデックスの使用傾向を検出し、より情報に基づいたプルーニングの決定を行うことができます。

## <code>CLUSTER_TIDB_INDEX_USAGE</code>を使用して TiDB ノード間でインデックス使用状況データを統合します。 {#consolidate-index-usage-data-across-tidb-nodes-using-code-cluster-tidb-index-usage-code}

TiDBは分散SQLデータベースであるため、クエリのワークロードは複数のノードに分散されます。各TiDBノードは、自身のローカルインデックスの使用状況を追跡します。インデックスパフォーマンスのグローバルビューとして、TiDBは[`CLUSTER_TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md#cluster_tidb_index_usage)システムテーブルを提供しています。このビューは、すべてのTiDBノードからのインデックス使用状況データを統合し、インデックス戦略の最適化において分散クエリのワークロードを完全に考慮します。

TiDBノードごとにクエリのワークロードが異なる場合があります。一部のノードでは未使用のように見えるインデックスが、他のノードでは依然として重要なものとなっている可能性があります。ワークロード別にインデックス分析を分割するには、次のSQL文を実行します。

```sql
SELECT INSTANCE, TABLE_NAME, INDEX_NAME, SUM(QUERY_TOTAL) AS total_queries
FROM INFORMATION_SCHEMA.CLUSTER_TIDB_INDEX_USAGE
GROUP BY INSTANCE, TABLE_NAME, INDEX_NAME
ORDER BY total_queries DESC;
```

これにより、インデックスがすべてのノードで実際に未使用であるか、特定のインスタンスでのみ未使用であるかを判断し、情報に基づいたインデックスの削除を決定できるようになります。

### <code>TIDB_INDEX_USAGE</code>と<code>CLUSTER_TIDB_INDEX_USAGE</code>の主な違い {#key-differences-between-code-tidb-index-usage-code-and-code-cluster-tidb-index-usage-code}

次の表は、 `TIDB_INDEX_USAGE`と`CLUSTER_TIDB_INDEX_USAGE`の主な違いを示しています。

| 特徴       | `TIDB_INDEX_USAGE`                     | `CLUSTER_TIDB_INDEX_USAGE`         |
| -------- | -------------------------------------- | ---------------------------------- |
| 範囲       | 単一のデータベース インスタンス内のインデックスの使用状況を追跡します。   | TiDB クラスター全体のインデックスの使用状況を集計します。    |
| インデックス追跡 | データは各データベース インスタンスに対してローカルです。          | クラスター全体の集中ビューを提供します。               |
| 主な使用例    | データベース インスタンス レベルでインデックスの使用状況をデバッグします。 | グローバル インデックス パターンとマルチノードの動作を分析します。 |

### <code>CLUSTER_TIDB_INDEX_USAGE</code>効果的に使用する {#use-code-cluster-tidb-index-usage-code-effectively}

`CLUSTER_TIDB_INDEX_USAGE`システム テーブルは複数のノードからのデータを統合するため、次の点に注意してください。

-   データ更新の遅延

    パフォーマンスへの影響を最小限に抑えるため、 `CLUSTER_TIDB_INDEX_USAGE`即座に更新されません。インデックス使用状況の指標は最大 5 分ほど遅延する場合があります。クエリを分析する際は、このレイテンシーにご注意ください。

-   メモリベースのstorage

    `TIDB_INDEX_USAGE`と同様に、このシステムテーブルはノードの再起動後にデータを保持しません。ノードがダウンした場合、記録されたインデックス使用状況データは失われます。

`CLUSTER_TIDB_INDEX_USAGE`使用すると、インデックスの動作を全体的に把握でき、インデックス戦略が分散クエリのワークロードに適合していることを確認できます。

## <code>schema_unused_indexes</code>を使用して未使用のインデックスを識別する {#identify-unused-indexes-using-code-schema-unused-indexes-code}

インデックス使用状況データを手動で分析するのは時間がかかります。このプロセスを簡素化するために、TiDBは[`schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md)提供しています。これは、データベースの最後の再起動以降に使用されていないインデックスを一覧表示するシステムビューです。

これにより、次の操作を簡単に実行できるようになります。

-   使用されなくなったインデックスを識別し、不要なstorageコストを削減します。
-   `INSERT` 、 `UPDATE` 、 `DELETE`クエリにオーバーヘッドを追加するインデックスを削除することで、DML 操作を高速化します。
-   クエリ パターンを手動で分析する必要なく、インデックス監査を合理化します。

`schema_unused_indexes`使用すると、不要なインデックスをすばやく識別し、最小限の労力でデータベースのオーバーヘッドを削減できます。

### <code>schema_unused_indexes</code>仕組み {#how-code-schema-unused-indexes-code-works}

`schema_unused_indexes`ビューは`TIDB_INDEX_USAGE`から派生しており、最後の TiDB 再起動以降にクエリ アクティビティが 0 個記録されたインデックスを自動的に除外することを意味します。

未使用のインデックスのリストを取得するには、次の SQL ステートメントを実行します。

```sql
SELECT * FROM sys.schema_unused_indexes;
```

次のような結果が返されます。

    +-----------------+---------------+--------------------+
    | object_schema   | object_name   | index_name         |
    +---------------- + ------------- + -------------------+
    | bookshop        | users         | nickname           |
    | bookshop        | ratings       | uniq_book_user_idx |
    +---------------- + ------------- + -------------------+

### <code>schema_unused_indexes</code>を使用する際の考慮事項 {#considerations-when-using-code-schema-unused-indexes-code}

`schema_unused_indexes`使用する場合は、次の点に注意してください。

#### インデックスは最後の再起動以降のみ未使用とみなされます {#indexes-are-considered-unused-only-since-the-last-restart}

-   TiDB ノードが再起動すると、使用状況追跡データはリセットされます。
-   このデータに依存する前に、代表的なワークロードをキャプチャできるほど十分にシステムが実行中であることを確認してください。

#### 未使用のインデックスをすべてすぐに削除できるわけではない {#not-all-unused-indexes-can-be-dropped-immediately}

インデックスの中には、あまり使用されないものの、特定のクエリ、バッチジョブ、レポート作成タスクには不可欠なものもあります。インデックスを削除する前に、以下の機能をサポートしているかどうかを検討してください。

-   稀だが重要なクエリ（例：月次レポート、分析）
-   毎日実行されないバッチ処理ジョブ
-   アドホックトラブルシューティングクエリ

重要だが頻度の低いクエリにインデックスが表示される場合は、まずインデックスを保持するか非表示にすることをお勧めします。

[目に見えないインデックス](#safely-test-index-removal-using-invisible-indexes)使用すると、パフォーマンスに影響を与えずにインデックスを削除できるかどうかを安全にテストできます。

### <code>schema_unused_indexes</code>ビューを手動で作成する {#manually-create-the-code-schema-unused-indexes-code-view}

以前のバージョンから TiDB v8.0.0 以降にアップグレードされたクラスターの場合は、システム スキーマと含まれるビューを手動で作成する必要があります。

詳細については[`schema_unused_indexes`ビューを手動で作成する](/sys-schema/sys-schema-unused-indexes.md#manually-create-the-schema_unused_indexes-view)参照してください。

## 非表示のインデックスを使用してインデックスの削除を安全にテストする {#safely-test-index-removal-using-invisible-indexes}

適切な検証を行わずにインデックスを削除すると、特にインデックスが頻繁に使用されないものの、特定のクエリにとって依然として重要である場合、予期しないパフォーマンスの問題が発生する可能性があります。

このリスクを軽減するために、TiDBは不可視インデックスを提供しています。これにより、インデックスを削除せずに一時的に無効化することができます。不可視インデックスを使用することで、インデックス削除の決定を安全に検証でき、より制御された予測可能なデータベース最適化プロセスを実現できます。

### 非表示のインデックスとは何ですか? {#what-are-invisible-indexes}

非表示のインデックスはデータベースに残りますが、TiDBオプティマイザによって無視されます。1 [`ALTER TABLE ... INVISIBLE`](/sql-statements/sql-statement-alter-table.md)使用してインデックスを非表示にすることで、インデックスを永久に削除することなく、本当に不要かどうかをテストできます。

非表示インデックスの主な利点は次のとおりです。

-   **安全なインデックステスト**：クエリはインデックスを使用しなくなりますが、関連するオプティマイザ統計は引き続き維持されます。必要に応じていつでも簡単に復元できます。
-   **インデックスstorageの中断はゼロ**: インデックスはそのまま残るため、コストのかかる再作成は不要です。
-   **パフォーマンス監視**: DBA は、最終決定を下す前に、インデックスなしでクエリの動作を観察できます。

### インデックスを非表示にする {#make-an-index-invisible}

インデックスを削除せずに非表示にするには、次のような SQL ステートメントを実行します。

```sql
ALTER TABLE bookshop.users ALTER INDEX nickname INVISIBLE;
```

インデックスを非表示にした後、システムのクエリ パフォーマンスを観察します。

-   パフォーマンスに変化がない場合、インデックスは不要である可能性が高いため、安全に削除できます。
-   クエリのレイテンシーが増加すると、インデックスが依然として必要になる可能性があります。

### 目に見えないインデックスを効果的に使用する {#use-invisible-indexes-effectively}

-   **オフピーク時にテストする**: 制御された環境でパフォーマンスへの影響を監視します。
-   **クエリ監視ツールを使用する**: インデックスを非表示にする前と後のクエリ実行プランを分析します。
-   **複数のワークロードで確認します**。特定のレポートやスケジュールされたクエリにインデックスが必要ないことを確認します。

### インデックスを非表示のままにできる期間はどのくらいですか? {#how-long-can-an-index-remain-invisible}

-   OLTP ワークロード: 毎日の変動を考慮するために少なくとも 1 週間監視します。
-   バッチ処理または ETL ワークロード: 月次財務レポートなどの 1 つの完全なレポート サイクルを許可します。
-   アドホック分析クエリ: クエリ ログを使用して、インデックスを削除する前にインデックスが必要ないことを確認します。

安全のため、最終決定を下す前にすべてのワークロードがテストされていることを確認するために、少なくとも 1 つのビジネス サイクル全体にわたってインデックスを非表示にしておきます。

## インデックス最適化のベストプラクティストップ5 {#top-five-best-practices-for-index-optimization}

高いパフォーマンスと効率的なリソース利用を維持するために、定期的なインデックス最適化はデータベースメンテナンスの一部です。TiDBでインデックスを効果的に管理するためのベストプラクティスを以下に示します。

1.  **インデックスの使用状況を定期的に監視します。**

    -   インデックスの使用アクティビティを追跡するには、 [`TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md)と[`CLUSTER_TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md#cluster_tidb_index_usage)使用します。
    -   [`schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md)を使用して未使用のインデックスを識別し、削除できるかどうかを評価します。
    -   クエリ実行プランを監視して、過剰な I/O を引き起こす可能性のある非効率的なインデックスを検出します。

2.  **インデックスを削除する前に検証します。**

    -   [`ALTER TABLE ... INVISIBLE`](/sql-statements/sql-statement-alter-table.md)使用してインデックスを非表示にし、一時的にインデックスを無効にして、完全に削除する前にその影響を確認します。
    -   クエリのパフォーマンスが安定している場合は、インデックスの削除に進みます。
    -   最終決定を下す前に、すべてのクエリ パターンを考慮するのに十分な観察期間を確保してください。

3.  **既存のインデックスを最適化します。**

    -   冗長なインデックスを統合することで、storageのオーバーヘッドを削減し、書き込みパフォーマンスを向上させることができます。複数のインデックスが類似したクエリを処理している場合は、それらを単一の、より効率的なインデックスに統合することを検討してください。

        -   重複するプレフィックスを持つインデックス (冗長性を示している可能性があります) を検索するには、次の SQL ステートメントを実行します。

            ```sql
            SELECT TABLE_SCHEMA, TABLE_NAME, INDEX_NAME, COLUMN_NAME, SEQ_IN_INDEX
            FROM INFORMATION_SCHEMA.STATISTICS
            WHERE TABLE_NAME = 'your_table'
            ORDER BY TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, SEQ_IN_INDEX;
            ```

        -   2 つのインデックスの先頭列が同じ場合は、代わりにそれらを複合インデックスにマージすることを検討してください。

    -   選択性の向上。選択性の低いインデックス（フィルタリングする行が多すぎるインデックス）は、次のように最適化できます。

        -   フィルタリングの効率を向上させるために列を追加します。
        -   インデックス構造の変更 (プレフィックス インデックス、複合インデックスなど)。

    -   インデックスの選択性を分析します。3 `TIDB_INDEX_USAGE`フィールドのうち`PERCENTAGE_ACCESS_*`使用して、インデックスがデータをどの程度適切にフィルタリングしているかを評価します。

4.  **DML パフォーマンスへの影響に注意してください。**

    -   過剰なインデックス作成は避けてください。インデックスを追加するごとに`UPDATE` `INSERT` `DELETE`のオーバーヘッドが増加します。
    -   書き込みが多いワークロードのメンテナンス コストを最小限に抑えるために、クエリに必要なものだけをインデックスします。

5.  **定期的にテストと調整を行ってください。**

    -   特にワークロードに大きな変更があった場合には、インデックス監査を定期的に実行します。
    -   TiDB の実行プラン分析ツールを使用して、インデックスが最適に使用されているかどうかを確認します。
    -   新しいインデックスを追加するときは、予期しない回帰を防ぐために、まず分離された環境でテストしてください。

これらのベスト プラクティスに従うことで、効率的なクエリ実行を実現し、不要なstorageオーバーヘッドを削減し、最適なデータベース パフォーマンスを維持できます。
