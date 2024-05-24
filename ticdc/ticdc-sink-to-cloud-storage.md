---
title: Replicate Data to Storage Services
summary: Learn how to replicate data to storage services using TiCDC, and learn about the storage path of the replicated data.
---

# Replicate Data to Storage Services

Starting from TiDB v6.5.0, TiCDC supports saving row change events to storage services, including Amazon S3, GCS, Azure Blob Storage, and NFS. This document describes how to create a changefeed that replicates incremental data to such storage services using TiCDC, and how data is stored. The organization of this document is as follows:

- [How to replicate data to storage services](#replicate-change-data-to-storage-services).
- [How data is stored in storage services](#storage-path-structure).

## Replicate change data to storage services

Run the following command to create a changefeed task:

```shell
cdc cli changefeed create \
    --server=http://10.0.10.25:8300 \
    --sink-uri="s3://logbucket/storage_test?protocol=canal-json" \
    --changefeed-id="simple-replication-task"
```

The output is as follows:

```shell
Info: {"upstream_id":7171388873935111376,"namespace":"default","id":"simple-replication-task","sink_uri":"s3://logbucket/storage_test?protocol=canal-json","create_time":"2024-05-24T18:52:05.566016967+08:00","start_ts":437706850431664129,"engine":"unified","config":{"case_sensitive":false,"enable_old_value":true,"force_replicate":false,"ignore_ineligible_table":false,"check_gc_safe_point":true,"enable_sync_point":false,"sync_point_interval":600000000000,"sync_point_retention":86400000000000,"filter":{"rules":["*.*"],"event_filters":null},"mounter":{"worker_num":16},"sink":{"protocol":"canal-json","schema_registry":"","csv":{"delimiter":",","quote":"\"","null":"\\N","include_commit_ts":false},"column_selectors":null,"transaction_atomicity":"none","encoder_concurrency":16,"terminator":"\r\n","date_separator":"none","enable_partition_separator":false},"consistent":{"level":"none","max_log_size":64,"flush_interval":2000,"storage":""}},"state":"normal","creator_version":"v8.1.0"}
```

- `--server`: The address of any TiCDC server in the TiCDC cluster.
- `--changefeed-id`: The ID of the changefeed. The format must match the `^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$` regular expression. If this ID is not specified, TiCDC automatically generates a UUID (the version 4 format) as the ID.
- `--sink-uri`: The downstream address of the changefeed. For details, see [Configure sink URI](#configure-sink-uri).
- `--start-ts`: The starting TSO of the changefeed. TiCDC starts pulling data from this TSO. The default value is the current time.
- `--target-ts`: The ending TSO of the changefeed. TiCDC stops pulling data until this TSO. The default value is empty, which means that TiCDC does not automatically stop pulling data.
- `--config`: The configuration file of the changefeed. For details, see [TiCDC changefeed configuration parameters](/ticdc/ticdc-changefeed-config.md).

## Configure sink URI

This section describes how to configure Sink URI for storage services, including Amazon S3, GCS, Azure Blob Storage, and NFS. Sink URI is used to specify the connection information of the TiCDC target system. The format is as follows:

```shell
[scheme]://[host]/[path]?[query_parameters]
```

For `[query_parameters]` in the URI, the following parameters can be configured:

| Parameter | Description | Default value | Value range |
| :---------| :---------- | :------------ | :---------- |
| `worker-count` | Concurrency for saving data changes to cloud storage in the downstream.  | `16` | `[1, 512]` |
| `flush-interval` | Interval for saving data changes to cloud storage in the downstream.   | `5s` | `[2s, 10m]` |
| `file-size` | A data change file is stored to cloud storage if the number of bytes exceeds the value of this parameter. | `67108864` | `[1048576, 536870912]` |
| `protocol` | The protocol format of the messages sent to the downstream.  | N/A |  `canal-json` and `csv` |
| `enable-tidb-extension` | When `protocol` is set to `canal-json` and `enable-tidb-extension` is set to `true`, TiCDC sends [WATERMARK events](/ticdc/ticdc-canal-json.md#watermark-event) and adds the [TiDB extension field](/ticdc/ticdc-canal-json.md#tidb-extension-field) to Canal-JSON messages. | `false` | `false` and `true` |

> **Note:**
>
> Data change files are saved to the downstream when either `flush-interval` or `file-size` meets the requirements.
> The `protocol` parameter is mandatory. If TiCDC does not receive this parameter when creating a changefeed, the `CDC:ErrSinkUnknownProtocol` error is returned.

### Configure sink URI for external storage

When storing data in a cloud storage system, you need to set different authentication parameters depending on the cloud service provider. This section describes the authentication methods when using Amazon S3, Google Cloud Storage (GCS), and Azure Blob Storage, and how to configure accounts to access the corresponding storage services.

<SimpleTab groupId="storage">
<div label="Amazon S3" value="amazon">

The following is an example configuration for Amazon S3:

```shell
--sink-uri="s3://bucket/prefix?protocol=canal-json"
```

Before replicating data, you need to set appropriate access permissions for the directory in Amazon S3:

- Minimum permissions required by TiCDC: `s3:ListBucket`, `s3:PutObject`, and `s3:GetObject`.
- If the changefeed configuration item `sink.cloud-storage-config.flush-concurrency` is greater than 1, which means parallel uploading of single files is enabled, you need to additionally add permissions related to [ListParts](https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListParts.html):
    - `s3:AbortMultipartUpload`
    - `s3:ListMultipartUploadParts`
    - `s3:ListBucketMultipartUploads`

If you have not created a replication data storage directory, refer to [Create a bucket](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-bucket.html) to create an S3 bucket in the specified region. If necessary, you can also create a folder in the bucket by referring to [Organize objects in the Amazon S3 console by using folders](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-folder.html).

You can configure an account to access Amazon S3 in the following ways:

- Method 1: Specify the access key

    If you specify an access key and a secret access key, authentication is performed according to them. In addition to specifying the key in the URI, the following methods are supported:

    - TiCDC reads the `$AWS_ACCESS_KEY_ID` and `$AWS_SECRET_ACCESS_KEY` environment variables.
    - TiCDC reads the `$AWS_ACCESS_KEY` and `$AWS_SECRET_KEY` environment variables.
    - TiCDC reads the shared credentials file in the path specified by the `$AWS_SHARED_CREDENTIALS_FILE` environment variable.
    - TiCDC reads the shared credentials file in the `~/.aws/credentials` path.

- Method 2: Access based on an IAM role

    Associate an [IAM role with configured permissions to access Amazon S3](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2.html) to the EC2 instance running the TiCDC server. After successful setup, TiCDC can directly access the corresponding directories in Amazon S3 without additional settings.

</div>
<div label="GCS" value="gcs">

The following is an example configuration for GCS:

```shell
--sink-uri="gcs://bucket/prefix?protocol=canal-json"
```

You can configure the account used to access GCS by specifying an access key. Authentication is performed according to the specified `credentials-file`. In addition to specifying the key in the URI, the following methods are supported:

- TiCDC reads the file in the path specified by the `$GOOGLE_APPLICATION_CREDENTIALS` environment variable.
- TiCDC reads the file `~/.config/gcloud/application_default_credentials.json`.
- TiCDC obtains credentials from the metadata server when the cluster is running in GCE or GAE.

</div>
<div label="Azure Blob Storage" value="azure">

The following is an example configuration for Azure Blob Storage:

```shell
--sink-uri="azure://bucket/prefix?protocol=canal-json"
```

You can configure an account to access Azure Blob Storage in the following ways:

- Method 1: Specify a shared access signature

    If you configure `account-name` and `sas-token` in the URI, the storage account name and shared access signature token specified by this parameter are used. Because the shared access signature token has the `&` character, you need to encode it as `%26` before adding it to the URI. You can also directly encode the entire `sas-token` using percent-encoding.

- Method 2: Specify the access key

    If you configure `account-name` and `account-key` in the URI, the storage account name and key specified by this parameter are used. In addition to specifying the key file in the URI, TiCDC can also read the key from the environment variable `$AZURE_STORAGE_KEY`.

- Method 3: Use Azure AD to restore the backup

    Configure the environment variables `$AZURE_CLIENT_ID`, `$AZURE_TENANT_ID`, and `$AZURE_CLIENT_SECRET`.

</div>
</SimpleTab>

> **Tip:**
>
> For more information about the URI parameters of Amazon S3, GCS, and Azure Blob Storage in TiCDC, see [URI Formats of External Storage Services](/external-storage-uri.md).

### Configure sink URI for NFS

The following is an example configuration for NFS:

```shell
--sink-uri="file:///my-directory/prefix?protocol=canal-json"
```

## Storage path structure

This section describes the storage path structure of data change records, metadata, and DDL events.

### Data change records

Data change records are saved to the following path:

```shell
{scheme}://{prefix}/{schema}/{table}/{table-version-separator}/{partition-separator}/{date-separator}/CDC{num}.{extension}
```

- `scheme`: specifies the storage type, for example, `s3`, `gcs`, `azure`, or `file`.
- `prefix`: specifies the user-defined parent directory, for example, <code>s3://**bucket/bbb/ccc**</code>.
- `schema`: specifies the schema name, for example, <code>s3://bucket/bbb/ccc/**test**</code>.
- `table`: specifies the table name, for example, <code>s3://bucket/bbb/ccc/test/**table1**</code>.
- `table-version-separator`: specifies the separator that separates the path by the table version, for example, <code>s3://bucket/bbb/ccc/test/table1/**9999**</code>.
- `partition-separator`: specifies the separator that separates the path by the table partition, for example, <code>s3://bucket/bbb/ccc/test/table1/9999/**20**</code>.
- `date-separator`: classifies the files by the transaction commit date. The default value is `day`. Value options are:
    - `none`: no `date-separator`. For example, all files with `test.table1` version being `9999` are saved to `s3://bucket/bbb/ccc/test/table1/9999`.
    - `year`: the separator is the year of the transaction commit date, for example, <code>s3://bucket/bbb/ccc/test/table1/9999/**2022**</code>.
    - `month`: the separator is the year and month of the transaction commit date, for example, <code>s3://bucket/bbb/ccc/test/table1/9999/**2022-01**</code>.
    - `day`: the separator is the year, month, and day of the transaction commit date, for example, <code>s3://bucket/bbb/ccc/test/table1/9999/**2022-01-02**</code>.
- `num`: saves the serial number of the file that records the data change, for example, <code>s3://bucket/bbb/ccc/test/table1/9999/2022-01-02/CDC**000005**.csv</code>.
- `extension`: specifies the extension of the file. TiDB v6.5.0 supports the CSV and Canal-JSON formats.

> **Note:**
>
> The table version changes only after a DDL operation is performed on the upstream table, and the new table version is the TSO when the upstream TiDB completes the execution of the DDL. However, the change of the table version does not mean the change of the table schema. For example, adding a comment to a column does not cause the schema file content to change.

### Index files

An index file is used to prevent written data from being overwritten by mistake. It is stored in the same path as the data change records.

```shell
{scheme}://{prefix}/{schema}/{table}/{table-version-separator}/{partition-separator}/{date-separator}/meta/CDC.index
```

The index file records the largest file name used in the current directory. For example:

```
CDC000005.csv
```

In this example, the files `CDC000001.csv` through `CDC000004.csv` in this directory are occupied. When a table scheduling or node restart occurs in the TiCDC cluster, the new node reads the index file and determines if `CDC000005.csv` is occupied. If it is not occupied, the new node writes the file starting from `CDC000005.csv`. If it is occupied, it starts writing from `CDC000006.csv`, which prevents overwriting data written by other nodes.

### Metadata

Metadata is saved in the following path:

```shell
{protocol}://{prefix}/metadata
```

Metadata is a JSON-formatted file, for example:

```json
{
    "checkpoint-ts":433305438660591626
}
```

- `checkpoint-ts`: Transactions with `commit-ts` smaller than `checkpoint-ts` are written to the target storage in the downstream.

### DDL events

### DDL events at the table level

When a DDL event of an upstream table causes a table version change, TiCDC automatically does the following:

- Switches to a new path to write data change records. For example, when the version of `test.table1` changes to `441349361156227074`, TiCDC changes to the `s3://bucket/bbb/ccc/test/table1/441349361156227074/2022-01-02/` path to write data change records.
- Generates a schema file in the following path to store the table schema information:

    ```shell
    {scheme}://{prefix}/{schema}/{table}/meta/schema_{table-version}_{hash}.json
    ```

Taking the `schema_441349361156227074_3131721815.json` schema file as an example, the table schema information in this file is as follows:

```json
{
    "Table":"table1",
    "Schema":"test",
    "Version":1,
    "TableVersion":441349361156227074,
    "Query":"ALTER TABLE test.table1 ADD OfficeLocation blob(20)",
    "Type":5,
    "TableColumns":[
        {
            "ColumnName":"Id",
            "ColumnType":"INT",
            "ColumnNullable":"false",
            "ColumnIsPk":"true"
        },
        {
            "ColumnName":"LastName",
            "ColumnType":"CHAR",
            "ColumnLength":"20"
        },
        {
            "ColumnName":"FirstName",
            "ColumnType":"VARCHAR",
            "ColumnLength":"30"
        },
        {
            "ColumnName":"HireDate",
            "ColumnType":"DATETIME"
        },
        {
            "ColumnName":"OfficeLocation",
            "ColumnType":"BLOB",
            "ColumnLength":"20"
        }
    ],
    "TableColumnsTotal":"5"
}
```

- `Table`: Table name.
- `Schema`: Schema name.
- `Version`: Protocol version of the storage sink.
- `TableVersion`: Table version.
- `Query`: DDL statement.
- `Type`: DDL type.
- `TableColumns`: An array of one or more maps, each of which describes a column in the source table.
    - `ColumnName`: Column name.
    - `ColumnType`: Column type. For details, see [Data type](#data-type).
    - `ColumnLength`: Column length. For details, see [Data type](#data-type).
    - `ColumnPrecision`: Column precision. For details, see [Data type](#data-type).
    - `ColumnScale`: The number of digits following the decimal point (the scale). For details, see [Data type](#data-type).
    - `ColumnNullable`: The column can be NULL when the value of this option is `true`.
    - `ColumnIsPk`: The column is part of the primary key when the value of this option is `true`.
- `TableColumnsTotal`: The size of the `TableColumns` array.

### DDL events at the database level

When a database-level DDL event is performed in the upstream database, TiCDC automatically generates a schema file in the following path to store the database schema information:

```shell
{scheme}://{prefix}/{schema}/meta/schema_{table-version}_{hash}.json
```

Taking the `schema_441349361156227000_3131721815.json` schema file as an example, the database schema information in this file is as follows:

```json
{
  "Table": "",
  "Schema": "schema1",
  "Version": 1,
  "TableVersion": 441349361156227000,
  "Query": "CREATE DATABASE `schema1`",
  "Type": 1,
  "TableColumns": null,
  "TableColumnsTotal": 0
}
```

### Data type

This section describes the data types used in the `schema_{table-version}_{hash}.json` file (hereafter referred to as "schema file" in the following sections). The data types are defined as `T(M[, D])`. For details, see [Data Types](/data-type-overview.md).

#### Integer types

Integer types in TiDB are defined as `IT[(M)] [UNSIGNED]`, where

- `IT` is the integer type, which can be `TINYINT`, `SMALLINT`, `MEDIUMINT`, `INT`, `BIGINT`, or `BIT`.
- `M` is the display width of the type.

Integer types are defined as follows in the schema file:

```json
{
    "ColumnName":"COL1",
    "ColumnType":"{IT} [UNSIGNED]",
    "ColumnPrecision":"{M}"
}
```

#### Decimal types

Decimal types in TiDB are defined as `DT[(M,D)][UNSIGNED]`, where

- `DT` is the floating-point type, which can be `FLOAT`, `DOUBLE`, `DECIMAL`, or `NUMERIC`.
- `M` is the precision of the data type, or the total number of digits.
- `D` is the number of digits following the decimal point.

Decimal types are defined as follows in the schema file:

```json
{
    "ColumnName":"COL1",
    "ColumnType":"{DT} [UNSIGNED]",
    "ColumnPrecision":"{M}",
    "ColumnScale":"{D}"
}
```

#### Date and time types

Date types in TiDB are defined as `DT`, where

- `DT` is the date type, which can be `DATE` or `YEAR`.

The date types are defined as follows in the schema file:

```json
{
    "ColumnName":"COL1",
    "ColumnType":"{DT}"
}
```

The time types in TiDB are defined as `TT[(M)]`, where

- `TT` is the time type, which can be `TIME`, `DATETIME`, or `TIMESTAMP`.
- `M` is the precision of seconds in the range from 0 to 6.

The time types are defined as follows in the schema file:

```json
{
    "ColumnName":"COL1",
    "ColumnType":"{TT}",
    "ColumnScale":"{M}"
}
```

#### String types

The string types in TiDB are defined as `ST[(M)]`, where

- `ST` is the string type, which can be `CHAR`, `VARCHAR`, `TEXT`, `BINARY`, `BLOB`, or `JSON`.
- `M` is the maximum length of the string.

The string types are defined as follows in the schema file:

```json
{
    "ColumnName":"COL1",
    "ColumnType":"{ST}",
    "ColumnLength":"{M}"
}
```

#### Enum and Set types

The Enum and Set types are defined as follows in the schema file:

```json
{
    "ColumnName":"COL1",
    "ColumnType":"{ENUM/SET}",
}
```
