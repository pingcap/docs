---
title: Import Data into TiDB Cloud Premium using the MySQL Command-Line Client
summary: MySQL コマンドライン クライアント (mysql`) を使用して、小さな CSV または SQL ファイルをTiDB Cloud Premium インスタンスにインポートする方法を学習します。
---

# MySQL コマンドラインクライアントを使用してTiDB Cloud Premium にデータをインポートする {#import-data-into-tidb-cloud-premium-using-the-mysql-command-line-client}

このドキュメントでは、 [MySQL コマンドラインクライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html) ( `mysql` ) を使用してTiDB Cloud Premium にデータをインポートする方法について説明します。以下のセクションでは、SQL ファイルまたは CSV ファイルからデータをインポートするための手順を段階的に説明します。このプロセスでは論理インポートが実行され、MySQL コマンドラインクライアントがローカルマシンからTiDB Cloudに対して SQL 文を再生します。

> **警告：**
>
> TiDB Cloud Premium は現在、一部の AWS リージョンで**プライベートプレビュー**としてご利用いただけます。
>
> 組織で Premium がまだ有効になっていない場合、または別のクラウド プロバイダーやリージョンでアクセスする必要がある場合は、 [TiDB Cloudコンソール](https://tidbcloud.com/)の左下隅にある**[サポート]**をクリックするか、Web サイトの[お問い合わせ](https://www.pingcap.com/contact-us)フォームからリクエストを送信してください。

> **ヒント：**
>
> -   論理インポートは、比較的小さなSQLファイルまたはCSVファイルに最適です。クラウドstorageからの高速な並列インポート、または[Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)エクスポートから複数のファイルを処理する場合は、 [クラウドストレージからTiDB Cloud PremiumにCSVファイルをインポートする](/tidb-cloud/premium/import-csv-files-premium.md)ご覧ください。
> -   TiDB Cloud Starter または Essential については、 [MySQL CLI 経由でTiDB Cloud Starter または Essential にデータをインポートする](/tidb-cloud/import-with-mysql-cli-serverless.md)参照してください。
> -   TiDB Cloud Dedicated については、 [MySQL CLI 経由でTiDB Cloud Dedicated にデータをインポートする](/tidb-cloud/import-with-mysql-cli.md)参照してください。

## 前提条件 {#prerequisites}

MySQL コマンドライン クライアントを介してTiDB Cloud Premium インスタンスにデータをインポートする前に、次の前提条件を満たす必要があります。

-   TiDB Cloud Premium インスタンスにアクセスできます。
-   ローカルコンピュータにMySQLコマンドラインクライアント（ `mysql` ）をインストールします。

## ステップ1. TiDB Cloud Premiumインスタンスに接続する {#step-1-connect-to-your-tidb-cloud-premium-instance}

MySQLコマンドラインクライアントを使用してTiDBインスタンスに接続します。初めての場合は、以下の手順に従ってネットワーク接続を設定し、 TiDB SQL `root`ユーザーパスワードを生成します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、 [**TiDBインスタンス**](https://tidbcloud.com/project/instances)ページに移動します。次に、ターゲットインスタンスの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログの構成が動作環境と一致していることを確認します。

    -   **接続タイプは**`Public`に設定されています。

    -   **Connect With が**`MySQL CLI`に設定されています。

    -   **オペレーティング システムは**環境に適合します。

    > **注記：**
    >
    > TiDB Cloud Premiumインスタンスでは、パブリックエンドポイントはデフォルトで無効になっています。1オプションが表示され`Public`場合は、インスタンスの詳細ページ（「**ネットワーク」**タブ）でパブリックエンドポイントを有効にするか、組織管理者に有効化を依頼してから続行してください。

4.  **「パスワードを生成」**をクリックすると、ランダムなパスワードが生成されます。既にパスワードを設定している場合は、その認証情報を再利用するか、パスワードをローテーションしてから続行してください。

## ステップ2. ターゲットデータベースとテーブルスキーマを定義する {#step-2-define-the-target-database-and-table-schema}

データをインポートする前に、データセットに一致するターゲット テーブル構造を作成します。

以下は、サンプルデータベースとテーブルを作成するSQLファイルの例（ `products-schema.sql` ）です。データベース名またはテーブル名は、環境に合わせて更新してください。

```sql
CREATE DATABASE IF NOT EXISTS test;
USE test;

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(255),
    price DECIMAL(10, 2)
);
```

次の手順でデータをロードする前に、 TiDB Cloud Premium インスタンスに対してスキーマ ファイルを実行し、データベースとテーブルが存在するようにします。

## ステップ3. SQLまたはCSVファイルからデータをインポートする {#step-3-import-data-from-an-sql-or-csv-file}

MySQL コマンドライン クライアントを使用して、手順 2 で作成したスキーマにデータをロードします。必要に応じてプレースホルダーを独自のファイル パス、資格情報、データセットに置き換え、ソース形式に一致するワークフローに従います。

<SimpleTab>
<div label="From an SQL file">

SQL ファイルからデータをインポートするには、次の手順を実行します。

1.  インポートするデータを含むSQLファイル（例： `products.sql` ）を用意してください。このSQLファイルには、次のような`INSERT`ステートメントとデータが含まれている必要があります。

    ```sql
    INSERT INTO products (product_id, product_name, price) VALUES
        (1, 'Laptop', 999.99),
        (2, 'Smartphone', 499.99),
        (3, 'Tablet', 299.99);
    ```

2.  SQL ファイルからデータをインポートするには、次のコマンドを使用します。

    ```bash
    mysql --comments --connect-timeout 150 \
      -u '<your_username>' -h <your_instance_host> -P 4000 -D test \
      --ssl-mode=VERIFY_IDENTITY --ssl-ca=<your_ca_path> \
      -p<your_password> < products.sql
    ```

    プレースホルダー値 (たとえば、 `<your_username>` 、 `<your_instance_host>` 、 `<your_password>` 、 `<your_ca_path>` 、および SQL ファイル名) を、独自の接続詳細とファイル パスに置き換えます。

> **注記：**
>
> サンプルスキーマは`test`データベースを作成し、コマンドは`-D test`使用します。別のデータベースにインポートする場合は、スキーマファイルと`-D`パラメータの両方を変更してください。

<Important>

認証に使用する SQL ユーザーには、テーブルを定義してターゲット データベースにデータをロードするために必要な権限(たとえば、 `CREATE`および`INSERT` ) が必要です。

</Important>

</div>
<div label="From a CSV file">

CSV ファイルからデータをインポートするには、次の手順を実行します。

1.  ターゲット データベースとテーブルが TiDB に存在することを確認します (たとえば、手順 2 で作成した`products`テーブル)。

2.  インポートしたいデータを含むサンプルCSVファイル（例： `products.csv` ）をご提供ください。以下に例を示します。

    **製品.csv:**

    ```csv
    product_id,product_name,price
    1,Laptop,999.99
    2,Smartphone,499.99
    3,Tablet,299.99
    ```

3.  CSV ファイルからデータをインポートするには、次のコマンドを使用します。

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

    プレースホルダー値 (たとえば、 `<your_username>` 、 `<your_instance_host>` 、 `<your_password>` 、 `<your_ca_path>` 、 `<your_csv_path>` 、およびテーブル名) を、独自の接続の詳細とデータセット パスに置き換えます。

> **注記：**
>
> `LOAD DATA LOCAL INFILE`詳細な構文については、 [`LOAD DATA`](/sql-statements/sql-statement-load-data.md)参照してください。

</div>
</SimpleTab>

## ステップ4. インポートしたデータを検証する {#step-4-validate-the-imported-data}

インポートが完了したら、基本的なクエリを実行して、必要な行が存在し、データが正しいことを確認します。

MySQL コマンドライン クライアントを使用して同じデータベースに接続し、行数のカウントやサンプル レコードの検査などの検証クエリを実行します。

```bash
mysql --comments --connect-timeout 150 \
  -u '<your_username>' -h <your_instance_host> -P 4000 -D test \
  --ssl-mode=VERIFY_IDENTITY --ssl-ca=<your_ca_path> \
  -p<your_password> \
  -e "SELECT COUNT(*) AS row_count FROM products; \
      SELECT * FROM products ORDER BY product_id LIMIT 5;"
```

期待される出力（例）:

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

プレースホルダー値を独自の接続詳細に置き換え、データセットの形状に合わせて検証クエリを調整します。
