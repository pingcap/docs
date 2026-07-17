---
title: Apache Iceberg™ Tables
summary: Learn how to connect TiDB Cloud Lake to Apache Iceberg catalogs and query or write Iceberg tables.
---

# Apache Iceberg™ Tables

## Overview

{{{ .lake }}} can connect to [Apache Iceberg™](https://iceberg.apache.org/) catalogs so that you can query Iceberg tables without loading their data into Fuse tables. You can also create and write Iceberg tables when the connected catalog supports write operations.

## When to Use Iceberg

Use Iceberg when:

- Your data is already managed by an Iceberg catalog.
- Multiple query engines need to share the same table metadata and object storage.
- You need Iceberg capabilities such as schema evolution and snapshots.
- You want to query or write Iceberg tables from {{{ .lake }}}.

## Create an Iceberg Catalog

Create a catalog before accessing Iceberg databases and tables.

### Syntax

```sql
CREATE CATALOG <catalog_name>
TYPE = ICEBERG
CONNECTION = (
    TYPE = '<catalog_type>'
    [ ADDRESS = '<catalog_address>' ]
    [ WAREHOUSE = '<warehouse_location>' ]
    [ "<connection_parameter>" = '<connection_parameter_value>' ]
    ...
);
```

### Parameters

| Parameter | Required? | Description |
| --- | --- | --- |
| `<catalog_name>` | Yes | Name of the catalog in {{{ .lake }}}. |
| `TYPE` | Yes | Catalog engine. Set this value to `ICEBERG`. |
| `CONNECTION` | Yes | Connection properties for the Iceberg catalog and its storage. |
| `TYPE` inside `CONNECTION` | Yes | Iceberg catalog type: `rest`, `glue`, `storage`, or `hive`. |
| `ADDRESS` | Depends on catalog type | Catalog service endpoint or Hive Metastore address. |
| `WAREHOUSE` | Depends on catalog type | Warehouse location used by the catalog. |
| `<connection_parameter>` | Depends on catalog type | Catalog, authentication, and object storage properties. |

The following connection parameters are available for S3-compatible storage:

| Connection Parameter | Description |
| --- | --- |
| `s3.endpoint` | S3-compatible service endpoint. |
| `s3.access-key-id` | S3 access key ID. |
| `s3.secret-access-key` | S3 secret access key. |
| `s3.session-token` | Session token used with temporary credentials. |
| `s3.region` | S3 region. |
| `client.region` | Region used by the client. This value takes precedence over `s3.region`. |
| `s3.path-style-access` | Whether to use path-style S3 access. |
| `s3.sse.type` | Server-side encryption type. |
| `s3.sse.key` | KMS key ID or customer-provided encryption key. |
| `s3.sse.md5` | MD5 checksum for a customer-provided encryption key. |
| `client.assume-role.arn` | ARN of the IAM role to assume. |
| `client.assume-role.external-id` | External ID used when assuming an IAM role. |
| `client.assume-role.session-name` | Session name used when assuming an IAM role. |
| `s3.allow-anonymous` | Whether to allow anonymous access to public storage. |
| `s3.disable-ec2-metadata` | Whether to disable credentials from EC2 instance metadata. |
| `s3.disable-config-load` | Whether to disable credentials and settings from local configuration sources. |

## Supported Catalog Types

{{{ .lake }}} supports the following Iceberg catalog types:

| Catalog Type | `TYPE` Value | Connection Requirements |
| --- | --- | --- |
| REST | `rest` | REST catalog address, warehouse location, and storage properties. |
| AWS Glue | `glue` | Glue region and authentication properties, plus S3 storage properties. |
| Storage (Amazon S3 Tables) | `storage` | Table bucket ARN and AWS client authentication properties. |
| Hive Metastore | `hive` | Hive Metastore address, warehouse location, and storage properties. |

The Storage catalog supports the following AWS client properties:

| Connection Parameter | Description |
| --- | --- |
| `table_bucket_arn` | ARN of the Amazon S3 Tables table bucket. |
| `profile_name` | AWS profile name. |
| `region_name` | AWS region. |
| `aws_access_key_id` | AWS access key ID. |
| `aws_secret_access_key` | AWS secret access key. |
| `aws_session_token` | AWS session token used with temporary credentials. |

## Manage and Query Iceberg Catalogs

Use the following statements to inspect and select catalogs:

```sql
SHOW CREATE CATALOG <catalog_name>;
```

```sql
SHOW CATALOGS [ LIKE '<pattern>' | WHERE <expression> ];
```

```sql
USE CATALOG <catalog_name>;
```

For more information, see [SHOW CREATE CATALOG](/tidb-cloud-lake/sql/show-create-catalog.md) and [SHOW CATALOGS](/tidb-cloud-lake/sql/show-catalogs.md).

After selecting a catalog, use standard SQL to query its tables:

```sql
SELECT <select_list>
FROM [ <catalog_name>. ]<database_name>.<table_name>
[ WHERE <condition> ];
```

## Data Type Mapping

The following table shows the supported mappings from Iceberg types to {{{ .lake }}} types. Iceberg types not listed here are not supported.

| Apache Iceberg™ | {{{ .lake }}} |
| --- | --- |
| BOOLEAN | [BOOLEAN](/tidb-cloud-lake/sql/boolean.md) |
| INT | [INT32](/tidb-cloud-lake/sql/numeric.md#integer-data-types) |
| LONG | [INT64](/tidb-cloud-lake/sql/numeric.md#integer-data-types) |
| DATE | [DATE](/tidb-cloud-lake/sql/date-time.md) |
| TIMESTAMP / TIMESTAMPZ | [TIMESTAMP](/tidb-cloud-lake/sql/date-time.md) |
| FLOAT | [FLOAT](/tidb-cloud-lake/sql/numeric.md#floating-point-data-types) |
| DOUBLE | [DOUBLE](/tidb-cloud-lake/sql/numeric.md#floating-point-data-types) |
| STRING / BINARY | [STRING](/tidb-cloud-lake/sql/string.md) |
| DECIMAL | [DECIMAL](/tidb-cloud-lake/sql/decimal.md) |
| LIST | [ARRAY](/tidb-cloud-lake/sql/array.md) |
| MAP | [MAP](/tidb-cloud-lake/sql/map.md) |
| STRUCT | [TUPLE](/tidb-cloud-lake/sql/tuple.md) |

## Refresh Cached Metadata

{{{ .lake }}} caches Iceberg catalog metadata after the first query. The metadata cache is valid for 10 minutes by default and is refreshed asynchronously.

Use the following statements when you need to refresh cached metadata immediately:

```sql
USE CATALOG <catalog_name>;
ALTER DATABASE <database_name> REFRESH CACHE;
ALTER TABLE <database_name>.<table_name> REFRESH CACHE;
```

{{{ .lake }}} also supports caching table data read from Iceberg catalogs.

## Write to Iceberg Tables

You can create and write Iceberg tables in a catalog that supports write operations.

### Create a Table

```sql
CREATE TABLE [ <database_name>. ]<table_name> (
    <column_name> <data_type> [ , ... ]
)
ENGINE = ICEBERG
[ PARTITION BY ( <column_name> [ , ... ] ) ];
```

| Parameter | Description |
| --- | --- |
| `ENGINE = ICEBERG` | Stores the table in Iceberg format. |
| `PARTITION BY` | Defines one or more partition columns. |

The following {{{ .lake }}} data types are supported when writing Iceberg tables:

| {{{ .lake }}} Type | Apache Iceberg™ Type |
| --- | --- |
| BOOLEAN | Boolean |
| INT | Int |
| BIGINT | Long |
| FLOAT | Float |
| DOUBLE | Double |
| STRING | String |
| DATE | Date |
| TIMESTAMP | Timestamp |

### Insert Data

Use `INSERT INTO` to write rows to an Iceberg table:

```sql
INSERT INTO [ <database_name>. ]<table_name>
[ ( <column_name> [ , ... ] ) ]
VALUES ( <value> [ , ... ] ) [ , ... ];
```

Both partitioned and non-partitioned Iceberg tables support single-row and multi-row inserts. For partitioned tables, {{{ .lake }}} routes rows to the corresponding partitions.

## Iceberg Table Functions

Use the following table functions to inspect Iceberg metadata:

- [ICEBERG_MANIFEST](/tidb-cloud-lake/sql/iceberg-manifest.md)
- [ICEBERG_SNAPSHOT](/tidb-cloud-lake/sql/iceberg-snapshot.md)
