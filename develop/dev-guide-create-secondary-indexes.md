---
title: Create a Secondary Index
summary: Learn steps, rules, and examples to create a secondary index.
---

# セカンダリ インデックスを作成する {#create-a-secondary-index}

このドキュメントでは、SQL とさまざまなプログラミング言語を使用してセカンダリ インデックスを作成する方法について説明し、インデックス作成の規則を示します。このドキュメントでは、 [書店](/develop/dev-guide-bookshop-schema-design.md)アプリケーションを例として、セカンダリ インデックス作成の手順を説明します。

## 始める前に {#before-you-start}

セカンダリ インデックスを作成する前に、次の操作を行います。

-   [TiDB Cloud(Serverless Tier) で TiDBクラスタを構築する](/develop/dev-guide-build-cluster-in-cloud.md) .
-   [スキーマ設計の概要](/develop/dev-guide-schema-design-overview.md)を読んでください。
-   [データベースを作成する](/develop/dev-guide-create-database.md) .
-   [テーブルを作成する](/develop/dev-guide-create-table.md) .

## 二次索引とは {#what-is-secondary-index}

セカンダリ インデックスは、TiDB クラスター内の論理オブジェクトです。これは単に、TiDB がクエリのパフォーマンスを向上させるために使用するデータの並べ替えタイプと見なすことができます。 TiDB では、セカンダリ インデックスの作成はオンライン操作であり、テーブルに対するデータの読み取りおよび書き込み操作をブロックしません。インデックスごとに、TiDB はテーブル内の各行の参照を作成し、直接データではなく選択した列で参照を並べ替えます。

<CustomContent platform="tidb">

