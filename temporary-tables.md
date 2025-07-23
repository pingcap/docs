---
title: 临时表
summary: 了解 TiDB 中的临时表功能，学习如何使用临时表存储应用的中间数据，有助于减少表管理开销并提升性能。
---

# 临时表

临时表功能在 TiDB v5.3.0 中引入。该功能解决了临时存储应用中间结果的问题，免去了频繁创建和删除表的繁琐。你可以将中间计算数据存放在临时表中。当中间数据不再需要时，TiDB 会自动清理和回收临时表。这避免了用户应用过于复杂，减少了表管理的开销，并提升了性能。

本文介绍了用户场景和临时表的类型，提供了使用示例及限制临时表内存使用的方法，并说明了与其他 TiDB 功能的兼容性限制。

## 用户场景

你可以在以下场景中使用 TiDB 临时表：

- 缓存应用的中间临时数据。计算完成后，将数据导出到普通表，临时表会自动释放。
- 在短时间内对同一数据进行多次 DML 操作。例如，在电商购物车应用中，添加、修改、删除商品，完成支付，以及删除购物车信息。
- 快速批量导入中间临时数据，以提升导入临时数据的性能。
- 批量更新数据。批量导入数据到临时表，完成修改后导出到文件。

## 临时表的类型

TiDB 中的临时表分为两种：本地临时表和全局临时表。

- 本地临时表，其表定义和表中的数据仅对当前会话可见。适用于在会话中临时存储中间数据。
- 全局临时表，其表定义对整个 TiDB 集群可见，表中的数据仅对当前事务可见。适用于在事务中临时存储中间数据。

## 本地临时表

TiDB 中的本地临时表语义与 MySQL 临时表一致，具有以下特性：

- 本地临时表的表定义不具备持久性。仅对创建该临时表的会话可见，其他会话无法访问。
- 可以在不同会话中创建同名的本地临时表，每个会话只读写自己创建的临时表。
- 本地临时表的数据对会话中的所有事务可见。
- 会话结束后，创建的本地临时表会自动删除。
- 本地临时表可以与普通表同名。在这种情况下，在 DDL 和 DML 语句中，普通表会被隐藏，直到临时表被删除。

要创建本地临时表，可以使用 `CREATE TEMPORARY TABLE` 语句。删除本地临时表，可以使用 `DROP TABLE` 或 `DROP TEMPORARY TABLE` 语句。

不同于 MySQL，TiDB 中的本地临时表全部为外部表，执行 SQL 语句时不会自动创建内部临时表。

### 本地临时表的使用示例

