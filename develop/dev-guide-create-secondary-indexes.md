---
title: Create a Secondary Index
summary: セカンダリ インデックスを作成する手順、ルール、および例を学習します。
---

# セカンダリインデックスを作成する {#create-a-secondary-index}

このドキュメントでは、SQLと様々なプログラミング言語を用いてセカンダリインデックスを作成する方法と、インデックス作成のルールを列挙します。このドキュメントでは、アプリケーション[書店](/develop/dev-guide-bookshop-schema-design.md)例に、セカンダリインデックスの作成手順を順を追って説明します。

## 始める前に {#before-you-start}

セカンダリ インデックスを作成する前に、次の操作を実行します。

-   [{{{ .starter }}}クラスタを構築する](/develop/dev-guide-build-cluster-in-cloud.md) 。
-   [スキーマ設計の概要](/develop/dev-guide-schema-design-overview.md)読んでください。
-   [データベースを作成する](/develop/dev-guide-create-database.md) 。
-   [テーブルを作成する](/develop/dev-guide-create-table.md) 。

## セカンダリインデックスとは {#what-is-secondary-index}

セカンダリインデックスは、TiDBクラスタ内の論理オブジェクトです。TiDBがクエリパフォーマンスを向上させるために使用する、ソート用のデータと考えることができます。TiDBでは、セカンダリインデックスの作成はオンライン操作であり、テーブルに対するデータの読み取りおよび書き込み操作をブロックすることはありません。TiDBは各インデックスに対して、テーブル内の各行への参照を作成し、データではなく選択された列に基づいて参照をソートします。

<CustomContent platform="tidb">

