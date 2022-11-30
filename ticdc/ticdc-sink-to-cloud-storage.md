---
title: Replicate Data to Cloud Storage
summary: Learn how to replicate data to cloud storage using TiCDC.
---

# Replicate Data to Cloud Storage

Since v6.5.0, TiCDC supports saving row change events to Amazon S3, Azure Blob Storage, and NFS. This document describes how to create a changefeed that replicates incremental data to these cloud storages using TiCDC.

## Create a changefeed

Run the following command to create a changefeed task:

```shell
cdc cli changefeed create \
    --server=http://10.0.10.25:8300 \
    --sink-uri="s3://logbucket/storage_test?access-key=minioadmin&secret-access-key=minioadmin&endpoint=http://10.2.7.69:9000&force-path-style=true&protocol=canal-json" \
    --changefeed-id="simple-replication-task"
```

```shell
Info: {"upstream_id":7171388873935111376,"namespace":"default","id":"simple-replication-task","sink_uri":"s3://logbucket/storage_test?access-key=minioadmin\u0026secret-access-key=minioadmin\u0026endpoint=http://10.2.7.69:9000\u0026force-path-style=true\u0026protocol=canal-json","create_time":"2022-11-29T18:52:05.566016967+08:00","start_ts":437706850431664129,"engine":"unified","config":{"case_sensitive":true,"enable_old_value":true,"force_replicate":false,"ignore_ineligible_table":false,"check_gc_safe_point":true,"enable_sync_point":false,"sync_point_interval":600000000000,"sync_point_retention":86400000000000,"filter":{"rules":["*.*"],"event_filters":null},"mounter":{"worker_num":16},"sink":{"protocol":"canal-json","schema_registry":"","csv":{"delimiter":",","quote":"\"","null":"\\N","include_commit_ts":false},"column_selectors":null,"transaction_atomicity":"none","encoder_concurrency":16,"terminator":"\r\n","date_separator":"none","enable_partition_separator":false},"consistent":{"level":"none","max_log_size":64,"flush_interval":2000,"storage":""}},"state":"normal","creator_version":"v6.5.0-master-dirty"}
```

