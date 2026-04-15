---
title: Create a Secondary Index
summary: 二次索引を作成するための手順、ルール、および例を学びましょう。
aliases: ['/ja/tidb/stable/dev-guide-create-secondary-indexes/','/ja/tidb/dev/dev-guide-create-secondary-indexes/','/ja/tidbcloud/dev-guide-create-secondary-indexes/']
---

# セカンダリーインデックスを作成する {#create-a-secondary-index}

このドキュメントでは、SQLと各種プログラミング言語を使用してセカンダリインデックスを作成する方法と、インデックス作成のルールについて説明します。このドキュメントでは、 [書店](/develop/dev-guide-bookshop-schema-design.md)を例として、セカンダリインデックス作成の手順を順を追って説明します。

## 始める前に {#before-you-start}

セカンダリインデックスを作成する前に、以下の手順を実行してください。

-   [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md)。
-   [スキーマ設計の概要](/develop/dev-guide-schema-design-overview.md)お読みください。
-   [データベースを作成する](/develop/dev-guide-create-database.md)。
-   [テーブルを作成する](/develop/dev-guide-create-table.md)。

## 二次インデックスとは何ですか？ {#what-is-secondary-index}

TiDBにおけるセカンダリインデックスは論理オブジェクトです。簡単に言えば、TiDBがクエリパフォーマンスを向上させるために使用するソートタイプのデータと考えることができます。TiDBでは、セカンダリインデックスの作成はオンライン操作であり、テーブルに対するデータの読み書き操作をブロックしません。TiDBは、各インデックスに対してテーブルの各行への参照を作成し、データ自体ではなく、選択された列に基づいて参照をソートします。

