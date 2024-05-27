---
title: Bookshop Example Application
summary: Bookshop は、書籍を購入して評価するためのオンライン書店アプリです。テーブル構造とデータは、 TiUPまたはTiDB Cloud経由でインポートできます。方法 1 では、 TiUPを使用してサンプルデータをすばやく生成してインポートし、方法 2 では、AWS S3 からTiDB Cloudにデータをインポートします。データベース テーブルには、書籍、著者、ユーザー、評価、書籍の著者、注文が含まれます。データベース初期化スクリプト `dbinit.sql` は、Bookshop アプリケーションのテーブル構造を作成します。
---

# 書店のサンプルアプリケーション {#bookshop-example-application}

Bookshop は、さまざまなカテゴリの本を購入したり、読んだ本に評価を付けたりできる仮想オンライン書店アプリケーションです。

アプリケーション開発者ガイドをよりスムーズに読んでいただくために、Bookshop アプリケーションの[テーブル構造](#description-of-the-tables)とデータに基づいたサンプル SQL ステートメントを紹介します。このドキュメントでは、テーブル構造とデータのインポート方法、およびテーブル構造の定義に重点を置いています。

## テーブル構造とデータをインポートする {#import-table-structures-and-data}

<CustomContent platform="tidb">

Bookshop テーブル構造とデータを[TiUP経由](#method-1-via-tiup-demo)または[TiDB Cloudのインポート機能を介して](#method-2-via-tidb-cloud-import)いずれかでインポートできます。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB Cloudの場合は、 [方法1: `tiup demo`経由](#method-1-via-tiup-demo)スキップして Bookshop テーブル構造[TiDB Cloudのインポート機能を介して](#method-2-via-tidb-cloud-import)をインポートできます。

</CustomContent>

### 方法1: <code>tiup demo</code>経由 {#method-1-via-code-tiup-demo-code}

<CustomContent platform="tidb">

TiDB クラスターが[TiUP](/tiup/tiup-reference.md#tiup-reference)を使用してデプロイされている場合、または TiDBサーバーに接続できる場合は、次のコマンドを実行して、Bookshop アプリケーションのサンプル データをすばやく生成してインポートできます。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB クラスターが[TiUP](https://docs.pingcap.com/tidb/stable/tiup-reference)を使用してデプロイされている場合、または TiDBサーバーに接続できる場合は、次のコマンドを実行して、Bookshop アプリケーションのサンプル データをすばやく生成してインポートできます。

</CustomContent>

```shell
tiup demo bookshop prepare
```

デフォルトでは、このコマンドにより、アプリケーションはアドレス`127.0.0.1`のポート`4000`に接続できるようになり、パスワードなしで`root`ユーザーとしてログインできるようになり、 `bookshop`という名前のデータベースに[テーブル構造](#description-of-the-tables)が作成されます。

#### 接続情報を構成する {#configure-connection-information}

次の表に接続パラメータを示します。環境に合わせてデフォルト設定を変更できます。

| パラメータ        | 略語   | デフォルト値      | 説明              |
| ------------ | ---- | ----------- | --------------- |
| `--password` | `-p` | なし          | データベースユーザーパスワード |
| `--host`     | `-H` | `127.0.0.1` | データベースアドレス      |
| `--port`     | `-P` | `4000`      | データベースポート       |
| `--db`       | `-D` | `bookshop`  | データベース名         |
| `--user`     | `-U` | `root`      | データベースユーザー      |

たとえば、 TiDB Cloud上のデータベースに接続する場合は、次のように接続情報を指定できます。

```shell
tiup demo bookshop prepare -U <username> -H <endpoint> -P 4000 -p <password>
```

#### データ量を設定する {#set-the-data-volume}

次のパラメータを構成することで、各データベース テーブルに生成されるデータの量を指定できます。

| パラメータ       | デフォルト値   | 説明                        |
| ----------- | -------- | ------------------------- |
| `--users`   | `10000`  | `users`テーブルに生成されるデータの行数   |
| `--authors` | `20000`  | `authors`テーブルに生成される行数     |
| `--books`   | `20000`  | `books`テーブルに生成されるデータの行数   |
| `--orders`  | `300000` | `orders`テーブルに生成されるデータの行数  |
| `--ratings` | `300000` | `ratings`テーブルに生成されるデータの行数 |

たとえば、次のコマンドを実行して生成します。

-   `--users`パラメータ経由で 200,000 行のユーザー情報
-   `--books`パラメータで50万行の書籍情報
-   `--authors`パラメータによる著者情報 100,000 行
-   `--ratings`パラメータによる 1,000,000 行の評価レコード
-   `--orders`パラメータによる 1,000,000 行の注文レコード

```shell
tiup demo bookshop prepare --users=200000 --books=500000 --authors=100000 --ratings=1000000 --orders=1000000 --drop-tables
```

`--drop-tables`パラメータを使用して元のテーブル構造を削除できます。パラメータの詳細な説明については、 `tiup demo bookshop --help`コマンドを実行してください。

### 方法2: TiDB Cloudインポート経由 {#method-2-via-tidb-cloud-import}

TiDB Cloudのクラスター詳細ページで、 **「インポート」**領域の**「データのインポート」**をクリックして、 **「データのインポート」**ページに入ります。このページで、次の手順を実行して、Bookshop サンプルデータを AWS S3 からTiDB Cloudにインポートします。

1.  **データ形式**として**SQLファイル**を選択します。

2.  次の**バケット URI**と**ロール ARN**を対応する入力ボックスにコピーします。

    **バケットURI** :

        s3://developer.pingcap.com/bookshop/

    **ロール ARN** :

        arn:aws:iam::494090988690:role/s3-tidb-cloud-developer-access

3.  **「次へ」**をクリックして**「ファイルとフィルター」**の手順に進み、インポートするファイルの情報を確認します。

4.  もう一度**「次へ」**をクリックして**「プレビュー」**手順に進み、インポートするデータのプレビューを確認します。

    この例では、次のデータが事前に生成されます。

    -   200,000行のユーザー情報
    -   50万行の書籍情報
    -   著者情報10万行
    -   1,000,000行の評価記録
    -   1,000,000行の注文記録

5.  **「インポートの開始」**をクリックしてインポート プロセスを開始し、 TiDB Cloud がインポートを完了するまで待ちます。

TiDB Cloudにデータをインポートまたは移行する方法の詳細については、 [TiDB Cloud移行の概要](https://docs.pingcap.com/tidbcloud/tidb-cloud-migration-overview)を参照してください。

### データのインポートステータスをビュー {#view-data-import-status}

インポートが完了したら、次の SQL ステートメントを実行して、各テーブルのデータ ボリューム情報を表示できます。

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

結果は以下のようになります。

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

## テーブルの説明 {#description-of-the-tables}

このセクションでは、Bookshop アプリケーションのデータベース テーブルについて詳しく説明します。

### <code>books</code> {#code-books-code-table}

このテーブルには書籍の基本情報が格納されます。

| フィールド名 | タイプ          | 説明                    |
| ------ | ------------ | --------------------- |
| id     | ビッグイント(20)   | 本の一意のID               |
| タイトル   | varchar(100) | 本のタイトル                |
| タイプ    | 列挙型          | 本の種類（雑誌、アニメーション、教材など） |
| ストック   | ビッグイント(20)   | ストック                  |
| 価格     | 小数点(15,2)    | 価格                    |
| 公開日時   | 日付時刻         | 公開日                   |

### <code>authors</code>表 {#code-authors-code-table}

このテーブルには著者の基本情報が格納されます。

| フィールド名 | タイプ          | 説明                           |
| ------ | ------------ | ---------------------------- |
| id     | ビッグイント(20)   | 著者の一意のID                     |
| 名前     | varchar(100) | 著者名                          |
| 性別     | タイニーイント(1)   | 生物学的性別（0: 女性、1: 男性、NULL: 不明） |
| 生年     | 小さい整数(6)     | 生年                           |
| 死亡年    | 小さい整数(6)     | 死亡年                          |

### <code>users</code>テーブル {#code-users-code-table}

このテーブルには、Bookshop ユーザーの情報が保存されます。

| フィールド名 | タイプ          | 説明         |
| ------ | ------------ | ---------- |
| id     | ビッグイント(20)   | ユーザーの一意のID |
| バランス   | 小数点(15,2)    | バランス       |
| ニックネーム | varchar(100) | ニックネーム     |

### <code>ratings</code>表 {#code-ratings-code-table}

このテーブルには、書籍に対するユーザーの評価の記録が保存されます。

| フィールド名 | タイプ    | 説明                                     |
| ------ | ------ | -------------------------------------- |
| 書籍ID   | ビッグイント | 書籍の一意の ID ( [本](#books-table)にリンク)     |
| ユーザーID | ビッグイント | ユーザーの一意の識別子（ [ユーザー](#users-table)にリンク） |
| スコア    | ちっちゃい  | ユーザー評価 (1-5)                           |
| 評価     | 日付時刻   | 評価時間                                   |

### <code>book_authors</code>テーブル {#code-book-authors-code-table}

著者は複数の本を執筆する場合があり、また、1 冊の本に複数の著者が関与している場合もあります。このテーブルには、本と著者の対応関係が格納されます。

| フィールド名 | タイプ        | 説明                                  |
| ------ | ---------- | ----------------------------------- |
| 書籍ID   | ビッグイント(20) | 書籍の一意の ID ( [本](#books-table)にリンク)  |
| 著者ID   | ビッグイント(20) | 著者の固有ID（ [著者](#authors-table)へのリンク） |

### <code>orders</code>表 {#code-orders-code-table}

このテーブルにはユーザーの購入情報が保存されます。

| フィールド名 | タイプ        | 説明                                          |
| ------ | ---------- | ------------------------------------------- |
| id     | ビッグイント(20) | 注文の一意のID                                    |
| 書籍ID   | ビッグイント(20) | 書籍の一意の ID ( [本](#books-table)にリンク)          |
| ユーザーID | ビッグイント(20) | ユーザー固有の識別子（ [ユーザー](#users-table)に関連付けられている） |
| 量      | タイニーイント(4) | 購入数量                                        |
| 注文日時   | 日付時刻       | 購入時間                                        |

## データベース初期化スクリプト<code>dbinit.sql</code> {#database-initialization-script-code-dbinit-sql-code}

Bookshop アプリケーションでデータベース テーブル構造を手動で作成する場合は、次の SQL ステートメントを実行します。

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
