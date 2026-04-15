---
title: Import Data into TiDB Cloud Starter or Essential via MySQL CLI
summary: MySQL CLIを使用して、 TiDB Cloud StarterまたはTiDB Cloud Essentialにデータをインポートする方法を学びましょう。
---

# MySQL CLI を介してTiDB Cloud StarterまたはEssentialにデータをインポートする {#import-data-into-tidb-cloud-starter-or-essential-via-mysql-cli}

このドキュメントでは[MySQLコマンドラインクライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)を介してTiDB Cloud StarterまたはTiDB Cloud Essentialにデータをインポートする方法について説明します。 SQL ファイルまたは CSV ファイルからデータをインポートできます。次のセクションでは、各種類のファイルからデータをインポートするための詳細な手順を説明します。

## 前提条件 {#prerequisites}

MySQL CLI を介してTiDB Cloud StarterまたはTiDB Cloud Essentialにデータをインポートするには、以下の前提条件を満たす必要があります。

-   TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスにアクセスできます。お持ちでない場合は、 [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md)」の手順に従って作成します。
-   ローカルコンピュータにMySQL CLIをインストールしてください。

## ステップ1. TiDB Cloud StarterまたはEssentialインスタンスに接続します。 {#step-1-connect-to-your-tidb-cloud-starter-or-essential-instance}

TiDB Cloud StarterまたはEssentialインスタンスに接続してください。

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud StarterまたはEssentialインスタンスの名前をクリックして、概要ページに移動します。

2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

3.  接続ダイアログの設定がご使用のオペレーティング環境と一致していることを確認してください。

    -   **接続タイプ**は`Public`に設定されています。
    -   **「接続」は**`MySQL CLI`に設定されています。
    -   お使いの環境に合った**オペレーティングシステム**を選択してください。

4.  **「パスワードを生成」を**クリックすると、ランダムなパスワードが生成されます。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードをリセット」**をクリックして新しいパスワードを生成してください。

## ステップ2：テーブルを定義し、サンプルデータを挿入する {#step-2-define-the-table-and-insert-sample-data}

データをインポートする前に、テーブル構造を準備し、実際のサンプルデータを挿入する必要があります。以下は、テーブルを作成してサンプルデータを挿入するために使用できるSQLファイルの例です（ `product_data.sql` ）。

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

## ステップ3. SQLファイルまたはCSVファイルからデータをインポートする {#step-3-import-data-from-an-sql-or-csv-file}

SQLファイルまたはCSVファイルからデータをインポートできます。以下のセクションでは、それぞれのファイル形式からデータをインポートするための手順を詳しく説明します。

<SimpleTab>
<div label="From an SQL file">

SQLファイルからデータをインポートするには、以下の手順を実行してください。

1.  インポートしたいデータを含む実際のSQLファイル（例： `product_data.sql` ）を提供してください。このSQLファイルには、実際のデータを含む`INSERT`個のステートメントが含まれている必要があります。

2.  SQLファイルからデータをインポートするには、以下のコマンドを使用してください。

    ```bash
    mysql --comments --connect-timeout 150 -u '<your_username>' -h <your_cluster_host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=<your_ca_path> -p<your_password> < product_data.sql
    ```

> **注記：**
>
> ここで使用されるデフォルトのデータベース名は`test`です。データベースは手動で作成することも、SQL ファイルで`CREATE DATABASE`コマンドを使用することもできます。

</div>
<div label="From a CSV file">

CSVファイルからデータをインポートするには、以下の手順を実行してください。

1.  TiDBで、データインポートのニーズに合わせてデータベースとスキーマを作成します。

2.  インポートしたいデータを含むサンプルCSVファイル（例： `product_data.csv` ）を提供してください。以下はCSVファイルの例です。

    **product_data.csv:**

    ```csv
    product_id,product_name,price
    4,Laptop,999.99
    5,Smartphone,499.99
    6,Tablet,299.99
    ```

3.  以下のコマンドを使用して、CSVファイルからデータをインポートします。

    ```bash
    mysql --comments --connect-timeout 150 -u '<your_username>' -h <your_host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=<your_ca_path> -p<your_password> -e "LOAD DATA LOCAL INFILE '<your_csv_path>' INTO TABLE products
    FIELDS TERMINATED BY ','
    LINES TERMINATED BY '\n'
    IGNORE 1 LINES (product_id, product_name, price);"
    ```

    パス、テーブル名（この例では`products` ）、 `<your_username>` 、 `<your_host>` 、 `<your_password>` 、 `<your_csv_path>` 、 `<your_ca_path>` 、およびその他のプレースホルダーを実際の情報に置き換え、必要に応じてサンプルCSVデータを実際のデータセットに置き換えてください。

> **注記：**
>
> `LOAD DATA LOCAL INFILE`の構文の詳細については、 [`LOAD DATA`](/sql-statements/sql-statement-load-data.md)参照してください。

</div>
</SimpleTab>
