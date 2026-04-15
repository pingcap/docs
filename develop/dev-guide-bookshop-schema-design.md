---
title: Bookshop Example Application
summary: Bookshopは、書籍の購入と評価を行うオンライン書店アプリです。TiUPまたはTiDB Cloudを使用して、テーブル構造とデータをインポートできます。方法1ではTiUPを使用してサンプルデータを迅速に生成してインポートし、方法2ではAmazon S3からTiDB Cloudにデータをインポートします。データベーステーブルには、書籍、著者、ユーザー、評価、書籍著者、注文が含まれます。データベース初期化スクリプトdbinit.sql`は、Bookshopアプリケーションのテーブル構造を作成します。
aliases: ['/ja/tidb/stable/dev-guide-bookshop-schema-design/','/ja/tidb/dev/dev-guide-bookshop-schema-design/','/ja/tidbcloud/dev-guide-bookshop-schema-design/']
---

# 書店向けアプリケーション例 {#bookshop-example-application}

Bookshopは、さまざまなジャンルの本を購入したり、読んだ本を評価できるオンラインの仮想書店アプリケーションです。

アプリケーション開発者ガイドをよりスムーズにお読みいただけるよう、Bookshopアプリケーションの[テーブル構造](#description-of-the-tables)とデータに基づいたSQL文の例を示します。このドキュメントでは、テーブル構造とデータのインポート方法、およびテーブル構造の定義に焦点を当てています。

## テーブル構造とデータをインポートする {#import-table-structures-and-data}

Bookshopアプリケーションのテーブル構造とデータをインポートするには、以下のインポート方法のいずれかを選択してください。

-   [TiDB セルフマネージド: `tiup demo`経由](#tidb-self-managed-via-tiup-demo)。
-   [TiDB Cloud：インポート機能経由](#tidb-cloud-via-the-import-feature)。

### TiDB セルフマネージド: <code>tiup demo</code>経由 {#tidb-self-managed-via-code-tiup-demo-code}

[TiUP](/tiup/tiup-reference.md#tiup-reference)を使用してTiDBセルフマネージドクラスタをデプロイしている場合、またはTiDBサーバーに接続できる場合は、次のコマンドを実行することで、Bookshopアプリケーション用のサンプルデータをすばやく生成してインポートできます。

```shell
tiup demo bookshop prepare
```

デフォルトでは、このコマンドは、アプリケーションがアドレス`4000`のポート`127.0.0.1`に接続できるようにし、パスワードなしで`root`ユーザーとしてログインできるようにし、データベースに`bookshop`という名前の[テーブル構造](#description-of-the-tables)を作成します。

#### 接続情報を設定する {#configure-connection-information}

以下の表に接続パラメータを示します。環境に合わせてデフォルト設定を変更できます。

| パラメータ        | 略語   | デフォルト値      | 説明               |
| ------------ | ---- | ----------- | ---------------- |
| `--password` | `-p` | なし          | データベースユーザーのパスワード |
| `--host`     | `-H` | `127.0.0.1` | データベースアドレス       |
| `--port`     | `-P` | `4000`      | データベースポート        |
| `--db`       | `-D` | `bookshop`  | データベース名          |
| `--user`     | `-U` | `root`      | データベースユーザー       |

例えば、 TiDB Cloud上のデータベースに接続したい場合は、接続情報を次のように指定できます。

```shell
tiup demo bookshop prepare -U <username> -H <endpoint> -P 4000 -p <password>
```

#### データ量を設定します {#set-the-data-volume}

各データベーステーブルで生成されるデータ量は、以下のパラメータを設定することで指定できます。

| パラメータ       | デフォルト値   | 説明                        |
| ----------- | -------- | ------------------------- |
| `--users`   | `10000`  | `users`テーブルで生成されるデータの行数   |
| `--authors` | `20000`  | `authors`テーブルで生成される行数     |
| `--books`   | `20000`  | `books`テーブルで生成されるデータの行数   |
| `--orders`  | `300000` | `orders`テーブルで生成されるデータの行数  |
| `--ratings` | `300000` | `ratings`テーブルで生成されるデータの行数 |

例えば、以下のコマンドを実行すると、次のものが生成されます。

-   `--users`パラメータを介して取得した 200,000 行のユーザー情報
-   `--books`パラメータを介して50万行の書籍情報を取得
-   `--authors`パラメータによる 100,000 行の著者情報
-   `--ratings`パラメータによる 1,000,000 行の評価レコード
-   `--orders`パラメータを介して1,000,000行の注文レコードを取得

```shell
tiup demo bookshop prepare --users=200000 --books=500000 --authors=100000 --ratings=1000000 --orders=1000000 --drop-tables
```

`--drop-tables`パラメータを使用すると、元のテーブル構造を削除できます。パラメータの詳細については、 `tiup demo bookshop --help`コマンドを実行してください。

### TiDB Cloud：インポート機能経由 {#tidb-cloud-via-the-import-feature}

1.  対象のTiDB Cloudリソースの**インポート**ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。

        > **ヒント：**
        >
        > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

    2.  対象リソースの名前をクリックして概要ページに移動し、左側のナビゲーションペインにある**「インポート」**をクリックします。

2.  **「クラウドストレージからデータをインポート」**を選択し、次に**「Amazon S3」**をクリックします。

3.  **Amazon S3 からデータをインポートする**ページで、以下のソースデータ情報を設定してください。

    -   **インポートするファイル数**： TiDB Cloud Starterの場合は、 **「複数のファイル」**を選択してください。このフィールドはTiDB Cloud Dedicatedでは利用できません。
    -   **スキーマファイルを含める**：**はい**を選択してください。
    -   **データ形式**: SELECT **SQL** 。
    -   **フォルダURI** : `s3://developer.pingcap.com/bookshop/`を入力してください。
    -   **バケットアクセス**: **AWSロールARN**を選択します。
    -   **ロール ARN** : `arn:aws:iam::494090988690:role/s3-tidb-cloud-developer-access`を入力してください。

    この例では、以下のデータが事前に生成されます。

    -   20万行のユーザー情報
    -   50万行の書籍情報
    -   著者情報10万行
    -   1,000,000行の評価記録
    -   1,000,000行の注文記録

