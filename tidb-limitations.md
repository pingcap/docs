---
title: TiDB 限制
summary: 了解 TiDB 的使用限制。
---

# TiDB 限制

本文档描述了 TiDB 的常见使用限制，包括标识符最大长度、支持的数据库、表、索引、分区表和序列的最大数量。

> **Note:**
>
> TiDB 对 MySQL 协议和语法具有高度兼容性，也包括许多 MySQL 的限制。例如，单个索引最多可以包含 16 列。更多信息请参见 [MySQL 兼容性](/mysql-compatibility.md) 及官方 MySQL 文档。

## 标识符长度限制

| 标识符类型 | 最大长度（允许的字符数） |
|:---------|:--------------|
| 数据库   | 64 |
| 表       | 64 |
| 列       | 64 |
| 索引     | 64 |
| 视图     | 64 |
| 序列     | 64 |

## 数据库、表、视图和连接总数限制

| 类型  | 最大数量  |
|:----------|:----------|
| 数据库   | 无限制 |
| 表       | 无限制 |
| 视图     | 无限制 |
| 连接     | 无限制 |

## 单个数据库的限制

| 类型       | 上限   |
|:----------|:----------|
| 表        | 无限制  |

## 单个表的限制

| 类型       | 上限（默认值）  |
|:----------|:----------|
| 列        | 默认 1017，可调整至 4096     |
| 索引      | 默认 64，可调整至 512        |
| 行数      | 无限制 |
| 大小      | 无限制 |
| 分区数    | 8192     |

<CustomContent platform="tidb">

* `列` 的上限可以通过 [`table-column-count-limit`](/tidb-configuration-file.md#table-column-count-limit-new-in-v50) 配置项进行修改。
* `索引` 的上限可以通过 [`index-limit`](/tidb-configuration-file.md#index-limit-new-in-v50) 配置项进行修改。

</CustomContent>

## 单行的限制

| 类型       | 上限（默认值）   |
|:----------|:----------|
| 大小      | 默认 6 MiB，可调整至 120 MiB  |

<CustomContent platform="tidb">

你可以通过 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v4010-and-v500) 配置项调整大小限制。

</CustomContent>

## 索引的限制

最大索引长度为 3072 字节，使用 4 字节 UTF-8 编码时相当于 768 个字符。单个索引包含的最大列数为 16。

<CustomContent platform="tidb">

你可以通过 [`max-index-length`](/tidb-configuration-file.md#max-index-length) 配置项调整该限制。

</CustomContent>

## 数据类型的限制

| 类型       | 上限   |
|:----------|:----------|
| CHAR       | 255 个字符      |
| BINARY     | 255 字节      |
| VARBINARY  | 65535 字节    |
| VARCHAR    | 16383 个字符    |
| TEXT       | 65535 字节    |
| BLOB       | 65535 字节    |

## SQL 语句的限制

| 类型       | 上限   |
|:----------|:----------|
| 单个事务中的 SQL 语句最大数量 | 当使用乐观事务并启用事务重试时，上限为 5000。 |

<CustomContent platform="tidb">

你可以通过 [`stmt-count-limit`](/tidb-configuration-file.md#stmt-count-limit) 配置项修改该限制。

</CustomContent>

## TiKV 版本的限制

在你的集群中，如果 TiDB 组件的版本为 v6.2.0 或更高，则 TiKV 的版本必须为 v6.2.0 或更高。