---
title: CREATE EXTERNAL TABLE
summary: `CREATE TABLE... CONNECTION = (...)` ステートメントは、デフォルトのローカルストレージを使用する代わりに、データ保存先として S3 互換ストレージのバケットを指定してテーブルを作成します。
---

# CREATE EXTERNAL TABLE

`CREATE TABLE ... CONNECTION = (...)` ステートメントは、デフォルトのローカルストレージを使用する代わりに、データ保存先として S3 互換ストレージのバケットを指定してテーブルを作成します。

その後、fuse テーブルエンジンのテーブルは、指定した S3 互換バケットに保存されます。

## 利点 {#benefits}

- テーブルデータの保存場所を決定できます。
- [Amazon S3 Express One Zone](https://aws.amazon.com/s3/storage-classes/express-one-zone/) のような高性能ストレージを活用して、パフォーマンスを向上できます。

## 構文 {#syntax}

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

接続パラメータ:

| パラメータ                  | 説明                                                                                                                                                                                                                     | 必須       |
|-----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|
| `s3://<bucket>/[<path>]`    | ファイルが指定された外部ロケーション（S3 互換バケット）に存在します                                                                                                                                                      | YES        |
| ENDPOINT_URL                | `https://` で始まるバケットのエンドポイント URL。                                                                                                                                                                        | Optional   |
| ACCESS_KEY_ID               | AWS S3 互換オブジェクトストレージに接続するための access key ID です。指定しない場合、{{{ .lake }}} は匿名でバケットにアクセスします。                                                                                 | Optional   |
| SECRET_ACCESS_KEY           | AWS S3 互換オブジェクトストレージに接続するための secret access key です。                                                                                                                                               | Optional   |
| ENABLE_VIRTUAL_HOST_STYLE   | バケットのアドレッシングに virtual hosting を使用する場合は、`"true"` に設定します。                                                                                                                                     | Optional   |

`CONNECTION_NAME` の詳細については、[CREATE CONNECTION](/tidb-cloud-lake/sql/create-connection.md) を参照してください。

## S3 互換バケットポリシーの要件 {#s3-compatible-bucket-policy-requirements}

外部ロケーションの S3 バケットには、S3 バケットポリシーを通じて次の権限が付与されている必要があります。

**読み取り専用アクセス:**

- `s3:GetObject`: バケットからオブジェクトを読み取ることを許可します。
- `s3:ListBucket`: バケット内のオブジェクト一覧を取得することを許可します。
- `s3:ListBucketVersions`: バケット内のオブジェクトバージョン一覧を取得することを許可します。
- `s3:GetObjectVersion`: オブジェクトの特定バージョンを取得することを許可します。

**書き込み可能アクセス:**

- `s3:PutObject`: バケットにオブジェクトを書き込むことを許可します。
- `s3:DeleteObject`: バケットからオブジェクトを削除することを許可します。
- `s3:AbortMultipartUpload`: マルチパートアップロードを中止することを許可します。
- `s3:DeleteObjectVersion`: オブジェクトの特定バージョンを削除することを許可します。

## 例 {#examples}

`SHOW CREATE TABLE` コマンドを使用する前に、`hide_options_in_show_create_table` 変数を `0` に設定する必要があります。

```sql
SET GLOBAL hide_options_in_show_create_table = 0;
```

### 外部ロケーションを使用してテーブルを作成する {#create-a-table-with-external-location}

Amazon S3 などの外部ロケーションにデータを保存するテーブルを作成します。

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

### 接続を使用してテーブルを作成する {#create-a-table-using-a-connection}

または、接続を作成してそれを使ってテーブルを作成することもできます。

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