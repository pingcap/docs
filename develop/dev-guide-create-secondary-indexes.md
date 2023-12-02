---
title: Create a Secondary Index
summary: Learn steps, rules, and examples to create a secondary index.
---

# セカンダリインデックスを作成する {#create-a-secondary-index}

このドキュメントでは、SQL およびさまざまなプログラミング言語を使用してセカンダリ インデックスを作成する方法を説明し、インデックス作成のルールを示します。このドキュメントでは、 [書店](/develop/dev-guide-bookshop-schema-design.md)アプリケーションを例として、セカンダリ インデックスの作成手順を説明します。

## 始める前に {#before-you-start}

セカンダリ インデックスを作成する前に、次の手順を実行します。

-   [TiDB サーバーレスクラスタを構築する](/develop/dev-guide-build-cluster-in-cloud.md) 。
-   [スキーマ設計の概要](/develop/dev-guide-schema-design-overview.md)を読みます。
-   [データベースを作成する](/develop/dev-guide-create-database.md) 。
-   [テーブルを作成する](/develop/dev-guide-create-table.md) 。

## セカンダリインデックスとは {#what-is-secondary-index}

セカンダリ インデックスは、TiDB クラスター内の論理オブジェクトです。これは、クエリのパフォーマンスを向上させるために TiDB が使用するデータの並べ替えタイプと単純に考えることができます。 TiDB では、セカンダリ インデックスの作成はオンライン操作であり、テーブルに対するデータの読み取りおよび書き込み操作はブロックされません。 TiDB はインデックスごとにテーブル内の各行の参照を作成し、データではなく選択した列によって参照を直接並べ替えます。

<CustomContent platform="tidb">

