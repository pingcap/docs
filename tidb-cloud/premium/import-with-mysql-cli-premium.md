---
title: Import Data into TiDB Cloud Premium using the MySQL Command-Line Client
summary: MySQLコマンドラインクライアント（mysql`）を使用して、小さなCSVファイルまたはSQLファイルをTiDB Cloud Premiumインスタンスにインポートする方法を学びましょう。
---

# MySQLコマンドラインクライアントを使用してTiDB Cloud Premiumにデータをインポートする {#import-data-into-tidb-cloud-premium-using-the-mysql-command-line-client}

このドキュメントでは[MySQLコマンドラインクライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)を使用してTiDB Cloud Premium にデータをインポートする方法について説明します。( `mysql` )。以下のセクションでは、SQL ファイルまたは CSV ファイルからデータをインポートするための手順を段階的に説明します。このプロセスでは論理インポートが実行され、MySQL コマンドライン クライアントがローカル マシンからTiDB Cloudに対して SQL ステートメントを再生します。

> **ヒント：**
>
> -   論理インポートは、比較的小さな SQL ファイルまたは CSV ファイルに最適です。クラウドstorageからのより高速な並行インポート、または[Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)エクスポートからの複数のファイルの処理については、 [クラウドストレージからCSVファイルをTiDB Cloud Premiumにインポートする](/tidb-cloud/premium/import-csv-files-premium.md)インポートするを参照してください。
> -   TiDB Cloud StarterまたはEssentialについては、 [MySQL CLI を介してTiDB Cloud StarterまたはEssentialにデータをインポートする](/tidb-cloud/import-with-mysql-cli-serverless.md)参照してください。
> -   TiDB Cloud Dedicatedについては、 [MySQL CLI を介してTiDB Cloud Dedicatedにデータをインポートする](/tidb-cloud/import-with-mysql-cli.md)参照してください。

## 前提条件 {#prerequisites}

MySQLコマンドラインクライアントを使用してTiDB Cloud Premiumインスタンスにデータをインポートするには、以下の前提条件を満たす必要があります。

-   TiDB Cloud Premiumインスタンスへのアクセス権が付与されています。
-   ローカルコンピュータにMySQLコマンドラインクライアント（ `mysql` ）をインストールしてください。

## ステップ1. TiDB Cloud Premiumインスタンスに接続します。 {#step-1-connect-to-your-tidb-cloud-premium-instance}

MySQLコマンドラインクライアントを使用してTiDB Cloud Premiumインスタンスに接続します。初めて接続する場合は、以下の手順を実行してネットワーク接続を設定し、 TiDB SQL `root`ユーザーパスワードを生成してください。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。次に、ターゲットのTiDB Cloud Premium インスタンスの名前をクリックして、その概要ページに移動します。

2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

3.  接続ダイアログの設定がご使用のオペレーティング環境と一致していることを確認してください。

    -   **接続タイプ**は`Public`に設定されています。

    -   **「接続」は**`MySQL CLI`に設定されています。

    -   お使いの環境に合った**オペレーティングシステム**を選択してください。

    > **注記：**
    >
    > TiDB Cloud Premiumインスタンスでは、パブリックエンドポイントはデフォルトで無効になっています。 `Public`オプションが表示されない場合は、インスタンスの詳細ページ（**ネットワーク**タブ）でパブリックエンドポイントを有効にするか、組織の管理者に有効化を依頼してから先に進んでください。

4.  **「パスワードを生成」をクリックすると、ランダムなパスワード**が生成されます。既にパスワードを設定している場合は、そのパスワードを再利用するか、変更してから先に進んでください。

## ステップ2. 対象データベースとテーブルスキーマを定義する {#step-2-define-the-target-database-and-table-schema}

データをインポートする前に、データセットに一致するターゲットテーブル構造を作成してください。

以下は、サンプルデータベースとテーブルを作成するSQLファイルの例です（ `products-schema.sql` ）。データベース名またはテーブル名は、ご使用の環境に合わせて更新してください。

```sql
CREATE DATABASE IF NOT EXISTS test;
USE test;

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(255),
    price DECIMAL(10, 2)
);
```

次のステップでデータをロードする前に、データベースとテーブルが存在するように、スキーマファイルをTiDB Cloud Premiumインスタンスに対して実行してください。

## ステップ3. SQLファイルまたはCSVファイルからデータをインポートする {#step-3-import-data-from-an-sql-or-csv-file}

手順2で作成したスキーマにデータをロードするには、MySQLコマンドラインクライアントを使用します。必要に応じて、プレースホルダーを独自のファイルパス、認証情報、データセットに置き換え、ソース形式に合ったワークフローに従ってください。

<SimpleTab>
<div label="From an SQL file">

SQLファイルからデータをインポートするには、以下の手順を実行してください。

1.  インポートするデータを含む SQL ファイル (例: `products.sql` ) を提供してください。この SQL ファイルには、次のようなデータを含む`INSERT`ステートメントが含まれている必要があります。

    ```sql
    INSERT INTO products (product_id, product_name, price) VALUES
        (1, 'Laptop', 999.99),
        (2, 'Smartphone', 499.99),
        (3, 'Tablet', 299.99);
    ```

2.  SQLファイルからデータをインポートするには、以下のコマンドを使用してください。

    ```bash
    mysql --comments --connect-timeout 150 \
      -u '<your_username>' -h <your_instance_host> -P 4000 -D test \
      --ssl-mode=VERIFY_IDENTITY --ssl-ca=<your_ca_path> \
      -p<your_password> < products.sql
    ```

    プレースホルダー値（例： `<your_username>` 、 `<your_instance_host>` 、 `<your_password>` 、 `<your_ca_path>` 、およびSQLファイル名）を、ご自身の接続情報とファイルパスに置き換えてください。

> **注記：**
>
> サンプルスキーマでは`test`データベースが作成され、コマンドでは`-D test`が使用されます。別のデータベースにインポートする場合は、スキーマファイルと`-D`パラメータの両方を変更してください。

<Important>

認証に使用する SQL ユーザーには、テーブルを定義し、ターゲット データベースにデータをロードするために必要な権限(例えば、 `CREATE`および`INSERT` ) が付与されている必要があります。

</Important>

</div>
<div label="From a CSV file">

CSVファイルからデータをインポートするには、以下の手順を実行してください。

1.  TiDB にターゲットのデータベースとテーブルが存在することを確認してください (例えば、ステップ 2 で作成した`products`テーブル)。

2.  インポートしたいデータを含むサンプルCSVファイル（例： `products.csv` ）を提供してください。以下に例を示します。

    **products.csv:**

    ```csv
    product_id,product_name,price
    1,Laptop,999.99
    2,Smartphone,499.99
    3,Tablet,299.99
    ```

3.  以下のコマンドを使用して、CSVファイルからデータをインポートします。

    ```bash
    mysql --comments --connect-timeout 150 \
      -u '<your_username>' -h <your_instance_host> -P 4000 -D test \
      --ssl-mode=VERIFY_IDENTITY --ssl-ca=<your_ca_path> \
      -p<your_password> \
      -e "LOAD DATA LOCAL INFILE '<your_csv_path>' INTO TABLE products
          FIELDS TERMINATED BY ','
          LINES TERMINATED BY '\n'
          IGNORE 1 LINES (product_id, product_name, price);"
    ```

    プレースホルダー値（例： `<your_username>` 、 `<your_instance_host>` 、 `<your_password>` 、 `<your_ca_path>` 、 `<your_csv_path>` 、およびテーブル名）を、ご自身の接続情報とデータセットパスに置き換えてください。

> **注記：**
>
> `LOAD DATA LOCAL INFILE`の構文の詳細については、 [`LOAD DATA`](/sql-statements/sql-statement-load-data.md)参照してください。

</div>
</SimpleTab>

## ステップ4．インポートしたデータを検証する {#step-4-validate-the-imported-data}

インポートが完了したら、基本的なクエリを実行して、期待どおりの行が存在し、データが正しいことを確認してください。

MySQLコマンドラインクライアントを使用して同じデータベースに接続し、行数のカウントやサンプルレコードの検査などの検証クエリを実行します。

```bash
mysql --comments --connect-timeout 150 \
  -u '<your_username>' -h <your_instance_host> -P 4000 -D test \
  --ssl-mode=VERIFY_IDENTITY --ssl-ca=<your_ca_path> \
  -p<your_password> \
  -e "SELECT COUNT(*) AS row_count FROM products; \
      SELECT * FROM products ORDER BY product_id LIMIT 5;"
```

期待される出力例：

```text
+-----------+
| row_count |
+-----------+
|         3 |
+-----------+
+------------+---------------+--------+
| product_id | product_name  | price  |
+------------+---------------+--------+
|          1 | Laptop        | 999.99 |
|          2 | Smartphone    | 499.99 |
|          3 | Tablet        | 299.99 |
+------------+---------------+--------+
```

プレースホルダーの値を実際の接続情報に置き換え、データセットの形状に合わせて検証クエリを調整してください。