副次索引について詳しくは、 [二次索引](/best-practices/tidb-best-practices.md#secondary-index)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

副次索引について詳しくは、 [二次索引](https://docs.pingcap.com/tidb/stable/tidb-best-practices#secondary-index)を参照してください。

</CustomContent>

TiDB では、 [セカンダリ インデックスを既存のテーブルに追加する](#add-a-secondary-index-to-an-existing-table)または[新しいテーブルを作成するときにセカンダリ インデックスを作成する](#create-a-secondary-index-when-creating-a-new-table)いずれかを使用できます。

## 既存のテーブルにセカンダリ インデックスを追加する {#add-a-secondary-index-to-an-existing-table}

セカンダリ インデックスを既存のテーブルに追加するには、次のように[インデックスを作成](/sql-statements/sql-statement-create-index.md)ステートメントを使用できます。

```sql
CREATE INDEX {index_name} ON {table_name} ({column_names});
```

パラメータの説明:

-   `{index_name}` : セカンダリ インデックスの名前。
-   `{table_name}` : テーブル名。
-   `{column_names}` : セミコロンのコンマで区切られた、索引付けされる列の名前。

## 新しいテーブルを作成するときにセカンダリ インデックスを作成する {#create-a-secondary-index-when-creating-a-new-table}

テーブルの作成と同時にセカンダリ インデックスを作成するには、 `KEY`キーワードを含む句を[テーブルを作成](/sql-statements/sql-statement-create-table.md)ステートメントの最後に追加します。

```sql
KEY `{index_name}` (`{column_names}`)
```

パラメータの説明:

-   `{index_name}` : セカンダリ インデックスの名前。
-   `{column_names}` : セミコロンのコンマで区切られた、索引付けされる列の名前。

## 副次索引作成のルール {#rules-in-secondary-index-creation}

[インデックス作成のベスト プラクティス](/develop/dev-guide-index-best-practice.md)を参照してください。

## 例 {#example}

`bookshop`アプリケーションで、**特定の年に出版されたすべての書籍の検索を**サポートするとします。

`books`テーブルのフィールドは次のとおりです。

| フィールド名       | タイプ          | フィールドの説明            |
| ------------ | ------------ | ------------------- |
| ID           | bigint(20)   | 書籍の一意の ID           |
| タイトル         | varchar(100) | 書名                  |
| タイプ          | 列挙           | 書籍の種類 (雑誌、アニメ、教材など) |
| ストック         | bigint(20)   | ストック                |
| 価格           | 10 進数 (15,2) | 価格                  |
| published_at | 日付時刻         | 発行日                 |

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

年による検索機能をサポートするには、**特定の年に発行されたすべての書籍を検索する**SQL ステートメントを作成する必要があります。 2022 年を例にとると、次のように SQL ステートメントを記述します。

```sql
SELECT * FROM `bookshop`.`books` WHERE `published_at` >= '2022-01-01 00:00:00' AND `published_at` < '2023-01-01 00:00:00';
```

SQL ステートメントの実行計画を確認するには、 [`EXPLAIN`](/sql-statements/sql-statement-explain.md)ステートメントを使用できます。

```sql
EXPLAIN SELECT * FROM `bookshop`.`books` WHERE `published_at` >= '2022-01-01 00:00:00' AND `published_at` < '2023-01-01 00:00:00';
```

以下は、実行計画の出力例です。

```
+-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------+
| id                      | estRows  | task      | access object | operator info                                                                                                            |
+-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------+
| TableReader_7           | 346.32   | root      |               | data:Selection_6                                                                                                         |
| └─Selection_6           | 346.32   | cop[tikv] |               | ge(bookshop.books.published_at, 2022-01-01 00:00:00.000000), lt(bookshop.books.published_at, 2023-01-01 00:00:00.000000) |
|   └─TableFullScan_5     | 20000.00 | cop[tikv] | table:books   | keep order:false                                                                                                         |
+-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------+
3 rows in set (0.61 sec)
```

出力例では、 **TableFullScan が**`id`列に表示されています。これは、TiDB がこのクエリの`books`テーブルでフル テーブル スキャンを実行する準備ができていることを意味します。ただし、大量のデータの場合、全表スキャンは非常に遅くなり、致命的な影響を与える可能性があります。

このような影響を避けるために、次のように`published_at`列のインデックスを`books`テーブルに追加できます。

```sql
CREATE INDEX `idx_book_published_at` ON `bookshop`.`books` (`bookshop`.`books`.`published_at`);
```

インデックスを追加したら、再度`EXPLAIN`ステートメントを実行して実行計画を確認します。

以下は出力例です。

```
+-------------------------------+---------+-----------+--------------------------------------------------------+-------------------------------------------------------------------+
| id                            | estRows | task      | access object                                          | operator info                                                     |
+-------------------------------+---------+-----------+--------------------------------------------------------+-------------------------------------------------------------------+
| IndexLookUp_10                | 146.01  | root      |                                                        |                                                                   |
| ├─IndexRangeScan_8(Build)     | 146.01  | cop[tikv] | table:books, index:idx_book_published_at(published_at) | range:[2022-01-01 00:00:00,2023-01-01 00:00:00), keep order:false |
| └─TableRowIDScan_9(Probe)     | 146.01  | cop[tikv] | table:books                                            | keep order:false                                                  |
+-------------------------------+---------+-----------+--------------------------------------------------------+-------------------------------------------------------------------+
3 rows in set (0.18 sec)
```

出力では、 **TableFullScan**の代わりに<strong>IndexRangeScan</strong>が表示されます。これは、TiDB がインデックスを使用してこのクエリを実行する準備ができていることを意味します。

実行計画の**TableFullScan**や<strong>IndexRangeScan</strong>などの単語は、TiDB では[オペレーター](/explain-overview.md#operator-overview)です。実行計画と演算子の詳細については、 [TiDB クエリ実行計画の概要](/explain-overview.md)を参照してください。

<CustomContent platform="tidb">

実行計画は、毎回同じ演算子を返すわけではありません。これは、TiDB が**コストベースの最適化 (CBO) アプローチ**を使用しているためです。このアプローチでは、実行計画はルールとデータ分散の両方に依存します。 TiDB SQLパフォーマンスの詳細については、 [SQL チューニングの概要](/sql-tuning-overview.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

実行計画は、毎回同じ演算子を返すわけではありません。これは、TiDB が**コストベースの最適化 (CBO) アプローチ**を使用しているためです。このアプローチでは、実行計画はルールとデータ分散の両方に依存します。 TiDB SQLパフォーマンスの詳細については、 [SQL チューニングの概要](/tidb-cloud/tidb-cloud-sql-tuning-overview.md)を参照してください。

</CustomContent>

> **ノート：**
>
> TiDB はクエリ時の明示的なインデックスの使用もサポートしており、 [オプティマイザーのヒント](/optimizer-hints.md)または[SQL 計画管理 (SPM)](/sql-plan-management.md)使用して人為的にインデックスの使用を制御できます。ただし、インデックス、オプティマイザ ヒント、または SPM についてよく知らない場合は、予期しない結果を避けるためにこの機能を使用し**ないでください**。

テーブルのインデックスをクエリするには、 [インデックスを表示](/sql-statements/sql-statement-show-indexes.md)ステートメントを使用できます。

```sql
SHOW INDEXES FROM `bookshop`.`books`;
```

次に出力例を示します。

```
+-------+------------+-----------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
| Table | Non_unique | Key_name              | Seq_in_index | Column_name  | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment | Visible | Expression | Clustered |
+-------+------------+-----------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
| books |          0 | PRIMARY               |            1 | id           | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | YES     | NULL       | YES       |
| books |          1 | idx_book_published_at |            1 | published_at | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | YES     | NULL       | NO        |
+-------+------------+-----------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
2 rows in set (1.63 sec)
```

## 次のステップ {#next-step}

データベースを作成し、それにテーブルとセカンダリ インデックスを追加したら、データ[書く](/develop/dev-guide-insert-data.md)と[読む](/develop/dev-guide-get-data-from-single-table.md)機能をアプリケーションに追加することができます。