4.  **「接続」** ＞ **「インポート開始」**をクリックしてインポート処理を開始し、 TiDB Cloudインポート完了をお待ちください。

データをTiDB Cloudにインポートまたは移行する方法の詳細については、 [TiDB Cloud移行の概要](https://docs.pingcap.com/tidbcloud/tidb-cloud-migration-overview)参照してください。

### データインポート状況をビュー {#view-data-import-status}

インポートが完了したら、次のSQL文を実行することで、各テーブルのデータ量情報を表示できます。

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

結果は以下のとおりです。

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

## 表の説明 {#description-of-the-tables}

このセクションでは、Bookshopアプリケーションのデータベーステーブルについて詳しく説明します。

### <code>books</code> {#code-books-code-table}

この表には書籍の基本情報が格納されています。

| フィールド名 | タイプ           | 説明                       |
| ------ | ------------- | ------------------------ |
| ID     | ビギント          | 書籍の固有ID                  |
| タイトル   | varchar(100)  | 本のタイトル                   |
| タイプ    | 列挙型           | 書籍の種類（例：雑誌、アニメーション、教材など） |
| ストック   | ビギント          | ストック                     |
| 価格     | decimal(15,2) | 価格                       |
| 公開日    | 日時            | 発行日                      |

### <code>authors</code>一覧 {#code-authors-code-table}

この表には著者の基本情報が格納されています。

| フィールド名 | タイプ          | 説明                        |
| ------ | ------------ | ------------------------- |
| ID     | ビギント         | 著者の固有ID                   |
| 名前     | varchar(100) | 著者名                       |
| 性別     | 小さな整数        | 生物学的性別（0：女性、1：男性、NULL：不明） |
| 生年     | スモールイント      | 生年                        |
| 死亡年    | スモールイント      | 死亡年                       |

### <code>users</code>テーブル {#code-users-code-table}

このテーブルには、書店利用者の情報が格納されています。

| フィールド名 | タイプ           | 説明        |
| ------ | ------------- | --------- |
| ID     | ビギント          | ユーザーの固有ID |
| バランス   | decimal(15,2) | バランス      |
| ニックネーム | varchar(100)  | ニックネーム    |

### <code>ratings</code>表 {#code-ratings-code-table}

このテーブルには、書籍に対するユーザー評価の記録が保存されています。

| フィールド名 | タイプ   | 説明                                     |
| ------ | ----- | -------------------------------------- |
| ブックID  | ビギント  | 書籍の固有ID（[本](#books-table)にリンク）         |
| ユーザーID | ビギント  | ユーザーの一意の識別子 ([ユーザー](#users-table)にリンク) |
| スコア    | 小さな整数 | ユーザー評価（1～5）                            |
| 評価_at  | 日時    | 評価時間                                   |

### <code>book_authors</code>テーブル {#code-book-authors-code-table}

著者は複数の書籍を執筆することがあり、また、一冊の書籍に複数の著者が関わる場合もあります。この表は、書籍と著者間の対応関係を格納します。

| フィールド名 | タイプ  | 説明                                 |
| ------ | ---- | ---------------------------------- |
| ブックID  | ビギント | 書籍の固有ID（[本](#books-table)にリンク）     |
| 著者ID   | ビギント | 著者の固有ID（[著者](#authors-table)へのリンク） |

### <code>orders</code>テーブル {#code-orders-code-table}

このテーブルにはユーザーの購入情報が保存されます。

| フィールド名 | タイプ   | 説明                                           |
| ------ | ----- | -------------------------------------------- |
| ID     | ビギント  | 注文の固有ID                                      |
| ブックID  | ビギント  | 書籍の固有ID（[本](#books-table)にリンク）               |
| ユーザーID | ビギント  | ユーザーの一意の識別子 ([ユーザー](#users-table)に関連付けられている) |
| 量      | 小さな整数 | 購入数量                                         |
| 注文日時   | 日時    | 購入時間                                         |

## データベース初期化スクリプト<code>dbinit.sql</code> {#database-initialization-script-code-dbinit-sql-code}

Bookshopアプリケーションでデータベーステーブル構造を手動で作成する場合は、次のSQLステートメントを実行してください。

```sql
CREATE DATABASE IF NOT EXISTS `bookshop`;

DROP TABLE IF EXISTS `bookshop`.`books`;
CREATE TABLE `bookshop`.`books` (
  `id` bigint AUTO_RANDOM NOT NULL,
  `title` varchar(100) NOT NULL,
  `type` enum('Magazine', 'Novel', 'Life', 'Arts', 'Comics', 'Education & Reference', 'Humanities & Social Sciences', 'Science & Technology', 'Kids', 'Sports') NOT NULL,
  `published_at` datetime NOT NULL,
  `stock` int DEFAULT '0',
  `price` decimal(15,2) DEFAULT '0.0',
  PRIMARY KEY (`id`) CLUSTERED
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

DROP TABLE IF EXISTS `bookshop`.`authors`;
CREATE TABLE `bookshop`.`authors` (
  `id` bigint AUTO_RANDOM NOT NULL,
  `name` varchar(100) NOT NULL,
  `gender` tinyint DEFAULT NULL,
  `birth_year` smallint DEFAULT NULL,
  `death_year` smallint DEFAULT NULL,
  PRIMARY KEY (`id`) CLUSTERED
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

DROP TABLE IF EXISTS `bookshop`.`book_authors`;
CREATE TABLE `bookshop`.`book_authors` (
  `book_id` bigint NOT NULL,
  `author_id` bigint NOT NULL,
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
  `id` bigint AUTO_RANDOM NOT NULL,
  `book_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `quality` tinyint NOT NULL,
  `ordered_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) CLUSTERED,
  KEY `orders_book_id_idx` (`book_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
```

## お困りですか？ {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDB Self-Managedのサポートチケットを送信してください](/support.md)
