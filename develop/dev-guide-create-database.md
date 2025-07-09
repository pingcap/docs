---
title: 创建数据库
summary: 了解创建数据库的步骤、规则和示例。
---

# 创建数据库

本文档介绍了如何使用 SQL 及各种编程语言创建数据库，并列出了数据库创建的规则。在本文档中，以 [Bookshop](/develop/dev-guide-bookshop-schema-design.md) 应用为例，带你了解数据库创建的步骤。

## 在开始之前

在创建数据库之前，请完成以下操作：

- [构建一个 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md)。
- 阅读 [Schema Design Overview](/develop/dev-guide-schema-design-overview.md)。

## 什么是数据库

TiDB 中的 [数据库](/develop/dev-guide-schema-design-overview.md) 对象包括 **tables**、**views**、**sequences** 以及其他对象。

## 创建数据库

要创建数据库，可以使用 `CREATE DATABASE` 语句。

例如，若要创建一个名为 `bookshop` 的数据库（如果不存在），请使用以下语句：

```sql
CREATE DATABASE IF NOT EXISTS `bookshop`;
```

关于 `CREATE DATABASE` 语句的更多信息和示例，请参见 [`CREATE DATABASE`](/sql-statements/sql-statement-create-database.md)。

若要以 `root` 用户执行建库语句，请运行以下命令：

```shell
mysql
    -u root \
    -h {host} \
    -P {port} \
    -p {password} \
    -e "CREATE DATABASE IF NOT EXISTS bookshop;"
```

## 查看数据库

要查看集群中的数据库，可以使用 [`SHOW DATABASES`](/sql-statements/sql-statement-show-databases.md) 语句。

例如：

```shell
mysql
    -u root \
    -h {host} \
    -P {port} \
    -p {password} \
    -e "SHOW DATABASES;"
```

以下是示例输出：

```
+--------------------+
| Database           |
+--------------------+
| INFORMATION_SCHEMA |
| PERFORMANCE_SCHEMA |
| bookshop           |
| mysql              |
| test               |
+--------------------+
```

## 数据库创建规则

- 遵循 [Database Naming Conventions](/develop/dev-guide-object-naming-guidelines.md)，并为你的数据库取有意义的名字。
- TiDB 默认带有一个名为 `test` 的数据库，但不建议在生产环境中使用它，除非必要。你可以使用 `CREATE DATABASE` 语句创建自己的数据库，并在 SQL 会话中使用 [`USE {databasename};`](/sql-statements/sql-statement-use.md) 语句切换当前数据库。
- 使用 `root` 用户创建对象（如数据库、角色和用户）。只授予角色和用户必要的权限。
- 作为最佳实践，建议你使用 **MySQL 命令行客户端** 或 **MySQL 图形界面客户端**，而不是驱动或 ORM 来执行数据库架构变更。

## 下一步

创建数据库后，你可以向其中添加 **tables**。更多信息请参见 [Create a Table](/develop/dev-guide-create-table.md)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>