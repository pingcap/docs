---
title: Bookshop Example Application
---

# 書店のサンプルアプリケーション {#bookshop-example-application}

Bookshopは、さまざまなカテゴリの本を購入し、読んだ本を評価できる仮想オンライン書店アプリケーションです。

アプリケーション開発者ガイドをよりスムーズに読むために、Bookshopアプリケーションの[テーブル構造](#description-of-the-tables)とデータに基づいたSQLステートメントの例を示します。このドキュメントでは、テーブル構造とデータのインポート方法、およびテーブル構造の定義に焦点を当てています。

## テーブルの構造とデータをインポートする {#import-table-structures-and-data}

Bookshopのテーブル構造とデータは[TiUP経由](#method-1-via-tiup-demo)または[TiDB Cloudのインポート機能を介して](#method-2-via-tidb-cloud-import)のいずれかでインポートできます。

### 方法1： <code>tiup demo</code>経由 {#method-1-via-code-tiup-demo-code}

TiDBクラスタが[TiUP](/tiup/tiup-reference.md#tiup-reference)を使用してデプロイされている場合、またはTiDBサーバーに接続できる場合は、次のコマンドを実行して、Bookshopアプリケーションのサンプルデータをすばやく生成およびインポートできます。

{{< copyable "" >}}

```shell
tiup demo bookshop prepare
```

デフォルトでは、このコマンドはアプリケーションがアドレス`127.0.0.1`のポート`4000`に接続できるようにし、パスワードなしで`root`ユーザーとしてログインできるようにし、 `bookshop`という名前のデータベースに[テーブル構造](#description-of-the-tables)を作成します。

#### 接続情報を構成する {#configure-connection-information}

次の表に、接続パラメーターを示します。環境に合わせてデフォルト設定を変更できます。

| パラメータ        | 略語   | デフォルト値      | 説明              |
| ------------ | ---- | ----------- | --------------- |
| `--password` | `-p` | なし          | データベースユーザーパスワード |
| `--host`     | `-H` | `127.0.0.1` | データベースアドレス      |
| `--port`     | `-P` | `4000`      | データベースポート       |
| `--db`       | `-D` | `bookshop`  | データベース名         |
| `--user`     | `-U` | `root`      | データベースユーザー      |

たとえば、 TiDB Cloud上のデータベースに接続する場合は、次のように接続情報を指定できます。

{{< copyable "" >}}

```shell
tiup demo bookshop prepare -U root -H tidb.xxx.yyy.ap-northeast-1.prod.aws.tidbcloud.com -P 4000 -p
```

#### データ量を設定する {#set-the-data-volume}

次のパラメータを設定することにより、各データベーステーブルで生成されるデータの量を指定できます。

| パラメータ       | デフォルト値   | 説明                         |
| ----------- | -------- | -------------------------- |
| `--users`   | `10000`  | `users`のテーブルで生成されるデータの行数   |
| `--authors` | `20000`  | `authors`のテーブルで生成される行数     |
| `--books`   | `20000`  | `books`のテーブルで生成されるデータの行数   |
| `--orders`  | `300000` | `orders`のテーブルで生成されるデータの行数  |
| `--ratings` | `300000` | `ratings`のテーブルで生成されるデータの行数 |

たとえば、次のコマンドを実行して生成します。

-   `--users`パラメーターを介した200,000行のユーザー情報
-   `--books`つのパラメータを介した500,000行の書籍情報
-   `--authors`つのパラメーターを介した100,000行の著者情報
-   `--ratings`パラメータによる1,000,000行の評価レコード
-   `--orders`パラメータによる1,000,000行の注文レコード

{{< copyable "" >}}

```shell
tiup demo bookshop prepare --users=200000 --books=500000 --authors=100000 --ratings=1000000 --orders=1000000 --drop-tables
```

`--drop-tables`パラメーターを使用して、元のテーブル構造を削除できます。パラメータの詳細については、 `tiup demo bookshop --help`コマンドを実行してください。

### 方法2： TiDB Cloudインポート経由 {#method-2-via-tidb-cloud-import}

TiDB Cloudのデータベース詳細ページで、[**インポート**]ボタンをクリックして、[<strong>データインポートタスク</strong>]ページに入ります。このページで、次の手順を実行して、BookshopサンプルデータをAWSS3からTiDB Cloudにインポートします。

1.  次の**バケットURL**と<strong>Role-ARN</strong>を対応する入力ボックスにコピーします。

    **バケットURL** ：

    {{< copyable "" >}}

    ```
    s3://developer.pingcap.com/bookshop/
    ```

    **役割-ARN** ：

    {{< copyable "" >}}

    ```
    arn:aws:iam::494090988690:role/s3-tidb-cloud-developer-access
    ```

    この例では、次のデータが事前に生成されています。

    -   200,000行のユーザー情報
    -   500,000行の書籍情報
    -   100,000行の著者情報
    -   1,000,000行の評価レコード
    -   1,000,000行の注文レコード

2.  BucketRegionとして**リージョン** <strong>（オレゴン）</strong>を選択します。

3.  **データ形式**に<strong>TiDBDumpling</strong>を選択します。

    ![Import Bookshop data in TiDB Cloud](/media/develop/tidb_cloud_import_bookshop_data.png)

4.  データベースのログイン情報を入力します。

5.  [**インポート**]ボタンをクリックして、インポートを確認します。

6.  TiDB Cloudがインポートを完了するのを待ちます。

    ![Bookshop data importing](/media/develop/importing_bookshop_data.png)

    インポート処理中に次のエラーメッセージが表示された場合は、 `DROP DATABASE bookshop;`コマンドを実行して、以前に作成したサンプルデータベースをクリアしてから、データを再度インポートしてください。

    > テーブル[ `bookshop` 。 `authors` `bookshop` `book_authors` `bookshop` `books` `bookshop` `orders` `bookshop` `ratings` `bookshop` `users` ]は空ではありません。

TiDB Cloudの詳細については、 [TiDB Cloudドキュメント](https://docs.pingcap.com/tidbcloud)を参照してください。

### データのインポートステータスをビューする {#view-data-import-status}

インポートが完了したら、次のSQLステートメントを実行して、各テーブルのデータボリューム情報を表示できます。

{{< copyable "" >}}

```sql
SELECT
    CONCAT(table_schema,'.',table_name) AS 'Table Name',
    table_rows AS 'Number of Rows',
    CONCAT(ROUND(data_length/(1024*1024*1024),4),'G') AS 'Data Size',
    CONCAT(ROUND(index_length/(1024*1024*1024),4),'G') AS 'Index Size',
    CONCAT(ROUND((data_length+index_length)/(1024*1024*1024),4),'G') AS 'Total'
FROM
    information_schema.TABLES
WHERE table_schema LIKE 'bookshop';
```

結果は次のとおりです。

```
+-----------------------+----------------+-----------+------------+---------+
| Table Name            | Number of Rows | Data Size | Index Size | Total   |
+-----------------------+----------------+-----------+------------+---------+
| bookshop.orders       |        1000000 | 0.0373G   | 0.0075G    | 0.0447G |
| bookshop.book_authors |        1000000 | 0.0149G   | 0.0149G    | 0.0298G |
| bookshop.ratings      |        4000000 | 0.1192G   | 0.1192G    | 0.2384G |
| bookshop.authors      |         100000 | 0.0043G   | 0.0000G    | 0.0043G |
| bookshop.users        |         195348 | 0.0048G   | 0.0021G    | 0.0069G |
| bookshop.books        |        1000000 | 0.0546G   | 0.0000G    | 0.0546G |
+-----------------------+----------------+-----------+------------+---------+
6 rows in set (0.03 sec)
```

## テーブルの説明 {#description-of-the-tables}

このセクションでは、Bookshopアプリケーションのデータベーステーブルについて詳しく説明します。

### <code>books</code>テーブル {#code-books-code-table}

このテーブルには、本の基本情報が格納されています。

| フィールド名         | タイプ          | 説明                    |
| -------------- | ------------ | --------------------- |
| id             | bigint（20）   | 本の一意のID               |
| 題名             | varchar（100） | 本のタイトル                |
| タイプ            | 列挙型          | 本の種類（雑誌、アニメーション、教材など） |
| 株式             | bigint（20）   | ストック                  |
| 価格             | 10進数（15,2）   | 価格                    |
| publication_at | 日付時刻         | 公開日                   |

### <code>authors</code>表 {#code-authors-code-table}

このテーブルには、作成者の基本情報が格納されています。

| フィールド名     | タイプ          | 説明                        |
| ---------- | ------------ | ------------------------- |
| id         | bigint（20）   | 著者の一意のID                  |
| 名前         | varchar（100） | 著者の名前                     |
| 性別         | tinyint（1）   | 生物学的性別（0：女性、1：男性、NULL：不明） |
| 生年         | smallint（6）  | 生年                        |
| death_year | smallint（6）  | 死の年                       |

### <code>users</code>テーブル {#code-users-code-table}

このテーブルには、Bookshopユーザーの情報が格納されます。

| フィールド名 | タイプ          | 説明         |
| ------ | ------------ | ---------- |
| id     | bigint（20）   | ユーザーの一意のID |
| 残高     | 10進数（15,2）   | バランス       |
| ニックネーム | varchar（100） | ニックネーム     |

### <code>ratings</code>表 {#code-ratings-code-table}

このテーブルには、書籍のユーザー評価の記録が保存されます。

| フィールド名   | タイプ     | 説明                                     |
| -------- | ------- | -------------------------------------- |
| book_id  | bigint  | 書籍の一意のID（ [本](#books-table)にリンク）       |
| ユーザーID   | bigint  | ユーザーの一意の識別子（ [ユーザー](#users-table)にリンク） |
| スコア      | tinyint | ユーザー評価（1-5）                            |
| rated_at | 日付時刻    | 評価時間                                   |

### <code>book_authors</code>テーブル {#code-book-authors-code-table}

著者は複数の本を書くことができ、1つの本には複数の著者が関与することがあります。このテーブルには、本と著者の対応が格納されています。

| フィールド名    | タイプ        | 説明                                   |
| --------- | ---------- | ------------------------------------ |
| book_id   | bigint（20） | 書籍の一意のID（ [本](#books-table)にリンク）     |
| author_id | bigint（20） | 著者の一意のID（ [著者](#authors-table)へのリンク） |

### <code>orders</code>表 {#code-orders-code-table}

このテーブルには、ユーザーの購入情報が格納されます。

| フィールド名     | タイプ        | 説明                                           |
| ---------- | ---------- | -------------------------------------------- |
| id         | bigint（20） | 注文の一意のID                                     |
| book_id    | bigint（20） | 書籍の一意のID（ [本](#books-table)にリンク）             |
| ユーザーID     | bigint（20） | ユーザーの一意の識別子（ [ユーザー](#users-table)に関連付けられている） |
| 量          | tinyint（4） | 購入数量                                         |
| Ordered_at | 日付時刻       | 購入時間                                         |

## データベース初期化スクリプト<code>dbinit.sql</code> {#database-initialization-script-code-dbinit-sql-code}

Bookshopアプリケーションでデータベーステーブル構造を手動で作成する場合は、次のSQLステートメントを実行します。

{{< copyable "" >}}

```sql
CREATE DATABASE IF NOT EXISTS `bookshop`;

DROP TABLE IF EXISTS `bookshop`.`books`;
CREATE TABLE `bookshop`.`books` (
  `id` bigint(20) AUTO_RANDOM NOT NULL,
  `title` varchar(100) NOT NULL,
  `type` enum('Magazine', 'Novel', 'Life', 'Arts', 'Comics', 'Education & Reference', 'Humanities & Social Sciences', 'Science & Technology', 'Kids', 'Sports') NOT NULL,
  `published_at` datetime NOT NULL,
  `stock` int(11) DEFAULT '0',
  `price` decimal(15,2) DEFAULT '0.0',
  PRIMARY KEY (`id`) CLUSTERED
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

DROP TABLE IF EXISTS `bookshop`.`authors`;
CREATE TABLE `bookshop`.`authors` (
  `id` bigint(20) AUTO_RANDOM NOT NULL,
  `name` varchar(100) NOT NULL,
  `gender` tinyint(1) DEFAULT NULL,
  `birth_year` smallint(6) DEFAULT NULL,
  `death_year` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`id`) CLUSTERED
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

DROP TABLE IF EXISTS `bookshop`.`book_authors`;
CREATE TABLE `bookshop`.`book_authors` (
  `book_id` bigint(20) NOT NULL,
  `author_id` bigint(20) NOT NULL,
  PRIMARY KEY (`book_id`,`author_id`) CLUSTERED
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

DROP TABLE IF EXISTS `bookshop`.`ratings`;
CREATE TABLE `bookshop`.`ratings` (
  `book_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `score` tinyint NOT NULL,
  `rated_at` datetime NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`book_id`,`user_id`) CLUSTERED,
  UNIQUE KEY `uniq_book_user_idx` (`book_id`,`user_id`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
ALTER TABLE `bookshop`.`ratings` SET TIFLASH REPLICA 1;

DROP TABLE IF EXISTS `bookshop`.`users`;
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM NOT NULL,
  `balance` decimal(15,2) DEFAULT '0.0',
  `nickname` varchar(100) UNIQUE NOT NULL,
  PRIMARY KEY (`id`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

DROP TABLE IF EXISTS `bookshop`.`orders`;
CREATE TABLE `bookshop`.`orders` (
  `id` bigint(20) AUTO_RANDOM NOT NULL,
  `book_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `quality` tinyint(4) NOT NULL,
  `ordered_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) CLUSTERED,
  KEY `orders_book_id_idx` (`book_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
```
