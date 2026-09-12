---
title: CREATE FILE FORMAT
summary: 创建命名的文件格式。
---

# CREATE FILE FORMAT

创建命名的文件格式。

## 语法 {#syntax}

```sql
CREATE [ OR REPLACE ] FILE FORMAT [ IF NOT EXISTS ] <format_name> FileFormatOptions
```

有关 `FileFormatOptions` 的详细信息，请参见[输入与输出文件格式](/tidb-cloud-lake/sql/input-output-file-formats.md)。

## 使用文件格式 {#use-the-file-format}

创建一次，然后在查询和加载中复用该格式：

```sql
-- 1) Create a reusable format
CREATE OR REPLACE FILE FORMAT my_custom_csv TYPE = CSV FIELD_DELIMITER = '\t';

-- 2) Query staged files (stage table function syntax uses =>)
SELECT * FROM @mystage/data.csv (FILE_FORMAT => 'my_custom_csv') LIMIT 10;

-- 3) Load staged files with COPY INTO (copy options use =)
COPY INTO my_table
FROM @mystage/data.csv
FILE_FORMAT = (FORMAT_NAME = 'my_custom_csv');
```

为什么使用不同的运算符？stage 表函数接受使用 `=>` 编写的键值参数，而 `COPY INTO` 选项使用标准赋值运算符 `=`。

**快速工作流：使用同一个格式进行创建、查询和加载**

```sql
-- Create a reusable format
CREATE FILE FORMAT my_parquet TYPE = PARQUET;

-- Query staged files with the format (stage table function syntax uses =>)
SELECT * FROM @sales_stage/2024/order.parquet (FILE_FORMAT => 'my_parquet') LIMIT 10;

-- Load staged files with COPY INTO (copy options use =)
COPY INTO analytics.orders
FROM @sales_stage/2024/order.parquet
FILE_FORMAT = (FORMAT_NAME = 'my_parquet');
```

## LANCE 格式说明 {#lance-format-note}

你也可以创建命名的 Lance 文件格式：

```sql
CREATE FILE FORMAT my_lance TYPE = LANCE;
```

与 CSV、TSV、NDJSON 或 PARQUET 不同，命名的 `LANCE` 格式只能与 `COPY INTO <location>` 一起复用。不支持将其用于 stage-table 读取或 `COPY INTO <table>`，因为 {{{ .lake}}} 写入的是 Lance 数据集目录，而不是独立文件。

```sql
COPY INTO @ml_stage/datasets/train
FROM my_training_table
FILE_FORMAT = (FORMAT_NAME = 'my_lance')
USE_RAW_PATH = TRUE
OVERWRITE = TRUE;
```

有关 Lance 特有的行为和限制，请参见[输入与输出文件格式](/tidb-cloud-lake/sql/input-output-file-formats.md#lance-options)和[`COPY INTO <location>`](/tidb-cloud-lake/sql/copy-into-location.md)。