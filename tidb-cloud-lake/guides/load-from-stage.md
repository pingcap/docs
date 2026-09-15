---
title: 从 Stage 加载
summary: "{{{ .lake }}} 使你能够轻松地从上传到用户 stage 或内部/外部 stage 的文件中导入数据。为此，你可以先使用 LakeSQL 将文件上传到 stage，然后使用 COPY INTO 命令从 stage 中的文件加载数据。请注意，文件必须采用 {{{ .lake }}} 支持的格式，否则无法导入数据。有关 {{{ .lake }}} 支持的文件格式的更多信息，请参见 Input & Output File Formats。"
---

# 从 Stage 加载

{{{ .lake }}} 使你能够轻松地从上传到用户 stage 或内部/外部 stage 的文件中导入数据。为此，你可以先使用 [LakeSQL](/tidb-cloud-lake/guides/connect-using-lakesql.md) 将文件上传到 stage，然后使用 [COPY INTO](/tidb-cloud-lake/sql/copy-into-table.md) 命令从 stage 中的文件加载数据。请注意，文件必须采用 {{{ .lake }}} 支持的格式，否则无法导入数据。有关 {{{ .lake }}} 支持的文件格式的更多信息，请参见 [输入与输出文件格式](/tidb-cloud-lake/sql/input-output-file-formats.md)。

![image](/media/tidb-cloud-lake/load-data-from-stage.png)

以下教程提供了详细的分步指南，帮助你顺利完成从 stage 中的文件加载数据的过程。

## 开始之前 {#before-you-begin}

开始之前，请确保你已完成以下任务：

