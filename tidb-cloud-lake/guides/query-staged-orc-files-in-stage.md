---
title: 在 Stage 中查询暂存的 ORC 文件
summary: 在本教程中，我们将带你完成以下过程：下载 ORC 格式的 Iris 数据集，将其上传到 Amazon S3 存储桶，创建外部 stage，并直接从 ORC 文件中查询数据。
---

# 在 Stage 中查询暂存的 ORC 文件

## 语法 {#syntax}

- [将行作为 Variant 查询](/tidb-cloud-lake/guides/query-stage.md#query-rows-as-variants)
- [按列名查询列](/tidb-cloud-lake/guides/query-stage.md#query-columns-by-name)
- [查询元信息](/tidb-cloud-lake/guides/query-stage.md#query-metadata)

## 教程 {#tutorial}

在本教程中，我们将带你完成以下过程：下载 ORC 格式的 Iris 数据集，将其上传到 Amazon S3 存储桶，创建外部 stage，并直接从 ORC 文件中查询数据。

## 第 1 步：下载 Iris 数据集 {#step-1-download-iris-dataset}

从 <https://github.com/tensorflow/io/raw/master/tests/test_orc/iris.orc> 下载 iris 数据集，然后将其上传到你的 Amazon S3 存储桶。

iris 数据集包含 3 个类，每个类有 50 个实例，其中每个类对应一种鸢尾花类型。它包含 4 个属性：(1) 萼片长度，(2) 萼片宽度，(3) 花瓣长度，(4) 花瓣宽度，最后一列包含类标签。

## 第 2 步：创建外部 stage {#step-2-create-external-stage}

使用存放 iris 数据集文件的 Amazon S3 存储桶创建一个外部 stage。

```sql
CREATE STAGE orc_query_stage
    URL = 's3://lake-doc'
    CONNECTION = (
        ACCESS_KEY_ID = '<your-key-id>',
        SECRET_ACCESS_KEY = '<your-secret-key>'
    );
```

## 第 3 步：查询 ORC 文件 {#step-3-query-orc-file}

按列查询

```sql
SELECT *
FROM @orc_query_stage
(
    FILE_FORMAT => 'orc',
    PATTERN => '.*[.]orc'
);

┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│    sepal_length   │    sepal_width    │    petal_length   │    petal_width    │      species     │
├───────────────────┼───────────────────┼───────────────────┼───────────────────┼──────────────────┤
│               5.1 │               3.5 │               1.4 │               0.2 │ setosa           │
│                 · │                 · │                 · │                 · │ ·                │
│               5.9 │                 3 │               5.1 │               1.8 │ virginica        │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

使用路径表达式查询：

```sql
SELECT $1
FROM @orc_query_stage
(
    FILE_FORMAT => 'orc',
    PATTERN => '.*[.]orc'

);
```

你也可以直接查询远程 ORC 文件：

```sql
SELECT
  *
FROM
  'https://github.com/tensorflow/io/raw/master/tests/test_orc/iris.orc' (file_format => 'orc');
```

## 第 4 步：结合元信息查询 {#step-4-query-with-metadata}

直接从 stage 查询 ORC 文件，包括 `METADATA$FILENAME` 和 `METADATA$FILE_ROW_NUMBER` 等元信息列：

```sql
SELECT
    METADATA$FILENAME,
    METADATA$FILE_ROW_NUMBER,
    *
FROM @orc_query_stage
(
    FILE_FORMAT => 'orc',
    PATTERN => '.*[.]orc'
);
```