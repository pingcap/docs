---
title: CREATE EXTERNAL TABLE
summary: `CREATE TABLE... CONNECTION = (...)` 语句用于创建表，并指定一个兼容 S3 的存储桶来存储数据，而不是使用默认的本地存储。
---

# CREATE EXTERNAL TABLE

`CREATE TABLE ... CONNECTION = (...)` 语句用于创建表，并指定一个兼容 S3 的存储桶来存储数据，而不是使用默认的本地存储。

随后，fuse table engine 表将存储在指定的兼容 S3 的存储桶中。

## 优势 {#benefits}

- 你可以自行决定表数据的存储位置。
- 利用高性能存储（如 [Amazon S3 Express One Zone](https://aws.amazon.com/s3/storage-classes/express-one-zone/)）来提升性能。

## 语法 {#syntax}

```sql
CREATE TABLE [IF NOT EXISTS] [db.]table_name (
    <column_name> <data_type> [NOT NULL | NULL] [{ DEFAULT <expr> }],
    <column_name> <data_type> [NOT NULL | NULL] [{ DEFAULT <expr> }],
    ...
)
's3://<bucket>/[<path>]'
CONNECTION = (
    ENDPOINT_URL = 'https://<endpoint-URL>'
    ACCESS_KEY_ID = '<your-access-key-ID>'
    SECRET_ACCESS_KEY = '<your-secret-access-key>'
    ENABLE_VIRTUAL_HOST_STYLE = 'true' | 'false'
)
|
CONNECTION = (
    CONNECTION_NAME = '<your-connection-name>'
);
```

连接参数：

| 参数                        | 说明                                                                                                                                                                                                                     | 必填       |
|-----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|
| `s3://<bucket>/[<path>]`    | 文件位于指定的外部位置（类 S3 存储桶）                                                                                                                                                                                   | YES        |
| ENDPOINT_URL                | 存储桶的 endpoint URL，必须以 `https://` 开头。                                                                                                                                                                          | Optional   |
| ACCESS_KEY_ID               | 用于连接 AWS S3 兼容对象存储的 access key ID。如果未提供，{{{ .lake }}} 将以匿名方式访问该存储桶。                                                                                                                      | Optional   |
| SECRET_ACCESS_KEY           | 用于连接 AWS S3 兼容对象存储的 secret access key。                                                                                                                                                                       | Optional   |
| ENABLE_VIRTUAL_HOST_STYLE   | 如果你使用虚拟主机方式来访问存储桶，请将其设置为 `"true"`。                                                                                                                                                              | Optional   |

关于 `CONNECTION_NAME` 的更多信息，请参见 [CREATE CONNECTION](/tidb-cloud-lake/sql/create-connection.md)

## 兼容 S3 的存储桶策略要求 {#s3-compatible-bucket-policy-requirements}

外部位置的 S3 存储桶必须通过 S3 bucket policy 授予以下权限：

**只读访问：**

- `s3:GetObject`：允许从存储桶中读取对象。
- `s3:ListBucket`：允许列出存储桶中的对象。
- `s3:ListBucketVersions`：允许列出存储桶中的对象版本。
- `s3:GetObjectVersion`：允许获取对象的特定版本。

**可写访问：**

- `s3:PutObject`：允许向存储桶写入对象。
- `s3:DeleteObject`：允许从存储桶删除对象。
- `s3:AbortMultipartUpload`：允许中止分段上传。
- `s3:DeleteObjectVersion`：允许删除对象的特定版本。

## 示例 {#examples}

在使用 `SHOW CREATE TABLE` 命令之前，你需要将 `hide_options_in_show_create_table` 变量设置为 `0`。

```sql
SET GLOBAL hide_options_in_show_create_table = 0;
```

### 使用外部位置创建表 {#create-a-table-with-external-location}

创建一个表，并将数据存储在外部位置，例如 Amazon S3：

```sql
-- Create a table named `mytable` and specify the location `s3://testbucket/admin/data/` for the data storage
CREATE TABLE mytable (
  a INT
)
's3://testbucket/admin/data/'
CONNECTION = (
  ACCESS_KEY_ID = '<your_aws_key_id>',
  SECRET_ACCESS_KEY = '<your_aws_secret_key>',
  ENDPOINT_URL = 'https://s3.amazonaws.com'
);

-- Show the table schema
SHOW CREATE TABLE mytable;

CREATE TABLE mytable (
  a INT NULL
)
ENGINE = FUSE
COMPRESSION = 'zstd'
STORAGE_FORMAT = 'parquet'
LOCATION = 's3 | bucket=testbucket,root=/admin/data/,endpoint=https://s3.amazonaws.com';
```

### 使用连接创建表 {#create-a-table-using-a-connection}

或者，你也可以先创建一个连接，再使用该连接创建表：

```sql
-- Create a connection named `s3_connection` for the S3 credentials
CREATE CONNECTION s3_connection
  STORAGE_TYPE = 's3'
  ACCESS_KEY_ID = '<your-access-key-id>'
  SECRET_ACCESS_KEY = '<your-secret-access-key>';

CREATE TABLE mytable (
  a INT
)
's3://testbucket/admin/data/'
CONNECTION = (
  CONNECTION_NAME = 's3_connection'
);

-- Show the table schema
SHOW CREATE TABLE mytable;

CREATE TABLE mytable (
  a INT NULL
)
ENGINE = FUSE
COMPRESSION = 'zstd'
STORAGE_FORMAT = 'parquet'
LOCATION = 's3 | bucket=testbucket,root=/admin/data/,endpoint=https://s3.amazonaws.com';
```