> **注意：**
>
> - 在使用 TiDB 临时表之前，请注意 [与其他 TiDB 功能的兼容性限制](#compatibility-restrictions-with-other-tidb-features) 和 [与 MySQL 临时表的兼容性](#compatibility-with-mysql-temporary-tables)。
> - 如果你在 TiDB v5.3.0 之前的集群上创建了本地临时表，这些表实际上是普通表，升级到 TiDB v5.3.0 或更高版本后，仍作为普通表处理。

假设存在一个普通表 `users`：

```sql
CREATE TABLE users (
    id BIGINT,
    name VARCHAR(100),
    PRIMARY KEY(id)
);
```

在会话 A 中，创建一个本地临时表 `users` 不会与普通表 `users` 冲突。当会话 A 访问 `users` 表时，访问的是本地临时表 `users`。

```sql
CREATE TEMPORARY TABLE users (
    id BIGINT,
    name VARCHAR(100),
    city VARCHAR(50),
    PRIMARY KEY(id)
);
```

```
Query OK, 0 rows affected (0.01 sec)
```

如果向 `users` 插入数据，数据会存入会话 A 中的本地临时表 `users`。

```sql
INSERT INTO users(id, name, city) VALUES(1001, 'Davis', 'LosAngeles');
```

```
Query OK, 1 row affected (0.00 sec)
```

```sql
SELECT * FROM users;
```

```
+------+-------+------------+
| id   | name  | city       |
+------+-------+------------+
| 1001 | Davis | LosAngeles |
+------+-------+------------+
1 row in set (0.00 sec)
```

在会话 B 中，创建一个本地临时表 `users` 不会与普通表 `users` 或会话 A 中的临时表冲突。当会话 B 访问 `users` 时，访问的是会话 B 中的本地临时表。

```sql
CREATE TEMPORARY TABLE users (
    id BIGINT,
    name VARCHAR(100),
    city VARCHAR(50),
    PRIMARY KEY(id)
);
```

```
Query OK, 0 rows affected (0.01 sec)
```

向 `users` 插入数据，数据存入会话 B 中的临时表。

```sql
INSERT INTO users(id, name, city) VALUES(1001, 'James', 'NewYork');
```

```
Query OK, 1 row affected (0.00 sec)
```

```sql
SELECT * FROM users;
```

```
+------+-------+---------+
| id   | name  | city    |
+------+-------+---------+
| 1001 | James | NewYork |
+------+-------+---------+
1 row in set (0.00 sec)
```

### 与 MySQL 临时表的兼容性

TiDB 本地临时表的以下特性和限制与 MySQL 临时表相同：

- 创建或删除本地临时表时，当前事务不会自动提交。
- 删除临时表所在的 schema 后，临时表不会被删除，仍然可读写。
- 创建本地临时表需要 `CREATE TEMPORARY TABLES` 权限，之后的所有操作不需要权限。
- 本地临时表不支持外键和分区表。
- 不支持基于本地临时表创建视图。
- `SHOW [FULL] TABLES` 不显示本地临时表。

TiDB 中的本地临时表在以下方面与 MySQL 临时表不兼容：

- TiDB 本地临时表不支持 `ALTER TABLE`。
- TiDB 本地临时表忽略 `ENGINE` 表选项，始终将临时表数据存储在 TiDB 内存中（[限制临时表内存使用](#limit-the-memory-usage-of-temporary-tables)）。
- 当声明 `MEMORY` 作为存储引擎时，TiDB 本地临时表不受 `MEMORY` 存储引擎限制。
- 当声明 `INNODB` 或 `MYISAM` 作为存储引擎时，TiDB 本地临时表会忽略 InnoDB 临时表的系统变量。
- MySQL 不允许在同一 SQL 语句中多次引用同一临时表，TiDB 本地临时表没有此限制。
- MySQL 中显示临时表的系统表 `information_schema.INNODB_TEMP_TABLE_INFO` 在 TiDB 中不存在。目前，TiDB 也没有显示本地临时表的系统表。
- TiDB 没有内部临时表，MySQL 中关于内部临时表的系统变量在 TiDB 中不生效。

## 全局临时表

全局临时表是 TiDB 的扩展，其特性如下：

- 全局临时表的表定义具备持久性，对所有会话可见。
- 全局临时表的数据仅在当前事务中可见。事务结束后，数据会自动清除。
- 全局临时表不能与普通表同名。

创建全局临时表，可以使用 `CREATE GLOBAL TEMPORARY TABLE` 语句，后跟 `ON COMMIT DELETE ROWS`。删除全局临时表，可以使用 `DROP TABLE` 或 `DROP GLOBAL TEMPORARY TABLE`。

### 全局临时表的使用示例

> **注意：**
>
> - 在使用 TiDB 临时表之前，请注意 [与其他 TiDB 功能的兼容性限制](#compatibility-restrictions-with-other-tidb-features)。
> - 如果你在 v5.3.0 及以上版本的 TiDB 集群上创建了全局临时表，当集群降级到 v5.3.0 以下版本时，这些表会被当作普通表处理。在这种情况下，会发生数据错误。

在会话 A 中创建一个全局临时表 `users`：

```sql
CREATE GLOBAL TEMPORARY TABLE users (
    id BIGINT,
    name VARCHAR(100),
    city VARCHAR(50),
    PRIMARY KEY(id)
) ON COMMIT DELETE ROWS;
```

```
Query OK, 0 rows affected (0.01 sec)
```

写入 `users` 的数据在当前事务中可见：

```sql
BEGIN;
```

```
Query OK, 0 rows affected (0.00 sec)
```


```sql
INSERT INTO users(id, name, city) VALUES(1001, 'Davis', 'LosAngeles');
```

```
Query OK, 1 row affected (0.00 sec)
```


```sql
SELECT * FROM users;
```

```
+------+-------+------------+
| id   | name  | city       |
+------+-------+------------+
| 1001 | Davis | LosAngeles |
+------+-------+------------+
1 row in set (0.00 sec)
```

事务结束后，数据会自动清除：

```sql
COMMIT;
```

```
Query OK, 0 rows affected (0.00 sec)
```


```sql
SELECT * FROM users;
```

```
Empty set (0.00 sec)
```

在会话 A 中创建 `users` 后，会话 B 也可以读写该表：

```sql
SELECT * FROM users;
```

```
Empty set (0.00 sec)
```

> **注意：**
>
> 如果事务是自动提交的，SQL 执行后，插入的数据会自动清除，后续 SQL 无法访问。因此，建议使用非自动提交事务来读写全局临时表。

## 限制临时表的内存使用

无论声明哪种存储引擎，定义表时，本地临时表和全局临时表的数据都只存储在 TiDB 实例的内存中，不会持久化。

为了避免内存溢出，可以使用 [`tidb_tmp_table_max_size`](/system-variables.md#tidb_tmp_table_max_size-new-in-v530) 系统变量限制每个临时表的大小。一旦临时表超过该阈值，TiDB 会报错。`tidb_tmp_table_max_size` 的默认值为 `64MB`。

例如，将临时表最大大小设置为 `256MB`：

```sql
SET GLOBAL tidb_tmp_table_max_size=268435456;
```

## 与其他 TiDB 功能的兼容性限制

TiDB 中的本地临时表和全局临时表**不**兼容以下 TiDB 功能：

- `AUTO_RANDOM` 列
- `SHARD_ROW_ID_BITS` 和 `PRE_SPLIT_REGIONS` 表选项
- 分区表
- `SPLIT REGION` 语句
- `ADMIN CHECK TABLE` 和 `ADMIN CHECKSUM TABLE` 语句
- `FLASHBACK TABLE` 和 `RECOVER TABLE` 语句
- 基于临时表执行 `CREATE TABLE LIKE`
- Stale Read
- 外键
- SQL 绑定
- TiFlash 副本
- 在临时表上创建视图
- Placement Rules
- 涉及临时表的执行计划不会被 `prepare plan cache` 缓存。

TiDB 中的本地临时表**不支持**以下功能：

- 使用 `tidb_snapshot` 系统变量读取历史数据。

## TiDB 迁移工具支持

TiDB 迁移工具**不导出**、**不备份**也不**复制**本地临时表，因为这些表仅对当前会话可见。

全局临时表会被导出、备份和复制，因为表定义在全局范围内可见。注意，表中的数据不会被导出。

> **注意：**
>
> - 使用 TiCDC 复制临时表需要 TiCDC v5.3.0 或更高版本，否则下游表的表定义会出错。
> - 使用 BR 备份临时表需要 BR v5.3.0 或更高版本，否则备份的临时表定义会出错。
> - 导出集群、数据恢复后的集群以及复制的下游集群都应支持全局临时表，否则会报错。

## 相关链接

* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [CREATE TABLE LIKE](/sql-statements/sql-statement-create-table-like.md)
* [DROP TABLE](/sql-statements/sql-statement-drop-table.md)