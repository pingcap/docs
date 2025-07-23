---
title: SQL Development Specifications
summary: 了解 TiDB 的 SQL 开发规范。
---

# SQL Development Specifications

本文档介绍一些使用 SQL 的通用开发规范。

## 创建和删除表

- 基本原则：在遵循表命名规范的前提下，建议应用内部封装表创建和删除语句，并添加判断逻辑，以防止业务流程异常中断。
- 细节：建议在 `create table if not exists table_name` 或 `drop table if exists table_name` 语句中添加 `if` 判断，避免 SQL 命令在应用端异常运行导致的中断。

## `SELECT *` 使用

- 基本原则：避免使用 `SELECT *` 进行查询。
- 细节：根据需要选择合适的列，避免使用 `SELECT *` 读取所有字段，因为此类操作会消耗网络带宽。可以考虑将查询字段加入索引，以充分利用覆盖索引。

## 在字段上使用函数

- 基本原则：可以在查询字段上使用相关函数。为了避免索引失效，不要在 `WHERE` 子句中过滤字段上使用任何函数，包括数据类型转换函数。可以考虑使用表达式索引。
- 详细描述：

    不推荐：

    
    ```sql
    SELECT gmt_create
    FROM ...
    WHERE DATE_FORMAT(gmt_create, '%Y%m%d %H:%i:%s') = '20090101 00:00:00'
    ```

    推荐：

    
    ```sql
    SELECT DATE_FORMAT(gmt_create, '%Y%m%d %H:%i:%s')
    FROM ...
    WHERE gmt_create = str_to_date('20090101 00:00:00', '%Y%m%d %H:%i:%s')
    ```

## 其他规范

- 不要在 `WHERE` 条件中对索引列进行数学运算或函数操作。
- 将 `OR` 替换为 `IN` 或 `UNION`。`IN` 的数量必须少于 `300`。
- 避免使用 `%` 前缀进行模糊前缀查询。
- 如果应用使用 **Multi Statements** 执行 SQL，即多个 SQL 语句用分号连接并一次性发送给客户端执行，TiDB 只会返回第一个 SQL 的结果。
- 使用表达式时，检查表达式是否支持下推计算到存储层（TiKV 或 TiFlash）。如果不支持，可能会导致更多内存消耗甚至在 TiDB 层出现 OOM。支持下推计算的内容包括：
    - [TiFlash supported push-down calculations](/tiflash/tiflash-supported-pushdown-calculations.md)。
    - [TiKV - List of Expressions for Pushdown](/functions-and-operators/expressions-pushed-down.md)。
    - [Predicate push down](/predicate-push-down.md)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>