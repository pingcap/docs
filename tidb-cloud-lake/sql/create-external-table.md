---
title: CREATE EXTERNAL TABLE
sidebar_position: 2
---

The `CREATE TABLE ... CONNECTION = (...)` statement creates a table and specifies an S3-compatible storage bucket for data storage instead of using the default local storage.

Then the fuse table engine table will be stored in the specified S3-compatible bucket.

## Benefits

- You can determine the storage location of the table data.
- Leverage high-performance storage like [Amazon S3 Express One Zone](https://aws.amazon.com/s3/storage-classes/express-one-zone/), to improve performance.

## Syntax

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

Connection parameters:

| Parameter                   | Description                                                                                                                                                                                                              | Required   |
|-----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|
| `s3://<bucket>/[<path>]`    | Files are in the specified external location (S3-like bucket)                                                                                                                                                            | YES        |
| ENDPOINT_URL              	 | The bucket endpoint URL starting with "https://". To use a URL starting with "http://", set `allow_insecure` to `true` in the [storage] block of the file `databend-query-node.toml`.                                  	 | Optional 	 |
| ACCESS_KEY_ID             	 | Your access key ID for connecting the AWS S3 compatible object storage. If not provided, Databend will access the bucket anonymously.    	                                                                               | Optional 	 |
| SECRET_ACCESS_KEY         	 | Your secret access key for connecting the AWS S3 compatible object storage. 	                                                                                                                                            | Optional 	 |
| ENABLE_VIRTUAL_HOST_STYLE 	 | If you use virtual hosting to address the bucket, set it to "true".                               	                                                                                                                      | Optional 	 |

For more information on `CONNECTION_NAME`, see [CREATE CONNECTION](../13-connection/create-connection.md)

## S3-compatible Bucket Policy Requirements

The external location S3 bucket must have the following permissions granted through an S3 bucket policy:

**Read-only Access:**
- `s3:GetObject`: Allows reading objects from the bucket.
- `s3:ListBucket`: Allows listing objects in the bucket.
- `s3:ListBucketVersions`: Allows listing object versions in the bucket.
- `s3:GetObjectVersion`: Allows retrieving a specific version of an object.

**Writable Access:**
- `s3:PutObject`: Allows writing objects to the bucket.
- `s3:DeleteObject`: Allows deleting objects from the bucket.
- `s3:AbortMultipartUpload`: Allows aborting multipart uploads.
- `s3:DeleteObjectVersion`: Allows deleting a specific version of an object.
:::

## Examples

:::info

Before using the `SHOW CREATE TABLE` command, you need to set the `hide_options_in_show_create_table` variable to `0`.
```sql
SET GLOBAL hide_options_in_show_create_table = 0;
```
:::

### Create a Table with External Location

Create a table with data stored on an external location, such as Amazon S3:

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

### Create a Table Using a Connection

Or you can create a connection and use it to create a table:
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