二次インデックスの詳細については、 [二次索引](/best-practices/tidb-best-practices.md#secondary-index)参照してください。

TiDB では、[既存のテーブルにセカンダリインデックスを追加する](#add-a-secondary-index-to-an-existing-table)か[新しいテーブルを作成する際にセカンダリインデックスを作成する](#create-a-secondary-index-when-creating-a-new-table)ことができます。

## 既存のテーブルにセカンダリインデックスを追加する {#add-a-secondary-index-to-an-existing-table}

既存のテーブルにセカンダリ インデックスを追加するには、次のようにインデックス[インデックスを作成する](/sql-statements/sql-statement-create-index.md)ステートメントを使用できます。

```sql
CREATE INDEX {index_name} ON {table_name} ({column_names});
```

パラメータの説明:

-   `{index_name}` : セカンダリ インデックスの名前。
-   `{table_name}` : テーブル名。
-   `{column_names}` : インデックスを作成する列の名前をセミコロンとカンマで区切ります。

## 新しいテーブルを作成する際にセカンダリインデックスを作成する {#create-a-secondary-index-when-creating-a-new-table}

テーブルの作成と同時にセカンダリ インデックスを作成するには、テーブルを作成する[テーブルを作成する](/sql-statements/sql-statement-create-table.md)の末尾に`KEY`キーワードを含む句を追加します。

```sql
KEY `{index_name}` (`{column_names}`)
```

パラメータの説明:

-   `{index_name}` : セカンダリ インデックスの名前。
-   `{column_names}` : インデックスを作成する列の名前をセミコロンとカンマで区切ります。

## 二次索引作成におけるルール {#rules-in-secondary-index-creation}

[インデックス作成のベストプラクティス](/develop/dev-guide-index-best-practice.md)を参照してください。

## 例 {#example}

`bookshop`アプリケーションで、**特定の年に出版されたすべての書籍を検索**できるようにしたいとします。

`books`テーブルのフィールドは以下のとおりです。

| フィールド名 | タイプ           | 分野の説明                  |
| ------ | ------------- | ---------------------- |
| ID     | ビギント          | 書籍の固有ID                |
| タイトル   | varchar(100)  | 書籍タイトル                 |
| タイプ    | 列挙型           | 書籍の種類（例：雑誌、アニメーション、教材） |
| ストック   | ビギント          | ストック                   |
| 価格     | decimal(15,2) | 価格                     |
| 公開日    | 日時            | 発行日                    |

`books`テーブルは、次の SQL ステートメントを使用して作成されます。

```sql
CREATE TABLE `bookshop`.`books` (
  `id` bigint AUTO_RANDOM NOT NULL,
  `title` varchar(100) NOT NULL,
  `type` enum('Magazine', 'Novel', 'Life', 'Arts', 'Comics', 'Education & Reference', 'Humanities & Social Sciences', 'Science & Technology', 'Kids', 'Sports') NOT NULL,
  `published_at` datetime NOT NULL,
  `stock` int DEFAULT '0',
  `price` decimal(15,2) DEFAULT '0.0',
  PRIMARY KEY (`id`) CLUSTERED
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
```

年による検索機能をサポートするには、**特定の年に出版されたすべての書籍を検索する**SQL文を作成する必要があります。2022年を例にとると、次のようなSQL文を作成します。

```sql
SELECT * FROM `bookshop`.`books` WHERE `published_at` >= '2022-01-01 00:00:00' AND `published_at` < '2023-01-01 00:00:00';
```

SQL文の実行計画を確認するには、 [`EXPLAIN`](/sql-statements/sql-statement-explain.md)文を使用できます。

```sql
EXPLAIN SELECT * FROM `bookshop`.`books` WHERE `published_at` >= '2022-01-01 00:00:00' AND `published_at` < '2023-01-01 00:00:00';
```

以下は実行計画の出力例です。

    +-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------+
    | id                      | estRows  | task      | access object | operator info                                                                                                            |
    +-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------+
    | TableReader_7           | 346.32   | root      |               | data:Selection_6                                                                                                         |
    | └─Selection_6           | 346.32   | cop[tikv] |               | ge(bookshop.books.published_at, 2022-01-01 00:00:00.000000), lt(bookshop.books.published_at, 2023-01-01 00:00:00.000000) |
    |   └─TableFullScan_5     | 20000.00 | cop[tikv] | table:books   | keep order:false                                                                                                         |
    +-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------+
    3 rows in set (0.61 sec)

出力例において、 `id`列に**TableFullScan**と表示されています。これは、TiDB がこのクエリの`books`テーブルに対してフルテーブルスキャンを実行する準備ができていることを意味します。ただし、データ量が多い場合、フルテーブルスキャンは非常に時間がかかり、致命的な影響を与える可能性があります。

このような影響を回避するには、次のように`published_at`テーブルの`books`列にインデックスを追加できます。

```sql
CREATE INDEX `idx_book_published_at` ON `bookshop`.`books` (`bookshop`.`books`.`published_at`);
```

インデックスを追加した後、 `EXPLAIN`ステートメントを再度実行して、実行プランを確認します。

以下は出力例です。

    +-------------------------------+---------+-----------+--------------------------------------------------------+-------------------------------------------------------------------+
    | id                            | estRows | task      | access object                                          | operator info                                                     |
    +-------------------------------+---------+-----------+--------------------------------------------------------+-------------------------------------------------------------------+
    | IndexLookUp_10                | 146.01  | root      |                                                        |                                                                   |
    | ├─IndexRangeScan_8(Build)     | 146.01  | cop[tikv] | table:books, index:idx_book_published_at(published_at) | range:[2022-01-01 00:00:00,2023-01-01 00:00:00), keep order:false |
    | └─TableRowIDScan_9(Probe)     | 146.01  | cop[tikv] | table:books                                            | keep order:false                                                  |
    +-------------------------------+---------+-----------+--------------------------------------------------------+-------------------------------------------------------------------+
    3 rows in set (0.18 sec)

出力では、 **TableFullScan**の代わりに**IndexRangeScan**が表示されます。これは、TiDB がインデックスを使用してこのクエリを実行する準備ができていることを意味します。

実行プラン内の**TableFullScan**や**IndexRangeScan**などの単語は、TiDB では[オペレーター](/explain-overview.md#operator-overview)です。実行プランと演算子の詳細については、 [TiDBクエリ実行プランの概要](/explain-overview.md)参照してください。

実行プランは毎回同じ演算子を返すとは限りません。これは、TiDBが**コストベース最適化（CBO）**方式を採用しているためで、実行プランはルールとデータ分布の両方に依存します。

SQLパフォーマンスチューニングの詳細については、以下のドキュメントを参照してください。

-   [TiDB CloudのSQLチューニング概要](/tidb-cloud/tidb-cloud-sql-tuning-overview.md)
-   [TiDBセルフマネージドのSQLチューニング概要](/sql-tuning-overview.md)

> **注記：**
>
> TiDB はクエリ時のインデックスの明示的な使用もサポートしており、[オプティマイザのヒント](/optimizer-hints.md)や[SQLプラン管理（SPM）](/sql-plan-management.md)を使用してインデックスの使用を人為的に制御できます。ただし、インデックス、オプティマイザ ヒント、または SPM についてよく知らない場合は、予期しない結果を避けるためにこの機能を使用**しないでください**。

テーブルのインデックスをクエリするには、インデックス[インデックスを表示](/sql-statements/sql-statement-show-indexes.md)ステートメントを使用できます。

```sql
SHOW INDEXES FROM `bookshop`.`books`;
```

以下は出力例です。

    +-------+------------+-----------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
    | Table | Non_unique | Key_name              | Seq_in_index | Column_name  | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment | Visible | Expression | Clustered |
    +-------+------------+-----------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
    | books |          0 | PRIMARY               |            1 | id           | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | YES     | NULL       | YES       |
    | books |          1 | idx_book_published_at |            1 | published_at | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | YES     | NULL       | NO        |
    +-------+------------+-----------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
    2 rows in set (1.63 sec)

## 次のステップ {#next-step}

データベースを作成し、テーブルとセカンダリ インデックスを追加したら、アプリケーションにデータ[書く](/develop/dev-guide-insert-data.md)機能と[読む](/develop/dev-guide-get-data-from-single-table.md)機能を追加できます。

## お困りですか？ {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDB Self-Managedのサポートチケットを送信してください](/support.md)
