---
title: Bookshop Example Application
summary: Bookshopは、書籍の購入と評価を行うオンライン書店アプリです。テーブル構造とデータは、 TiUPまたはTiDB Cloudを介してインポートできます。方法1ではTiUPを使用してサンプルデータを迅速に生成・インポートし、方法2ではAmazon S3からTiDB Cloudにデータをインポートします。データベーステーブルには、書籍、著者、ユーザー、評価、書籍著者、注文情報が含まれます。データベース初期化スクリプト「dbinit.sql」は、Bookshopアプリケーションのテーブル構造を作成します。
aliases: ['/tidb/stable/dev-guide-bookshop-schema-design/','/tidb/dev/dev-guide-bookshop-schema-design/','/tidbcloud/dev-guide-bookshop-schema-design/']
---

# 書店のサンプルアプリケーション {#bookshop-example-application}

Bookshop は、さまざまなカテゴリの本を購入したり、読んだ本を評価できる仮想オンライン書店アプリケーションです。

アプリケーション開発者ガイドをよりスムーズにお読みいただけるよう、Bookshopアプリケーションの[テーブル構造](#description-of-the-tables)とデータに基づいたSQL文の例を示します。このドキュメントでは、テーブル構造とデータのインポート方法、およびテーブル構造の定義に重点を置いています。

## テーブル構造とデータをインポートする {#import-table-structures-and-data}

Bookshop アプリケーションのテーブル構造とデータをインポートするには、次のいずれかのインポート方法を選択します。

-   [TiDB セルフマネージド: `tiup demo`経由](#tidb-self-managed-via-tiup-demo) 。
-   [TiDB Cloud: インポート機能経由](#tidb-cloud-via-the-import-feature) 。

### TiDB セルフマネージド: <code>tiup demo</code>経由 {#tidb-self-managed-via-code-tiup-demo-code}

TiDB クラスターが[TiUP](/tiup/tiup-reference.md#tiup-reference)使用してデプロイされている場合、または TiDBサーバーに接続できる場合は、次のコマンドを実行して、Bookshop アプリケーションのサンプル データを簡単に生成してインポートできます。

```shell
tiup demo bookshop prepare
```

デフォルトでは、このコマンドにより、アプリケーションはアドレス`127.0.0.1`のポート`4000`に接続できるようになり、パスワードなしで`root`ユーザーとしてログインできるようになり、 `bookshop`という名前のデータベースに[テーブル構造](#description-of-the-tables)作成されます。

#### 接続情報を構成する {#configure-connection-information}

以下の表に接続パラメータの一覧を示します。環境に合わせてデフォルト設定を変更できます。

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
-   `--authors`パラメータ経由で 100,000 行の著者情報
-   `--ratings`パラメータによる 1,000,000 行の評価レコード
-   `--orders`パラメータ経由で 1,000,000 行の注文レコード

```shell
tiup demo bookshop prepare --users=200000 --books=500000 --authors=100000 --ratings=1000000 --orders=1000000 --drop-tables
```

`--drop-tables`のパラメータを使用して、元のテーブル構造を削除できます。パラメータの詳細については、 `tiup demo bookshop --help`コマンドを実行してください。

### TiDB Cloud: インポート機能経由 {#tidb-cloud-via-the-import-feature}

1.  ターゲット クラスターの**インポート**ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

        > **ヒント：**
        >
        > 複数のプロジェクトがある場合は、<mdsvgicon name="icon-left-projects">左下隅にある をクリックして、別のプロジェクトに切り替えます。</mdsvgicon>

    2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[インポート] を**クリックします。

2.  **「Cloud Storage からデータをインポート」**を選択し、 **「Amazon S3」**をクリックします。

3.  **「Amazon S3 からのデータのインポート」**ページで、次のソースデータ情報を設定します。

    -   **インポートファイル数**： TiDB Cloud Starterの場合は**「複数ファイル」**を選択してください。このフィールドはTiDB Cloud Dedicatedでは使用できません。
    -   **含まれるスキーマ ファイル**:**はい**を選択します。
    -   **データ形式**: **SQL**を選択します。
    -   **フォルダー URI** : `s3://developer.pingcap.com/bookshop/`を入力します。
    -   **バケットアクセス**: **AWS ロール ARN**を選択します。
    -   **ロール ARN** : `arn:aws:iam::494090988690:role/s3-tidb-cloud-developer-access`を入力します。

    この例では、次のデータが事前に生成されます。

    -   20万行のユーザー情報
    -   50万行の書籍情報
    -   10万行の著者情報
    -   1,000,000行の評価記録
    -   1,000,000行の注文記録

4.  **[接続]** &gt; **[インポートの開始]**をクリックしてインポート プロセスを開始し、 TiDB Cloud がインポートを完了するまで待ちます。

TiDB Cloudにデータをインポートまたは移行する方法の詳細については、 [TiDB Cloud移行の概要](https://docs.pingcap.com/tidbcloud/tidb-cloud-migration-overview)参照してください。

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

結果は次のようになります。

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

このセクションでは、Bookshop アプリケーションのデータベース テーブルについて詳しく説明します。

### <code>books</code> {#code-books-code-table}

このテーブルには書籍の基本情報が格納されます。

| フィールド名 | タイプ          | 説明                    |
| ------ | ------------ | --------------------- |
| id     | ビッグイント       | 本の一意のID               |
| タイトル   | varchar(100) | 本のタイトル                |
| タイプ    | 列挙型          | 本の種類（例：雑誌、アニメーション、教材） |
| ストック   | ビッグイント       | ストック                  |
| 価格     | 小数点(15,2)    | 価格                    |
| 公開日時   | 日時           | 公開日                   |

### <code>authors</code>表 {#code-authors-code-table}

このテーブルには著者の基本情報が格納されます。

| フィールド名 | タイプ          | 説明                        |
| ------ | ------------ | ------------------------- |
| id     | ビッグイント       | 著者の一意のID                  |
| 名前     | varchar(100) | 著者名                       |
| 性別     | タイニーイント      | 生物学的性別（0：女性、1：男性、NULL：不明） |
| 生年     | スモールイント      | 生年                        |
| 死亡年    | スモールイント      | 死亡年                       |

### <code>users</code>テーブル {#code-users-code-table}

このテーブルには、Bookshop ユーザーの情報が保存されます。

| フィールド名 | タイプ          | 説明         |
| ------ | ------------ | ---------- |
| id     | ビッグイント       | ユーザーの一意のID |
| バランス   | 小数点(15,2)    | バランス       |
| ニックネーム | varchar(100) | ニックネーム     |

### <code>ratings</code>表 {#code-ratings-code-table}

このテーブルには、書籍に対するユーザーの評価の記録が保存されます。

| フィールド名 | タイプ     | 説明                                     |
| ------ | ------- | -------------------------------------- |
| 書籍ID   | ビッグイント  | 書籍の一意のID（ [本](#books-table)にリンク）       |
| ユーザーID | ビッグイント  | ユーザーの一意の識別子（ [ユーザー](#users-table)にリンク） |
| スコア    | タイニーイント | ユーザー評価（1～5）                            |
| 定格     | 日時      | 評価時間                                   |

### <code>book_authors</code>テーブル {#code-book-authors-code-table}

著者は複数の本を執筆する場合があり、また、1冊の本に複数の著者が関わる場合もあります。このテーブルは、本と著者の対応関係を保存します。

| フィールド名 | タイプ    | 説明                                  |
| ------ | ------ | ----------------------------------- |
| 書籍ID   | ビッグイント | 書籍の一意のID（ [本](#books-table)にリンク）    |
| 著者ID   | ビッグイント | 著者の固有ID（ [著者](#authors-table)へのリンク） |

### <code>orders</code>表 {#code-orders-code-table}

このテーブルにはユーザーの購入情報が保存されます。

| フィールド名 | タイプ     | 説明                                         |
| ------ | ------- | ------------------------------------------ |
| id     | ビッグイント  | 注文の一意のID                                   |
| 書籍ID   | ビッグイント  | 書籍の一意のID（ [本](#books-table)にリンク）           |
| ユーザーID | ビッグイント  | ユーザー固有識別子（ [ユーザー](#users-table)に関連付けられている） |
| 量      | タイニーイント | 購入数量                                       |
| 注文日時   | 日時      | 購入時間                                       |

## データベース初期化スクリプト<code>dbinit.sql</code> {#database-initialization-script-code-dbinit-sql-code}

Bookshop アプリケーションでデータベース テーブル構造を手動で作成する場合は、次の SQL ステートメントを実行します。

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

## ヘルプが必要ですか? {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに問い合わせてください。
-   [TiDB Cloudのサポートチケットを送信する](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDBセルフマネージドのサポートチケットを送信する](/support.md)
