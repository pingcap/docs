---
title: COPY INTO <location>
summary: COPY INTO 允许你将表或查询中的数据卸载到以下某个位置中的一个或多个文件。
---

# `COPY INTO <location>`

COPY INTO 允许你将表或查询中的数据卸载到以下某个位置中的一个或多个文件：

- 用户 / Internal / External stage：参阅 [Stage 是什么？](/tidb-cloud-lake/guides/stage-overview.md) 了解 {{{ .lake }}} 中的 stage。
- 在存储服务中创建的存储桶或容器。

另请参阅：[`COPY INTO <table>`](/tidb-cloud-lake/sql/copy-into-table.md)

## 语法 {#syntax}

```sql
COPY INTO { internalStage | externalStage | externalLocation }
FROM { [<database_name>.]<table_name> | ( <query> ) }
[ PARTITION BY ( <expr> ) ]
[ FILE_FORMAT = (
         FORMAT_NAME = '<your-custom-format>'
         | TYPE = { CSV | TSV | NDJSON | PARQUET | LANCE } [ formatTypeOptions ]
       ) ]
[ copyOptions ]
[ VALIDATION_MODE = RETURN_ROWS ]
[ DETAILED_OUTPUT = true | false ]
```

### internalStage {#internalstage}

```sql
internalStage ::= @<internal_stage_name>[/<path>]
```

### externalStage {#externalstage}

```sql
externalStage ::= @<external_stage_name>[/<path>]
```

### externalLocation {#externallocation}

<SimpleTab groupId="externallocation">

<div label="Amazon S3-like Storage Services" value="Amazon S3-like Storage Services">

```sql
externalLocation ::=
  's3://<bucket>[<path>]'
  CONNECTION = (
        <connection_parameters>
  )
```

有关访问 Amazon S3-like 存储服务时可用的连接参数，请参阅 [连接参数](/tidb-cloud-lake/sql/connection-parameters.md)。

</div>

<div label="Azure Blob Storage" value="Azure Blob Storage">

```sql
externalLocation ::=
  'azblob://<container>[<path>]'
  CONNECTION = (
        <connection_parameters>
  )
```

有关访问 Azure Blob Storage 时可用的连接参数，请参阅 [连接参数](/tidb-cloud-lake/sql/connection-parameters.md)。

</div>

<div label="Google Cloud Storage" value="Google Cloud Storage">

```sql
externalLocation ::=
  'gcs://<bucket>[<path>]'
  CONNECTION = (
        <connection_parameters>
  )
```

有关访问 Google Cloud Storage 时可用的连接参数，请参阅 [连接参数](/tidb-cloud-lake/sql/connection-parameters.md)。

</div>

<div label="Alibaba Cloud OSS" value="Alibaba Cloud OSS">

```sql
externalLocation ::=
  'oss://<bucket>[<path>]'
  CONNECTION = (
        <connection_parameters>
  )
```

有关访问 Alibaba Cloud OSS 时可用的连接参数，请参阅 [连接参数](/tidb-cloud-lake/sql/connection-parameters.md)。

</div>

<div label="Tencent Cloud Object Storage" value="Tencent Cloud Object Storage">

```sql
externalLocation ::=
  'cos://<bucket>[<path>]'
  CONNECTION = (
        <connection_parameters>
  )
```

有关访问 Tencent Cloud Object Storage 时可用的连接参数，请参阅 [连接参数](/tidb-cloud-lake/sql/connection-parameters.md)。

</div>
</SimpleTab>

### FILE_FORMAT {#file-format}

详情请参阅 [输入与输出文件格式](/tidb-cloud-lake/sql/input-output-file-formats.md)。

`LANCE` 仅在 `COPY INTO <location>` 中受支持。{{{ .lake}}} 会在目标路径下写入一个 Lance 数据集目录，而不是单个独立文件。

### PARTITION BY {#partition-by}

指定一个表达式，用于将卸载的数据分区到不同的文件夹中。该表达式必须计算为 `STRING` 类型。表达式生成的每个不同值都会在目标路径中创建一个子文件夹，相应的行会被写入该子文件夹下的文件中。

- 如果表达式计算结果为 `NULL`，这些行会被放入一个特殊的 `_NULL_` 文件夹中。
- 该表达式可以引用源表或查询中的任意列。
- 分区值中不允许使用路径遍历（`..`）。

以下选项与 `PARTITION BY` 不兼容，如果设置会导致报错：

| 选项 | 限制 |
| ------------------- | ------------------------------------------------ |
| SINGLE              | 使用 `PARTITION BY` 时不能为 `TRUE`。      |
| OVERWRITE           | 使用 `PARTITION BY` 时不能为 `TRUE`。      |
| INCLUDE_QUERY_ID    | 使用 `PARTITION BY` 时不能为 `FALSE`。     |

### copyOptions {#copyoptions}

```sql
copyOptions ::=
  [ SINGLE = true | false ]
  [ MAX_FILE_SIZE = <num> ]
  [ OVERWRITE = true | false ]
  [ INCLUDE_QUERY_ID = true | false ]
  [ USE_RAW_PATH = true | false ]
```