- `--changefeed-id`: The ID of the changefeed. The format must match the `^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$` regular expression. If this ID is not specified, TiCDC automatically generates a UUID (the version 4 format) as the ID.
- `--sink-uri`: The downstream address of the changefeed. For details, see [Configure Cloud Storage in Sink URI](#configure-cloud-storage-in-sink-uri).
- `--start-ts`: The starting TSO of the changefeed. From this TSO, the TiCDC cluster starts pulling data. The default value is the current time.
- `--target-ts`: The ending TSO of the changefeed. To this TSO, the TiCDC cluster stops pulling data. The default value is empty, which means that TiCDC does not automatically stop pulling data.
- `--config`: The configuration file of the `changefeed`. For details, see [TiCDC changefeed configuration parameters](/ticdc/ticdc-changefeed-config.md)

## Configure cloud storage in sink URI

This section describes how to configure cloud storage, including `S3`, `Azure Blob Storage`, and `NFS`, in the changefeed URI.

### Configure S3 in sink URI

The following configuration saves row change events to Amazon S3:

```shell
--sink-uri="s3://my-bucket/prefix?region=us-west-2&worker-count=4"
```

The URI parameters of Amazon S3 in TiCDC are the same as the URL parameters of Amazon S3 in BR. For details, see [S3 URL parameters](/br/backup-and-restore-storages.md#s3-url-parameters).

### Configure Azure Blob Storage in sink URI

The following configuration saves row change events to Azure Blob Storage:

```shell
--sink-uri="azblob://my-bucket/prefix"
or
--sink-uri="azure://my-bucket/prefix"
```

The URI parameters of Azure Blob Storage in TiCDC are the same as the URL parameters of Azure Blob Storage in BR. For details, see [Azblob URL parameters](/br/backup-and-restore-storages.md#azblob-url-parameters).

### Configure NFS in sink URI

The following configuration saves row change events to NFS:

```
shell
--sink-uri="file:///my-directory/prefix"
```

Other parameters optional in the URI are as follows:

| Parameter         | Description                                             |
| :------------ | :------------------------------------------------ |
| `worker-count` | Concurrency for saving data changes to cloud storage in the downstream (optional, default value: `16`, value range: [`1`, `512`] |
| `flush-interval` | Interval for saving data changes to cloud storage in the downstream (optional, default value: `5s`, value range: [`2s`, `10s`] |
| `file-size` | A data change file is stored to cloud storage if its bytes exceed the value of this parameter (optional, default value: `67108864`, value range: [`67108864`, `536870912`]) |

> **Note:**
>
> Data change files are saved to cloud storage in the downstream when either `flush-interval` or `file-size` meets the requirements.

## Storage path structure

This section describes the storage path structure of data change records, metadata, and DDL events.

### Data change records

Data change records are saved to the following path:

```shell
{protocol}://{prefix}/{schema}/{table}/{table-version-separator}/{partition-separator}/{date-separator}/CDC{num}.{extension}
```

- `protocol`: specifies the data transmission protocol, or the storage type, for example, `s3://xxxxx`.
- `prefix`: specifies the user-defined parent directory, for example, `s3://bucket/bbb/ccc`.
- `schema`: specifies the schema name, for example, `s3://bucket/bbb/ccc/test`.
- `table`: specifies the table name, for example, `s3://bucket/bbb/ccc/test/table1`.
- `table-version-separator`: specifies the separator that separates the file path by the table version, for example, `s3://bucket/bbb/ccc/test/table1/9999`.
- `partition-separator`: specifies the separator that separates the file path by the table partition, for example, `s3://bucket/bbb/ccc/test/table1/9999/20`
- `date-separator`: classifies the files by the transaction commit date. Value options are:
    - none: no date-separator. For example, all files with `test.table1` version being `9999` are saved to `s3://bucket/bbb/ccc/test/table1/9999`.
    - `year`: the separator is the year a transaction is committed, for example, `s3://bucket/bbb/ccc/test/table1/9999/2022`.
    - `month`: the separator is the year and month a transaction is committed, for example,`s3://bucket/bbb/ccc/test/table1/9999/2022-01`.
    - `day`: the separator is the year, month, and day a transaction is committed, for example,`s3://bucket/bbb/ccc/test/table1/9999/2022-01-02`.
- `num`: saves the serial number of the file that records the data change, for example, `s3://bucket/bbb/ccc/test/table1/9999/2022-01-02/CDC000005.csv`.
- `extension`: specifies the extension of the file. TiDB v6.5.0 supports the CSV format only.

### Metadata

Metadata is saved in the following path:

```shell
{protocol}://{prefix}/metadata
```

Metadata is a JSON-formatted file, for example:

```shell
{
    "checkpoint-ts":433305438660591626
}
```

- checkpoint-ts: Transactions with `commit-ts` smaller than `checkpoint-ts` are written to the target storage in the downstream.

### DDL events

When DDL events cause the table version to change, TiCDC switches to the new path to write data change records. For example, when the version of `test.table1` changes from `9999` to `10000`, data will be written to the path `s3://bucket/bbb/ccc/test/table1/10000/2022-01-02/CDC000001.csv`. In addition, when DDL events occur, TiCDC generates a `schema.json` file to save the table structure information.

Table structure information is saved in the following path:

```shell
{protocol}://{prefix}/{schema}/{table}/{table-version-separator}/schema.json
```

The following is a `schema.json` file:

```shell
{
    "Table":"employee",
    "Schema":"hr",
    "Version":123123,
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
- `Version`: Table version.
- `TableColumns`: An array of one or more maps, each of which describes a column in the source table.
    - `ColumnName`: Column name.
    - `ColumnType`: Column type. For details, see [Data type](#data-type).
    - `ColumnLength`: Column length. For details, see [Data type](#data-type).
    - `ColumnPrecision`: Column precision. For details, see [Data type](#data-type).
    - `ColumnScale`: The number of digits following the decimal point (the scale). For details, see [Data type](#data-type).
    - `ColumnNullable`: The column can be null when the value of this option is `true`.
    - `ColumnIsPk`: The column is part of the primary key when the value of this option is `true`.
- `TableColumnsTotal`: The size of the `TableColumns` array.

### Data type

Data type is defined as `T(M[, D])`. For details, see [Data Types](/data-type-overview.md).

#### Integer types

Integer types in TiDB are defined as `IT[(M)] [UNSIGNED]`, where

- `IT` is the integer type, which can be `TINYINT`, `SMALLINT`, `MEDIUMINT`, `INT`, `BIGINT`, or `BIT`.
- `M` is the display width of the type.

Integer types are defined as follows in `schema.json`:

```shell
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

Decimal types are defined as follows in `schema.json`:

```shell
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

The date types are defined as follows in `schema.json`:

```shell
{
    "ColumnName":"COL1",
    "ColumnType":"{DT}"
}
```

The time types in TiDB are defined as `TT[(M)]`, where

- `TT` is the time type, which can be `TIME`, `DATETIME`, or `TIMESTAMP`.
- `M` is the precision of seconds in the range from 0 to 6.

The time types are defined as follows in `schema.json`:

```shell
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

The string types are defined as follows in `schema.json`:

```shell
{
    "ColumnName":"COL1",
    "ColumnType":"{ST}",
    "ColumnLength":"{M}"
}
```

#### Enum and Set types

The `ENUM` and `SET` types are defined as follows in `schema.json`:

```shell
{
    "ColumnName":"COL1",
    "ColumnType":"{ENUM/SET}",
}
```