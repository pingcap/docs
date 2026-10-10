---
title: stage からのロード
summary: "{{{ .lake }}} では、user stage または internal/external stage にアップロードされたファイルからデータを簡単にインポートできます。これを行うには、まず LakeSQL を使用してファイルを stage にアップロードし、その後 [COPY INTO] コマンドを使用して stage 上のファイルからデータをロードできます。ファイルは {{{ .lake }}} がサポートする形式である必要があり、そうでない場合はデータをインポートできません。{{{ .lake }}} がサポートするファイル形式の詳細については、Input & Output File Formats を参照してください。"
---

# stage からのロード

{{{ .lake }}} では、user stage または internal/external stage にアップロードされたファイルからデータを簡単にインポートできます。これを行うには、まず [LakeSQL](/tidb-cloud-lake/guides/connect-using-lakesql.md) を使用してファイルを stage にアップロードし、その後 [COPY INTO](/tidb-cloud-lake/sql/copy-into-table.md) コマンドを使用して stage 上のファイルからデータをロードできます。ファイルは {{{ .lake }}} がサポートする形式である必要があり、そうでない場合はデータをインポートできません。{{{ .lake }}} がサポートするファイル形式の詳細については、[入出力ファイル形式](/tidb-cloud-lake/sql/input-output-file-formats.md) を参照してください。

![image](/media/tidb-cloud-lake/load-data-from-stage.png)

以下のチュートリアルでは、stage 内のファイルからデータをロードする手順を、ステップごとに詳しく説明します。

## 始める前に {#before-you-begin}

開始する前に、次のタスクを完了していることを確認してください。