| 参数 | 默认值 | 描述 |
| ---------------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| SINGLE           | false                  | 当为 `true` 时，该命令会将数据卸载到单个文件中。                                                                                                                    |
| MAX_FILE_SIZE    | 67108864 bytes (64 MB) | 每个要创建文件的最大大小（以字节为单位）。当 `SINGLE` 为 false 时生效。                                                                                      |
| OVERWRITE        | false                  | 当为 `true` 时，目标路径下同名的现有文件将被覆盖。注意：`OVERWRITE = true` 要求 `USE_RAW_PATH = true` 且 `INCLUDE_QUERY_ID = false`。 |
| INCLUDE_QUERY_ID | true                   | 当为 `true` 时，导出文件名中会包含一个唯一的 UUID。                                                                                                        |
| USE_RAW_PATH     | false                  | 当为 `true` 时，将使用用户提供的精确路径（包括完整文件名）来导出数据。如果设置为 `false`，用户必须提供一个目录路径。       |

> **注意：**
>
> - 当 `TYPE = LANCE` 时，不支持 `SINGLE`。
> - 当 `TYPE = LANCE` 时，不支持 `PARTITION BY`。
> - 当 `TYPE = LANCE` 且你希望为下游 Lance 读取器提供稳定的数据集 URI 时，建议使用 `USE_RAW_PATH = TRUE`。
> - 当 `TYPE = LANCE` 且 `USE_RAW_PATH = FALSE` 时，{{{ .lake}}} 会将查询 ID 追加到目标路径，并为每次导出创建一个单独的数据集根目录。

### DETAILED_OUTPUT {#detailed-output}

