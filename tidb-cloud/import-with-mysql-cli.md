---
title: Import Data into TiDB Cloud via MySQL CLI
summary: Learn how to import Data into TiDB Cloud via MySQL CLI.
---

# MySQL CLI 経由でTiDB Cloudにデータをインポート {#import-data-into-tidb-cloud-via-mysql-cli}

このドキュメントでは、 [MySQL コマンドライン クライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)を介してTiDB Cloudにデータをインポートする方法について説明します。 SQL ファイルまたは CSV ファイルからデータをインポートできます。次のセクションでは、各種類のファイルからデータをインポートするための詳細な手順を説明します。

## 前提条件 {#prerequisites}

MySQL CLI を介してデータをTiDB Cloudにインポートするには、次の前提条件が必要です。

-   TiDB Cloudクラスターにアクセスできるようになりました。 TiDB クラスターがない場合は、 [TiDB サーバーレスクラスタを構築する](/develop/dev-guide-build-cluster-in-cloud.md)の手順に従って作成します。
-   MySQL CLI をローカル コンピューターにインストールします。

## ステップ 1. TiDB Cloudクラスターに接続する {#step-1-connect-to-your-tidb-cloud-cluster}

選択した TiDB デプロイメント オプションに応じて、TiDB クラスターに接続します。

<SimpleTab>
<div label="TiDB Serverless">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして、その概要ページに移動します。

2.  右上隅にある**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログの設定が動作環境と一致していることを確認してください。

    -   **エンドポイント タイプは**`Public`に設定されます。
    -   **[接続先] は**`MySQL CLI`に設定されます。
    -   **オペレーティング システムが**環境に一致します。

4.  **「パスワードの生成」**をクリックして、ランダムなパスワードを作成します。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードのリセット」**をクリックして新しいパスワードを生成します。

</div>
<div label="TiDB Dedicated">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして、その概要ページに移動します。

2.  右上隅にある**「接続」**をクリックします。接続ダイアログが表示されます。

3.  **[どこからでもアクセスを許可する]**をクリックします。

    接続文字列を取得する方法の詳細については、 [標準接続経由で TiDB 専用に接続する](/tidb-cloud/connect-via-standard-connection.md)を参照してください。

</div>
</SimpleTab>

## ステップ 2. テーブルを定義し、サンプル データを挿入する {#step-2-define-the-table-and-insert-sample-data}

データをインポートする前に、テーブル構造を準備し、そこに実際のサンプル データを挿入する必要があります。以下は、テーブルの作成とサンプル データの挿入に使用できる SQL ファイルの例 ( `product_data.sql` ) です。

```sql
-- Create a table in your TiDB database
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(255),
    price DECIMAL(10, 2)
);

-- Insert sample data into the table
INSERT INTO products (product_id, product_name, price) VALUES
    (1, 'Laptop', 999.99),
    (2, 'Smartphone', 499.99),
    (3, 'Tablet', 299.99);
```

## ステップ 3. SQL または CSV ファイルからデータをインポートする {#step-3-import-data-from-a-sql-or-csv-file}

SQL ファイルまたは CSV ファイルからデータをインポートできます。次のセクションでは、各タイプからデータをインポートするための詳細な手順を説明します。

<SimpleTab>
<div label="From an SQL file">

SQL ファイルからデータをインポートするには、次の手順を実行します。

1.  インポートするデータを含む実際の SQL ファイル (たとえば、 `product_data.sql` ) を指定します。この SQL ファイルには、実際のデータを含む`INSERT`ステートメントが含まれている必要があります。

2.  SQL ファイルからデータをインポートするには、次のコマンドを使用します。

    ```bash
    mysql --comments --connect-timeout 150 -u '<your_username>' -h <your_cluster_host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=<your_ca_path> -p <your_password> < product_data.sql
    ```

> **注記：**
>
> ここで使用されるデフォルトのデータベース名は`test`で、独自のデータベースを手動で作成することも、SQL ファイルで`CREATE DATABASE`コマンドを使用することもできます。

</div>
<div label="From a CSV file">

CSV ファイルからデータをインポートするには、次の手順を実行します。

1.  データ インポートのニーズに合わせて TiDB にデータベースとスキーマを作成します。

2.  インポートするデータを含むサンプル CSV ファイル (たとえば、 `product_data.csv` ) を提供します。以下は CSV ファイルの例です。

    **製品データ.csv:**

    ```csv
    product_id,product_name,price
    4,Laptop,999.99
    5,Smartphone,499.99
    6,Tablet,299.99
    ```

3.  CSV ファイルからデータをインポートするには、次のコマンドを使用します。

    ```bash
    mysql --comments --connect-timeout 150 -u '<your_username>' -h <your_host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=<your_ca_path> -p<your_password> -e "LOAD DATA LOCAL INFILE '<your_csv_path>' INTO TABLE products
    FIELDS TERMINATED BY ','
    LINES TERMINATED BY '\n'
    IGNORE 1 LINES (product_id, product_name, price);"
    ```

4.  パス、テーブル名 (この例では`products` )、 `<your_username>` 、 `<your_host>` 、 `<your_password>` 、 `<your_csv_path>` 、 `<your_ca_path>` 、およびその他のプレースホルダーを実際の情報に置き換えてください。必要に応じて、サンプル CSV データを実際のデータセットに置き換えてください。

> **注記：**
>
> `LOAD DATA LOCAL INFILE`に関する構文の詳細については、 [`LOAD DATA`](/sql-statements/sql-statement-load-data.md)を参照してください。

</div>
</SimpleTab>