セカンダリ インデックスの詳細については、 [セカンダリインデックス](/best-practices/tidb-best-practices.md#secondary-index)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

セカンダリ インデックスの詳細については、 [セカンダリインデックス](https://docs.pingcap.com/tidb/stable/tidb-best-practices#secondary-index)を参照してください。

</CustomContent>

TiDB では、 [既存のテーブルにセカンダリ インデックスを追加する](#add-a-secondary-index-to-an-existing-table)または[新しいテーブルを作成するときにセカンダリインデックスを作成する](#create-a-secondary-index-when-creating-a-new-table)いずれかを選択できます。

## 既存のテーブルにセカンダリ インデックスを追加する {#add-a-secondary-index-to-an-existing-table}

既存のテーブルにセカンダリ インデックスを追加するには、次のように[インデックスの作成](/sql-statements/sql-statement-create-index.md)ステートメントを使用します。

```sql
CREATE INDEX {index_name} ON {table_name} ({column_names});
```

パラメータの説明:

-   `{index_name}` : セカンダリインデックスの名前。
-   `{table_name}` : テーブル名。
-   `{column_names}` : セミコロン・カンマで区切られた、インデックスを作成する列の名前。

## 新しいテーブルを作成するときにセカンダリインデックスを作成する {#create-a-secondary-index-when-creating-a-new-table}

テーブルの作成と同時にセカンダリ インデックスを作成するには、 `KEY`キーワードを含む句を[テーブルの作成](/sql-statements/sql-statement-create-table.md)ステートメントの最後に追加します。

```sql
KEY `{index_name}` (`{column_names}`)
```

パラメータの説明:

-   `{index_name}` : セカンダリインデックスの名前。
-   `{column_names}` : セミコロン・カンマで区切られた、インデックスを作成する列の名前。

## セカンダリインデックス作成のルール {#rules-in-secondary-index-creation}

[インデックス作成のベスト プラクティス](/develop/dev-guide-index-best-practice.md)を参照してください。

## 例 {#example}

`bookshop`アプリケーションで、**特定の年に出版されたすべての書籍の検索を**サポートしたいとします。

`books`テーブルのフィールドは次のとおりです。

| フィールド名  | タイプ          | フィールドの説明           |
| ------- | ------------ | ------------------ |
| ID      | bigint(20)   | 本の一意のID            |
| タイトル    | varchar(100) | 本のタイトル             |
| タイプ     | 列挙型          | 本の種類 (雑誌、アニメ、教材など) |
| ストック    | bigint(20)   | ストック               |
| 価格      | 10 進数(15,2)  | 価格                 |
| 公開された_で | 日付時刻         | 発行日                |

`books`テーブルは、次の SQL ステートメントを使用して作成されます。

```sql
CREATE TABLE `bookshop`.`books` (
  `id` bigint(20) AUTO_RANDOM NOT NULL,
  `title` varchar(100) NOT NULL,
  `type` enum('Magazine', 'Novel', 'Life', 'Arts', 'Comics', 'Education & Reference', 'Humanities & Social Sciences', 'Science & Technology', 'Kids', 'Sports') NOT NULL,
  `published_at` datetime NOT NULL,
  `stock` int(11) DEFAULT '0',
  `price` decimal(15,2) DEFAULT '0.0',
  PRIMARY KEY (`id`) CLUSTERED
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
```

年による検索機能をサポートするには、**特定の年に出版されたすべての書籍を検索する**SQL ステートメントを作成する必要があります。 2022 を例として、次のように SQL ステートメントを作成します。

```sql
SELECT * FROM `bookshop`.`books` WHERE `published_at` >= '2022-01-01 00:00:00' AND `published_at` < '2023-01-01 00:00:00';
```

SQL ステートメントの実行計画を確認するには、 [`EXPLAIN`](/sql-statements/sql-statement-explain.md)ステートメントを使用できます。

```sql
EXPLAIN SELECT * FROM `bookshop`.`books` WHERE `published_at` >= '2022-01-01 00:00:00' AND `published_at` < '2023-01-01 00:00:00';
```

以下は、実行計画の出力例です。

    +-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------+
    | id                      | estRows  | task      | access object | operator info                                                                                                            |
    +-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------+
    | TableReader_7           | 346.32   | root      |               | data:Selection_6                                                                                                         |
    | └─Selection_6           | 346.32   | cop[tikv] |               | ge(bookshop.books.published_at, 2022-01-01 00:00:00.000000), lt(bookshop.books.published_at, 2023-01-01 00:00:00.000000) |
    |   └─TableFullScan_5     | 20000.00 | cop[tikv] | table:books   | keep order:false                                                                                                         |
    +-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------+
    3 rows in set (0.61 sec)

出力例では、 **TableFullScan が**`id`列に表示されます。これは、TiDB がこのクエリの`books`テーブルに対してフル テーブル スキャンを実行する準備ができていることを意味します。ただし、大量のデータの場合、テーブル全体のスキャンが非常に遅くなり、致命的な影響を引き起こす可能性があります。

このような影響を回避するには、次のように`published_at`列のインデックスを`books`テーブルに追加します。

```sql
CREATE INDEX `idx_book_published_at` ON `bookshop`.`books` (`bookshop`.`books`.`published_at`);
```

インデックスを追加した後、 `EXPLAIN`ステートメントを再度実行して実行計画を確認します。

以下は出力例です。

    +-------------------------------+---------+-----------+--------------------------------------------------------+-------------------------------------------------------------------+
    | id                            | estRows | task      | access object                                          | operator info                                                     |
    +-------------------------------+---------+-----------+--------------------------------------------------------+-------------------------------------------------------------------+
    | IndexLookUp_10                | 146.01  | root      |                                                        |                                                                   |
    | ├─IndexRangeScan_8(Build)     | 146.01  | cop[tikv] | table:books, index:idx_book_published_at(published_at) | range:[2022-01-01 00:00:00,2023-01-01 00:00:00), keep order:false |
    | └─TableRowIDScan_9(Probe)     | 146.01  | cop[tikv] | table:books                                            | keep order:false                                                  |
    +-------------------------------+---------+-----------+--------------------------------------------------------+-------------------------------------------------------------------+
    3 rows in set (0.18 sec)

出力では、 **TableFullScan**の代わりに**IndexRangeScan**が表示されます。これは、TiDB がこのクエリを実行するためにインデックスを使用する準備ができていることを意味します。

実行計画内の**TableFullScan**や**IndexRangeScan**などの単語は、TiDB では[演算子](/explain-overview.md#operator-overview)です。実行プランと演算子の詳細については、 [TiDB クエリ実行計画の概要](/explain-overview.md)を参照してください。

<CustomContent platform="tidb">

実行プランは毎回同じ演算子を返すわけではありません。これは、TiDB が**コストベースの最適化 (CBO)**アプローチを使用しており、実行計画がルールとデータ分散の両方に依存するためです。 TiDB SQL のパフォーマンスの詳細については、 [SQLチューニングの概要](/sql-tuning-overview.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

実行プランは毎回同じ演算子を返すわけではありません。これは、TiDB が**コストベースの最適化 (CBO)**アプローチを使用しており、実行計画がルールとデータ分散の両方に依存するためです。 TiDB SQL のパフォーマンスの詳細については、 [SQLチューニングの概要](/tidb-cloud/tidb-cloud-sql-tuning-overview.md)を参照してください。

</CustomContent>

> **注記：**
>
> TiDB はクエリ時のインデックスの明示的な使用もサポートしており、 [オプティマイザーのヒント](/optimizer-hints.md)または[SQL 計画管理 (SPM)](/sql-plan-management.md)使用してインデックスの使用を人為的に制御できます。ただし、インデックス、オプティマイザ ヒント、または SPM についてよく知らない場合は、予期しない結果を避けるためにこの機能を使用し**ないでください**。

テーブルのインデックスをクエリするには、 [インデックスを表示](/sql-statements/sql-statement-show-indexes.md)ステートメントを使用できます。

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

データベースを作成し、テーブルとセカンダリ インデックスを追加した後、アプリケーションにデータ[書く](/develop/dev-guide-insert-data.md)および[読む](/develop/dev-guide-get-data-from-single-table.md)機能の追加を開始できます。
