---
title: MySQLコマンドラインクライアントを使用して{{{ .premium }}}または{{{ .byoc }}}にデータをインポートする
summary: "MySQLコマンドラインクライアント（`mysql`）を使用して、小さなCSVファイルまたはSQLファイルを{{{ .premium }}}または{{{ .byoc }}}インスタンスにインポートする方法を学びましょう。"
---

# MySQLコマンドラインクライアントを使用して{{{ .premium }}}または{{{ .byoc }}}にデータをインポートする

このドキュメントでは、[MySQLコマンドラインクライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)（`mysql`）を使用して{{{ .premium }}}または{{{ .byoc }}}にデータをインポートする方法について説明します。以下のセクションでは、SQLファイルまたはCSVファイルからデータをインポートするための手順を順を追って説明します。このプロセスでは論理インポートが実行され、MySQLコマンドラインクライアントがローカルマシンからTiDB Cloudに対してSQLステートメントを再実行します。

> **Tip:**
>
> - 論理インポートは、比較的小さなSQLファイルまたはCSVファイルに最適です。クラウドストレージからより高速に並列インポートする場合、または[Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)エクスポートの複数ファイルを処理する場合は、[クラウドストレージからCSVファイルを{{{ .premium }}}または{{{ .byoc }}}にインポートする](/tidb-cloud/premium/import-csv-files-premium.md)を参照してください。
> - {{{ .starter }}}またはEssentialについては、[MySQL CLI を介してTiDB Cloud StarterまたはEssentialにデータをインポートする](/tidb-cloud/import-with-mysql-cli-serverless.md)を参照してください。
> - {{{ .dedicated }}}については、[MySQL CLI を介してTiDB Cloud Dedicatedにデータをインポートする](/tidb-cloud/import-with-mysql-cli.md)を参照してください。

## 前提条件 {#prerequisites}

MySQLコマンドラインクライアントを使用して{{{ .premium }}}または{{{ .byoc }}}インスタンスにデータをインポートするには、以下の前提条件を満たす必要があります。

- {{{ .premium }}}または{{{ .byoc }}}インスタンスへのアクセス権が付与されています。
- ローカルコンピュータにMySQLコマンドラインクライアント（`mysql`）をインストールしてください。

## ステップ1. {{{ .premium }}}または{{{ .byoc }}}インスタンスに接続する {#step-1-connect-to-your-premium-or-byoc-instance}

MySQLコマンドラインクライアントを使用して{{{ .premium }}}または{{{ .byoc }}}インスタンスに接続します。初めての場合は、以下の手順を実行してネットワーク接続を設定し、TiDB SQL `root` ユーザーのパスワードを生成してください。

1. [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**My TiDB**](https://tidbcloud.com/tidbs)ページに移動します。次に、対象の{{{ .premium }}}または{{{ .byoc }}}インスタンスの名前をクリックして、その概要ページに移動します。

2. 右上隅の**Connect**をクリックします。接続ダイアログが表示されます。

3. 接続ダイアログ内の設定が、ご使用の動作環境と一致していることを確認します。

    - **Connection Type** は `Public`<CustomContent plan="byoc"> または `Private`（BYOC のデプロイに応じて）</CustomContent> に設定します。
    - **Connect With** は `MySQL CLI` に設定します。
    - **Operating System** がご使用の環境と一致していることを確認します。

    <CustomContent plan="premium">

    > **Note:**
    >
    > {{{ .premium }}}インスタンスでは、パブリックエンドポイントはデフォルトで無効になっています。`Public` オプションが表示されない場合は、インスタンス詳細ページ（**Network** タブ内）でパブリックエンドポイントを有効にするか、続行する前に組織管理者に有効化を依頼してください。

    </CustomContent>

    <CustomContent plan="byoc">

    > **Note:**
    >
    > パブリック接続を利用できるのは、BYOCデプロイメント時にパブリックホストゾーンを指定した場合のみです。プライベートホストゾーンを指定した場合は、プライベート接続を使用してインスタンスに接続してください。

    </CustomContent>

4. **Generate Password** をクリックしてランダムなパスワードを作成します。すでにパスワードを設定している場合は、その認証情報を再利用するか、続行する前にローテーションしてください。

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

次のステップでデータをロードする前に、データベースとテーブルが存在するように、スキーマファイルを{{{ .premium }}}または{{{ .byoc }}}インスタンスに対して実行してください。

## ステップ3. SQLファイルまたはCSVファイルからデータをインポートする {#step-3-import-data-from-an-sql-or-csv-file}

手順2で作成したスキーマにデータをロードするには、MySQLコマンドラインクライアントを使用します。必要に応じて、プレースホルダーを独自のファイルパス、認証情報、データセットに置き換え、ソース形式に合ったワークフローに従ってください。

<SimpleTab>
<div label="From an SQL file">

SQLファイルからデータをインポートするには、以下の手順を実行してください。

1. インポートするデータを含む SQL ファイル (例: `products.sql` ) を提供してください。この SQL ファイルには、次のようなデータを含む`INSERT`文が含まれている必要があります。

    ```sql
    INSERT INTO products (product_id, product_name, price) VALUES
        (1, 'Laptop', 999.99),
        (2, 'Smartphone', 499.99),
        (3, 'Tablet', 299.99);
    ```

2. SQLファイルからデータをインポートするには、以下のコマンドを使用してください。

    ```bash
    mysql --comments --connect-timeout 150 \
      -u '<your_username>' -h <your_instance_host> -P 4000 -D test \
      --ssl-mode=VERIFY_IDENTITY --ssl-ca=<your_ca_path> \
      -p<your_password> < products.sql
    ```

    プレースホルダー値（例： `<your_username>` 、 `<your_instance_host>` 、 `<your_password>` 、 `<your_ca_path>` 、およびSQLファイル名）を、ご自身の接続情報とファイルパスに置き換えてください。

> **Note:**
>
> サンプルスキーマでは`test`データベースが作成され、コマンドでは`-D test`が使用されます。別のデータベースにインポートする場合は、スキーマファイルと`-D`パラメータの両方を変更してください。

<Important>

認証に使用する SQL ユーザーには、テーブルを定義し、ターゲットデータベースにデータをロードするために必要な権限(例えば、 `CREATE`および`INSERT` ) が付与されている必要があります。

</Important>

</div>
<div label="From a CSV file">

CSVファイルからデータをインポートするには、以下の手順を実行してください。

1. TiDB にターゲットのデータベースとテーブルが存在することを確認してください (例えば、ステップ 2 で作成した`products`テーブル)。

2. インポートしたいデータを含むサンプルCSVファイル（例： `products.csv` ）を提供してください。以下に例を示します。

    **products.csv:**

    ```csv
    product_id,product_name,price
    1,Laptop,999.99
    2,Smartphone,499.99
    3,Tablet,299.99
    ```

3. 以下のコマンドを使用して、CSVファイルからデータをインポートします。

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

> **Note:**
>
> `LOAD DATA LOCAL INFILE`の構文の詳細については、 [`LOAD DATA`](/sql-statements/sql-statement-load-data.md)を参照してください。

</div>
</SimpleTab>

## ステップ4. インポートしたデータを検証する {#step-4-validate-the-imported-data}

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
