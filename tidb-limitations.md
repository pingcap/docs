---
title: TiDB 限制
summary: 了解 TiDB 的使用限制。
---

# TiDB 限制

本文档描述了 TiDB 的常见使用限制，包括最大标识符长度以及支持的数据库、表、索引、分区表和序列的最大数量。

> **Note:**
>
> TiDB 提供了与 MySQL 协议和语法的高兼容性，包括许多 MySQL 的限制。例如，单个索引最多可以包含 16 列。更多信息请参见 [MySQL Compatibility](/mysql-compatibility.md) 和官方 MySQL 文档。

## 标识符长度限制

| 标识符类型 | 最大长度（允许的字符数） |
|:---------|:--------------|
| Database | 64 |
| Table    | 64 |
| Column   | 64 |
| Index    | 64 |
| View     | 64 |
| Sequence | 64 |

## 数据库、表、视图和连接总数限制

| 类型       | 最大数量  |
|:----------|:----------|
| Databases | unlimited |
| Tables    | unlimited |
| Views     | unlimited |
| Connections | unlimited |

## 单个数据库的限制

| 类型       | 上限   |
|:----------|:----------|
| Tables    | unlimited  |

## 单个表的限制

| 类型       | 上限（默认值）  |
|:----------|:----------|
| Columns   | 默认为 1017，可调整至 4096     |
| Indexes   | 默认为 64，可调整至 512        |
| Rows      | unlimited |
| Size      | unlimited |
| Partitions | 8192     |

<CustomContent platform="tidb">

* `Columns` 的上限可以通过 [`table-column-count-limit`](/tidb-configuration-file.md#table-column-count-limit-new-in-v50) 修改。
* `Indexes` 的上限可以通过 [`index-limit`](/tidb-configuration-file.md#index-limit-new-in-v50) 修改。

</CustomContent>

## 单行的限制

| 类型       | 上限（默认值）   |
|:----------|:----------|
| Size       | 默认为 6 MiB，可调整至 120 MiB  |

<CustomContent platform="tidb">

你可以通过 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v4010-and-v500) 配置项调整大小限制。

</CustomContent>

## 索引的限制

最大索引长度为 3072 字节，相当于使用 4 字节 UTF-8 编码的 768 个字符。单个索引中的最大列数限制为 16。

<CustomContent platform="tidb">

你可以使用 [`max-index-length`](/tidb-configuration-file.md#max-index-length) 配置项调整此限制。

</CustomContent>

## 数据类型的限制

| 类型       | 上限   |
|:----------|:----------|
| CHAR       | 255 字符      |
| BINARY     | 255 字符      |
| VARBINARY  | 65535 字符    |
| VARCHAR    | 16383 字符    |
| TEXT       | 默认为 6 MiB，可调整至 120 MiB                |
| BLOB       | 默认为 6 MiB，可调整至 120 MiB               |

## SQL 语句的限制

| 类型       | 上限   |
|:----------|:----------|
| 单个事务中最大 SQL 语句数 | 当使用乐观事务且启用事务重试时，上限为 5000。 |

<CustomContent platform="tidb">

你可以通过 [`stmt-count-limit`](/tidb-configuration-file.md#stmt-count-limit) 配置项修改此限制。

</CustomContent>

## TiKV 版本的限制

在你的集群中，如果 TiDB 组件的版本为 v6.2.0 或更高，则 TiKV 的版本必须为 v6.2.0 或更高。