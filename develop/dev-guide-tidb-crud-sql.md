---
title: CRUD SQL in TiDB
summary: 对 TiDB 的 CRUD SQL 的简要介绍。
---

# CRUD SQL in TiDB

本文档简要介绍如何使用 TiDB 的 CRUD SQL。

## 在开始之前

请确保你已连接到一个 TiDB 集群。如果没有，参考 [Build a {{{ .starter }}} Cluster](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-tidb-cloud-cluster) 来创建一个 {{{ .starter }}} 集群。

## 使用 TiDB 探索 SQL

> **Note:**
>
> 本文档引用并简化了 [Explore SQL with TiDB](/basic-sql-operations.md)。更多详情请参见 [Explore SQL with TiDB](/basic-sql-operations.md)。

TiDB 兼容 MySQL，在大多数情况下你可以直接使用 MySQL 语句。对于不支持的功能，请参见 [Compatibility with MySQL](/mysql-compatibility.md#unsupported-features)。

为了试验 SQL 并测试 TiDB 与 MySQL 查询的兼容性，你可以尝试 [TiDB Playground](https://play.tidbcloud.com/?utm_source=docs&utm_medium=basic-sql-operations)。你也可以先部署一个 TiDB 集群，然后在其中运行 SQL 语句。

本页面将引导你了解基本的 TiDB SQL 语句，如 DDL、DML 和 CRUD 操作。完整的 TiDB 语句列表，请参见 [SQL Statement Overview](/sql-statements/sql-statement-overview.md)。

## 分类

根据功能，SQL 分为以下 4 种类型：

- **DDL (Data Definition Language)**：用于定义数据库对象，包括数据库、表、视图和索引。

- **DML (Data Manipulation Language)**：用于操作应用相关的记录。

- **DQL (Data Query Language)**：用于在条件过滤后查询记录。

- **DCL (Data Control Language)**：用于定义访问权限和安全级别。

以下主要介绍 DML 和 DQL。关于 DDL 和 DCL 的更多信息，请参见 [Explore SQL with TiDB](/basic-sql-operations.md) 或 [SQL Statement Overview](/sql-statements/sql-statement-overview.md)。

## 数据操作语言

常见的 DML 功能包括添加、修改和删除表中的记录。对应的命令是 `INSERT`、`UPDATE` 和 `DELETE`。

向表中插入数据，使用 `INSERT` 语句：

```sql
INSERT INTO person VALUES(1,'tom','20170912');
```

向表中插入包含部分字段数据的记录，使用 `INSERT` 语句：

```sql
INSERT INTO person(id,name) VALUES('2','bob');
```

更新表中某条记录的部分字段，使用 `UPDATE` 语句：

```sql
UPDATE person SET birthday='20180808' WHERE id=2;
```

删除表中的数据，使用 `DELETE` 语句：

```sql
DELETE FROM person WHERE id=2;
```

> **Note:**
>
> 不带 `WHERE` 条件的 `UPDATE` 和 `DELETE` 语句会对整个表操作。

## 数据查询语言

DQL 用于从表或多个表中检索所需的数据行。

查看表中的数据，使用 `SELECT` 语句：

```sql
SELECT * FROM person;
```

查询特定列，添加列名到 `SELECT` 关键字后：

```sql
SELECT name FROM person;
```

结果如下：

```
+------+
| name |
+------+
| tom  |
+------+
1 rows in set (0.00 sec)
```

使用 `WHERE` 条件过滤所有匹配条件的记录，然后返回结果：

```sql
SELECT * FROM person WHERE id < 5;
```

## 需要帮助吗？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>