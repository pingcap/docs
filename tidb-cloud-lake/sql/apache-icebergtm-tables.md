---
title: Apache Iceberg™ Tables
summary: 了解如何将 TiDB Cloud Lake 连接到 Apache Iceberg catalog，并查询或写入 Iceberg 表。
---

# Apache Iceberg™ Tables

{{{ .lake }}} 可以连接到 [Apache Iceberg™](https://iceberg.apache.org/) catalog，这样你无需将数据加载到 Fuse 表中即可查询 Iceberg 表。当所连接的 catalog 支持写操作时，你还可以创建并写入 Iceberg 表。

## 何时使用 Iceberg {#when-to-use-iceberg}

在以下情况下使用 Iceberg：

- 你的数据已经由 Iceberg catalog 管理。
- 多个查询引擎需要共享相同的表元信息和对象存储。
- 你需要 Iceberg 提供的能力，例如 schema evolution 和快照。
- 你希望从 {{{ .lake }}} 查询或写入 Iceberg 表。

## 创建 Iceberg Catalog {#create-an-iceberg-catalog}

在访问 Iceberg 数据库和表之前，请先创建 catalog。

### 语法 {#syntax}

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

### 参数 {#parameters}

| 参数 | 必填？ | 说明 |
| --- | --- | --- |
| `<catalog_name>` | 是 | {{{ .lake }}} 中的 catalog 名称。 |
| `TYPE` | 是 | Catalog 引擎。将该值设置为 `ICEBERG`。 |
| `CONNECTION` | 是 | Iceberg catalog 及其存储的连接属性。 |
| `TYPE` inside `CONNECTION` | 是 | Iceberg catalog 类型：`rest`、`glue`、`storage` 或 `hive`。 |
| `ADDRESS` | 取决于 catalog 类型 | Catalog 服务端点或 Hive Metastore 地址。 |
| `WAREHOUSE` | 取决于 catalog 类型 | Catalog 使用的计算集群位置。 |
| `<connection_parameter>` | 取决于 catalog 类型 | Catalog、认证和对象存储属性。 |

以下连接参数可用于兼容 S3 的存储：

| 连接参数 | 说明 |
| --- | --- |
| `s3.endpoint` | 兼容 S3 的服务端点。 |
| `s3.access-key-id` | S3 access key ID。 |
| `s3.secret-access-key` | S3 secret access key。 |
| `s3.session-token` | 与临时凭证一起使用的 session token。 |
| `s3.region` | S3 Region。 |
| `client.region` | 客户端使用的 Region。该值优先于 `s3.region`。 |
| `s3.path-style-access` | 是否使用 path-style 的 S3 访问方式。 |
| `s3.sse.type` | 服务端加密类型。 |
| `s3.sse.key` | KMS key ID 或客户提供的加密密钥。 |
| `s3.sse.md5` | 客户提供的加密密钥的 MD5 校验和。 |
| `client.assume-role.arn` | 要承担的 IAM role 的 ARN。 |
| `client.assume-role.external-id` | 承担 IAM role 时使用的 external ID。 |
| `client.assume-role.session-name` | 承担 IAM role 时使用的 session 名称。 |
| `s3.allow-anonymous` | 是否允许对公共存储进行匿名访问。 |
| `s3.disable-ec2-metadata` | 是否禁用来自 EC2 实例元信息的凭证。 |
| `s3.disable-config-load` | 是否禁用来自本地配置源的凭证和设置。 |

## 支持的 Catalog 类型 {#supported-catalog-types}

{{{ .lake }}} 支持以下 Iceberg catalog 类型：

| Catalog 类型 | `TYPE` 值 | 连接要求 |
| --- | --- | --- |
| REST | `rest` | REST catalog 地址、计算集群位置以及存储属性。 |
| AWS Glue | `glue` | Glue Region 和身份验证属性，以及 S3 存储属性。 |
| Storage (Amazon S3 Tables) | `storage` | 表存储桶 ARN 和 AWS 客户端身份验证属性。 |
| Hive Metastore | `hive` | Hive Metastore 地址、计算集群位置以及存储属性。 |

Storage catalog 支持以下 AWS 客户端属性：

| 连接参数 | 说明 |
| --- | --- |
| `table_bucket_arn` | Amazon S3 Tables 表存储桶的 ARN。 |
| `profile_name` | AWS profile 名称。 |
| `region_name` | AWS Region。 |
| `aws_access_key_id` | AWS access key ID。 |
| `aws_secret_access_key` | AWS secret access key。 |
| `aws_session_token` | 与临时凭证一起使用的 AWS session token。 |

## 管理和查询 Iceberg Catalog {#manage-and-query-iceberg-catalogs}

使用以下语句查看和选择 catalog：

```sql
SHOW CREATE CATALOG <catalog_name>;
```

```sql
SHOW CATALOGS [ LIKE '<pattern>' | WHERE <expression> ];
```

```sql
USE CATALOG <catalog_name>;
```

更多信息，请参见 [SHOW CREATE CATALOG](/tidb-cloud-lake/sql/show-create-catalog.md) 和 [SHOW CATALOGS](/tidb-cloud-lake/sql/show-catalogs.md)。

选择 catalog 后，使用标准 SQL 查询其中的表：

```sql
SELECT <select_list>
FROM [ <catalog_name>. ]<database_name>.<table_name>
[ WHERE <condition> ];
```

## 数据类型映射 {#data-type-mapping}

下表展示了从 Iceberg 类型到 {{{ .lake }}} 类型的支持映射。此处未列出的 Iceberg 类型不受支持。

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

## 刷新缓存的元信息 {#refresh-cached-metadata}

{{{ .lake }}} 在首次查询后会缓存 Iceberg catalog 的元信息。默认情况下，元信息缓存有效期为 10 分钟，并会异步刷新。

当你需要立即刷新缓存的元信息时，请使用以下语句：

```sql
USE CATALOG <catalog_name>;
ALTER DATABASE <database_name> REFRESH CACHE;
ALTER TABLE <database_name>.<table_name> REFRESH CACHE;
```

{{{ .lake }}} 还支持缓存从 Iceberg catalog 读取的表数据。

## 写入 Iceberg 表 {#write-to-iceberg-tables}

你可以在支持写操作的 catalog 中创建并写入 Iceberg 表。

### 创建表 {#create-a-table}

```sql
CREATE TABLE [ <database_name>. ]<table_name> (
    <column_name> <data_type> [ , ... ]
)
ENGINE = ICEBERG
[ PARTITION BY ( <column_name> [ , ... ] ) ];
```

| 参数 | 说明 |
| --- | --- |
| `ENGINE = ICEBERG` | 以 Iceberg 格式存储该表。 |
| `PARTITION BY` | 定义一个或多个分区列。 |

写入 Iceberg 表时支持以下 {{{ .lake }}} 数据类型：

| {{{ .lake }}} 类型 | Apache Iceberg™ 类型 |
| --- | --- |
| BOOLEAN | Boolean |
| INT | Int |
| BIGINT | Long |
| FLOAT | Float |
| DOUBLE | Double |
| STRING | String |
| DATE | Date |
| TIMESTAMP | Timestamp |

### 插入数据 {#insert-data}

使用 `INSERT INTO` 将行写入 Iceberg 表：

```sql
INSERT INTO [ <database_name>. ]<table_name>
[ ( <column_name> [ , ... ] ) ]
VALUES ( <value> [ , ... ] ) [ , ... ];
```

分区和非分区 Iceberg 表都支持单行和多行插入。对于分区表，{{{ .lake }}} 会将行路由到相应的分区。

## Iceberg 表函数 {#iceberg-table-functions}

使用以下表函数检查 Iceberg 元信息：

- [ICEBERG_MANIFEST](/tidb-cloud-lake/sql/iceberg-manifest.md)
- [ICEBERG_SNAPSHOT](/tidb-cloud-lake/sql/iceberg-snapshot.md)