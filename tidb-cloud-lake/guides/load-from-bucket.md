---
title: バケットからのロード
summary: データファイルが Amazon S3 などのオブジェクトストレージのバケットに保存されている場合、COPY INTO コマンドを使用してそれらを {{{ .lake }}} に直接ロードできます。ファイルは {{{ .lake }}} がサポートする形式である必要があり、そうでない場合はデータをインポートできないことに注意してください。{{{ .lake }}} がサポートするファイル形式の詳細については、Input & Output File Formats を参照してください。
---

# バケットからのロード

データファイルが Amazon S3 などのオブジェクトストレージのバケットに保存されている場合、[COPY INTO](/tidb-cloud-lake/sql/copy-into-table.md) コマンドを使用してそれらを {{{ .lake }}} に直接ロードできます。ファイルは {{{ .lake }}} がサポートする形式である必要があり、そうでない場合はデータをインポートできないことに注意してください。{{{ .lake }}} がサポートするファイル形式の詳細については、[入出力ファイル形式](/tidb-cloud-lake/sql/input-output-file-formats.md) を参照してください。

![image](/media/tidb-cloud-lake/load-data-from-s3.jpeg)

このチュートリアルでは Amazon S3 バケットを例として使用し、バケットに保存されたファイルからデータをロード (load) するプロセスを効果的に進められるよう、詳細なステップバイステップのガイドを提供します。

## チュートリアル: Amazon S3 バケットからのロード {#tutorial-loading-from-amazon-s3-bucket}

### 始める前に {#before-you-begin}

開始する前に、次のタスクを完了していることを確認してください。

1. サンプルファイル [books.parquet](https://lakesql-bin.tidbcloud.com/datasets/books.parquet) をダウンロードし、ローカルフォルダに保存します。このファイルには 2 件のレコードが含まれています。

    ```text title='books.parquet'
    Transaction Processing,Jim Gray,1992
    Readings in Database Systems,Michael Stonebraker,2004
    ```

2. Amazon S3 にバケットを作成し、そのバケットにサンプルファイルをアップロードします。手順については、次のリンクを参照してください。

- バケットの作成: <https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html>
- オブジェクトのアップロード: <https://docs.aws.amazon.com/AmazonS3/latest/userguide/upload-objects.html>

このチュートリアルでは、**US East (Ohio)** リージョン（ID: us-east-2）に **lake-toronto** という名前のバケットを作成しています。

### ステップ 1. 対象テーブルを作成する {#step-1-create-target-table}

{{{ .lake }}} で次の SQL 文を使用してテーブルを作成します。

```sql
USE default;
CREATE TABLE books
(
    title VARCHAR,
    author VARCHAR,
    date VARCHAR
);
```

### ステップ 2. テーブルにデータをコピーする {#step-2-copy-data-into-table}

1. [COPY INTO](/tidb-cloud-lake/sql/copy-into-table.md) コマンドを使用して、対象テーブルにデータをロードします。

    ```sql
    COPY INTO books
    FROM 's3://lake-toronto/'
    CONNECTION = (
        ACCESS_KEY_ID = '<your-access-key-id>',
        SECRET_ACCESS_KEY = '<your-secret-access-key>'
    )
    PATTERN = '.*[.]parquet'
    FILE_FORMAT = (
        TYPE = 'PARQUET'
    );
    ```

2. ロードされたデータを確認します。

```sql
SELECT * FROM books;

---
title                       |author             |date|
----------------------------+-------------------+----+
Transaction Processing      |Jim Gray           |1992|
Readings in Database Systems|Michael Stonebraker|2004|
```