---
title: ADMIN CLEANUP INDEX
summary: 关于 TiDB 数据库中 ADMIN CLEANUP 的使用概述。
---

# ADMIN CLEANUP INDEX

`ADMIN CLEANUP INDEX` 语句用于删除表中冗余的索引，当表存在不一致的数据和索引时。注意，该语法目前尚不支持 [foreign key constraints](/foreign-key.md)。

## 概述

```ebnf+diagram
AdminCleanupStmt ::=
    'ADMIN' 'CLEANUP' ( 'INDEX' TableName IndexName | 'TABLE' 'LOCK' TableNameList )

TableNameList ::=
    TableName ( ',' TableName )*
```

## 示例

假设某个数据库中的 `tbl` 表由于某些原因（例如，在灾难恢复场景中集群中部分行数据丢失）导致数据和索引不一致：

```sql
SELECT * FROM tbl;
ERROR 1105 (HY000): inconsistent index idx handle count 3 isn't equal to value count 2

ADMIN CHECK INDEX tbl idx ;
ERROR 1105 (HY000): handle &kv.CommonHandle{encoded:[]uint8{0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xf8}, colEndOffsets:[]uint16{0xa}}, index:types.Datum{k:0x5, decimal:0x0, length:0x0, i:0, collation:"utf8mb4_bin", b:[]uint8{0x0}, x:interface {}(nil)} != record:<nil>
```

从 `SELECT` 查询的错误信息可以看出，`tbl` 表中存在两行数据和三行索引数据，说明行数据和索引数据不一致。同时，至少有一个索引处于悬挂状态。在这种情况下，可以使用 `ADMIN CLEANUP INDEX` 语句删除悬挂的索引：

```sql
ADMIN CLEANUP INDEX tbl idx;
```

执行结果如下：

```sql
ADMIN CLEANUP INDEX tbl idx;
+---------------+
| REMOVED_COUNT |
+---------------+
|             1 |
+---------------+
```

你可以再次执行 `ADMIN CHECK INDEX` 语句，检查数据和索引的一致性，确认数据是否已恢复到正常状态：

```sql
ADMIN CHECK INDEX tbl idx;
Query OK, 0 rows affected (0.01 sec)
```

<CustomContent platform="tidb">

> **Note:**
>
> 当由于副本丢失导致数据和索引不一致时：
>
> - 可能会同时丢失行数据和索引数据。为恢复一致性，可以结合使用 `ADMIN CLEANUP INDEX` 和 [`ADMIN RECOVER INDEX`](/sql-statements/sql-statement-admin-recover.md) 语句。
> - `ADMIN CLEANUP INDEX` 语句始终在单线程中执行。当表数据较大时，建议通过重建索引来恢复索引数据。
> - 执行 `ADMIN CLEANUP INDEX` 时，相关的表或索引不会被锁定，TiDB 允许其他会话同时修改表记录。但在这种情况下，`ADMIN CLEANUP INDEX` 可能无法正确处理所有表记录。因此，执行时应避免同时修改表数据。
> - 如果你使用 TiDB 企业版，可以 [提交请求](/support.md) 联系技术支持获取帮助。
>
> `ADMIN CLEANUP INDEX` 语句不是原子操作：如果在执行过程中被中断，建议重新执行直到成功。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> 当由于副本丢失导致数据和索引不一致时：
>
> - 可能会同时丢失行数据和索引数据。为恢复一致性，可以结合使用 `ADMIN CLEANUP INDEX` 和 [`ADMIN RECOVER INDEX`](/sql-statements/sql-statement-admin-recover.md) 语句。
> - `ADMIN CLEANUP INDEX` 语句始终在单线程中执行。当表数据较大时，建议通过重建索引来恢复索引数据。
> - 执行 `ADMIN CLEANUP INDEX` 时，相关的表或索引不会被锁定，TiDB 允许其他会话同时修改表记录。但在这种情况下，`ADMIN CLEANUP INDEX` 可能无法正确处理所有表记录。因此，执行时应避免同时修改表数据。
> - 如果你使用 TiDB 企业版，可以 [提交请求](https://tidb.support.pingcap.com/) 联系技术支持获取帮助。
>
> `ADMIN CLEANUP INDEX` 语句不是原子操作：如果在执行过程中被中断，建议重新执行直到成功。

</CustomContent>

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 相关链接

* [`ADMIN CHECK TABLE/INDEX`](/sql-statements/sql-statement-admin-check-table-index.md)
* [`ADMIN RECOVER INDEX`](/sql-statements/sql-statement-admin-recover.md)