决定是否返回数据卸载的详细结果，默认值为 `false`。更多信息，请参阅 [输出](#output)。

## 输出 {#output}

COPY INTO 会通过以下列提供数据卸载结果的摘要：

| 列 | 描述 |
| ------------- | --------------------------------------------------------------------------------------------- |
| rows_unloaded | 成功卸载到目标位置的行数。 |
| input_bytes   | 卸载操作期间从源表读取的数据总大小（以字节为单位）。 |
| output_bytes  | 写入目标位置的数据总大小（以字节为单位）。 |

当 `DETAILED_OUTPUT` 设置为 `true` 时，COPY INTO 会返回包含以下列的结果。这有助于定位已卸载的文件，尤其是在使用 `MAX_FILE_SIZE` 将卸载数据拆分为多个文件时。

| 列 | 描述 |
| --------- | -------------------------------------------------- |
| file_name | 卸载文件的名称。                     |
| file_size | 卸载文件的大小（以字节为单位）。            |
| row_count | 卸载文件中包含的行数。 |

## 示例 {#examples}

在本节中，以下示例使用了如下表和数据：

```sql
-- Create sample table
CREATE TABLE canadian_city_population (
     city_name VARCHAR(50),
     population INT
);

-- Insert sample data
INSERT INTO canadian_city_population (city_name, population)
VALUES
('Toronto', 2731571),
('Montreal', 1704694),
('Vancouver', 631486),
('Calgary', 1237656),
('Ottawa', 934243),
('Edmonton', 972223),
('Quebec City', 542298),
('Winnipeg', 705244),
('Hamilton', 536917),
('Halifax', 403390);
```

### 示例 1：卸载到内部 stage {#example-1-unloading-to-internal-stage}

本示例将数据卸载到内部 stage：

```sql
-- Create an internal stage
CREATE STAGE my_internal_stage;

-- Unload data from the table to the stage using the PARQUET file format
COPY INTO @my_internal_stage
    FROM canadian_city_population
    FILE_FORMAT = (TYPE = PARQUET);

┌────────────────────────────────────────────┐
│ rows_unloaded │ input_bytes │ output_bytes │
├───────────────┼─────────────┼──────────────┤
│            10 │         211 │          572 │
└────────────────────────────────────────────┘

LIST @my_internal_stage;

┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               name                              │  size  │        md5       │         last_modified         │      creator     │
├─────────────────────────────────────────────────────────────────┼────────┼──────────────────┼───────────────────────────────┼──────────────────┤
│ data_abe520a3-ee88-488c-9221-b07c562c9a30_0000_00000000.parquet │    572 │ NULL             │ 2024-01-18 16:20:48.979 +0000 │ NULL             │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 示例 2：卸载到压缩文件 {#example-2-unloading-to-compressed-file}

本示例将数据卸载到压缩文件中：

```sql
-- Create an internal stage
CREATE STAGE my_internal_stage;

-- Unload data from the table to the stage using the CSV file format with gzip compression
COPY INTO @my_internal_stage
    FROM canadian_city_population
    FILE_FORMAT = (TYPE = CSV COMPRESSION = gzip);

┌────────────────────────────────────────────┐
│ rows_unloaded │ input_bytes │ output_bytes │
├───────────────┼─────────────┼──────────────┤
│            10 │         182 │          168 │
└────────────────────────────────────────────┘

LIST @my_internal_stage;

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              name                              │  size  │        md5       │         last_modified         │      creator     │
├────────────────────────────────────────────────────────────────┼────────┼──────────────────┼───────────────────────────────┼──────────────────┤
│ data_7970afa5-32e3-4e7d-b793-e42a2a82a8e6_0000_00000000.csv.gz │    168 │ NULL             │ 2024-01-18 16:27:01.663 +0000 │ NULL             │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

-- COPY INTO also works with custom file formats. See below:
-- Create a custom file format named my_csv_gzip with CSV format and gzip compression
CREATE FILE FORMAT my_csv_gzip TYPE = CSV COMPRESSION = gzip;

-- Unload data from the table to the stage using the custom file format my_csv_gzip
COPY INTO @my_internal_stage
    FROM canadian_city_population
    FILE_FORMAT = (FORMAT_NAME = 'my_csv_gzip');

┌────────────────────────────────────────────┐
│ rows_unloaded │ input_bytes │ output_bytes │
├───────────────┼─────────────┼──────────────┤
│            10 │         182 │          168 │
└────────────────────────────────────────────┘

LIST @my_internal_stage;

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              name                              │  size  │        md5       │         last_modified         │      creator     │
├────────────────────────────────────────────────────────────────┼────────┼──────────────────┼───────────────────────────────┼──────────────────┤
│ data_d006ba1c-0609-46d7-a67b-75c7078d86ff_0000_00000000.csv.gz │    168 │ NULL             │ 2024-01-18 16:29:29.721 +0000 │ NULL             │
│ data_7970afa5-32e3-4e7d-b793-e42a2a82a8e6_0000_00000000.csv.gz │    168 │ NULL             │ 2024-01-18 16:27:01.663 +0000 │ NULL             │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 示例 3：卸载到存储桶 {#example-3-unloading-to-bucket}

本示例将数据卸载到 MinIO 上的存储桶中：

```sql
-- Unload data from the table to a bucket named 'lake' on MinIO using the PARQUET file format
COPY INTO 's3://lake'
    CONNECTION = (
    ENDPOINT_URL = 'http://localhost:9000/',
    ACCESS_KEY_ID = 'ROOTUSER',
    SECRET_ACCESS_KEY = 'CHANGEME123',
    region = 'us-west-2'
    )
    FROM canadian_city_population
    FILE_FORMAT = (TYPE = PARQUET);

┌────────────────────────────────────────────┐
│ rows_unloaded │ input_bytes │ output_bytes │
├───────────────┼─────────────┼──────────────┤
│            10 │         211 │          572 │
└────────────────────────────────────────────┘
```

### 示例 4：使用 PARTITION BY 卸载 {#example-4-unloading-with-partition-by}

本示例根据派生表达式将数据卸载到分区目录中：

```sql
-- Create a sample table
CREATE TABLE sales_data (
    sale_date DATE,
    region VARCHAR,
    amount INT
);

INSERT INTO sales_data VALUES
    ('2025-01-15', 'east', 100),
    ('2025-01-20', 'west', 200),
    ('2025-02-10', 'east', 150),
    (NULL, 'west', 50);

-- Create an internal stage
CREATE STAGE partitioned_stage;

-- Unload data partitioned by year-month derived from sale_date
-- When sale_date is NULL, to_varchar() returns NULL, so the entire
-- concatenation evaluates to NULL and the row lands in the _NULL_ folder.
COPY INTO @partitioned_stage
    FROM sales_data
    PARTITION BY ('month=' || to_varchar(sale_date, 'YYYY-MM'))
    FILE_FORMAT = (TYPE = PARQUET);

-- Verify the partitioned folder layout
SELECT name FROM list_stage(location => '@partitioned_stage') ORDER BY name;

┌──────────────────────────────────────────────────────────────────┐
│                              name                                │
├──────────────────────────────────────────────────────────────────┤
│ _NULL_/data_<query_id>_0000_00000000.parquet                     │
│ month=2025-01/data_<query_id>_0000_00000000.parquet              │
│ month=2025-02/data_<query_id>_0000_00000000.parquet              │
└──────────────────────────────────────────────────────────────────┘
```

当分区表达式计算结果为 `NULL` 时，数据会被放入 `_NULL_` 目录中。每个唯一的分区值都会创建各自的子目录，其中包含对应的数据文件。

### 示例 5：卸载到 Lance 数据集 {#example-5-unloading-to-a-lance-dataset}

本示例将数据卸载为 Lance 数据集目录，而不是独立文件：

```sql
CREATE STAGE ml_stage;

COPY INTO @ml_stage/datasets/train
FROM (
    SELECT number, number + 1 AS label
    FROM numbers(10)
)
FILE_FORMAT = (TYPE = LANCE)
USE_RAW_PATH = TRUE
OVERWRITE = TRUE
DETAILED_OUTPUT = TRUE;
```

输出路径将包含 Lance 数据集布局，类似如下：

```text
datasets/train/_versions/...
datasets/train/data/... .lance
datasets/train/*.manifest
```

有关完整的端到端示例（包括使用 Python `lance` 进行验证），请参见[卸载 Lance 数据集](/tidb-cloud-lake/guides/unload-lance-dataset.md)。