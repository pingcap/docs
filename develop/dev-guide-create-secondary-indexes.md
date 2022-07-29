---
title: Create a Secondary Index
summary: Learn steps, rules, and examples to create a secondary index.
---

# セカンダリインデックスを作成する {#create-a-secondary-index}

このドキュメントでは、SQLとさまざまなプログラミング言語を使用してセカンダリインデックスを作成する方法について説明し、インデックス作成のルールを示します。このドキュメントでは、 [書店](/develop/dev-guide-bookshop-schema-design.md)のアプリケーションを例として取り上げ、セカンダリインデックスの作成手順を説明します。

## 始める前に {#before-you-start}

セカンダリインデックスを作成する前に、次の手順を実行します。

-   [TiDB Cloud開発者層でTiDBクラスターを構築する](/develop/dev-guide-build-cluster-in-cloud.md) 。
-   [スキーマ設計の概要](/develop/dev-guide-schema-design-overview.md)を読んでください。
-   [データベースを作成する](/develop/dev-guide-create-database.md) 。
-   [テーブルを作成する](/develop/dev-guide-create-table.md) 。

## 二次インデックスとは {#what-is-secondary-index}

セカンダリインデックスは、TiDBクラスタの論理オブジェクトです。これは、TiDBがクエリのパフォーマンスを向上させるために使用するデータの並べ替えタイプと単純に見なすことができます。 TiDBでは、セカンダリインデックスの作成はオンライン操作であり、テーブルに対するデータの読み取りおよび書き込み操作をブロックしません。 TiDBは、インデックスごとに、テーブルの各行の参照を作成し、データから直接ではなく、選択した列で参照を並べ替えます。詳細については、 [二次インデックス](/best-practices/tidb-best-practices.md#secondary-index)を参照してください。

TiDBでは、 [既存のテーブルにセカンダリインデックスを追加します](#add-a-secondary-index-to-an-existing-table)または[新しいテーブルを作成するときにセカンダリインデックスを作成します](#create-a-secondary-index-when-creating-a-new-table)のいずれかを使用できます。

## 既存のテーブルにセカンダリインデックスを追加します {#add-a-secondary-index-to-an-existing-table}

既存のテーブルにセカンダリインデックスを追加するには、次のように[インデックスの作成](/sql-statements/sql-statement-create-index.md)ステートメントを使用できます。

{{< copyable "" >}}

```sql
CREATE INDEX {index_name} ON {table_name} ({column_names});
```

パラメータの説明：

-   `{index_name}` ：セカンダリインデックスの名前。
-   `{table_name}` ：テーブル名。
-   `{column_names}` ：セミコロンコンマで区切られた、インデックス付けされる列の名前。

## 新しいテーブルを作成するときにセカンダリインデックスを作成します {#create-a-secondary-index-when-creating-a-new-table}

テーブルの作成と同時にセカンダリインデックスを作成するには、 [CREATE TABLE](/sql-statements/sql-statement-create-table.md)ステートメントの最後に`KEY`キーワードを含む句を追加します。

{{< copyable "" >}}

```sql
KEY `{index_name}` (`{column_names}`)
```

パラメータの説明：

-   `{index_name}` ：セカンダリインデックスの名前。
-   `{column_names}` ：セミコロンコンマで区切られた、インデックス付けされる列の名前。

## 二次インデックス作成のルール {#rules-in-secondary-index-creation}

[インデックス作成のベストプラクティス](/develop/dev-guide-index-best-practice.md)を参照してください。

## 例 {#example}

`bookshop`のアプリケーション**で、特定の年に出版されたすべての本の検索**をサポートするとします。

`books`テーブルのフィールドは次のとおりです。

| フィールド名         | タイプ          | フィールドの説明              |
| -------------- | ------------ | --------------------- |
| id             | bigint（20）   | 書籍の一意のID              |
| 題名             | varchar（100） | 本のタイトル                |
| タイプ            | 列挙型          | 本の種類（雑誌、アニメーション、教材など） |
| 株式             | bigint（20）   | ストック                  |
| 価格             | 10進数（15,2）   | 価格                    |
| publication_at | 日付時刻         | 公開日                   |

`books`テーブルは、次のSQLステートメントを使用して作成されます。

{{< copyable "" >}}

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

年による検索機能をサポートする**には、特定の年に出版されたすべての本を検索**するSQLステートメントを作成する必要があります。 2022を例にとると、次のようにSQLステートメントを記述します。

{{< copyable "" >}}

```sql
SELECT * FROM `bookshop`.`books` WHERE `published_at` >= '2022-01-01 00:00:00' AND `published_at` < '2023-01-01 00:00:00';
```

SQLステートメントの実行プランを確認するには、 [`EXPLAIN`](/sql-statements/sql-statement-explain.md)ステートメントを使用できます。

{{< copyable "" >}}

```sql
EXPLAIN SELECT * FROM `bookshop`.`books` WHERE `published_at` >= '2022-01-01 00:00:00' AND `published_at` < '2023-01-01 00:00:00';
```

以下は、実行プランの出力例です。

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

出力例では、 **TableFullScan**が`id`列に表示されています。これは、TiDBがこのクエリの`books`テーブルで全表スキャンを実行する準備ができていることを意味します。ただし、大量のデータの場合、全表スキャンは非常に遅く、致命的な影響を与える可能性があります。

このような影響を回避するために、次のように`published_at`列のインデックスを`books`テーブルに追加できます。

{{< copyable "" >}}

```sql
CREATE INDEX `idx_book_published_at` ON `bookshop`.`books` (`bookshop`.`books`.`published_at`);
```

インデックスを追加した後、 `EXPLAIN`ステートメントを再度実行して実行プランを確認してください。

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

出力では、 **TableFullScan**の代わりに<strong>IndexRangeScan</strong>が表示されます。これは、TiDBがインデックスを使用してこのクエリを実行する準備ができていることを意味します。

> **ノート：**
>
> 実行プランの**TableFullScan**や<strong>IndexRangeScan</strong>などの単語はTiDBでは[演算子](/explain-overview.md#operator-overview)です。実行プランと演算子の詳細については、 [TiDBクエリ実行プランの概要](/explain-overview.md)を参照してください。
>
> 実行プランは、毎回同じ演算子を返すわけではありません。これは、TiDBが**コストベースの最適化（CBO）**アプローチを使用しているためです。このアプローチでは、実行プランはルールとデータ分散の両方に依存します。 TiDB SQLのパフォーマンスの詳細については、 [SQLチューニングの概要](/sql-tuning-overview.md)を参照してください。
>
> TiDBは、クエリ時のインデックスの明示的な使用もサポートしており、 [オプティマイザーのヒント](/optimizer-hints.md)または[SQL計画管理（SPM）](/sql-plan-management.md)を使用して、インデックスの使用を人為的に制御できます。ただし、インデックス、オプティマイザヒント、またはSPMについてよく知らない場合は、予期しない結果を回避するためにこの機能を使用し**ない**でください。

テーブルのインデックスをクエリするには、次の[インデックスを表示](/sql-statements/sql-statement-show-indexes.md)のステートメントを使用できます。

{{< copyable "" >}}

```sql
SHOW INDEXES FROM `bookshop`.`books`;
```

以下は出力例です。

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

データベースを作成し、それにテーブルとセカンダリインデックスを追加したら、データ[書きます](/develop/dev-guide-insert-data.md)と[読んだ](/develop/dev-guide-get-data-from-single-table.md)の機能をアプリケーションに追加し始めることができます。
