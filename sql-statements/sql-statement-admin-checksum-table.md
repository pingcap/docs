---
title: ADMIN CHECKSUM TABLE | TiDB SQL 语句参考
summary: 关于 TiDB 数据库中 ADMIN 的用法概述。
category: reference
---

# ADMIN CHECKSUM TABLE

`ADMIN CHECKSUM TABLE` 语句用于计算表的数据和索引的 CRC64 校验和。

<CustomContent platform="tidb">

[checksum](/tidb-lightning/tidb-lightning-glossary.md#checksum) 是基于表数据及其属性（如 `table_id`）计算得出的。这意味着即使两个表的数据相同，但 `table_id` 不同，它们的校验和也会不同。

在使用 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)、[TiDB Data Migration](/dm/dm-overview.md) 或 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 导入表后，默认会执行 `ADMIN CHECKSUM TABLE <table>` 以验证数据完整性。

</CustomContent>

<CustomContent platform="tidb-cloud">

[checksum](https://docs.pingcap.com/tidb/stable/tidb-lightning-glossary#checksum) 是基于表数据及其属性（如 `table_id`）计算得出的。这意味着即使两个表的数据相同，但 `table_id` 不同，它们的校验和也会不同。

在使用 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 导入表后，默认会执行 `ADMIN CHECKSUM TABLE <table>` 以验证数据完整性。

</CustomContent>

## 概要

```ebnf+diagram
AdminChecksumTableStmt ::=
    'ADMIN' 'CHECKSUM' 'TABLE' TableNameList

TableNameList ::=
    TableName ( ',' TableName )*
```

## 示例

创建表 `t1`：

```sql
CREATE TABLE t1(id INT PRIMARY KEY);
```

向 `t1` 插入一些数据：

```sql
INSERT INTO t1 VALUES (1),(2),(3);
```

计算 `t1` 的校验和：

```sql
ADMIN CHECKSUM TABLE t1;
```

输出结果如下：

```sql
+---------+------------+----------------------+-----------+-------------+
| Db_name | Table_name | Checksum_crc64_xor   | Total_kvs | Total_bytes |
+---------+------------+----------------------+-----------+-------------+
| test    | t1         | 10909174369497628533 |         3 |          75 |
+---------+------------+----------------------+-----------+-------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。