セカンダリインデックスの詳細については、 [セカンダリインデックス](/best-practices/tidb-best-practices.md#secondary-index)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

セカンダリインデックスの詳細については、 [セカンダリインデックス](https://docs.pingcap.com/tidb/stable/tidb-best-practices#secondary-index)参照してください。

</CustomContent>

TiDB では、 [既存のテーブルにセカンダリインデックスを追加する](#add-a-secondary-index-to-an-existing-table)または[新しいテーブルを作成するときにセカンダリインデックスを作成する](#create-a-secondary-index-when-creating-a-new-table)いずれかを選択できます。

## 既存のテーブルにセカンダリインデックスを追加する {#add-a-secondary-index-to-an-existing-table}

既存のテーブルにセカンダリ インデックスを追加するには、次のように[インデックスの作成](/sql-statements/sql-statement-create-index.md)ステートメントを使用できます。

```sql
CREATE INDEX {index_name} ON {table_name} ({column_names});
```

パラメータの説明:

-   `{index_name}` : セカンダリインデックスの名前。
-   `{table_name}` : テーブル名。
-   `{column_names}` : インデックスを作成する列の名前 (セミコロンで区切られます)。

## 新しいテーブルを作成するときにセカンダリインデックスを作成する {#create-a-secondary-index-when-creating-a-new-table}

テーブル作成と同時にセカンダリ インデックスを作成するには、 [テーブルの作成](/sql-statements/sql-statement-create-table.md)ステートメントの末尾に`KEY`キーワードを含む句を追加します。

```sql
KEY `{index_name}` (`{column_names}`)
```

パラメータの説明:

-   `{index_name}` : セカンダリインデックスの名前。
-   `{column_names}` : インデックスを作成する列の名前 (セミコロンで区切られます)。

## セカンダリインデックス作成のルール {#rules-in-secondary-index-creation}

[インデックス作成のベストプラクティス](/develop/dev-guide-index-best-practice.md)参照。

## 例 {#example}

`bookshop`アプリケーション**で、特定の年に出版されたすべての書籍の検索を**サポートするとします。

`books`テーブルのフィールドは次のとおりです。

| フィールド名 | タイプ          | フィールドの説明               |
| ------ | ------------ | ---------------------- |
| id     | ビッグイント(20)   | 本の一意のID                |
| タイトル   | varchar(100) | 書籍タイトル                 |
| タイプ    | 列挙型          | 書籍の種類（例：雑誌、アニメーション、教材） |
| ストック   | ビッグイント(20)   | ストック                   |
| 価格     | 小数点(15,2)    | 価格                     |
| 公開日時   | 日時           | 発行日                    |

`books`テーブルは次の SQL ステートメントを使用して作成されます。

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

年による検索機能をサポートするには、**特定の年に出版されたすべての書籍を検索する**SQL文を記述する必要があります。2022年を例にとると、次のようなSQL文を記述します。

```sql
SELECT * FROM `bookshop`.`books` WHERE `published_at` >= '2022-01-01 00:00:00' AND `published_at` < '2023-01-01 00:00:00';
```

SQL ステートメントの実行プランを確認するには、 [`EXPLAIN`](/sql-statements/sql-statement-explain.md)ステートメントを使用できます。

```sql
EXPLAIN SELECT * FROM `bookshop`.`books` WHERE `published_at` >= '2022-01-01 00:00:00' AND `published_at` < '2023-01-01 00:00:00';
```

以下は実行プランの出力例です。

    +-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------+
    | id                      | estRows  | task      | access object | operator info                                                                                                            |
    +-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------+
    | TableReader_7           | 346.32   | root      |               | data:Selection_6                                                                                                         |
    | └─Selection_6           | 346.32   | cop[tikv] |               | ge(bookshop.books.published_at, 2022-01-01 00:00:00.000000), lt(bookshop.books.published_at, 2023-01-01 00:00:00.000000) |
    |   └─TableFullScan_5     | 20000.00 | cop[tikv] | table:books   | keep order:false                                                                                                         |
    +-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------+
    3 rows in set (0.61 sec)

出力例では、 `id`列目に**TableFullScan**が表示されています。これは、TiDBがこのクエリの`books`番目のテーブルに対してフルテーブルスキャンを実行する準備ができていることを意味します。ただし、データ量が多い場合、フルテーブルスキャンは非常に遅くなり、致命的な影響を与える可能性があります。

このような影響を回避するには、次のように`published_at`列目のインデックスを`books`テーブルに追加します。

```sql
CREATE INDEX `idx_book_published_at` ON `bookshop`.`books` (`bookshop`.`books`.`published_at`);
```

インデックスを追加した後、 `EXPLAIN`ステートメントを再度実行して実行プランを確認します。

以下は出力例です。

    +-------------------------------+---------+-----------+--------------------------------------------------------+-------------------------------------------------------------------+
    | id                            | estRows | task      | access object                                          | operator info                                                     |
    +-------------------------------+---------+-----------+--------------------------------------------------------+-------------------------------------------------------------------+
    | IndexLookUp_10                | 146.01  | root      |                                                        |                                                                   |
    | ├─IndexRangeScan_8(Build)     | 146.01  | cop[tikv] | table:books, index:idx_book_published_at(published_at) | range:[2022-01-01 00:00:00,2023-01-01 00:00:00), keep order:false |
    | └─TableRowIDScan_9(Probe)     | 146.01  | cop[tikv] | table:books                                            | keep order:false                                                  |
    +-------------------------------+---------+-----------+--------------------------------------------------------+-------------------------------------------------------------------+
    3 rows in set (0.18 sec)

出力には**TableFullScan**の代わりに**IndexRangeScan**が表示されます。これは、TiDB がインデックスを使用してこのクエリを実行する準備ができていることを意味します。

実行プラン内の**TableFullScan**や**IndexRangeScan**といった単語は、TiDBでは[オペレーター](/explain-overview.md#operator-overview)です。実行プランと演算子の詳細については、 [TiDB クエリ実行プランの概要](/explain-overview.md)参照してください。

<CustomContent platform="tidb">

実行プランは毎回同じ演算子を返すわけではありません。これは、TiDBが**コストベース最適化（CBO）**アプローチを採用しているためです。CBOアプローチでは、実行プランはルールとデータ配分の両方に依存します。TiDBのTiDB SQLパフォーマンスの詳細については、 [SQLチューニングの概要](/sql-tuning-overview.md)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

実行プランは毎回同じ演算子を返すわけではありません。これは、TiDBが**コストベース最適化（CBO）**アプローチを採用しているためです。CBOアプローチでは、実行プランはルールとデータ配分の両方に依存します。TiDBのTiDB SQLパフォーマンスの詳細については、 [SQLチューニングの概要](/tidb-cloud/tidb-cloud-sql-tuning-overview.md)参照してください。

</CustomContent>

> **注記：**
>
> TiDBはクエリ実行時にインデックスを明示的に使用することもサポートしており、 [オプティマイザヒント](/optimizer-hints.md)または[SQL プラン管理 (SPM)](/sql-plan-management.md)使用してインデックスの使用を人為的に制御できます。ただし、インデックス、オプティマイザヒント、SPMについてよく理解していない場合は、予期しない結果を回避するために、この機能を使用**しないでください**。

テーブルのインデックスをクエリするには、 [インデックスを表示](/sql-statements/sql-statement-show-indexes.md)ステートメントを使用できます。

```sql
SHOW INDEXES FROM `bookshop`.`books`;
```

出力例は次のとおりです。

    +-------+------------+-----------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
    | Table | Non_unique | Key_name              | Seq_in_index | Column_name  | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment | Visible | Expression | Clustered |
    +-------+------------+-----------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
    | books |          0 | PRIMARY               |            1 | id           | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | YES     | NULL       | YES       |
    | books |          1 | idx_book_published_at |            1 | published_at | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | YES     | NULL       | NO        |
    +-------+------------+-----------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
    2 rows in set (1.63 sec)

## 次のステップ {#next-step}

データベースを作成し、そこにテーブルとセカンダリ インデックスを追加したら、データ[書く](/develop/dev-guide-insert-data.md)と[読む](/develop/dev-guide-get-data-from-single-table.md)機能をアプリケーションに追加できるようになります。

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](/support.md)についてコミュニティに質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](https://tidb.support.pingcap.com/)についてコミュニティに質問してください。

</CustomContent>
