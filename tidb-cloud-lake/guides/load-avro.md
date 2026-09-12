---
title: 将 Avro 加载到 TiDB Cloud Lake
summary: Apache Avro™ 是记录数据的主流序列化格式，也是流式数据管道的首选格式。
---

# 将 Avro 加载到 TiDB Cloud Lake

## 什么是 Avro？ {#what-is-avro}

[Apache Avro™](https://avro.apache.org/) 是记录数据的主流序列化格式，也是流式数据管道的首选格式。

## 加载 Avro 文件 {#loading-avro-file}

加载 AVRO 文件的通用语法如下：

```sql
COPY INTO [<database>.]<table_name>
     FROM { internalStage | externalStage | externalLocation }
[ PATTERN = '<regex_pattern>' ]
FILE_FORMAT = (TYPE = AVRO)
```

- 有关更多 Avro 文件格式选项，请参阅[Avro 文件格式选项](/tidb-cloud-lake/sql/input-output-file-formats.md#avro-options)。
- 有关更多 COPY INTO table 选项，请参阅[COPY INTO table](/tidb-cloud-lake/sql/copy-into-table.md)。

## 教程：通过远程 HTTP URL 将 Avro 数据加载到 {{{ .lake }}} {#tutorial-loading-avro-data-into-lake-from-remote-http-url}

在本教程中，你将基于 Avro schema 在 {{{ .lake }}} 中创建一张表，并通过 HTTPS 直接从 GitHub 托管的 `.avro` 文件加载 Avro 数据。

### 第 1 步：查看 Avro schema {#step-1-review-the-avro-schema}

在 {{{ .lake }}} 中创建表之前，先快速了解一下我们要使用的 Avro schema：[userdata.avsc](https://github.com/Teradata/kylo/blob/master/samples/sample-data/avro/userdata.avsc)。该 schema 定义了一个名为 `User` 的 record，包含 13 个字段，大多为字符串类型，另外还有 `int` 和 `float` 类型。

```json
{
  "type": "record",
  "name": "User",
  "fields": [
    {"name": "registration_dttm", "type": "string"},
    {"name": "id", "type": "int"},
    {"name": "first_name", "type": "string"},
    {"name": "last_name", "type": "string"},
    {"name": "email", "type": "string"},
    {"name": "gender", "type": "string"},
    {"name": "ip_address", "type": "string"},
    {"name": "cc", "type": "string"},
    {"name": "country", "type": "string"},
    {"name": "birthdate", "type": "string"},
    {"name": "salary", "type": "float"},
    {"name": "title", "type": "string"},
    {"name": "comments", "type": "string"}
  ]
}
```

### 第 2 步：在 {{{ .lake }}} 中创建表 {#step-2-create-a-table-in-lake}

创建一张与该 schema 中定义的结构相匹配的表：

```sql
CREATE TABLE userdata (
  registration_dttm STRING,
  id INT,
  first_name STRING,
  last_name STRING,
  email STRING,
  gender STRING,
  ip_address STRING,
  cc VARIANT,
  country STRING,
  birthdate STRING,
  salary FLOAT,
  title STRING,
  comments STRING
);
```

### 第 3 步：从远程 HTTPS URL 加载数据 {#step-3-load-data-from-a-remote-https-url}

```sql
COPY INTO userdata
FROM 'https://raw.githubusercontent.com/Teradata/kylo/master/samples/sample-data/avro/userdata1.avro'
FILE_FORMAT = (type = avro);
```

```sql
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                             File                             │ Rows_loaded │ Errors_seen │    First_error   │ First_error_line │
├──────────────────────────────────────────────────────────────┼─────────────┼─────────────┼──────────────────┼──────────────────┤
│ Teradata/kylo/master/samples/sample-data/avro/userdata1.avro │        1000 │           0 │ NULL             │             NULL │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 第 4 步：查询数据 {#step-4-query-the-data}

现在，你可以查看刚刚导入的数据：

```sql
SELECT id, first_name, email, salary FROM userdata LIMIT 5;
```

```sql
┌───────────────────────────────────────────────────────────────────────────────────┐
│        id       │    first_name    │           email          │       salary      │
├─────────────────┼──────────────────┼──────────────────────────┼───────────────────┤
│               1 │ Amanda           │ ajordan0@com.com         │          49756.53 │
│               2 │ Albert           │ afreeman1@is.gd          │         150280.17 │
│               3 │ Evelyn           │ emorgan2@altervista.org  │         144972.52 │
│               4 │ Denise           │ driley3@gmpg.org         │          90263.05 │
│               5 │ Carlos           │ cburns4@miitbeian.gov.cn │              NULL │
└───────────────────────────────────────────────────────────────────────────────────┘
```