- 下载示例文件 [books.parquet](https://lakesql-bin.tidbcloud.com/datasets/books.parquet) 并将其保存到本地文件夹中。该文件包含两条记录：

```text
Transaction Processing,Jim Gray,1992
Readings in Database Systems,Michael Stonebraker,2004
```

- 在 {{{ .lake }}} 中使用以下 SQL 语句创建表：

```sql
USE default;
CREATE TABLE books
(
    title VARCHAR,
    author VARCHAR,
    date VARCHAR
);
```

## 教程 1：从用户 stage 加载 {#tutorial-1-loading-from-user-stage}

按照本教程将示例文件上传到用户 stage，并将 stage 中文件的数据加载到 {{{ .lake }}} 中。

### 步骤 1. 上传示例文件 {#step-1-upload-sample-file}

1. 使用 [LakeSQL](/tidb-cloud-lake/guides/connect-using-lakesql.md) 上传示例文件：

    ```sql
    root@localhost:8000/default> PUT fs:///Users/eric/Documents/books.parquet @~

    ┌───────────────────────────────────────────────┐
    │                 file                │  status │
    │                String               │  String │
    ├─────────────────────────────────────┼─────────┤
    │ /Users/eric/Documents/books.parquet │ SUCCESS │
    └───────────────────────────────────────────────┘
    ```

2. 验证 stage 中的文件：

```sql
LIST @~;

name         |size|md5                               |last_modified                |creator|
-------------+----+----------------------------------+-----------------------------+-------+
books.parquet| 998|"88432bf90aadb79073682988b39d461c"|2023-06-27 16:03:51.000 +0000|       |
```

### 步骤 2. 将数据复制到表中 {#step-2-copy-data-into-table}

1. 使用 [COPY INTO](/tidb-cloud-lake/sql/copy-into-table.md) 命令将数据加载到目标表中：

    ```sql
    COPY INTO books FROM @~ files=('books.parquet') FILE_FORMAT = (TYPE = PARQUET);
    ```

2. 验证已加载的数据：

```sql
SELECT * FROM books;

---
title                       |author             |date|
----------------------------+-------------------+----+
Transaction Processing      |Jim Gray           |1992|
Readings in Database Systems|Michael Stonebraker|2004|
```

## 教程 2：从内部 stage 加载 {#tutorial-2-loading-from-internal-stage}

按照本教程将示例文件上传到内部 stage，并将 stage 中文件的数据加载到 {{{ .lake }}} 中。

### 步骤 1. 创建内部 stage {#step-1-create-an-internal-stage}

1. 使用 [CREATE STAGE](/tidb-cloud-lake/sql/create-stage.md) 命令创建内部 stage：

    ```sql
    CREATE STAGE my_internal_stage;
    ```

2. 验证已创建的 stage：

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

### 步骤 2. 上传示例文件 {#step-2-upload-sample-file}

1. 使用 [LakeSQL](/tidb-cloud-lake/guides/connect-using-lakesql.md) 上传示例文件：

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

2. 验证 stage 中的文件：

```sql
LIST @my_internal_stage;

name                               |size  |md5                               |last_modified                |creator|
-----------------------------------+------+----------------------------------+-----------------------------+-------+
books.parquet                      |   998|"88432bf90aadb79073682988b39d461c"|2023-06-28 02:32:15.000 +0000|       |
```

### 步骤 3. 将数据复制到表中 {#step-3-copy-data-into-table}

1. 使用 [COPY INTO](/tidb-cloud-lake/sql/copy-into-table.md) 命令将数据加载到目标表中：

    ```sql
    COPY INTO books
    FROM @my_internal_stage
    FILES = ('books.parquet')
    FILE_FORMAT = (
        TYPE = 'PARQUET'
    );
    ```

2. 验证已加载的数据：

```sql
SELECT * FROM books;

---
title                       |author             |date|
----------------------------+-------------------+----+
Transaction Processing      |Jim Gray           |1992|
Readings in Database Systems|Michael Stonebraker|2004|
```

## 教程 3：从外部 stage 加载 {#tutorial-3-loading-from-external-stage}

按照本教程将示例文件上传到外部 stage，并将 stage 中文件的数据加载到 {{{ .lake }}} 中。

### 步骤 1. 创建外部 stage {#step-1-create-an-external-stage}

1. 使用 [CREATE STAGE](/tidb-cloud-lake/sql/create-stage.md) 命令创建外部 stage：

    ```sql
    CREATE STAGE my_external_stage
        URL = 's3://lake'
        CONNECTION = (
            ENDPOINT_URL = 'http://127.0.0.1:9000',
            ACCESS_KEY_ID = 'ROOTUSER',
            SECRET_ACCESS_KEY = 'CHANGEME123'
        );
    ```

2. 验证已创建的 stage：

    ```sql
    SHOW STAGES;

    name             |stage_type|creator           |comment|
    -----------------+----------+------------------+-------+
    my_external_stage|External  |'root'@'%'|       |
    ```

### 第 2 步：上传示例文件 {#step-2-upload-sample-file}

1. 使用 [LakeSQL](/tidb-cloud-lake/guides/connect-using-lakesql.md) 上传示例文件：

    ```sql
    root@localhost:8000/default> PUT fs:///Users/eric/Documents/books.parquet @my_external_stage

    ┌───────────────────────────────────────────────┐
    │                 file                │  status │
    │                String               │  String │
    ├─────────────────────────────────────┼─────────┤
    │ /Users/eric/Documents/books.parquet │ SUCCESS │
    └───────────────────────────────────────────────┘
    ```

2. 验证已暂存的文件：

    ```sql
    LIST @my_external_stage;

    name         |size|md5                               |last_modified                |creator|
    -------------+----+----------------------------------+-----------------------------+-------+
    books.parquet| 998|"88432bf90aadb79073682988b39d461c"|2023-06-28 04:13:15.178 +0000|       |
    ```

### 第 3 步：将数据复制到表中 {#step-3-copy-data-into-table}

1. 使用 [COPY INTO](/tidb-cloud-lake/sql/copy-into-table.md) 命令将数据加载到目标表中：

    ```sql
    COPY INTO books
    FROM @my_external_stage
    FILES = ('books.parquet')
    FILE_FORMAT = (
        TYPE = 'PARQUET'
    );
    ```

2. 验证已加载的数据：

```sql
SELECT * FROM books;

---
title                       |author             |date|
----------------------------+-------------------+----+
Transaction Processing      |Jim Gray           |1992|
Readings in Database Systems|Michael Stonebraker|2004|
```