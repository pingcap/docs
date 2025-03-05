---
title: Import Data into TiDB Cloud Dedicated via MySQL CLI
summary: MySQL CLI 経由でTiDB Cloud Dedicated にデータをインポートする方法を学びます。
---

# MySQL CLI 経由でTiDB Cloud Dedicated にデータをインポートする {#import-data-into-tidb-cloud-dedicated-via-mysql-cli}

このドキュメントでは、 [MySQL コマンドラインクライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)を介してTiDB Cloud Dedicated にデータをインポートする方法について説明します。SQL ファイルまたは CSV ファイルからデータをインポートできます。次のセクションでは、各ファイル タイプからデータをインポートするための手順を順を追って説明します。

## 前提条件 {#prerequisites}

MySQL CLI 経由でTiDB Cloud Dedicated にデータをインポートするには、次の前提条件を満たす必要があります。

-   TiDB Cloud Dedicated クラスターにアクセスできます。アクセスできない場合は、 [TiDB Cloud専用クラスターを作成する](/tidb-cloud/create-tidb-cluster.md)手順に従って作成してください。
-   ローカル コンピュータに MySQL CLI をインストールします。

## ステップ1. TiDB Cloud Dedicatedクラスタに接続する {#step-1-connect-to-your-tidb-cloud-dedicated-cluster}

TiDB クラスターに接続します。

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  左側のナビゲーション ペインで、 **[ネットワーク]**をクリックします。

3.  **[ネットワーク]**ページで、 **[IP アクセス リスト]**領域の**[IP アドレスの追加] を**クリックします。

4.  ダイアログで、 **[どこからでもアクセスを許可する]**を選択し、 **[確認]**をクリックします。

5.  右上隅の**「接続」**をクリックすると、接続情報のダイアログが開きます。

    接続文字列を取得する方法の詳細については、 [パブリック接続経由​​でTiDB Cloud Dedicatedに接続する](/tidb-cloud/connect-via-standard-connection.md)参照してください。

## ステップ2. テーブルを定義し、サンプルデータを挿入する {#step-2-define-the-table-and-insert-sample-data}

データをインポートする前に、テーブル構造を準備し、実際のサンプルデータを挿入する必要があります。以下は、テーブルを作成してサンプルデータを挿入するために使用できるサンプルSQLファイル（ `product_data.sql` ）です。

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

## ステップ3. SQLまたはCSVファイルからデータをインポートする {#step-3-import-data-from-a-sql-or-csv-file}

SQL ファイルまたは CSV ファイルからデータをインポートできます。次のセクションでは、各タイプからデータをインポートする手順を順を追って説明します。

<SimpleTab>
<div label="From an SQL file">

SQL ファイルからデータをインポートするには、次の手順を実行します。

1.  インポートするデータを含む実際の SQL ファイル (たとえば、 `product_data.sql` ) を指定します。この SQL ファイルには、実際のデータを含む`INSERT`ステートメントが含まれている必要があります。

2.  SQL ファイルからデータをインポートするには、次のコマンドを使用します。

    ```bash
    mysql --comments --connect-timeout 150 -u '<your_username>' -h <your_cluster_host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=<your_ca_path> -p<your_password> < product_data.sql
    ```

> **注記：**
>
> ここで使用されるデフォルトのデータベース名は`test`ですが、独自のデータベースを手動で作成するか、SQL ファイルで`CREATE DATABASE`コマンドを使用することができます。

</div>
<div label="From a CSV file">

CSV ファイルからデータをインポートするには、次の手順を実行します。

1.  データのインポートのニーズに合わせて、TiDB でデータベースとスキーマを作成します。

2.  インポートするデータを含むサンプル CSV ファイル (例: `product_data.csv` ) を提供します。次に、CSV ファイルの例を示します。

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

4.  パス、テーブル名 (この例では`products` )、 `<your_username>` 、 `<your_host>` 、 `<your_password>` 、 `<your_csv_path>` 、 `<your_ca_path>` 、およびその他のプレースホルダーを実際の情報に置き換え、必要に応じてサンプル CSV データを実際のデータセットに置き換えてください。

> **注記：**
>
> `LOAD DATA LOCAL INFILE`構文の詳細については、 [`LOAD DATA`](/sql-statements/sql-statement-load-data.md)参照してください。

</div>
</SimpleTab>
