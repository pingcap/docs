---
title: TiDB 数据库模式设计概述
summary: 了解 TiDB 数据库模式设计的基础知识。
---

# TiDB 数据库模式设计概述

本文档提供了 TiDB 数据库模式设计的基础知识，包括 TiDB 中的对象、访问控制、数据库模式变更以及对象限制。

在后续的文档中，[Bookshop](/develop/dev-guide-bookshop-schema-design.md) 将作为示例，向你展示如何设计数据库以及在数据库中进行数据读写操作。

## TiDB 中的对象

为区分一些常用术语，以下是对 TiDB 中使用术语的简要说明：

- 为避免与通用术语 [database](https://en.wikipedia.org/wiki/Database) 混淆，本文档中的 **database** 指的是逻辑对象，**TiDB** 指的是 TiDB 本身，**cluster** 指的是部署的 TiDB 实例。

- TiDB 使用与 MySQL 兼容的语法，其中 **schema** 表示通用术语 [schema](https://en.wiktionary.org/wiki/schema)，而不是数据库中的逻辑对象。更多信息请参见 [MySQL 文档](https://dev.mysql.com/doc/refman/8.0/en/create-database.html)。如果你从具有逻辑对象 schema 的数据库迁移（例如 [PostgreSQL](https://www.postgresql.org/docs/current/ddl-schemas.html)、[Oracle](https://docs.oracle.com/en/database/oracle/oracle-database/21/tdddg/creating-managing-schema-objects.html)、[Microsoft SQL Server](https://docs.microsoft.com/en-us/sql/relational-databases/security/authentication-access/create-a-database-schema?view=sql-server-ver15)），请务必注意这一差异。

### Database

TiDB 中的 database 是一组对象的集合，例如表和索引。

TiDB 默认带有一个名为 `test` 的 database。然而，建议你创建自己的 database，而不是使用 `test`。

### Table

Table 是在 [database](#database) 中相关数据的集合。

每个 table 由 **rows** 和 **columns** 组成。每行中的每个值属于特定的 **column**。每个 column 只允许一种数据类型。为了进一步限定列，可以添加一些 [constraints](/constraints.md)。为了加快计算速度，可以添加 [generated columns](/generated-columns.md)。

### Index

Index 是 table 中选定列的副本。你可以使用一个或多个列创建索引。通过索引，TiDB 可以快速定位数据，而不必每次都搜索 table 中的每一行，从而大大提高查询性能。

常见的索引类型有：

- **Primary Key**：在主键列上的索引。
- **Secondary Index**：在非主键列上的索引。

> **Note:**
>
> 在 TiDB 中，**Primary Key** 的默认定义与 [InnoDB](https://dev.mysql.com/doc/refman/8.0/en/innodb-storage-engine.html)（MySQL 常用存储引擎）中的定义不同。
>
> - 在 InnoDB 中，**Primary Key** 是唯一的、非空的，并且是 **clustered index**。
> - 在 TiDB 中，**Primary Key** 是唯一的、非空的，但不保证是 **clustered index**。如果要指定主键是否为聚簇索引，可以在 `CREATE TABLE` 语句中在 `PRIMARY KEY` 后添加非保留关键字 `CLUSTERED` 或 `NONCLUSTERED`。如果语句未明确指定这些关键字，默认行为由系统变量 `@@global.tidb_enable_clustered_index` 控制。更多信息请参见 [Clustered Indexes](/clustered-indexes.md)。

#### 专用索引

<CustomContent platform="tidb">

为了提升各种用户场景下的查询性能，TiDB 提供了一些专用类型的索引。每种类型的详细信息，请参见 [Indexing and constraints](/basic-features.md#indexing-and-constraints)。

</CustomContent>

<CustomContent platform="tidb-cloud">

为了提升各种用户场景下的查询性能，TiDB 提供了一些专用类型的索引。每种类型的详细信息，请参见 [Indexing and constraints](https://docs.pingcap.com/tidb/stable/basic-features#indexing-and-constraints)。

</CustomContent>

### 其他支持的逻辑对象

TiDB 支持以下与 **table** 同级的逻辑对象：

- [View](/views.md)：视图作为虚拟表，其 schema 由创建视图的 `SELECT` 语句定义。
- [Sequence](/sql-statements/sql-statement-create-sequence.md)：序列用于生成和存储连续的数据。
- [Temporary table](/temporary-tables.md)：临时表，其数据不持久化。

## 访问控制

<CustomContent platform="tidb">

TiDB 支持基于用户和基于角色的访问控制。为了允许用户查看、修改或删除数据对象和数据 schema，你可以直接授予 [privileges](/privilege-management.md) 给 [users](/user-account-management.md)，或者通过 [roles](/role-based-access-control.md) 授予 [privileges](/privilege-management.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB 支持基于用户和基于角色的访问控制。为了允许用户查看、修改或删除数据对象和数据 schema，你可以直接授予 [privileges](https://docs.pingcap.com/tidb/stable/privilege-management) 给 [users](https://docs.pingcap.com/tidb/stable/user-account-management)，或者通过 [roles](https://docs.pingcap.com/tidb/stable/role-based-access-control) 授予 [privileges](https://docs.pingcap.com/tidb/stable/privilege-management)。

</CustomContent>

## 数据库模式变更

作为最佳实践，建议你使用 [MySQL 客户端](https://dev.mysql.com/doc/refman/8.0/en/mysql.html) 或图形界面客户端，而非驱动或 ORM 来执行数据库模式变更。

## 对象限制

更多信息请参见 [TiDB Limitations](/tidb-limitations.md)。

## 需要帮助？

<CustomContent platform="tidb">

可以在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或者 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

可以在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或者 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>