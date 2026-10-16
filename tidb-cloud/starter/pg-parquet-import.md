---
title: 导入 Parquet 数据
summary: 了解如何在兼容 PostgreSQL 的 TiDB Cloud Starter 中查询并导入 Parquet 数据。
---

# 导入 Parquet 数据

兼容 PostgreSQL 的 {{{ .starter }}} 支持 `parquet` 扩展，用于读取 Parquet 数据并将其导入 SQL 表中。

> **Note:**
>
> 兼容 PostgreSQL 的 {{{ .starter }}} 当前处于公测阶段。

本文档介绍如何通过 HTTP 或 HTTPS URL 访问 Parquet。源 URL 必须可从 TiDB Cloud 访问。

## 启用 `parquet` 扩展 {#enable-the-parquet-extension}

在目标数据库中启用该扩展：

```sql
CREATE EXTENSION IF NOT EXISTS parquet;
```

## 查询 Parquet 文件 {#query-a-parquet-file}

使用带数据库模式限定的 `extensions.read_parquet()` 表函数可直接查询 Parquet 文件：

```sql
SELECT *
FROM extensions.read_parquet('https://example.com/data.parquet');
```

例如，统计行数：

```sql
SELECT count(*)
FROM extensions.read_parquet('https://example.com/data.parquet');
```

> **Note:**
>
> `read_parquet()` 必须写成带数据库模式限定的 `extensions.read_parquet()`。

## 将 Parquet 数据导入表中 {#import-parquet-data-into-a-table}

使用 `COPY ... WITH (FORMAT parquet)` 可将 Parquet 数据导入现有表中。

例如：

```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    name TEXT,
    created_at TIMESTAMP
);

COPY users
FROM 'https://example.com/users.parquet'
WITH (FORMAT parquet);
```

列会按名称进行不区分大小写的匹配。

- 没有与目标表列匹配的 Parquet 列会被忽略。
- 没有与 Parquet 列匹配的目标表列会填充为 `NULL`，但仍需满足目标列的约束。

## 类型映射 {#type-mapping}

以下常见 Parquet 类型会映射为兼容 PostgreSQL 的类型：

| Parquet 类型 | PostgreSQL 类型 |
| --- | --- |
| `BOOLEAN` | `BOOLEAN` |
| `INT32` | `INTEGER` |
| `INT64` | `BIGINT` |
| `FLOAT` | `DOUBLE PRECISION` |
| `DOUBLE` | `DOUBLE PRECISION` |
| 带 UTF-8 注解的 `BYTE_ARRAY` | `TEXT` |
| 二进制 `BYTE_ARRAY` | `BYTEA` |
| `INT96` 时间戳 | `TIMESTAMP` |
| `DATE` 逻辑类型 | `DATE` |
| `TIME` 逻辑类型 | 不支持 |
| `TIMESTAMP` 逻辑类型 | `TIMESTAMP` |
| `DECIMAL` 逻辑类型 | `NUMERIC`，仅限精度最多为 28 的 Decimal128 |

导入数据前，请验证 Parquet 表结构与目标表结构兼容。

## 支持的 Parquet 格式 {#supported-parquet-formats}

支持以下 Parquet 格式：

| 项目 | 支持的值 |
| --- | --- |
| Parquet 版本 | v1 和 v2 |
| 压缩编解码器 | Snappy、Gzip、Zstd，以及未压缩 |
| 远程 URL 协议 | HTTP 和 HTTPS |

## 限制 {#limitations}

公测期间有以下限制：

- 在运行 `COPY ... WITH (FORMAT parquet)` 之前，目标表必须已存在。
- 请使用 TiDB Cloud 可访问的 HTTP 或 HTTPS URL。
- 导入前请验证 Parquet 列类型。某些不兼容的类型组合在导入期间可能不会被拒绝。
- `extensions.read_parquet()` 必须使用 `extensions` 数据库模式限定符调用。
- 远程请求会受到连接超时和请求超时的限制。