- サンプルファイル [books.parquet](https://lakesql-bin.tidbcloud.com/datasets/books.parquet) をダウンロードし、ローカルフォルダに保存します。このファイルには 2 件のレコードが含まれています。

```text
Transaction Processing,Jim Gray,1992
Readings in Database Systems,Michael Stonebraker,2004
```

- {{{ .lake }}} で次の SQL 文を使用してテーブルを作成します。

```sql
USE default;
CREATE TABLE books
(
    title VARCHAR,
    author VARCHAR,
    date VARCHAR
);
```

## チュートリアル 1: User Stage からのロード {#tutorial-1-loading-from-user-stage}

このチュートリアルでは、サンプルファイルを user stage にアップロードし、stage 上のファイルから {{{ .lake }}} にデータをロードする方法を説明します。

### ステップ 1. サンプルファイルをアップロードする {#step-1-upload-sample-file}

1. [LakeSQL](/tidb-cloud-lake/guides/connect-using-lakesql.md) を使用してサンプルファイルをアップロードします。

    ```sql
    root@localhost:8000/default> PUT fs:///Users/eric/Documents/books.parquet @~

    ┌───────────────────────────────────────────────┐
    │                 file                │  status │
    │                String               │  String │
    ├─────────────────────────────────────┼─────────┤
    │ /Users/eric/Documents/books.parquet │ SUCCESS │
    └───────────────────────────────────────────────┘
    ```

2. stage 上のファイルを確認します。

```sql
LIST @~;

name         |size|md5                               |last_modified                |creator|
-------------+----+----------------------------------+-----------------------------+-------+
books.parquet| 998|"88432bf90aadb79073682988b39d461c"|2023-06-27 16:03:51.000 +0000|       |
```

### ステップ 2. テーブルにデータをコピーする {#step-2-copy-data-into-table}

1. [COPY INTO](/tidb-cloud-lake/sql/copy-into-table.md) コマンドを使用して、対象テーブルにデータをロードします。

    ```sql
    COPY INTO books FROM @~ files=('books.parquet') FILE_FORMAT = (TYPE = PARQUET);
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

## チュートリアル 2: Internal Stage からのロード {#tutorial-2-loading-from-internal-stage}

このチュートリアルでは、サンプルファイルを internal stage にアップロードし、stage 上のファイルから {{{ .lake }}} にデータをロードする方法を説明します。

### ステップ 1. Internal Stage を作成する {#step-1-create-an-internal-stage}

1. [CREATE STAGE](/tidb-cloud-lake/sql/create-stage.md) コマンドを使用して internal stage を作成します。

    ```sql
    CREATE STAGE my_internal_stage;
    ```

2. 作成した stage を確認します。

    ```sql
    SHOW STAGES;

    ╭────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
    │        name       │ stage_type │   storage_type   │        url       │     endpoint     │ has_credentials │   has_encryption_key  │   storage_params  │  file_format_options │      creator     │  created_on │ comment │       owner      │
    │       String      │   String   │ Nullable(String) │ Nullable(String) │ Nullable(String) │     Boolean     │        Boolean        │ Nullable(Variant) │        Variant       │ Nullable(String) │  Timestamp  │  String │ Nullable(String) │
    ├───────────────────┼────────────┼──────────────────┼──────────────────┼──────────────────┼─────────────────┼───────────────────────┼───────────────────┼──────────────────────┼──────────────────┼─────────────┼─────────┼──────────────────┤
    │ my_internal_stage │ Internal   │ NULL             │ NULL             │ NULL             │ false           │ false                 │ NULL              │ {"compression":"Zst… │ 'root'@'%'       │ 2026-06-16  │         │ account_admin    │
    │                   │            │                  │                  │                  │                 │                       │                   │                      │                  │ 22:21:19…   │         │                  │
    ╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
    ```

### ステップ 2. サンプルファイルをアップロードする {#step-2-upload-sample-file}

1. [LakeSQL](/tidb-cloud-lake/guides/connect-using-lakesql.md) を使用してサンプルファイルをアップロードします。

    ```sql
    root@localhost:8000/default> CREATE STAGE my_internal_stage;

    root@localhost:8000/default> PUT fs:///Users/eric/Documents/books.parquet @my_internal_stage

    ┌───────────────────────────────────────────────┐
    │                 file                │  status │
    │                String               │  String │
    ├─────────────────────────────────────┼─────────┤
    │ /Users/eric/Documents/books.parquet │ SUCCESS │
    └───────────────────────────────────────────────┘
    ```

2. stage 上のファイルを確認します。

```sql
LIST @my_internal_stage;

name                               |size  |md5                               |last_modified                |creator|
-----------------------------------+------+----------------------------------+-----------------------------+-------+
books.parquet                      |   998|"88432bf90aadb79073682988b39d461c"|2023-06-28 02:32:15.000 +0000|       |
```

### ステップ 3. テーブルにデータをコピーする {#step-3-copy-data-into-table}

1. [COPY INTO](/tidb-cloud-lake/sql/copy-into-table.md) コマンドを使用して、対象テーブルにデータをロードします。

    ```sql
    COPY INTO books
    FROM @my_internal_stage
    FILES = ('books.parquet')
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

## チュートリアル 3: External Stage からのロード {#tutorial-3-loading-from-external-stage}

このチュートリアルでは、サンプルファイルを external stage にアップロードし、stage 上のファイルから {{{ .lake }}} にデータをロードする方法を説明します。

### ステップ 1. External Stage を作成する {#step-1-create-an-external-stage}

1. [CREATE STAGE](/tidb-cloud-lake/sql/create-stage.md) コマンドを使用して external stage を作成します。

    ```sql
    CREATE STAGE my_external_stage
        URL = 's3://lake'
        CONNECTION = (
            ENDPOINT_URL = 'http://127.0.0.1:9000',
            ACCESS_KEY_ID = 'ROOTUSER',
            SECRET_ACCESS_KEY = 'CHANGEME123'
        );
    ```

2. 作成した stage を確認します。

    ```sql
    SHOW STAGES;

    name             |stage_type|creator           |comment|
    -----------------+----------+------------------+-------+
    my_external_stage|External  |'root'@'%'|       |
    ```

### Step 2. サンプルファイルをアップロードする {#step-2-upload-sample-file}

1. [LakeSQL](/tidb-cloud-lake/guides/connect-using-lakesql.md) を使用してサンプルファイルをアップロードします。

    ```sql
    root@localhost:8000/default> PUT fs:///Users/eric/Documents/books.parquet @my_external_stage

    ┌───────────────────────────────────────────────┐
    │                 file                │  status │
    │                String               │  String │
    ├─────────────────────────────────────┼─────────┤
    │ /Users/eric/Documents/books.parquet │ SUCCESS │
    └───────────────────────────────────────────────┘
    ```

2. stage に配置されたファイルを確認します。

    ```sql
    LIST @my_external_stage;

    name         |size|md5                               |last_modified                |creator|
    -------------+----+----------------------------------+-----------------------------+-------+
    books.parquet| 998|"88432bf90aadb79073682988b39d461c"|2023-06-28 04:13:15.178 +0000|       |
    ```

### Step 3. テーブルにデータをコピーする {#step-3-copy-data-into-table}

1. [COPY INTO](/tidb-cloud-lake/sql/copy-into-table.md) コマンドを使用して、対象テーブルにデータをロード (load) します。

    ```sql
    COPY INTO books
    FROM @my_external_stage
    FILES = ('books.parquet')
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