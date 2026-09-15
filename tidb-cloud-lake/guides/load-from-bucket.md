---
title: 从存储桶加载
summary: 当数据文件存储在对象存储存储桶（例如 Amazon S3）中时，可以使用 COPY INTO 命令将其直接加载到 {{{ .lake }}} 中。请注意，文件必须采用 {{{ .lake }}} 支持的格式，否则无法导入数据。有关 {{{ .lake }}} 支持的文件格式的更多信息，请参见 Input & Output File Formats。
---

# 从存储桶加载

当数据文件存储在对象存储存储桶（例如 Amazon S3）中时，可以使用 [COPY INTO](/tidb-cloud-lake/sql/copy-into-table.md) 命令将其直接加载到 {{{ .lake }}} 中。请注意，文件必须采用 {{{ .lake }}} 支持的格式，否则无法导入数据。有关 {{{ .lake }}} 支持的文件格式的更多信息，请参见 [输入与输出文件格式](/tidb-cloud-lake/sql/input-output-file-formats.md)。

![image](/media/tidb-cloud-lake/load-data-from-s3.jpeg)

本教程以 Amazon S3 存储桶为例，提供详细的分步指南，帮助你顺利完成从存储桶中的文件加载数据的过程。

## 教程：从 Amazon S3 存储桶加载 {#tutorial-loading-from-amazon-s3-bucket}

### 开始之前 {#before-you-begin}

开始之前，请确保你已完成以下任务：

1. 将示例文件 [books.parquet](https://lakesql-bin.tidbcloud.com/datasets/books.parquet) 下载并保存到本地文件夹中。该文件包含两条记录：

    ```text title='books.parquet'
    Transaction Processing,Jim Gray,1992
    Readings in Database Systems,Michael Stonebraker,2004
    ```

2. 在 Amazon S3 中创建一个存储桶，并将示例文件上传到该存储桶。具体操作请参考以下链接：

- 创建存储桶：<https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html>
- 上传对象：<https://docs.aws.amazon.com/AmazonS3/latest/userguide/upload-objects.html>

在本教程中，将在区域 **US East (Ohio)**（ID：us-east-2）中创建一个名为 **lake-toronto** 的存储桶。

### 步骤 1：创建目标表 {#step-1-create-target-table}

在 {{{ .lake }}} 中使用以下 SQL 语句创建表：

```sql
USE default;
CREATE TABLE books
(
    title VARCHAR,
    author VARCHAR,
    date VARCHAR
);
```

### 步骤 2：将数据复制到表中 {#step-2-copy-data-into-table}

1. 使用 [COPY INTO](/tidb-cloud-lake/sql/copy-into-table.md) 命令将数据加载到目标表中：

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

2. 检查已加载的数据：

```sql
SELECT * FROM books;

---
title                       |author             |date|
----------------------------+-------------------+----+
Transaction Processing      |Jim Gray           |1992|
Readings in Database Systems|Michael Stonebraker|2004|
```